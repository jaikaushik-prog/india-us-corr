import os,glob
src=open('wq.py',encoding='utf8').read().split("O={}")[0];exec(src)
s=U['S&P'];p=pd.concat([N,s],axis=1,keys=['n','u']).dropna()
for k in(1,2,5,10,21):
    r=np.log(p).diff(k).dropna();print('horizon',k,'2023',round(c(r.loc['2023']),2),'2026',round(c(r.loc['2026']),2),'2026 ex Nov',round(c(r['2026-01-01':'2026-10-31']),2))
for k in('IT','METAL','BANK','FIN','AUTO','INFRA','PHARMA','REALTY','PSUBANK','ENERGY','FMCG'):
    d=daily(rd(f'sect/{k}.csv'),s);print(k,'H2',round(c(d['2026-07-01':]),2),'Jul-Oct',round(c(d['2026-07-01':'2026-10-31']),2),'2026 exNov',round(c(d['2026-01-01':'2026-10-31']),2))
w=weekly(N,s);ag=(np.sign(w.n)==np.sign(w.u));print('agree 2026 ex Nov',round(100*ag['2026-01-01':'2026-10-31'].mean()),len(ag['2026-01-01':'2026-10-31']))
t=pd.concat([pd.read_csv(x) for x in glob.glob('macro/tsy*.csv')]);t['Date']=pd.to_datetime(t.Date,format='%m/%d/%Y');Y=t.set_index('Date').sort_index()['10 Yr'].dropna()
v=Y.reindex(N.index.union(Y.index)).ffill().shift(1).reindex(N.index).diff();z=pd.DataFrame({'n':np.log(N).diff(),'u':v}).dropna();print('y10 2026',round(c(z.loc['2026']),2),'exNov',round(c(z['2026-01-01':'2026-10-31']),2))
