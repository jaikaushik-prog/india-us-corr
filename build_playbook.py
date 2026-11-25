import json, re
A = {k: json.load(open(f'{k}.json')) for k in ('s2', 's3b', 's4b')}
f = lambda v, d=2: ('−' if round(v, d) < 0 else '') + f'{abs(v):.{d}f}'
T = A['s3b']['tab']; NM = A['s3b']['names']
sec = ''.join(f"<tr><td>{NM[k]}</td><td>{f(v[1])}% ({f(v[2])} to {f(v[3])})</td><td>{f(v[4])}%</td><td>{v[6]}%</td><td>{f(v[5])}%</td></tr>" for k, v in sorted(T.items(), key=lambda x: -x[1][1]))
ft = ''.join(f"<tr><td>{t[0]}</td><td>{t[1]}</td><td>{t[2]}</td><td>{f(t[3])}</td><td>{t[4]:.3f}</td><td>{f(t[5])} to {f(t[6])}</td></tr>" for t in A['s2']['t'])
by = ''.join(f"<tr><td>{y}</td><td>{f(v['cr'],0)}</td><td>{f(v['nr'],1)}</td><td>{f(v['rel'],1)}</td></tr>" for y, v in A['s2']['by'].items())
R = {(r[0], r[1], r[2], r[3]): r[4:] for r in A['s4b']['rows']}
F06, F10, DR = 'Indian fund, 0.6% a year', 'Indian fund, 1.0% a year', 'Direct US ETF, 0.4% a year + 1% entry'
at = ''
for nm, sc in (('What happened, 2015 to 2024', 'actual'), ('US only matched NIFTY', 'equal'), ('US 3% a year behind NIFTY', 'minus3')):
    at += f'<tr><td>{nm}</td>' + ''.join(f"<td>{R[(sc, F06, 'band', w)][0]:.1f}%</td>" for w in (0, 10, 20, 30, 40)) + '</tr>'
