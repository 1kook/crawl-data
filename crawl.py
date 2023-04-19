from mexc_sdk import Market, Spot 
import time
import os
from dotenv import load_dotenv
from influxdb import InfluxDBClient

# import api key and secret from .env
load_dotenv()

market = Market(os.getenv('API_KEY'), os.getenv('API_SECRET'))
client = InfluxDBClient(host='localhost', port=8086)
client.create_database('mydb')
client.switch_database('mydb')

checkpoint = 0

while True:
    if int(time.time())*1000>checkpoint:
        kline = market.klines(symbol='BTCUSDT', interval='1m', options={'limit': 2})
  
        if (checkpoint == kline[1][6]):
            continue
        
        data = {
            'time': kline[0][0],
            'open': float(kline[0][1]),
            'high': float(kline[0][2]),
            'low': float(kline[0][3]),
            'close': float(kline[0][4]),
            'volume': float(kline[0][5]),
            'close_time': kline[0][6],
            'quote_asset_volume': float(kline[0][7]),
        }
        
        print(data)
        
        checkpoint = kline[1][6]
        client.write_points(data)
        time.sleep(2)