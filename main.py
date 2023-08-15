import asyncio
import os
import signal
import threading
import uvicorn
from fastapi import FastAPI
from src.service.crawl import crawl
from src.router import router as api_router

stopThreads = [False]

app = FastAPI()
app.include_router(api_router.router)


def sigintHandler(signum, frame):
    global stopThreads
    stopThreads[0] = True
    print("Ctrl+C detected. Waiting for threads to finish...")
    # wait for threads to finish


@app.on_event('startup')
async def startup_event():
    global stopThreads
    
    symbolList = os.getenv('SYMBOL_LIST').split(',')
    for symbol in symbolList:
        #start threads
        thread = threading.Thread(
            target=crawl.crawlPrice, args=(symbol, stopThreads,))
        thread.start()

@app.on_event('shutdown')
async def shutdown_event():
    global stopThreads
    stopThreads[0] = True
    print("Waiting for threads to finish...")
    # wait for threads to finish


def main():
    uvicorn.run("main:app", host='0.0.0.0', port=8000,
                log_level="info", reload=True)


if __name__ == '__main__':
    main()
    print('App started')
