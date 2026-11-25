import urllib.request,json,time
src=open('wq.py',encoding='utf8').read().split("O={}")[0];exec(src)
def y(s):
    r=json.load(urllib.request.urlopen(urllib.request.Request(f'https://query1.finance.yahoo.com/v8/finance/chart/{s}?period1=1640000000&period2={int(time.time())}&interval=1d',headers={'User-Agent':'Mozilla/5.0'}),timeout=60))['chart']['result'][0]
    ix=pd.to_datetime([pd.Timestamp(t,unit='s',tz='UTC').tz_convert('America/New_York').date() for t in r['timestamp']]);x=pd.Series(r['indicators']['adjclose'][0]['adjclose'],index=ix).dropna();return x[~x.index.duplicated()][:END]
I,P=y('INDA'),y('SPY');e=np.log(pd.concat([I,P],axis=1,keys=['n','u']).dropna()).diff().dropna()['2023':]
S=U['S&P'];d=daily(N,S)['2023':];fx=rd('data/USDINR.csv');Nd=(N/fx.reindex(N.index.union(fx.index)).ffill().reindex(N.index)).dropna()
qk=lambda x:x.groupby(x.index.to_period('Q'))
L=lambda x:qk(x).last()
T=pd.DataFrame({'daily':qk(d)[['n','u']].apply(c),'inda':qk(e)[['n','u']].apply(c),'N%':100*L(N).pct_change(),'N$%':100*L(Nd).pct_change(),'S%':100*L(S).pct_change()})['2023Q1':];T['gap$']=T['N$%']-T['S%'];print(T.round(2).to_string())
print('corr(daily corr, gap$)',round(T.daily.corr(T['gap$']),2),'corr(daily corr,|gap|)',round(T.daily.corr(T['gap$'].abs()),2),'ex Q4 26',round(T.daily[:-1].corr(T['gap$'][:-1].abs()),2))
def pp(a,b):
    o=abs(a.corr(b));pm=[abs(np.corrcoef(a.values,rng.permutation(b.values))[0,1]) for _ in range(5000)];return round(float((np.array(pm)>=o).mean()),3)
print('p |gap|',pp(T.daily,T['gap$'].abs()),'p gap',pp(T.daily,T['gap$']))
g=T['gap$'].abs();print('quarters with |gap|>8 and corr>.1:',[(str(i),round(r.daily,2),round(r['gap$'],1)) for i,r in T.iterrows() if abs(r['gap$'])>8])
# 13-week pooled
wk=d.index.to_period('W-FRI');ws=sorted(set(wk));gp={w:d[wk==w][['n','u']].values for w in ws}
def pooled(arrs,k=13): return np.array([np.corrcoef(np.vstack(arrs[i-k+1:i+1]).T)[0,1] for i in range(k-1,len(arrs))])
A0=[gp[w] for w in ws];o=pooled(A0);print('13wk: now',o[-1].round(2),'min',o.min().round(2),'neg share',(o<0).mean().round(2))
def dips(v):
    n=0;i=0;s=v<0;gap=99
    for b in s:
        if b:
            if gap>=8:n+=1
            gap=0
        else: gap+=1
    return n
print('episodes below 0 (8wk+ apart)',dips(o))
R=[]
for _ in range(1500):
    idx=rng.integers(0,len(A0),len(A0));z=pooled([A0[i] for i in idx]);R.append((dips(z),z.min(),(z<0).mean(),z[-1]))
R=np.array(R);print('null constant link: mean dips',R[:,0].mean().round(1),'P(>=obs)',(R[:,0]>=dips(o)).mean().round(2),'median min',np.median(R[:,1]).round(2),'neg share',R[:,2].mean().round(3),'P(share>=obs)',(R[:,2]>=(o<0).mean()).mean().round(2),'P(now<=obs)',(R[:,3]<=o[-1]).mean().round(3))
# persistence of true regimes: shuffle of weeks vs actual lag-1 of 13w non-overlap
nb=[np.corrcoef(np.vstack(A0[i:i+13]).T)[0,1] for i in range(0,len(A0)-12,13)];print('non-overlap 13wk',np.round(nb,2),'lag1',round(np.corrcoef(nb[:-1],nb[1:])[0,1],2))
sw=np.array([np.corrcoef(a.T)[0,1] for a in A0 if len(a)>=4]);print('single-week: neg share',(sw<0).mean().round(2),'sd',sw.std().round(2));sim=[]
for _ in range(200):
    al=d[['n','u']].values
    for k in range(5): sim.append(np.corrcoef(al[rng.integers(0,len(al),5)].T)[0,1])
print('random 5-day draws neg share',(np.array(sim)<0).mean().round(2))
w=weekly(N,S,'same');w2=weekly(N,S)
for m,b in(('3M','2026-08-25'),('6M','2026-05-25'),('12M','2025-11-25')):
    x=d[b:];print(m,'daily lag',round(c(x),2),'CI',ci(x,5),'weekly same',round(c(w[b:]),2),len(w[b:]),ci(w[b:],2),'weekly lag',round(c(w2[b:]),2),'| to Oct: daily',round(c(x[:'2026-10-31']),2),'weekly same',round(c(w[b:'2026-10-31']),2),len(w[b:'2026-10-31']))
z=e.loc['2026-10-01':];print('INDA Q4 ci',ci(z,5),len(z),'Oct',round(c(z[:'2026-10-31']),2),'Nov',round(c(z['2026-11-01':]),2));z=e['2025-07-01':'2025-09-30'];print('INDA 25Q3',ci(z,5))
for q,a,b in(('24Q1','2024-01-01','2024-03-31'),('25Q3','2025-07-01','2025-09-30'),('25Q4','2025-10-01','2025-12-31'),('26Q4','2026-10-01','2026-12-31')): print(q,'daily CI',ci(d[a:b],5),len(d[a:b]))
print('weeks ending:',(100*w['2026-09-25':]).round(1).values.tolist())

# variants for the bold line end point (he shows about -0.16)
for lab,x in (('lag',d),('same',daily(N,S) if 0 else np.log(pair(N,S,'same')).diff().dropna()['2023':])):
    k=x.index.to_period('W-FRI');gs=[x[k==q] for q in sorted(set(k))]
    for m in range(0,3):
        g=gs[len(gs)-13-m:len(gs)-m];z=pd.concat(g);dm=pd.concat([q-q.mean() for q in g]);print(lab,'ending',str(g[-1].index[-1].date()),'pooled',round(c(z),2),'demeaned within week',round(c(dm),2),'rank',round(c(z.rank()),2),'mean of weekly r',round(np.nanmean([c(q) for q in g if len(q)>2]),2))
x=pd.DataFrame({'n':np.log(N).diff(),'u':np.log(S).diff().reindex(N.index.union(S.index)).shift(1).reindex(N.index)}).dropna()['2023':];k=x.index.to_period('W-FRI');gs=[x[k==q] for q in sorted(set(k))]
g=gs[-13:];z=pd.concat(g);dm=pd.concat([q-q.mean() for q in g]);print('strict t-1',round(c(z),2),'demeaned',round(c(dm),2),len(z))
