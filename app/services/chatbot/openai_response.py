import os
from typing import AsyncGenerator, NoReturn
import openai
from openai import AsyncOpenAI
from dotenv import load_dotenv
from dotenv import load_dotenv

from openai import AsyncOpenAI

load_dotenv()
client = AsyncOpenAI()


async def get_ai_response(message: str):
    """
    OpenAI Response
    """
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant, skilled in explaining "
                    "complex concepts in simple terms."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        stream=True,
    )

    all_content = ""
    async for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            all_content += content
            yield all_content


def get_chat_response(query):
    """Call out to OpenAI's endpoint."""

    if len(os.environ["OPENAI_API_KEY"])>0:


        openai.api_key = os.environ["OPENAI_API_KEY"]
        response = openai.chat.completions.create(
                                    model="gpt-3.5-turbo",
                                    messages=[
                                        {"role": "user", "content": (query)},        
                                    ], 
                                    temperature=0.5,
                                    )

    
    return response.choices[0].message.content