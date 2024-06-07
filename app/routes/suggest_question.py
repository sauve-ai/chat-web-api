from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from http import HTTPStatus
from app.db_utils import models
from app.db_utils.database import SessionLocal, engine
from app.services.scraper.scrape_url import ScrapeWebPage
from app.services.chatbot.openai_response import get_chat_response

models.Base.metadata.create_all(bind=engine)
router  = APIRouter()

_PROMPT_TEMPLATE = """Please act as a teacher that needs to generate 4 questions from a paragraph. 

If you cannot find the answer in the given context, Please respond with you are not aware about the question and ask for context.
 Don't try to makeup the answer.
    

Paragraph is listed in triple backticks.

```{question}```

Your Helpful Questions:

"""


@router.get("/api/v1/suggest/", tags=["urls"], status_code=HTTPStatus.OK)
async def suggest(
    url: str
):
    """Get request for user url limit"""

    # Scraping the base URL and returning the content
    tai_scraper = ScrapeWebPage(url)
    processed_url = tai_scraper.process_urls(url_list=[url], base_url=url)
    content = tai_scraper.get_page_contents(url_list = set(processed_url))
    data = content[0]["text"][:1500]

    # creating prompt to generate question.
    query = _PROMPT_TEMPLATE.format(
        question=data
    )
    response = get_chat_response(query=query)
    return {"status":"success",
            "questions":response}

    
