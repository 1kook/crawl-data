import plotly.graph_objects as go


def ema(self, period=100):
    self.emas[period] = self.dtf["close_price"].ewm(
        span=period, adjust=False).mean()
    return self


def drawEmasPlot(self, period, plot):
    if period not in self.emas:
        self.ema(period)

    color = "rgb("+str(255-period*100/200)+","+str(255)+","+str(0)+")"

    plot.fig.add_trace(
        go.Scatter(
            x=self.emas[period].index,
            y=self.emas[period],
            mode="lines",
            name="EMA " + str(period),
            line=dict(color=color, width=1),
        ),
        row=1, col=2
    )

    return self
