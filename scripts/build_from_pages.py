"""Stage D: build the six app datasets from the verified per-page transcripts.

Inputs : transcriptions_verbatim/<vol>/page_*.md        (stage A, agy_transcribe.py)
         scripts/page_data/<vol>_sections.json           (stage B, agy_segment.py)
         scripts/page_data/<vol>_enrich/s*.json          (stage C, agy_enrich.py)
Outputs: app/src/data/<dataset>.js  (same export names and shapes the UI already uses, plus a
         `verbatim` field on every concept and `kind` on every scansCatalog entry)

Every transcribed page becomes one concept card whose `verbatim` holds the full handwritten text,
so nothing on the page is dropped. Run from the repo root:  python scripts/build_from_pages.py
"""
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agy_util import ROOT, VOLUMES, WORK_DIR, load_pages  # noqa: E402

DATASETS = {
    "p1_part1": ("paper1IptData", "Paper 1", "Section A & B (Part 1)", "/scans_p1"),
    "p1_part2": ("paper1Part2Data", "Paper 1", "Section B (Part 2)", "/scans_p1_part2"),
    "p1_part4": ("paper1Part4Data", "Paper 1", "Section A & B (Part 4)", "/scans_p1_part4"),
    "p1_part5": ("paper1Part5Data", "Paper 1", "Section A (Part 5)", "/scans_p1_part5"),
    "p2_part1": ("paper2IndiaWorldData", "Paper 2", "Section B (Part 1)", "/scans_p2_part1"),
    "p2_part2": ("paper2ComparativeData", "Paper 2", "Section A (Part 2)", "/scans_p2_part2"),
}
WATERMARK = re.compile(r"^.*(join telegram|t\.me/upsc_pdf|upscpdf\.com).*$\n?", re.I | re.M)
BADGES = {"content": "Handwritten Notes", "index": "Contents Page", "cover": "Cover Page", "diagram": "Diagram Page"}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]


def clean(s):
    return str(s or "").strip()


def short(s, n):
    s = clean(s)
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def as_list(v, limit):
    return [clean(x) for x in (v or []) if clean(x)][:limit]


def fallback_title(d, p):
    """Title for a page without an AI label: its heading, else its first underlined or first real line."""
    if clean(d["heading"]):
        return clean(d["heading"])
    text = re.sub(r"~~.*?~~|\[[^\]]*\]", "", WATERMARK.sub("", d["text"]))  # drop struck-out words, [notes]
    m = re.search(r"__([^_]{4,80})__", text)
    if m:
        return clean(m.group(1)).strip(":-. ")
    for line in text.splitlines():
        line = re.sub(r"^[^A-Za-z]+", "", line).strip()
        if len(line) >= 8 and not line.lower().startswith(("lecture", "page")):
            return short(line, 70)
    return f"Handwritten page {p}"


def legacy_flashcards(name):
    """Old deck for a volume, used only while its AI enrichment is missing. Scan links are dropped
    because the old datasets mapped topics to the wrong pages."""
    f = os.path.join(ROOT, "backup_legacy_data", f"{name}.js")
    if not os.path.exists(f):
        return []
    url = "file:///" + f.replace(os.sep, "/")
    res = subprocess.run(
        ["node", "-e", f"import({json.dumps(url)}).then(m => process.stdout.write(JSON.stringify(m.{name})))"],
        capture_output=True, text=True, encoding="utf-8")
    data = json.loads(res.stdout) if res.returncode == 0 and res.stdout else {}
    out = []
    for i, c in enumerate(data.get("flashcards", []), 1):
        front, back = clean(c.get("front") or c.get("question")), clean(c.get("back") or c.get("answer"))
        if front and back:
            topic = short(c.get("category") or c.get("mnemonic") or "General", 40)
            out.append({"id": i, "front": front, "back": back, "category": topic, "mnemonic": topic,
                        "badge": "Active Recall", "legacy": True})
    return out


def load_enrich(vol, count):
    out = {}
    for i in range(1, count + 1):
        f = os.path.join(WORK_DIR, f"{vol}_enrich", f"s{i:02d}.json")
        out[i] = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {"pages": [], "flashcards": [], "answers": []}
    return out


def notebook_range(pages, start, end):
    nums = []
    for p in range(start, end + 1):
        nb = pages.get(p, {}).get("notebook", "?")
        m = re.match(r"\d+", nb)
        if m:
            nums.append(int(m.group()))
    if not nums:
        return f"Scans {start}–{end}"
    lo, hi = min(nums), max(nums)
    return f"Notebook Page {lo}" if lo == hi else f"Notebook Pages {lo}–{hi}"


