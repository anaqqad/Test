// Video for the whistled-languages song: node song/render_song.mjs [--still 3,20,52] -> out/whistle_song.mp4
// Reads song/out/song.wav + song/out/timeline.json (from song/compose.py). Wojaks from wojaks/w_*.png.
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import { FONT_CSS, logoSvg, renderClip } from "../render.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const LINGO = path.join(HERE, "..");
const url = (p) => pathToFileURL(p).href;
const TL = JSON.parse(fs.readFileSync(path.join(HERE, "out", "timeline.json")));
const args = process.argv.slice(2);
const stills = args.includes("--still") ? args[args.indexOf("--still") + 1].split(",").map(Number) : null;

const WHO = {
  "Silbo Gomero": { w: "w_silbo", flag: "es", place: "La Gomera, Spain" },
  "Bird Language": { w: "w_kuskoy", flag: "tr", place: "Kuşköy, Turkey" },
  "Sfyria": { w: "w_sfyria", flag: "gr", place: "Antia, Greece" },
  "Whistled Occitan": { w: "w_aas", flag: "fr", place: "Aas, French Pyrenees" },
  "Whistled Yoruba": { w: "w_yoruba", flag: "ng", place: "Nigeria" },
  "Hmong": { w: "w_hmong", flag: "la", place: "Northern Laos" },
  "Chinantec": { w: "w_chinantec", flag: "mx", place: "Oaxaca, Mexico" },
  "Pirahã": { w: "w_piraha", flag: "br", place: "Amazonas, Brazil" },
  "Wayãpi": { w: "w_wayapi", flag: "gf", place: "French Guiana" },
};
// trimmed Wojaks (no transparent margin) so they stand on the stage floor
const pages = path.join(LINGO, "cache", "pages"); fs.mkdirSync(pages, { recursive: true });
for (const [n, o] of Object.entries(WHO)) {
  const t = path.join(pages, `song_${o.w}.png`);
  if (!fs.existsSync(t)) execFileSync("convert", [path.join(LINGO, "wojaks", o.w + ".png"), "-trim", "+repage", t]);
  o.img = url(t);
}
const flag = (c) => url(path.join(LINGO, "node_modules", "flag-icons", "flags", "4x3", c + ".svg"));
const names = Object.keys(WHO);

