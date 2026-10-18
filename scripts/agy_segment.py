"""Stage B: group a volume's transcribed pages into contiguous topic sections using agy.

Reads transcriptions_verbatim/<vol>/page_*.md, writes scripts/page_data/<vol>_sections.json.
Usage (repo root):  python scripts/agy_segment.py all --workers 3
"""
import argparse
import concurrent.futures as cf
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agy_util import VOLUMES, WORK_DIR, agy_json, load_pages  # noqa: E402

PROMPT = """Below are the {n} consecutive pages (1..{n}) of one volume of handwritten UPSC Political Science & IR
lecture notes: "{title}". For every page you get: page number, page kind, notebook page, heading, and
the first words of its text.

Group ALL pages into thematic SECTIONS, the way a syllabus table of contents would. Rules:
- Sections are contiguous page ranges, in order, together covering page 1 to page {n} exactly once (no gaps,
  no overlaps). Aim for {lo}-{hi} sections; a section is normally 4-15 pages but may be shorter/longer if the
  topic really is.
- Cut where the TOPIC actually changes (a new thinker, doctrine, institution, bilateral relationship,
  case, debate), using the headings and text. Do NOT cut into equal-size chunks.
- Index/cover/blank pages at the start belong to a first section titled "Contents & Front Matter".
- For each section give: "title" (<= 10 words), "subtitle" (3-6 sub-topics separated by " | "), "start", "end",
  "keyScholars" (<= 8 names that really appear in those pages), "coreTheories" (<= 5 doctrines/concepts
  that really appear in those pages).
Reply with ONLY this JSON, no commentary:
{{"sections":[{{"title":"","subtitle":"","start":1,"end":5,"keyScholars":[],"coreTheories":[]}}]}}

PAGES:
{listing}"""


def listing(pages, n):
    rows = []
    for p in range(1, n + 1):
        d = pages.get(p)
        if not d:
            rows.append(f"p{p} | MISSING")
            continue
        first = " ".join(d["text"].split())[:170]
        rows.append(f"p{p} | {d['kind']} | nb {d['notebook']} | {d['heading'][:60]} | {first}")
    return "\n".join(rows)


def validator(n):
    def check(data):
        secs = data["sections"]
        assert secs, "empty sections"
        expect = 1
        for s in secs:
            assert int(s["start"]) == expect, f"section '{s.get('title')}' starts at {s['start']}, expected {expect}"
            assert int(s["end"]) >= int(s["start"]), f"section '{s.get('title')}' ends before it starts"
            expect = int(s["end"]) + 1
        assert expect == n + 1, f"sections stop at page {expect - 1}, must reach {n}"
    return check


def segment(vol, model):
    n = VOLUMES[vol]["pages"]
    pages = load_pages(vol)
    missing = [p for p in range(1, n + 1) if p not in pages]
    if missing:
        return vol, f"SKIPPED: {len(missing)} pages not transcribed yet (e.g. {missing[:5]})"
    out = os.path.join(WORK_DIR, f"{vol}_sections.json")
    if os.path.exists(out):
        return vol, "already segmented"
    prompt = PROMPT.format(n=n, title=VOLUMES[vol]["title"], lo=max(10, n // 18), hi=max(16, n // 8),
                           listing=listing(pages, n))
    data = agy_json(prompt, model=model, validate=validator(n))
    os.makedirs(WORK_DIR, exist_ok=True)
    json.dump(data, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return vol, f"{len(data['sections'])} sections"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("volume")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--model", default="gemini-3.8-flash-high")
    a = ap.parse_args()
    vols = list(VOLUMES) if a.volume == "all" else [a.volume]
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        for fut in cf.as_completed([ex.submit(segment, v, a.model) for v in vols]):
            try:
                print(*fut.result(), flush=True)
            except Exception as e:  # noqa: BLE001
                print("FAILED:", e, flush=True)
