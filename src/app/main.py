import os
from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse
from fastapi import FastAPI, Response
import pandas as pd

from src.service.common.common import CommonService
from src.service.indicator.indicator import Indicator
from src.service.plot.plot import PlotService

load_dotenv()

app = FastAPI()
common = CommonService(os.getenv('CONNECTION'))


@app.get("/", response_class=PlainTextResponse)
async def root():
    return {"message": "Hello World"}

@app.get("/plot")
async def vap(d: int = 14, tf: int = 60):
    df = common.getData(d)
    dtf = common.resampleTimeframe(df, tf)
    vp = common.calVolumeProfile(df, 50)

    plot = PlotService()
    plot.drawCommon(dtf, vp)

    Indicator(df).calVpActionArea(vp).drawVpPlot(plot)

    return Response(content=plot.exportHtml(), media_type="text/html")


@app.get("/plot/ema")
async def vap(d: int = 14, tf: int = 60, fast: int = 7, slow: int = 26, signal: int = 9):
    df = common.getData(d)
    dtf = common.resampleTimeframe(df, tf)
    vp = common.calVolumeProfile(df, 50)

    plot = PlotService()
    plot.drawCommon(dtf, vp)

    Indicator(df).calVpActionArea(vp).drawVpPlot(plot)
    indicator = Indicator(dtf).calMacd(fast, slow, signal).drawMacd(plot)

    return Response(content=plot.exportHtml(), media_type="text/html")


@app.get("/plot/atrbb")
async def atrbb(d: int = 14, tf: int = 60, atr: int = 14, bb: int = 20, bb_std: int = 2):
    df = common.getData(d)
    dtf = common.resampleTimeframe(df, tf)
    vp = common.calVolumeProfile(df, 50)

    plot = PlotService()
    plot.drawCommon(dtf, vp)

    Indicator(dtf).calAtr(atr).drawAtr(plot)
    Indicator(dtf).calBB(bb, bb_std).drawBB(plot)

    return Response(content=plot.exportHtml(), media_type="text/html")


@app.get("/plot/rsi")
async def rsi(d: int = 14, tf: int = 60, rsi: int = 14):
    df = common.getData(d)
    dtf = common.resampleTimeframe(df, tf)
    vp = common.calVolumeProfile(df, 50)

    plot = PlotService()
    plot.drawCommon(dtf, vp)

    Indicator(dtf).calRsi(rsi).drawRsi(plot)

    return Response(content=plot.exportHtml(), media_type="text/html")


@app.get("/plot/adx")
async def adx(d: int = 14, tf: int = 60, adx: int = 14):
    df = common.getData(d)
    dtf = common.resampleTimeframe(df, tf)
    vp = common.calVolumeProfile(df, 50)

    plot = PlotService()
    plot.drawCommon(dtf, vp)

    Indicator(dtf).calAdx(adx).drawAdx(plot)

    return Response(content=plot.exportHtml(), media_type="text/html")


@app.get("/plot/obv")
async def obv(d: int = 14, tf: int = 60):
    df = common.getData(d)
    dtf = common.resampleTimeframe(df, tf)
    vp = common.calVolumeProfile(df, 50)

    plot = PlotService([0.5, 0.5])
    plot.drawCommon(dtf, vp)

    Indicator(dtf).calObv().drawObv(plot)

    return Response(content=plot.exportHtml(), media_type="text/html")
