from presentation_reader import read_pptx
import chatgpt_interaction as gpt
#from json_handler import save_to_json
import asyncio

async def main():
    slides_content = read_pptx("Corona.pptx")
    slides_summary = await gpt.process_slides(slides_content)
    #save_to_json(slides_summary, "Corona.json")

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
