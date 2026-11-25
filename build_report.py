import re, json, os, subprocess, time, math, io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
HERE = os.path.abspath('.').replace('\\', '/')
os.makedirs('rep', exist_ok=True)
PRINT = '''<style>
@page{size:A4;margin:16mm 16mm 18mm}
*{-webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{background:#fff!important}:root{--bg:#ffffff;padding:0!important}
body{font-size:13px;line-height:1.5;margin:0;--bg:#ffffff;--r3:#8c99a5}
main{max-width:none!important;width:672px;margin:0!important;padding:0!important}
h1{font-size:25px;margin:0 0 10px}h2{font-size:18px;margin:26px 0 7px}h3{font-size:14px;margin:15px 0 4px}
h1,h2,h3{break-after:avoid}p,ul{max-width:none;margin:0 0 9px}p,li{orphans:4;widows:4}.lead{font-size:15px}.mut{font-size:11.5px}li{margin-bottom:4px}
table{font-size:11px}th,td{padding:4px 5px;white-space:normal!important}td.w{min-width:0!important}tr,svg,.waf>div,.row{break-inside:avoid}thead{display:table-header-group}
.tw{overflow:visible;margin-bottom:10px}.lg{break-after:avoid;font-size:11.5px}.ctl,.box,.tip{display:none!important}
.det{border-top:1px solid var(--line);margin-top:10px;padding-top:2px}.det>h3:first-child{color:var(--mut)}
.waf .g{max-width:120px}.waf{gap:14px;margin:8px 0;grid-template-columns:repeat(4,1fr)}#c-waf{grid-template-columns:repeat(3,1fr)}#c-odds{display:block}
p:has(+div),p:has(+.lg),p:has(+.tw),.lg{break-after:avoid}.tw,table{break-inside:avoid}a{color:#1d5fb0}.nb{break-inside:avoid}
</style>'''
LIGHT = '<script>document.documentElement.dataset.theme="light"</script>'


def prep(src, num, extra_js='', subs=()):
    h = open(src, encoding='utf8').read()
    for a, b in subs:
        assert a in h, (src, a[:60])
        h = h.replace(a, b)
    h = h.replace('<details>', '<section class="det">').replace('</details>', '</section>').replace('<summary>', '<h3>').replace('</summary>', '</h3>')
    h = h.replace('<h1>', f'<h1>{num}. ', 1)
    h = re.sub(r'<meta name="claude[^>]*>', '', h)
    body = h.index('<main>')
    return '<!doctype html><html lang="en"><meta charset="utf-8">' + LIGHT + h[:body] + PRINT + h[body:] + extra_js


def pdf(html, name):
    p = f'rep/{name}.html'; open(p, 'w', encoding='utf8').write(html); out = f'{HERE}/rep/{name}.pdf'
    if os.path.exists(out): os.remove(out)
    subprocess.run([EDGE, '--headless', '--disable-gpu', '--no-pdf-header-footer', '--window-size=800,1100', '--virtual-time-budget=8000', f'--print-to-pdf={out}', f'file:///{HERE}/{p}'], capture_output=True)
    for _ in range(40):
        if os.path.exists(out) and os.path.getsize(out) > 1000: break
        time.sleep(.5)
    time.sleep(1); return len(PdfReader(out).pages)


js1 = '''<script>
{const host=$('charts');let s='';[['lag','Returns, US session first'],['same','Returns, same date'],['level','Price levels']].forEach(([m,n])=>{M=m;draw();s+=`<h3 style="font-size:16px;margin-top:20px;${s?'break-before:page':''}">${n}</h3><p class="mut">${$('note').textContent}</p>`+host.innerHTML});$('note').textContent='';host.innerHTML=s;
let c='';[['SPX','S&amp;P 500'],['COMP','Nasdaq'],['DJI','Dow']].forEach(([k,n])=>{I=k;months();c+=`<div class="nb"><h3>${n}</h3>${$('c-mon').innerHTML}</div>`});$('c-mon').innerHTML=c}
</script>'''
inr = lambda v: '₹' + (lambda s: s if len(s) <= 3 else re.sub(r'(?<=\d)(?=(\d\d)+$)', ',', s[:-3]) + ',' + s[-3:])(str(int(round(v))))
al = ''.join(f'<tr><td>{inr(c)}</td>' + ''.join(f'<td>{inr(c*s)} (band {inr(c*(s-.05))} to {inr(c*(s+.05))})</td>' for s in (.1, .2, .3)) + '</tr>' for c in (500000, 1000000, 2000000))
alloc = f'<h3>Target US holding, by portfolio size</h3><div class="tw"><table><thead><tr><th>Portfolio</th><th>10% share</th><th>20% share</th><th>30% share</th></tr></thead><tbody>{al}</tbody></table></div><p class="mut">Band is 5 points either side of the target. Do nothing while the holding is inside it.</p>'
Z = json.load(open('s3b.json')); K = Z['K']; DEF = {'BANK': 30, 'IT': 15, 'ENERGY': 12, 'FMCG': 10, 'AUTO': 8, 'PHARMA': 7, 'METAL': 5, 'INFRA': 5, 'FIN': 5, 'REALTY': 2, 'PSUBANK': 1}
def port(w):
    t = sum(w.values()); x = [w.get(k, 0) / t for k in K]; b = sum(v * Z['tab'][k][1] for v, k in zip(x, K)); q = sum(x[i] * x[j] * Z['cov'][i][j] for i in range(len(K)) for j in range(len(K))); return b, math.sqrt(q)
