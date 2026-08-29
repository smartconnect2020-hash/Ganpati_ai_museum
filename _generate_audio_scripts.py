"""Generate a recording script (verbatim from data.json's guide) for every
item that doesn't have real audio yet. Same format already used for item-003,
now applied to all remaining items so recording has zero prep friction."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "audio-scripts"
OUT.mkdir(exist_ok=True)

d = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))

# item-001 already has a real recording; skip it. Everyone else still has a
# placeholder audio-mr.mp3 and needs a script.
SKIP_IDS = {"001"}


def slugify(mr_title: str) -> str:
    # keep it simple/ascii for the filename; content stays Marathi
    table = str.maketrans("", "", "()/'\"")
    return mr_title.translate(table).strip().split()[0]


def build_script(item: dict) -> str:
    g = item["guide"]["mr"]
    iid = item["id"]
    s = g["sections"]
    L = []
    A = L.append

    A(f"# {g['docTitle']} — रेकॉर्डिंग स्क्रिप्ट")
    A("")
    A(f"**फाइल कुठे ठेवायची:** `media/item-{iid}/audio-mr.mp3`  ")
    A(f"**अंदाजे वेळ:** ~{item['duration_sec']} सेकंद (`data.json` मध्ये `duration_sec` आधीच सेट आहे — खरं रेकॉर्डिंग झाल्यावर पडताळा)")
    A("")
    A("> मजकूर मूळ गाईड ग्रंथातून **जसाच्या तसा** घेतला आहे — एकही शब्द बदललेला नाही.  ")
    A("> `[SFX]` आणि `(पार्श्वभूमी ध्वनी...)` या ओळी **वाचायच्या नाहीत** — त्या ध्वनी-संयोजकासाठीच्या सूचना आहेत.")
    A("")
    A("---")
    A("")
    A("### 🔊 ध्वनी सूचना")
    A(f"> {s[0]['sfx']}")
    A("")
    A("### 🎙 वाचा")
    A("")
    A(g["intro"])
    A("")
    for p in s[0]["paras"]:
        A(p)
        A("")
    A(s[0]["sources"])
    A("")
    A("---")
    A("")
    A("### 🔊 ध्वनी सूचना")
    A(f"> {s[1]['sfx']}")
    A("")
    A("### 🎙 वाचा")
    A("")
    for p in s[1]["paras"]:
        A(p)
        A("")
    A(g["darshanik"])
    A("")
    A(g["nextGuide"])
    A("")
    A("---")
    A("")
    A("### 🔊 समाप्ती ध्वनी")
    A(f"> {g['outro']}")
    A("")
    return "\n".join(L)


count = 0
for item in d["items"]:
    if item["id"] in SKIP_IDS:
        continue
    fname = f"item-{item['id']}-{slugify(item['title']['mr'])}-mr.md"
    (OUT / fname).write_text(build_script(item), encoding="utf-8")
    count += 1

print(f"Wrote {count} recording scripts to {OUT}")
