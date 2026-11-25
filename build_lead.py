import json, re, pandas as pd
R = pd.read_csv('lead_tests.csv'); S = json.load(open('lead_series.json'))
f = lambda v, d=2: 'n/a' if pd.isna(v) else ('−' if round(v, d) < 0 else '') + f'{abs(v):.{d}f}'
Y = {'rel4': 'NIFTY minus S&amp;P, 4 weeks', 'rel13': 'NIFTY minus S&amp;P, 13 weeks', 'link13': 'Link, 13 weeks'}
R['x'] = R.x.str.replace('&', '&amp;')
allt = ''.join(f"<tr><td>{r.x}</td><td>{Y[r.y]}</td><td>{f(r.c1)}</td><td>{f(r.p1,3)}</td><td>{f(r.c2)}</td><td>{f(r.p2one)}</td></tr>" for r in R.sort_values('p1').itertuples())
top = ''.join(f"<tr><td>{r.x}</td><td>{Y[r.y]}</td><td>{f(r.c1)}</td><td>{f(r.p1,3)}</td><td>{f(r.c2)}</td><td>{f(r.p2one)}</td></tr>" for r in R.sort_values('p1').head(5).itertuples())
Q = [('Q1 2023', .51, -11.0, -26), ('Q1 2024', -.08, -7.0, 11), ('Q4 2024', .14, -10.8, -100), ('Q3 2025', 0., -11.1, -77), ('Q1 2026', .61, -11.0, -131), ('Q2 2026', .21, -7.2, -143), ('Q3 2026', .17, -7.4, 14), ('Q4 2026', 0., 17.5, 87)]
qt = ''.join(f'<tr><td>{a}</td><td>{f(b)}</td><td>{f(c,1)}</td><td>{f(d,0)}</td></tr>' for a, b, c, d in Q)
html = '''<title>NIFTY Decoupling Signals</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap">
<style>
''' + open('simple.css', encoding='utf8').read() + '''</style>
<main>
<h1>Can anything warn of a split between NIFTY and the US?</h1>
<p class="lead">Not that we could find. The correlation line reacts late, and none of 70 tests of bond spreads and other measures gave an earlier warning. The best open idea is that India gains when AI and chip stocks fall. It is growing since 2023 but not proven.</p>

<h2>The signal is there, and it is late</h2>
<p>We simulated a link that drops suddenly from 0.30 to −0.20. A 13-week correlation takes about 36 trading days to show it. Faster versions take about 10, and raise about three false alarms a year.</p>
<div class="lg"><span><i style="background:var(--s1)"></i>Days to notice</span></div><div id="c-det"></div>
<p class="mut">Median delay. False dips a year are in brackets.</p>
<h3>Slow and fast measures since 2023</h3><div class="lg"><span><i style="background:var(--s1)"></i>13 weeks (63 sessions)</span><span><i style="background:var(--s3)"></i>Fast, 10-day half-life</span></div><div id="c-ser"></div>
<p>This time the fast measure first went below zero on 15 October 2026 and reached −0.36 on 3 November. By 23 November it was back at 0.05. It crossed below zero 9 times in 2024 and 6 in 2025, so it cannot be used alone. Korea, Taiwan and Japan read 0.53 to 0.67 against the S&amp;P on the same measure.</p>
<p>Dips below zero are common even when nothing has changed. With a constant link, simulations since 2023 produce about 2.5 separate dips, and 47% of them show three or more. We saw three.</p>

<h2>Bond spreads and other early warnings</h2>
<p>We tried 24 measures against NIFTY minus S&amp;P over the next 4 and 13 weeks, and the link over the next 13. We searched 2015 to 2022 and checked 2023 to September 2026. To pass, a measure had to survive a correction for many tests and then hold up in the check.</p>
<div id="c-70"></div><p><b>0 of 70 passed.</b> Four looked significant in the first period, and chance alone gives 3.5.</p>
<div class="tw"><table><thead><tr><th>Closest five</th><th>Target</th><th>2015 to 2022</th><th>p</th><th>Check</th><th>p</th></tr></thead><tbody>''' + top + '''</tbody></table></div>
<p>Yields, the US curve, real yields, breakevens, the India-US gap, the Indian curve, high yield, EM bonds, bond volatility, the dollar, the rupee, oil, VIX and foreign flows all failed. Flows move with the gap in the same month (0.31) and last month's flow does not lead it. Chips against the S&amp;P came closest on the 13-week return gap, at −0.41 and then −0.18 in the check.</p>
<p>The India-US 10-year gap was low before all three dips (−2.3, −1.9 and −1.1 standard deviations). It was low for most of 2023 to 2026, so it cannot time them.</p>
<details><summary>All 70 tests and 2 without enough early data</summary><div class="tw"><table><thead><tr><th>Measure</th><th>Target</th><th>2015 to 2022</th><th>p</th><th>Check</th><th>p</th></tr></thead><tbody>''' + allt + '''</tbody></table></div><p class="mut">The second p is one-sided, in the direction found first.</p></details>

<h2>This quarter, India broke away from Korea and Taiwan</h2>
<p>From 1 October to 24 November 2026 NIFTY rose 12.1% while Korea fell 26.8%, Taiwan 16.3% and the Nasdaq 11.6%. Same-date correlations with NIFTY turned negative, and the 95% ranges stay below zero. The quarter was picked after seeing it.</p>
<div id="c-kt"></div>
<p>Korea and Taiwan kept their usual link to the S&amp;P (0.45 and 0.47). India is the market that separated.</p>

<h2>Does decoupling mean money rotated?</h2>
<p>Partly, for this quarter. Foreigners bought a net 87 thousand crore rupees of Indian shares, and in Q3 2025 they sold 77 thousand. The general rule does not hold.</p>
<div class="tw"><table><thead><tr><th>Quarter</th><th>Link</th><th>NIFTY minus S&amp;P, log %</th><th>Foreign net, thousand crore</th></tr></thead><tbody>''' + qt + '''</tbody></table></div>
<p>In Q1 2024 foreigners were net buyers while the link was at its lowest. Q1 2026 had 131 thousand crore of selling and the highest link. Over 23 quarters the size of flows and the link have no significant relation (0.25, p = 0.26). Flows and the return gap are at 0.57 since 2023 (p = 0.02), 0.34 over all 23 quarters (p = 0.11) and 0.26 without this quarter. Indian flow data cannot show that money left the US.</p>

<h2>The AI and chip idea</h2>
<p>Each bar is how much NIFTY moved in the same week for each 1% chips gained over the S&amp;P, after allowing for the S&amp;P. Below zero means India gains when chips lag.</p>
<div id="c-ai"></div>
<p>There was no effect in 2015 to 2022 (t = 0.6). It was −0.07 in 2023 to September 2026 (t = −1.9) and −0.09 in 2025 to September 2026 (t = −2.3). Our rule needed it in both long periods, so it fails. The last bar covers eight weeks (t = −1.8). Last week's chip move did not reliably predict NIFTY, so it gives no early warning.</p>
<p>In this quarter's five weeks of heavy chip underperformance NIFTY beat the S&amp;P by 4.4% on average, mostly in the week ending 6 November.</p>
<h3>The frozen test</h3><p>We fixed this test on 25 November 2026 for the 26 weeks ending 4 December 2026 to 28 May 2027. It passes if the chip effect is below zero with one-sided p under 0.05. We look once, after it ends.</p>

<h2>Where weekly data stands with November included</h2>
<p>November belongs in the data. With it, the same-Friday weekly correlation is 0.44, 0.38, 0.32 and 0.03 for 2023 to 2026. The 2026 drop from the three earlier years has a one-sided p of 0.06, and the 2026 figure has a range of −0.26 to 0.54. India has diverged from the US in returns this quarter. A negative correlation is not established.</p>

<h2>What to do</h2>
<ul><li>Watch the fast measure beside the 13-week line, and treat a dip as a reason to look. It is no trade signal.</li><li>Leave the chip test alone until it ends.</li><li>Find country ETF and fund flows for India, Korea, Taiwan and the US.</li><li>Stop testing yield spreads against this link.</li></ul>
<details><summary>Method and limits</summary><ul><li>Predictors use data before each Friday's close in India. Indian yields are lagged a full month and flows to the last complete month. Blocks do not overlap.</li><li>The check has 48 blocks of 4 weeks or 14 of 13 weeks, so modest effects could be missed.</li><li>Shared charts, the fourth quarter of 2026 and earlier yield tests had been seen before this protocol was written.</li><li>The delay simulation uses normal, independent days. Real breaks may look different.</li><li>Flow history is a third-party copy of NSDL data. The chip measure is SOXX against SPY.</li><li>A separate volatility project reserves January 2025 to October 2026, and these studies use that window.</li><li>Research for discussion. It is not investment advice.</li></ul></details>
</main>
<script>
const S=/*S*/,$=i=>document.getElementById(i),f=(v,d=2)=>(v<0&&+v.toFixed(d)!==0?'−':'')+Math.abs(v).toFixed(d),W=i=>Math.max(300,$(i).clientWidth);
$('c-70').innerHTML=`<div style="display:grid;grid-template-columns:repeat(24,1fr);gap:4px;max-width:520px;margin:8px 0;break-inside:avoid" role="img" aria-label="0 of 70 passed">${Array.from({length:70},()=>'<i style="aspect-ratio:1;background:var(--r3)"></i>').join('')}</div>`;
function draw(){
{const R=[['13 weeks',36,.4],['5 weeks',11,3.5],['Fast, 10 days',10,3]],w=W('c-det'),L=110,K=(w-L-150)/36;$('c-det').innerHTML=`<svg viewBox="0 0 ${w} 120" height="120" role="img" aria-label="Detection delay">${R.map(([n,v,a],i)=>`<text x="${L-8}" y="${i*38+24}" text-anchor="end">${n}</text><rect x="${L}" y="${i*38+8}" width="${v*K}" height="24" fill="var(--s1)"/><text class="pt" x="${L+v*K+8}" y="${i*38+25}">${v} days (${a})</text>`).join('')}</svg>`}
{const w=W('c-ser'),h=270,l=42,r=8,t=12,b=26,n=S.d.length,X=i=>l+(w-l-r)*i/(n-1),Y=v=>t+(h-t-b)*(.9-v)/1.4;let g=[-.4,0,.4,.8].map(v=>`<line x1="${l}" x2="${w-r}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(${v?'--line':'--zero'})"/><text x="${l-6}" y="${Y(v)+4}" text-anchor="end">${v?f(v,1):'0'}</text>`).join('');['2023','2024','2025','2026'].forEach(y=>{const i=S.d.findIndex(d=>d.startsWith(y));g+=`<text x="${X(i)}" y="${h-6}">${y}</text>`});[['fast','--s3',1.5],['slow','--s1',2.5]].forEach(([k,c,q])=>g+=`<polyline fill="none" stroke="var(${c})" stroke-width="${q}" stroke-linejoin="round" points="${S[k].map((v,i)=>X(i).toFixed(1)+','+Y(v).toFixed(1)).join(' ')}"/>`);
$('c-ser').innerHTML=`<div class="ch"><svg viewBox="0 0 ${w} ${h}" height="${h}" role="img" aria-label="Slow and fast correlation">${g}<line class="x" y1="${t}" y2="${h-b}" stroke="var(--fg)" stroke-opacity=".5" visibility="hidden"/></svg><div class="tip" hidden></div></div>`;
const sv=$('c-ser').querySelector('svg'),ln=sv.querySelector('.x'),tip=$('c-ser').querySelector('.tip');sv.addEventListener('pointermove',e=>{const i=Math.max(0,Math.min(n-1,Math.round((e.clientX-sv.getBoundingClientRect().left-l)/(w-l-r)*(n-1)))),x=X(i);ln.setAttribute('x1',x);ln.setAttribute('x2',x);ln.setAttribute('visibility','visible');tip.hidden=false;tip.innerHTML=`${S.d[i]}<br>13 weeks ${f(S.slow[i])}<br>Fast ${f(S.fast[i])}`;tip.style.left=(x>w/2?x-tip.offsetWidth-10:x+10)+'px'});sv.addEventListener('pointerleave',()=>{tip.hidden=true;ln.setAttribute('visibility','hidden')})}
{const R=[['Korea, Q1 2024',.32,.11,.51],['Korea, Q3 2025',.23,-.10,.47],['Korea, Q4 2026',-.31,-.60,-.11],['Taiwan, Q1 2024',.24,.05,.42],['Taiwan, Q3 2025',.22,.04,.37],['Taiwan, Q4 2026',-.43,-.62,-.16]],w=W('c-kt'),L=124,X=v=>L+(w-L-60)*(v+.7)/1.4;$('c-kt').innerHTML=`<svg viewBox="0 0 ${w} 250" height="250" role="img" aria-label="NIFTY correlation with Korea and Taiwan"><line x1="${X(0)}" x2="${X(0)}" y1="4" y2="222" stroke="var(--zero)"/>${R.map(([n,v,a,b],i)=>`<text x="${L-8}" y="${i*36+24}" text-anchor="end">${n}</text><line x1="${X(a)}" x2="${X(b)}" y1="${i*36+20}" y2="${i*36+20}" stroke="var(--fg)" stroke-width="2"/><circle cx="${X(v)}" cy="${i*36+20}" r="6" fill="var(${v<0?'--neg':'--pos'})"/><text class="pt" x="${X(b)+8}" y="${i*36+25}">${f(v)}</text>`).join('')}${[-.5,0,.5].map(v=>`<text x="${X(v)}" y="244" text-anchor="middle">${v?f(v,1):'0'}</text>`).join('')}</svg>`}
{const R=[['2015 to 2022',.03],['2023 to Sep 2026',-.07],['2025 to Sep 2026',-.09],['Oct to Nov 2026',-.16]],w=W('c-ai'),L=130,X=v=>L+(w-L-60)*(v+.18)/.26;$('c-ai').innerHTML=`<svg viewBox="0 0 ${w} 156" height="156" role="img" aria-label="Chip effect by period"><line x1="${X(0)}" x2="${X(0)}" y1="2" y2="152" stroke="var(--zero)"/>${R.map(([n,v],i)=>`<text x="${L-8}" y="${i*38+24}" text-anchor="end">${n}</text><rect x="${Math.min(X(0),X(v))}" y="${i*38+8}" width="${Math.abs(X(v)-X(0))}" height="24" fill="var(${v<0?'--neg':'--pos'})"/><text class="pt" x="${X(Math.max(v,0))+8}" y="${i*38+25}">${f(v)}</text>`).join('')}</svg>`}}
draw();let z;addEventListener('resize',()=>{clearTimeout(z);z=setTimeout(draw,150)});
</script>
'''.replace('/*S*/', json.dumps(S, separators=(',', ':')))
open('decoupling_signals.html', 'w', encoding='utf8').write(html); print('dashes', len(re.findall('[—–]', html)))
