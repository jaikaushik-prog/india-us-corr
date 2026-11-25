src=open('wq.py',encoding='utf8').read().split("O={}")[0];exec(src)
for k in A:
    d=daily(A[k],U['S&P']);a=d['2026-07-01':'2026-10-31'];b=d['2026-11-01':]
    print(k,'H2',round(c(d['2026-07-01':]),2),'Jul-Oct',round(c(a),2),len(a),ci(a,5),'Nov',round(c(b),2),len(b),'ex-Nov 2026',round(c(d['2026':'2026-10-31']),2))
d=daily(N,U['S&P']);print((100*d['2026-11-01':]).round(1).T.to_string())
v=d['2026-07-01':];print('Spearman H2',round(c(v.rank()),2),'ex top2 |n|',round(c(v.drop(v.n.abs().nlargest(2).index)),2))
for k in('Nasdaq','Dow'): e=daily(N,U[k]);print(k,'H2',round(c(e['2026-07-01':]),2),'Jul-Oct',round(c(e['2026-07-01':'2026-10-31']),2))
p=pd.concat([N,U['S&P']],axis=1,keys=['n','u']).dropna();print('price-level 2026',round(c(p['2026']) if 0 else c(p.loc['2026']),2),'ex Nov',round(c(p['2026-01-01':'2026-10-31']),2))
