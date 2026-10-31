// Map-tour videos (blueprints/LANGUAGE_VIDEO_BLUEPRINT.md): world map -> zoom into each country ->
// flag-filled country with a face reveals, one speech bubble pops per language while a counter climbs,
// characters stay on the map, the record holder comes last.
// node maptour.mjs <episode> [--still t1,t2] [--preview]   -> out/<episode>.mp4
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import * as d3 from "d3-geo";
import * as topo from "topojson-client";
import { FONT_CSS, renderClip } from "./render.mjs";
import { EPISODES } from "./maptour_episodes.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, "out");
const W = 1920, H = 1080, FPS = 30;
const T = { cold: 3.0, title: 4.7, block: 350 / 30, outro: 5.0 };
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf("--" + k); return i < 0 ? d : args[i + 1] ?? true; };
const fileUrl = (p) => pathToFileURL(p).href;
const nm = (p) => path.join(HERE, "node_modules", p);

// ---------- map geometry (precomputed in Node, drawn as SVG paths) ----------
const world = JSON.parse(fs.readFileSync(nm("world-atlas/countries-50m.json")));
const countries = topo.feature(world, world.objects.countries).features.filter((f) => f.id !== "010"); // no Antarctica
const proj = d3.geoNaturalEarth1().fitExtent([[30, 70], [W - 30, H - 30]], { type: "FeatureCollection", features: countries });
const gp = d3.geoPath(proj);
const r2 = (d) => (d || "").replace(/\d+\.\d+/g, (n) => (+n).toFixed(1));

function mainland(f) { // largest polygon: bounds/centroid without far-away islands
  const polys = f.geometry.type === "MultiPolygon" ? f.geometry.coordinates.map((c) => ({ type: "Polygon", coordinates: c })) : [f.geometry];
  return polys.map((g) => ({ g, a: gp.area(g) })).sort((a, b) => b.a - a.a)[0].g;
}

function episodeData(ep) {
  return ep.items.map((it) => {
    const f = countries.find((c) => c.id === it.id);
    if (!f) throw new Error("no country " + it.id);
    const m = mainland(f);
    const [[x0, y0], [x1, y1]] = gp.bounds(m);
    const [cx, cy] = gp.centroid(m);
    const bw = Math.max(x1 - x0, 0.5), bh = Math.max(y1 - y0, 0.5);
    const s = Math.min(Math.min((W * 0.42) / bw, (H * 0.55) / bh), it.maxZoom || 60);
    return { ...it, d: r2(gp(f)), box: [x0, y0, bw, bh], c: [cx + (it.dx || 0) / s, cy + (it.dy || 0) / s], s };
  });
}

