"""Copy the Flow exports from the Downloads folder (D:\\) into app/public/explainers/ under stable names.

Images are re-saved as optimised JPEGs; videos are re-encoded to 720p H.264 + AAC with faststart
so they stream in the browser. Originals in D:\\ are left untouched. Re-run safely at any time.
Usage (repo root):  python scripts/install_explainer_media.py [--src D:/]
"""
import argparse
import glob
import os
import subprocess

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "app", "public", "explainers")

# Flow names each export after its tile title; match on the start of that title.
IMAGES = {
    "Platos_cave_allegory_cutaway": "plato-cave.jpg",
    "Sovereign_rising_above_town": "leviathan.jpg",
    "Glowing_headless_giant_holds_sword": "general-will.jpg",
    "Comparing_Marx_and_Gramsci": "marx-vs-gramsci.jpg",
    "Large_fish_swallowing_smaller_fish": "matsyanyaya.jpg",
    "Prisoners_monitored_from_central": "panopticon.jpg",
    "Featureless_figures_sitting": "veil-of-ignorance.jpg",
    "Kautilya_Saptanga_chariot_wheel": "saptanga-wheel.jpg",
    "Tired_worker_experiencing_aliena": "alienation.jpg",
    "State_of_nature_triptych": "state-of-nature.jpg",
    "Mandala_theory_painted_map": "mandala-map.jpg",
    "Three_panels_depicting_power": "lukes-three-faces.jpg",
}
VIDEOS = {
    "Prisoner_escapes_cave_into_sunlight": "plato-cave.mp4",
    "Crown_dissolving_into_citizens": "leviathan-to-general-will.mp4",
    "Prisoners_standing_still_in_cells": "panopticon.mp4",
    "King_restores_peace_to_river": "matsyanyaya.mp4",
}


def newest(src, prefix, ext):
    hits = sorted(glob.glob(os.path.join(src, prefix + "*" + ext)), key=os.path.getmtime)
    return hits[-1] if hits else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="D:/")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    for prefix, name in IMAGES.items():
        f = newest(a.src, prefix, ".jpg") or newest(a.src, prefix, ".png")
        if not f:
            print("MISSING image", prefix)
            continue
        im = Image.open(f).convert("RGB")
        if im.width > 1600:
            im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
        dest = os.path.join(OUT, name)
        im.save(dest, "JPEG", quality=85, optimize=True, progressive=True)
        print(f"{name:28} {im.width}x{im.height}  {os.path.getsize(dest) // 1024} KB")

    for prefix, name in VIDEOS.items():
        f = newest(a.src, prefix, ".mp4")
        if not f:
            print("MISSING video", prefix)
            continue
        dest = os.path.join(OUT, name)
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", f,
             "-vf", "scale=-2:720", "-c:v", "libx264", "-preset", "slow", "-crf", "24",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", dest],
            check=True)
        print(f"{name:28} {os.path.getsize(f) // 1024} KB -> {os.path.getsize(dest) // 1024} KB")


if __name__ == "__main__":
    main()
