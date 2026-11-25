import json, re
A = {k: json.load(open(f'{k}.json')) for k in ('s1', 's3', 's4', 's5')}
tr = ''.join(f"<tr><td>{t[0]*100:.1f}%</td><td>{t[1]}</td><td>{t[2]}</td><td>{t[3]:+.1f}</td><td>{t[5]:.1f}</td><td>{t[6]:+.1f}</td><td>{t[7]:.2f}</td><td>{t[8]:+.1f}</td></tr>" for t in A['s1']['tr'])
bk = ''.join(f"<tr><td>{b[0].replace('<','&lt;').replace('>','&gt;')}</td><td>{b[1]}</td><td>{b[2]:+.2f}%</td><td>{b[4]:+.2f}% ± {b[5]:.2f}</td></tr>" for b in A['s1']['bk'])
wm = ''.join(f'<tr><td>{w[0]}</td><td>{w[1]}%</td><td>{w[2]}%</td></tr>' for w in A['s4']['worst'])
nm = {'NIFTY': 'NIFTY 50', **A['s3']['names']}
yr = ''.join(f"<tr><td>{nm[k]}</td>" + ''.join(f'<td>{v[y]}%</td>' for y in ('2023', '2024', '2025', '2026')) + '</tr>' for k, v in A['s3']['ret'].items())
html = '''<title>NIFTY and US Action Tests</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap">
<style>
''' + open('simple.css', encoding='utf8').read() + '''</style>
<main>
<h1>What can you do with the NIFTY and US link?</h1>
<p class="lead">Use it to diversify. Of four ideas we tested, holding some US stocks passed clearly. Trading NIFTY after big US moves failed, a macro warning system failed, and sector differences are real but small.</p>
<p>We wrote the pass rules before running anything.</p>
<div class="tw"><table><thead><tr><th>Idea</th><th class="l">Result</th><th class="l">What to do</th></tr></thead><tbody>
<tr><td>Trade NIFTY after big US moves</td><td class="w">Failed</td><td class="w">Drop it. Expect the gap and avoid chasing it</td></tr>
<tr><td>Pick sectors by US exposure</td><td class="w">Ranking passed, 2026 did not follow it</td><td class="w">Use for rough risk awareness only</td></tr>
<tr><td>Hold some US stocks</td><td class="w">Passed</td><td class="w">Consider 10% to 30%. Check taxes and fund costs</td></tr>
<tr><td>Macro warning monitor</td><td class="w">Failed</td><td class="w">Watch India VIX instead</td></tr></tbody></table></div>

<h2>The opening gap takes most of the move</h2>
<p>For every 1% the S&amp;P moves, NIFTY futures move about 0.28% from the previous close to 15:20. The open accounts for 0.23 of that. After the first five minutes, 0.02 is left, which cannot be told apart from zero.</p>
<div id="c-gap"></div>
<p>We then tested following the US direction from 09:20 to 15:20 with futures, in 2020 to 2022 first and 2023 to October 2024 as a check. None of the three thresholds passed. The 1.5% rule made 3.1 bp a trade after costs in the first period (t = 0.28), and lost money when costs were doubled. Its 11.5 bp in the check period comes from 29 trades.</p>
<details><summary>All trading results</summary><p class="mut">Basis points per trade. 1 bp is 0.01%.</p><div class="tw"><table><thead><tr><th>S&amp;P move</th><th>Period</th><th>Trades</th><th>Gross</th><th>Cost</th><th>Net</th><th>Net t</th><th>Net, 2x cost</th></tr></thead><tbody>''' + tr + '''</tbody></table></div><h3>Average move by size of US session</h3><div class="tw"><table><thead><tr><th>S&amp;P</th><th>Days</th><th>Opening gap</th><th>09:20 to 15:20</th></tr></thead><tbody>''' + bk + '''</tbody></table></div><p class="mut">The profit in 2020 to 2022 came from 2020. 2021 and 2022 lost money at all three thresholds. Leaving out 20 February to May 2020, the gap takes 0.28 of a 0.27 total.</p></details>

<h2>Holding US stocks lowered risk in both halves</h2>
<p>We mixed NIFTY 50 with the S&amp;P 500 in rupees, dividends included, and rebalanced monthly. With 20% in the US, yearly volatility fell from 15.8% to 14.5% over 2015 to 2024, and the worst fall shrank from 34.3% to 31.3%.</p>
<div class="lg"><span><i style="background:var(--s1)"></i>2015 to 2019</span><span><i style="background:var(--s3)"></i>2020 to 2024</span></div><div id="c-vol"></div>
<p class="mut">Yearly volatility by share held in the S&amp;P 500. Lower is calmer.</p>
<p>The cut in volatility at 20% was 8.7% of its starting level, with a 95% range of 5.5% to 11.9%. It was 12.8% in the first half and 6.4% in the second, so the benefit got smaller as the two markets moved more closely. The lowest-risk share was 50% in the first half and 40% in the second, and the curve is flat near there.</p>
<h3>It helps less in a crash</h3>
<div id="c-ev"></div>
<p>In NIFTY's 26 worst weeks out of about 520, it lost 5.0% on average and the S&amp;P in rupees lost 1.9%. The S&amp;P rose in 35% of those weeks. It fell more than NIFTY in the first half of 2022. NIFTY's worst month of 2015 to 2019 was no better with 20% in the US.</p>
<p>The rupee does part of the work. A currency-hedged S&amp;P at 20% also lowered volatility, to 14.8% against 14.5% unhedged.</p>
<p>Returns were higher with US stocks too, but that came from a strong US decade and is no forecast. We left out taxes, fund fees, remittance limits and tracking error.</p>
<details><summary>Full table and NIFTY's 12 worst months</summary><div class="tw"><table><thead><tr><th>US share</th><th>Return a year</th><th>Volatility</th><th>Worst fall</th><th>Worst month</th></tr></thead><tbody id="t-p"></tbody></table></div><p class="mut">2015 to 2024, unhedged, net of 0.125% per side on rebalancing trades.</p><div class="tw"><table><thead><tr><th>Month</th><th>NIFTY</th><th>S&amp;P in rupees</th></tr></thead><tbody>''' + wm + '''</tbody></table></div></details>

<h2>No sector hides a strong US link</h2>
<p>We thought a near-zero NIFTY link might hide IT stocks following the Nasdaq. The data says no: since July 2026 IT's link to the S&amp;P is −0.01 and metals are highest at 0.17. From July to October alone, IT is 0.01 and financials are highest at 0.21.</p>
<div class="tw hm" id="c-sec"></div>
<p class="mut">Correlation with the previous S&amp;P 500 session. 2026 runs to 24 November.</p>
<p>The order of sectors held up between 2015 to 2020 and 2021 to 2026 (rank correlation 0.84 with the S&amp;P, p = 0.001, and 0.73 with the Nasdaq). FMCG, PSU banks and pharma were the least linked in the first half. Pharma has since moved up. IT's edge over banks is small: 0.05 in the first half (range −0.03 to 0.13) and 0.08 in the second (0.02 to 0.15).</p>
<p>2026 broke that order. Without November every sector we list has a higher 2026 link (IT 0.16, metals 0.35). Metals became the most linked sector and IT fell to 0.11 with November included, its lowest year in the data. Sensitivity to US yields was no guide: the ranking did not hold (0.18, p = 0.29).</p>
<details><summary>Sector returns</summary><div class="tw"><table><thead><tr><th>Price return</th><th>2023</th><th>2024</th><th>2025</th><th>2026 to 24 Nov</th></tr></thead><tbody>''' + yr + '''</tbody></table></div><p>IT is down 15.9% in 2026 after falling 12.6% in 2025, so the sector lags as well as decoupling.</p></details>

<h2>The macro monitor did not beat India VIX</h2>
<p>We counted six flags: US yields, the dollar, Brent, USDINR, US VIX and India VIX. The task was to warn of a NIFTY fall of 5% or more from today's close within 21 sessions. A score of 0.50 is a coin toss and 1.00 is perfect.</p>
<div class="lg"><span><i style="background:var(--r3)"></i>Macro monitor (6 flags)</span><span><i style="background:var(--s1)"></i>India VIX alone</span></div><div id="c-auc"></div>
<p>The monitor was almost a coin toss in 2015 to 2021 and worse than India VIX in both periods. Adding macro counts to India VIX did not help either. The gap's range includes zero, so we can say it failed to beat India VIX and not that it is clearly worse.</p>
<p>India VIX is better at ranking future volatility (rank correlation 0.63 and 0.67) than at calling falls (0.54 and 0.76). In the check period red days were followed by a 5% fall 31% of the time against 8% for green, but those days come from only 12 red episodes, and only 2 of those 12 starts were followed by such a fall. In the first period red and green were both 16%.</p>
<h3>Reading on 25 November 2026</h3>
<p>Two of six flags are on, the dollar and US VIX at 26.4, which is amber. The figures show no reason to act on that.</p>

<h2>What to do now</h2>
<ul><li>Close the opening-gap trade. A trader can use 0.23% per 1% of S&amp;P as the usual opening gap and not chase it.</li>
<li>Take the US allocation result to the group and settle the tax, remittance and fund-cost side before choosing a share.</li>
<li>Show India VIX and the volatility forecasts on the risk dashboard. Keep the macro regime as a label at most.</li>
<li>Use the sector table as a rough map of US exposure and recheck it yearly, since 2026 moved off it.</li>
<li>Foreign flows were tested afterwards. They account for about half of the 2026 gap and do not predict the next month. Domestic flows are still untested.</li></ul>
<details><summary>Method and limits</summary><ul>
<li>The trading test uses 5-minute NIFTY futures, entry at the 09:20 open and exit at the 15:20 open, with dated costs of about 4.1 to 4.5 bp. The futures series rolls each month, which adds noise to a few gaps. Both periods of this index data were used in earlier studies, so the check is not pristine.</li>
<li>The portfolio test is weekly, so it blurs the time-zone gap. Using the US close from one session earlier gave the same conclusion.</li>
<li>The monitor was fitted on 2015 to 2021 and checked on 2022 to 2024, with the windows that overlap removed. Ranges use 63-session blocks. Crash warnings are rare, so all of these are uncertain.</li>
<li>The trading, portfolio and monitor tests stop at the end of 2024 at the latest. A separate volatility project reserves 2025 to October 2026. The sector study goes to November 2026.</li>
<li>Sources are Yahoo Finance, NSE total return index, US Treasury and a vendor futures file. This is research for discussion and not investment advice.</li></ul></details>
</main>
<script>
const A=/*DATA*/,$=i=>document.getElementById(i),f=(v,d=2)=>(v<0&&+v.toFixed(d)!==0?'−':'')+Math.abs(v).toFixed(d);
const W=id=>Math.max(300,$(id).clientWidth);
const pc=v=>`color-mix(in srgb,var(${v<0?'--neg':'--pos'}) ${Math.min(60,Math.abs(v)/.5*60).toFixed(0)}%,var(--bg))`;
const NM=/*NAMES*/,PR=['2015-20','2021-26','2023','2024','2025','2026','H2 2026'];
$('c-sec').innerHTML='<table><thead><tr><th>Sector</th>'+PR.map(p=>`<th>${p.replace('2015-20','2015 to 20').replace('2021-26','2021 to 26')}</th>`).join('')+'</tr></thead><tbody>'+Object.keys(A.s3.spx).sort((a,b)=>A.s3.spx[b]['2015-20']-A.s3.spx[a]['2015-20']).map(k=>`<tr><td>${NM[k]}</td>`+PR.map(p=>`<td style="background:${pc(A.s3.spx[k][p])}">${f(A.s3.spx[k][p])}</td>`).join('')+'</tr>').join('')+'</tbody></table>';
$('t-p').innerHTML=[0,10,20,30,40,50].map(w=>{const r=A.s4['0|2015-24|U|'+w];return `<tr><td>${w}%</td><td>${r[0].toFixed(1)}%</td><td>${r[1].toFixed(1)}%</td><td>${f(r[2],1)}%</td><td>${f(r[3],1)}%</td></tr>`}).join('');
function draw(){
{const s=A.s1.slope.find(x=>x[0]=='all'),w=W('c-gap'),rows=[['Total, close to 15:20',s[2],'--r3'],['Opening gap',s[5],'--s1'],['First 5 minutes',s[8],'--s1'],['09:20 to 15:20',s[11],'--s1']],L=150,S=(w-L-60)/.32;
$('c-gap').innerHTML=`<svg viewBox="0 0 ${w} 160" height="160" role="img" aria-label="NIFTY move per 1% S&amp;P move">${rows.map(([n,v,c],i)=>`<text x="${L-8}" y="${i*38+24}" text-anchor="end">${n}</text><rect x="${L}" y="${i*38+8}" width="${Math.max(2,v*S)}" height="24" fill="var(${c})"/><text class="pt" x="${L+v*S+8}" y="${i*38+25}">${f(v)}%</text>`).join('')}</svg>`}
{const w=W('c-vol'),h=250,l=46,r=14,t=14,b=44,X=v=>l+(w-l-r)*v/50,Y=v=>t+(h-t-b)*(20-v)/(20-8);let g=[8,12,16,20].map(v=>`<line x1="${l}" x2="${w-r}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(--line)"/><text x="${l-6}" y="${Y(v)+4}" text-anchor="end">${v}%</text>`).join('');
[['2015-19','--s1'],['2020-24','--s3']].forEach(([p,c])=>{const q=[0,10,20,30,40,50].map(k=>[k,A.s4['0|'+p+'|U|'+k][1]]);g+=`<polyline fill="none" stroke="var(${c})" stroke-width="2.5" points="${q.map(a=>X(a[0])+','+Y(a[1])).join(' ')}"/>`+q.map(a=>`<circle cx="${X(a[0])}" cy="${Y(a[1])}" r="5" fill="var(${c})"><title>${p}: ${a[0]}% US, ${a[1]}% volatility</title></circle>`).join('')+`<text class="pt" x="${X(0)+8}" y="${Y(q[0][1])-9}">${q[0][1]}%</text><text class="pt" x="${X(20)}" y="${Y(q[2][1])-10}" text-anchor="middle">${q[2][1]}%</text>`});
$('c-vol').innerHTML=`<svg viewBox="0 0 ${w} ${h}" height="${h}" role="img" aria-label="Volatility by US share">${g}${[0,10,20,30,40,50].map(k=>`<text x="${X(k)}" y="${h-22}" text-anchor="${k==50?'end':k?'middle':'start'}">${k}%</text>`).join('')}<text x="${X(25)}" y="${h-4}" text-anchor="middle">Share in the S&amp;P 500</text></svg>`}
{const w=W('c-ev'),ev=[['Covid 2020','Feb to Mar 2020'],['2018 Sep-Oct','Sep to Oct 2018'],['2022 H1','Jan to Jun 2022']].map(([k,n])=>[n,A.s4['ev|'+k]]),L=125,S=(w-L-105)/30;
$('c-ev').innerHTML=`<svg viewBox="0 0 ${w} 190" height="190" role="img" aria-label="Falls in three sell-offs">${ev.map(([n,v],i)=>`<text x="${L-8}" y="${i*62+32}" text-anchor="end">${n}</text><rect x="${L}" y="${i*62+6}" width="${-v[0]*S}" height="20" fill="var(--r3)"/><text class="pt" x="${L-v[0]*S+6}" y="${i*62+21}">NIFTY ${f(v[0],1)}%</text><rect x="${L}" y="${i*62+30}" width="${-v[1]*S}" height="20" fill="var(--s1)"/><text class="pt" x="${L-v[1]*S+6}" y="${i*62+45}">S&amp;P ${f(v[1],1)}%</text>`).join('')}</svg>`.replaceAll('text class="pt" x','text class="pt" x')}
{const w=W('c-auc'),rows=[['2015 to 2021',A.s5.auc[0][3]],['2022 to 2024',A.s5.auc[1][3]]],L=110,X=v=>L+(w-L-60)*(v-.4)/.45;
$('c-auc').innerHTML=`<svg viewBox="0 0 ${w} 165" height="165" role="img" aria-label="Warning scores"><line x1="${X(.5)}" x2="${X(.5)}" y1="18" y2="150" stroke="var(--fg)" stroke-dasharray="4 3"/><text class="pt" x="${X(.5)}" y="13" text-anchor="middle">Coin toss</text>${rows.map(([n,a],i)=>`<text x="${L-8}" y="${i*68+52}" text-anchor="end">${n}</text><rect x="${L}" y="${i*68+26}" width="${X(a.all6)-L}" height="20" fill="var(--r3)"/><text class="pt" x="${X(a.all6)+6}" y="${i*68+41}">${f(a.all6)}</text><rect x="${L}" y="${i*68+50}" width="${X(a.iv)-L}" height="20" fill="var(--s1)"/><text class="pt" x="${X(a.iv)+6}" y="${i*68+65}">${f(a.iv)}</text>`).join('')}</svg>`}}
draw();let z;addEventListener('resize',()=>{clearTimeout(z);z=setTimeout(draw,150)});
</script>
'''
html = html.replace('/*DATA*/', json.dumps({k: A[k] for k in A}, separators=(',', ':')).replace('NaN', 'null')).replace('/*NAMES*/', json.dumps(nm))
open('action_tests.html', 'w', encoding='utf8').write(html)
print('dashes', len(re.findall('[—–]', html)))