def build(vol):
    name, paper, section_name, base = DATASETS[vol]
    n = VOLUMES[vol]["pages"]
    pages = load_pages(vol)
    missing = [p for p in range(1, n + 1) if p not in pages]
    sec_file = os.path.join(WORK_DIR, f"{vol}_sections.json")
    if missing or not os.path.exists(sec_file):
        return vol, f"SKIPPED (missing pages: {len(missing)}, sections file: {os.path.exists(sec_file)})"
    secs = json.load(open(sec_file, encoding="utf-8"))["sections"]
    enrich = load_enrich(vol, len(secs))

    sections, flashcards, answers = [], [], []
    page_title = {}
    fc_id = 1
    for i, s in enumerate(secs, 1):
        start, end = int(s["start"]), int(s["end"])
        e = enrich[i]
        meta_by_page = {int(x["page"]): x for x in e["pages"]}
        concepts = []
        for p in range(start, end + 1):
            d = pages[p]
            m = meta_by_page.get(p, {})
            title = clean(m.get("title")) or fallback_title(d, p)
            page_title[p] = short(title, 90)
            if d["kind"] == "blank" or not d["text"].strip():
                continue
            concepts.append({
                "title": short(title, 110),
                "scanPage": p,
                "badge": BADGES.get(d["kind"], "Handwritten Notes"),
                "summary": clean(m.get("summary")) or short(" ".join(d["text"].split()), 220),
                "details": [],
                "verbatim": WATERMARK.sub("", d["text"]).strip(),
            })
        sec_title = short(s["title"], 100)
        sections.append({
            "id": f"v{VOLUMES[vol]['n']}-{i:02d}-{slug(sec_title)}",
            "number": f"{i:02d}",
            "title": sec_title,
            "subtitle": clean(s.get("subtitle")),
            "scanPages": list(range(start, end + 1)),
            "notebookPages": notebook_range(pages, start, end),
            "lecture": f"Scans {start}–{end}",
            "keyScholars": as_list(s.get("keyScholars"), 8),
            "coreTheories": as_list(s.get("coreTheories"), 5),
            "concepts": concepts,
        })
        for c in e["flashcards"]:
            sp = int(c.get("scanPage") or start)
            flashcards.append({
                "id": fc_id,
                "front": clean(c["front"]),
                "back": clean(c["back"]),
                "category": short(sec_title, 40),
                "mnemonic": short(c.get("category") or sec_title, 40),
                "badge": "Active Recall",
                "scanPage": sp if start <= sp <= end else start,
            })
            fc_id += 1
        for k, a in enumerate(e["answers"], 1):
            sp = int(a.get("scanPage") or start)
            answers.append({
                "id": f"ans-v{VOLUMES[vol]['n']}-{i:02d}-{k}",
                "question": clean(a["question"]),
                "marks": clean(a.get("marks")) or "15 Marks (250 Words)",
                "topic": clean(a.get("topic")) or sec_title,
                "scanPage": sp if start <= sp <= end else start,
                "structure": {
                    "intro": clean(a["intro"]),
                    "body": as_list(a["body"], 8),
                    "scholars": as_list(a.get("scholars"), 10),
                    "conclusion": clean(a["conclusion"]),
                },
            })

    if not flashcards:
        flashcards = legacy_flashcards(name)

    catalog, last_nb = [], 1
    for p in range(1, n + 1):
        m = re.match(r"\d+", pages[p]["notebook"])
        nb = int(m.group()) if m else last_nb
        last_nb = nb
        catalog.append({"page": p, "scanFile": f"page_{p:03d}.png", "notebookPage": nb,
                        "title": page_title.get(p) or f"Page {p}", "kind": pages[p]["kind"]})

    data = {
        "meta": {
            "paper": f"{paper} {section_name}",
            "topicTitle": VOLUMES[vol]["title"],
            "summary": "Page-by-page verbatim transcription of every scan in this volume, grouped by topic: "
                       + " • ".join(s["title"] for s in sections[:14]) + (" • …" if len(sections) > 14 else ""),
            "notebookPages": f"Scans 001–{n:03d} ({n} pages transcribed)",
            "scanStart": 1,
            "scanEnd": n,
            "scanBasePath": base,
        },
        "sections": sections,
        "flashcards": flashcards,
        "answers": answers,
        "scansCatalog": catalog,
    }
    out = os.path.join(ROOT, "app", "src", "data", f"{name}.js")
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"export const {name} = {json.dumps(data, ensure_ascii=False, separators=(',', ':'))};\n")
    concepts_n = sum(len(s["concepts"]) for s in sections)
    return vol, (f"{len(sections)} sections, {concepts_n} page concepts, {len(flashcards)} flashcards, "
                 f"{len(answers)} answers, {os.path.getsize(out) // 1024} KB")


if __name__ == "__main__":
    backup = os.path.join(ROOT, "backup_legacy_data")
    if not os.path.isdir(backup):
        os.makedirs(backup)
        for f in os.listdir(os.path.join(ROOT, "app", "src", "data")):
            if f.endswith(".js"):
                shutil.copy(os.path.join(ROOT, "app", "src", "data", f), backup)
        print("backed up previous datasets to backup_legacy_data/")
    targets = [a for a in sys.argv[1:] if a in VOLUMES] or list(VOLUMES)
    for v in targets:
        print(*build(v))
