import subprocess,re,html,time,urllib.parse
UA="LingoDudeVideoBot/0.1 (lingodude video research)"
def get(url):
    for a in range(10):
        r=subprocess.run(["curl","-s","-L","-A",UA,"-w","\n%{http_code}",url],capture_output=True,text=True).stdout
        body,code=r.rsplit("\n",1)
        if code=="200" and "mw-pages" in body or code=="200" and "mw-subcategories" in body or code=="200" and "noarticletext" in body: return body
        if code=="404": return ""
        time.sleep(min(120,10*(a+1)))
    return ""
def section(body,ids):
    out=[]
    for sid in ids:
        m=re.search(r'<div id="'+sid+r'"(.*?)(?:<div id="mw-|<div class="printfooter|$)',body,re.S)
        if m: out.append(m.group(1))
    return "".join(out)
def walk(host,cat,depth=0,seen=None):
    seen=seen if seen is not None else set()
    if cat in seen: return set()
    seen.add(cat)
    pages=set(); url=f"https://{host}/wiki/"+urllib.parse.quote(cat.replace(" ","_"))
    subcats=set()
    while url:
        body=get(url)
        if not body: break
        mp=section(body,["mw-pages"])
        for t in re.findall(r'<li[^>]*><a href="[^"]*" title="([^"]+)"',mp): pages.add(html.unescape(t))
        sc=section(body,["mw-subcategories"])
        for t in re.findall(r'href="/wiki/([^"#?]+)"',sc):
            t=urllib.parse.unquote(t).replace("_"," ")
            if ":" in t: subcats.add(t)
        nxt=re.search(r'<a href="([^"]+pagefrom=[^"]+)"[^>]*>[^<]*(?:next page|次のページ|다음 페이지|หน้าถัดไป)',mp)
        url=("https://"+host+html.unescape(nxt.group(1))) if nxt else None
        time.sleep(1.5)
    if depth>0:
        for s in subcats: pages|=walk(host,s,depth-1,seen)
    return pages
