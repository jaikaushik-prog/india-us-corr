import pandas as pd, numpy as np, json, glob
rng = np.random.default_rng(31); END = pd.Timestamp('2026-11-24')
def rd(p):
    s = pd.read_csv(p, index_col=0, parse_dates=True).iloc[:, 0]; s = pd.to_numeric(s, errors='coerce').dropna()[:END]; return s[~s.index.duplicated()].sort_index()
N, S = rd('data/NIFTY.csv'), rd('data/SPX.csv')
t = pd.concat([pd.read_csv(x) for x in glob.glob('macro/tsy*.csv')]); t['Date'] = pd.to_datetime(t.Date, format='%m/%d/%Y'); t = t.set_index('Date').sort_index()[:END]
us = S.reindex(N.index.union(S.index)).ffill().shift(1).reindex(N.index); d = np.log(pd.DataFrame({'n': N, 'u': us}).dropna()).diff().dropna()
G = pd.date_range('2014-06-06', '2026-11-20', freq='W-FRI')
def at(s): return s.reindex(G.union(s.index)).ffill().shift(1).reindex(G)   # last value strictly before Friday
L = {k: rd(f'lead/{k}.csv') for k in ('SOXX', 'SPY', 'HYG', 'IEF', 'EMB', 'MOVE', 'HG', 'GC', 'INDA', 'EEM', 'CNY', 'T10YIE')}
VIX, DXY, BR, INR, IV = rd('data/VIX.csv'), rd('macro/DXY.csv'), rd('macro/BRENT.csv'), rd('data/USDINR.csv'), rd('macro/INVIX.csv')
ch = lambda s, k=13: at(s).diff(k); pc = lambda s, k=13: np.log(at(s)).diff(k); rt = lambda a, b: np.log(L[a] / L[b]).dropna()
def mon(s, lag=1):   # monthly series, usable only after `lag` full months
    s = s.copy(); s.index = s.index.to_period('M'); return pd.Series([s.get(g.to_period('M') - lag, np.nan) for g in G], index=G)
in10, in3 = rd('macro/INDIRLTLT01STM.csv'), rd('macro/INDIR3TIB01STM.csv'); u10m = t['10 Yr'].groupby(t.index.to_period('M')).mean(); u10m.index = u10m.index.to_timestamp()
spm = (in10 - u10m).dropna(); fl = pd.read_csv('flows/gh/fb_month.csv'); fl.index = pd.PeriodIndex(fl.month, freq='M').to_timestamp(); lv = N.groupby(N.index.to_period('M')).last().shift(1); lv.index = lv.index.to_timestamp(); fs = (fl.net_equity_cr / lv.reindex(fl.index))
X = pd.DataFrame({
    'US 10y, 13w change': ch(t['10 Yr']), 'US 2s10s level': at(t['10 Yr'] - t['2 Yr']), 'US 2s10s, 13w change': ch(t['10 Yr'] - t['2 Yr']), 'US 3m10y, 13w change': ch(t['10 Yr'] - t['3 Mo']),
    'US real 10y, 13w change': ch(rd('macro/DFII10.csv')), 'US breakeven, 13w change': ch(L['T10YIE']), 'India-US 10y level': mon(spm), 'India-US 10y, 3m change': mon(spm) - mon(spm, 4), 'India 10y-3m level': mon((in10 - in3).dropna()),
    'High yield vs Treasuries, 13w': ch(rt('HYG', 'IEF')), 'EM bonds vs Treasuries, 13w': ch(rt('EMB', 'IEF')), 'MOVE bond volatility': at(L['MOVE']),
    'Chips vs S&P, 13w': ch(rt('SOXX', 'SPY')), 'Chips vs S&P, 4w': ch(rt('SOXX', 'SPY'), 4), 'Dollar index, 13w': pc(DXY), 'USDINR, 13w': pc(INR), 'Brent, 13w': pc(BR), 'Copper vs gold, 13w': ch(np.log(L['HG'] / L['GC']).dropna()),
    'VIX': at(VIX), 'India VIX minus VIX': at(IV) - at(VIX), 'EM vs S&P, 13w': ch(rt('EEM', 'SPY')), 'NIFTY vs S&P, 13w': pc(N) - pc(S), 'INDA vs NIFTY in USD, 4w': (np.log(at(L['INDA'])).diff(4) - (np.log(at(N)).diff(4) - np.log(at(INR)).diff(4))), 'Foreign flow, last month': mon(fs)})
