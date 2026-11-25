import pandas as pd, numpy as np, json
rng = np.random.default_rng(8); rd = lambda p: pd.read_csv(p, index_col=0, parse_dates=True).close.dropna()
S = rd('data/SPX.csv'); names = {'IT': 'IT', 'BANK': 'Banks', 'PSUBANK': 'PSU banks', 'FIN': 'Financials', 'METAL': 'Metals', 'ENERGY': 'Energy', 'AUTO': 'Autos', 'PHARMA': 'Pharma', 'FMCG': 'FMCG', 'REALTY': 'Realty', 'INFRA': 'Infra'}
N = rd('data/NIFTY.csv'); A = {'NIFTY': N, **{k: rd(f'sect/{k}.csv') for k in names}}
u = np.log(S.reindex(N.index.union(S.index)).ffill().shift(1).reindex(N.index)).diff()
R = pd.DataFrame({k: np.log(x).diff() for k, x in A.items()}).reindex(N.index); R['u'] = u; R = R.dropna()['2015':'2024-12-31']
a, b = R[:'2020'], R['2021':]; K = list(names); out = {'names': {'NIFTY': 'NIFTY 50', **names}, 'tab': {}}
bt = lambda d, k: np.polyfit(d.u, d[k], 1)[0]
b1 = pd.Series({k: bt(a, k) for k in K}); dn = b[b.u <= -.015]; up = b[b.u >= .015]; print('down days', len(dn), 'up', len(up))
act = dn[K].mean() * 100; rho = b1.rank().corr(act.rank()); sg = -rho
pm = np.array([-b1.rank().corr(pd.Series(rng.permutation(act.rank().values), index=K)) for _ in range(10000)]); p = float((pm >= sg).mean()); print('OOS Spearman (higher beta -> bigger fall)', round(sg, 2), 'p', p); out['oos'] = [round(sg, 2), round(p, 3), len(dn)]
aft = b1.rank().corr(pd.Series({k: bt(b, k) for k in K}).rank()); print('beta rank 2015-20 vs 2021-24', round(aft, 2))
out['rankstab'] = round(aft, 2)
for k in ['NIFTY'] + K:
    bs = []
    for _ in range(1000):
        i = (rng.integers(0, len(b) - 5, len(b) // 5 + 1)[:, None] + np.arange(5)).ravel(); q = b.iloc[i]; bs.append(np.polyfit(q.u, q[k], 1)[0])
    out['tab'][k] = [round(bt(a, k), 2), round(bt(b, k), 2), *np.quantile(bs, [.05, .95]).round(2).tolist(), round(100 * dn[k].mean(), 2), round(100 * up[k].mean(), 2), round(100 * (dn[k] < 0).mean()), round(100 * b[k].std(), 2), round(b[k].corr(b.u), 2)]; print(k, out['tab'][k])
# residual covariance for calculator (daily %, 2021-24)
E = pd.DataFrame({k: 100 * (b[k] - np.polyval(np.polyfit(b.u, b[k], 1), b.u)) for k in K}); out['cov'] = E.cov().round(4).values.tolist(); out['K'] = K
json.dump(out, open('s3b.json', 'w'))
