import json, re
D = json.load(open('macro.json'))
old = open('macro_tmpl.html', encoding='utf8').read()
head = '''<title>NIFTY Macro Regimes</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap">
<style>
''' + open('simple.css', encoding='utf8').read() + '</style>\n'
body = '''<main>
<h1>Can yields, oil and the dollar explain when NIFTY follows the US?</h1>
<p class="lead">Very little, as far as we can measure. The gap between Indian and US bond yields has more than halved since 2015 and NIFTY's link to the S&amp;P 500 barely changed. We expect a weak positive link next month, close to its long-run average.</p>
<p class="mut">"Link" means the correlation between NIFTY's daily return and the S&amp;P 500 session that finished before it. +1 is in step, 0 is no link and −1 is opposite. Data runs from February 2015 to 24 November 2026.</p>

<h2>What we expect next month</h2>
<p>Our forecast is 0.28, with an 80% range of −0.09 to 0.60. Out of 100 months like this, we would expect the link to be negative in about 18 (red).</p>
<div class="waf" id="c-odds"></div>
<p>A negative link lasting a full year would be a first: no 12-month window since 2015 has been below zero.</p>
<details><summary>Ranges for 3, 6 and 12 months</summary><div id="c-fan"></div><p class="mut">The next-month range uses the errors of past forecasts. The longer ranges are the 10th to 90th percentiles of overlapping history since 2015, so they describe the past and are not independent forecasts.</p></details>

<h2>The yield gap narrowed and the link did not follow</h2>
<p>The top line is India's 10-year bond yield minus the US one. It fell from about 5.6 points in 2015 to 2.4 in 2026. The bottom line is NIFTY's link to the S&amp;P over six months, which kept swinging around 0.3.</p>
<div class="lg" id="lg"></div><div id="c-two"></div>
<p>The coloured strip shows the macro regime each month, explained below. Hover or tap to read a month.</p>
<h3>50 checks, none significant</h3>
<p>We compared ten yield measures with five NIFTY outcomes, in the same quarter and the next. Each square is one check and would be red if it passed the usual 5% test. None did.</p>
<div id="c-50"></div>
<p class="mut">With 47 quarters of data, an effect below roughly 0.3 would often be missed, so this does not prove there is none.</p>
<details><summary>See every check</summary>
<p class="mut">Correlation across 46 or 47 quarters. Blue is positive and red is negative. An asterisk marks p below 0.10; chance alone would produce about five of those in 50, and we found three.</p><div class="tw" id="t-q"></div>
<p>Two came closest. NIFTY lagged in quarters when the US 3-month to 10-year curve steepened (−0.28, p = 0.06), and beat the S&amp;P in the quarter after US 10-year yields rose (+0.27, p = 0.06). Neither survives the number of tests.</p>
<h3>India-US yield gap against NIFTY's relative return</h3><p class="mut">Each dot is a quarter: change in the gap (points, across) and NIFTY minus S&amp;P return (%, up). A real effect would form a slope. Correlation −0.16, p = 0.28.</p><div id="c-sc"></div></details>
<details><summary>All five panels: performance, link, yield gap, US curve, US 10-year</summary><p>NIFTY's performance relative to the S&amp;P peaked in September 2022 and has fallen on balance since, while the yield gap kept narrowing. That overlap is one slow trend and cannot count as repeated evidence.</p><div id="c-main"></div></details>

<h2>One change in 2026: NIFTY reacts to US yields</h2>
<p>NIFTY tended to fall after US 10-year yields rose. The correlation is −0.25, the most negative in 12 years. Bars below zero mean NIFTY fell when yields rose.</p>
<div id="c-yd"></div>
<p>The S&amp;P showed the same sign in 2026 (−0.18), which points to a global rates effect. It is one year out of 12, too few to call a pattern.</p>

<h2>Where we are now: Neutral, one trigger from Squeeze</h2>
<p>A Squeeze month needs two of four pressures to pass their limits over three months. In November only the dollar has. September and October were Squeeze months, with US yields and oil over the limit in September and oil and the dollar in October.</p>
<div id="c-trig"></div>
<p class="mut">Each bar is the three-month change as a share of its limit. The limits are US 10-year +0.25 points, dollar index +2%, Brent oil +15% and USDINR +2%. USDINR falling means the rupee strengthened.</p>
<h3>The four regimes</h3>
<div class="tw"><table><thead><tr><th>Regime</th><th class="l">Rule</th><th class="l">What it means</th></tr></thead><tbody>
<tr><td>Stress</td><td class="w">VIX averages 25 or more</td><td class="w">Global fear, most things fall together</td></tr>
<tr><td>Squeeze</td><td class="w">Two or more pressures above their limit</td><td class="w">Costly dollars and oil. Hard on an oil importer that relies on foreign money</td></tr>
<tr><td>Tailwind</td><td class="w">Two or more of the same moves in reverse</td><td class="w">Cheaper dollars and oil</td></tr>
<tr><td>Neutral</td><td class="w">Anything else</td><td class="w">No dominant outside force</td></tr></tbody></table></div>
<h3>How strong the link was in each</h3><div id="c-reg"></div>
<p>The link is strongest in Stress and weakest in Squeeze, where NIFTY also lagged the S&amp;P by 0.5 points a month. The order makes economic sense, but the ranges (vertical lines) overlap and that lag is within one standard error. Using the previous month's regime, the figures bunch closer together: 0.35, 0.25, 0.29 and 0.25.</p>
<details><summary>Returns by regime</summary><div class="tw"><table><thead><tr><th>Regime</th><th>Months</th><th>Link</th><th>NIFTY per month</th><th>S&amp;P per month</th><th>NIFTY minus S&amp;P</th><th>± 1 SE</th></tr></thead><tbody id="t-reg"></tbody></table></div></details>

<h2>Where the regime may go next</h2>
<p>From a Neutral month, history went on to Neutral 70% of the time, Squeeze 18%, Tailwind 9% and Stress 3%.</p>
<div id="c-next"></div>
<details><summary>Full transition table</summary><div class="tw"><table><thead><tr><th>From</th><th>Neutral</th><th>Squeeze</th><th>Stress</th><th>Tailwind</th></tr></thead><tbody id="t-tr"></tbody></table></div><p class="mut">Month-to-month frequencies. Stress has 15 months in total and seven are in 2020, so its row is thin.</p></details>
<h3>What to watch</h3>
<div class="tw"><table><thead><tr><th>Scenario</th><th class="l">What we would see</th><th class="l">What the link did in the month after</th></tr></thead><tbody>
<tr><td>Neutral holds (base)</td><td class="w">Fewer than two pressures over the limit</td><td class="w">Mostly −0.05 to 0.56, middle 0.26</td></tr>
<tr><td>Squeeze returns</td><td class="w">The dollar stays strong and US yields, Brent or USDINR also passes its limit</td><td class="w">Middle 0.29. NIFTY lagged by 0.5 points in Squeeze months themselves, not significant</td></tr>
<tr><td>Global stress</td><td class="w">VIX averages 25 or more. November averaged 23.4</td><td class="w">Highest, middle 0.35. Diversification weakens</td></tr>
<tr><td>Tailwind</td><td class="w">Two or more of dollar, oil, US yields and USDINR fall past their limits</td><td class="w">Middle 0.19, from 18 months</td></tr></tbody></table></div>
<p class="mut">The evidence does not support scenario odds beyond the transition table, or a NIFTY price target.</p>

<h2>The simplest forecast was the best</h2>
<p>We tested five ways to forecast next month's link on 94 months from January 2019 to October 2026, using only data available at the time. Longer bars mean bigger errors than the long-run average.</p>
<div id="c-fc"></div>
<p>HAR combines 1, 3 and 12-month averages. It and the regime model did worse because monthly correlations are so noisy. This tests HAR on correlation and says nothing about HAR forecasts of volatility.</p>
<details><summary>Forecast errors</summary><div class="tw"><table><thead><tr><th>Model</th><th>Error (RMSE, Fisher z)</th><th>Squared error against average</th></tr></thead><tbody id="t-fc"></tbody></table></div></details>

<h2>Background and where to dig next</h2>
<p>Brent closed March 2026 at $118. USDINR moved from about 87 on average in 2025 to 94 in 2026, and the US 10-year ended September at 5.3%. Press reports tie NIFTY's 2026 lag to <a href="https://www.business-standard.com/markets/news/global-funds-dump-indian-equities-at-record-pace-on-oil-shock-growth-fears-126041100158_1.html">record foreign selling during the oil shock</a>, and say the <a href="https://www.5paisa.com/blog/india-us-10-year-bond-yield-spread-widens-to-251-basis-points">India-US gap widened to 251 bp in October</a>. We have not verified those reports or tested flows.</p>
<ul><li>Do foreign flows (NSDL) and mutual-fund SIPs explain why domestic money blunted the US link?</li>
<li>Does sector mix matter? NIFTY has little AI hardware, while Taiwan and Korea stayed linked.</li>
<li>Does the gap in earnings growth or valuation explain relative returns better than yields?</li>
<li>Do daily Indian yields show effects around RBI and Fed meetings? Ours are monthly averages.</li>
<li>On the risk dashboard, the regime can be shown as a label beside volatility forecasts. It failed its forecasting test, so it should not change position size.</li></ul>
<details><summary>Method and limits</summary><ul>
<li>Sources are Yahoo Finance, US Treasury and FRED (OECD Indian yields, monthly averages to October 2026).</li>
<li>Regime limits were set before looking at outcomes. Triggers are three-month changes at month-end. Some 2026 outcomes had been seen in earlier work, but the limits were not tuned to them.</li>
<li>Ranges in the regime chart are 95% intervals from resampling months. There are 142 months and 47 quarters.</li>
<li>Other reasonable regime rules would classify some months differently.</li>
<li>This is research for discussion. No costs or trades are modelled and it is not investment advice.</li></ul></details>
</main>
'''
js = old[old.index('<script>') + 8:old.index('</script>')]
js = re.sub('[–—]', lambda m: '-' if m.group() == '–' else '0%', js)
js = js.replace('NIFTY − S&amp;P', 'NIFTY minus S&amp;P').replace('function main(){\nconst el=$(\'c-main\')', "function main(id,PN){\nconst el=$(id)")
js = js.replace('const PN=[', 'const PANELS=[').replace('function all(){main();', '''
function all(){main('c-main',PANELS);main('c-two',[PANELS[2],PANELS[1]]);''')
js = js.replace("a[0]=='mean'?'0%':Math.abs(a[2]).toFixed(1)+'% worse (squared error)'", "a[0]=='mean'?'Baseline':Math.abs(a[2]).toFixed(1)+'% worse'")
js = js.replace('6m correlation', '6-month link')
js = js.replace('<text x="${x}" y="${o.h-8}" text-anchor="middle">${a[0]}</text></g>`}).join(\'\'),\'Correlation by regime\'', '<text x="${x+11}" y="${o.Y(a[2])+4}">${f(a[2])}</text><text x="${x}" y="${o.h-8}" text-anchor="middle">${a[0]}</text></g>`}).join(\'\'),\'Correlation by regime\'')
js = js.replace('all();let z;', r'''
$('c-odds').innerHTML=`<div><div class="g" style="max-width:260px;grid-template-columns:repeat(20,1fr)" role="img" aria-label="18 of 100 negative">${Array.from({length:100},(_,i)=>`<i style="background:var(${i<18?'--neg':'--r3'})"></i>`).join('')}</div><span>Red: negative link. Grey: positive link.</span></div>`;
$('c-50').innerHTML=`<div style="display:grid;grid-template-columns:repeat(25,1fr);gap:4px;max-width:520px;margin:8px 0" role="img" aria-label="0 of 50 significant">${Array.from({length:50},()=>'<i style="aspect-ratio:1;background:var(--r3)"></i>').join('')}</div><p><b>0 of 50</b></p>`;
function hb(id,rows,lo,hi,fmt,mark,L=130){const el=$(id),w=Math.max(300,el.clientWidth),X=v=>L+(w-L-70)*(v-lo)/(hi-lo),H=rows.length*36+(mark!=null?26:6),top=mark!=null?24:0;
el.innerHTML=`<svg viewBox="0 0 ${w} ${H}" height="${H}" role="img">${mark!=null?`<line x1="${X(mark)}" x2="${X(mark)}" y1="18" y2="${H}" stroke="var(--fg)" stroke-dasharray="4 3"/><text class="pt" x="${X(mark)}" y="13" text-anchor="middle">Limit</text>`:''}<line x1="${X(0)}" x2="${X(0)}" y1="${top}" y2="${H}" stroke="var(--zero)"/>${rows.map(([n,v,c,t],i)=>`<text x="${L-8}" y="${top+i*36+22}" text-anchor="end" ${lo<0?'style="paint-order:stroke"':''}>${n}</text><rect x="${Math.min(X(0),X(v))}" y="${top+i*36+7}" width="${Math.max(2,Math.abs(X(v)-X(0)))}" height="22" fill="var(${c})"/><text class="pt" x="${v<0?X(0)+6:X(v)+6}" y="${top+i*36+23}">${t||fmt(v)}</text>`).join('')}</svg>`}
function extra(){const u=D.u3[D.u3.length-1];
hb('c-trig',[['US 10-year +0.16 pts',u[0],'--r3',' '],['Dollar index +4.4%',u[1],'--r2',' '],['Brent oil +1.0%',u[2],'--r3',' '],['USDINR −2.6%',u[3],'--r4',' ']],-1.4,2.4,f,1,155);
hb('c-next',[['Neutral',70,'--r3','70%'],['Squeeze',18,'--r2','18%'],['Tailwind',9,'--r4','9%'],['Stress',3,'--r1','3%']],0,75,f,null,80);
hb('c-fc',D.fc.map(a=>[ML[a[0]].replace(' (1, 3, 12 months)',''),Math.abs(a[2]),a[0]=='mean'?'--r4':'--r3',a[0]=='mean'?'Best':Math.abs(a[2]).toFixed(1)+'% worse']),0,90,f,null,130)}
extra();document.querySelectorAll('details').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)all()}));
addEventListener('resize',()=>{clearTimeout(window.z3);window.z3=setTimeout(extra,160)});
all();let z;''')
out = head + body + '<script>' + js.replace('/*DATA*/', json.dumps(D, separators=(',', ':')).replace('NaN', 'null')) + '</script>\n'
open('macro_regimes.html', 'w', encoding='utf8').write(out)
print('dashes', len(re.findall('[—–]', out)), D['u3'][-1], [round(x, 2) for x in D['u3'][-2]])
