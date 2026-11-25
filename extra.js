const E=/*DEEP*/,$=i=>document.getElementById(i);
const pc=(v,s=1)=>`color-mix(in srgb,var(${v<0?'--neg':'--pos'}) ${Math.min(60,Math.abs(v)/s*60).toFixed(0)}%,var(--bg))`;
const esc=s=>s.replaceAll('-','−').replace('<','&lt;').replace('>','&gt;');
function heat(id,head,rows){$(id).innerHTML='<table><thead><tr>'+head.map(x=>`<th>${x}</th>`).join('')+'</tr></thead><tbody>'+rows.map(([n,a])=>`<tr><td>${n}</td>`+a.map(v=>v==null?'<td></td>':`<td style="background:${pc(v,.8)}">${f(v)}</td>`).join('')+'</tr>').join('')+'</tbody></table>'}
const MN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],Y4=['2023','2024','2025','2026'];let I='SPX';
function months(){
document.querySelectorAll('[data-i]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.i===I));
heat('c-mon',['',...MN],Y4.map(y=>[y,MN.map((_,m)=>{const i=D.d_lag_1m.indexOf(y+'-'+String(m+1).padStart(2,'0'));return i<0?null:D['lag_'+I+'_1m'][i]})]))}
document.querySelectorAll('[data-i]').forEach(b=>b.onclick=()=>{I=b.dataset.i;months()});months();
const h26={NIFTY:.02,Nikkei:.46,'Hang Seng':.15,KOSPI:.33,Taiwan:.45,'ASX 200':.49};
heat('c-peer',['Market',...Y4,'H2 2026'],Object.entries(E.peer).map(([k,a])=>[k,[...a,h26[k]]]));
heat('c-lead',['','NIFTY leads by 3','By 2','By 1','Same date','Prior US session','2 earlier','3 earlier'],Object.entries(E.lead));
heat('c-hor',['','1 session','2','5','10','21'],Object.entries(E.hor));
$('t-bk').innerHTML=E.bk.map(b=>`<tr><td>${esc(b[0])}</td><td>${b[3]}</td><td>${b[1]<0?'−':'+'}${Math.abs(b[1]).toFixed(2)}% ± ${b[2].toFixed(2)}</td><td>${b[4]}%</td></tr>`).join('');
$('t-beta').innerHTML='<tr><td>NIFTY % per 1%</td>'+E.beta.SPX.map(b=>`<td>${b[1].toFixed(2)}</td>`).join('')+'</tr><tr><td>Variance explained</td>'+E.beta.SPX.map(b=>`<td>${b[2].toFixed(1)}%</td>`).join('')+'</tr>';
function frame(id,h,lo,hi,ticks,fmt,body,label){
const w=Math.max(300,$(id).clientWidth),l=46,r=8,t=10,b=28,Y=v=>t+(h-t-b)*(hi-v)/(hi-lo);
let g=ticks.map(v=>`<line x1="${l}" x2="${w-r}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(${v?'--line':'--zero'})"/><text x="${l-6}" y="${Y(v)+4}" text-anchor="end">${fmt(v)}</text>`).join('');
g+=body({w,h,l,r,t,b,Y});
$(id).innerHTML=`<div class="ch"><svg viewBox="0 0 ${w} ${h}" height="${h}" role="img" aria-label="${label}">${g}</svg></div>`}
const s1=v=>v?(v<0?'−':'')+Math.abs(v).toFixed(1):'0',yr=(q,w)=>w<520&&/^20/.test(q)?"'"+q.slice(2):q;
function ciplot(id,rows,lab,lo){
frame(id,220,lo,.75,[-.25,0,.25,.5,.75].filter(v=>v>=lo),v=>v?f(v):'0',o=>rows.map((q,i)=>{
const x=o.l+(o.w-o.l-o.r)*(i+.5)/rows.length;
return `<g><title>${q[0]}: ${f(q[1])} (${f(q[2])} to ${f(q[3])})</title><rect x="${x-12}" width="24" y="${o.t}" height="${o.h-o.t-o.b}" fill="transparent"/><line x1="${x}" x2="${x}" y1="${o.Y(q[2])}" y2="${o.Y(q[3])}" stroke="var(--s1)" stroke-width="2"/><circle cx="${x}" cy="${o.Y(q[1])}" r="5" fill="var(--s1)"/><text x="${x}" y="${o.h-8}" text-anchor="middle">${yr(q[0],o.w)}</text></g>`}).join(''),lab)}
function bars(id,rows,lo,hi,tk,fmt,lab,err){
frame(id,220,lo,hi,tk,fmt,o=>rows.map((q,i)=>{
const st=(o.w-o.l-o.r)/rows.length,x=o.l+st*(i+.5),bw=Math.min(36,st*.6),y=o.Y(q[1]);
const name=err?(o.w<560?['Big fall','Fall','Flat','Rise','Big rise'][i]:esc(q[0])):yr(q[0],o.w);
return `<g><title>${esc(q[0])}: ${f(q[1])}</title><rect x="${x-bw/2}" width="${bw}" y="${Math.min(y,o.Y(0))}" height="${Math.abs(y-o.Y(0))}" fill="var(${q[1]<0?'--neg':'--pos'})"/>${err?`<line x1="${x}" x2="${x}" y1="${o.Y(q[1]-q[2])}" y2="${o.Y(q[1]+q[2])}" stroke="var(--fg)" stroke-width="1.5"/>`:''}<text x="${x}" y="${o.h-8}" text-anchor="middle">${name}</text></g>`}).join(''),lab)}
function extra(){
frame('c-lev',300,90,270,[100,150,200,250],v=>v,o=>{
const n=E.lev.d.length,X=i=>o.l+(o.w-o.l-o.r)*i/(n-1);let g='';
[['SPX','--s1'],['COMP','--s2'],['DJI','--s3'],['NIFTY','--fg']].forEach(([k,c])=>g+=`<polyline fill="none" stroke="var(${c})" stroke-width="${k=='NIFTY'?3:2}" stroke-linejoin="round" points="${E.lev[k].map((v,i)=>X(i).toFixed(1)+','+o.Y(v).toFixed(1)).join(' ')}"/>`);
Y4.forEach(y=>{const i=E.lev.d.findIndex(d=>d.startsWith(y));g+=`<text x="${X(i)}" y="${o.h-8}">${y}</text>`});
return g+`<line class="x" y1="${o.t}" y2="${o.h-o.b}" stroke="var(--zero)" visibility="hidden"/>`},'Rebased index levels');
const ch=$('c-lev').firstChild,sv=ch.firstChild,tip=document.createElement('div');tip.className='tip';tip.hidden=true;ch.append(tip);
sv.addEventListener('pointermove',e=>{
const n=E.lev.d.length,w=sv.clientWidth,i=Math.max(0,Math.min(n-1,Math.round((e.clientX-sv.getBoundingClientRect().left-46)/(w-54)*(n-1)))),x=46+(w-54)*i/(n-1),ln=sv.querySelector('.x');
ln.setAttribute('x1',x);ln.setAttribute('x2',x);ln.setAttribute('visibility','visible');tip.hidden=false;
tip.innerHTML=E.lev.d[i]+'<br>'+[['NIFTY','NIFTY'],['SPX','S&amp;P 500'],['COMP','Nasdaq'],['DJI','Dow']].map(([k,n])=>`${n} ${E.lev[k][i].toFixed(1)}`).join('<br>');
tip.style.left=(x>w/2?x-tip.offsetWidth-10:x+10)+'px'});
sv.addEventListener('pointerleave',()=>{tip.hidden=true;sv.querySelector('.x').setAttribute('visibility','hidden')});
ciplot('c-long',E.long.SPX,'Yearly correlation since 2015',-.25);
bars('c-ll',E.ll,-.5,1,[-.5,0,.5,1],s1,'Yearly price-level correlation with the S&amp;P');
ciplot('c-vix',E.vix.map(v=>['VIX '+v[4].toFixed(1)+'–'+v[5].toFixed(1),v[1],v[2],v[3]]),'Correlation by VIX level',-.25);
bars('c-bk',E.bk,-1,1,[-1,-.5,0,.5,1],v=>s1(v)+'%','NIFTY response by S&amp;P move',true);
frame('c-sc',340,-6,6,[-6,-3,0,3,6],v=>v<0?'−'+-v:v,o=>{
const X=v=>o.l+(o.w-o.l-o.r)*(v+6)/12;let g='';
[-6,-3,0,3,6].forEach(v=>g+=`<line x1="${X(v)}" x2="${X(v)}" y1="${o.t}" y2="${o.h-o.b}" stroke="var(${v?'--line':'--zero'})"/><text x="${X(v)}" y="${o.h-8}" text-anchor="${v==6?'end':'middle'}">${v==0?'S&amp;P 0':v<0?'−'+-v:v}</text>`);
E.sc.filter(p=>Math.abs(p[0])<=6&&Math.abs(p[1])<=6).forEach(p=>g+=`<circle cx="${X(p[0]).toFixed(1)}" cy="${o.Y(p[1]).toFixed(1)}" r="3" fill="var(--s1)" fill-opacity=".45"><title>S&amp;P ${f(p[0])}%, NIFTY ${f(p[1])}%</title></circle>`);
return g},'Scatter of S&amp;P and NIFTY returns')}
extra();let z2;addEventListener('resize',()=>{clearTimeout(z2);z2=setTimeout(extra,150)});
