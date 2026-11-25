import pandas as pd, numpy as np, json
rng = np.random.default_rng(5)
n = pd.read_csv('../nexus-volatility-research/outputs/nifty50_tri_20261103/nifty50_tri_daily_2012_2026.csv', parse_dates=['Date']).set_index('Date')['Total Returns Index'].astype(float)[:'2024-12-31']
s = pd.read_csv('sect/SPXTR.csv', index_col=0, parse_dates=True).close[:'2024-12-31']; fx = pd.read_csv('data/USDINR.csv', index_col=0, parse_dates=True).close.dropna()[:'2024-12-31']
print('fx daily >3%', fx.pct_change().abs().loc[lambda x: x > .03].to_dict())
def weekly(lag=0):
    ix = pd.date_range('2014-12-26', '2024-12-27', freq='W-FRI'); a = lambda x: x.reindex(ix, method='ffill')
    ss = s.shift(lag); return pd.DataFrame({'N': a(n), 'U': a(ss) * a(fx), 'H': a(ss)}).pct_change().dropna(), ix
def port(R, col, w, cost=.00125):
    v = np.array([1 - w, w]); V = [1.]; tot = 1.; tc = 0
    m = R.index.month
    for i, (a, b) in enumerate(R[['N', col]].values):
        v = v * [1 + a, 1 + b]; tot = v.sum()
        if i + 1 < len(R) and m[i + 1] != m[i] and 0 < w < 1:
            tr = abs(v - tot * np.array([1 - w, w])).sum(); tot -= tr * cost; v = tot * np.array([1 - w, w])
        V.append(tot)
    return np.array(V)
def met(V, idx):
    r = V[1:] / V[:-1] - 1; dd = (V / np.maximum.accumulate(V) - 1).min(); mm = pd.Series(V[1:], idx).resample('ME').last(); mr = mm.pct_change().dropna()
    return [round(100 * (V[-1] ** (52 / len(r)) - 1), 1), round(100 * r.std() * 52 ** .5, 1), round(100 * dd, 1), round(100 * mr.min(), 1)]
out = {}
for lag in (0, 1):
    R, ix = weekly(lag)
    for per, a, b in (('2015-19', '2015', '2019'), ('2020-24', '2020', '2024'), ('2015-24', '2015', '2024')):
        Z = R[a:b]; print('\nlag', lag, per, 'corr NIFTY/US rupee', round(Z.N.corr(Z.U), 2), 'hedged', round(Z.N.corr(Z.H), 2))
        for col in ('U', 'H'):
            for w in (0, .1, .2, .3, .4, .5, 1.):
                r = met(port(Z, col, w), Z.index); out[f'{lag}|{per}|{col}|{int(w * 100)}'] = r
                if lag == 0 or w in (0, .2): print(col, w, 'CAGR vol maxDD worstM', r)
        if lag == 0:
            v = Z[['N', 'U']].values
            for w in (.1, .2, .3):
                base = [];
                for _ in range(3000):
                    i = (rng.integers(0, len(v) - 8, len(v) // 8 + 1)[:, None] + np.arange(8)).ravel(); q = v[i]
                    base.append(((1 - w) * q[:, 0] + w * q[:, 1]).std() / q[:, 0].std() - 1)
                out[f'ci|{per}|{int(w * 100)}'] = (100 * np.quantile(base, [.025, .5, .975])).round(1).tolist(); print('vol change % CI', w, out[f'ci|{per}|{int(w * 100)}'])
            V = np.arange(0, 1.01, .05); vol = [((1 - w) * Z.N + w * Z.U).std() for w in V]; print('min-vol weight', V[int(np.argmin(vol))]); out['minw|' + per] = float(V[int(np.argmin(vol))])
R, ix = weekly(0); M = (1 + R).groupby(R.index.to_period('M')).prod() - 1; w = M.nsmallest(12, 'N'); print((100 * w).round(1)); out['worst'] = [[str(i), *(100 * x).round(1).tolist()] for i, x in zip(w.index, w.values)]
wk = R.nsmallest(26, 'N'); print('worst 26 NIFTY weeks mean N,U,H', (100 * wk.mean()).round(2).tolist(), 'U up share', (wk.U > 0).mean()); out['wk'] = [(100 * wk.mean()).round(2).tolist(), round(float((wk.U > 0).mean()), 2)]
yrs = R.index.year; out['yr'] = {int(y): [round(100 * x, 1) for x in ((1 + R[yrs == y]).prod() - 1)] for y in sorted(set(yrs))}; print(out['yr'])
for nm, a, b in (('Covid 2020', '2020-02-14', '2020-03-27'), ('2022 H1', '2022-01-01', '2022-06-24'), ('2018 Sep-Oct', '2018-08-31', '2018-10-26')):
    z = (1 + R[a:b].iloc[0 if a == '2022-01-01' else 1:]).prod() - 1; out['ev|' + nm] = (100 * z).round(1).tolist(); print(nm, out['ev|' + nm])
json.dump(out, open('s4.json', 'w'))
