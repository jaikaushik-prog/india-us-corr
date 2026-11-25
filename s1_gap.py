import pandas as pd, numpy as np, json, sys
sys.path.insert(0, '../momentum_bot'); from costs import side_costs_bp
f = pd.read_csv('../NIFTY_FUT_5MIN_2020_2024.csv', parse_dates=['datetime']).drop_duplicates('datetime').sort_values('datetime')
f['d'] = f.datetime.dt.normalize(); f['t'] = f.datetime.dt.strftime('%H:%M')
p = f.pivot(index='d', columns='t', values='open'); c = f.groupby('d').close.last(); n = f.groupby('d').size()
S = pd.read_csv('data/SPX.csv', index_col=0, parse_dates=True).close.dropna()
g = pd.DataFrame({'o': p['09:15'], 'e': p['09:20'], 'x': p['15:20'], 'c': c, 'n': n}); g['pc'] = g.c.shift(1)
g['sp'] = S.reindex(g.index.union(S.index)).ffill().shift(1).reindex(g.index)
g['us'] = g.sp.pct_change()
g = g[(g.n >= 70)].dropna(); g = g[g.index >= '2020-01-02']
g['gap'], g['rest'], g['tot'] = g.o / g.pc - 1, g.x / g.e - 1, g.x / g.pc - 1; g['first5'] = g.e / g.o - 1
print('days', len(g), g.index[0], g.index[-1], 'gap>3%', (g.gap.abs() > .03).sum(), 'rest max', g.rest.abs().max())
out = {'slope': [], 'bk': [], 'tr': []}
P = {'2020-22': g[:'2022'], '2023-24': g['2023':]}
for k, d in {**P, 'all': g, 'ex Mar-May 2020': g.drop(g['2020-02-20':'2020-05-31'].index)}.items():
    r = [k, len(d)]
    for y in ('tot', 'gap', 'first5', 'rest'):
        b = np.polyfit(d.us, d[y], 1)[0]; bs = [np.polyfit(q.us, q[y], 1)[0] for s in range(800) for q in [d.sample(len(d), replace=True, random_state=s)]]
        r += [round(b, 3), *np.quantile(bs, [.025, .975]).round(3).tolist()]
    out['slope'].append(r); print('slope per 1% tot/gap/first5/rest', r)
lb = ['< -1.5%', '-1.5 to -0.5%', '-0.5 to 0.5%', '0.5 to 1.5%', '> 1.5%']
g['k'] = pd.cut(g.us, [-1, -.015, -.005, .005, .015, 1], labels=lb)
for k, d in g.groupby('k', observed=True):
    r = [k, len(d), *[round(100 * d[y].mean(), 3) for y in ('gap', 'first5', 'rest')], round(196 * d.rest.std() / len(d) ** .5, 3), round(100 * ((d.rest > 0)).mean())]; out['bk'].append(r); print(r)
for th in (.005, .01, .015):
    for k, d in P.items():
        d = d[d.us.abs() >= th]; s = np.sign(d.us); gr = s * d.rest * 1e4
        co = np.array([sum(side_costs_bp(i.date())) for i in d.index]); nt = gr - co; t = lambda x: x.mean() / x.std() * len(x) ** .5
        r = [th, k, len(d), round(gr.mean(), 1), round(t(gr), 2), round(co.mean(), 1), round(nt.mean(), 1), round(t(nt), 2), round((gr - 2 * co).mean(), 1), round(100 * (nt > 0).mean())]; out['tr'].append(r); print('follow', r, 'by yr', nt.groupby(nt.index.year).mean().round(1).to_dict())
json.dump(out, open('s1.json', 'w'))
