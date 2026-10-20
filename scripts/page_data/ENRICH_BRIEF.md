# Enrichment brief (same output as scripts/agy_enrich.py)

You turn verbatim transcripts of handwritten UPSC PSIR (Political Science & International Relations)
lecture-notebook pages into study aids for a student who finds the subject hard. Everything you write
must come from the notes themselves.

## Input
- Repo root: `C:\Users\ASUS VIVOBOOK\Documents\antigravity\jolly-mendel`
- Page files: `transcriptions_verbatim/<vol>/page_NNN.md` (NNN = 3-digit page). Format:
  ```
  KIND: content | index | cover | blank | diagram
  NOTEBOOK_PAGE: <n or ?>
  HEADING: <heading or empty>
  ---
  <verbatim handwritten text>
  ```
- Each section you are given has a volume key, a section number NN, a title and a page range.
- Ignore watermark text ("Join Telegram", "t.me/upsc_pdf", "upscpdf.com") and Hindi margin glosses.

## Output: one file per section
Write `scripts/page_data/<vol>_enrich/sNN.json` (create the folder if needed; NN two digits, as given),
UTF-8, valid JSON, exactly this shape:

```json
{
  "pages": [{"page": 27, "title": "...", "summary": "..."}],
  "flashcards": [{"front": "...", "back": "...", "category": "...", "scanPage": 27}],
  "answers": [{"question": "...", "marks": "15 Marks (250 Words)", "topic": "...", "scanPage": 27,
               "intro": "...", "body": ["...", "...", "..."], "scholars": ["..."], "conclusion": "..."}]
}
```

### pages
- One entry for EVERY page in the range whose KIND is not `blank`, in page order.
- `title`: at most 8 words, naming the topic, thinker, case or relationship on that page. For index or
  cover pages say so (for example "Contents page: topic list with page numbers").
- `summary`: 1-2 plain sentences, only from what is written on that page. No outside knowledge.

### flashcards (only if the section has 2 or more `content`/`diagram` pages; otherwise `[]`)
- Count: max(4, min(10, round(0.7 x number of content/diagram pages))).
- `front`: a precise exam-style question. `back`: the answer in 1-3 sentences, from the notes.
- `category`: a 2-4 word sub-topic label. `scanPage`: the page where the answer is written.
- Spread cards across the section; test the facts, thinkers, doctrines, agreements, dates and arguments
  that the notes actually contain. No trivia about the notebook itself.

### answers (only if 2 or more content/diagram pages; otherwise `[]`)
- Count: 2 if the section has 10 or more content/diagram pages, else 1.
- `question`: a realistic UPSC PSIR Mains question on the section's most examinable theme.
- `marks`: "10 Marks (150 Words)" or "15 Marks (250 Words)". `topic`: short theme name.
- `scanPage`: the main source page (inside the section range).
- `intro`: 30-40 words. `body`: 3-5 strings, together about 150-170 words, each a distinct analytical
  point naming the thinkers, cases, agreements or examples from the notes. `scholars`: 3-8 names or
  works that appear in the notes. `conclusion`: 30-40 words, balanced and forward-looking.

## Rules
- Ground everything in the given pages. Do not import outside facts, invent quotations, numbers or
  dates, or add scholars who are not in the notes. If the notes are thin, write fewer, simpler points.
- English only.
- Write each file, then check it parses: `python -c "import json,sys;json.load(open(sys.argv[1],encoding='utf-8'))" <file>`.
- Do not create, edit or delete any other file, and do not run the build scripts.
- Final report (short): the files you wrote, each with counts (pages / flashcards / answers), and any
  page you could not use. Do not paste file contents.
