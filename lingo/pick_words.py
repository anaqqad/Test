"""Find Lingua Libre recordings of chosen everyday words (hello, thank you, water...) per ranking language."""
import json, time
import fetch_audio as fa
WORDS = {
 "nor": ["takk", "hei", "vann", "venn", "kjærlighet", "god morgen"],
 "spa": ["hola", "gracias", "agua", "amigo", "corazón", "mañana"],
 "nld": ["dank je", "hallo", "water", "vriend", "fiets", "gezellig"],
 "ita": ["ciao", "grazie", "acqua", "amico", "bellissimo", "buongiorno"],
 "fra": ["bonjour", "merci", "eau", "ami", "écureuil", "grenouille"],
 "ind": ["terima kasih", "halo", "air", "teman", "selamat pagi", "cinta"],
 "deu": ["danke", "hallo", "Wasser", "Freund", "Eichhörnchen", "Brötchen"],
 "rus": ["спасибо", "привет", "вода", "друг", "здравствуйте", "любовь"],
 "hin": ["नमस्ते", "धन्यवाद", "पानी", "दोस्त", "प्यार", "किताब"],
 "pol": ["dziękuję", "cześć", "woda", "przyjaciel", "chrząszcz", "dzień dobry"],
 "fin": ["kiitos", "hei", "vesi", "ystävä", "rakkaus", "sauna"],
 "hun": ["köszönöm", "szia", "víz", "barát", "szerelem", "egészségedre"],
 "vie": ["xin chào", "cảm ơn", "nước", "bạn", "phở", "ma"],
 "kor": ["안녕하세요", "감사합니다", "물", "친구", "사랑", "김치"],
 "ara": ["مرحبا", "شكرا", "ماء", "صديق", "حب", "سلام"],
 "cmn": ["你好", "谢谢", "水", "朋友", "爱", "中国"],
 "jpn": ["こんにちは", "ありがとう", "水", "友達", "愛", "猫"],
}
res = {}
for code, words in WORDS.items():
    got = []
    for w in words:
        d = fa.api(action="query", list="search", srsearch=f'intitle:"({code})" intitle:"{w}" LL', srnamespace=6, srlimit=20)
        for h in d["query"]["search"]:
            if h["title"].startswith("File:LL-") and fa.ll_word(h["title"]).lower() == w.lower():
                got.append(h["title"]); break
        if len(got) >= 3: break
        time.sleep(0.3)
    res[code] = got
    print(code, [fa.ll_word(t) for t in got], flush=True)
json.dump(res, open("cache/ranking_words.json", "w"), ensure_ascii=False, indent=1)
