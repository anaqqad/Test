# Read the comments on every LingoDude video and count which languages viewers mention or ask for.
#   python read_comments.py                -> comments/comments.csv (all comments) + comments/summary.txt (send this one)
#   python read_comments.py --days 14      -> only comments from the last 14 days
# Uses the same Google Cloud OAuth client as upload_youtube.py (client_secret.json). The first run opens the browser to
# sign in; the token is kept in youtube_token_read.json. Both files are gitignored: never print or commit them.
# Free: about 1 quota unit per 100 comments.
import argparse, collections, csv, datetime, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]
OUT = os.path.join(HERE, "comments")

# languages and common alternative names viewers write (lower case); value = name used in the summary
LANGS = {}
for line in """Afrikaans|Ainu|Akkadian|Albanian|Amharic|Arabic|Aramaic|Armenian|Assamese|Asturian|Aymara|Azerbaijani,Azeri|Balinese|Balochi|Bambara|Bashkir|Basque,Euskara|
Belarusian|Bemba|Bengali,Bangla|Berber,Amazigh,Tamazight,Kabyle,Tachelhit,Tarifit|Bhojpuri|Bislama|Bosnian|Breton|Bulgarian|Burmese|Burushaski|Buryat|Cantonese|
Catalan|Cebuano|Chamorro|Chechen|Cherokee|Cheyenne|Chichewa,Chewa|Choctaw|Chuvash|Coptic|Cornish|Corsican|Cree|Creole|Croatian|Czech|Dalmatian|Danish|Dari|
Darija,Moroccan|Dutch,Flemish|Dzongkha|Egyptian|English|Esperanto|Estonian|Etruscan|Ewe|Faroese|Fijian|Filipino,Tagalog|Finnish|French|Frisian|Friulian|Fula,Fulani,Pulaar|
Ga|Gaelic|Galician|Ganda,Luganda|Georgian|German|Gothic|Greek|Greenlandic,Kalaallisut|Guarani|Gujarati|Gullah|Haitian|Hakka|Hausa|Hawaiian|Hebrew|Hindi|Hittite|Hmong|
Hokkien,Taiwanese|Hungarian,Magyar|Icelandic|Igbo|Ilocano|Indonesian|Ingush|Interlingua|Inuktitut|Irish|Italian|Japanese|Javanese|Kannada|Kazakh|Khmer,Cambodian|
Khoekhoe,Nama|Kikuyu|Kinyarwanda|Kirundi|Klingon|Korean|Kurdish,Kurmanji,Sorani|Kyrgyz|Ladino|Lakota|Lao|Latin|Latvian|Lingala|Lithuanian|Livonian|Lojban|Luxembourgish|
Macedonian|Malagasy|Malay|Malayalam|Maltese|Manchu|Manx|Maori,Māori|Mapudungun,Mapuche|Marathi|Mayan,K'iche'|Mi'kmaq|Minangkabau|Mohawk|Mongolian|Montenegrin|
Nahuatl|Navajo|Neapolitan|Nepali|Norwegian|Norn|Occitan|Ojibwe|Old English|Old Norse|Oromo|Ossetian|Pashto|Persian,Farsi|Phoenician|Polish|Portuguese|Punjabi|Quechua|
Romani|Romanian|Romansh|Russian|Rusyn|Sami,Saami|Samoan|Sanskrit|Sardinian|Scots|Serbian|Shona|Sicilian|Sindhi|Sinhala|Slovak|Slovene,Slovenian|Somali|Sorbian|Sotho|
Spanish|Sumerian|Sundanese|Swahili|Swedish|Swiss German|Syriac|Tahitian|Tajik|Tamil|Tatar|Telugu|Thai|Tibetan|Tigrinya|Tok Pisin|Toki Pona|Tongan|Tsonga|Tswana|
Turkish|Turkmen|Tuvan|Twi,Akan|Udmurt|Ukrainian|Urdu|Uyghur|Uzbek|Venetian|Vietnamese|Volapük,Volapuk|Walloon|Welsh|Wolof|Xhosa|Yakut,Sakha|Yiddish|Yoruba|Zapotec|Zulu""".replace("\n", "").split("|"):
    names = [n.strip() for n in line.split(",") if n.strip()]
    for n in names:
        LANGS[n.lower()] = names[0]