const html = `<!doctype html><html><head><meta charset="utf-8">${FONT_CSS}<style>
*{margin:0;padding:0;box-sizing:border-box}body{width:1920px;height:1080px;overflow:hidden;font-family:Montserrat;background:#0b0820}
.abs{position:absolute}
#stage{inset:0;background:radial-gradient(ellipse at 50% 120%,#3b1d6e 0%,#170d36 45%,#07051a 80%)}
.beam{top:-200px;width:420px;height:1400px;transform-origin:50% 0;background:linear-gradient(rgba(255,240,180,.22),rgba(255,240,180,0) 80%);clip-path:polygon(45% 0,55% 0,100% 100%,0 100%);mix-blend-mode:screen}
#floor{left:0;right:0;bottom:0;height:150px;background:linear-gradient(#2a1650,#120a28);border-top:4px solid #ff9de2}
#flash{inset:0;background:radial-gradient(circle at 50% 60%,rgba(255,120,220,.35),rgba(0,0,0,0) 60%);opacity:0}
#bar{left:0;top:0;width:1920px;height:118px;background:linear-gradient(#ffffff,#efeaf8);box-shadow:0 6px 24px rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center}
#bar h1{font-weight:800;font-size:52px;color:#18181d;letter-spacing:-1px}
#brand{left:30px;top:22px;display:flex;flex-direction:column;align-items:flex-start}
#brand small{font-weight:800;font-size:22px;color:#fff;background:#e8262b;border-radius:8px;padding:2px 12px;margin-top:4px;letter-spacing:1px}
.wj{bottom:110px;transform-origin:50% 100%;filter:drop-shadow(0 18px 30px rgba(0,0,0,.6));transition:none}
.wj img{display:block;height:100%}
.plate{display:flex;align-items:center;gap:16px;background:rgba(255,255,255,.95);border-radius:16px;padding:10px 22px;box-shadow:0 8px 24px rgba(0,0,0,.45)}
.plate img{height:46px;border-radius:6px;box-shadow:0 0 0 2px rgba(0,0,0,.1)}
.plate b{font-weight:800;font-size:44px;color:#18181d;line-height:1}.plate i{display:block;font-style:normal;font-weight:700;font-size:22px;color:#7a4fc0}
#cap{right:70px;top:170px;max-width:760px;background:#fff;border-radius:26px;padding:24px 34px;font-weight:800;font-size:46px;line-height:1.15;color:#18181d;box-shadow:0 12px 30px rgba(0,0,0,.45)}
#cap:after{content:"";position:absolute;left:-26px;bottom:40px;border:20px solid transparent;border-right:34px solid #fff}
#tag{right:70px;top:150px;background:#ffcc00;color:#18181d;font-weight:800;font-size:26px;padding:8px 18px;border-radius:10px;transform:rotate(-2deg)}
.note{font-size:70px;color:#ffd6f5;text-shadow:0 0 18px #ff6ad5;font-weight:800}
#big{left:0;right:0;top:150px;text-align:center;font-weight:800;font-size:110px;color:#fff;text-shadow:0 0 30px #ff6ad5,0 8px 0 #7a1fa0}
#credit{left:30px;bottom:18px;font-weight:600;font-size:18px;color:rgba(255,255,255,.75)}
#eq{right:40px;bottom:30px;display:flex;gap:8px;align-items:flex-end;height:80px}#eq i{display:block;width:14px;background:#ff6ad5;border-radius:4px}
</style></head><body>
<div id="stage" class="abs"></div>
<div class="abs beam" id="b1" style="left:180px"></div><div class="abs beam" id="b2" style="left:750px"></div><div class="abs beam" id="b3" style="left:1320px"></div>
<div id="floor" class="abs"></div><div id="flash" class="abs"></div>
<div id="people"></div>
<div id="notes"></div>
<div id="cap" class="abs"></div><div id="tag" class="abs"></div><div id="big" class="abs"></div>
<div id="plate" class="abs plate" style="left:70px;bottom:40px"></div>
<div id="eq" class="abs">${"<i></i>".repeat(10)}</div>
<div id="bar" class="abs"><h1>I Made a Song Using Only Whistled Languages</h1></div>
<div id="brand" class="abs">${logoSvg(52, true)}<small>PART 1</small></div>
<div id="credit" class="abs"></div>
<script>
const TL=${JSON.stringify(TL)}, WHO=${JSON.stringify(WHO)}, NAMES=${JSON.stringify(names)}, FLAG=${JSON.stringify(Object.fromEntries(names.map((n) => [n, flag(WHO[n].flag)])))};
const $=(id)=>document.getElementById(id);
const beat=60/TL.bpm;
function pulse(t){const ph=(t%beat)/beat;return Math.exp(-ph*6);}
let lastKey="";
function layout(sec){
  const ppl=$("people"); ppl.innerHTML="";
  const solo=sec.section==="solo"||sec.section==="intro";
  const who=sec.section==="intro"?["Silbo Gomero"]:sec.singers;
  if(solo){
    const n=who[0];
    ppl.innerHTML='<div class="abs wj" data-n="'+n+'" style="left:120px;height:760px"><img src="'+WHO[n].img+'"></div>';
    $("plate").style.display="flex";
    $("plate").innerHTML='<img src="'+FLAG[n]+'"><div><b>'+(n==="Bird Language"?"Turkish Bird Language":n)+'</b><i>'+WHO[n].place+'</i></div>';
  } else if(sec.section==="break"){
    ppl.innerHTML=who.map((n,i)=>'<div class="abs wj" data-n="'+n+'" style="left:'+(220+i*760)+'px;height:640px"><img src="'+WHO[n].img+'"></div><div class="abs plate" style="left:'+(240+i*760)+'px;bottom:30px"><img src="'+FLAG[n]+'"><div><b>'+(n==="Bird Language"?"Turkish Bird Language":n)+'</b><i>'+WHO[n].place+'</i></div></div>').join("");
    $("plate").style.display="none";
  } else {
    // group: 5 at the back, 4 in front
    ppl.innerHTML=NAMES.map((n,i)=>{const back=i%2===0, k=back?i/2:(i-1)/2;
      const x=back?60+k*380:250+k*380, h=back?430:470, b=back?250:110;
      return '<div class="abs wj" data-n="'+n+'" style="left:'+x+'px;height:'+h+'px;bottom:'+b+'px;z-index:'+(back?1:2)+'"><img src="'+WHO[n].img+'"></div>';}).join("");
    $("plate").style.display="none";
  }
  $("cap").style.display=solo&&sec.section==="solo"?"block":"none";
  $("cap").textContent=sec.caption;
  $("tag").style.display=sec.section==="break"?"block":"none";
  $("tag").textContent="ORIGINAL RECORDINGS, NO TUNING";
  $("big").style.left=sec.section==="intro"?"760px":"0";
  $("big").style.top=sec.section==="intro"?"430px":"150px";
  $("big").style.fontSize=sec.section==="intro"?"84px":"100px";
  $("big").innerHTML=sec.section==="intro"?"9 languages.<br>0 words.<br>1 song.":"";
  if(sec.section!=="intro") $("big").textContent=sec.section==="chorus"?"EVERYBODY NOW 🎶":sec.section==="outro"?"9 languages, 0 words 🐦":"";
  $("credit").textContent=solo?"Real recording: "+(sec.section==="intro"?"Silbo Gomero":who[0])+" · tuned to the melody · credits in the description":"Real whistled-language recordings · credits in the description";
}
window.setT=(t)=>{
  const sec=TL.sections.find(s=>t>=s.start&&t<s.end)||TL.sections[TL.sections.length-1];
  const key=sec.section+sec.start; if(key!==lastKey){layout(sec);lastKey=key;}
  const p=pulse(t), full=sec.section==="chorus"||sec.section==="outro";
  // who is whistling right now
  const active=new Set(TL.onsets.filter(o=>t>=o[0]&&t<o[0]+o[1]).map(o=>o[2]));
  if(sec.section==="intro"||sec.section==="break") sec.singers.forEach((n,i)=>{ if(sec.section!=="break"||(i===0)===(t<sec.start+TL.bar)) active.add(n); });
  document.querySelectorAll(".wj").forEach((el,i)=>{
    const on=active.has(el.dataset.n), b=on?p:p*0.35;
    el.style.transform="translateY("+(-b*(on?26:10))+"px) scale("+(1+b*(on?0.05:0.015))+") rotate("+(Math.sin(t*2.2+i)*(full?3:1.5))+"deg)";
    el.style.filter="drop-shadow(0 18px 30px rgba(0,0,0,.6)) brightness("+(on?1.12:full?0.75:0.9)+")"+(on?" drop-shadow(0 0 24px rgba(255,110,220,.8))":"");
  });
  // floating notes from the whistlers
  let nh="";
  document.querySelectorAll(".wj").forEach(el=>{ if(!active.has(el.dataset.n)) return;
    const r=el.getBoundingClientRect(); const ons=TL.onsets.filter(o=>o[2]===el.dataset.n&&t>=o[0]&&t<o[0]+1.2).slice(-3);
    ons.forEach((o,j)=>{const a=(t-o[0])/1.2; nh+='<div class="abs note" style="left:'+(r.left+r.width*0.62+a*120+j*20)+'px;top:'+(r.top+r.height*0.25-a*200)+'px;opacity:'+(1-a)+';font-size:'+(full?44:70)+'px">'+(j%2?"♫":"♪")+'</div>';});
  });
  $("notes").innerHTML=nh;
  ["b1","b2","b3"].forEach((id,i)=>{$(id).style.transform="rotate("+(Math.sin(t*0.8+i*2)*18)+"deg)";$(id).style.opacity=0.5+p*(full?0.5:0.25);});
  $("flash").style.opacity=full?p*0.9:p*0.25;
  document.querySelectorAll("#eq i").forEach((e,i)=>{e.style.height=(10+70*Math.abs(Math.sin(t*7+i*1.3))*(0.4+0.6*p))+"px";});
  $("big").style.transform="scale("+(1+p*0.06)+")";
};
</script></body></html>`;

const outFile = path.join(LINGO, "out", "whistle_song_video.mp4");
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
await renderClip(b, html, TL.duration, outFile, stills);
await b.close();
if (!stills) {
  const final = path.join(LINGO, "out", "whistle_song.mp4");
  execFileSync("ffmpeg", ["-v", "error", "-y", "-i", outFile, "-i", path.join(HERE, "out", "song.wav"), "-c:v", "copy",
    "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", final]);
  console.log("done:", final);
} else console.log("stills in out/");
