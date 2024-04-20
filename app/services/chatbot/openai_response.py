import os
from typing import AsyncGenerator, NoReturn
import openai
from openai import AsyncOpenAI
from dotenv import load_dotenv
from dotenv import load_dotenv

from openai import AsyncOpenAI

load_dotenv()
client = AsyncOpenAI()

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



_PROMPT_TEMPLATE_MARKDOWN = """
    CONTEXT: {context}
    You are a helpful assistant, above is some context, 
    Please answer the question, and make sure you follow ALL of the rules below:
    1. Answer the questions only based on context provided, do not make things up
    2. Answer questions in a helpful manner that straight to the point, with clear structure & all relevant information that might help users answer the question
    3. Anwser should be formatted in Markdown
    4. If there are relevant images, video, links, they are very important reference data, please include them as part of the answer
    QUESTION: {question}
    ANSWER (formatted in markdown):
    """

def generate_markdown_response(
        query: str,
        content: str,
        prompt_markdown: str = _PROMPT_TEMPLATE_MARKDOWN
        ):
    """Call out to OpenAI's endpoint."""

    if len(os.environ["OPENAI_API_KEY"])>0:

        prompt_markdown = prompt_markdown.format(
                context= content,
                question= query
        )
        openai.api_key = os.environ["OPENAI_API_KEY"]
        response = openai.chat.completions.create(
                                    model="gpt-3.5-turbo",
                                    messages=[
                                        {"role": "user", "content": (prompt_markdown)},        
                                    ], 
                                    temperature=0.5,
                                    )

    
    return response.choices[0].message.content