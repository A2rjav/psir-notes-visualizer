"""Per-page verbatim transcription of the scanned notebooks using the Antigravity CLI (agy).

Why this exists: the original transcripts for volumes 2-6 are not page-grounded (sections were
sliced into equal page ranges, and several pages are index/cover pages presented as content).
This script reads each scan with a vision model and stores a verbatim transcript per page, so the
app can be rebuilt from what is really on each page.

Output (one file per page, resumable):  transcriptions_verbatim/<vol>/page_XXX.md
    KIND: content | index | cover | blank | diagram
    NOTEBOOK_PAGE: <number printed on the page, or ?>
    HEADING: <page heading/topic as written, or empty>
    ---
    <verbatim text>

Usage (from the repo root):
    python scripts/agy_transcribe.py p2_part1 --start 1 --end 8 --per-call 4 --workers 2
    python scripts/agy_transcribe.py all --per-call 4 --workers 6
"""
import argparse
import concurrent.futures as cf
import os
import re
import subprocess
import sys
import time

AGY = os.path.expandvars(r"%LOCALAPPDATA%\agy\bin\agy.exe")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# key -> (scan folder under app/public, page count)
VOLUMES = {
    "p1_part1": ("scans_p1", 214),
    "p1_part2": ("scans_p1_part2", 150),
    "p1_part4": ("scans_p1_part4", 224),
    "p1_part5": ("scans_p1_part5", 180),
    "p2_part1": ("scans_p2_part1", 214),
    "p2_part2": ("scans_p2_part2", 164),
}

PROMPT = """You are a meticulous transcriber of scanned handwritten UPSC lecture notebook pages.
Open each of these image files (paths relative to the current directory) and read them:
{paths}

For EACH page produce a block in EXACTLY this format, in the order given, and nothing else:

=====PAGE <number>=====
KIND: <content|index|cover|blank|diagram>
NOTEBOOK_PAGE: <the page number handwritten on the sheet, or ?>
HEADING: <the heading/topic written at the top of the page, or empty>
---
<verbatim transcription>

Rules for the transcription:
- Transcribe EVERY handwritten word exactly as written, keeping line breaks, numbering, bullets and
  indentation. Do not summarise, paraphrase, correct, translate or add anything that is not on the page.
- Underlined headings: wrap in __double underscores__. Struck-through text: ~~text~~.
- Margin notes: [Margin: ...]. Tables: markdown tables. Diagrams/flowcharts/maps: reproduce the labels and
  arrows as text inside [Diagram: ...].
- A word you cannot read: [illegible]. Do not guess.
- IGNORE watermark, header and footer text such as "Join Telegram for More Update", "t.me/upsc_pdf",
  "upscpdf.com" and the page-binding holes.
- KIND: index = table of contents / list of topics with page numbers; cover = title page; blank = no
  handwriting; diagram = page that is mainly a drawing; content = everything else.
Do not run any shell commands. Do not create, edit or delete any files. Output only the blocks."""

BLOCK = re.compile(r"=====PAGE\s+0*(\d+)=====\s*\n(.*?)(?=\n=====PAGE\s+\d+=====|\Z)", re.S)


def page_path(vol, page):
    return f"app/public/{VOLUMES[vol][0]}/page_{page:03d}.png"


def out_path(vol, page):
    return os.path.join(ROOT, "transcriptions_verbatim", vol, f"page_{page:03d}.md")


def run_batch(vol, pages, model, timeout):
    prompt = PROMPT.format(paths="\n".join(f"- page {p}: {page_path(vol, p)}" for p in pages))
    cmd = [AGY, "-p", prompt, "--model", model, "--mode", "plan", "--print-timeout", f"{timeout}s"]
    t0 = time.time()
    try:
        res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                             errors="replace", timeout=timeout + 60)
        text = res.stdout
    except subprocess.TimeoutExpired:
        return vol, pages, [], time.time() - t0, "timeout"
    saved = []
    for m in BLOCK.finditer(text):
        page = int(m.group(1))
        body = m.group(2).strip("\n")
        if page not in pages or "---" not in body:
            continue
        head, _, content = body.partition("\n---")
        if not re.search(r"^KIND:\s*\w+", head, re.M):
            continue
        os.makedirs(os.path.dirname(out_path(vol, page)), exist_ok=True)
        with open(out_path(vol, page), "w", encoding="utf-8") as f:
            f.write(head.strip() + "\n---\n" + content.strip("\n") + "\n")
        saved.append(page)
    note = "" if saved else (text[:200].replace("\n", " ") or (res.stderr or "")[:200])
    return vol, pages, saved, time.time() - t0, note


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("volume", help="volume key or 'all'")
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=0)
    ap.add_argument("--per-call", type=int, default=4)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--model", default="gemini-3.8-flash-medium")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--retries", type=int, default=2)
    args = ap.parse_args()

    vols = list(VOLUMES) if args.volume == "all" else [args.volume]
    for attempt in range(args.retries + 1):
        jobs = []
        for v in vols:
            last = args.end or VOLUMES[v][1]
            todo = [p for p in range(args.start, last + 1) if not os.path.exists(out_path(v, p))]
            # smaller batches on retries: a failed 4-page call is usually one bad page
            size = max(1, args.per_call // (2 ** attempt))
            jobs += [(v, todo[i:i + size]) for i in range(0, len(todo), size)]
        if not jobs:
            print("all requested pages are transcribed")
            return
        print(f"attempt {attempt + 1}: {len(jobs)} calls", flush=True)
        done = 0
        with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = [ex.submit(run_batch, v, pages, args.model, args.timeout) for v, pages in jobs]
            for fut in cf.as_completed(futs):
                v, pages, saved, secs, note = fut.result()
                done += 1
                miss = sorted(set(pages) - set(saved))
                print(f"[{done}/{len(jobs)}] {v} {pages[0]}-{pages[-1]} saved={len(saved)}/{len(pages)} "
                      f"{secs:.0f}s {('MISSING ' + str(miss) + ' ' + note) if miss else ''}", flush=True)
    remaining = sum(1 for v in vols for p in range(args.start, (args.end or VOLUMES[v][1]) + 1)
                    if not os.path.exists(out_path(v, p)))
    print(f"finished; pages still missing: {remaining}")


if __name__ == "__main__":
    sys.exit(main())
