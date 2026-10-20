"""Run the rest of the dataset rebuild unattended: wait for transcription, then segment, enrich, build.

Launch detached from the repo root (survives the Claude session ending):
    powershell Start-Process python -ArgumentList 'scripts/run_rebuild.py' -WindowStyle Hidden
Progress: scripts/page_data/rebuild.log
"""
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "scripts", "page_data", "rebuild.log")
TOTAL = 1146


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%H:%M:%S ") + msg + "\n")


def transcribed():
    base = os.path.join(ROOT, "transcriptions_verbatim")
    return sum(len([f for f in os.listdir(os.path.join(base, d)) if f.endswith(".md")])
               for d in os.listdir(base) if os.path.isdir(os.path.join(base, d)))


def run(args):
    log("RUN " + " ".join(args))
    with open(LOG, "a", encoding="utf-8") as f:
        code = subprocess.call([sys.executable, *args], cwd=ROOT, stdout=f, stderr=subprocess.STDOUT)
    log(f"EXIT {code}")
    return code


if __name__ == "__main__":
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    waited = 0
    while transcribed() < TOTAL and waited < 3600:
        time.sleep(30)
        waited += 30
    log(f"transcribed pages: {transcribed()} / {TOTAL}")
    if transcribed() < TOTAL:
        # fill the last gaps one page per call before giving up
        run(["scripts/agy_transcribe.py", "all", "--per-call", "1", "--workers", "4",
             "--model", "gemini-3.8-flash-low", "--retries", "2"])
    run(["scripts/agy_segment.py", "all", "--workers", "3"])
    run(["scripts/agy_enrich.py", "all", "--workers", "6"])
    run(["scripts/build_from_pages.py"])
    log("DONE")
