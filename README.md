# NIFTY and the US

A study of how closely India's NIFTY 50 follows US markets, what drives the link, and what can be done with it. Data runs to 24 November 2026.

Start with [NIFTY_and_the_US_report.pdf](NIFTY_and_the_US_report.pdf); the summary is on pages 2 and 3.

## Main findings

- NIFTY's daily correlation with the previous S&P 500 session was 0.40 in 2023 and 0.25 in 2026. It is about zero since July 2026 and has not been negative in any year since 2015.
- On price levels, 2026 is the first negative year since at least 2015 (-0.36).
- 0 of 50 bond-yield tests were significant. The long-run average beat HAR and a regime model at forecasting the correlation.
- Foreign flows account for about half of NIFTY's 2026 gap and do not predict the next month.
- Trading NIFTY after big US moves failed. The opening gap takes 0.23 of a 0.28 move per 1% in the S&P.
- A macro monitor did not beat India VIX at warning of falls.
- Holding 20% in US stocks cut volatility from 15.8% to 14.4% over 2015 to 2024, after assumed tax and fees.

## Run it

```
pip install -r requirements.txt
python fetch_data.py
```

Raw market data is not stored here. Yahoo and others revise history, so refetched numbers can differ slightly. Use Python 3.11 or later and run scripts from the repo root.

| Study | Script | Output |
|---|---|---|
| Rolling correlations (first version) | `analyse.py`, `nulls.py` | `results.txt`, `nulls.txt`, `roll.json` |
| Month, half-year and year | `periods.py` | `results_periods.txt`, `period_correlations.csv` |
| Peers, VIX, lead-lag, response sizes | `deep.py` (needs `periods.json`) | `results_deep.txt`, `deep.json` |
| Yields, regimes, forecasts | `macro_study.py` | `results_macro.txt`, `macro.json` |
| 1. Opening gap | `s1_gap.py` | `res_s1_gap.txt` |
| 2. Foreign flows | `s2_flows.py` | `res_s2_flows.txt` |
| 3. Sectors and sector map | `s3_sectors.py`, `s3b_map.py` | `res_s3_sectors.txt`, `res_s3b_map.txt` |
| 4. US allocation, before and after tax | `s4_portfolio.py`, `s4b_aftertax.py` | `res_s4_*.txt`, `res_s4b_*.txt` |
| 5. Macro monitor | `s5_monitor.py` | `res_s5_monitor.txt` |

Rules fixed before running are in `protocol_next.json` (studies 1, 3, 4, 5) and `protocol_phase3.json` (flows, sector map, after-tax test). The regime rules are at the top of `macro_study.py`.

Pages: `build_simple.py`, `build_macro_simple.py`, `build_actions.py` and `build_playbook.py` make the four HTML pages. `build_report.py` makes the PDF and needs Microsoft Edge on Windows.

### Files you must supply

These scripts read local files one folder above the repo:

- `analyse.py`: optional NIFTY 1-minute CSVs for a data check. It skips the check if they are missing.
- `s1_gap.py`: NIFTY futures 5-minute vendor file and `momentum_bot/costs.py`.
- `s4_portfolio.py`, `s4b_aftertax.py`: NIFTY 50 total return index CSV, available from niftyindices.com.

## Before you build on this

- A separate volatility project reserves January 2025 to October 2026 as a holdout. Some studies here show NIFTY outcomes in that window, so do not treat it as unseen for US and NIFTY ideas.
- The same data was cut many ways and p-values are not adjusted. Log every new test you run and fix its pass rule first.
- Monthly flows come from a third-party copy of NSDL figures ([FinBizNet](https://github.com/FinBizNet-AI-Tech-Pvt-Ltd/india-market-data), CC BY 4.0). Years before 2026 were not checked against NSDL.
- Tax rules come from secondary sources that disagree, and fund fees are assumptions.

## Open work

- Domestic flows over a longer history
- Earnings growth and valuation gaps
- Daily Indian yields around RBI and Fed meetings
- Why Taiwan and Korea stayed linked while India did not (AI exposure, flows, oil)
- Whether morning moves in Japan, Korea and Australia add anything to NIFTY after its open

Research for discussion. Not investment or tax advice.