g = lambda v: ('−' if round(v, 2) < 0 else '+' if round(v, 2) > 0 else '') + f'{abs(v):.2f}%'
MIX = [('Example mix', DEF), ('All IT', {'IT': 1}), ('All banks', {'BANK': 1}), ('FMCG and pharma, half each', {'FMCG': 1, 'PHARMA': 1})]
sm = ''
for n, w in MIX:
    b, sd = port(w); sm += f'<tr><td>{n}</td>' + ''.join(f'<td>{g(b*m)}</td>' for m in (-3, -2, -1, 1, 2)) + f'<td>± {sd:.2f}%</td></tr>'
secs = f'<h3>Likely next session, by S&amp;P move</h3><div class="tw"><table><thead><tr><th>Portfolio</th><th>S&amp;P −3%</th><th>−2%</th><th>−1%</th><th>+1%</th><th>+2%</th><th>Two in three sessions fall within</th></tr></thead><tbody>{sm}</tbody></table></div><p class="mut">Example mix: banks 30%, IT 15%, energy 12%, FMCG 10%, autos 8%, pharma 7%, metals 5%, infra 5%, financials 5%, realty 2%, PSU banks 1%. These are placeholder weights.</p>'
CH = [('c1', 'Is the correlation turning negative?', prep('us_nifty.html', 1, js1, [('<h2>Explore month','<h2 style="break-before:page">Explore month')])),
      ('c2', 'Yields, oil and the dollar', prep('macro_regimes.html', 2, '', [('Hover or tap to read a month.', ''), ('Do foreign flows (NSDL) and mutual-fund SIPs explain why domestic money blunted the US link?', 'Do foreign flows (NSDL) and mutual-fund SIPs explain why domestic money blunted the US link? Chapter 4 tests foreign flows. Domestic flows are still open.')])),
      ('c3', 'Four tests of what to do', prep('action_tests.html', 3, '', [('-0.00%','0.00%'), ('Foreign flows were tested afterwards.', 'Foreign flows are in chapter 4.')])),
      ('c4', 'Playbook: allocation, sectors, flows', prep('playbook.html', 4, '', [('<p class="mut">The 10 lakh rupees is an example. Change it to your own.</p>', alloc), ('Set your sector weights and a US move. The answer is the typical effect on the next Indian session, using 2021 to 2024.', 'The table shows the typical effect on the next Indian session, using 2021 to 2024.'), ('<p class="mut">The weights shown are placeholders and are rescaled to 100%.</p>', secs)]))]
