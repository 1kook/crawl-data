import plotly.graph_objects as go

def calBB(self, period, std):
    self.bb = self.df[["close_price"]].copy()
    self.bb["middle"] = self.df["close_price"].rolling(period).mean()
    self.bb["upper"] = self.bb["middle"] + self.df["close_price"].rolling(period).std() * std
    self.bb["lower"] = self.bb["middle"] - self.df["close_price"].rolling(period).std() * std
    return self
    
def drawBB(self, plot):
    plot.fig.add_trace(
        go.Scatter(
            x=self.bb.index,
            y=self.bb["middle"],
            name="lower",
            line=dict(color="red")
        ), row=1, col=2)
    
    #fill color between upper and lower band
    plot.fig.add_trace(
        go.Scatter(
            x=self.bb.index,
            y=self.bb["upper"],
            name="upper",
            line=dict(color='rgb(181, 181, 181)'),
            showlegend=False,
        ), row=1, col=2)
    
    plot.fig.add_trace(
        go.Scatter(
            x=self.bb.index,
            y=self.bb["lower"],
            name="lower",
            line=dict(color='rgb(181, 181, 181)'),
            showlegend=False,
            fill="tonexty",
            fillcolor='rgba(181, 181, 181, 0.2)'
        ), row=1, col=2)
    
    
    return self