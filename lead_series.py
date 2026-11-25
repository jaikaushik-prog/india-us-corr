import json
src=open('wq.py',encoding='utf8').read().split("O={}")[0];exec(src)
d=daily(N,U['S&P']);r=d.n.rolling(63).corr(d.u)
z=d-d.mean();a=1-.5**(1/10);e=lambda x:x.ewm(alpha=a).mean();f=e(z.n*z.u)/np.sqrt(e(z.n**2)*e(z.u**2))
s=pd.DataFrame({'slow':r,'fast':f})['2023':];s=s.iloc[::-2][::-1]
json.dump({'d':[str(x.date()) for x in s.index],'slow':s.slow.round(2).tolist(),'fast':s.fast.round(2).tolist()},open('lead_series.json','w'),separators=(',',':'));print(len(s),s.tail(2))
