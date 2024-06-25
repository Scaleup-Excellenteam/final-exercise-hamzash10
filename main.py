from presentation_reader import read_pptx
import chatgpt_interaction as gpt
from json_handler import save_to_json
import asyncio
import argparse


async def main():
    parser = argparse.ArgumentParser(description='process a powerpoint (.pptx) file and summarize its content using '
                                                 'chatgpt')
    parser.add_argument('input_pptx', type=str, nargs='?', default='Corona.pptx', help='path to the powerpoint file ('
                                                                                       '.pptx) default is: Corona.pptx')

    args = parser.parse_args()

    slides_content = read_pptx(args.input_pptx)
    slides_summary = await gpt.process_slides(slides_content)
    save_to_json(slides_summary, args.input_pptx)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
