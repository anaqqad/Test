"""Upload a finished episode to YouTube as PRIVATE, with its title, description, tags, thumbnail and captions.

Reads everything from the episode folder:
  youtube.md            "## Title" (first ``` block), "## Description" (up to the next "## "), "## Tags" (comma list)
  out/<slug>.mp4        the video (or pass --video)
  out/<slug>.srt        English captions, if present
  thumbnail/thumbnail_A.jpg   custom thumbnail, if present (or pass --thumb)

Secrets never live in the repo. The OAuth client (a "Desktop app" client from Google Cloud Console, YouTube Data API v3
enabled) is read from $YT_CLIENT_SECRETS, default ~/.config/wwii-frontlines/client_secret.json. The refresh token is
cached next to it in token.json. Nothing secret is printed.

Usage:
  python tools/upload_youtube.py video/interrogation-sukiyaki --dry-run    # parse and check metadata only
  python tools/upload_youtube.py video/interrogation-sukiyaki              # upload as private
  python tools/upload_youtube.py video/<slug> --video-id <id>              # re-send thumbnail/captions to an existing upload
"""
import argparse, json, os, re, sys, time
from pathlib import Path

CONF = Path(os.environ.get("YT_CONFIG_DIR", Path.home() / ".config/wwii-frontlines"))
SECRETS = Path(os.environ.get("YT_CLIENT_SECRETS", CONF / "client_secret.json"))
TOKEN = Path(os.environ.get("YT_TOKEN", CONF / "token.json"))
# upload = videos.insert + thumbnails.set; force-ssl = captions.insert
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl"]
API = "https://www.googleapis.com"
CHUNK = 16 * 1024 * 1024


def section(md, name):
    m = re.search(rf"^## {re.escape(name)}\s*\n(.*?)(?=^## |\Z)", md, re.S | re.M)
    return m.group(1).strip() if m else ""


def metadata(ep):
    md = (ep / "youtube.md").read_text(encoding="utf-8")
    t = re.search(r"```\s*\n(.*?)\n```", section(md, "Title"), re.S)
    title = (t.group(1) if t else section(md, "Title").splitlines()[0]).strip()
    desc = section(md, "Description")
    tags = [x.strip() for x in section(md, "Tags").replace("\n", " ").split(",") if x.strip()]
    problems = []
    if len(title) > 100: problems.append(f"title is {len(title)} chars (max 100)")
    if "<" in title or ">" in title or "<" in desc or ">" in desc: problems.append("title/description may not contain < or >")
    if len(desc.encode("utf-8")) > 5000: problems.append(f"description is {len(desc.encode('utf-8'))} bytes (max 5000)")
    if sum(len(x) + (2 if " " in x else 0) for x in tags) + len(tags) - 1 > 500: problems.append("tags exceed 500 characters")
    if not re.search(r"^0:00 ", desc, re.M): problems.append("no chapter list starting at 0:00 in the description")
    if "PLACEHOLDER" in desc or "TODO" in desc: problems.append("description still has a placeholder")
    return title, desc, tags, problems


def session():
    from google.auth.transport.requests import AuthorizedSession, Request
    from google.oauth2.credentials import Credentials
    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES) if TOKEN.exists() else None
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        if not SECRETS.exists():
            raise SystemExit(f"OAuth client not found at {SECRETS}. Download it from Google Cloud Console "
                             "(APIs & Services > Credentials > OAuth client ID > Desktop app) and save it there, "
                             "or set YT_CLIENT_SECRETS.")
        from google_auth_oauthlib.flow import InstalledAppFlow
        creds = InstalledAppFlow.from_client_secrets_file(str(SECRETS), SCOPES).run_local_server(port=0, prompt="consent")
    TOKEN.parent.mkdir(parents=True, exist_ok=True)
    TOKEN.write_text(creds.to_json(), encoding="utf-8")
    try: os.chmod(TOKEN, 0o600)
    except OSError: pass
    return AuthorizedSession(creds)


def check(r, what):
    if r.status_code >= 400:
        try: msg = r.json()["error"]["message"]
        except Exception: msg = r.text[:500]
        raise SystemExit(f"{what} failed ({r.status_code}): {msg}")
    return r


