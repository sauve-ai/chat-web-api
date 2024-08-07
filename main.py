from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.routes import (
    signup, 
    fetchurl,
    get_login_token, 
    chatbot, 
    suggest_question, 
    forgot_password, 
    password_reset
    )

import uvicorn


from typing import AsyncGenerator, NoReturn

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from openai import AsyncOpenAI


app = FastAPI(
    description="suave.ai"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(signup.router)
app.include_router(fetchurl.router)
app.include_router(get_login_token.routes)
app.include_router(chatbot.routes)
app.include_router(suggest_question.router)
app.include_router(forgot_password.router)
app.include_router(password_reset.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  ## make false in production.
    )