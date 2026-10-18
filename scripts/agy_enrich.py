"""Stage C: per-section page titles/summaries, flashcards and model answers, grounded in the transcripts.

Reads transcriptions_verbatim/<vol>/ and scripts/page_data/<vol>_sections.json.
Writes scripts/page_data/<vol>_enrich/s<NN>.json  (one file per section, resumable).
Usage (repo root):  python scripts/agy_enrich.py all --workers 6
"""
import argparse
import concurrent.futures as cf
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agy_util import VOLUMES, WORK_DIR, agy_json, load_pages  # noqa: E402

PAGES_PROMPT = """These are consecutive pages of handwritten UPSC {subject} lecture notes (section: "{section}").
For EACH page below write a short label of what that page covers.
- "title": <= 8 words, naming the topic/thinker/case on that page (index or cover pages: say so, e.g.
  "Contents page: topic list with page numbers").
- "summary": 1-2 sentences, ONLY from what is written on that page. Do not add outside knowledge.
Reply with ONLY: {{"pages":[{{"page":<int>,"title":"","summary":""}}]}} covering exactly pages {first}..{last}
that appear below.

{body}"""

AIDS_PROMPT = """Below are the notes of one section ("{section}") of handwritten UPSC Political Science & IR
lecture notes ({subject}), each page prefixed with its scan page number.

Create study aids STRICTLY grounded in these notes: use only facts, thinkers, cases and examples that appear in
the text below; do not import outside material and do not invent quotations or numbers.

1. "flashcards": {fc} active-recall cards. "front" = a precise exam-style question, "back" = the answer in 1-3
   sentences from the notes, "category" = a 2-4 word sub-topic label, "scanPage" = the page where the answer
   is written.
2. "answers": {na} UPSC Mains model answer outline(s) on this section's most examinable theme. Each:
   "question" (a realistic PSIR Mains question), "marks" ("10 Marks (150 Words)" or
   "15 Marks (250 Words)"), "topic", "scanPage" (main source page),
   "intro" (30-40 words), "body" (3-5 strings, together ~150-170 words, each a distinct analytical point
   naming the thinkers/cases from the notes), "scholars" (3-8 names/works that appear in the notes),
   "conclusion" (30-40 words, balanced and forward-looking).

Reply with ONLY this JSON, no commentary:
{{"flashcards":[{{"front":"","back":"","category":"","scanPage":0}}],
 "answers":[{{"question":"","marks":"","topic":"","scanPage":0,"intro":"","body":[""],"scholars":[""],"conclusion":""}}]}}

NOTES:
{body}"""


def fmt(pages, nums, cap):
    parts = []
    for p in nums:
        d = pages[p]
        parts.append(f"--- PAGE {p} (kind: {d['kind']}) ---\n{d['text'][:cap]}")
    return "\n\n".join(parts)


def check_pages(first, last, present):
    def check(data):
        got = {int(x["page"]) for x in data["pages"]}
        need = set(present)
        assert need <= got, f"missing pages {sorted(need - got)[:6]}"
        for x in data["pages"]:
            assert x["title"].strip() and x["summary"].strip(), f"empty title/summary on page {x['page']}"
    return check


def check_aids(fc_min):
    def check(data):
        assert len(data["flashcards"]) >= fc_min, f"need >= {fc_min} flashcards"
        for c in data["flashcards"]:
            assert c["front"].strip() and c["back"].strip(), "empty flashcard side"
        assert data["answers"], "need at least one answer"
        for a in data["answers"]:
            assert a["question"].strip() and a["intro"].strip() and a["conclusion"].strip(), "empty answer part"
            assert isinstance(a["body"], list) and len(a["body"]) >= 3, "answer body needs >= 3 points"
    return check


def enrich_section(vol, idx, sec, pages, model):
    out_dir = os.path.join(WORK_DIR, f"{vol}_enrich")
    out = os.path.join(out_dir, f"s{idx:02d}.json")
    if os.path.exists(out):
        return vol, idx, "cached"
    subject = VOLUMES[vol]["title"]
    nums = [p for p in range(sec["start"], sec["end"] + 1) if p in pages and pages[p]["kind"] != "blank"]
    if not nums:
        res = {"pages": [], "flashcards": [], "answers": []}
    else:
        page_items = []
        for i in range(0, len(nums), 10):
            chunk = nums[i:i + 10]
            data = agy_json(
                PAGES_PROMPT.format(subject=subject, section=sec["title"], first=chunk[0], last=chunk[-1],
                                    body=fmt(pages, chunk, 3500)),
                model=model, validate=check_pages(chunk[0], chunk[-1], chunk))
            page_items += [x for x in data["pages"] if int(x["page"]) in chunk]
        content_pages = [p for p in nums if pages[p]["kind"] in ("content", "diagram")]
        if len(content_pages) >= 2:
            fc = max(4, min(10, round(len(content_pages) * 0.7)))
            na = 2 if len(content_pages) >= 10 else 1
            aids = agy_json(
                AIDS_PROMPT.format(section=sec["title"], subject=subject, fc=fc, na=na,
                                   body=fmt(pages, content_pages, 2600)),
                model=model, validate=check_aids(min(3, fc)))
        else:
            aids = {"flashcards": [], "answers": []}
        res = {"pages": page_items, "flashcards": aids["flashcards"], "answers": aids["answers"]}
    os.makedirs(out_dir, exist_ok=True)
    json.dump(res, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return vol, idx, f"{len(res['pages'])} pages, {len(res['flashcards'])} cards, {len(res['answers'])} answers"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("volume")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--model", default="gemini-3.8-flash-high")
    a = ap.parse_args()
    vols = list(VOLUMES) if a.volume == "all" else [a.volume]
    jobs = []
    for v in vols:
        sec_file = os.path.join(WORK_DIR, f"{v}_sections.json")
        if not os.path.exists(sec_file):
            print(f"{v}: no sections file yet, run agy_segment.py first")
            continue
        pages = load_pages(v)
        for i, s in enumerate(json.load(open(sec_file, encoding="utf-8"))["sections"], 1):
            jobs.append((v, i, s, pages))
    print(f"{len(jobs)} sections to enrich", flush=True)
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(enrich_section, v, i, s, pg, a.model) for v, i, s, pg in jobs]
        for n, fut in enumerate(cf.as_completed(futs), 1):
            try:
                v, i, msg = fut.result()
                print(f"[{n}/{len(jobs)}] {v} s{i:02d}: {msg}", flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"[{n}/{len(jobs)}] FAILED: {e}", flush=True)
