"""
Database Setup Script
Creates required tables in Supabase.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.supabase import get_service_client
from app.utils.logger import setup_logger, logger


# SQL statements for table creation
CREATE_TABLES_SQL = """
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Chat sessions table
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT DEFAULT 'New Conversation',
    summary TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index on user_id for faster queries
CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_updated_at ON chat_sessions(updated_at DESC);

-- Chat messages table
CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for messages
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON chat_messages(created_at);

-- Legal chunks table with vector embedding
CREATE TABLE IF NOT EXISTS legal_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding vector(384),  -- Dimension for all-MiniLM-L6-v2
    act_name TEXT,
    section TEXT,
    chapter TEXT,
    source_url TEXT,
    domain TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for legal chunks
CREATE INDEX IF NOT EXISTS idx_legal_chunks_domain ON legal_chunks(domain);
CREATE INDEX IF NOT EXISTS idx_legal_chunks_act_name ON legal_chunks(act_name);

-- Create vector similarity search index
CREATE INDEX IF NOT EXISTS idx_legal_chunks_embedding ON legal_chunks 
USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Agent logs table for audit
CREATE TABLE IF NOT EXISTS agent_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(id) ON DELETE SET NULL,
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    node_name TEXT NOT NULL,
    input_state JSONB,
    output_state JSONB,
    duration_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_agent_logs_session_id ON agent_logs(session_id);
CREATE INDEX IF NOT EXISTS idx_agent_logs_created_at ON agent_logs(created_at DESC);

-- Function for vector similarity search
CREATE OR REPLACE FUNCTION match_legal_chunks(
    query_embedding vector(384),
    match_threshold float DEFAULT 0.5,
    match_count int DEFAULT 5,
    filter_domain text DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    content TEXT,
    act_name TEXT,
    section TEXT,
    chapter TEXT,
    source_url TEXT,
    domain TEXT,
    metadata JSONB,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        lc.id,
        lc.content,
        lc.act_name,
        lc.section,
        lc.chapter,
        lc.source_url,
        lc.domain,
        lc.metadata,
        1 - (lc.embedding <=> query_embedding) AS similarity
    FROM legal_chunks lc
    WHERE 
        (filter_domain IS NULL OR lc.domain = filter_domain)
        AND 1 - (lc.embedding <=> query_embedding) > match_threshold
    ORDER BY lc.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- RLS Policies
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

-- Users can only see their own sessions
CREATE POLICY "Users can view own sessions" ON chat_sessions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own sessions" ON chat_sessions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own sessions" ON chat_sessions
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own sessions" ON chat_sessions
    FOR DELETE USING (auth.uid() = user_id);

-- Users can only see messages in their sessions
CREATE POLICY "Users can view own messages" ON chat_messages
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM chat_sessions 
            WHERE chat_sessions.id = chat_messages.session_id 
            AND chat_sessions.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert messages in own sessions" ON chat_messages
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM chat_sessions 
            WHERE chat_sessions.id = chat_messages.session_id 
            AND chat_sessions.user_id = auth.uid()
        )
    );

-- Legal chunks are readable by all authenticated users
ALTER TABLE legal_chunks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Authenticated users can read legal chunks" ON legal_chunks
    FOR SELECT TO authenticated USING (true);
"""


def setup_database():
    """Set up database tables and functions."""
    setup_logger()
    logger.info("Starting database setup...")
    
    try:
        # Note: In Supabase, you typically run SQL through the dashboard
        # or use migrations. This script shows what needs to be created.
        
        logger.info("Database setup SQL generated.")
        logger.info("Please run the following SQL in your Supabase SQL Editor:")
        print("\n" + "="*60)
        print(CREATE_TABLES_SQL)
        print("="*60 + "\n")
        
        logger.info("Database setup instructions complete.")
        
    except Exception as e:
        logger.error(f"Setup error: {str(e)}")
        raise


if __name__ == "__main__":
    setup_database()