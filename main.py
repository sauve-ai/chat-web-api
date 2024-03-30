from fastapi import FastAPI

from app.routes import (
    signup, 
    fetchurl,
    get_login_token
    )

app = FastAPI(
    description="Sauve ai"
)


app.include_router(signup.router)
app.include_router(fetchurl.router)
app.include_router(get_login_token.routes)


@app.get("/")
async def home():
    return {"message": "Healthy api"}