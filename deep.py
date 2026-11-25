import io,contextlib,json
src=open('analyse.py').read().split("# data check")[0]
exec(src)
def mbb_idx(n,b):
    st=rng.integers(0,n-b+1,size=int(np.ceil(n/b)));return np.concatenate([np.arange(x,x+b) for x in st])[:n]
def ci(a,B=2000,b=5):
    a=(a[['n','u']] if isinstance(a,pd.DataFrame) else a);a=np.asarray(a,float);q=np.array([np.corrcoef(a[mbb_idx(len(a),b)].T)[0,1] for _ in range(B)]);return np.quantile(q,[.025,.975]).round(2).tolist()
O={}
rd=lambda n:pd.read_csv(f'data/{n}.csv',index_col=0,parse_dates=True)['close'].dropna()[:END].pipe(lambda s:s[~s.index.duplicated()])
def al(asia,us):
    u=us.reindex(asia.index.union(us.index)).ffill().shift(1);return np.log(pd.DataFrame({'n':asia,'u':u.reindex(asia.index)}).dropna()).diff().dropna()
Y=[str(y) for y in range(2015,2027)]
# 1 rebased levels weekly
lv=pd.concat({k:L[k] for k in['NIFTY']+US},axis=1).ffill()['2022-12-30':]
lv=(lv/lv.iloc[0]*100).resample('W-FRI').last().dropna();lv.index=lv.index.map(lambda x:min(x,END))
O['lev']={'d':[str(x.date()) for x in lv.index],**{k:lv[k].round(1).tolist() for k in lv}}
for y in range(2023,2027):
    print('ret%',y,{k:round(100*(L[k][:str(y)].iloc[-1]/L[k][:str(y-1)].iloc[-1]-1),1) for k in['NIFTY']+US})
# 2 long history w/ CI
O['long']={u:[[y,round(cor(rets(u,'lag').loc[y]),2)]+ci(rets(u,'lag').loc[y]) for y in Y] for u in US};print('LONG',O['long']['SPX'])
# 3 peers vs SPX
pe={'NIFTY':N,'Nikkei':rd('N225'),'Hang Seng':rd('HSI'),'KOSPI':rd('KOSPI'),'Taiwan':rd('TWSE'),'ASX 200':rd('ASX')}
O['peer']={k:[round(cor(al(v,L['SPX']).loc[y]),2) for y in Y[8:]] for k,v in pe.items()};print('PEER',O['peer'])
print('peer H2 2026',{k:round(cor(al(v,L['SPX'])['2026-07-01':]),2) for k,v in pe.items()})
print('nifty vs peers same date',{k:[round(np.log(pd.concat([N,v],axis=1).dropna()).diff().dropna().loc[y].corr().iloc[0,1],2) for y in Y[8:]] for k,v in pe.items() if k!='NIFTY'})
# 4 lead-lag using common trading dates
d=np.log(pd.concat([N,L['SPX']],axis=1,keys=['n','u']).dropna()).diff().dropna()
O['lead']={y:[round(d.n.corr(d.u.shift(k)[d.index.isin(d.loc[y].index)].reindex(d.loc[y].index)),2) if 0 else round(d.n.loc[y].corr(d.u.shift(k).loc[y]),2) for k in(-3,-2,-1,0,1,2,3)] for y in Y[8:]};print('LEAD',O['lead'])
# 5 vix regime
v=rd('VIX');r=rets('SPX','lag')['2023':].copy();r['v']=v.reindex(r.index.union(v.index)).ffill().shift(1).reindex(r.index)
r['b']=pd.qcut(r.v,3,labels=['low','mid','high']);O['vix']=[[b,round(cor(g),2)]+ci(g)+[round(g.v.min(),1),round(g.v.max(),1),len(g)] for b,g in r.groupby('b',observed=True)];print('VIX',O['vix'])
q=r.drop(r['2025-04-03':'2025-04-15'].index);print('ex Apr25',[(b,round(cor(g),2)) for b,g in q.groupby('b',observed=True)])
R15=rets('SPX','lag');R15['v']=v.reindex(R15.index.union(v.index)).ffill().shift(1).reindex(R15.index);R15=R15[:'2022'];R15['b']=pd.qcut(R15.v,3,labels=['low','mid','high']);print('VIX 2015-22',[(b,round(cor(g),2)) for b,g in R15.groupby('b',observed=True)])
# 6 response buckets
e=[-1,-.015,-.005,.005,.015,1];lb=['< -1.5%','-1.5 to -0.5%','-0.5 to 0.5%','0.5 to 1.5%','> 1.5%']
r['k']=pd.cut(np.expm1(r.u),e,labels=lb);O['bk']=[]
for k,g in r.groupby('k',observed=True):
    s=g.n.std()/np.sqrt(len(g));O['bk'].append([k,round(100*g.n.mean(),2),round(100*1.96*s,2),len(g),round(100*(g.n>0).mean())])
print('BK',O['bk'])
for a,b in(('2023','2023'),('2024','2025'),('2026','2026')):print('bk',a,[(k,round(100*g.n.mean(),2),len(g)) for k,g in r[a:b].groupby('k',observed=True)])
# 7 beta / R2
O['beta']={u:[[y,round(np.polyfit(x.u,x.n,1)[0],2),round(100*cor(x)**2,1)] for y in Y[7:] for x in[rets(u,'lag').loc[y]]] for u in US};print('BETA',O['beta'])
O['sc']=[[round(100*a,2),round(100*b,2)] for a,b in rets('SPX','lag')['2023':][['u','n']].values]
# 8 horizon
H=(1,2,5,10,21);O['hor']={y:[round(cor(rets('SPX','same',k).loc[y]),2) for k in H] for y in Y[8:]};print('HOR',O['hor'])
# 9 usd
fx=rd('USDINR');nu=(N/fx.reindex(N.index.union(fx.index)).ffill().reindex(N.index)).dropna()
print('USD ret',{y:round(cor(al(nu,L['SPX']).loc[y]),2) for y in Y[8:]},'USD lvl',{y:round(pd.concat([nu,L['SPX']],axis=1).dropna().loc[y].corr().iloc[0,1],2) for y in Y[8:]})
# level long history: how often do calendar years come out negative?
O['ll']=[[y,round(aligned('SPX','same').loc[y].corr().iloc[0,1],2)] for y in Y];print('LVL',O['ll'])
P=json.load(open('periods.json'));O['months']=P['d_lag_1m']
json.dump(O,open('deep.json','w'),separators=(',',':'))
