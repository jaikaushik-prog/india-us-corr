src=open('wq.py',encoding='utf8').read().split("O={}")[0];exec(src)
def ew(d,h):
    d=d-d.mean();a=1-.5**(1/h);e=lambda x:x.ewm(alpha=a).mean();return e(d.n*d.u)/np.sqrt(e(d.n**2)*e(d.u**2))
for k in('NIFTY','KOSPI','Taiwan','Nikkei'):
    v=ew(daily(A[k],U['S&P']),10)['2023':];print(k,'now',round(v.iloc[-1],2),'share<0 since 2023',round((v<0).mean(),2),'min',round(v.min(),2),v.idxmin().date(),{str(x.date()):round(v.asof(x),2) for x in pd.to_datetime(['2026-08-31','2026-09-30','2026-10-15','2026-10-30','2026-11-06','2026-11-13','2026-11-20'])})
v=ew(daily(N,U['S&P']),10)['2023':];s=(v<0);st=s&~s.shift(1,fill_value=False);print('crossings per yr',st.groupby(v.index.year).sum().to_dict());print([str(x.date()) for x in v.index[st]])
