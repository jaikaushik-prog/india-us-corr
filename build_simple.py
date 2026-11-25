import json
D = json.load(open('periods.json'))
f = lambda v: ('−' if round(v, 2) < 0 else '') + f'{abs(v):.2f}'
U = [('SPX', 'S&amp;P 500'), ('COMP', 'Nasdaq'), ('DJI', 'Dow')]
M = [('lag', 'Returns, US session first'), ('same', 'Returns, same date'), ('level', 'Price levels')]


def table(w):
    h = ''
    for m, name in M:
        h += f'<h3>{name}</h3><div class="tw"><table><thead><tr><th>Index</th>' + ''.join(f'<th>{p}</th>' for p in D[f'd_{m}_{w}']) + '</tr></thead><tbody>'
        for u, un in U:
            h += f'<tr><td>{un}</td>' + ''.join(f'<td>{f(v)}</td>' for v in D[f'{m}_{u}_{w}']) + '</tr>'
        h += '</tbody></table></div>'
    return h


head = '''<title>NIFTY vs US Indices</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap">
<style>
''' + open('simple.css', encoding='utf8').read() + '</style>\n'
body = '''<main>
<h1>Is NIFTY's correlation with the US turning negative?</h1>
<p class="lead">Mostly no. NIFTY has drifted away from the US in 2026, and its daily link to the S&amp;P 500 has been weak since July. Much of the sharper change comes from November 2026, when NIFTY rose as the US fell. It still does not tend to fall when the US rises.</p>
<p>Correlation runs from −1 to +1. At +1 two markets always move together, at 0 they ignore each other, and at −1 they move opposite ways. The dots show NIFTY against the S&amp;P 500, comparing each NIFTY day with the US session that finished before it.</p>
<div id="c-scale"></div>
<p class="mut">Daily closes to 24 November 2026 from Yahoo Finance, so 2026, its second half and November are incomplete. S&amp;P 500 unless stated. Nasdaq and Dow figures are further down.</p>

<h2>NIFTY fell behind in 2026</h2>
<p>NIFTY is down 3.0% this year while the S&amp;P 500 is up 5.2%. NIFTY also trailed the S&amp;P in each of the three years before, though both were rising then.</p>
<div class="lg"><span><i style="background:var(--fg)"></i>NIFTY 50</span><span><i style="background:var(--s1)"></i>S&amp;P 500</span><span><i style="background:var(--s2)"></i>Nasdaq</span><span><i style="background:var(--s3)"></i>Dow</span></div><div id="c-lev"></div>
<p class="mut">Each index starts at 100 at the end of 2022. Local currency.</p>
<div class="tw"><table><thead><tr><th>Price return</th><th>2023</th><th>2024</th><th>2025</th><th>2026 to 24 Nov</th></tr></thead><tbody><tr><td>NIFTY 50</td><td>20.0%</td><td>8.8%</td><td>10.5%</td><td>−3.0%</td></tr><tr><td>S&amp;P 500</td><td>24.2%</td><td>23.3%</td><td>16.4%</td><td>5.2%</td></tr><tr><td>Nasdaq</td><td>43.4%</td><td>28.6%</td><td>20.4%</td><td>2.1%</td></tr><tr><td>Dow</td><td>13.7%</td><td>12.9%</td><td>13.0%</td><td>4.1%</td></tr></tbody></table></div>

<h2>Two ways to measure it give two answers</h2>
<p>Price levels ask whether the two markets trended the same way over the year. Daily returns ask whether they moved the same way each day. Two markets can agree most days and still finish the year apart.</p>
<h3>Trend over the year: negative in 2026</h3><div id="c-ll"></div>
<p>2026 is the first negative year since at least 2015. From 2015 to 2025 this ranged between 0.18 and 0.93. The 2026 figures are −0.36 for the S&amp;P, −0.42 for Nasdaq and −0.09 for the Dow. In US dollars NIFTY's S&amp;P figure is −0.54, so the rupee made the gap wider. Trending prices can easily give large readings of either sign.</p>
<h3>Day by day: still positive every year</h3><div id="c-long"></div>
<p>The line through each dot is the 95% range. 2022 and 2023 were the two highest years, so a chart that starts in 2023 makes the fall look bigger than it is. 2024 to 2026 (0.18 to 0.26) sit just under the 0.27 to 0.31 of 2015 to 2018. Their ranges overlap too much to rank them, 2025 just includes zero, and 2019 was effectively zero at 0.01.</p>
<p>2025 also leans on one event. Without the April tariff shock (3 to 15 April), that year's S&amp;P correlation drops from 0.26 to 0.04.</p>

<h2>Since July, the link is weak in NIFTY and Hong Kong</h2>
<p>Each pair is a market's daily correlation with the S&amp;P 500. November makes a difference, so it is shown both ways.</p>
<div class="lg"><span><i style="background:var(--s1)"></i>July to October 2026</span><span><i style="background:var(--r3)"></i>July to November 2026</span></div>
<div id="c-pb"></div>
<p>From July to October NIFTY's link is 0.10 (95% range −0.07 to 0.26) and Hong Kong's is 0.04. With November, NIFTY's falls to 0.02 and it becomes the lowest. Japan, Taiwan, Korea and Australia are higher either way. In the first half of 2026 it was 0.43. NIFTY still moves with Asia: over 2026 its same-date correlation was 0.46 with Australia, 0.45 with Hong Kong, 0.31 with Japan, 0.30 with Korea and 0.13 with Taiwan.</p>
<details><summary>All markets, 2023 to 2026</summary><p>Hong Kong and NIFTY were the two least linked to the US every year. H2 2026 is part of 2026.</p><div class="tw hm" id="c-peer"></div></details>

<h2>NIFTY usually follows a big US move</h2>
<p>If NIFTY moved opposite to the US, it would fall after strong US days. It does the reverse. The blue squares show how often, out of 100, NIFTY closed higher in the session after each kind of US day since 2023.</p>
<div class="waf" id="c-waf"></div>
<p>NIFTY gained 0.54% on average after US rises above 1.5%, and lost 0.49% after falls of more than 1.5%. Part of that can happen at the open, before anyone can trade it, so this is no trading result.</p>
<details><summary>Average NIFTY move by size of US move</summary><p class="mut">2023 to 2026, close to close. Lines show 95% ranges.</p><div id="c-bk"></div><div class="tw"><table><thead><tr><th>S&amp;P move</th><th>Sessions</th><th>Average NIFTY return</th><th>NIFTY up</th></tr></thead><tbody id="t-bk"></tbody></table></div><h3>Every session</h3><p class="mut">Each dot is one NIFTY session since 2023, in percent. Two sessions beyond ±6% fall outside the frame.</p><div id="c-sc"></div></details>

<h2>The US explains a small share of NIFTY's day</h2>
<p>Picture all of NIFTY's daily movement as 100 squares. The blue ones are the share that the previous S&amp;P session accounts for.</p>
<div class="waf" id="c-r2"></div>
<p>A 1% S&amp;P move went with about 0.26% in NIFTY in 2026, against 0.30% in 2023.</p>
<details><summary>All years</summary><div class="tw"><table><thead><tr><th>Previous S&amp;P session</th><th>2022</th><th>2023</th><th>2024</th><th>2025</th><th>2026</th></tr></thead><tbody id="t-beta"></tbody></table></div></details>

<h2>The link is stronger when markets are nervous</h2>
<p>VIX measures how much fear is priced into US stocks. We split the days since 2023 into three equal groups by VIX.</p>
<div id="c-vix"></div>
<p>So diversifying between India and the US may help least in a scare. April 2025 drives part of this: without it, the high-VIX figure is 0.25. The same order appeared in 2015 to 2022 (0.21, 0.24, 0.32), but the ranges overlap.</p>

<h2>Longer holding periods look weaker only with November</h2>
<p>Measuring returns over a month of trading (21 sessions) reduces the time-zone problem. On that basis the correlation fell from 0.59 in 2023 to 0.22 in 2026. Without November 2026 it is 0.63, so the fall depends on that month.</p>
<div class="tw hm" id="c-hor"></div>
<p class="mut">Columns are the number of sessions each return covers, ending on the same date. Long returns overlap, so they hold few independent observations. Without November, 2026 reads 0.24, 0.36, 0.51, 0.57 and 0.63.</p>
<details><summary>Who leads, the US or India?</summary><p>The US. The previous US session is the one column that is clearly positive every year. NIFTY's own past moves say little about later US sessions.</p><div class="tw hm" id="c-lead"></div></details>

<h2>Weekly and quarterly: no lasting decoupling</h2>
<p>Our rule was that a decoupling trend must be significant whether it starts in 2023 or in 2015. Neither weekly nor quarterly data met it for the S&amp;P.</p>
<h3>Weekly returns against the S&amp;P</h3><div class="lg"><span><i style="background:var(--s1)"></i>As measured (red if negative)</span><span><i style="background:var(--s3)"></i>2026 without November</span></div><div id="c-wk"></div>
<p>Weekly correlation slides from 0.40 in 2023 to −0.03 in 2026. Without November 2026 it is 0.38, level with 2023. In the weeks ending 6 and 20 November NIFTY rose 8.2% and 2.6% while the S&amp;P fell 4.9% and 5.6%. The last 52 weeks are −0.01 with November and 0.38 without it (95% range 0.04 to 0.60).</p>
<h3>Quarterly</h3><div class="tw"><table><thead><tr><th>Test</th><th class="l">Result</th></tr></thead><tbody><tr><td>Daily correlation inside each quarter</td><td class="w">No trend: p = 0.17 from 2023 and 0.40 from 2015</td></tr><tr><td>Weekly correlation inside each quarter</td><td class="w">p = 0.12 from 2023 and 0.04 from 2015, which fails the rule</td></tr><tr><td>Correlation of quarterly returns</td><td class="w">0.74 in 2015 to 2022 and 0.35 in 2023 to 2026, from 16 quarters (range 0.03 to 0.75)</td></tr><tr><td>Quarters moving opposite ways</td><td class="w">6 of 16 since 2023, and 8 of 32 before</td></tr></tbody></table></div>
<p>The Nasdaq and Dow also fail the rule on the first two quarterly tests. One hint is left: NIFTY and the S&amp;P moved the same way in 73% of weeks in 2023, 67% in 2024, 54% in 2025 and 51% in 2026 (52% without November). We did not test that for significance. Dropping November was decided after seeing the result, so it shows how fragile the figure is. It is no reason to ignore the month. With November in, the drop in 2026 from 2023 to 2025 has a one-sided p of 0.06 on same-Friday returns.</p>

<h2>Explore month, half-year and year</h2>
<div class="ctl" role="group" aria-label="Correlation measure"><button id="b-lag" data-m="lag">Returns, US session first</button><button id="b-same" data-m="same">Returns, same date</button><button id="b-level" data-m="level">Price levels</button></div>
<p class="mut" id="note"></p>
<div class="lg"><span><i style="background:var(--s1)"></i>S&amp;P 500</span><span><i style="background:var(--s2)"></i>Nasdaq</span><span><i style="background:var(--s3)"></i>Dow</span></div>
<div id="charts"></div>
<h3>Month by month</h3><p class="mut">Returns with the US session first. Blue is positive and red is negative.</p>
<div class="ctl" role="group" aria-label="Index"><button id="i-SPX" data-i="SPX">S&amp;P 500</button><button id="i-COMP" data-i="COMP">Nasdaq</button><button id="i-DJI" data-i="DJI">Dow</button></div><div class="tw hm" id="c-mon"></div>
<p>Negative months against the S&amp;P numbered 1 in 2023, 6 in 2024, 3 in 2025 and 1 so far in 2026. A month has about 20 sessions, which makes its figure uncertain by roughly ±0.4.</p>
<details><summary>What the period figures show</summary>
<p>By year the S&amp;P went 0.40, 0.18, 0.26, 0.25. Half-years swing between about 0 and 0.45 with no clear direction. In the second half of 2026 the S&amp;P, Nasdaq and Dow are at 0.02, 0.00 and 0.09, after 0.43, 0.39 and 0.42 in the first half.</p>
<p>On price levels the S&amp;P went 0.91, 0.79, 0.76, −0.36, and the second half of 2026 is −0.58. Nasdaq is similar and the Dow is weaker, at 0.09 in that half. Most of the yearly change comes from 2026 alone.</p>
<p>Same-date returns in November 2026 are sharply negative (−0.61, −0.61 and −0.53) in an incomplete month. The three months before it were positive.</p>
<p>No trend in returns is significant at any frequency. On levels, the monthly downtrend is significant at 5% for the S&amp;P and Nasdaq (one-sided p about 0.03 and 0.02) but not for the Dow (0.45). Eight half-years and four years are too few for a strong test.</p></details>
<details><summary>Yearly figures</summary>''' + table('1y') + '''</details>
<details><summary>Half-yearly figures</summary>''' + table('6m') + '''</details>
<details><summary>Method and limits</summary>
<ul><li>NIFTY closes at 15:30 IST, before the US opens. "US session first" pairs each NIFTY return with the US sessions that closed since NIFTY's previous close. "Same date" asks whether the US followed NIFTY.</li>
<li>Each period figure is the Pearson correlation of daily log returns, or of daily closes for price levels, inside that period. Periods do not overlap and prices are in local currency.</li>
<li>Trend p-values come from shuffling the order of periods 4,000 times, with no adjustment for the number of tests. Yearly ranges use a bootstrap with 5-session blocks.</li>
<li>Other Asian markets use their own closes and the US sessions since their previous close.</li>
<li>With this many cuts of the same data, some differences will be chance. We tested no strategies and included no trading costs.</li>
<li>Yahoo lacks five special NIFTY sessions (Muhurat, Saturday and Budget sessions).</li></ul></details>
</main>
'''
src = open('build.py', encoding='utf8').read()
js = src[src.index("js = '''<script>") + len("js = '''<script>"):src.index("</script>")]
js = js.replace('This is the main test.', 'This is the main test.').replace('Trend dominates it, so read it as a description of divergence.', 'Trends dominate this, so it mainly shows whether the markets drifted apart.')
ex = open('extra.js', encoding='utf8').read()
ex = ex.replace("['VIX '+v[4].toFixed(1)+'–'+v[5].toFixed(1),", "[['Calm','Middle','Nervous'][E.vix.indexOf(v)]+' ('+v[4].toFixed(1)+' to '+v[5].toFixed(1)+')',")
ex = ex.replace("'NIFTY leads by 3','By 2','By 1','Same date','Prior US session'", "'NIFTY leads by 3','By 2','By 1','Same date','Previous US session'")
# value labels on the dot charts
ex = ex.replace('r="5" fill="var(--s1)"/><text x="${x}" y="${o.h-8}"', 'r="5" fill="var(--s1)"/>${rows.length<5||o.w>560?`<text x="${x+8}" y="${o.Y(q[1])+4}">${f(q[1])}</text>`:""}<text x="${x}" y="${o.h-8}"')
ex = ex.replace('extra();let z2', '''function waf(id,a){$(id).innerHTML=a.map(([t,n,s])=>`<div><b>${t}</b><div class="g" role="img" aria-label="${n} of 100">${Array.from({length:100},(_,i)=>`<i${i<n?' style="background:var(--pos)"':''}></i>`).join('')}</div><span>${s}</span></div>`).join('')}
waf('c-waf',[['After a big US fall',33,'33 of 100 times NIFTY rose. S&amp;P down more than 1.5%, 45 days.'],['After a quiet US day',53,'53 of 100. S&amp;P within 0.5%, 482 days.'],['After a big US rise',74,'74 of 100. S&amp;P up more than 1.5%, 42 days.']]);
waf('c-r2',[['2023',16,'16%'],['2024',3,'3%'],['2025',7,'7%'],['2026',6,'6%']]);
function simple(){
const w=Math.max(300,$('c-scale').clientWidth),l=14,X=v=>l+(w-2*l)*(v+1)/2,pts=[['2023',.40,-1],['2026',.25,1],['Jul to Oct 2026',.10,-1]];
$('c-scale').innerHTML=`<svg viewBox="0 0 ${w} 150" height="150" role="img" aria-label="Correlation scale"><rect x="${l}" y="70" width="${(w-2*l)/2}" height="8" fill="var(--neg)" fill-opacity=".45"/><rect x="${X(0)}" y="70" width="${(w-2*l)/2}" height="8" fill="var(--pos)" fill-opacity=".45"/>${[-1,0,1].map(v=>`<line x1="${X(v)}" x2="${X(v)}" y1="64" y2="84" stroke="var(--zero)"/><text x="${X(v)}" y="130" text-anchor="${v<0?'start':v?'end':'middle'}">${v<0?'−1':v?'+1':'0'}</text><text x="${X(v)}" y="147" text-anchor="${v<0?'start':v?'end':'middle'}">${v<0?'Opposite':v?'In step':'No link'}</text>`).join('')}${pts.map(([n,v,s])=>`<circle cx="${X(v)}" cy="74" r="7" fill="var(--fg)" stroke="var(--bg)" stroke-width="2"/><text class="pt" x="${X(v)}" y="${s<0?(n.length>5?32:50):104}" text-anchor="middle">${n}: ${f(v)}</text>${n.length>5?`<line x1="${X(v)}" x2="${X(v)}" y1="38" y2="66" stroke="var(--zero)"/>`:''}`).join('')}</svg>`;
const b=[['Taiwan',.41,.45],['Australia',.33,.49],['Japan',.33,.46],['Korea',.28,.33],['NIFTY',.10,.02],['Hong Kong',.04,.15]],pw=Math.max(300,$('c-pb').clientWidth),L=92,S=(pw-L-50)/.6;
$('c-pb').innerHTML=`<svg viewBox="0 0 ${pw} 282" height="282" role="img" aria-label="Correlation with the S&amp;P, July to October and to November">${b.map(([n,v,x],i)=>`<text ${n=='NIFTY'?'class="pt"':''} x="${L-8}" y="${i*47+28}" text-anchor="end">${n}</text><rect x="${L}" y="${i*47+6}" width="${Math.max(2,v*S)}" height="16" fill="var(--s1)"/><text class="pt" x="${L+v*S+8}" y="${i*47+19}">${f(v)}</text><rect x="${L}" y="${i*47+24}" width="${Math.max(2,x*S)}" height="16" fill="var(--r3)"/><text x="${L+x*S+8}" y="${i*47+37}">${f(x)}</text>`).join('')}</svg>`;
frame('c-wk',230,-.2,.8,[0,.2,.4,.6,.8],v=>v?v.toFixed(1):'0',o=>{const R=[[2015,.47],[2016,.60],[2017,.36],[2018,.35],[2019,.19],[2020,.72],[2021,.31],[2022,.67],[2023,.40],[2024,.32],[2025,.28],[2026,-.03]],st=(o.w-o.l-o.r)/12;return R.map(([y,v],i)=>{const x=o.l+st*(i+.5),bw=Math.min(34,st*.62),Y=o.Y(v);return `<rect x="${x-bw/2}" width="${bw}" y="${Math.min(Y,o.Y(0))}" height="${Math.max(2,Math.abs(Y-o.Y(0)))}" fill="var(${v<0?'--neg':'--s1'})"/><text class="pt" x="${x}" y="${v<0?o.Y(0)+22:Y-5}" text-anchor="middle">${y==2026||o.w>560?f(v):''}</text>${y==2026?`<circle cx="${x}" cy="${o.Y(.38)}" r="6" fill="var(--s3)"/><text class="pt" x="${x}" y="${o.Y(.38)-10}" text-anchor="middle">0.38</text>`:''}<text x="${x}" y="${o.h-6}" text-anchor="middle">${o.w<560?"'"+String(y).slice(2):y}</text>`}).join('')},'Weekly correlation by year')}
simple();document.querySelectorAll('details').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)extra()}));
extra();let z2''').replace('setTimeout(extra,150)', 'setTimeout(()=>{extra();simple()},150)')
out = head + body + '<script>' + js.replace('/*DATA*/', json.dumps(D, separators=(',', ':'))) + '</script>\n<script>' + ex.replace('/*DEEP*/', open('deep.json').read()) + '</script>\n'
open('us_nifty.html', 'w', encoding='utf8').write(out)
import re
vis = re.sub('<script>.*?</script>|<style>.*?</style>', '', out, flags=re.S)
print('dashes in text', len(re.findall('[—–]', vis)), 'js', len(re.findall('[—–]', out)) - len(re.findall('[—–]', vis)))