Nf, Sf = at(N), at(S)
def target(k): return (np.log(Nf.shift(-k) / Nf) - np.log(Sf.shift(-k) / Sf))
def link(k):
    o = []
    for g in G:
        z = d[(d.index >= g) & (d.index < g + pd.Timedelta(weeks=k))]; o.append(np.arctanh(np.clip(z.n.corr(z.u), -.97, .97)) if len(z) >= 50 and g + pd.Timedelta(weeks=k) <= END else np.nan)
    return pd.Series(o, index=G)
Y = {'rel4': (target(4), 4), 'rel13': (target(13), 13), 'link13': (link(13), 13)}
G15 = np.flatnonzero(G >= '2015-01-01')[0]
def perm(a, b, B=4000):
    c = np.corrcoef(a, b)[0, 1]; p = np.array([np.corrcoef(a, rng.permutation(b))[0, 1] for _ in range(B)]); return c, float((np.abs(p) >= abs(c)).mean()), p
rows = []
for y, (ys, k) in Y.items():
    ids = np.arange(G15, len(G), k)
    for x in X:
        z = pd.DataFrame({'x': X[x], 'y': ys}).iloc[ids].dropna(); endw = z.index + pd.Timedelta(weeks=k)
        a, b = z[endw <= '2022-12-31'], z[(z.index >= '2023-01-01') & (endw <= '2026-09-30')]
        if len(a) < 12:
            c2, p2, _ = perm(b.x.values, b.y.values); rows.append([y, x, len(a), np.nan, np.nan, len(b), c2, np.nan, p2]); continue
        c1, p1, _ = perm(a.x.values, a.y.values); c2, p2t, pv = perm(b.x.values, b.y.values); p2 = float((np.sign(c1) * pv >= np.sign(c1) * c2).mean()); rows.append([y, x, len(a), c1, p1, len(b), c2, p2, p2t])
R = pd.DataFrame(rows, columns=['y', 'x', 'n1', 'c1', 'p1', 'n2', 'c2', 'p2one', 'p2two']); m = R.p1.notna(); o = R[m].sort_values('p1'); q = (o.p1 * m.sum() / np.arange(1, m.sum() + 1))[::-1].cummin()[::-1]; R.loc[o.index, 'q'] = q
R['pass'] = (R.q <= .10) & (R.p2one < .10) & (np.sign(R.c1) == np.sign(R.c2))
print(R.sort_values('p1').round(3).to_string()); print('tests', m.sum(), 'p1<.05', (R.p1 < .05).sum(), 'pass', R['pass'].sum(), 'same sign share', round((np.sign(R.c1) == np.sign(R.c2))[m].mean(), 2), 'nominal p1<.05 and p2<.10:', R[(R.p1 < .05) & (R.p2one < .1)][['y', 'x']].values.tolist())
R.round(3).to_csv('lead_tests.csv', index=False)
# readings (z-score on trailing 5y) at 4 weeks before and at start of the three episodes
Zs = (X - X.rolling(260, min_periods=100).mean()) / X.rolling(260, min_periods=100).std(); ep = {'24Q1': '2023-12-29', '25Q3': '2025-06-27', '26Q4': '2026-09-25'}
E = pd.DataFrame({k: Zs.loc[v] for k, v in ep.items()}); E['now'] = Zs.iloc[-1]; E['raw now'] = X.iloc[-1]; print('\nz-scores just before each episode\n', E.round(2).to_string())
# lead/lag profile monthly: predictor change month t-k vs NIFTY-S&P month t
MN = lambda s: s.groupby(s.index.to_period('M')).last(); rel = np.log(MN(N)).diff() - np.log(MN(S)).diff()
P = pd.DataFrame({'US 10y': MN(t['10 Yr']).diff(), '2s10s': MN(t['10 Yr'] - t['2 Yr']).diff(), 'HY vs Tsy': MN(rt('HYG', 'IEF')).diff(), 'EM bonds vs Tsy': MN(rt('EMB', 'IEF')).diff(), 'Dollar': np.log(MN(DXY)).diff(), 'USDINR': np.log(MN(INR)).diff(), 'Brent': np.log(MN(BR)).diff(), 'Chips vs S&P': MN(rt('SOXX', 'SPY')).diff(), 'VIX': MN(VIX).diff()})
sp = spm.copy(); sp.index = sp.index.to_period('M'); P['India-US 10y'] = sp.diff(); F2 = fs.copy(); F2.index = F2.index.to_period('M'); P['Foreign flow'] = F2
pf = {}
for c in P:
    pf[c] = [round(pd.concat([P[c].shift(k), rel], axis=1).loc['2015-01':'2026-10'].dropna().corr().iloc[0, 1], 2) for k in (3, 2, 1, 0, -1, -2, -3)]
