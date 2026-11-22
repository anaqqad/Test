def LQ(file, head, key, who, source, before="", after=""):
    return {"type": "LedgerQuote", "file": file, "head": head, "before": before, "key": key, "after": after, "who": who, "source": source}


def HL(kicker, before, accent, at, source, after=""):
    return {"type": "Headline", "kicker": kicker, "before": before, "accent": accent, "after": after, "at": at, "source": source}


def TL(file, head, rows, source):
    return {"type": "LedgerTimeline", "file": file, "head": head, "rows": [{"date": a, "text": b} for a, b in rows], "source": source}


def BARS(file, head, bars, mx, source):
    return {"type": "LedgerBars", "file": file, "head": head, "bars": [{"label": a, "value": b, "figure": c, "note": d} for a, b, c, d in bars], "max": mx, "source": source}


def SLUG(title, sub):
    return {"type": "Slug", "title": title, "subtitle": sub}


def QC(bg, lines, by, by_at, portrait=None):
    c = {"type": "QuoteCard", "bg": bg, "lines": [{"text": a, "at": b} for a, b in lines], "by": by, "byAt": by_at}
    if portrait:
        c["portrait"] = portrait
    return c


def DESK(page, aspect, shots, credit):
    return {"type": "DocDesk", "page": page, "aspect": aspect, "desk": "stills/desk.jpg", "credit": credit,
            "shots": [{"t": t, "kind": k, "args": a} for t, k, a in shots]}


