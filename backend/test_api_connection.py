"""
Test script to debug API connection issues with Gemini, OpenRouter, etc.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

async def test_gemini():
    """Test Gemini API connection."""
    print("\n=== Testing Gemini API ===")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("[X] GOOGLE_API_KEY is not set")
        return False
    
    print(f"[OK] GOOGLE_API_KEY found (length: {len(api_key)})")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import HumanMessage
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=api_key,
            temperature=0,
            max_output_tokens=256,
            max_retries=2,
            timeout=30
        )
        
        print("* Sending test message to Gemini...")
        response = await llm.ainvoke([HumanMessage(content="Say 'Hello, I am working!' in 5 words or less.")])
        print(f"[OK] Gemini Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"[X] Gemini Error: {type(e).__name__}: {str(e)}")
        return False


async def test_openrouter():
    """Test OpenRouter API connection."""
    print("\n=== Testing OpenRouter API ===")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("[X] OPENROUTER_API_KEY is not set")
        return False
    
    print(f"[OK] OPENROUTER_API_KEY found (length: {len(api_key)})")
    
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage
        
        llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            model="mistralai/mistral-7b-instruct",
            temperature=0,
            max_tokens=256,
            timeout=30
        )
        
        print("* Sending test message to OpenRouter...")
        response = await llm.ainvoke([HumanMessage(content="Say 'Hello, I am working!' in 5 words or less.")])
        print(f"[OK] OpenRouter Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"[X] OpenRouter Error: {type(e).__name__}: {str(e)}")
        return False


async def test_openai():
    """Test OpenAI API connection."""
    print("\n=== Testing OpenAI API ===")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[X] OPENAI_API_KEY is not set")
        return False
    
    print(f"[OK] OPENAI_API_KEY found (length: {len(api_key)})")
    
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage
        
        llm = ChatOpenAI(
            api_key=api_key,
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=256,
            timeout=30
        )
        
        print("* Sending test message to OpenAI...")
        response = await llm.ainvoke([HumanMessage(content="Say 'Hello, I am working!' in 5 words or less.")])
        print(f"[OK] OpenAI Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"[X] OpenAI Error: {type(e).__name__}: {str(e)}")
        return False


async def main():
    print("=" * 60)
    print("API Connection Test")
    print("=" * 60)
    
    # Check which provider is configured
    provider = os.getenv("LLM_PROVIDER", "gemini")
    print(f"\nConfigured LLM_PROVIDER: {provider}")
    
    results = {}
    
    # Test Gemini
    results["gemini"] = await test_gemini()
    
    # Test OpenRouter
    results["openrouter"] = await test_openrouter()
    
    # Test OpenAI
    results["openai"] = await test_openai()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    for provider, success in results.items():
        status = "[OK] Working" if success else "[X] Failed"
        print(f"  {provider}: {status}")
    
    if not any(results.values()):
        print("\n[!] All API connections failed!")
        print("    Please check your API keys and network connection.")
    else:
        working = [k for k, v in results.items() if v]
        print(f"\n[OK] Working providers: {', '.join(working)}")


if __name__ == "__main__":
    asyncio.run(main())
