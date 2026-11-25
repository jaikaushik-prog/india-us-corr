"""Regimes, yield spreads, conditional forecasts. Rules fixed BEFORE outcomes were viewed (2026-11-25):
 monthly regime, from month-end values, 3-month changes:
   STRESS   : mean VIX of month >= 25
   SQUEEZE  : >=2 of {US10y +25bp, DXY +2%, Brent +15%, USDINR +2%}
   TAILWIND : >=2 of {US10y -25bp, DXY -2%, Brent -15%, USDINR -2%}
   NEUTRAL  : everything else (also if both fire). Priority STRESS > SQUEEZE/TAILWIND.
 forecast target: Fisher-z of next-month NIFTY/SPX daily correlation; OOS start 2019-01, expanding window.
"""
import pandas as pd, numpy as np, json, glob
rng = np.random.default_rng(11)
END = pd.Timestamp('2026-11-24')
def rd(p):
    d = pd.read_csv(p, index_col=0, parse_dates=True).iloc[:, 0]
    d = pd.to_numeric(d, errors='coerce').dropna()[:END]
    return d[~d.index.duplicated()].sort_index()
N, S = rd('data/NIFTY.csv'), rd('data/SPX.csv')
t = pd.concat([pd.read_csv(f) for f in glob.glob('macro/tsy*.csv')])
t['Date'] = pd.to_datetime(t['Date'], format='%m/%d/%Y'); t = t.set_index('Date').sort_index()[:END]
DXY, BR, VIX, INR = rd('macro/DXY.csv'), rd('macro/BRENT.csv'), rd('data/VIX.csv'), rd('data/USDINR.csv')
REAL, HY = rd('macro/DFII10.csv'), rd('macro/BAMLH0A0HYM2.csv')
IN10, IN3 = rd('macro/INDIRLTLT01STM.csv'), rd('macro/INDIR3TIB01STM.csv')
for s in (IN10, IN3): s.index = s.index.to_period('M')
us = S.reindex(N.index.union(S.index)).ffill().shift(1).reindex(N.index)
r = np.log(pd.DataFrame({'n': N, 'u': us}).dropna()).diff().dropna(); r['m'] = r.index.to_period('M')
last = lambda s: s.groupby(s.index.to_period('M')).last()
mean = lambda s: s.groupby(s.index.to_period('M')).mean()
M = pd.DataFrame({'corr': r.groupby('m')[['n', 'u']].apply(lambda g: g.n.corr(g.u)), 'nr': r.groupby('m').n.sum(),
                  'sr': np.log(last(S)).diff()})
M['nr'] = np.log(last(N)).diff(); M['rel'] = M.nr - M.sr
M['us10'], M['s2s10'], M['s3m10'] = last(t['10 Yr']), last(t['10 Yr'] - t['2 Yr']), last(t['10 Yr'] - t['3 Mo'])
M['us10avg'] = mean(t['10 Yr']); M['in10'] = IN10; M['inus'] = M.in10 - M.us10avg; M['interm'] = IN10 - IN3
M['real'], M['vix'], M['dxy'], M['br'], M['inr'] = last(REAL), mean(VIX), last(DXY), last(BR), last(INR)
M = M['2014-06':]
u3 = pd.DataFrame({'us': (M.us10.diff(3)) / .25, 'dx': M.dxy.pct_change(3) / .02, 'br': M.br.pct_change(3) / .15, 'fx': M.inr.pct_change(3) / .02})
sq, tw = (u3 >= 1).sum(axis=1) >= 2, (u3 <= -1).sum(axis=1) >= 2
M['reg'] = np.select([M.vix >= 25, sq & ~tw, tw & ~sq], ['Stress', 'Squeeze', 'Tailwind'], 'Neutral')
M = M['2015-02':]; M['reg'] = M.reg.where(M.us10.notna())
z = lambda c: np.arctanh(c.clip(-.97, .97)); M['z'] = z(M['corr'])
M['regp'] = M.reg.shift(1)
print(M.tail(14).round(2).to_string())
out = {}
for lab, col in (('concurrent', 'reg'), ('known beforehand', 'regp')):
    print('\nREGIME', lab); out[lab] = []
    d = r.copy(); d['g'] = d.m.map(M[col])
    for g in ('Stress', 'Squeeze', 'Neutral', 'Tailwind'):
        x = d[d.g == g]; mm = M[M[col] == g]; ms = x.m.unique(); a = {k: v for k, v in x.groupby('m')[['n', 'u']]}
        bs = []
        for _ in range(1500):
            p = np.concatenate([a[k].values for k in rng.choice(len(ms), len(ms)).tolist() for k in [ms[k]]]); bs.append(np.corrcoef(p.T)[0, 1])
        med = [round(100 * mm[c].mean(), 2) for c in ('nr', 'sr', 'rel')]
        se = round(100 * mm.rel.std() / np.sqrt(len(mm)), 2)
        row = [g, len(mm), round(x.n.corr(x.u), 2), *np.quantile(bs, [.025, .975]).round(2).tolist(), *med, se, round(100 * (mm.rel > 0).mean())]
        out[lab].append(row); print(row)
