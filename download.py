import json,sys,time,urllib.parse,urllib.request,datetime as dt
import pandas as pd
T={'NIFTY':'^NSEI','SPX':'^GSPC','NDX':'^NDX','COMP':'^IXIC','DJI':'^DJI','SENSEX':'^BSESN'}
p1=int(dt.datetime(2015,1,1).timestamp());p2=int(time.time())
for n,s in T.items():
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(s)}?period1={p1}&period2={p2}&interval=1d'
    r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=60))['chart']['result'][0]
    idx=pd.to_datetime(r['timestamp'],unit='s',utc=True).tz_convert(r['meta']['exchangeTimezoneName'])
    d=pd.DataFrame({'close':r['indicators']['quote'][0]['close']},index=idx.date);d.index.name='date'
    d.to_csv(f'data/{n}.csv');print(n,len(d),d.index[0],d.index[-1],'nan',d.close.isna().sum(),'dup',d.index.duplicated().sum())
