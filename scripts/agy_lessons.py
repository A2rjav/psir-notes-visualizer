"""Write a short, narrated, animated lesson script for every topic (BYJU'S-style), grounded in the notes.

Reads  transcriptions_verbatim/<vol>/page_*.md, scripts/page_data/<vol>_sections.json and
       scripts/page_data/<vol>_enrich/sNN.json (page titles and summaries).
Writes scripts/page_data/<vol>_lessons/sNN.json (resumable; front-matter sections are skipped).
The app's LessonPlayer turns each scene into a motion-graphics scene with voice-over.

Usage (repo root):  python scripts/agy_lessons.py all --workers 6 [--model gemini-3.8-flash-high]
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agy_util import VOLUMES, WORK_DIR, agy_json, load_pages  # noqa: E402

SCENE_TYPES = {
    "hook": "a big question or surprising fact that makes the student curious. Fields: text (max 14 words)",
    "analogy": "an everyday Indian-student analogy (cricket, school, family, a housing society, a WhatsApp group...) "
               "that makes the idea click. Fields: emoji (1 emoji), text (max 16 words). Mark it clearly as an analogy in the narration",
    "points": "2-5 key points that appear one by one. Fields: heading (max 6 words), items (each max 10 words)",
    "thinker": "one thinker named in the notes. Fields: name, idea (max 14 words), work (book/year if in the notes, else empty)",
    "compare": "2 or 3 columns compared side by side. Fields: heading, columns: [{title, items: [max 3, each max 8 words]}]",
    "timeline": "events in order. Fields: heading, events: [{when (year/period from the notes), what (max 8 words)}] (3-6 events)",
    "cycle": "a loop of 3-5 stages that feed back into each other. Fields: heading, nodes (each max 3 words)",
    "flow": "a chain where one thing leads to the next. Fields: heading, steps (3-5, each max 6 words)",
    "rings": "concentric circles from the centre outwards. Fields: heading, rings: [{label (max 3 words), tone: self|enemy|friend|neutral}] (3-6 rings, first is the centre)",
    "matrix": "a 2x2 grid (choices/payoffs/types). Fields: heading, rows (2 labels), cols (2 labels), cells (2x2 strings, max 6 words each), highlight ([row, col] of the key cell)",
    "pyramid": "levels from top to bottom (hierarchy, base and superstructure, core-periphery). Fields: heading, levels (3-4, top first, max 4 words)",
    "balance": "two sides weighed against each other. Fields: heading, left (max 4 words), right (max 4 words), tilt: left|right|even",
    "quote": "a line quoted in the notes (only if the notes quote it). Fields: quote (max 25 words), by",
    "recap": "the 3 things to remember. Fields: items (exactly 3, each max 10 words)",
}

PROMPT = """You are a brilliant, warm teacher making a short animated video lesson (like BYJU'S) for a student
who finds UPSC PSIR (Political Science & IR) hard. Topic: "{title}" ({subtitle}).
Volume: {volume}.

Write the lesson as 6-9 scenes. Each scene has a "type", the on-screen fields for that type, and
"narration": what the narrator says while the scene animates (1-3 short spoken sentences, simple English a
class 10 student understands, friendly, second person: "Imagine...", "Here's the trick...").

Scene types you can use (pick what explains THIS topic best; do not use every type):
{types}

Rules:
- Start with "hook", then usually an "analogy". End with "recap". Use at least two motion-graphic types
  (compare, timeline, cycle, flow, rings, matrix, pyramid, balance) where the content really has that shape.
- Every fact, name, date, case or quote must come from the notes below. Analogies are your own, but must be
  clearly analogies. Never invent quotations, statistics or dates. Do not use Hindi.
- Total narration 170-260 words (about 1.5-2 minutes spoken). Keep on-screen text much shorter than narration.
- Use plain words. Explain any technical term the first time you use it.

Reply with ONLY this JSON (no commentary):
{{"title": "lesson title, max 8 words", "scenes": [{{"type": "hook", "text": "...", "narration": "..."}}]}}

NOTES FOR THIS TOPIC (page summaries first, then the handwritten text):
{body}"""

REQUIRED = {
    "hook": ["text"], "analogy": ["text"], "points": ["heading", "items"], "thinker": ["name", "idea"],
    "compare": ["heading", "columns"], "timeline": ["heading", "events"], "cycle": ["heading", "nodes"],
    "flow": ["heading", "steps"], "rings": ["heading", "rings"], "matrix": ["heading", "rows", "cols", "cells"],
    "pyramid": ["heading", "levels"], "balance": ["heading", "left", "right"], "quote": ["quote", "by"],
    "recap": ["items"],
}
DEVANAGARI = re.compile(r"[ऀ-ॿ]")


def validate(data):
    scenes = data.get("scenes")
    assert isinstance(scenes, list) and 5 <= len(scenes) <= 11, "need 6-9 scenes"
    assert scenes[0].get("type") == "hook", "first scene must be hook"
    assert scenes[-1].get("type") == "recap", "last scene must be recap"
    words = 0
    graphics = 0
    for s in scenes:
        t = s.get("type")
        assert t in REQUIRED, f"unknown scene type {t}"
        for f in REQUIRED[t]:
            assert s.get(f) not in (None, "", []), f"{t} scene missing {f}"
        assert str(s.get("narration", "")).strip(), f"{t} scene has no narration"
        words += len(str(s["narration"]).split())
        graphics += t in ("compare", "timeline", "cycle", "flow", "rings", "matrix", "pyramid", "balance")
        if t == "matrix":
            assert len(s["rows"]) == 2 and len(s["cols"]) == 2 and len(s["cells"]) == 2 and all(len(r) == 2 for r in s["cells"]), "matrix must be 2x2"
        if t == "recap":
            assert len(s["items"]) == 3, "recap needs exactly 3 items"
    assert 140 <= words <= 320, f"narration is {words} words, want 170-260"
    assert graphics >= 1, "use at least one motion-graphic scene"
    assert not DEVANAGARI.search(json.dumps(data, ensure_ascii=False)), "English only"


def body_for(vol, sec, pages, enrich):
    meta = {int(x["page"]): x for x in enrich.get("pages", [])}
    parts = []
    for p in range(int(sec["start"]), int(sec["end"]) + 1):
        if p in meta:
            parts.append(f"[p{p}] {meta[p]['title']}: {meta[p]['summary']}")
    parts.append("")
    for p in range(int(sec["start"]), int(sec["end"]) + 1):
        d = pages.get(p)
        if d and d["kind"] in ("content", "diagram"):
            parts.append(f"--- page {p} ---\n{d['text'][:1400]}")
    return "\n".join(parts)


def make(vol, idx, sec, pages, model):
    out = os.path.join(WORK_DIR, f"{vol}_lessons", f"s{idx:02d}.json")
    if os.path.exists(out):
        return vol, idx, "cached"
    ef = os.path.join(WORK_DIR, f"{vol}_enrich", f"s{idx:02d}.json")
    enrich = json.load(open(ef, encoding="utf-8")) if os.path.exists(ef) else {}
    prompt = PROMPT.format(
        title=sec["title"], subtitle=sec.get("subtitle", ""), volume=VOLUMES[vol]["title"],
        types="\n".join(f"- {k}: {v}" for k, v in SCENE_TYPES.items()), body=body_for(vol, sec, pages, enrich))
    data = agy_json(prompt, model=model, validate=validate)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(data, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return vol, idx, f"{len(data['scenes'])} scenes"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("volume")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--model", default="gemini-3.8-flash-high")
    a = ap.parse_args()
    vols = list(VOLUMES) if a.volume == "all" else [a.volume]
    jobs = []
    for v in vols:
        pages = load_pages(v)
        secs = json.load(open(os.path.join(WORK_DIR, f"{v}_sections.json"), encoding="utf-8"))["sections"]
        for i, s in enumerate(secs, 1):
            if re.search(r"^contents\b|front matter", s["title"], re.I):
                continue
            jobs.append((v, i, s, pages))
    print(f"{len(jobs)} lessons to write", flush=True)
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(make, v, i, s, pg, a.model) for v, i, s, pg in jobs]
        for n, fut in enumerate(cf.as_completed(futs), 1):
            try:
                v, i, msg = fut.result()
                print(f"[{n}/{len(jobs)}] {v} s{i:02d}: {msg}", flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"[{n}/{len(jobs)}] FAILED: {str(e)[:200]}", flush=True)