print('\nprofile: predictor leads 3,2,1 | 0 | lags 1,2,3 months\n', pd.DataFrame(pf, index=['lead3', 'lead2', 'lead1', 'same', 'lag1', 'lag2', 'lag3']).T.to_string())
# AI rotation
W = pd.DataFrame({'n': np.log(N.reindex(G, method='ffill')).diff(), 's': np.log(at(S)).diff(), 'c': at(rt('SOXX', 'SPY')).diff()}).dropna()['2015':]
def hac(y, A, lag=4):
    A = np.c_[np.ones(len(A)), A]; b = np.linalg.lstsq(A, y, rcond=None)[0]; e = y - A @ b; U = A * e[:, None]; V = U.T @ U
    for j in range(1, lag + 1): w = 1 - j / (lag + 1); g = U[j:].T @ U[:-j]; V += w * (g + g.T)
    I = np.linalg.inv(A.T @ A); return b, b / np.sqrt(np.diag(I @ V @ I))
out = {'ai': []}
for nm, a, b in (('2015-22', '2015', '2022'), ('2023-Sep26', '2023-01-01', '2026-09-30'), ('2025-Sep26', '2025-01-01', '2026-09-30'), ('Oct-Nov26', '2026-10-01', '2026-11-30')):
    z = W[a:b]; bb, tt = hac(z.n.values, z[['s', 'c']].values, 4 if len(z) > 20 else 1); out['ai'].append([nm, len(z), *bb.round(2).tolist(), *tt.round(2).tolist()]); print('AI same week', out['ai'][-1])
Wl = W.copy(); Wl['cl'] = Wl.c.shift(1); Wl['rel'] = Wl.n - Wl.s; Wl = Wl.dropna()
for nm, a, b in (('2015-22', '2015', '2022'), ('2023-Sep26', '2023-01-01', '2026-09-30'), ('Oct-Nov26', '2026-10-01', '2026-11-30')):
    z = Wl[a:b]; bb, tt = hac(z.rel.values, z[['cl']].values, 4 if len(z) > 20 else 1); print('AI lead 1w', nm, len(z), bb.round(3), tt.round(2)); out['ai'].append(['lead ' + nm, len(z), *bb.round(3).tolist(), *tt.round(2).tolist()])
dn = W[W.c <= W.c[:'2022'].quantile(.1)]; print('weeks of big chip underperformance: NIFTY-S&P mean', [(nm, len(dn[a:b]), round(100 * (dn[a:b].n - dn[a:b].s).mean(), 2)) for nm, a, b in (('15-22', '2015', '2022'), ('23-Sep26', '2023-01-01', '2026-09-30'), ('Q4', '2026-10-01', '2026-11-30'))])
print(W['2026-10-01':].mul(100).round(1).to_string())
# detector delay
def sim(rho, n): z = rng.standard_normal((n, 2)); z[:, 1] = rho * z[:, 0] + np.sqrt(1 - rho ** 2) * z[:, 1]; return z
def ew(z, hl):
    a = 1 - .5 ** (1 / hl); xy = pd.Series(z[:, 0] * z[:, 1]).ewm(alpha=a).mean(); return (xy / np.sqrt(pd.Series(z[:, 0] ** 2).ewm(alpha=a).mean() * pd.Series(z[:, 1] ** 2).ewm(alpha=a).mean())).values
meas = {'13 weeks': lambda z: pd.Series(z[:, 0]).rolling(63).corr(pd.Series(z[:, 1])).values, '5 weeks': lambda z: pd.Series(z[:, 0]).rolling(25).corr(pd.Series(z[:, 1])).values, 'EWMA 10d': lambda z: ew(z, 10)}
det = {}
for k, fn in meas.items():
    dl, fa = [], []
    for _ in range(400):
        z = np.vstack([sim(.3, 250), sim(-.2, 250)]); v = fn(z)[250:]; h = np.flatnonzero(v < 0); dl.append(h[0] if len(h) else 250)
        v0 = fn(sim(.3, 1250))[100:] < 0; fa.append((np.diff(v0.astype(int)) == 1).sum() / (1150 / 250))
    det[k] = [int(np.median(dl)), int(np.quantile(dl, .9)), round(float(np.mean(fa)), 1)]
print('detector: median delay days, 90%, false dips per year', det); out['det'] = det; out['profile'] = pf; json.dump(out, open('lead.json', 'w'))
