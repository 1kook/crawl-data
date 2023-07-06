from fastapi.responses import PlainTextResponse
from fastapi import FastAPI, Response
from vap.handler import *

app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
async def root():
    return {"message": "Hello World"}


@app.get("/vap")
async def vap(d: int=14, tf: int=60):
    return Response(content=vapHandler(d, tf), media_type="text/html")
