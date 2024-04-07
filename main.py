from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    signup, 
    fetchurl,
    get_login_token, 
    chatbot
    )

import uvicorn

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



@app.get("/")
async def home():
    return {"message": "Healthy api"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  ## make false in production.
    )