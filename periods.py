import io,contextlib,json
src=open('analyse.py').read().split("out={}")[0]
with contextlib.redirect_stdout(io.StringIO()): exec(src)
P={'1m':lambda i:i.strftime('%Y-%m'),'6m':lambda i:i.year.astype(str)+' H'+((i.month>6)+1).astype(str),'1y':lambda i:i.year.astype(str)}
D={};rows=[]
for m in('lag','same','level'):
  for u in US:
    d=(aligned(u,'same') if m=='level' else rets(u,m))['2023':]
    for w,fn in P.items():
      g=d.groupby(np.asarray(fn(d.index)));c=g.apply(cor);n=g.size()
      D['d_'+m+'_'+w]=list(c.index);D[f'{m}_{u}_{w}']=c.round(2).tolist()
      rows+=[dict(measure=m,index=u,freq=w,period=k,corr=round(c[k],3),sessions=n[k]) for k in c.index]
      x=np.arange(len(c));sl=np.polyfit(x,c.values,1)[0]*{'1m':12,'6m':2,'1y':1}[w]
      pm=np.array([np.polyfit(x,rng.permutation(c.values),1)[0] for _ in range(4000)])*{'1m':12,'6m':2,'1y':1}[w]
      t=f'{m} {u} {w} slope/yr {sl:.3f} p1 {(pm<=sl).mean():.3f} neg {(c<0).sum()}/{len(c)}'
      if w=='1m': t+=' neg by yr '+str((c<0).groupby(c.index.str[:4]).sum().to_dict())+' mean '+str(c.groupby(c.index.str[:4]).mean().round(2).to_dict())+' last6 '+str(c.tail(6).round(2).to_dict())
      else: t+=' '+str(c.round(2).to_dict())
      print(t)
pd.DataFrame(rows).to_csv('period_correlations.csv',index=False)
json.dump(D,open('periods.json','w'),separators=(',',':'))
