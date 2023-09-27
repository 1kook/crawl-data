from dotenv import load_dotenv
import pandas as pd
import pandas as pd
from plotly.subplots import make_subplots
import datetime
import numpy as np
import psycopg2
from cachetools import TTLCache
from sqlalchemy import create_engine, select


class CommonService:
    def __init__(self, DB_CON):
        self.db = create_engine(DB_CON)
        self.DB_CON = self.db.connect()
        self.cache = TTLCache(maxsize=10, ttl=60)

    def getData(self, symbol: str ,days=14.0):
        cacheKey = f"{symbol}-{days}"
        if cacheKey in self.cache:
            return self.cache[cacheKey]
        
        fromDate = datetime.datetime.now() - datetime.timedelta(days=days)
        # df = pd.read_sql_query(
            # "SELECT * FROM btc_price WHERE open_time >= %s", self.DB_CON, params=(fromDate,))
        df = pd.read_sql_query(
            f"SELECT * FROM {symbol.lower()}_price WHERE open_time >= %s", self.DB_CON, params=(fromDate,))
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms', utc=False)
        df['close_time'] = pd.to_datetime(
            df['close_time'], unit='ms', utc=False)
        df = df.set_index('open_time')
        df = df.resample('1MIN').ffill()
        
        self.cache[cacheKey] = df

        return df

    def resampleTimeframe(self, df, tf):
        df = df.copy()
        
        last_index_minute = int(df.index[-1].timestamp() / 60)
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

        vap = pd.DataFrame(
            {'price': price, 'volume': volume, 'bin': bin_labels})
        vap = vap.groupby('bin').sum()

        # Update index
        new_index = [bin.mid for bin in vap.index]
        vap.index = new_index

        return vap
