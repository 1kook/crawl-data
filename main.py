import asyncio
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
    # thread1 = threading.Thread(
    #     target=crawl.crawlPrice, args=("BTC", stopThreads,))
    # thread2 = threading.Thread(
    #     target=crawl.crawlPrice, args=("ETH", stopThreads,))
    # thread3 = threading.Thread(
    #     target=crawl.crawlPrice, args=("ADA", stopThreads,))
    thread4 = threading.Thread(
        target=crawl.crawlPrice, args=("MATIC", stopThreads,))

    signal.signal(signal.SIGINT, sigintHandler)

    # thread1.start()
    # thread2.start()
    # thread3.start()
    thread4.start()


def main():
    uvicorn.run("main:app", host='0.0.0.0', port=8000,
                log_level="info", reload=True)


if __name__ == '__main__':
    main()
    print('App started')
