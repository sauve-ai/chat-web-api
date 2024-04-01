from fastapi import APIRouter, HTTPException, Depends

from typing import Annotated

from http import HTTPStatus

from app.services.scraper import scrape_url
from app.services import get_user

router  = APIRouter()

@router.get("/api/v1/geturl/", tags=["urls"], status_code=HTTPStatus.OK)
def fetch_url(
    base_url:str,
    current_user: Annotated[str, Depends(get_user.get_current_user)]
    ):
    """Fetch all the anchor tag from the url"""

    ##TODO: Check for the number of urls, for premium
    tai_scraper = scrape_url.ScrapeWebPage(base_url)
    url_list, base_url = tai_scraper.get_url()
    processed_url = tai_scraper.process_urls(url_list=url_list, base_url=base_url)
    # content = tai_scraper.get_page_contents(url_list = set(processed_url))
    response = {"success":"true",
                "urls": processed_url}
    return response
