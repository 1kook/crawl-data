from dotenv import load_dotenv
import pandas as pd
import pandas as pd
from plotly.subplots import make_subplots
import datetime
import numpy as np
import psycopg2

class CommonService:
    def __init__(self, DB_CON):
        self.DB_CON = psycopg2.connect(DB_CON)

    def getData(self, days=14):
        print(self.DB_CON)
        fromDate = datetime.datetime.now() - datetime.timedelta(days=days)

        df = pd.read_sql_query(
            'SELECT * FROM btc_price WHERE open_time > %s', self.DB_CON, params=(fromDate,))
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms', utc=False)
        df['close_time'] = pd.to_datetime(
            df['close_time'], unit='ms', utc=False)
        df = df.set_index('open_time')
        df = df.resample('1MIN').ffill()

        return df

    def resampleTimeframe(self, df, tf):
        df = df.copy()

        last_index_minute = df.index[-1].minute
        minutes_to_adjust = (tf - (last_index_minute + 1) % tf) % tf

        if minutes_to_adjust > 0:
            last_row = df.iloc[-1]
            for _ in range(minutes_to_adjust):
                df.loc[df.index[-1] + pd.Timedelta(minutes=1)] = last_row

        dtf = df.resample(str(tf)+'Min').agg({
            'open_price': 'first',
            'high_price': 'max',
            'low_price': 'min',
            'volume': 'sum',
            'close_price': lambda x: x.iloc[-1],
            'close_time': lambda x: x.iloc[-1]
        }).dropna()

        return dtf

    def calVolumeProfile(self, df, bin_size=10):
        price = df['close_price']
        volume = df['volume']
        
        # Calculate histogram
        bins = np.arange(price.min(), price.max(), bin_size)
        bin_labels = pd.cut(price, bins)

        vap = pd.DataFrame({'price': price, 'volume': volume, 'bin': bin_labels})
        vap = vap.groupby('bin').sum()

        # Update index
        new_index = [bin.mid for bin in vap.index]
        vap.index = new_index

        return vap