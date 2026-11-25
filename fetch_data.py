"""Rebuild the raw inputs. Needs internet and curl. Usage: python fetch_data.py"""
import json, os, subprocess, sys, time, urllib.parse, urllib.request
import pandas as pd
for d in ('data', 'macro', 'sect', 'flows/gh'):
    os.makedirs(d, exist_ok=True)
for s in ('download.py', 'download2.py', 'dl_sect.py'):
    subprocess.run([sys.executable, s], check=True)
for n, s in {'BRENT': 'BZ=F', 'DXY': 'DX-Y.NYB', 'INVIX': '^INDIAVIX'}.items():
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(s)}?period1=1400000000&period2={int(time.time())}&interval=1d'
    r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60))['chart']['result'][0]
    ix = pd.to_datetime(r['timestamp'], unit='s', utc=True).tz_convert(r['meta']['exchangeTimezoneName']).date
    d = pd.DataFrame({'close': r['indicators']['quote'][0]['close']}, index=ix).dropna(); d.index.name = 'date'; d.to_csv(f'macro/{n}.csv')
def curl(url, out):
    subprocess.run(['curl', '-sS', '-f', '-L', '-m', '90', '--http1.1', '--retry', '3', '-o', out, url], check=True)
for s in ('INDIRLTLT01STM', 'INDIR3TIB01STM', 'BAMLH0A0HYM2', 'DFII10'):
    curl(f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}', f'macro/{s}.csv')
for y in range(2015, 2027):
    curl(f'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{y}/all?type=daily_treasury_yield_curve&field_tdr_date_value={y}&_format=csv', f'macro/tsy{y}.csv')
B = 'https://raw.githubusercontent.com/'
for p, o in (('FinBizNet-AI-Tech-Pvt-Ltd/india-market-data/main/data/fii-flows-by-month.csv', 'fb_month.csv'), ('rrb396-sketch/finance---flows/main/data/fpi_monthly.csv', 'rr.csv'), ('nalinisubir-oss/fii-dii-data/main/data/history.json', 'na.json')):
    curl(B + p, 'flows/gh/' + o)
print('done')
