import Presentation as presentation
import openAI as gpt
import asyncio

async def main():
    await gpt.start_connection()

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
