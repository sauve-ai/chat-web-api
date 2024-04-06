from typing import AsyncGenerator, NoReturn
from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.services.openai_response import get_ai_response
from app.services.schema import Token
from app.routes.signup import get_db
from app.services import get_user
from app.db_utils.utils import (
                                get_user_by_userid_request_table,
                                create_user_plan_request
                                )
from app.services.utils import JWTBearer

routes = APIRouter()

@routes.post("/token")
async def websocket_endpoint(
    websocket: WebSocket,
    current_user_credential: str = Depends(JWTBearer()),
    db: Session = Depends(get_db)
    ) :
    """
    Websocket for AI responses
    """
    user_id =  get_user.get_current_user(
        credentials= current_user_credential,
        db= db
    )
    print("This is the user_id", user_id)
    ##getuser from table
    # db_request_user = get_user_by_userid_request_table(
    #     db= db,
    #     user_id= user_id
    # )
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        async for text in get_ai_response(message):
            await websocket.send_text(text)