from fastapi import FastAPI

from app.routes import signup

app = FastAPI(
    description="Sauve ai"
)


app.include_router(signup.router)


@app.get("/")
async def home():
    return {"message": "Healthy api"}