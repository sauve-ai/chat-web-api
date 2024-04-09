from typing import AsyncGenerator, NoReturn
from fastapi import APIRouter, WebSocket, Depends, HTTPException, WebSocketDisconnect
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.services.chatbot.openai_response import get_ai_response
from app.services.schema import Token
from app.routes.signup import get_db
from app.services import get_user
from app.db_utils.utils import (
                                get_user_by_userid_request_table,
                                create_user_plan_request
                                )
from app.services.utils import JWTBearer

routes = APIRouter()

@routes.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
    # current_user_credential: str = Depends(JWTBearer()),
    # db: Session = Depends(get_db)
    ) :
    """
    Websocket for AI responses
    """
    # user_id =  get_user.get_current_user(
    #     credentials= current_user_credential,
    #     db= db
    # )
    # print("[USER ID] for chatbot verification: ", user_id)
    # #getuser from table
    # db_request_user = get_user_by_userid_request_table(
    #     db= db,
    #     user_id= user_id
    # )
    # USER ID VERIFICATION AND PLAN extraction
    # TODO plan = extract_chatbot_plan(user_id)
    plan = "Free"
    USER_LIMIT = 15
    message_count = 0
    message_counts = {}
    is_premium_user = False if plan=="Free" else "True"
    try:
        await websocket.accept()

        async for message in websocket.iter_text():
            message_count +=1
            message_counts["user_id"] = message_count
            # print(f"Received message {message_count} from user {user_id}: {message}")
            async for text in get_ai_response(message=message):
                await websocket.send_text(text)
            if not is_premium_user and message_count > USER_LIMIT:
                await websocket.send_json({"detail": "Message limit reached"})
                await websocket.close()
                return HTTPException(status_code=429, detail="Message limit reached")
    except Exception as e:
        print(e)
        # print(f"[WEBSOCKET] Connection closed for: {user_id} Total Message recieved: {message_count}")
        ## Implement update user databse of count
        pass