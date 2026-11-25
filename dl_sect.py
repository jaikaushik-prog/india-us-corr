import urllib.request,urllib.parse,json,time,os,pandas as pd
os.makedirs('sect',exist_ok=True)
for n,s in {'NIFTY':'^NSEI','BANK':'^NSEBANK','IT':'^CNXIT','METAL':'^CNXMETAL','PHARMA':'^CNXPHARMA','AUTO':'^CNXAUTO','FMCG':'^CNXFMCG','ENERGY':'^CNXENERGY','REALTY':'^CNXREALTY','INFRA':'^CNXINFRA','PSUBANK':'^CNXPSUBANK','FIN':'NIFTY_FIN_SERVICE.NS','MEDIA':'^CNXMEDIA','SPXTR':'^SP500TR','SPY':'SPY','NIFTYBEES':'NIFTYBEES.NS','GOLD':'GC=F'}.items():
    try:
        u=f'https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(s)}?period1=1100000000&period2={int(time.time())}&interval=1d'
        r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=40))['chart']['result'][0]
        ix=pd.to_datetime(r['timestamp'],unit='s',utc=True).tz_convert(r['meta']['exchangeTimezoneName']).date
        q=r['indicators']['quote'][0];d=pd.DataFrame({k:q[k] for k in('open','high','low','close')},index=ix)
        a=r['indicators'].get('adjclose');d['adj']=a[0]['adjclose'] if a else d.close
        d=d.dropna(subset=['close']);d=d[~d.index.duplicated()];d.index.name='date';d.to_csv(f'sect/{n}.csv')
        c=d.close.pct_change().abs();print(n,len(d),d.index[0],d.index[-1],'days>12%:',[(str(i),round(v,2)) for i,v in c[c>.12].items()][:4],'since2015',sum(pd.to_datetime(d.index)>='2015'))
    except Exception as e: print(n,'ERR',e)
