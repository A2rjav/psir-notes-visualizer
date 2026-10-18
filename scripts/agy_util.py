"""Shared helpers for the agy (Antigravity CLI) pipeline: page loading and JSON-returning calls."""
import json
import os
import re
import subprocess
import time

AGY = os.path.expandvars(r"%LOCALAPPDATA%\agy\bin\agy.exe")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE_DIR = os.path.join(ROOT, "transcriptions_verbatim")
WORK_DIR = os.path.join(ROOT, "scripts", "page_data")

VOLUMES = {
    "p1_part1": {"n": 1, "pages": 214, "title": "Indian Political Thought & Indian Government and Politics (Part 1)"},
    "p1_part2": {"n": 2, "pages": 150, "title": "Indian Government & Politics: Grassroots, Judiciary, Parliament, Executive, Social Movements"},
    "p1_part4": {"n": 3, "pages": 224, "title": "Western Political Thought II & Political Theory (ideologies, state, power, justice, rights)"},
    "p1_part5": {"n": 4, "pages": 180, "title": "Western Political Thought I: Plato to Hannah Arendt"},
    "p2_part1": {"n": 5, "pages": 214, "title": "India and the World: foreign policy, bilaterals, multilateral institutions"},
    "p2_part2": {"n": 6, "pages": 164, "title": "Comparative Politics & International Relations Theory"},
}


def load_pages(vol):
    """Return {page: {kind, notebook, heading, text}} for every transcribed page of a volume."""
    pages = {}
    d = os.path.join(PAGE_DIR, vol)
    if not os.path.isdir(d):
        return pages
    for name in sorted(os.listdir(d)):
        m = re.match(r"page_(\d+)\.md$", name)
        if not m:
            continue
        raw = open(os.path.join(d, name), encoding="utf-8").read()
        head, _, text = raw.partition("\n---\n")
        meta = dict(re.findall(r"^(KIND|NOTEBOOK_PAGE|HEADING):[ \t]*(.*)$", head, re.M))
        pages[int(m.group(1))] = {
            "kind": (meta.get("KIND") or "content").strip().lower(),
            "notebook": (meta.get("NOTEBOOK_PAGE") or "?").strip(),
            "heading": (meta.get("HEADING") or "").strip(),
            "text": text.strip(),
        }
    return pages


def extract_json(text):
    """Pull the first JSON object/array out of a model reply (tolerates code fences and chatter)."""
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    candidates = [fence.group(1)] if fence else []
    candidates.append(text)
    for cand in candidates:
        cand = cand.strip()
        for opener, closer in (("{", "}"), ("[", "]")):
            i, j = cand.find(opener), cand.rfind(closer)
            if i != -1 and j > i:
                try:
                    return json.loads(cand[i:j + 1])
                except json.JSONDecodeError:
                    continue
    raise ValueError("no parseable JSON in model reply")


def agy_json(prompt, model="gemini-3.8-flash-high", timeout=600, validate=None, retries=3):
    """Call agy in read-only plan mode and return parsed JSON; retry (with feedback) on failures."""
    last_err = None
    for attempt in range(retries):
        p = prompt if last_err is None else (
            prompt + f"\n\nYour previous reply was rejected: {last_err}. Fix this and output ONLY the JSON.")
        try:
            res = subprocess.run(
                [AGY, "-p", p, "--model", model, "--mode", "plan", "--output-format", "json",
                 "--print-timeout", f"{timeout}s"],
                cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=timeout + 60)
            outer = extract_json(res.stdout)
            reply = outer.get("response", "") if isinstance(outer, dict) else res.stdout
            data = extract_json(reply)
            if validate:
                validate(data)
            return data
        except Exception as e:  # noqa: BLE001 - any failure -> retry with feedback
            last_err = f"{type(e).__name__}: {str(e)[:300]}"
            time.sleep(2)
    raise RuntimeError(last_err)
