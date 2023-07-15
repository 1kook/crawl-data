from dotenv import load_dotenv
import pandas as pd
import pandas as pd
from scipy import stats, signal
from plotly.subplots import make_subplots
import numpy as np

from src.service.plot.plot import PlotService


def calVpActionArea(self, vp):
    kde_factor = 0.05
    num_samples = 500
    kde = stats.gaussian_kde(
        self.df["close_price"], weights=self.df["volume"], bw_method=kde_factor)
    xr = np.linspace(self.df["close_price"].min(),
                     self.df["close_price"].max(), num_samples)
    kdy = kde(xr)

    peaks, peaks_props = signal.find_peaks(kdy)
    pkx = xr[peaks]
    pky = kdy[peaks]

    scaleY = vp["volume"].max() / kdy.max()

    kdy = kdy * scaleY
    peaks, peaks_props = signal.find_peaks(
        kdy, prominence=kdy.max() * 0.3, width=1)
    pkx = xr[peaks]
    pky = kdy[peaks]

    ticks_per_sample = (xr.max() - xr.min()) / num_samples

    left_base = peaks_props["left_bases"]
    right_base = peaks_props["right_bases"]
    line_x = pkx
    line_y0 = pky
    line_y1 = pky - peaks_props['prominences']

    left_ips = peaks_props['left_ips']
    right_ips = peaks_props['right_ips']
    width_x0 = xr.min() + (left_ips * ticks_per_sample)
    width_x1 = xr.min() + (right_ips * ticks_per_sample)
    width_y = peaks_props['width_heights']

    self.vp = [line_x, line_y0, line_y1, width_x0, width_x1, width_y]

    return self


def drawVpPlot(self, plot: PlotService):
    [line_x, line_y0, line_y1, width_x0, width_x1, width_y] = self.vp
    for x, y0, y1 in zip(line_x, line_y0, line_y1):
        plot.fig.add_shape(
            type='line',
            xref='x', yref='y',
            x0=y0, y0=x, x1=y1, y1=x,
            line=dict(
                color='red',
                width=2,
            ),
            row=1, col=1
        )

    for x0, x1, y in zip(width_x0, width_x1, width_y):
        plot.fig.add_shape(
            type='line',
            xref='x', yref='y',
            x0=y, y0=x0, x1=y, y1=x1,
            line=dict(
                color='red',
                width=2,
            ),
            row=1, col=1
        )

        plot.fig.add_shape(
            type="rect",
            x0=self.df.index.min(), y0=x0, x1=self.df.index.max()+pd.Timedelta(minutes=120), y1=x1,
            line=dict(width=0),
            fillcolor='rgba(181, 181, 181, 0.2)',
            row=1, col=2
        )
        
    return self
