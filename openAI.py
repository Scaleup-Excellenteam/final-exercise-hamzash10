from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()



async def start_connection():
    client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    message = "hi chat im communicating with you using python and openai, if the connection is successful please tell me"
    try:
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model="gpt-3.5-turbo",
        )
        print(chat_completion.choices[0].message.content.strip())
        return
    except Exception as e:
        print(f"An error occurred: {e}")