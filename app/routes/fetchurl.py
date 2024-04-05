from fastapi import APIRouter,  Depends,Request, HTTPException, status
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from http import HTTPStatus
from sqlalchemy.orm import Session

from app.services.scraper import scrape_url
from app.services import get_user
from app.routes.signup import get_db
from app.db_utils.utils import (
                                get_user_by_userid_request_table,
                                create_user_plan_request
                                )

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
    print("This is the user_id", user_id)
    ##getuser from table
    db_request_user = get_user_by_userid_request_table(
        db= db,
        user_id= user_id
    )
    print("This is the db_user: ",db_request_user)
    if not db_request_user:
        ##create user plan
        user_plan = create_user_plan_request(
            user_id= user_id,
            request= 1,
            db= db,
            plan_id=0
        )
        print(user_plan)
    else:
        ## increase the request for the particular user
        db_plan = db_request_user.plan_id

        if db_plan == 0:
            if db_request_user.request<=5:
                
                db_request_user.request+=1
                db.add(db_request_user)
                db.commit()
                print("database updateed")
            
            else:
                raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Max limit of request exceed.",
                    )
        
    base_url = url_request.base_url
    tai_scraper = scrape_url.ScrapeWebPage(base_url)
    url_list, base_url = tai_scraper.get_url()
    processed_url = tai_scraper.process_urls(url_list=url_list, base_url=base_url)
    # content = tai_scraper.get_page_contents(url_list = set(processed_url))
    response = {"success": "true", "urls": processed_url}
    return response