src=open('wq.py',encoding='utf8').read().split("O={}")[0];exec(src)
S=U['S&P'];d=daily(N,S);w=weekly(N,S,'same');f=pd.read_csv('flows/gh/fb_month.csv');f.index=pd.PeriodIndex(f.month,freq='M')
F=f.net_equity_cr;lv=N.groupby(N.index.to_period('M')).last().shift(1)
L=lambda x:x.groupby(x.index.to_period('Q')).last()
q=d.index.to_period('Q');T=pd.DataFrame({'corr':d.groupby(q)[['n','u']].apply(c),'gap':100*(np.log(L(N)).diff()-np.log(L(S)).diff()),'flow':F.groupby(F.index.asfreq('Q')).sum()/1000,'fs':(F/lv.reindex(F.index)).groupby(F.index.asfreq('Q')).sum(),'sp':100*np.log(L(S)).diff(),'nf':100*np.log(L(N)).diff()})['2021Q2':]
print(T.round(2).to_string())
def p(a,b):
    o=a.corr(b);pm=[np.corrcoef(a.values,rng.permutation(b.values))[0,1] for _ in range(10000)];return round(o,2),round(float((np.abs(pm)>=abs(o)).mean()),3)
def rep(G,l):
    print(l,len(G),'corr~|flow|',p(G['corr'],G.fs.abs()),'corr~flow',p(G['corr'],G.fs),'gap~flow',p(G.gap,G.fs),'SP return~flow',p(G.sp,G.fs))
rep(T,'quarters 2021Q2+');rep(T['2023Q1':],'2023Q1+');rep(T[:'2026Q3'],'excl 26Q4')
m=d.index.to_period('M');M=pd.DataFrame({'corr':d.groupby(m)[['n','u']].apply(c),'fs':F/lv.reindex(F.index)}).dropna();print('monthly',len(M),'corr~|flow|',p(M['corr'],M.fs.abs()),'corr~flow',p(M['corr'],M.fs))
# is pattern low corr => big rotation? top-5 |flow| quarters and 5 lowest corr
print('lowest corr',T['corr'].nsmallest(5).round(2).to_dict());print('largest |flow|',T.fs.abs().nlargest(5).index.astype(str).tolist())
# US fall weeks with FPI buying: flow vs S&P sign months
R=pd.DataFrame({'f':F,'sp':100*np.log(S.groupby(S.index.to_period('M')).last()).diff().reindex(F.index),'nf':100*np.log(N.groupby(N.index.to_period('M')).last()).diff().reindex(F.index)});R['out']=(R.sp<0)&(R.f>0);print('months S&P fell & FPI bought',int(R.out.sum()),'of S&P down months',int((R.sp<0).sum()),'|',[(str(i),round(x.sp,1),round(x.f/1000),round(x.nf,1)) for i,x in R[R.out].iterrows()])
print('flow in S&P up months mean',round(R.f[R.sp>0].mean()),'down',round(R.f[R.sp<0].mean()))
# weekly trend 2023-26 with November: split sample years + leave one week out
for mode in('same','lag'):
    v=weekly(N,S,mode);y={t:round(c(v.loc[str(t)]),2) for t in range(2023,2027)};z=v.loc['2026'];lo=[round(c(z.drop(i)),2) for i in z.index];print(mode,y,'2026 CI',ci(z,2),'LOO range',min(lo),max(lo))
v=weekly(N,S,'same')['2023':];a=v['2023':'2025'];b=v['2026':];o=c(b)-c(a);al=v.values;pm=[]
for _ in range(5000):
    k=rng.permutation(len(al));pm.append(np.corrcoef(al[k[:len(b)]].T)[0,1]-np.corrcoef(al[k[len(b):]].T)[0,1])
print('2026 vs 2023-25 incl Nov',round(c(a),2),round(c(b),2),'p',round(float((np.array(pm)<=o).mean()),3))
ry=(v-v.groupby(v.index.year).transform('mean'));print('full weekly slopes: last col')
