from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)


def start_connection():
    message = "hi chat im communicating with you using python and openai, if the connection is successful please tell me"
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model="gpt-3.5-turbo",
        )
        print(chat_completion.choices[0].message.content.strip())
    except Exception as e:
        print(f"An error occurred: {e}")