PAT = re.compile(r"\b(" + "|".join(sorted(map(re.escape, LANGS), key=len, reverse=True)) + r")\b", re.I)
ASK = re.compile(r"\b(do|add|cover|include|make|what about|how about|next|pls|please|plz|part|forgot|missing|where is|where's|you missed)\b", re.I)


def service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    tok = os.path.join(HERE, "youtube_token_read.json")
    creds = Credentials.from_authorized_user_file(tok, SCOPES) if os.path.exists(tok) else None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            secret = os.environ.get("YT_CLIENT_SECRET", os.path.join(HERE, "client_secret.json"))
            creds = InstalledAppFlow.from_client_secrets_file(secret, SCOPES).run_local_server(port=0)
        open(tok, "w").write(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=0, help="only comments newer than this many days (0 = all)")
    a = ap.parse_args()
    since = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=a.days) if a.days else None
    yt = service()
    ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    videos, tok = [], None
    while True:
        r = yt.playlistItems().list(part="snippet", playlistId=uploads, maxResults=50, pageToken=tok).execute()
        videos += [(i["snippet"]["resourceId"]["videoId"], i["snippet"]["title"]) for i in r["items"]]
        tok = r.get("nextPageToken")
        if not tok: break
    rows = []
    for vid, title in videos:
        tok = None
        while True:
            try:
                r = yt.commentThreads().list(part="snippet,replies", videoId=vid, maxResults=100, pageToken=tok, textFormat="plainText").execute()
            except Exception as e:  # comments turned off, etc.
                print(f"  skipped {title}: {str(e)[:80]}")
                break
            for t in r["items"]:
                cs = [t["snippet"]["topLevelComment"]] + t.get("replies", {}).get("comments", [])
                for c in cs:
                    s = c["snippet"]
                    when = datetime.datetime.fromisoformat(s["publishedAt"].replace("Z", "+00:00"))
                    if since and when < since: continue
                    rows.append({"video": title, "date": s["publishedAt"][:10], "likes": s.get("likeCount", 0), "text": s["textDisplay"].replace("\n", " ")})
            tok = r.get("nextPageToken")
            if not tok: break
        print(f"{title}: done")
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "comments.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, ["video", "date", "likes", "text"]); w.writeheader(); w.writerows(rows)
    mention, ask, per_video, examples = collections.Counter(), collections.Counter(), collections.defaultdict(collections.Counter), collections.defaultdict(list)
    for r in rows:
        found = {LANGS[m.lower()] for m in PAT.findall(r["text"])}
        for l in found:
            weight = 1 + int(r["likes"])  # a liked suggestion counts for its likes too
            mention[l] += weight
            per_video[r["video"]][l] += weight
            if ASK.search(r["text"]):
                ask[l] += weight
                if len(examples[l]) < 3: examples[l].append(r["text"][:160])
    lines = [f"LingoDude comments: {len(rows)} comments on {len(videos)} videos" + (f" (last {a.days} days)" if a.days else ""), "",
             "MOST REQUESTED (comment asks to add / cover / do it; likes count too)"]
    lines += [f"{n:5d}  {l}" + (f"   e.g. \"{examples[l][0]}\"" if examples[l] else "") for l, n in ask.most_common(60)]
    lines += ["", "MOST MENTIONED (any mention)"] + [f"{n:5d}  {l}" for l, n in mention.most_common(80)]
    lines += ["", "BY VIDEO (top 8 each)"]
    for v, c in per_video.items():
        lines.append(f"{v}: " + ", ".join(f"{l} {n}" for l, n in c.most_common(8)))
    open(os.path.join(OUT, "summary.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines[:40]))
    print(f"\nSaved {OUT}/summary.txt (send this to Claude) and comments.csv")


if __name__ == "__main__":
    main()
