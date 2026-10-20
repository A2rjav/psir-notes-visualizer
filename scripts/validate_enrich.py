"""Check every section's enrichment file against ENRICH_BRIEF.md before the dataset build.

Usage (repo root):  python scripts/validate_enrich.py [vol ...]
Prints one line per problem and a per-volume summary; exit code 1 if any file is missing or malformed.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agy_util import VOLUMES, WORK_DIR, load_pages  # noqa: E402

DEVANAGARI = re.compile(r"[ऀ-ॿ]")


def words(s):
    return len(str(s).split())


def check(vol):
    problems, totals = [], {"sections": 0, "pages": 0, "flashcards": 0, "answers": 0}
    pages = load_pages(vol)
    secs = json.load(open(os.path.join(WORK_DIR, f"{vol}_sections.json"), encoding="utf-8"))["sections"]
    for i, s in enumerate(secs, 1):
        f = os.path.join(WORK_DIR, f"{vol}_enrich", f"s{i:02d}.json")
        tag = f"{vol} s{i:02d}"
        if not os.path.exists(f):
            problems.append(f"{tag}: MISSING")
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except json.JSONDecodeError as e:
            problems.append(f"{tag}: invalid JSON ({e})")
            continue
        lo, hi = int(s["start"]), int(s["end"])
        nonblank = [p for p in range(lo, hi + 1) if p in pages and pages[p]["kind"] != "blank"]
        content = [p for p in nonblank if pages[p]["kind"] in ("content", "diagram")]
        got = {int(x.get("page", -1)) for x in d.get("pages", [])}
        if set(nonblank) - got:
            problems.append(f"{tag}: pages without title/summary {sorted(set(nonblank) - got)[:8]}")
        for x in d.get("pages", []):
            if not str(x.get("title", "")).strip() or not str(x.get("summary", "")).strip():
                problems.append(f"{tag}: empty title/summary on page {x.get('page')}")
        fcs, ans = d.get("flashcards", []), d.get("answers", [])
        if len(content) >= 2:
            want_fc = max(4, min(10, round(0.7 * len(content))))
            if len(fcs) < min(3, want_fc):
                problems.append(f"{tag}: only {len(fcs)} flashcards (want ~{want_fc})")
            if not ans:
                problems.append(f"{tag}: no model answer")
        for c in fcs:
            if not str(c.get("front", "")).strip() or not str(c.get("back", "")).strip():
                problems.append(f"{tag}: empty flashcard side")
            sp = c.get("scanPage")
            if not isinstance(sp, int) or not lo <= sp <= hi:
                problems.append(f"{tag}: flashcard scanPage {sp} outside {lo}-{hi}")
        for a in ans:
            for k in ("question", "intro", "conclusion"):
                if not str(a.get(k, "")).strip():
                    problems.append(f"{tag}: answer missing {k}")
            body = a.get("body")
            if not isinstance(body, list) or not 3 <= len(body) <= 6:
                problems.append(f"{tag}: answer body has {len(body) if isinstance(body, list) else 'no'} points")
            elif not 90 <= sum(words(b) for b in body) <= 260:
                problems.append(f"{tag}: answer body is {sum(words(b) for b in body)} words (want ~150-170)")
            sp = a.get("scanPage")
            if not isinstance(sp, int) or not lo <= sp <= hi:
                problems.append(f"{tag}: answer scanPage {sp} outside {lo}-{hi}")
        if DEVANAGARI.search(json.dumps(d, ensure_ascii=False)):
            problems.append(f"{tag}: contains Devanagari text (English only)")
        totals["sections"] += 1
        totals["pages"] += len(d.get("pages", []))
        totals["flashcards"] += len(fcs)
        totals["answers"] += len(ans)
    return problems, totals


if __name__ == "__main__":
    vols = sys.argv[1:] or list(VOLUMES)
    bad = False
    for v in vols:
        probs, t = check(v)
        print(f"== {v}: {t['sections']} sections, {t['pages']} pages, {t['flashcards']} flashcards, {t['answers']} answers")
        for p in probs:
            print("   ", p)
        bad = bad or any("MISSING" in p or "invalid JSON" in p for p in probs)
    sys.exit(1 if bad else 0)
