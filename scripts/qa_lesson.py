"""Headless QA for the lesson player: open a topic, play its lesson, screenshot every scene.

Usage (dev server running):  python scripts/qa_lesson.py <volumeId> <sectionPrefix> <outDir> [--mobile] [--final]
  --final skips the staggered entrance animations, so each screenshot shows the finished scene.
  e.g. python scripts/qa_lesson.py p1_part5 v4-09- C:/tmp/qa
Prints scene types seen and any console errors; saves scene_NN.png in outDir.
"""
import json
import re
import os
import sys

from playwright.sync_api import sync_playwright

URL = os.environ.get("QA_URL", "http://127.0.0.1:5173/")


def main():
    vol, prefix, out = sys.argv[1], sys.argv[2], sys.argv[3]
    mobile = "--mobile" in sys.argv
    os.makedirs(out, exist_ok=True)
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        ctx = browser.new_context(viewport={"width": 390, "height": 844} if mobile else {"width": 1366, "height": 800},
                                  device_scale_factor=1)
        page = ctx.new_page()
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("response", lambda r: errors.append(f"HTTP {r.status} {r.url}") if r.status >= 400 else None)
        page.add_init_script(f"localStorage.setItem('psir-progress-v1', JSON.stringify({{done:{{}}, lastVolumeId:'{vol}', lastSection:{{}}}}));"
                             "localStorage.setItem('psir-narrator-v1', JSON.stringify({enabled:false, rate:1.3}));")
        page.goto(URL)
        page.wait_for_selector("#study-guide", timeout=20000)
        if "--final" in sys.argv:  # skip the staggered entrances so each shot shows the scene fully built
            page.add_style_tag(content=".lp-anim{animation-delay:0s!important;animation-duration:.01s!important}")
        sec = page.locator(f"section[id^='{prefix}']").first
        if sec.locator("h4").count() == 0:  # topic closed: open it
            sec.locator("button").first.click()
            page.wait_for_timeout(500)
        sec.get_by_text("Watch the lesson").first.click()
        page.wait_for_timeout(600)
        types = []
        for n in range(20):
            page.wait_for_timeout(1900)
            stage = page.locator("[data-stage]").first
            stage.screenshot(path=os.path.join(out, f"scene_{n:02d}.png"))
            caption = page.locator("div.min-h-\\[3\\.5rem\\] p").first
            types.append(caption.inner_text()[:70] if caption.count() else "(no caption)")
            if page.get_by_text("Lesson complete!").count():
                break
            quiz = page.get_by_text(re.compile(r"Quick check \d of \d")).count()
            if quiz:
                page.locator("[data-stage] button").first.click()
                page.wait_for_timeout(400)
                stage.screenshot(path=os.path.join(out, f"scene_{n:02d}_answered.png"))
                page.locator("[data-stage]").get_by_role("button", name="Continue", exact=True).click()
                continue
            page.locator("button[title='Next (→)']").click()
        print(json.dumps({"scenes_seen": len(types), "captions": types, "errors": errors[:10]}, indent=1, ensure_ascii=False))
        browser.close()


if __name__ == "__main__":
    main()
