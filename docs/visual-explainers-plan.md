# Visual explainers: plan, prompts and credit ledger

Goal: help a student who finds PSIR "too difficult" go from 0 to 100. Each explainer is an AI image
or short video, placed only where a topic is abstract, boring or hard to picture, and drawn
from what the handwritten notes actually say.

## How the topics were chosen
- Research (coaching analyses, PYQ tallies; no first-hand student threads were found):
  - Paper 1 Section A (political theory and thought) is consistently called the hardest part,
    because answers need abstract reasoning.
  - Western Political Thought is the most-tested topic (about 93 questions, 2016-25).
  - IR-theory answers score poorly without a concrete picture or application.
- Professor's filter: an explainer earns a place only if the idea is (a) abstract, (b) built on a
  metaphor the thinker already used (cave, Leviathan, trenches, veil, panopticon, Matsyanyaya), or
  (c) a process or system that moves (dialectic, feedback loop, game of chicken). Fact-heavy topics
  (amendments, cases, bilaterals) are left out: a picture does not make a list easier to recall.
- Labels are never baked into the art (AI garbles text). Numbered hotspots and beats are drawn by the
  app (`VisualExplainer.jsx`), so they stay exact and editable.

## Medium and cost (Flow, account aarjav1512, 1,050 credits on 2026-10-18)
| Model | Cost |
|---|---|
| Nano Banana Pro / 2.1 / 2 Lite images | free |
| Omni 1.1 Flash video, 720p | 7 (4 s) / 10 (6 s) / 12 (8 s) / 15 (10 s) |
| Veo 3.1 Lite / Fast / Quality, 8 s | 10 / 20 / 100 |

Pipeline: perfect a still image first (free, iterate freely). Animate only the strongest process
topics, image-to-video from the approved still so the clip matches it. Draft video on Lite (10),
final on Fast (20). Veo Quality (100) is not used. **Budget cap for this wave: 300 credits.**

## Wave 1 (images free; videos marked)
| # | Topic | Vol / pages | Visual idea | Video? |
|---|---|---|---|---|
| 1 | Plato: Allegory of the Cave | V4 p18-19 | cutaway cave: prisoners, shadows, fire, climb, sun | yes |
| 2 | Plato: philosopher-king and the myth of metals | V4 p31-32 | city as a soul: gold, silver, bronze | |
| 3 | State of nature: Hobbes vs Locke vs Rousseau | V4 p85, 91, 101 | one landscape, three worlds | |
| 4 | Hobbes: Leviathan | V4 p95-96, 115 | giant sovereign made of citizens | yes |
| 5 | Marx: dialectical and historical materialism | V4 p139-142 | spiral stair of modes of production | yes |
| 6 | Marx: base and superstructure | V4 p144, 163 | building on an economic foundation | |
| 7 | Marx: alienation | V4 p153-155 | four-way alienated factory worker | |
| 8 | Gramsci: hegemony, war of position | V4 p168-171 | fortress state ringed by civil-society trenches | |
| 9 | Rawls: veil of ignorance | V3 p173-174 | drafting society behind a veil | |
| 10 | Foucault: panopticon and power/knowledge | V3 p104-108 | the tower and the self-watching cells | yes |
| 11 | Lukes: three dimensions of power | V3 p98 | open vote, closed agenda, shaped minds | |
| 12 | Matsyanyaya: why the state exists | V1 p10 | big fish eating small fish | |
| 13 | Kautilya: Saptanga | V1 p14-17 | the state as a body of seven limbs | |
| 14 | Kautilya: Mandala | V1 p18-20 | concentric rings of kingdoms | |
| 15-18 | Game theory (chicken), billiard ball vs cobweb, world-systems, Easton's systems model | V6, pages after transcription | | chicken + Easton |

Video budget: 6 finals x 20 = 120, plus up to 8 Lite drafts x 10 = 80, so 200 of 300.

## Ledger
| Date | Item | Model | Credits | Note |
|---|---|---|---|---|
| 2026-10-18 | Cave v1, v2 (edit), v3 | Nano Banana Pro | 0 | v1/v2 had prisoners facing away from the shadows; v3 approved |
| 2026-10-18 | Leviathan, General Will (headless), Marx vs Gramsci | Nano Banana Pro | 0 | approved first time |
| 2026-10-18 | Veil v1, v2 | Nano Banana Pro | 0 | v1 veils read as veiled women (gender/religion); v2 frosted-glass figures approved |
| 2026-10-18 | Panopticon, Matsyanyaya, State of nature, Alienation | Nano Banana Pro | 0 | approved first time |
| 2026-10-18 | Saptanga v1, v2; Mandala v1, v2 | Nano Banana Pro | 0 | v1s: 8 spokes / first ring green (wrong); v2s approved |
| 2026-10-18 | Lukes v1, v2 | Nano Banana Pro | 0 | v1 had a monk, a Taj-like 'temple' and visible text; v2 secular, approved |
| 2026-10-18 | Cave clip (i2v) | Veo 3.1 Lite | 10 | reviewed frame by frame: glide from shadows to freed prisoner in sunlight; approved |
| 2026-10-18 | Leviathan to General Will morph (first/last frame) | Veo 3.1 Lite | 10 | approved: crown and head dissolve into glowing citizens |
| 2026-10-18 | Panopticon clip | Veo 3.1 Lite | 10 | approved: tower light goes dark, prisoners stay still |
| 2026-10-18 | Matsyanyaya clip | Veo 3.1 Lite | 10 | approved: chaos, staff of danda, fish at peace |
| 2026-10-18 | Leviathan clip upscaled to 1080p (an accidental menu click, done twice) | Flow upscale | unknown | the 720p re-encode is what the app uses |
| | **Spent so far** | | **40 of 1,050** | budget cap 300 |

Flow showed "We noticed some unusual activity... browser extensions that modify the page may cause issues"
after about 20 automated requests, and refused the next batch. Automation was stopped there; the
remaining prompts below are ready to paste into Flow by hand.

## Installed
All 12 stills and 4 clips are in app/public/explainers (13 MB; videos re-encoded to 720p H.264) via
scripts/install_explainer_media.py, and wired in app/src/data/visualExplainers.js.

## Still to generate (paste into the Flow agent; images are free)
1. Easton's systems model: a huge brass-and-wood machine; left funnels take petitions and requests
   (demands) and coins and raised hands (support); gears turn in a glowing chamber with a council table
   (conversion); scrolls and laws come out on the right (outputs); a curved pipe loops from output back
   to the funnels (feedback). Anchor V6 p13. Video candidate.
2. Billiard ball vs cobweb model: diptych; left, solid billiard balls with tiny castles knocking into each
   other (state-centric); right, the same table under a glowing web linking the balls to ships, factories,
   computers, people with phones, aid workers. Anchor V6 p61.
3. Game of chicken (Cuban missile crisis 1962): two vintage cars, blue and red, speeding head-on on a
   cliff-top road at dusk; below, a naval blockade facing a cargo ship with missiles. Anchor V6 p114. Video candidate.
4. Prisoner's dilemma (India-Pakistan nuclear choice): two men in separate interrogation cells divided by
   a stone wall; on each table an olive branch and a locked iron box. Anchor V6 p115.
5. Security dilemma: two walled kingdoms on facing hills, each building higher walls and bigger cannons,
   lookouts pointing in alarm at the other side; storm clouds over the valley. Anchor V6 p62-72.
Always append: "Nano Banana Pro, 16:9, same painterly textbook style, absolutely no text, letters or labels."
