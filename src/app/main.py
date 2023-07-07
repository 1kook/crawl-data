import os
from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse
from fastapi import FastAPI, Response

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

    indicator = Indicator(df, dtf)
    
    indicator.calVpActionArea(vp).drawVpPlot(plot)
    
    indicator.drawEmasPlot(13, plot)
    indicator.drawEmasPlot(21, plot)
    indicator.drawEmasPlot(34, plot)
    indicator.drawEmasPlot(55, plot)
    indicator.drawEmasPlot(89, plot)

    return Response(content=plot.exportHtml(), media_type="text/html")
