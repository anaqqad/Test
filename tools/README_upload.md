# Uploading to YouTube (Data API v3, free)

`tools/upload_youtube.py` uploads an episode as **Private** with the title, description (with chapters), tags, category
Education, "made for kids: no", "altered or synthetic content: yes", the custom thumbnail and the English captions. You
then review it in YouTube Studio, add the end screen and pinned comment, and publish by hand.

## One-time setup (owner, ~10 minutes)
1. Go to https://console.cloud.google.com/ and create a project (e.g. "WWII Frontlines uploader").
2. **APIs & Services → Library →** enable **YouTube Data API v3**.
3. **APIs & Services → OAuth consent screen:** User type **External**, app name anything, your email as support and
   developer contact. Under **Test users**, add the Google account that owns the WWII Frontlines channel. Leave it in
   "Testing" (no Google review needed for your own channel).
4. **APIs & Services → Credentials → Create credentials → OAuth client ID →** Application type **Desktop app**.
   Download the JSON.
5. Save it as `C:\Users\<you>\.config\wwii-frontlines\client_secret.json` (outside the repo), or point to it with the
   environment variable `YT_CLIENT_SECRETS`. Never put it in the repo (`.gitignore` blocks `client_secret*.json` and
   `token*.json` anyway).

## Each upload
```
python tools/upload_youtube.py video/<slug> --dry-run     # checks title length, description size, chapters, files
python tools/upload_youtube.py video/<slug>               # uploads as private
```
The first run opens a browser to sign in and pick the channel (choose the WWII Frontlines brand account). The refresh token
is stored next to the client file in `token.json`. In "Testing" mode Google expires it after 7 days, so you may be asked to
sign in again; that is expected.

## Notes
- Quota: 10,000 units/day free. One upload costs about 1,600 units for the video plus 50 for the thumbnail and 400 for the
  captions, so roughly 4–5 uploads a day.
- Custom thumbnails need a phone-verified channel (YouTube Studio → Settings → Channel → Feature eligibility).
- **Important:** YouTube locks every video uploaded through an *unverified* API project (any project created after
  July 2020) to private, and Studio will not let you make it public until the project passes Google's free API compliance
  audit (YouTube API Services audit form, linked from the "videos.insert" docs). Until then the API upload is good for a
  private review copy only; publish by uploading the reviewed file by hand in Studio with `youtube.md`, or apply for the audit.
- To re-send only the thumbnail or captions: `--video-id <id>`.
