import io,contextlib,json
src=open('analyse.py').read().split("out={}")[0]
with contextlib.redirect_stdout(io.StringIO()): exec(src)
for u in US:
    r=rets(u,'lag');print(u,'2026 H1 %.2f H2 %.2f'%(cor(r['2026-01-01':'2026-06-30']),cor(r['2026-07-01':])))
    for nm in ['lag','same']:
        R=rets(u,nm)['2023':];a=R.values;cm=[];
        for _ in range(500):
            z=pd.DataFrame(a[mbb_idx(len(a),10)]);c=z[0].rolling(21).corr(z[1]).dropna();cm.append(((c<0).mean(),c.min(),c.iloc[-1]))
        cm=np.array(cm);print('  1m null',nm,'neg share mean %.2f'%cm[:,0].mean(),'min 5/50/95',np.quantile(cm[:,1],[.05,.5,.95]).round(2),'P(1m<=now)',(cm[:,2]<=rets(u,nm)['n'].rolling(21).corr(rets(u,nm)['u']).iloc[-1]).mean())
    # level null: pairs keep their true daily link, independent of order
    d=aligned(u,'same');a=np.log(d).diff().dropna()['2023':].values
    for k in(21,126,252):
        nl=[]
        for _ in range(4000):
            p=np.exp(a[mbb_idx(len(a),10)][:k-1].cumsum(0));nl.append(np.corrcoef(p.T)[0,1])
        nl=np.array(nl);now=d.n.rolling(k).corr(d.u).iloc[-1];print('  level null',k,'P(neg) %.2f'%(nl<0).mean(),'P(<=now %.2f) %.3f'%(now,(nl<=now).mean()))
    w=np.log(d.resample('W-FRI').last()).diff().dropna();p=w['2023':'2025'];q=w.iloc[-52:]
    f=lambda x:np.array([np.corrcoef(x.values[rng.integers(0,len(x),len(x))].T)[0,1] for _ in range(5000)])
    # gap defined on exact disjoint samples
    p=w['2023':].iloc[:-52];bp,bq=f(p),f(q);dd=bq-bp
    print('  weekly same prior %.2f [%.2f,%.2f] last52 %.2f [%.2f,%.2f] diff CI [%.2f,%.2f]'%(cor(p),*np.quantile(bp,[.025,.975]),cor(q),*np.quantile(bq,[.025,.975]),*np.quantile(dd,[.025,.975])))
D={}
for m in('lag','same','level'):
  for u in US:
    d=aligned(u,'same') if m=='level' else rets(u,m)
    for w,k in W.items():
      c=d.n.rolling(k).corr(d.u)['2023':];c=c.iloc[::-2][::-1]
      if 'd_'+m not in D: D['d_'+m]=[str(x.date()) for x in c.index]
      assert len(D['d_'+m])==len(c); D[f'{m}_{u}_{w}']=c.round(2).tolist()
json.dump(D,open('roll.json','w'),separators=(',',':'))
