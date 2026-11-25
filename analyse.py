import pandas as pd,numpy as np,json
rng=np.random.default_rng(7)
END=pd.Timestamp('2026-11-24') # last day both markets complete
L={n:pd.read_csv(f'data/{n}.csv',index_col=0,parse_dates=True)['close'].dropna()[:END] for n in['NIFTY','SPX','COMP','DJI','NDX','SENSEX']}
US=['SPX','COMP','DJI'];W={'1m':21,'6m':126,'1y':252}
N=L['NIFTY']
def aligned(u,mode):
    s=L[u]
    if mode=='same':          # same calendar date
        d=pd.concat([N,s],axis=1,keys=['n','u']).dropna()
    elif mode=='lag':         # last US close strictly before NIFTY date d
        us=s.reindex(N.index.union(s.index)).ffill().shift(1) # strictly before each date
        d=pd.DataFrame({'n':N,'u':us.reindex(N.index)}).dropna()
    return d
def rets(u,mode,k=1):
    d=aligned(u,mode);return np.log(d).diff(k).dropna()
def cor(d):return d['n'].corr(d['u'])
# data check vs local 1-min
import os
if os.path.exists('../NIFTY 1min 2022-2025.csv') and os.path.exists('../NIFTY 1min YTD 2026.csv'):
    loc=pd.concat([pd.read_csv('../NIFTY 1min 2022-2025.csv').rename(columns={'time':'t'})[['t','close']],pd.read_csv('../NIFTY 1min YTD 2026.csv').rename(columns={'datetime':'t'})[['t','close']]])
    loc['t']=pd.to_datetime(loc.t);loc=loc.drop_duplicates('t').sort_values('t').reset_index(drop=True);lc=loc.groupby(loc.t.dt.normalize()).close.last()
    j=pd.concat([N,lc],axis=1,keys=['y','l']).dropna()
    print('yahoo vs local: n',len(j),'ret corr',np.log(j).diff().corr().iloc[0,1],'max lvl diff%',((j.y/j.l-1).abs()*100).quantile([.5,.99,1]).tolist(),'local missing in yahoo',[str(x.date()) for x in lc.index.difference(N.index)][:20])
print('big moves',{k:v.pct_change().abs().loc['2022':].nlargest(2).round(4).to_dict() for k,v in L.items()})
def mbb_idx(n,b):
    st=rng.integers(0,n-b+1,size=int(np.ceil(n/b)));return np.concatenate([np.arange(x,x+b) for x in st])[:n]
def boot(d,B=4000,b=10):
    a=d[['n','u']].values;return np.array([np.corrcoef(a[mbb_idx(len(a),b)].T)[0,1] for _ in range(B)])
out={}
for mode in['lag','same']:
  for u in US+['NDX']:
    r=rets(u,mode);R=r['2023':]
    print('\n==',mode,u,'full 2023+ corr %.3f n=%d'%(cor(R),len(R)))
    print(' by year',{y:round(cor(r.loc[str(y)]),2) for y in range(2015,2027)})
    for w,k in W.items():
      c=r['n'].rolling(k).corr(r['u'])['2023':]
      m=c.groupby(c.index.year).mean().round(2).to_dict()
      print(f' {w}: now {c.iloc[-1]:.2f} min {c.min():.2f}@{c.idxmin().date()} max {c.max():.2f} neg% {100*(c<0).mean():.0f} neg% by yr',(c.groupby(c.index.year).apply(lambda x:round(100*(x<0).mean()))).to_dict(),'mean',m)
      # trend test: slope of rolling corr per yr; null = constant-correlation block bootstrap of pairs
      x=(np.arange(len(c))/250);sl=np.polyfit(x,c.values,1)[0]
      a=r.loc[:, ['n','u']].iloc[-(len(c)+k-1):].values;ns=[]
      for _ in range(1000):
        z=pd.DataFrame(a[mbb_idx(len(a),10)]);cc=z[0].rolling(k).corr(z[1]).dropna().values;ns.append(np.polyfit(x[:len(cc)],cc,1)[0])
      print(f'   slope/yr {sl:.3f} p(slope<=obs|constant) {(np.array(ns)<=sl).mean():.3f}')
    p,q=R['2023':'2024'],r.iloc[-252:]
    bp,bq=boot(p),boot(q);dd=bq-bp
    print(f' 2023-24 {cor(p):.2f} [{np.quantile(bp,.025):.2f},{np.quantile(bp,.975):.2f}] last252 {cor(q):.2f} [{np.quantile(bq,.025):.2f},{np.quantile(bq,.975):.2f}] diff {cor(q)-cor(p):.2f} [{np.quantile(dd,.025):.2f},{np.quantile(dd,.975):.2f}]')
print('\nweekly (non-overlap, Fri, US through Thu close via lag alignment vs plain Fri)')
for u in US:
    d=aligned(u,'lag').resample('W-FRI').last();r=np.log(d).diff().dropna()
    d2=aligned(u,'same').resample('W-FRI').last();r2=np.log(d2).diff().dropna()
    print(u,'lag',{y:round(cor(r.loc[str(y)]),2) for y in range(2019,2027)},'last52',round(cor(r.iloc[-52:]),2),'| same',{y:round(cor(r2.loc[str(y)]),2) for y in range(2019,2027)},'last52',round(cor(r2.iloc[-52:]),2))
print('\nPRICE LEVEL rolling')
for u in US:
    d=aligned(u,'same')
    for w,k in W.items():
        c=d.n.rolling(k).corr(d.u)['2023':];print(u,w,'now %.2f'%c.iloc[-1],'neg%% by yr',c.groupby(c.index.year).apply(lambda x:round(100*(x<0).mean())).to_dict(),'mean',c.groupby(c.index.year).mean().round(2).to_dict())
print('\nSPEARMAN / 8-Apr..11-Apr-2025 excluded, lag')
for u in US:
    r=rets(u,'lag');q=r.drop(r['2025-04-03':'2025-04-15'].index)
    print(u,{y:(round(r.loc[str(y)].corr('spearman').iloc[0,1],2) if 0 else round(r.loc[str(y)].rank().corr().iloc[0,1],2)) for y in range(2023,2027)},'ex-Apr25 2025:',round(cor(q.loc['2025']),2))
