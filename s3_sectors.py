import pandas as pd, numpy as np, json, glob
rng = np.random.default_rng(3); END = '2026-11-24'
rd = lambda p: pd.read_csv(p, index_col=0, parse_dates=True).close.dropna()[:END]
S, Q = rd('data/SPX.csv'), rd('data/COMP.csv')
t = pd.concat([pd.read_csv(x) for x in glob.glob('macro/tsy*.csv')]); t['Date'] = pd.to_datetime(t.Date, format='%m/%d/%Y'); Y = t.set_index('Date').sort_index()['10 Yr'].dropna()
names = {'IT': 'IT', 'BANK': 'Banks', 'PSUBANK': 'PSU banks', 'FIN': 'Financials', 'METAL': 'Metals', 'ENERGY': 'Energy', 'AUTO': 'Autos', 'PHARMA': 'Pharma', 'FMCG': 'FMCG', 'REALTY': 'Realty', 'INFRA': 'Infra'}
A = {'NIFTY': rd('data/NIFTY.csv'), **{k: rd(f'sect/{k}.csv') for k in names}}
def al(x, u, diff=False):
    v = u.reindex(x.index.union(u.index)).ffill().shift(1).reindex(x.index)
    return pd.DataFrame({'n': np.log(x).diff(), 'u': v.diff() if diff else np.log(v).diff()}).dropna()['2015':]
PE = {'2015-20': ('2015', '2020'), '2021-26': ('2021', '2026'), '2015-22': ('2015', '2022'), '2023': ('2023', '2023'), '2024': ('2024', '2024'), '2025': ('2025', '2025'), '2026': ('2026', '2026'), 'H2 2026': ('2026-07-01', '2026-12-31')}
out = {}
for nm, u, df in (('spx', S, 0), ('ndx', Q, 0), ('y10', Y, 1)):
    R = {}
    for k, x in A.items():
        d = al(x, u, df); R[k] = {p: round(d[a:b].n.corr(d[a:b].u), 2) for p, (a, b) in PE.items()}
        R[k]['beta'] = round(np.polyfit(d['2021':].u, d['2021':].n, 1)[0], 2)
    T = pd.DataFrame(R).T; print('\n', nm, '\n', T.to_string()); out[nm] = R
    s = T.drop('NIFTY'); rho = s['2015-20'].rank().corr(s['2021-26'].rank()); pm = [s['2015-20'].rank().corr(pd.Series(rng.permutation(s['2021-26'].rank().values), index=s.index)) for _ in range(10000)]
    out[nm + '_stab'] = [round(rho, 2), round(float((np.array(pm) >= rho).mean()), 4)]; print('stability', out[nm + '_stab'])
# IT: own US link after removing NIFTY the same day
for k in ('IT', 'BANK', 'METAL', 'PHARMA'):
    d = al(A[k], Q).join(np.log(A['NIFTY']).diff().rename('m'), how='inner').dropna()
    for p in ('2015-20', '2021-26', '2026', 'H2 2026'):
        a, b = PE[p]; z = d[a:b]; e1 = z.n - np.polyval(np.polyfit(z.m, z.n, 1), z.m); e2 = z.u - np.polyval(np.polyfit(z.m, z.u, 1), z.m); print('partial corr w Nasdaq given NIFTY', k, p, round(e1.corr(e2), 2))
        out.setdefault('part', {}).setdefault(k, {})[p] = round(e1.corr(e2), 2)
# bootstrap CI for IT minus bank and H2-2026
d = al(A['IT'], S).join(al(A['BANK'], S).n.rename('b'), how='inner').dropna()
for p in ('2015-20', '2021-26', 'H2 2026'):
    a, b = PE[p]; z = d[a:b]; v = z.values; bs = []
    for _ in range(2000):
        i = (rng.integers(0, len(v) - 5, len(v) // 5 + 1)[:, None] + np.arange(5)).ravel(); q = v[i]; bs.append(np.corrcoef(q[:, 0], q[:, 1])[0, 1] - np.corrcoef(q[:, 2], q[:, 1])[0, 1])
    r = [round(z.n.corr(z.u) - z.b.corr(z.u), 2), *np.quantile(bs, [.025, .975]).round(2).tolist()]; out['itbank ' + p] = r; print('IT-bank corr diff', p, r)
yr = {k: {y: round(100 * (x[:str(y)].iloc[-1] / x[:str(y - 1)].iloc[-1] - 1), 1) for y in (2023, 2024, 2025, 2026)} for k, x in A.items()}; print(pd.DataFrame(yr).T); out['ret'] = yr; out['names'] = names
# IT residual link by year (S&P)
print('IT by yr', {y: round(al(A['IT'], S)[str(y):str(y)].corr().iloc[0, 1], 2) for y in range(2015, 2027)})
json.dump(out, open('s3.json', 'w'))