def upload_video(s, path, body):
    size = path.stat().st_size
    r = check(s.post(f"{API}/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                     json=body, headers={"X-Upload-Content-Length": str(size), "X-Upload-Content-Type": "video/mp4"}), "start upload")
    url, pos, fails = r.headers["Location"], 0, 0
    with open(path, "rb") as f:
        while True:
            f.seek(pos); data = f.read(CHUNK)
            try:
                r = s.put(url, data=data, headers={"Content-Range": f"bytes {pos}-{pos + len(data) - 1}/{size}"}, timeout=300)
                if r.status_code >= 500: raise IOError(f"HTTP {r.status_code}")
            except IOError as e:  # network errors (requests' exceptions are IOErrors) and 5xx: ask the server where it got to
                fails += 1
                if fails > 6: raise SystemExit(f"upload failed repeatedly ({e}); run again to start over")
                time.sleep(2 ** fails)
                r = s.put(url, headers={"Content-Range": f"bytes */{size}"}, timeout=60)
            if r.status_code in (200, 201):
                print("\rupload 100%     "); return r.json()["id"]
            if r.status_code != 308: check(r, "upload chunk")
            pos = int(r.headers["Range"].split("-")[1]) + 1 if "Range" in r.headers else 0
            print(f"\rupload {pos * 100 // size}%", end="", flush=True)


def set_thumbnail(s, vid, path):
    ctype = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    if path.stat().st_size > 2 * 1024 * 1024: print("WARNING: thumbnail over 2 MB, YouTube will reject it")
    check(s.post(f"{API}/upload/youtube/v3/thumbnails/set?videoId={vid}&uploadType=media", data=path.read_bytes(),
                 headers={"Content-Type": ctype}), "thumbnail (custom thumbnails need a phone-verified channel)")
    print("thumbnail set:", path.name)


def add_captions(s, vid, path):
    meta = json.dumps({"snippet": {"videoId": vid, "language": "en", "name": "English", "isDraft": False}})
    b = "wwiif" + str(int(time.time()))
    body = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{meta}\r\n"
            f"--{b}\r\nContent-Type: application/octet-stream\r\n\r\n").encode() + path.read_bytes() + f"\r\n--{b}--\r\n".encode()
    check(s.post(f"{API}/upload/youtube/v3/captions?part=snippet&uploadType=multipart", data=body,
                 headers={"Content-Type": f"multipart/related; boundary={b}"}), "captions")
    print("captions added:", path.name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", type=Path)
    ap.add_argument("--video", type=Path); ap.add_argument("--thumb", type=Path); ap.add_argument("--srt", type=Path)
    ap.add_argument("--video-id", help="skip the video upload and only set thumbnail/captions on this video")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    ep, slug = a.episode.resolve(), a.episode.resolve().name
    video = a.video or ep / f"out/{slug}.mp4"
    thumb = a.thumb or ep / "thumbnail/thumbnail_A.jpg"
    srt = a.srt or ep / f"out/{slug}.srt"
    title, desc, tags, problems = metadata(ep)
    print(f"title ({len(title)}): {title}\ntags: {len(tags)}\ndescription: {len(desc)} chars")
    print("video:", video, "OK" if video.exists() else "MISSING")
    print("thumbnail:", thumb if thumb.exists() else "none")
    print("captions:", srt if srt.exists() else "none")
    for p in problems: print("PROBLEM:", p)
    if a.dry_run: return
    if problems: raise SystemExit("fix the problems above first")
    s = session()
    vid = a.video_id
    if not vid:
        if not video.exists(): raise SystemExit(f"no video at {video}")
        body = {"snippet": {"title": title, "description": desc, "tags": tags, "categoryId": "27",  # Education
                            "defaultLanguage": "en", "defaultAudioLanguage": "en"},
                "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False,
                           "containsSyntheticMedia": True,  # AI narration and AI thumbnail (altered or synthetic content)
                           "embeddable": True, "license": "youtube"}}
        vid = upload_video(s, video, body)
    print(f"video id: {vid} (private)  https://studio.youtube.com/video/{vid}/edit")
    if thumb.exists(): set_thumbnail(s, vid, thumb)
    if srt.exists(): add_captions(s, vid, srt)
    print("Done. Review it in YouTube Studio, add the end screen and pinned comment, then publish.")


if __name__ == "__main__":
    main()
