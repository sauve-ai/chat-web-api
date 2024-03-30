from fastapi import FastAPI

from app.routes import signup, fetchurl

app = FastAPI(
    description="Sauve ai"
)


app.include_router(signup.router)
app.include_router(fetchurl.router)



@app.get("/")
async def home():
    return {"message": "Healthy api"}