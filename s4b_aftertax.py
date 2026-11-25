import pandas as pd, numpy as np, json
n = pd.read_csv('../nexus-volatility-research/outputs/nifty50_tri_20261103/nifty50_tri_daily_2012_2026.csv', parse_dates=['Date']).set_index('Date')['Total Returns Index'].astype(float)[:'2024-12-31']
s = pd.read_csv('sect/SPXTR.csv', index_col=0, parse_dates=True).close[:'2024-12-31']; fx = pd.read_csv('data/USDINR.csv', index_col=0, parse_dates=True).close.dropna()[:'2024-12-31']
ix = pd.date_range('2014-12-26', '2024-12-27', freq='W-FRI'); a = lambda x: x.reindex(ix, method='ffill')
R0 = pd.DataFrame({'N': a(n), 'U': a(s) * a(fx)}).pct_change().dropna()
cg = lambda x: (1 + x).prod() ** (52 / len(x)) - 1
TAX = .13
def sim(R, w, mode, feeU, feeN=.002, cost=.00125, entry=0.0, band=.05):
    """Average-cost gains taxed at 13% when units are sold; entry = one-off cost on US buys (FX etc). Tax at end on both sleeves."""
    v = np.array([1 - w, w * (1 - entry)]); basis = np.array([1 - w, w]); V = [v.sum()]; trades = 0; taxes = 0.
    fee = np.array([feeN, feeU]) / 52
    for i, (rn, ru) in enumerate(R[['N', 'U']].values):
        v = v * (1 + np.array([rn, ru])) * (1 - fee); tot = v.sum()
        do = 0 < w < 1 and i + 1 < len(R) and ((mode == 'year' and (i + 1) % 52 == 0) or (mode == 'band' and abs(v[1] / tot - w) > band))
        if do:
            tgt = tot * np.array([1 - w, w]); j = 0 if v[0] > tgt[0] else 1; sell = v[j] - tgt[j]; gain = sell * (1 - basis[j] / v[j]); tax = max(gain, 0) * TAX
            basis[j] *= 1 - sell / v[j]; v[j] -= sell; buy = sell * (1 - 2 * cost) - tax; k = 1 - j; got = buy * (1 - (entry if k == 1 else 0)); v[k] += got; basis[k] += buy; trades += 1; taxes += tax
        V.append(v.sum())
    endt = (np.maximum(v - basis, 0) * TAX).sum(); V = np.array(V); r = V[1:] / V[:-1] - 1
    return [round(100 * ((V[-1] - endt) ** (52 / len(r)) - 1), 2), round(100 * r.std() * 52 ** .5, 1), round(100 * (V / np.maximum.accumulate(V) - 1).min(), 1), trades, round(100 * taxes, 2)]
m = cg(R0.N); print('gross CAGR N,U', m, cg(R0.U))
def shift(tgt):  # shift US weekly returns by a constant so its CAGR equals tgt
    lo, hi = -.02, .02
    for _ in range(60):
        c = (lo + hi) / 2; lo, hi = (c, hi) if cg(R0.U + c) < tgt else (lo, c)
    return R0.assign(U=R0.U + c)
SC = {'actual': R0, 'equal': shift(m), 'minus3': shift(m - .03)}; RT = {'Indian fund, 0.6% a year': (.006, 0.), 'Indian fund, 1.0% a year': (.010, 0.), 'Direct US ETF, 0.4% a year + 1% entry': (.004, .01)}
out = {'gross': [round(100 * m, 1), round(100 * cg(R0.U), 1)], 'rows': []}
for sc, R in SC.items():
    for rt, (fee, en) in RT.items():
        for mode in ('none', 'year', 'band'):
            for w in (0, .1, .2, .3, .4):
                r = sim(R, w, mode, fee, entry=en); out['rows'].append([sc, rt, mode, int(w * 100), *r])
D = pd.DataFrame(out['rows'], columns=['sc', 'rt', 'mode', 'w', 'cagr', 'vol', 'dd', 'trades', 'tax']); print(D[(D.mode if False else D['mode']) == 'band'].to_string()); print(D[(D.rt.str.contains('0.6')) & (D.w == 20)].to_string())
for pa, pb in (('2015', '2019'), ('2020', '2024')):
    print(pa, [sim(R0[pa:pb], w, 'band', .006) for w in (0, .2, .4)]); out['half' + pa] = [sim(R0[pa:pb], w, 'band', .006) for w in (0, .2, .4)]
# fixed-cost at small size: direct route
out['fixed'] = [[k, w, round(k * w), [round(100 * x / (k * w), 2) for x in (1000, 2000)]] for k in (500000, 1000000, 2000000) for w in (.2,)]; print(out['fixed'])
json.dump(out, open('s4b.json', 'w'))