rt = ''.join(f"<tr><td>{n}</td>" + ''.join(f"<td>{R[(sc, r, 'band', 20)][0]:.2f}%</td>" for sc in ('actual', 'equal', 'minus3')) + '</tr>' for n, r in ((F06, F06), (F10, F10), ('Direct US ETF, 0.4% a year and 1% entry', DR)))
rk = '<tr><td>Yearly volatility</td>' + ''.join(f"<td>{R[('actual', F06, 'band', w)][1]}%</td>" for w in (0, 10, 20, 30, 40)) + '</tr><tr><td>Worst fall</td>' + ''.join(f"<td>{f(R[('actual', F06, 'band', w)][2],1)}%</td>" for w in (0, 10, 20, 30, 40)) + '</tr>'
html = '''<title>NIFTY and US Playbook</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap">
<style>
''' + open('simple.css', encoding='utf8').read() + '''
.box{background:var(--soft);padding:16px;margin:14px 0}.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px 20px}
label{display:block;font-size:.875rem;color:var(--mut)}input[type=number],select{font:500 1rem var(--body);color:var(--fg);background:var(--bg);border:1px solid var(--line);border-radius:4px;padding:8px;width:100%;box-sizing:border-box}
input[type=range]{width:100%;accent-color:var(--s1)}.out{font:600 1.25rem/1.4 var(--disp);margin:14px 0 4px}input:focus-visible,select:focus-visible{outline:2px solid var(--s1);outline-offset:1px}
</style>
<main>
<h1>NIFTY and US playbook</h1>
<p class="lead">Hold a fixed US share and rebalance it rarely. Know which Indian sectors move most with the US. Use foreign flows to explain a month after it ends, because they did not predict the next one.</p>

<h2>Set your US share</h2>
<p>A 20% share with a 5-point band means doing nothing until the share leaves 15% to 25%. In 2015 to 2024 that needed one rebalance in ten years.</p>
<div class="box"><div class="row"><label for="cap">Portfolio, rupees<input id="cap" type="number" min="0" step="50000" value="1000000"></label><label for="shr">US share: <b id="shrv"></b><input id="shr" type="range" min="0" max="40" step="5" value="20"></label><label for="cur">US holding now, rupees<input id="cur" type="number" min="0" step="10000" value="0"></label></div><p class="out" id="a1"></p><p class="mut" id="a2" style="margin:0"></p></div>
<p class="mut">The 10 lakh rupees is an example. Change it to your own.</p>
<h3>What it cost and what it saved</h3>
<div class="lg"><span><i style="background:var(--s1)"></i>Volatility a year</span><span><i style="background:var(--r3)"></i>Worst fall</span></div><div id="c-risk"></div>
<p>These figures are after a 0.6% yearly fund fee, trading costs and 13% tax on gains (12.5% plus cess). Volatility fell from 15.8% to 14.4% at 20%, and the worst fall from 34.4% to 31.4%. Both halves of the decade show the same direction.</p>
<h3>Return after tax and fees, yearly</h3>
<div class="tw"><table><thead><tr><th>US share</th><th>0%</th><th>10%</th><th>20%</th><th>30%</th><th>40%</th></tr></thead><tbody>''' + at + rk + '''</tbody></table></div>
<p>If the US had only matched NIFTY, 20% would have cost about 0.1% a year, which passes our 0.5% limit. If it had trailed by 3% a year, the cost would have been 0.6% a year. That is the price of the lower risk if the strong US decade does not repeat.</p>
<details><summary>Ways to hold it, and what differs</summary>
<div class="tw"><table><thead><tr><th>20% US, yearly return</th><th>Actual</th><th>US matches</th><th>US 3% behind</th></tr></thead><tbody>''' + rt + '''</tbody></table></div>
<p>The route changed the result by about 0.1% a year, far less than how US stocks do. Fees here are our assumptions, so replace them with a quote.</p>
<ul><li>An Indian fund that holds the S&amp;P 500 is simplest. The <a href="https://vestedfinance.com/in/globed/accessing-global-markets/global-investing-through-domestic-funds-and-etfs/sebi-limits-on-overseas-investment-by-mutual-funds/">SEBI overseas cap</a> has closed several funds to new money during 2026, so check which are open. Listed ETFs can trade above their asset value when the cap binds. Compare the price with the NAV before buying.</li>
<li>Direct US ETFs through LRS involve currency and remittance charges. On a 2 lakh rupee purchase a 1,000 to 2,000 rupee fee is 0.5% to 1.0%. Secondary sources put <a href="https://agrawalkhandelwal.com/blog/tcs-foreign-remittance-lrs-rates-fy2026-27">TCS at 20% above 10 lakh rupees a year</a>, adjustable against tax. You must also report the holding in Schedule FA.</li>
<li>Foreign equity held over 24 months is reported as taxed at <a href="https://www.winvesta.in/blog/investors/capital-gains-tax-on-us-stocks-short-term-vs-long-term-for-indians">12.5% without indexation</a>. Sources disagree on listed ETFs and fund of funds, and our test used 13% for everything. Confirm with a chartered accountant.</li></ul></details>
<details><summary>Rules to follow</summary><ul><li>Pick a share from 10% to 30% and write it down. Going to 40% lowered risk further in the data, but more of the result then depends on one foreign market.</li><li>Check once a month. Rebalance only if the share has moved 5 points from target.</li><li>Use new savings to rebalance first, since selling triggers tax.</li><li>Expect it to help less in a crash. In early 2020 NIFTY fell 28% and the S&amp;P fell 21% in rupees.</li></ul></details>

<h2>How hard would a US move hit your sectors?</h2>
<p>Set your sector weights and a US move. The answer is the typical effect on the next Indian session, using 2021 to 2024.</p>
<div class="box"><div class="row" id="secs"></div><label for="mv" style="margin-top:14px">S&amp;P 500 move: <b id="mvv"></b><input id="mv" type="range" min="-5" max="5" step="0.5" value="-2"></label><p class="out" id="b1"></p><p class="mut" id="b2" style="margin:0"></p></div>
<p class="mut">The weights shown are placeholders and are rescaled to 100%.</p>
<h3>Sector response to a 1% S&amp;P move</h3><div id="c-sec"></div>
<p>IT, realty and metals react most. FMCG and pharma react least. The chart uses 2021 to 2024. To test whether such an order lasts, we ranked sectors on 2015 to 2020 and checked 64 sessions in 2021 to 2024 that followed S&amp;P falls of 1.5% or more. Sectors ranked higher did fall more (rank correlation 0.65, p = 0.02).</p>
<p>The map stops at 2024. In 2026 IT's link to the US fell to 0.11 (0.16 without November) and metals rose to the top, so recheck it every year.</p>
<details><summary>Sector table</summary><div class="tw"><table><thead><tr><th>Sector</th><th>Per 1% S&amp;P (90% range)</th><th>After S&amp;P falls of 1.5%+</th><th>Sector fell</th><th>After S&amp;P rises of 1.5%+</th></tr></thead><tbody>''' + sec + '''</tbody></table></div></details>

<h2>Foreign flows account for about half of the 2026 gap</h2>
<p>From January to 24 November, S&amp;P moves alone would have put NIFTY up about 9.9%. It fell 3.0%. Adding foreign buying and selling brings the estimate to 3.1%, which closes about half of the gap.</p>
<div id="c-attr"></div>
<p class="mut">Monthly log returns summed. Estimates use only 2021 to 2025 patterns.</p>
<p>The result does not rest on November. From January to October the S&amp;P alone implied 11.0%, S&amp;P and flows implied −3.0%, and NIFTY fell 12.7%, so flows close a little over half.</p>
<p>Foreign investors sold a net 2.95 lakh crore rupees from January to October 2026, including 1.18 lakh crore in March, the largest month in the file. In November, still incomplete, they bought 1.22 lakh crore and NIFTY rose 9.5%, while the S&amp;P fell 5.1%.</p>
<h3>Foreign flows and NIFTY by month</h3><div class="lg"><span><i style="background:var(--s1)"></i>Net buying</span><span><i style="background:var(--neg)"></i>Net selling</span></div><div id="c-flow"></div><p class="mut">Thousand crore rupees, net foreign equity, February 2021 to November 2026.</p>
<h3>They move together, and do not lead</h3><div id="c-lead"></div>
<p>Flows and NIFTY in the same month correlate at 0.56 over 69 months. Flows against NIFTY minus S&amp;P in the next month correlate at −0.06, which is nothing. Our rule needed a lead effect in 2021 to 2024 with p below 0.05; we found −0.02 (p = 0.87). Selling months were even followed by slightly better NIFTY returns, but not reliably.</p>
<p>Same-month figures cannot show cause. Foreigners may push prices, or may sell when prices fall. In 2022 they sold 1.21 lakh crore and NIFTY still beat the S&amp;P by 26 points. Flows also do not explain how closely NIFTY follows the US: their correlation with the monthly link is 0.00.</p>
<h3>Domestic funds buy what foreigners sell</h3><p>Over 60 sessions from 24 August to 23 November 2026, daily foreign and domestic flows correlate at −0.91. Foreign flows went with NIFTY the same day (0.47). That is too short to test domestic flows properly.</p>
<details><summary>All flow tests</summary><div class="tw"><table><thead><tr><th>Test</th><th>Period</th><th>Months</th><th>Correlation</th><th>p</th><th>95% range</th></tr></thead><tbody>''' + ft + '''</tbody></table></div><p class="mut">Flows are divided by the NIFTY level. Around 24 rows were run with no adjustment for that.</p><h3>By year</h3><div class="tw"><table><thead><tr><th>Year</th><th>Foreign net, crore</th><th>NIFTY, log %</th><th>NIFTY minus S&amp;P</th></tr></thead><tbody>''' + by + '''</tbody></table></div><p class="mut">2021 starts in February. Adding flows to the S&amp;P lifted the share of NIFTY's monthly moves explained from 20% to 44% in 2021 to 2025.</p></details>

<h2>Monthly checklist</h2>
<ul><li>Check your US share against its band.</li><li>Look at NSDL foreign flows to understand the month that ended, and make no forecast from them.</li><li>Watch India VIX for expected volatility.</li><li>Re-run the sector map once a year.</li></ul>
<details><summary>Method and limits</summary><ul>
<li>The flow history is <a href="https://github.com/FinBizNet-AI-Tech-Pvt-Ltd/india-market-data">FinBizNet's monthly file of NSDL figures</a>. NSDL refused direct downloads. The ten 2026 months match a second repository to within half a crore. Earlier years come from one copy and we have not matched them to NSDL.</li>
<li>Daily flows come from <a href="https://github.com/nalinisubir-oss/fii-dii-data">a repository of NSE figures</a> covering 60 sessions.</li>
<li>Taxes are simplified: 13% on every gain at sale and at the end, with no exemptions, surcharge, dividend tax or losses. Remittance limits are ignored.</li>
<li>The allocation test covers 2015 to 2024, one decade with a strong US market. Flow results use NIFTY returns through November 2026. A separate volatility project reserves 2025 to October 2026, so those months should not count as unseen there.</li>
<li>The sector answer ignores news, opening gaps and stock selection. Its range comes from 2021 to 2024 and real moves can be larger.</li>
<li>This is research for discussion. It is not investment or tax advice.</li></ul></details>
</main>
<script>
const A=/*DATA*/,$=i=>document.getElementById(i),f=(v,d=2)=>(v<0&&+v.toFixed(d)!==0?'−':'')+Math.abs(v).toFixed(d),W=i=>Math.max(300,$(i).clientWidth);
const B=A.s3b.K,T=A.s3b.tab,NM=A.s3b.names,DEF={BANK:30,IT:15,ENERGY:12,FMCG:10,AUTO:8,PHARMA:7,METAL:5,INFRA:5,FIN:5,REALTY:2,PSUBANK:1};
const rs=v=>'₹'+Math.round(v).toLocaleString('en-IN');
$('secs').innerHTML=B.map(k=>`<label for="w-${k}">${NM[k]}, %<input id="w-${k}" type="number" min="0" max="100" value="${DEF[k]||0}"></label>`).join('');
function sec(){const w=B.map(k=>Math.max(0,+$('w-'+k).value||0)),t=w.reduce((a,b)=>a+b,0);$('mvv').textContent=(+$('mv').value>0?'+':'')+f(+$('mv').value,1)+'%';if(!t){$('b1').textContent='Enter at least one sector weight.';$('b2').textContent='';return}
const x=w.map(v=>v/t),b=x.reduce((a,v,i)=>a+v*T[B[i]][1],0),mv=+$('mv').value,e=b*mv;let q=0;x.forEach((u,i)=>x.forEach((v,j)=>q+=u*v*A.s3b.cov[i][j]));const sd=Math.sqrt(q);
$('b1').textContent=`Expect about ${e>0?'+':''}${f(e)}% on the next session.`;$('b2').textContent=`Two sessions in three should land between ${f(e-sd)}% and ${f(e+sd)}%. Your portfolio moves ${f(b)}% per 1% in the S&P, and most of the range is local news.`}
function alloc(){const c=Math.max(0,+$('cap').value||0),s=+$('shr').value/100,u=Math.max(0,+$('cur').value||0);$('shrv').textContent=(s*100)+'%';const tgt=c*s,lo=Math.max(0,s-.05),hi=s+.05,now=c?u/c:0;
let t;if(!c)t='Enter a portfolio value.';else if(u>c)t='US holding is larger than the portfolio.';else if(s===0)t=u?'Target is 0%, so sell the US holding or raise the share.':'Nothing to buy at 0%.';else if(now<lo)t=`Buy about ${rs(tgt-u)} of US stocks to reach ${rs(tgt)}.`;else if(now>hi)t=`Sell about ${rs(u-tgt)} to return to ${rs(tgt)}, or add new money to the Indian side first.`;else t='Inside your band. Do nothing.';$('a1').textContent=t;
$('a2').textContent=c&&s&&u<=c?`Band is ${Math.round(lo*100)}% to ${Math.round(hi*100)}%, or ${rs(lo*c)} to ${rs(hi*c)}. You hold ${Math.round(now*1000)/10}%. ${tgt-u>1e6?'This is over 10 lakh rupees, where TCS on direct LRS transfers is reported to start.':'This is under 10 lakh rupees, where TCS on direct LRS transfers is reported not to apply.'}`:''}
['cap','shr','cur'].forEach(i=>$(i).addEventListener('input',alloc));$('mv').addEventListener('input',sec);B.forEach(k=>$('w-'+k).addEventListener('input',sec));alloc();sec();
const RW=A.s4b.rows.filter(r=>r[0]=='actual'&&r[1].includes('0.6%')&&r[2]=='band');
function draw(){
{const w=W('c-risk'),L=56,S=(w-L-60)/36;$('c-risk').innerHTML=`<svg viewBox="0 0 ${w} 260" height="260" role="img" aria-label="Volatility and worst fall by US share">${RW.map((r,i)=>`<text x="${L-8}" y="${i*52+26}" text-anchor="end">${r[3]}%</text><rect x="${L}" y="${i*52+4}" width="${r[5]*S}" height="18" fill="var(--s1)"/><text class="pt" x="${L+r[5]*S+6}" y="${i*52+18}">${r[5]}%</text><rect x="${L}" y="${i*52+24}" width="${-r[6]*S}" height="18" fill="var(--r3)"/><text class="pt" x="${L-r[6]*S+6}" y="${i*52+38}">${f(r[6],1)}%</text>`).join('')}</svg>`}
{const w=W('c-sec'),ks=Object.keys(T).sort((a,b)=>T[b][1]-T[a][1]),L=96,S=(w-L-70)/.58;$('c-sec').innerHTML=`<svg viewBox="0 0 ${w} ${ks.length*30+6}" height="${ks.length*30+6}" role="img" aria-label="Sector response per 1% S&amp;P">${ks.map((k,i)=>`<text ${k=='NIFTY'?'class="pt"':''} x="${L-8}" y="${i*30+20}" text-anchor="end">${NM[k]}</text><rect x="${L}" y="${i*30+6}" width="${T[k][1]*S}" height="20" fill="var(${k=='NIFTY'?'--r3':'--s1'})"/><line x1="${L+T[k][2]*S}" x2="${L+T[k][3]*S}" y1="${i*30+16}" y2="${i*30+16}" stroke="var(--fg)" stroke-width="1.5"/><text class="pt" x="${L+T[k][3]*S+8}" y="${i*30+21}">${f(T[k][1])}%</text>`).join('')}</svg>`}
{const w=W('c-attr'),R=[['S&amp;P only',9.9,'--r3'],['S&amp;P and flows',3.1,'--s1'],['What happened',-3.0,'--neg']],L=110,lo=-4,hi=12,X=v=>L+(w-L-60)*(v-lo)/(hi-lo);$('c-attr').innerHTML=`<svg viewBox="0 0 ${w} 130" height="130" role="img" aria-label="2026 NIFTY estimate and actual"><line x1="${X(0)}" x2="${X(0)}" y1="0" y2="122" stroke="var(--zero)"/>${R.map(([n,v,c],i)=>`<text x="${L-8}" y="${i*40+26}" text-anchor="end">${n}</text><rect x="${Math.min(X(0),X(v))}" y="${i*40+10}" width="${Math.abs(X(v)-X(0))}" height="24" fill="var(${c})"/><text class="pt" x="${v<0?X(0)+8:X(v)+8}" y="${i*40+27}">${v>0?'+':''}${f(v,1)}%</text>`).join('')}</svg>`}
{const w=W('c-flow'),h=230,m=A.s2.m,l=46,r=4,t=10,b=26,mx=130,Y=v=>t+(h-t-b)*(mx-v)/(2*mx),st=(w-l-r)/m.length;let g=[-120,-60,0,60,120].map(v=>`<line x1="${l}" x2="${w-r}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(${v?'--line':'--zero'})"/><text x="${l-5}" y="${Y(v)+4}" text-anchor="end">${f(v,0)}</text>`).join('');m.forEach((q,i)=>{const v=q[1]/1000;g+=`<g><title>${q[0]}: ${f(v,1)} thousand crore, NIFTY ${f(q[3],1)}%</title><rect x="${l+st*i+.5}" width="${Math.max(1,st-1)}" y="${Math.min(Y(v),Y(0))}" height="${Math.max(1,Math.abs(Y(v)-Y(0)))}" fill="var(${v<0?'--neg':'--s1'})"/></g>`;if(q[0].endsWith('-01'))g+=`<text x="${l+st*i}" y="${h-6}">${q[0].slice(0,4)}</text>`});$('c-flow').innerHTML=`<svg viewBox="0 0 ${w} ${h}" height="${h}" role="img" aria-label="Monthly foreign flows">${g}</svg>`}
{const P=[['Same month, NIFTY',.56],['Same month, vs S&amp;P',.31],['Next month, vs S&amp;P',-.06],['Next month, NIFTY',-.18]],w=W('c-lead'),L=150,X=v=>L+(w-L-60)*(v+.3)/1;$('c-lead').innerHTML=`<svg viewBox="0 0 ${w} 150" height="150" role="img" aria-label="Flow correlations"><line x1="${X(0)}" x2="${X(0)}" y1="0" y2="146" stroke="var(--zero)"/>${P.map(([n,v],i)=>`<text x="${L-8}" y="${i*36+24}" text-anchor="end">${n}</text><rect x="${Math.min(X(0),X(v))}" y="${i*36+8}" width="${Math.abs(X(v)-X(0))}" height="22" fill="var(${i<2?'--s1':'--r3'})"/><text class="pt" x="${v<0?X(0)+8:X(v)+8}" y="${i*36+25}">${f(v)}</text>`).join('')}</svg>`}}
draw();let z;addEventListener('resize',()=>{clearTimeout(z);z=setTimeout(draw,150)});
</script>
'''
html = html.replace('/*DATA*/', json.dumps(A, separators=(',', ':')).replace('NaN', 'null'))
open('playbook.html', 'w', encoding='utf8').write(html); print('dashes', len(re.findall('[—–]', html)))
