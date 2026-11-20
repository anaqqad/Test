# The Five-Second Rule

**Origin:** Owner's rule for Malta v4; enforced by `longform4.mjs`.

**When to use:** Every long-form edit. No shot stays on screen longer than 5 s; one idea may run across several shots.

**How to build (`lingo/longform4.mjs`):**
Write `shots` per line; the renderer splits the line's time and prints the longest shot, writing `cache/longform/<key>/shots_<tag>.json`. A new shot must give something new to look at: a different angle, an action, new evidence or a new composition (a slow zoom, a new date or a caption on the same image does not count). Alternate quick accents (1–2 s) with calmer 4–5 s shots; keep quotes and translations in place across cuts; keep labels and colours identical across map and table cuts.

**Pitfalls:** Check the actual render too: scene detection on the MP4 (see `lingo/longform_qa.py`).

**Used in Malta v4:** {{TS4:s4b}}
