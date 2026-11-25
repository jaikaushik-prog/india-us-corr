import pandas as pd,numpy as np,json
rng=np.random.default_rng(17);END='2026-11-24'
def rd(p):
    s=pd.read_csv(p,index_col=0,parse_dates=True).close.dropna()[:END];return s[~s.index.duplicated()]
N=rd('data/NIFTY.csv');U={'S&P':rd('data/SPX.csv'),'Nasdaq':rd('data/COMP.csv'),'Dow':rd('data/DJI.csv')}
A={'NIFTY':N,'Nikkei':rd('data/N225.csv'),'Hang Seng':rd('data/HSI.csv'),'KOSPI':rd('data/KOSPI.csv'),'Taiwan':rd('data/TWSE.csv'),'ASX':rd('data/ASX.csv')}
def pair(x,u,mode='lag'):
    v=u.reindex(x.index.union(u.index)).ffill()
    v=v.shift(1) if mode=='lag' else v
    return pd.DataFrame({'n':x,'u':v.reindex(x.index)}).dropna()['2014-12-01':]
def weekly(x,u,mode='lag'): 
    d=pair(x,u,mode).resample('W-FRI').last().dropna();r=np.log(d).diff().dropna();return r['2015':END]
daily=lambda x,u:np.log(pair(x,u)).diff().dropna()['2015':]
c=lambda g:g.n.corr(g.u)
def tr(s,per):
    x=np.arange(len(s));b=np.polyfit(x,s.values,1)[0];pm=np.array([np.polyfit(x,rng.permutation(s.values),1)[0] for _ in range(5000)]);return [round(b*per,3),round(float((pm<=b).mean()),3),len(s)]
def ci(v,b=4,B=3000):
    v=v.values;q=[np.corrcoef(v[(rng.integers(0,len(v)-b+1,len(v)//b+1)[:,None]+np.arange(b)).ravel()].T)[0,1] for _ in range(B)];return np.quantile(q,[.025,.975]).round(2).tolist()
O={}
for k,u in U.items():
    for m in('lag','same'):
        w=weekly(N,u,m);y={t:round(c(w[str(t)]),2) for t in range(2015,2027)} if 0 else {t:round(c(w.loc[str(t)]),2) for t in range(2015,2027)}
        print('WEEKLY',k,m,y,'last52',round(c(w[-52:]),2),ci(w[-52:]),'last26',round(c(w[-26:]),2),ci(w[-26:]))
        O[f'w|{k}|{m}']=[y,round(c(w[-52:]),2),ci(w[-52:]),round(c(w[-26:]),2),ci(w[-26:])]
    w=weekly(N,u);ag=(np.sign(w.n)==np.sign(w.u));print('  same-direction weeks %',{t:round(100*ag.loc[str(t)].mean()) for t in range(2015,2027)},'H2 2026',round(100*ag['2026-07-01':].mean()),len(ag['2026-07-01':]))
    O[f'ag|{k}']={t:round(100*ag.loc[str(t)].mean()) for t in range(2015,2027)}
    d=daily(N,u);qd=d.groupby(d.index.to_period('Q'))[['n','u']].apply(c);qw=w.groupby(w.index.to_period('Q'))[['n','u']].apply(c)
    print('  QTR daily',{str(i):round(v,2) for i,v in qd['2023Q1':].items()});print('  QTR weekly',{str(i):round(v,2) for i,v in qw['2023Q1':].items()})
    for nm,s,per in(('qtr daily',qd,4),('qtr weekly',qw,4)):
        O[f'{nm}|{k}']={'s':{str(i):round(v,2) for i,v in s.items()},'t23':tr(s['2023Q1':],4),'t15':tr(s,4),'neg23':int((s['2023Q1':]<0).sum())};print('  trend',nm,'2023+',O[f'{nm}|{k}']['t23'],'2015+',O[f'{nm}|{k}']['t15'],'neg',O[f'{nm}|{k}']['neg23'])
    a=pd.Series({t:v for t,v in O[f'w|{k}|lag'][0].items()});print('  trend weekly by yr 2015+',tr(a,1),'2023+',tr(a[a.index>=2023],1))
    L=lambda s:s.groupby(s.index.to_period('Q')).last();Q=pd.DataFrame({'n':np.log(L(N)).diff(),'u':np.log(L(u)).diff()})['2015Q1':]
    O[f'qr|{k}']=[round(c(Q[:'2022Q4']),2),round(c(Q['2023Q1':]),2),round(c(Q['2025Q1':]),2),ci(Q[:'2022Q4'],2),ci(Q['2023Q1':],2)];print('  QTR RETURNS corr 15-22,23-26,25-26',O[f'qr|{k}'],'rel by q %',{str(i):round(100*(x.n-x.u),1) for i,x in Q['2023Q1':].iterrows()},'opp-sign q 2023+',int((np.sign(Q.n)!=np.sign(Q.u))['2023Q1':].sum()),'/',len(Q['2023Q1':]),'2015-22',int((np.sign(Q.n)!=np.sign(Q.u))[:'2022Q4'].sum()),'/',len(Q[:'2022Q4']))
    if k=='S&P': O['Q']=[[str(i),round(100*x.n,1),round(100*x.u,1)] for i,x in Q['2023Q1':].iterrows()]
    # rolling weekly 2023+ trend against constant-correlation null (block resample pairs)
    for st in('2023','2015'):
        z=w[st:];k2=26;rc=lambda v:pd.Series(v[:,0]).rolling(k2).corr(pd.Series(v[:,1])).dropna().values;o=rc(z[['n','u']].values);x=np.arange(len(o));b=np.polyfit(x,o,1)[0];ns=[]
        for _ in range(1500):
            i=(rng.integers(0,len(z)-3,len(z)//4+1)[:,None]+np.arange(4)).ravel()[:len(z)];q=rc(z[['n','u']].values[i]);ns.append(np.polyfit(x[:len(q)],q,1)[0])
        r=[round(b*52,3),round(float((np.array(ns)<=b).mean()),3),round(o[-1],2),round(float((o<0).mean()),2)];O[f'r26|{k}|{st}']=r;print('  rolling 26wk slope/yr,p,now,neg share',st,r)
    # break test: last 52 weeks vs prior since 2023 and since 2015
    for st in('2023','2015'):
        p=w[st:][:-52];q=w[-52:];o=c(q)-c(p);al=w[st:];pm=[]
        for _ in range(3000):
            i=rng.permutation(len(al));pm.append(c(al.iloc[i[-52:]])-c(al.iloc[i[:-52]]))
        r=[round(c(p),2),round(c(q),2),round(float((np.array(pm)<=o).mean()),3)];O[f'br|{k}|{st}']=r;print('  last52 vs before',st,r)
print('\nPEERS vs S&P')
for k,x in A.items():
    w=weekly(x,U['S&P']);d=daily(x,U['S&P']);qd=d.groupby(d.index.to_period('Q'))[['n','u']].apply(c)
    r={'w':{t:round(c(w.loc[str(t)]),2) for t in range(2023,2027)},'w52':round(c(w[-52:]),2),'w26':round(c(w[-26:]),2),'q':{str(i):round(v,2) for i,v in qd['2025Q1':].items()},'t23':tr(qd['2023Q1':],4)};O['peer|'+k]=r;print(k,r)
json.dump(O,open('wq.json','w'))