pages = {n: pdf(h, n) for n, _, h in CH}; print(pages)
front = lambda toc: '<!doctype html><html lang="en"><meta charset="utf-8">' + LIGHT + '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap"><style>' + open('simple.css', encoding='utf8').read() + '</style>' + PRINT + f'''<main>
<div style="height:930px;display:flex;flex-direction:column;justify-content:space-between;break-after:page"><div style="padding-top:150px"><h1 style="font-size:44px;max-width:600px">NIFTY and the US</h1><p class="lead" style="font-size:19px;max-width:520px">How closely India's market follows Wall Street, what drives it, and what to do about it</p><p class="mut" style="margin-top:24px">Version 2. Data to 24 November 2026. Report dated 25 November 2026.</p></div>
<div><h3>Contents</h3><table style="font-size:13px"><tbody>{toc}</tbody></table></div></div>
<h1>Summary</h1>
<p class="lead">NIFTY has drifted away from the US in 2026 but does not move opposite to it. The link is useful for spreading risk. We found no trade in it.</p>
<h2>What we found</h2>
<div class="tw"><table><thead><tr><th>Question</th><th class="l">Answer</th><th class="l">How sure</th><th>Chapter</th></tr></thead><tbody>
<tr><td>Is the daily link negative?</td><td class="w">No. It was 0.40 in 2023, then 0.18, 0.26 and 0.25. It has been positive every year since 2015, though about zero in 2019</td><td class="w">Good</td><td>1</td></tr>
<tr><td>Did the trends split?</td><td class="w">Yes. NIFTY is down 3.0% in 2026 and the S&amp;P is up 5.2%. The yearly price-level correlation is −0.36, the first negative since at least 2015</td><td class="w">Fair. Trending prices give large readings easily</td><td>1</td></tr>
<tr><td>Has the link faded lately?</td><td class="w">From July to October 2026 it is 0.10, or 0.02 with November. Japan, Taiwan, Korea and Australia are 0.28 to 0.41, and Hong Kong is 0.04</td><td class="w">Fair, 85 to 100 sessions</td><td>1</td></tr>
<tr><td>Is there a weekly or quarterly decoupling trend?</td><td class="w">None that lasts. Weekly correlation is −0.03 in 2026 but 0.38 without November. Quarterly tests found no reliable trend</td><td class="w">Fair</td><td>1</td></tr>
<tr><td>Do bond yields explain it?</td><td class="w">0 of 50 tests were significant. The India-US gap fell from 5.6 to 2.4 points and the link stayed near 0.3</td><td class="w">Fair. Small effects could be missed</td><td>2</td></tr>
<tr><td>Can we forecast the link?</td><td class="w">The long-run average beat HAR and a regime model. Next month's forecast is 0.28, with an 18% chance of a negative month</td><td class="w">Fair, 94 test months</td><td>2</td></tr>
<tr><td>Can we trade the gap?</td><td class="w">No. The open takes 0.23 of a 0.28 move. All three rules failed</td><td class="w">Good</td><td>3</td></tr>
<tr><td>Does a macro monitor warn of falls?</td><td class="w">No better than India VIX</td><td class="w">Fair, few crashes</td><td>3</td></tr>
<tr><td>Do US stocks lower risk?</td><td class="w">Yes. At 20%, volatility fell from 15.8% to 14.4% after tax and fees, and the worst fall from 34.4% to 31.4%</td><td class="w">Good on risk, 2015 to 2024 only</td><td>3, 4</td></tr>
<tr><td>Which sectors follow the US?</td><td class="w">IT, realty and metals most. FMCG and pharma least. 2026 broke part of this order</td><td class="w">Fair</td><td>3, 4</td></tr>
<tr><td>Do foreign flows explain 2026?</td><td class="w">They account for about half of the gap and do not predict the next month</td><td class="w">Fair. Same-month links do not show cause</td><td>4</td></tr>
</tbody></table></div>
<h2>What to do</h2>
<ul><li>Consider a fixed US share of 10% to 30%. Rebalance only when it moves 5 points from target, and use new savings first. If the US only matches NIFTY, 20% costs about 0.1% a year. If it trails by 3%, the cost is about 0.6%.</li>
<li>Do not trade NIFTY on the previous US session. Expect an opening gap of about 0.23% per 1% in the S&amp;P.</li>
<li>Use India VIX and volatility forecasts on the risk dashboard. Show the macro regime as a label at most.</li>
<li>Use foreign flows to explain a month that has ended.</li>
<li>Recheck the sector map once a year.</li></ul>
<h2>Read this before relying on it</h2>
<ul><li>This is version 2. The first version said the link was about zero since July and weakest in NIFTY, and that 21-session correlations showed the clearest weakening. Those depended heavily on November 2026 and are corrected here.</li><li>A separate volatility project reserves January 2025 to October 2026 as a holdout. Chapters 1, 2 and parts of 3 and 4 show NIFTY outcomes in that window, so it is no longer unseen for US and NIFTY ideas. No volatility model was run on it.</li>
<li>The yield, regime, trading, portfolio, monitor, sector and flow rules were fixed before their results were seen, but some periods had been looked at in earlier work. Many views of the same data were taken, so some differences are chance.</li>
<li>Monthly flows come from a public GitHub copy of NSDL data. Its ten complete 2026 months match a second copy. Earlier years were not checked against NSDL, and November is incomplete.</li>
<li>Tax rules come from secondary sources that disagree on some funds, and fund fees are our assumptions. Ask a chartered accountant before investing.</li>
<li>Portfolio figures differ slightly between chapters. Chapter 3 is before tax and fund fees with monthly rebalancing, and chapter 4 is after both with a 5-point band.</li>
<li>Still open: domestic flows over a longer history, earnings and valuation gaps, and daily Indian yields.</li>
<li>This is research for discussion. It is not investment or tax advice.</li></ul>
</main>'''
def toc(nf):
    p = nf + 1; s = f'<tr><td>Summary</td><td>2</td></tr>'
    for i, (n, t, _) in enumerate(CH, 1): s += f'<tr><td>{i}. {t}</td><td>{p}</td></tr>'; p += pages[n]
    return s
nf = pdf(front(toc(3)), 'front'); nf = pdf(front(toc(nf)), 'front')
W = PdfWriter(); no = 0; total = nf + sum(pages.values())
for n, t in [('front', None)] + [(a, b) for a, b, _ in CH]:
    for i, pg in enumerate(PdfReader(f'rep/{n}.pdf').pages):
        no += 1
        if no > 1:
            buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=A4); c.setFont('Helvetica', 8); c.setFillGray(.4); c.drawString(45, 26, 'NIFTY and the US' + (f'  |  {t}' if t else '')); c.drawRightString(A4[0] - 45, 26, f'{no} of {total}'); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0])
        W.add_page(pg)
        if n == 'front' and i == 1: W.add_outline_item('Summary', no - 1)
        if t and i == 0: W.add_outline_item(f'{CH.index(next(x for x in CH if x[0] == n)) + 1}. {t}', no - 1)
W.add_metadata({'/Title': 'NIFTY and the US: research report'})
W.write('NIFTY_and_the_US_report.pdf'); print('pages', total, os.path.getsize('NIFTY_and_the_US_report.pdf') // 1024, 'KB')