// ---------- the page ----------
function page(ep, items) {
  const land = countries.map((f) => `<path d="${r2(gp(f))}"/>`).join("");
  const flag = (code) => fileUrl(nm(`flag-icons/flags/4x3/${code}.svg`));
  const blocks0 = T.cold + T.title;
  const total = blocks0 + items.length * T.block + T.outro;
  // map-space layers per country: flag fill, face, bubbles (sizes are screen px at that country's hold zoom)
  const chars = items.map((it, i) => {
    const k = 1 / it.s, [cx, cy] = it.c, [x0, y0, bw, bh] = it.box;
    const pad = Math.max(bw, bh) * 0.1;
    const er = 62 * k, ex = 88 * k, ey = cy - 105 * k;
    const n = it.langs.length;
    // counter badge under the eyes: counts up to the number of languages, stays on the map afterwards
    const badge = `<g class="badge" transform="translate(${cx.toFixed(2)} ${(cy + 45 * k).toFixed(2)}) scale(${k.toFixed(5)})"><g class="bz"><circle r="78" fill="#fff" stroke="#1b1b1b" stroke-width="9"/><text class="bn" y="30" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="${n > 9 ? 84 : 100}" fill="#e8262b">0</text></g></g>`;
    const eye = (x, side) => `<g transform="translate(${x.toFixed(2)} ${ey.toFixed(2)}) scale(${(er / 30).toFixed(4)})">
      <path d="M-30 2 C-18 -16 18 -16 30 2 C18 18 -18 18 -30 2Z" fill="#fff" stroke="#1b1b1b" stroke-width="4"/>
      <g class="pupil"><circle cx="${side * 2}" cy="3" r="10" fill="#1b1b1b"/><circle cx="${side * 2 - 3}" cy="-1" r="3" fill="#fff"/></g>
      <path class="lid" d="M-30 2 C-18 -16 18 -16 30 2" fill="none" stroke="#1b1b1b" stroke-width="7" stroke-linecap="round"/>
      <path d="M-22 16 C-10 24 10 24 22 15" fill="none" stroke="#1b1b1b" stroke-width="3" opacity=".55" stroke-linecap="round"/>
      <rect class="shut" x="-32" y="-18" width="64" height="40" fill="url(#skin${i})" opacity="0"/></g>`;
    return `<g class="char" id="ch${i}" opacity="0">
      <defs><clipPath id="cl${i}"><path d="${it.d}"/></clipPath><linearGradient id="skin${i}"><stop stop-color="#e8d9b5"/></linearGradient></defs>
      <g clip-path="url(#cl${i})"><image href="${flag(it.flag)}" x="${x0 - pad}" y="${y0 - pad}" width="${bw + 2 * pad}" height="${bh + 2 * pad}" preserveAspectRatio="xMidYMid slice"/></g>
      <path d="${it.d}" fill="none" stroke="#fff" class="inner"/>
      <path d="${it.d}" fill="none" stroke="#1b1b1b" class="outer"/>
      <g class="face" opacity="0">${eye(cx - ex, -1)}${eye(cx + ex, 1)}</g>
      ${badge}</g>`;
  }).join("");
  const clouds = [[180, 230, 1.0], [700, 160, 0.8], [1240, 250, 1.1], [1650, 140, 0.9], [420, 760, 1.0], [1050, 840, 0.85], [1500, 700, 1.0], [250, 940, 0.7]]
    .map(([x, y, s], i) => `<g class="cloud" data-x="${x}" data-v="${10 + (i % 3) * 6}" transform="translate(${x} ${y}) scale(${s})"><path d="M-110 30 C-140 30 -140 -10 -105 -12 C-100 -50 -40 -55 -25 -28 C-5 -60 60 -55 62 -15 C100 -18 115 30 80 30Z" fill="#f4f8fb" stroke="#c9d6e2" stroke-width="5" opacity=".92"/></g>`).join("");
  const C = JSON.stringify(items.map((it) => ({ c: it.c, s: it.s, n: it.langs.length })));
  const L = JSON.stringify(items.map((it) => it.langs));
  return `<!doctype html><html><head><meta charset="utf-8">${FONT_CSS}<style>
  *{margin:0;padding:0;box-sizing:border-box}body{width:${W}px;height:${H}px;overflow:hidden;font-family:Montserrat;background:#1d5f9a}
  .abs{position:absolute}
  #sea{inset:0;background:linear-gradient(#5fc3c9,#2f86b8 45%,#1d5a96)}
  .band{left:-200px;width:2400px;height:26px;border-radius:13px;background:rgba(255,255,255,.10)}
  svg{position:absolute;left:0;top:0}
  #land path{fill:#e6cf96;stroke:#1b1b1b;stroke-linejoin:round}
  #card{right:48px;top:44px;width:400px;text-align:center;opacity:0}
  #card .flag{width:400px;height:300px;background-size:cover;background-position:center;border:6px solid #fff;border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.4)}
  #card .name{margin-top:10px;font-weight:800;font-size:58px;color:#fff;text-shadow:${[...Array(12)].map((_, i) => `${(Math.cos(i / 12 * 6.283) * 5).toFixed(1)}px ${(Math.sin(i / 12 * 6.283) * 5).toFixed(1)}px 0 #1b1b1b`).join(",")}}
  #card .count{display:inline-block;margin-top:8px;background:#e8262b;color:#fff;font-weight:800;font-size:96px;line-height:1;padding:8px 30px 12px;border:6px solid #fff;border-radius:16px;box-shadow:0 8px 20px rgba(0,0,0,.35)}
  #card .count small{font-size:24px;letter-spacing:1px;display:block;margin-top:4px}
  #tick{left:30px;right:30px;bottom:26px;display:flex;flex-wrap:wrap;gap:10px;justify-content:center;opacity:0}
  #tick span{background:rgba(15,18,28,.88);color:#fff;font-weight:800;border-radius:24px;padding:6px 18px 8px;opacity:0;border:3px solid rgba(255,255,255,.85)}
  .t{left:0;width:${W}px;text-align:center;font-weight:800;color:#fff;opacity:0;text-shadow:${[...Array(16)].map((_, i) => `${(Math.cos(i / 16 * 6.283) * 6).toFixed(1)}px ${(Math.sin(i / 16 * 6.283) * 6).toFixed(1)}px 0 #1b1b1b`).join(",")},0 10px 0 #1b1b1b}
  #cold{top:330px;font-size:84px;line-height:1.08}
  #t1{top:300px;font-size:104px}#t2{top:430px;font-size:104px}
  #t3{top:600px}#t3 span{display:inline-block;background:#e8262b;border:6px solid #fff;border-radius:18px;padding:6px 34px 12px;font-size:64px}
  #outro{top:960px;font-size:46px}
  #fw{inset:0;pointer-events:none}
  </style></head><body>
  <div id="sea" class="abs"></div>
  ${[120, 300, 520, 700, 880, 1010].map((y, i) => `<div class="abs band" style="top:${y}px;transform:translateX(${(i % 2) * 140}px)"></div>`).join("")}
  <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><g id="cam"><g id="land">${land}</g>${chars}</g></svg>
  <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" id="clouds">${clouds}</svg>
  <svg id="fw" class="abs" width="${W}" height="${H}"></svg>
  <div id="card" class="abs"><div class="flag"></div><div class="name"></div><div class="count"><span class="n">0</span><small></small></div></div>
  <div id="tick" class="abs"></div>
  <div id="cold" class="abs t">${ep.cold}</div>
  <div id="t1" class="abs t">${ep.titleLines[0]}</div><div id="t2" class="abs t">${ep.titleLines[1]}</div><div id="t3" class="abs t"><span>${ep.titleLines[2]}</span></div>
  <div id="outro" class="abs t">${ep.outro}</div>
  <script>
  const C=${C}, L=${L}, META=${JSON.stringify(items.map((it) => ({ name: it.name, unit: it.unit, flag: flag(it.flag) })))};
  const B0=${blocks0}, BL=${T.block}, TOTAL=${total}, COLD=${T.cold}, TITLE=${T.title};
  const $=(s)=>document.querySelector(s), cam=$('#cam');
  const cl=(x)=>Math.min(1,Math.max(0,x)), ease=(x)=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}, back=(x)=>{x=cl(x);const c=1.6;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
  const W0=[${W / 2},${H / 2}];
  function camAt(c1,s1,e){ // zoom from the world (s=1, centre W0) towards c1/s1, keeping the motion smooth
    const s=Math.exp(Math.log(s1)*e); const w=(1-1/s)/(1-1/s1);
    const tgt=[c1[0]-(760-${W / 2})/s1, c1[1]-(540-${H / 2})/s1];
    return [[W0[0]+(tgt[0]-W0[0])*w, W0[1]+(tgt[1]-W0[1])*w], s];
  }
  let tickFor=-1;
  window.setT=(t)=>{
    // ----- which segment
    let blk=-1, bt=0;
    if(t>=B0 && t<B0+C.length*BL){blk=Math.floor((t-B0)/BL); bt=t-B0-blk*BL;}
    // ----- camera
    let c=W0, s=1, fg=0;
    if(blk>=0){
      const q=C[blk];
      let e=0;
      if(bt<0.33) e=0; else if(bt<1.8) e=ease((bt-0.33)/1.47); else if(bt<9.5) e=1; else if(bt<11.0) e=1-ease((bt-9.5)/1.5); else e=0;
      if(bt>3.0&&bt<3.25) e=1+0.04*Math.sin((bt-3.0)/0.25*Math.PI); // small push-in on the reveal
      [c,s]=camAt(q.c,q.s,Math.min(e,1)); if(e>1) s*=e;
      fg=bt<1.4?cl((bt-0.33)/0.9):bt<9.6?1:1-cl((bt-9.6)/1.2);
    }
    cam.setAttribute('transform','translate('+W0[0]+' '+W0[1]+') scale('+s+') translate('+(-c[0])+' '+(-c[1])+')');
    document.querySelectorAll('#land path').forEach(p=>p.style.strokeWidth=(1.1+Math.log(s)*1.1)/s);
    $('#clouds').style.opacity=(1-fg).toFixed(3);
    // ----- characters: hidden until their reveal, then persistent
    C.forEach((q,i)=>{
      const g=document.getElementById('ch'+i);
      const start=B0+i*BL;
      const local=t-start;
      const vis = t>=start+2.5 ? 1 : 0;
      g.setAttribute('opacity', vis);
      if(!vis) return;
      const flagA = local<3.2 ? 0.4*cl((local-2.5)/0.4) : 1;
      g.querySelector('image').setAttribute('opacity', flagA);
      g.querySelectorAll('.inner').forEach(p=>{p.style.strokeWidth=(5/q.s)+'px'});
      g.querySelectorAll('.outer').forEach(p=>{p.style.strokeWidth=(Math.max(1.5,(1.1+Math.log(s)*1.1))/s*1.6)+'px'});
      const face=g.querySelector('.face');
      face.setAttribute('opacity', local>=3.2?1:0);
      // blinks and glances
      const blink = [5.3,7.6,9.0].some(b=>local>b&&local<b+0.1) || (t>B0+C.length*BL && ((t*10)%37<1));
      g.querySelectorAll('.shut').forEach(r=>r.setAttribute('opacity',blink?1:0));
      const gl = (local>6.4&&local<7.2)? (i%2?6:-6) : 0;
      g.querySelectorAll('.pupil').forEach(p=>p.setAttribute('transform','translate('+gl+' 0)'));
      // counter counts up, with a small bump on every new number
      const n=q.n, gap=Math.min(0.25, 4.2/n), since=local-3.5;
      const shown=since<0?0:Math.min(n, Math.floor(since/gap)+1);
      const bz=g.querySelector('.bz'), bn=g.querySelector('.bn');
      bn.textContent=shown;
      const intro=back((local-3.3)/0.3), bump= shown<n ? 1+0.12*Math.max(0,1-((since%gap)/gap)*3) : 1+0.18*Math.max(0,1-(since-(n-1)*gap)/0.4);
      bz.setAttribute('transform','scale('+(local<3.3?0:intro*bump).toFixed(3)+')');
    });
    // ----- card + ticker for the current block
    const card=$('#card'), tick=$('#tick');
    if(blk>=0 && bt>3.3 && bt<9.3){
      const m=META[blk], q=C[blk], gap=Math.min(0.25, 4.2/q.n);
      const k=ease((bt-3.3)/0.4), out=ease((bt-9.0)/0.3);
      card.style.opacity=1; card.style.transform='translateX('+((1-k)*500+out*500)+'px)';
      card.querySelector('.flag').style.backgroundImage='url('+m.flag+')';
      card.querySelector('.name').textContent=m.name; card.querySelector('.name').style.fontSize=Math.min(58,Math.floor(540/m.name.length))+'px';
      const shown=Math.max(0,Math.min(q.n, Math.floor((bt-3.5)/gap)+1));
      card.querySelector('.n').textContent=shown;
      card.querySelector('small').textContent=m.unit;
      if(tickFor!==blk){ tick.innerHTML=L[blk].map(x=>'<span>'+x+'</span>').join(''); tickFor=blk; }
      const fs = q.n>30?29:q.n>20?33:q.n>10?40:52;
      tick.style.opacity=1-out;
      tick.querySelectorAll('span').forEach((sp,j)=>{sp.style.fontSize=fs+'px'; sp.style.opacity=(bt-3.5-j*gap)>0?1:0;});
    } else { card.style.opacity=0; tick.style.opacity=0; }
    // ----- cold open, title, outro
    const fade=(a,b,x)=>cl((x-a)/0.25)*(1-cl((x-b)/0.3));
    $('#cold').style.opacity=fade(0.1,COLD-0.35,t);
    $('#cold').style.transform='scale('+(0.9+0.1*back((t-0.1)/0.35))+')';
    [['#t1',COLD+0.0],['#t2',COLD+0.35],['#t3',COLD+0.7]].forEach(([id,a])=>{const e=$(id); e.style.opacity=fade(a,COLD+TITLE-0.6,t); e.style.transform='scale('+(0.6+0.4*back((t-a)/0.35))+')';});
    $('#outro').style.opacity=fade(TOTAL-T_OUT+0.6,TOTAL+9,t);
    // ----- clouds drift
    document.querySelectorAll('.cloud').forEach(c=>{const x=(+c.dataset.x+t*(+c.dataset.v))%2150-100; c.setAttribute('transform',c.getAttribute('transform').replace(/translate\\([^ ]+/,'translate('+x));});
    // ----- fireworks on the finale block only
    const fw=$('#fw'); fw.innerHTML='';
    if(blk===C.length-1 && bt>3.4 && bt<9.4){
      let s2='';
      for(let b=0;b<7;b++){
        const t0=3.4+b*0.8, u=(bt-t0)/1.1; if(u<0||u>1) continue;
        const x=[1300,1650,1480,1180,1750,1380,1580][b], y=[260,200,380,160,330,120,250][b], col=['#ffd23f','#ff5c8a','#5ce1ff','#ffffff','#9bff5c','#ff9a3c','#c77dff'][b];
        for(let r=0;r<28;r++){const a=r/28*6.283, d=20+230*Math.sqrt(u), x2=x+Math.cos(a)*d, y2=y+Math.sin(a)*d+70*u*u, x1=x+Math.cos(a)*d*0.7, y1=y+Math.sin(a)*d*0.7+50*u*u; s2+='<line x1="'+x1+'" y1="'+y1+'" x2="'+x2+'" y2="'+y2+'" stroke="'+col+'" stroke-width="'+(7*(1-u)+2)+'" stroke-linecap="round" opacity="'+(1-u*u)+'"/>';}
      }
      fw.innerHTML=s2;
    }
  };
  const T_OUT=${T.outro};
  </script></body></html>`;
}

// ---------- sound: synthesized effects only (no music, no speech) ----------
// national anthem recordings (public domain, Wikimedia Commons) in cache/anthems/<flag>.*; credits in credits.json
function anthemFile(code) {
  const dir = path.join(HERE, "cache", "anthems");
  const f = fs.existsSync(dir) && fs.readdirSync(dir).find((x) => x.startsWith(code + ".") && !x.endsWith(".json"));
  return f ? path.join(dir, f) : null;
}
function sound(ep, items, wavOut) {
  const plan = { sr: 48000, total: T.cold + T.title + items.length * T.block + T.outro, cold: T.cold, title: T.title, block: T.block, b0: T.cold + T.title,
    blocks: items.map((it, i) => ({ n: it.langs.length, finale: i === items.length - 1, music: anthemFile(it.flag) })) };
  const py = `
import json, sys, wave, numpy as np
p=json.loads(sys.argv[1]); sr=p['sr']; N=int(p['total']*sr)+sr
L=np.zeros(N); R=np.zeros(N); rng=np.random.default_rng(7)
def add(sig,t,pan=0.0,g=1.0):
    i=int(t*sr); n=min(len(sig),N-i)
    if n<=0: return
    L[i:i+n]+=sig[:n]*g*(1-max(0,pan)); R[i:i+n]+=sig[:n]*g*(1+min(0,pan))
def env(n,a,d): x=np.arange(n)/sr; return np.minimum(1,x/max(a,1e-4))*np.exp(-x/d)
def whoosh(dur=1.5,up=True):
    n=int(dur*sr); w=rng.standard_normal(n); out=np.zeros(n); y=0
    f=np.linspace(300,2500,n) if up else np.linspace(2500,300,n)
    for k in range(n):
        a=f[k]/sr; y+= (w[k]-y)*min(1,a*6); out[k]=y
    shape=np.sin(np.linspace(0,np.pi,n))**2
    return out*shape*0.5
def hit():
    n=int(0.9*sr); x=np.arange(n)/sr
    body=np.sin(2*np.pi*(90*np.exp(-x*6)+45)*x)*np.exp(-x*5)
    click=rng.standard_normal(n)*np.exp(-x*60)*0.5
    return (body+click)*0.9
def pop(f):
    n=int(0.12*sr); x=np.arange(n)/sr
    return np.sin(2*np.pi*(f+f*1.5*np.exp(-x*40))*x)*np.exp(-x*35)*0.35
def crackle(dur=1.2):
    n=int(dur*sr); s=np.zeros(n)
    for _ in range(140):
        i=rng.integers(0,n-400); s[i:i+300]+=rng.standard_normal(300)*np.exp(-np.arange(300)/40)*rng.uniform(.2,.6)
    boom=np.sin(2*np.pi*60*np.arange(n)/sr)*np.exp(-np.arange(n)/sr*6)*0.6
    return s*0.5+boom
# cold open sting + title pops
add(hit()*0.7,0.1)
for k in range(3): add(pop(500+k*180)*1.4, p['cold']+0.35*k)
for i,b in enumerate(p['blocks']):
    t0=p['b0']+i*p['block']
    add(whoosh(1.5,True),t0+0.33,g=0.9)
    add(hit(),t0+3.2)
    gap=min(0.25,4.2/b['n'])
    for j in range(b['n']): add(pop(520+ (j%8)*70), t0+3.5+j*gap, pan=((j%5)-2)*0.15)
    add(whoosh(1.5,False),t0+9.5,g=0.8)
    if b['finale']:
        for k in range(7): add(crackle(), t0+3.4+k*0.8, pan=((k%3)-1)*0.4, g=0.7)
import subprocess
def load(fn):  # decode to 48 kHz stereo float, skip the silent start
    raw=subprocess.run(['ffmpeg','-v','error','-i',fn,'-ac','2','-ar',str(sr),'-f','f32le','-'],capture_output=True,check=True).stdout
    a=np.frombuffer(raw,np.float32).reshape(-1,2).astype(float)
    loud=np.where(np.abs(a).max(1)>0.02)[0]
    return a[loud[0]:] if len(loud) else a
for i,b in enumerate(p['blocks']):
    if not b.get('music'): continue
    t0=p['b0']+i*p['block']+3.15; dur=6.3 if not b['finale'] else 6.6
    a=load(b['music'])[:int(dur*sr)]
    a=a/ (np.abs(a).max()+1e-9) * 0.42
    n=len(a); fi=int(0.25*sr); fo=int(1.0*sr)
    g=np.ones(n); g[:fi]=np.linspace(0,1,fi); g[-fo:]=np.linspace(1,0,fo)
    j=int(t0*sr); m=min(n,N-j)
    L[j:j+m]+=a[:m,0]*g[:m]; R[j:j+m]+=a[:m,1]*g[:m]
m=max(np.abs(L).max(),np.abs(R).max()); L/=m/0.85; R/=m/0.85
d=(np.stack([L,R],1)*32767).astype(np.int16)
w=wave.open(sys.argv[2],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(d.tobytes()); w.close()
`;
  const r = spawnSync("python3", ["-c", py, JSON.stringify(plan), wavOut], { stdio: "inherit" });
  if (r.status) throw new Error("sound failed");
}

async function main() {
  const key = args.find((a) => !a.startsWith("--") && EPISODES[a]);
  if (!key) throw new Error("usage: node maptour.mjs <episode>  (" + Object.keys(EPISODES).join(", ") + ")");
  const ep = EPISODES[key], items = episodeData(ep);
  const html = page(ep, items);
  const dur = T.cold + T.title + items.length * T.block + T.outro;
  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
  const video = path.join(OUT, `${key}_video.mp4`);
  const stills = opt("still", null);
  await renderClip(browser, html, dur, video, stills ? String(stills).split(",").map(Number) : null);
  await browser.close();
  if (stills) { console.log("stills ->", OUT); return; }
  const wav = path.join(HERE, "cache", `${key}_sfx.wav`);
  sound(ep, items, wav);
  const final = path.join(OUT, `${key}.mp4`);
  spawnSync("ffmpeg", ["-v", "error", "-y", "-i", video, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-15:TP=-1.5", "-shortest", final], { stdio: "inherit" });
  fs.unlinkSync(video);
  // chapters for the description
  let t = T.cold + T.title;
  const ch = ["0:00 Intro", ...items.map((it) => { const s = Math.floor(t); t += T.block; return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")} ${it.name} (${it.langs.length})`; })];
  fs.writeFileSync(path.join(OUT, `${key}_chapters.txt`), ch.join("\n") + "\n");
  console.log("done:", final, dur.toFixed(1) + "s");
}
main().catch((e) => { console.error(e); process.exit(1); });
