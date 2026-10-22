# PSIR Notes Visualizer

A free study site for the UPSC **Political Science & International Relations (PSIR)** optional, built from
Shubhra Ranjan's handwritten class notes (6 volumes, 1,146 scanned pages). It is meant for someone starting
from zero: it gives a study order, a short animated lesson for every topic, then the notes themselves,
flashcards and model answers.

**Live site:** https://a2rjav.github.io/psir-notes-visualizer/

## What a learner gets

The site is a course in six steps: Western thought first, then political theory, Indian thought, Indian
government, comparative politics and IR theory, and finally India's foreign relations. Every topic offers:

| Part | What it is |
| --- | --- |
| **Watch the lesson** | A 2-3 minute animated explainer. It opens with a hook and an everyday analogy, then uses motion graphics (timelines, cycles, flows, rings, balances, pyramids, comparisons and thinker cards) and, for 11 hard topics, an illustrated picture or video clip. It has four quick-check questions (one midway, three after the recap) with plausible wrong options and a one-line "why" for the right answer, then one click plays the next topic's lesson. The browser's speech engine narrates it, with captions. |
| **Read the notes** | Every page of the topic: a plain-English title and summary, the full transcript of the handwriting, and the original scan beside it. |
| **Flashcards** | Active-recall cards, each linked to the scan page it came from. |
| **Answer blueprints** | Model Mains answers (intro, body pillars, thinkers to cite, conclusion) with an answer map to sketch first. |
| **Concept map** | For each topic, its key thinkers, core ideas and three things to remember, with links into the scans. |

Progress (topics done, last topic per volume) is kept in the browser's local storage.

### Content by volume

| Step | Volume | Pages | Topics | Lessons | Flashcards | Model answers |
| :-: | --- | :-: | :-: | :-: | :-: | :-: |
| 1 | Western Political Thought I: Plato to Hannah Arendt | 180 | 16 | 16 | 120 | 25 |
| 2 | Western Political Thought II & Political Theory | 224 | 22 | 22 | 153 | 36 |
| 3 | Indian Political Thought & IGP Part 1 | 214 | 22 | 22 | 147 | 32 |
| 4 | Indian Government & Politics | 150 | 16 | 16 | 103 | 23 |
| 5 | Comparative Politics & IR Theory | 164 | 18 | 18 | 111 | 25 |
| 6 | India and the World | 214 | 19 | 19 | 136 | 31 |
| | **Total** | **1,146** | **113** | **113** | **770** | **172** |

### Be aware

- **AI-made content.** The transcripts were read from handwriting by Gemini (through Antigravity's `agy`
  CLI). The titles, summaries, flashcards, model answers and lesson scripts were written by Gemini and
  Claude, grounded in those transcripts. Expect some misreadings. The original scan is always one click away,
  and it is the authority.
- **Narration voice** depends on the device's installed voices (it prefers Indian English). With no voice
  available, lessons still play with captions on a timer.
- **Fonts** load from Google Fonts. Offline, the site falls back to system fonts.

## Run it locally

Double-click `start_app.bat`, or:

```bash
cd app
npm install
npm run dev        # http://localhost:5173
```

The scan images are **not** on `master` (`.gitignore` excludes `page_*.png`). They are on the `gh-pages`
branch. In a fresh clone, restore them into `app/public` with:

```bash
git fetch origin gh-pages
git archive origin/gh-pages scans_p1 scans_p1_part2 scans_p1_part4 scans_p1_part5 scans_p2_part1 scans_p2_part2 | tar -x -C app/public
```

## Deploy

The site is the `gh-pages` branch, which holds only build output.

1. `cd app && npm run build`
2. Check out `gh-pages` in a temporary worktree and run `git rm -rq .` there.
3. Copy `app/dist/.` into the worktree, then commit and push.

All asset paths go through `import.meta.env.BASE_URL` (Vite `base: './'`), so the build works under the
`/psir-notes-visualizer/` sub-path.

## How the content is built

All content scripts are in `scripts/`. Run them from the repo root. Each one skips work that is already
done, so a failed run can simply be re-run.

| Step | Script | Output |
| --- | --- | --- |
| 1. Transcribe every page | `agy_transcribe.py all` | `transcriptions_verbatim/<vol>/page_NNN.md` |
| 2. Group pages into topics | `agy_segment.py all` | `scripts/page_data/<vol>_sections.json` |
| 3. Titles, flashcards, model answers | `agy_enrich.py all` (check with `validate_enrich.py`) | `scripts/page_data/<vol>_enrich/sNN.json` |
| 4. Lesson scripts | `agy_lessons.py all --workers 6` | `scripts/page_data/<vol>_lessons/sNN.json` |
| 5. Fact-check lessons, write topic quizzes | `agy_review.py all --workers 6` | `scripts/page_data/<vol>_review/sNN.json` |
| 6. App datasets | `build_from_pages.py` (applies the review corrections) | `app/src/data/<dataset>.js` |
| 7. Explainer media | `install_explainer_media.py` | `app/public/explainers/` and `app/src/data/visualExplainers.js` |

`agy` is Google Antigravity's CLI (`%LOCALAPPDATA%\agy\bin\agy.exe`). Prompts longer than about 6,000
characters are passed through a file, because longer command lines fail on Windows (WinError 206).

A lesson is a JSON list of scenes. Each scene has a `type`: hook, analogy, points, thinker, compare,
timeline, cycle, flow, rings, matrix, pyramid, balance, quote or recap. Each scene also has its
`narration`. `agy_lessons.py` checks every script before saving it:

- 5 to 11 scenes, opening with a hook and closing with a recap;
- 140 to 320 words of narration;
- at least one motion-graphic scene.

The player (`app/src/components/lesson/`) draws each scene type as an animated React/SVG component and adds
the topic's explainer pictures, the quiz from `agy_review.py`, and a closing screen.

The explainer pictures and clips were made in Google Flow. Their prompts, and the credits spent on them,
are in `docs/visual-explainers-plan.md`.

### QA

With the dev server running:

```bash
python scripts/qa_lesson.py p1_part5 v4-09- <outDir> [--mobile] [--final]
```

The script plays one topic's lesson headlessly in Chrome. It screenshots every scene into `<outDir>`
(`--final` shows each scene fully built), answers the quizzes, and reports console errors and failed
requests.

## Layout

```
app/                      React 19 + Vite 8 + Tailwind 4 site
  src/App.jsx             shell, volume loading, view switching
  src/components/         UniversalVisualNotesView (course + notes), lesson/ (player, scenes, narrator),
                          FlashcardsView, AnswerWritingView, MindMapView, ScanInspector, VisualExplainer
  src/data/               one generated dataset per volume, volumesCatalog.js, visualExplainers.js
  public/                 explainers/ (tracked), scans_*/ (from gh-pages, see above)
scripts/                  content pipeline (above); scripts/legacy/ is the old, unused pipeline
transcriptions_verbatim/  page-by-page transcripts (source of truth for all generated content)
docs/                     explainer media plan
```

The `transcriptions_*` folders at the repo root are from the first build and are no longer used.
