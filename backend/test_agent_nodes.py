
import asyncio
import sys
import os
sys.path.append(os.getcwd())

from app.agent.nodes import intake_node, classify_node
from app.agent.state import create_initial_state
from app.llm.router import get_llm

async def test():
    try:
        print('Initializing LLM...')
        llm = get_llm()
        print('LLM Initialized.')

        state = create_initial_state('I bought a phone online and it is defective', 'test_session', 'test_user')
        print('State created.')

        print('Running intake_node...')
        state = await intake_node(state, llm)
        print('Intake node finished.')
        
        print('Running classify_node...')
        state = await classify_node(state, llm)
        print('Classify node finished.')
        print('Classification:', state['classification'])
    except Exception as e:
        print('Error:', e)
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(test())

