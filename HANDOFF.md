# Handoff: state of the project (22 October 2026)

See `README.md` for what the site does, how to run and deploy it, and how the content pipeline works. This
file records where things stand and what is left.

## Done

- **Notes.** All 1,146 scan pages are transcribed (`transcriptions_verbatim/`) and grouped into 113 study
  topics plus front matter. Every topic has page titles and summaries. Across all topics there are 770
  flashcards and 172 model answers. `scripts/validate_enrich.py` passes on all 119 sections.
- **Lessons.** Every topic has an animated, narrated lesson (`scripts/page_data/<vol>_lessons/`), written
  by Gemini through `agy` and validated by `agy_lessons.py`. A second agy pass (`agy_review.py`) fact-checked each lesson against its pages, fixing the errors it found (for example, the Emergency dated 1970 instead of 1975), and wrote a 4-question topic quiz with explanations. The player is in
  `app/src/components/lesson/` and was checked with `scripts/qa_lesson.py`:
  - every scene type that appears in the lessons was checked on desktop and on a phone-sized screen;
  - no console errors and no failed requests.
- **Explainer media.** Flow made 12 illustrated stills and 4 video clips for 11 hard topics, among them
  Matsyanyaya, Saptanga, Mandala, Plato's cave, Leviathan, the general will, the panopticon, Lukes' three
  faces of power, the veil of ignorance, alienation, and Marx vs Gramsci. The lesson player shows them as
  numbered-hotspot pictures and clips.
- **Course UI.** The UI gives:
  - a study guide with a 6-step order;
  - a topic outline with only the open topic expanded;
  - "Watch the lesson / Read the notes / Flashcards / Answer" steps for each topic;
  - progress saved in the browser;
  - a concept map for each topic;
  - an answer map for each model answer.

## Known gaps

- **Transcripts are AI readings of handwriting**, and some words are wrong. Only sampled pages were checked
  against the scans.
- **Picture explainers cover 11 topics only.** Five more V6 image prompts are written but not generated
  (`docs/visual-explainers-plan.md`). Flow's "We noticed some unusual activity" check blocks automated
  generation through `gflow`, so these must be made by hand in Flow. Install them afterwards with
  `scripts/install_explainer_media.py`.
- **Thinker cards show initials, not portraits.** `ThinkerScene` accepts a `portrait` image path.
  Public-domain portraits (for example from Wikimedia Commons, with attribution) could be added.
- **Narration uses the browser's built-in voices.** Quality varies by device. Pre-recorded audio would need
  a TTS service.
- **The scans live only on the `gh-pages` branch** (see README, "Run it locally").

## To regenerate after changing the notes

```bash
python scripts/agy_enrich.py all          # only sections without output are redone
python scripts/agy_lessons.py all --workers 6
python scripts/agy_review.py all --workers 6
python scripts/build_from_pages.py
cd app && npm run build
```

To redo one topic, delete its `sNN.json` before re-running.
