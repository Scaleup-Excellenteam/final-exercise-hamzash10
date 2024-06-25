from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def creat_prompt(slide):
    """
    this function creates a prompt for a slide for chatgpt to understand and get the best results

    :param slide: The content of a slide.
    :type slide: str
    :return: A string containing an appropriate prompt for chatgpt
    :rtype: str
    """
    return (f"Hello ChatGPT, I have the following content from a slide in a PowerPoint presentation: \n{slide}\n"
            f" Please summarize the key insights from this slide in the best way possible")

async def get_gpt_response(slide):
    """
    Here is where the magic happens, this function sends api call for chatgpt for each slide it gets

    :param slide: The content of a slide.
    :type slide: str
    :return: A string containing the chatgpt response
    :rtype: str
    """
    message = creat_prompt(slide)
    try:
        response = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model="gpt-3.5-turbo",
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
    responses = list()
    for slide in slides:
        response = await get_gpt_response(slide)
        responses.append(response)
    return responses
