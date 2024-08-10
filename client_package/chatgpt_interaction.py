from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import asyncio
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
DEFAULT_TIMEOUT = 10

PROMPT_TEMPLATE = (
    "Hello ChatGPT, I have the following content from a slide in a PowerPoint presentation: \n{slide}\n"
    "Please summarize the key insights from this slide in the best way possible, make it short and straight "
    "to the point."
)
def create_prompt(slide):
    """
    this function creates a prompt for a slide for chatgpt to understand and get the best results

    :param slide: The content of a slide.
    :type slide: str
    :return: A string containing an appropriate prompt for chatgpt
    :rtype: str
    """
    return PROMPT_TEMPLATE.format(slide=slide)

async def ask_and_get_gpt_response(slide):
    """
    Here is where the magic happens, this function sends api call for chatgpt for each slide it gets

    :param slide: The content of a slide.
    :type slide: str
    :return: A string containing the chatgpt response
    :rtype: str
    """
    message = create_prompt(slide)
    try:
        response = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model="gpt-3.5-turbo",
            timeout=DEFAULT_TIMEOUT
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"


async def process_slides(slides):
    """
    gets a list of slides and sends it to chatgpt

    :param slides: The content of the whole PowerPoint presentation
    :type slides: list<str>
    :return: A list containing the chatgpt response
    :rtype: list<str>
    """
    tasks = []
    for slide in slides:
        task = asyncio.create_task(ask_and_get_gpt_response(slide))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)
    return responses
