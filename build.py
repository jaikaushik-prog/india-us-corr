import json
t = open('tmpl.html', encoding='utf8').read()
D = json.load(open('periods.json'))
f = lambda v: ('−' if round(v, 2) < 0 else '') + f'{abs(v):.2f}'
U = [('SPX', 'S&amp;P 500'), ('COMP', 'Nasdaq'), ('DJI', 'Dow')]
M = [('lag', 'Returns, prior US session'), ('same', 'Returns, same date'), ('level', 'Price levels')]


def table(w):
    h = ''
    for m, name in M:
        h += f'<h3>{name}</h3><div class="tw"><table><thead><tr><th>Index</th>' + ''.join(f'<th>{p}</th>' for p in D[f'd_{m}_{w}']) + '</tr></thead><tbody>'
        for u, un in U:
            h += f'<tr><td>{un}</td>' + ''.join(f'<td>{f(v)}</td>' for v in D[f'{m}_{u}_{w}']) + '</tr>'
        h += '</tbody></table></div>'
    return h


body = '''<main>
<h1>Is NIFTY's correlation with the US turning negative?</h1>
<p>On price levels, yes for this year: all three yearly figures are negative in 2026 after being strongly positive in 2023–25. On daily returns, no: every yearly figure is still positive, and the latest half-year is only around zero.</p>
<p class="mut">S&amp;P 500, Nasdaq Composite and Dow Jones against NIFTY 50. One correlation of daily data per calendar month, half-year and year, with no overlap. January 2023 to 24 November 2026, so November, H2 and full-year 2026 are incomplete. Source: Yahoo Finance.</p>
<h2>Correlation by period</h2>
<div class="ctl" role="group" aria-label="Correlation measure">
<button id="b-lag" data-m="lag">Returns, prior US session</button>
<button id="b-same" data-m="same">Returns, same date</button>
<button id="b-level" data-m="level">Price levels</button></div>
<p class="mut" id="note"></p>
<div class="lg"><span><i style="background:var(--s1)"></i>S&amp;P 500</span><span><i style="background:var(--s2)"></i>Nasdaq Composite</span><span><i style="background:var(--s3)"></i>Dow Jones</span></div>
<div id="charts"></div>
<h2>What the numbers say</h2>
<p><strong>Daily returns stepped down after 2023.</strong> The S&amp;P went 0.40, 0.18, 0.26, 0.25 by year. Half-years swing between about 0 and 0.45 without a clear direction. H2 2026 is close to zero (0.02, 0.00 and 0.09), but H1 2026 was among the highest (0.43, 0.39 and 0.42).</p>
<p><strong>Negative months peaked in 2024, not recently.</strong> Against the S&amp;P there was 1 negative month in 2023, 6 in 2024, 3 in 2025 and 1 so far in 2026. A month has about 20 sessions, so its error is roughly ±0.4 and a single negative month means little.</p>
<p><strong>Price levels moved apart.</strong> The S&amp;P yearly figure went 0.91, 0.79, 0.76, −0.36, and H2 2026 is −0.58. Nasdaq is similar. The Dow is weaker: H2 2026 is 0.09. Most of the yearly change comes from 2026 alone.</p>
<p><strong>The two results are compatible.</strong> Level correlation measures whether the indices trended the same way over the period. Return correlation measures whether they move together day to day. Trending series produce large level correlations of either sign easily, so levels describe divergence and say little about daily behaviour.</p>
<p><strong>Same-date returns in November 2026 are sharply negative</strong> (−0.61, −0.61 and −0.53), on an incomplete month. They were positive in each of the three months before it.</p>
<p><strong>Trend significance.</strong> For returns, no trend is significant at any frequency. For levels, the monthly downtrend is significant for the S&amp;P and Nasdaq at 5% (one-sided p about 0.03 and 0.02) and not for the Dow (0.45). With eight half-years and four years, those two frequencies cannot give a strong test.</p>
<h2>Yearly figures</h2>''' + table('1y') + '<h2>Half-yearly figures</h2>' + table('6m') + '''
<h2>Timing and method</h2>
<ul><li>NIFTY closes at 15:30 IST, before US cash trading opens. The default view pairs each NIFTY return with the US sessions that closed since NIFTY's previous close. The same-date view asks whether the US followed NIFTY.</li>
<li>Each figure is the Pearson correlation of daily log returns (or daily closes, for levels) inside that calendar period. Prices are in local currency.</li>
<li>Trend p-values come from shuffling the order of the periods 4,000 times. They are not adjusted for the number of tests.</li>
<li>2025 depends on the April tariff shock: without 3–15 April the year's S&amp;P return correlation is 0.04.</li>
<li>Yahoo lacks five special NIFTY sessions (Muhurat, Saturday and Budget sessions).</li></ul>
</main>'''
js = '''<script>
const D=/*DATA*/,U=['SPX','COMP','DJI'],NM=['S&amp;P 500','Nasdaq','Dow'],W=[['1m','Monthly'],['6m','Half-yearly'],['1y','Yearly']];
const NOTE={lag:'Does NIFTY follow the US session that finished overnight? This is the main test.',same:'NIFTY trades first on each date, so this shows whether the US followed NIFTY.',level:'Correlation of index values. Trend dominates it, so read it as a description of divergence.'};
const f=v=>(v<0?'−':'')+Math.abs(v).toFixed(2);let M='lag';
function draw(){
document.querySelectorAll('[data-m]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.m===M));
document.getElementById('note').textContent=NOTE[M];
const host=document.getElementById('charts');host.innerHTML='';
const w=Math.max(300,host.clientWidth),h=210,l=40,r=6,t=10,b=26,Y=v=>t+(h-t-b)*(1-v)/2;
W.forEach(([k,lab])=>{
const per=D['d_'+M+'_'+k],n=per.length,s=U.map(u=>D[M+'_'+u+'_'+k]),st=(w-l-r)/n,gap=st>40?2:st>10?.6:0,bw=Math.min(24,(st*.8-2*gap)/3),tot=3*bw+2*gap;let g='';
[1,.5,0,-.5,-1].forEach(v=>{g+=`<line x1="${l}" x2="${w-r}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(${v?'--line':'--zero'})"/><text x="${l-6}" y="${Y(v)+4}" text-anchor="end">${v?(v<0?'−':'')+Math.abs(v).toFixed(1):'0'}</text>`});
per.forEach((p,i)=>{const c=l+st*(i+.5);
s.forEach((a,j)=>{const v=a[i];g+=`<rect x="${c-tot/2+j*(bw+gap)}" width="${bw}" y="${Math.min(Y(v),Y(0))}" height="${Math.abs(Y(v)-Y(0))}" fill="var(--s${j+1})"/>`});
if(k==='1m'){if(p.endsWith('-01'))g+=`<text x="${c-st/2}" y="${h-6}">${p.slice(0,4)}</text>`}
else g+=`<text x="${c}" y="${h-6}" text-anchor="middle">${k==='6m'&&st<60?p.slice(5)+"'"+p.slice(2,4):p}</text>`});
const el=document.createElement('div');
el.innerHTML=`<h3>${lab}</h3><div class="ch"><svg viewBox="0 0 ${w} ${h}" height="${h}" role="img" aria-label="${lab} correlation">${g}</svg><div class="tip" hidden></div></div>`;
host.append(el);
const sv=el.querySelector('svg'),tip=el.querySelector('.tip');
sv.addEventListener('pointermove',e=>{const i=Math.max(0,Math.min(n-1,Math.floor((e.clientX-sv.getBoundingClientRect().left-l)/st))),c=l+st*(i+.5);tip.hidden=false;
tip.innerHTML=per[i]+'<br>'+s.map((a,j)=>`<span style="display:inline-block;width:8px;height:8px;background:var(--s${j+1})"></span> ${NM[j]} ${f(a[i])}`).join('<br>');
tip.style.left=(c>w/2?c-tip.offsetWidth-14:c+14)+'px'});
sv.addEventListener('pointerleave',()=>tip.hidden=true)})}
document.querySelectorAll('[data-m]').forEach(b=>b.onclick=()=>{M=b.dataset.m;draw()});
draw();let z;addEventListener('resize',()=>{clearTimeout(z);z=setTimeout(draw,150)});
</script>
'''
out = t[:t.index('<main>')] + body + '\n' + js.replace('/*DATA*/', json.dumps(D, separators=(',', ':')))
open('us_nifty.html', 'w', encoding='utf8').write(out)
