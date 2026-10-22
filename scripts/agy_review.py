"""Second pass over every lesson: fact-check it against the notes and write a proper topic quiz.
Reads  scripts/page_data/<vol>_lessons/sNN.json plus the topic's transcripts (as agy_lessons.py does).
Writes scripts/page_data/<vol>_review/sNN.json (resumable):
  {"corrections": [{"scene": i, "field": "narration", "new": "...", "reason": "..."}],
   "quiz": [{"q": "...", "options": [4 strings], "answer": 0-3, "why": "...", "page": N}]}
build_from_pages.py applies the corrections to the lesson and attaches the quiz, which replaces the
flashcard-built quick checks (their wrong options came from other topics, so they were too easy).
Usage (repo root):  python scripts/agy_review.py all --workers 6
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agy_lessons import body_for  # noqa: E402
from agy_util import VOLUMES, WORK_DIR, agy_json, load_pages  # noqa: E402

TEXT_FIELDS = {"narration", "text", "heading", "idea", "name", "work", "quote", "by", "left", "right"}
DEVANAGARI = re.compile(r"[ऀ-ॿ]")

PROMPT = """You are a strict UPSC PSIR examiner and a kind teacher. Below is a short animated lesson script
for the topic "{title}", and the student's handwritten class notes it was written from.

TASK 1 - FACT-CHECK. Compare every claim in the lesson (names, works, dates, cases, quotes, who-said-what,
numbers) with the notes and with well-established PSIR knowledge. List ONLY real errors or misleading
statements (wrong attribution, wrong date, invented quote, a claim the notes contradict). For each give the
scene index (0-based), the field to replace (one of: {fields}), the full corrected text for that field (same
length and tone as the original, simple English), and a short reason. If the lesson is accurate, return an
empty list. Do not rewrite for style.

TASK 2 - QUIZ. Write exactly 4 multiple-choice questions that check UNDERSTANDING of this topic (not trivia
about page numbers). Each has 4 options: one correct and three plausible wrong ones from the SAME topic
(common confusions, mixed-up thinkers, reversed ideas). Options max 18 words, similar length, no "all of
the above". "why": one or two simple sentences explaining the right answer. "page": the scan page number in
the notes that supports it. Mix easy and harder questions. All facts must agree with the notes. English only.

Reply with ONLY this JSON:
{{"corrections": [{{"scene": 0, "field": "narration", "new": "...", "reason": "..."}}],
 "quiz": [{{"q": "...", "options": ["...", "...", "...", "..."], "answer": 0, "why": "...", "page": 12}}]}}

LESSON SCRIPT (scenes in order, index first):
{lesson}

NOTES FOR THIS TOPIC (page summaries first, then the handwritten text):
{body}"""


def make_validator(lesson, start, end):
    scenes = lesson["scenes"]

    def validate(data):
        corr = data.get("corrections")
        quiz = data.get("quiz")
        assert isinstance(corr, list), "corrections must be a list"
        for c in corr:
            i = c.get("scene")
            assert isinstance(i, int) and 0 <= i < len(scenes), f"bad scene index {i}"
            f = c.get("field")
            assert f in TEXT_FIELDS and isinstance(scenes[i].get(f), str), f"scene {i} has no text field {f}"
            assert str(c.get("new", "")).strip(), "empty correction"
        assert isinstance(quiz, list) and len(quiz) == 4, "need exactly 4 quiz questions"
        for q in quiz:
            opts = q.get("options")
            assert str(q.get("q", "")).strip(), "question text missing"
            assert isinstance(opts, list) and len(opts) == 4 and len({str(o).strip().lower() for o in opts}) == 4, "need 4 distinct options"
            assert isinstance(q.get("answer"), int) and 0 <= q["answer"] <= 3, "answer must be 0-3"
            assert str(q.get("why", "")).strip(), "why missing"
            p = q.get("page")
            if not (isinstance(p, int) and start <= p <= end):
                q["page"] = start  # keep the question, point at the topic's first page
        assert not DEVANAGARI.search(json.dumps(data, ensure_ascii=False)), "English only"
    return validate


def review(vol, idx, sec, pages, model):
    out = os.path.join(WORK_DIR, f"{vol}_review", f"s{idx:02d}.json")
    if os.path.exists(out):
        return vol, idx, "cached"
    lf = os.path.join(WORK_DIR, f"{vol}_lessons", f"s{idx:02d}.json")
    if not os.path.exists(lf):
        return vol, idx, "no lesson"
    lesson = json.load(open(lf, encoding="utf-8"))
    ef = os.path.join(WORK_DIR, f"{vol}_enrich", f"s{idx:02d}.json")
    enrich = json.load(open(ef, encoding="utf-8")) if os.path.exists(ef) else {}
    start, end = int(sec["start"]), int(sec["end"])
    prompt = PROMPT.format(
        title=sec["title"], fields=", ".join(sorted(TEXT_FIELDS)),
        lesson="\n".join(f"[{i}] {json.dumps(s, ensure_ascii=False)}" for i, s in enumerate(lesson["scenes"])),
        body=body_for(vol, sec, pages, enrich))
    data = agy_json(prompt, model=model, validate=make_validator(lesson, start, end))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(data, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return vol, idx, f"{len(data['corrections'])} corrections, {len(data['quiz'])} questions"


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
            if not re.search(r"^contents\b|front matter", s["title"], re.I):
                jobs.append((v, i, s, pages))
    print(f"{len(jobs)} lessons to review", flush=True)
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(review, v, i, s, pg, a.model) for v, i, s, pg in jobs]
        for n, fut in enumerate(cf.as_completed(futs), 1):
            try:
                v, i, msg = fut.result()
                print(f"[{n}/{len(jobs)}] {v} s{i:02d}: {msg}", flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"[{n}/{len(jobs)}] FAILED: {str(e)[:200]}", flush=True)