rs = M.reg.dropna(); rs = rs[rs.index <= '2026-10']
tm = pd.crosstab(rs[:-1].values, rs[1:].values, normalize='index').round(2); print(tm); out['trans'] = tm.to_dict('index')
print('counts by yr\n', pd.crosstab(M.index.year, M.reg))
# spreads vs outcomes: non-overlapping quarters, permutation/bootstrap CIs
Q = M[:'2026-10'].copy(); Q['q'] = Q.index.to_timestamp().to_period('Q')
fd = lambda c: Q.groupby('q')[c].last().diff()
qq = pd.DataFrame({'rel': Q.groupby('q').rel.sum(), 'nr': Q.groupby('q').nr.sum(), 'd_inus': fd('inus'), 'd_2s10': fd('s2s10'), 'd_3m10': fd('s3m10'), 'd_us10': fd('us10'), 'd_real': fd('real'), 'd_interm': fd('interm'),
                   'l_inus': Q.groupby('q').inus.last(), 'l_2s10': Q.groupby('q').s2s10.last(), 'l_us10': Q.groupby('q').us10.last(), 'l_real': Q.groupby('q').real.last()})
rq = r.copy(); rq['q'] = rq.index.to_period('Q'); qq['corr'] = rq.groupby('q')[['n', 'u']].apply(lambda g: g.n.corr(g.u)); qq = qq.iloc[1:]
qq['rel_next'], qq['corr_next'] = qq.rel.shift(-1), qq['corr'].shift(-1)
out['q'] = []
for y in ('corr', 'rel', 'nr', 'corr_next', 'rel_next'):
    for x in ('d_inus', 'd_2s10', 'd_3m10', 'd_us10', 'd_real', 'd_interm', 'l_inus', 'l_2s10', 'l_us10', 'l_real'):
        d = qq[[x, y]].dropna().values; c = np.corrcoef(d.T)[0, 1]
        pm = np.array([np.corrcoef(d[:, 0], rng.permutation(d[:, 1]))[0, 1] for _ in range(2000)]); p = (abs(pm) >= abs(c)).mean()
        bs = np.array([np.corrcoef(d[rng.integers(0, len(d), len(d))].T)[0, 1] for _ in range(1000)])
        out['q'].append([y, x, round(c, 2), round(p, 3), *np.quantile(bs, [.025, .975]).round(2).tolist(), len(d)])
Qd = pd.DataFrame(out['q'], columns=['y', 'x', 'c', 'p', 'lo', 'hi', 'n']); print(Qd.to_string()); print('p<.05:', (Qd.p < .05).sum(), 'of', len(Qd))
# daily: yield change -> NIFTY
def dl(s):
    s = s.reindex(N.index.union(s.index)).ffill().shift(1).reindex(N.index); return s.diff()
dd = pd.DataFrame({'n': np.log(N).diff(), 'd10': dl(t['10 Yr']), 'd2s10': dl(t['10 Yr'] - t['2 Yr'])}).dropna()
sp = pd.DataFrame({'s': np.log(S).diff(), 'd': t['10 Yr'].diff()}).dropna()
out['ydaily'] = [[y, round(dd.loc[str(y)].n.corr(dd.loc[str(y)].d10), 2), round(dd.loc[str(y)].n.corr(dd.loc[str(y)].d2s10), 2), round(sp.loc[str(y)].s.corr(sp.loc[str(y)].d), 2)] for y in range(2015, 2027)]
print('DAILY yr nifty~d10, nifty~d2s10, SPX~d10', out['ydaily'])
# forecast comparison
F = M[:'2026-10'][['z', 'reg', 'corr']].copy(); F['h1'] = F.z.shift(1); F['h3'] = F.z.rolling(3).mean().shift(1); F['h6'] = F.z.rolling(6).mean().shift(1); F['h12'] = F.z.rolling(12).mean().shift(1)
F['stress'] = (F.reg.shift(1) == 'Stress') * 1.; F['squeeze'] = (F.reg.shift(1) == 'Squeeze') * 1.
F = F.dropna(); pr = []
def ols(Xa, ya, xn):
    b = np.linalg.lstsq(np.c_[np.ones(len(Xa)), Xa], ya, rcond=None)[0]; return b[0] + xn @ b[1:]
