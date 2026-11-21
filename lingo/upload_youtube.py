# Upload a finished video to the LingoDude YouTube channel with the metadata in meta/<key>.md.
#   python upload_youtube.py easy videos/ranking_easiest_languages.mp4 [--public] [--dry-run]
# Title, description, tags, category, "made for kids" and thumbnail are read from meta/<key>.md.
# One-time setup (see README section "Uploading to YouTube"): a Google Cloud OAuth client of type "Desktop app" with the
# YouTube Data API v3 enabled, saved as client_secret.json next to this script (or path in YT_CLIENT_SECRET).
# The first run opens the browser to sign in to the channel; the token is kept in youtube_token.json (never commit
# either file: both are in .gitignore). Default privacy is private, so you can check it in YouTube Studio first.
import argparse, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]
CATEGORY = {"Education": "27", "Entertainment": "24", "People & Blogs": "22"}


def read_meta(key):
    t = open(os.path.join(HERE, "meta", key + ".md"), encoding="utf-8").read()
    sec = dict(re.findall(r"^## (.+?)\n(.*?)(?=^## |\Z)", t, re.S | re.M))
    title = sec["Title"].strip().splitlines()[0]
    desc = sec["Description"].strip()
    tags = [x.strip() for x in sec.get("Tags", "").replace("\n", ",").split(",") if x.strip()]
    st = sec.get("Settings", "")
    cat = (re.search(r"Category:\s*(.+)", st) or [None, "Education"])[1].strip()
    kids = "yes" in ((re.search(r"Made for kids:\s*(\w+)", st) or [None, "No"])[1].lower())
    synthetic = (re.search(r"Altered or synthetic content:\s*(\w+)", st) or [None, "No"])[1].lower().startswith("yes")
    thumb = re.search(r"Thumbnail:\s*(?:lingo/)?(\S+\.(?:png|jpg))", st)
    if len(title) > 100: sys.exit(f"title is {len(title)} characters; YouTube allows 100")
    if len(desc) > 5000: sys.exit(f"description is {len(desc)} characters; YouTube allows 5000")
    if re.search(r"[<>]", desc + title): sys.exit("YouTube rejects < and > in the title or description")
    return {"title": title, "description": desc, "tags": tags, "categoryId": CATEGORY.get(cat, "27"), "kids": kids,
            "synthetic": synthetic, "thumbnail": os.path.join(HERE, thumb.group(1)) if thumb else None}


def service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    tok = os.path.join(HERE, "youtube_token.json")
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
    ap.add_argument("key", help="metadata file meta/<key>.md")
    ap.add_argument("video", help="path to the mp4")
    ap.add_argument("--public", action="store_true", help="publish immediately instead of private")
    ap.add_argument("--dry-run", action="store_true", help="only show what would be uploaded")
    a = ap.parse_args()
    m = read_meta(a.key)
    print(f"title: {m['title']}\ntags: {len(m['tags'])}, description: {len(m['description'])} chars, category {m['categoryId']}, "
          f"made for kids: {m['kids']}, synthetic: {m['synthetic']}, thumbnail: {m['thumbnail']}")
    if a.dry_run: return
    from googleapiclient.http import MediaFileUpload
    yt = service()
    body = {"snippet": {"title": m["title"], "description": m["description"], "tags": m["tags"], "categoryId": m["categoryId"],
                        "defaultLanguage": "en", "defaultAudioLanguage": "en"},
            "status": {"privacyStatus": "public" if a.public else "private", "selfDeclaredMadeForKids": m["kids"],
                       "containsSyntheticMedia": m["synthetic"]}}
    req = yt.videos().insert(part="snippet,status", body=body, media_body=MediaFileUpload(a.video, chunksize=8 * 1024 * 1024, resumable=True))
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status: print(f"  uploaded {int(status.progress() * 100)}%", flush=True)
    vid = resp["id"]
    print(f"done: https://youtu.be/{vid} ({body['status']['privacyStatus']})")
    if m["thumbnail"] and os.path.exists(m["thumbnail"]):
        yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(m["thumbnail"])).execute()
        print("thumbnail set (needs a verified channel: YouTube Studio > Settings > Channel > Feature eligibility)")


if __name__ == "__main__":
    main()
