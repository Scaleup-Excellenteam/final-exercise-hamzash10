import asyncio
import os
from time import sleep
from presentation_reader import read_pptx
from chatgpt_interaction import process_slides
from json_handler import save_to_json
from Modules import UPLOAD_FOLDER, OUTPUT_FOLDER



# make the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# make the outputs directory if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


async def run_explainer():
    """
    runs indefinably and search for new PowerPoint files that hasn't yet been explained, sends them
    to chatgpt and saves the response into jsonfile
    """
    while True:
        for filename in os.listdir(UPLOAD_FOLDER):
            if (filename[:-5]+".json") not in os.listdir(OUTPUT_FOLDER):
                print("DEBUGGING: processing file: " + filename.split('_')[0] + '.pptx')
                upload_file_path = os.path.join(UPLOAD_FOLDER, filename)
                slides_content = read_pptx(upload_file_path)
                slides_summary = await process_slides(slides_content)
                output_file_path = os.path.join(OUTPUT_FOLDER, filename[:-5] + ".json")
                save_to_json(slides_summary, output_file_path)
                print("DEBUGGING: finished processing file and saved in 'output' Directory as: " + filename[:-5] + ".json")

        sleep(10)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_explainer())
