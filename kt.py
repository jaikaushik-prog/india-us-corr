src=open('wq.py',encoding='utf8').read().split("O={}")[0];exec(src)
S=U['S&P'];X={'NIFTY':N,'S&P':S,'Nasdaq':U['Nasdaq'],'Korea':A['KOSPI'],'Taiwan':A['Taiwan'],'Japan':A['Nikkei'],'HK':A['Hang Seng'],'Aus':A['ASX']}
L=lambda x:x.groupby(x.index.to_period('Q')).last()
R=pd.DataFrame({k:100*L(x).pct_change() for k,x in X.items()})['2023Q1':];print(R.round(1).to_string())
mo=pd.DataFrame({k:100*x.groupby(x.index.to_period('M')).last().pct_change() for k,x in X.items()})['2026-07':];print(mo.round(1).to_string())
for k in('Korea','Taiwan'):
    z=np.log(pd.concat([N,X[k]],axis=1,keys=['n','u']).dropna()).diff().dropna()['2023':];g=z.groupby(z.index.to_period('Q'))[['n','u']].apply(c);l=daily(X[k],S);h=l.groupby(l.index.to_period('Q'))[['n','u']].apply(c)['2023Q1':]
    print(k,'with NIFTY same date',{str(i):round(v,2) for i,v in g.items()});print(k,'with S&P',{str(i):round(v,2) for i,v in h.items()})
    for q,a,b in(('24Q1','2024-01-01','2024-03-31'),('25Q3','2025-07-01','2025-09-30'),('26Q4','2026-10-01','2026-11-24')): print('  ',q,round(c(z[a:b]),2),ci(z[a:b],5))
print('India-minus-Korea vs India-minus-S&P corr by quarter',round((R.NIFTY-R.Korea).corr(R.NIFTY-R['S&P']),2),'ex 26Q4',round((R.NIFTY-R.Korea)[:-1].corr((R.NIFTY-R['S&P'])[:-1]),2))
