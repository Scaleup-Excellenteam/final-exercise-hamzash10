import Presentation as presentation
import openAI as gpt
import asyncio

async def main():
    print(await gpt.process_slides(presentation.read_pptx("Corona.pptx")))

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
