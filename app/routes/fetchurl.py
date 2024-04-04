from fastapi import APIRouter,  Depends,Request
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from http import HTTPStatus
from sqlalchemy.orm import Session
from app.services.scraper import scrape_url
from app.services import get_user

from app.routes.signup import get_db

router  = APIRouter()

## TODO: define in schema
class URLRequest(BaseModel):
    base_url: str

## TODO: Define in services
class JWTBearer(HTTPBearer):
   async def __call__(self, request: Request):
       credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
       if credentials:
           return credentials.credentials



@router.post("/api/v1/fetchurl/", tags=["urls"], status_code=HTTPStatus.OK)
async def fetch_url(
    url_request: URLRequest,
    current_user_credential: str = Depends(JWTBearer()),
    db: Session = Depends(get_db)
):
    """Fetch all the anchor tag from the url"""
    ##TODO: Check for the number of urls, for premium

    user_id =  get_user.get_current_user(
        credentials= current_user_credential,
        db= db
    )
    
    base_url = url_request.base_url
    tai_scraper = scrape_url.ScrapeWebPage(base_url)
    url_list, base_url = tai_scraper.get_url()
    processed_url = tai_scraper.process_urls(url_list=url_list, base_url=base_url)
    # content = tai_scraper.get_page_contents(url_list = set(processed_url))
    response = {"success": "true", "urls": processed_url}
    return response