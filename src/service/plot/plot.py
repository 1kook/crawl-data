import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class PlotService:
    fig = None

    def __init__(self):
        self.fig = make_subplots(
            rows=2,
            cols=2,
            vertical_spacing=0.07,
            subplot_titles=('VAP', 'OHLC', '', 'Volume'),
            row_width=[0.15, 0.85],
            column_widths=[0.15, 0.85],
            horizontal_spacing=0.01,
            shared_yaxes='rows',
        )

    def drawCommon(self, df, vp):
        self.fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['open_price'],
                high=df['high_price'],
                low=df['low_price'],
                close=df['close_price'],
                name='market data',
                increasing_line_color='rgb(149,117,205)',
                decreasing_line_color='white',
            ),
            row=1, col=2
        )

        self.fig.add_trace(
            go.Bar(
                x=df.index,
                y=df['volume'],
                name='volume',
                marker={
                    "color": "rgba(128,128,128,0.5)",
                }),
            row=2, col=2
        )

        self.fig.add_trace(
            go.Bar(
                x=vp.volume,
                y=vp.index,
                text=np.around(vp.volume, 2),
                textposition='auto',
                orientation='h',
                marker={
                    "color": "rgba(128,128,128,0.5)",
                },
            ),
            row=1, col=1
        )

        return self

    def updatePlot(self, func):
        self.fig = func(self.fig)
        return self

    def exportHtml(self):
        self.fig.update_layout(
            title_text='BTC/USDT',
            yaxis2=dict(
                title="Price (USD)",
                side="right"
            ),
            xaxis=dict(rangeslider=dict(visible=False)),
            xaxis2=dict(rangeslider=dict(visible=False)),
            template="plotly_dark",
        )

        self.fig.update_layout(autosize=True)
        return self.fig.to_html(full_html=True)
