import urllib.request,urllib.parse,json,time,os,pandas as pd
os.makedirs('lead',exist_ok=True)
for n,s in {'SOXX':'SOXX','SPY':'SPY','HYG':'HYG','IEF':'IEF','EMB':'EMB','MOVE':'^MOVE','HG':'HG=F','GC':'GC=F','INDA':'INDA','EEM':'EEM','LQD':'LQD','TIP':'TIP','CNY':'CNY=X','JPY':'JPY=X','SOX':'^SOX'}.items():
    try:
        r=json.load(urllib.request.urlopen(urllib.request.Request(f'https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(s)}?period1=1356998400&period2={int(time.time())}&interval=1d',headers={'User-Agent':'Mozilla/5.0'}),timeout=60))['chart']['result'][0]
        ix=pd.to_datetime(r['timestamp'],unit='s',utc=True).tz_convert(r['meta']['exchangeTimezoneName']).date;a=r['indicators'].get('adjclose');v=a[0]['adjclose'] if a else r['indicators']['quote'][0]['close']
        d=pd.DataFrame({'close':v},index=ix).dropna();d.index.name='date';d=d[~d.index.duplicated()];d.to_csv(f'lead/{n}.csv');print(n,len(d),d.index[0],d.index[-1])
    except Exception as e: print(n,'ERR',e)
