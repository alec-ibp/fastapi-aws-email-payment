from fastapi import FastAPI
from db.init_db import database
from api.v1.api_routes import api_router


app = FastAPI()
app.include_router(api_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()