HAR, HR = ['h1', 'h3', 'h12'], ['h1', 'h3', 'h12', 'stress', 'squeeze']
for m in F.index[F.index >= '2019-01']:
    a = F[F.index < m]; x = F.loc[m]
    pr.append([m, x.z, a.z.mean(), x.h1, x.h12, ols(a[HAR].values, a.z.values, x[HAR].values.astype(float)), ols(a[HR].values, a.z.values, x[HR].values.astype(float))])
P = pd.DataFrame(pr, columns=['m', 'z', 'mean', 'last', 'avg12', 'HAR', 'HAR+reg']).set_index('m')
out['fc'] = []
for c in P.columns[1:]:
    e, e0 = (P[c] - P.z) ** 2, (P['mean'] - P.z) ** 2; d = (e - e0).values
    bs = np.array([d[(rng.integers(0, len(d) - 5, len(d) // 6 + 1)[:, None] + np.arange(6)).ravel()].mean() for _ in range(3000)])
    out['fc'].append([c, round(np.sqrt(e.mean()), 3), round(100 * (1 - e.mean() / e0.mean()), 1), *np.quantile(bs, [.025, .975]).round(3).tolist()]); print('FC', out['fc'][-1], 'RMSE corr', round(np.sqrt(((np.tanh(P[c]) - np.tanh(P.z)) ** 2).mean()), 3), 'n', len(P))
# forecast distribution: baseline expanding mean + empirical OOS error, and regime conditional monthly quantiles
er = (P.z - P['mean']).values
lm = F.z.mean(); out['fcast1'] = [round(np.tanh(lm), 2), *np.tanh(lm + np.quantile(er, [.1, .9])).round(2).tolist(), round((np.tanh(lm + er) < 0).mean(), 2)]; print('next month', out['fcast1'])
def roll(k):
    c = [r.loc[(r.m > p - k) & (r.m <= p), ['n', 'u']].corr().iloc[0, 1] for p in M.index[k - 1:]]; return np.array(c)
for k in (3, 6, 12):
    c = roll(k)[::1]; out[f'h{k}'] = [round(float(np.median(c)), 2), *np.quantile(c, [.1, .9]).round(2).tolist(), round(float((c < 0).mean()), 2)]; print(k, 'mo hist', out[f'h{k}'])
out['cond'] = {g: [int((M.regp == g).sum()), *M.loc[M.regp == g, 'corr'].quantile([.1, .5, .9]).round(2).tolist(), round((M.loc[M.regp == g, 'corr'] < 0).mean(), 2)] for g in ('Stress', 'Squeeze', 'Neutral', 'Tailwind')}; print(out['cond'])
r6 = pd.Series(roll(6), index=M.index[5:])
rel = np.log(N / N.iloc[0]).reindex(S.index.union(N.index)).ffill() - np.log(S / S.iloc[0]).reindex(S.index.union(N.index)).ffill(); rl = last(rel)[M.index]
f = lambda s: [None if pd.isna(v) else round(float(v), 3) for v in s]
out['ts'] = {'m': [str(i) for i in M.index], 'reg': M.reg.tolist(), 'c6': f(r6.reindex(M.index)), 'rel': f(100 * np.exp(rl - rl.iloc[0])), **{k: f(M[k]) for k in ('inus', 's2s10', 's3m10', 'us10', 'in10', 'vix', 'inr', 'br', 'dxy', 'real', 'interm')}}
out['qs'] = [[str(i), None if pd.isna(a) else round(a, 2), round(100 * b, 2), round(c, 2)] for i, a, b, c in zip(qq.index, qq.d_inus, qq.rel, qq['corr'])]
out['u3'] = u3.tail(3).round(2).values.tolist(); print(u3.tail(6).round(2)); print(M.groupby(M.index.year)[['inus', 's2s10', 'us10', 'in10', 'vix', 'inr', 'br', 'dxy']].mean().round(2))
json.dump(out, open('macro.json', 'w'), separators=(',', ':'))
