import urllib.request,io,pandas as pd,json,urllib.parse,time
for s in ['DGS10','DGS2','DGS3MO','DFII10','BAMLH0A0HYM2','BAMLC0A0CM','INDIRLTLT01STM','INDIR3TIB01STM','DTWEXBGS','DCOILBRENTEU','CPIAUCSL','INDCPIALLMINMEI','FEDFUNDS','IRSTCI01INM156N']:
    try:
        r=urllib.request.urlopen(urllib.request.Request(f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}&cosd=2014-06-01',headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read()
        d=pd.read_csv(io.BytesIO(r),index_col=0,parse_dates=True,na_values='.').dropna();d.columns=['close'];d.index.name='date';d.to_csv(f'macro/{s}.csv');print(s,len(d),d.index[0].date(),d.index[-1].date(),d.close.iloc[-1])
    except Exception as e: print(s,'ERR',e)
for n,s in {'TNX':'^TNX','IRX':'^IRX','BRENT':'BZ=F','DXY':'DX-Y.NYB','NIFTYBANK':'^NSEBANK','NIFTYIT':'^CNXIT','LTGILT':'LTGILTBEES.NS','GILT5':'GILT5YBEES.NS','IN10':'IN10Y','INVIX':'^INDIAVIX'}.items():
    try:
        u=f'https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(s)}?period1=1400000000&period2={int(time.time())}&interval=1d'
        r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=40))['chart']['result'][0]
        ix=pd.to_datetime(r['timestamp'],unit='s',utc=True).tz_convert(r['meta']['exchangeTimezoneName']).date
        d=pd.DataFrame({'close':r['indicators']['quote'][0]['close']},index=ix).dropna();d.index.name='date';d.to_csv(f'macro/{n}.csv');print(n,len(d),d.index[0],d.index[-1],d.close.iloc[-1])
    except Exception as e: print(n,'ERR',e)
