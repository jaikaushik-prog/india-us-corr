src=open('wq.py',encoding='utf8').read().split("O={}")[0];exec(src)
w=weekly(N,U['S&P']);print((100*w[-9:]).round(1).to_string())
v=w[-52:];x=v[:'2026-10-31'];print('last52 all',round(c(v),2),'ex Nov',round(c(x),2),len(x),ci(x),'spearman all',round(c(v.rank()),2),'ex nov',round(c(x.rank()),2))
for a,b in(('2023','2024'),('2025','2025'),('2026-01-01','2026-06-30'),('2026-07-01','2026-10-31'),('2026','2026-10-31')):
    z=w[a:b];print(a,b,len(z),round(c(z),2),'spearman',round(c(z.rank()),2))
for k in range(len(v)):
    pass
d=[(str(v.index[i].date()),round(c(v.drop(v.index[i])),2)) for i in range(len(v))];print('leave-one-out min/max',min(d,key=lambda t:t[1]),max(d,key=lambda t:t[1]))
y=pd.Series({t:c(w.loc[str(t)][:'2026-10-31']) for t in range(2015,2027)});print('yearly ex Nov26 trend 2015+',tr(y,1),'2026',round(y[2026],2))
