import pandas as pd, numpy as np, json, glob
rng = np.random.default_rng(9)
rd = lambda p: (lambda d: d[~d.index.duplicated()])(pd.read_csv(p, index_col=0, parse_dates=True).close.dropna())
N = rd('sect/NIFTY.csv')['2014':'2024-12-31']
t = pd.concat([pd.read_csv(x) for x in glob.glob('macro/tsy*.csv')]); t['Date'] = pd.to_datetime(t.Date, format='%m/%d/%Y'); Y = t.set_index('Date').sort_index()['10 Yr'].dropna()
raw = {'y': Y, 'd': rd('macro/DXY.csv'), 'b': rd('macro/BRENT.csv'), 'i': rd('data/USDINR.csv'), 'v': rd('data/VIX.csv')}
def build(ix):
    X = pd.DataFrame({k: s.reindex(ix.union(s.index)).ffill().shift(1).reindex(ix) for k, s in raw.items()})
    iv = rd('macro/INVIX.csv'); X['iv'] = iv.reindex(ix).ffill(limit=2)
    F = pd.DataFrame({'US 10-year': X.y.diff(63) >= .25, 'Dollar': X.d.pct_change(63) >= .02, 'Brent': X.b.pct_change(63) >= .15, 'USDINR': X.i.pct_change(63) >= .02, 'US VIX': X.v >= 25, 'India VIX': X.iv >= 20}).astype(int)
    return X, F
X, F = build(N.index); D = pd.DataFrame({'macro4': F.iloc[:, :4].sum(axis=1), 'all6': F.sum(axis=1), 'iv': X.iv})
r = np.log(N).diff(); D['rv'] = r.rolling(21).std() * 252 ** .5 * 100
fm = pd.concat([N.shift(-k) for k in range(1, 22)], axis=1).min(axis=1, skipna=False) / N - 1
D['hit'] = (fm <= -.05).astype(float).where(fm.notna()); D['frv'] = r.rolling(21).std().shift(-21) * 252 ** .5 * 100; D['fr'] = N.shift(-21) / N - 1
D = D['2015-01-01':].dropna()
D['dev'] = D.index <= '2021-12-31'
d0 = D[D.index <= '2021-11-29']; d1 = D[~D.dev]  # purge dev rows whose 21-session window enters the check
Z = lambda q: np.c_[np.ones(len(q)), np.log(q.iv), q.macro4]
b = np.zeros(3)
for _ in range(50):
    p = 1 / (1 + np.exp(-Z(d0) @ b)); W = p * (1 - p); b = b + np.linalg.solve(Z(d0).T @ (Z(d0) * W[:, None]), Z(d0).T @ (d0.hit - p))
D['logit'] = Z(D) @ b; print('logit coef', b.round(2)); d0 = D.loc[d0.index]; d1 = D.loc[d1.index]
def auc(s, y):
    rk = s.rank().values; y = y.values; n1 = y.sum(); n0 = len(y) - n1; return (rk[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0) if n1 and n0 else np.nan
out = {'auc': [], 'col': [], 'flag': []}
for nm, d in (('dev', d0), ('check', d1)):
    print(nm, len(d), 'base rate', round(d.hit.mean(), 3)); a = {k: round(auc(d[k], d.hit), 3) for k in ('macro4', 'all6', 'logit', 'iv', 'rv')}; print(a)
    B = 63; df = {k: [] for k in ('macro4', 'all6', 'logit')}
    for _ in range(1500):
        i = (rng.integers(0, len(d) - B, len(d) // B + 1)[:, None] + np.arange(B)).ravel(); q = d.iloc[i]; base = auc(q.iv, q.hit)
        for k in df: df[k].append(auc(q[k], q.hit) - base)
    ci = {k: np.nanquantile(v, [.025, .975]).round(3).tolist() for k, v in df.items()}; print('diff vs India VIX CI', ci); out['auc'].append([nm, len(d), round(d.hit.mean(), 3), a, ci])
    c = pd.cut(d.all6, [-1, 1, 2, 6], labels=['Green', 'Amber', 'Red'])
    for k, q in d.groupby(c, observed=True): x = [nm, k, len(q), round(100 * q.hit.mean()), round(q.frv.mean(), 1), round(100 * q.fr.mean(), 2)]; out['col'].append(x); print(x)
    m = pd.cut(d.iv, [0, 15, 20, 100], labels=['IV<15', '15-20', '>20'])
    for k, q in d.groupby(m, observed=True): x = [nm, k, len(q), round(100 * q.hit.mean()), round(q.frv.mean(), 1), round(100 * q.fr.mean(), 2)]; out['col'].append(x); print(x)
    for k in F: f = F[k].reindex(d.index); x = [nm, k, int(f.sum()), round(100 * d.hit[f == 1].mean()) if f.sum() else None, round(100 * d.hit[f == 0].mean())]; out['flag'].append(x); print('flag', x)
# independent episodes: first day of red after non-red
for nm, d in (('dev', d0), ('check', d1)):
    e = (d.all6 >= 3) & (d.all6.shift(1) < 3); print(nm, 'red episodes', e.sum(), 'hits', d.hit[e].sum()); out['ep ' + nm] = [int(e.sum()), int(d.hit[e].sum())]
# spearman with forward vol
for nm, d in (('dev', d0), ('check', d1)): x = {k: round(d[k].rank().corr(d.frv.rank()), 2) for k in ('macro4', 'all6', 'iv', 'rv')}; print(nm, 'rank corr fwd vol', x); out['rk ' + nm] = x
# current reading only (inputs, no outcomes)
Xn, Fn = build(pd.date_range('2026-01-01', '2026-11-25', freq='B')[-80:].union(rd('data/NIFTY.csv').index[-400:]).unique()); ix = rd('data/NIFTY.csv').index; Xn, Fn = build(ix); out['now'] = [str(Fn.index[-1].date()), Fn.iloc[-1].to_dict(), Xn.iloc[-1].round(2).to_dict()]; print('NOW', out['now'])
json.dump(out, open('s5.json', 'w'), default=int)
