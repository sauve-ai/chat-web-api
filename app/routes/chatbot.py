from typing import AsyncGenerator, NoReturn, List

from fastapi import APIRouter, WebSocket, Depends, HTTPException, WebSocketDisconnect,Query, status
from fastapi.responses import HTMLResponse

from http import HTTPStatus

from sqlalchemy.orm import Session

from app.services.chatbot.openai_response import get_ai_response
from app.services.schema import Token
from app.routes.signup import get_db
from app.services import get_user
from app.db_utils.utils import (
                                get_user_by_userid_request_table,
                                create_user_plan_request,
                                get_user_by_userid_chatbot_plan,
                                create_user_chatbot_plan
                                )
from app.services.utils import JWTBearer
from app.services.chatbot import openai_response


routes = APIRouter()



@routes.post("/api/v1/chat/", tags=["chatbot"], status_code=HTTPStatus.OK)
async def chat(
    links: List,
    query: str,
    current_user_credential: str = Depends(JWTBearer()),
    db: Session = Depends(get_db)
):
    
    """Give a response for the query chatbot"""
    print(links)
    
    user_id =  get_user.get_current_user(
        credentials= current_user_credential,
        db= db
    )
    print("This is the user_id", user_id)
    ##getuser from table
    db_chatbot_plan_user_id = get_user_by_userid_chatbot_plan(
        db= db,
        user_id= user_id
    )
    print("This is the db_user: ",db_chatbot_plan_user_id)
    if not db_chatbot_plan_user_id:
        ##create user plan
        user_plan = create_user_chatbot_plan(
            user_id= user_id,
            chat_request= 1,
            db= db,
            plan_id=0
        )
        print(user_plan)
    else:
        ## increase the request for the particular user
        db_plan = db_chatbot_plan_user_id.plan_id

        if db_plan == 0:
            if db_chatbot_plan_user_id.chat_request<=5:
                
                db_chatbot_plan_user_id.chat_request+=1
                db.add(db_chatbot_plan_user_id)
                db.commit()
                print("database updateed")
            
            else:
                raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Max limit of request exceed.",
                    )
            
    print("I am here")
    response = openai_response.get_chat_response(query)
    return response



# @routes.websocket("/api/v1/chat")
# async def websocket_endpoint(
#     websocket: WebSocket,
#     token: str = Query(...), 
#     db: Session = Depends(get_db)
#     ) :
#     """
#     Websocket for AI responses
#     """
#     print(token)
#     # user_id =  get_user.get_current_user(
#     #     credentials= current_user_credential,
#     #     db= db
#     # )
#     # print("[USER ID] for chatbot verification: ", user_id)
#     # #getuser from table
#     # db_request_user = get_user_by_userid_request_table(
#     #     db= db,
#     #     user_id= user_id
#     # )
#     # USER ID VERIFICATION AND PLAN extraction
#     # plan = extract_chatbot_plan(user_id)
#     # USER_LIMIT = 15
#     # message_count = 0
#     # is_premium_user = False if plan=="Free" else "True"
#     try:
#         await websocket.accept()

#         async for message in websocket.iter_text():
#             message_count +=1
#             message_counts[user_id] = message_count
#             print(f"Received message {message_count} from user {user_id}: {message}")
#             if not is_premium_user and message_count > USER_LIMIT:
#                 await websocket.send_json({"detail": "Message limit reached"})
#                 await websocket.close()
#                 return HTTPException(status_code=429, detail="Message limit reached")
#     except WebSocketDisconnect:
#         print(f"[WEBSOCKET] Connection closed for: {user_id} Total Message recieved: {message_count}")
#         ## Implement update user databse of count


