import pandas as pd, numpy as np, json
rng = np.random.default_rng(21)
rd = lambda p: pd.read_csv(p, index_col=0, parse_dates=True).close.dropna()
N, S = rd('data/NIFTY.csv')[:'2026-11-24'], rd('data/SPX.csv')[:'2026-11-24']
f = pd.read_csv('flows/gh/fb_month.csv'); f.index = pd.PeriodIndex(f.month, freq='M')
rr = pd.read_csv('flows/gh/rr.csv'); print('cross-check max diff 2026 (cr):', max(abs(f.net_equity_cr[pd.Period(f'2026-{m:02d}')] - v) for m, v in zip(rr.month_no, rr.equity_net_cr)), 'parts sum diff', (f.net_equity_cr - f.stock_exchange_cr - f.primary_and_others_cr).abs().max())
L = lambda x: x.groupby(x.index.to_period('M')).last()
n, s = L(N), L(S); M = pd.DataFrame({'nr': 100 * np.log(n).diff(), 'sr': 100 * np.log(s).diff(), 'lv': n.shift(1)}); M['rel'] = M.nr - M.sr
us = S.reindex(N.index.union(S.index)).ffill().shift(1).reindex(N.index); d = np.log(pd.DataFrame({'n': N, 'u': us}).dropna()).diff().dropna()
M['corr'] = d.groupby(d.index.to_period('M'))[['n', 'u']].apply(lambda g: g.n.corr(g.u))
M['flow'], M['sec'] = f.net_equity_cr / M.lv, f.stock_exchange_cr / M.lv; M['cr'] = f.net_equity_cr
M['rel_n'], M['nr_n'], M['flow_n'] = M.rel.shift(-1), M.nr.shift(-1), M.flow.shift(-1)
M = M['2021-02':]; F = M[:'2026-10']
out = {'t': []}
def pv(x, y, B=5000):
    z = pd.concat([x, y], axis=1).dropna().values; c = np.corrcoef(z.T)[0, 1]; pm = np.array([np.corrcoef(z[:, 0], rng.permutation(z[:, 1]))[0, 1] for _ in range(B)])
    bs = [np.corrcoef(z[(rng.integers(0, len(z) - 3, len(z) // 3 + 1)[:, None] + np.arange(3)).ravel()].T)[0, 1] for _ in range(2000)]
    return [len(z), round(c, 2), round(float((abs(pm) >= abs(c)).mean()), 4), *np.quantile(bs, [.025, .975]).round(2).tolist()]
T = [('flow vs NIFTY same month', 'flow', 'nr'), ('flow vs NIFTY-S&P same month', 'flow', 'rel'), ('LEAD flow vs next NIFTY-S&P', 'flow', 'rel_n'), ('LEAD flow vs next NIFTY', 'flow', 'nr_n'), ('CHASE NIFTY-S&P vs next flow', 'rel', 'flow_n'), ('flow vs monthly link', 'flow', 'corr'), ('LEAD secondary flow vs next NIFTY-S&P', 'sec', 'rel_n'), ('flow persistence', 'flow', 'flow_n')]
for nm, x, y in T:
    for per, G in (('2021-24', F[:'2024-12']), ('2025-26', F['2025-01':]), ('all', F)):
        a, b = G[x], G[y]
        if per == '2021-24' and y.endswith('_n'): a, b = G[x][:'2024-11'], G[y][:'2024-11']
        r = [nm, per, *pv(a, b)]; out['t'].append(r); print(r)
# regression: rel on flow with S&P control, 2026 attribution using 2021-25 coefficients
G = F[:'2025-12']; A = np.c_[np.ones(len(G)), G.sr, G.flow]; b, *_ = np.linalg.lstsq(A, G.nr, rcond=None); res = G.nr - A @ b; r2 = 1 - (res ** 2).sum() / ((G.nr - G.nr.mean()) ** 2).sum()
b0, *_ = np.linalg.lstsq(A[:, :2], G.nr, rcond=None); r0 = 1 - ((G.nr - A[:, :2] @ b0) ** 2).sum() / ((G.nr - G.nr.mean()) ** 2).sum()
se = np.sqrt(np.diag(np.linalg.inv(A.T @ A)) * (res ** 2).sum() / (len(G) - 3)); print('coef const,S&P,flow', b.round(2), 't', (b / se).round(2), 'R2 S&P only', round(r0, 2), 'with flow', round(r2, 2))
H = M['2026-01':].copy(); H['fit'] = np.c_[np.ones(len(H)), H.sr, H.flow] @ b; H['fit0'] = np.c_[np.ones(len(H)), H.sr] @ b0; print(H[['nr', 'sr', 'cr', 'flow', 'fit', 'fit0']].round(2)); print('2026 sums actual/fit/fitS&P', H[['nr', 'fit', 'fit0']].sum().round(1).to_dict(), 'RMSE fit', round(((H.nr - H.fit) ** 2).mean() ** .5, 2), 'RMSE S&P only', round(((H.nr - H.fit0) ** 2).mean() ** .5, 2))
out['reg'] = [b.round(2).tolist(), (b / se).round(2).tolist(), round(r0, 2), round(r2, 2)]; out['h'] = [[str(i), round(x.nr, 1), round(x.sr, 1), round(x.cr), round(x.fit, 1), round(x.fit0, 1)] for i, x in H.iterrows()]
out['rm'] = [round(((H.nr - H.fit) ** 2).mean() ** .5, 2), round(((H.nr - H.fit0) ** 2).mean() ** .5, 2)]
by = M.groupby(M.index.year).agg(cr=('cr', 'sum'), nr=('nr', 'sum'), rel=('rel', 'sum')).round(1); print(by); out['by'] = {int(k): v for k, v in by.to_dict('index').items()}
q = pd.qcut(F.flow, 3, labels=['sell', 'mid', 'buy']); print(F.groupby(q, observed=True)[['nr', 'rel', 'rel_n', 'nr_n', 'corr']].mean().round(2)); out['terc'] = F.groupby(q, observed=True)[['nr', 'rel', 'rel_n', 'corr']].mean().round(2).to_dict('index')
out['m'] = [[str(i), round(x.cr), round(x.rel, 2), round(x.nr, 2)] for i, x in M.iterrows()]
# daily ~60 sessions: FII/DII
D = pd.DataFrame(json.load(open('flows/gh/na.json', encoding='utf8'))); D['d'] = pd.to_datetime(D.date, format='%d-%b-%Y'); D = D.drop_duplicates('d').set_index('d').sort_index(); D['nr'] = 100 * np.log(N).diff().reindex(D.index); D['us'] = 100 * d.u.reindex(D.index); D = D[['fii_net', 'dii_net', 'nr', 'us']].astype(float)
print('daily', len(D), D.index[0], D.index[-1]); D['nx'] = (100 * np.log(N).diff()).shift(-1).reindex(D.index)
for a, b_ in (('fii_net', 'dii_net'), ('fii_net', 'nr'), ('dii_net', 'nr'), ('fii_net', 'nx'), ('us', 'fii_net'), ('us', 'nr')): r = [a, b_, *pv(D[a], D[b_], 2000)]; out.setdefault('day', []).append(r); print(r)
json.dump(out, open('s2.json', 'w'))
