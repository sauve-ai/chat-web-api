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
from app.services.schema import URLRequest
from app.services.utils import JWTBearer

router  = APIRouter()


##get request
@router.get("/api/v1/count/", tags=["urls"], status_code=HTTPStatus.OK)
async def fetch_url(
        current_user_credential: str = Depends(JWTBearer()),
        db: Session = Depends(get_db)

):
    """Get request for user url limit"""

    ##get user information from JWT token
    user_id =  get_user.get_current_user(
        credentials= current_user_credential,
        db= db
    )

    ##query request table for url
    db_request_user = get_user_by_userid_request_table(
        db= db,
        user_id= user_id
    ) 

    if not db_request_user:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="No information about the user"
        )
    else:
        db_plan = db_request_user.plan_id
        if db_plan == 0:
            response = {
                "success": True,
                "Fetch_api_count": db_request_user.request - 1,
                "Fetch_api_limit":5
            }

            return response
        else:

            ##for premium users
            response = {
                "success": True,
                "Fetch_api_count": "unlimited",
                "Fetch_api_limit":"unlimited"
            }

            return response


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
    ##getuser from table
    db_request_user = get_user_by_userid_request_table(
        db= db,
        user_id= user_id
    )
    if not db_request_user:
        ##create user plan
        try:
            user_plan = create_user_plan_request(
                user_id= user_id,
                request= 0,
                db= db,
                plan_id=0
            )
            print(user_plan)
        except Exception as e:
            print("Warning: FALL back while updating fetch url table.")
            raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Something went wrong while creating user request. Please try again later.",
                    )
        
    else:
        ## increase the request for the particular user
        db_plan = db_request_user.plan_id

        if db_plan == 0:
            if db_request_user.request<=5:
                
                db_request_user.request+=1
                db.add(db_request_user)
                db.commit()
            
            else:
                raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Max limit of request exceed.",
                    )

    try:    
        base_url = url_request.base_url
        tai_scraper = scrape_url.ScrapeWebPage(base_url)
        url_list, base_url = tai_scraper.get_url()
        processed_url = tai_scraper.process_urls(url_list=url_list, base_url=base_url)
        # content = tai_scraper.get_page_contents(url_list = set(processed_url))
        response = {"success": "true", "urls": processed_url}
        return response
    except Exception as e:
        print(f"WARNING: Exception occured {e}")
        print("GEnerating the fallback for fetch url.")
        user_request = db_request_user.request
        if user_request !=0:
            db_request_user.request-=1
            db.add(db_request_user)
            db.commit()
            print("database updateed")
            raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Something went wrong while processing url.",
                    )

