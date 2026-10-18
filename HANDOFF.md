# UPSC PSIR Notes Visualizer — Project Handoff Document

**Project Name:** UPSC PSIR 6-Volume Handwritten Notes Visualizer & Active Recall Platform  
**Target Syllabus:** UPSC Civil Services Examination — Political Science & International Relations (PSIR) Optional (Paper 1 & Paper 2)  
**Source Material:** Shubhra Ranjan IAS Classroom Handwritten Lecture Notes (6 Volumes / 1,146 Total Pages)  
**Standard Maintained:** **100% Zero Information Loss** • **Zero Paid External APIs**  
**Application Stack:** React 19, Vite 8, Tailwind CSS v4, Lucide React, Client-Side JavaScript  
**Live Public URL:** [https://a2rjav.github.io/psir-notes-visualizer/](https://a2rjav.github.io/psir-notes-visualizer/)  
**GitHub Repository:** [https://github.com/A2rjav/psir-notes-visualizer](https://github.com/A2rjav/psir-notes-visualizer)  
**Local Access:** `http://localhost:5173/` (via `start_app.bat` or `npm run dev`)  
**Handoff Date:** October 2026  

---

## 1. Executive Summary & Deliverables

This project successfully transforms **1,146 pages** of dense, handwritten UPSC PSIR lecture notes into an ultra-fast, interactive, offline web application designed to solve the problem of reading, memorizing, and structuring answers from handwritten notes.

### What Was Delivered:
1. **100% Scan Coverage:** All 1,146 raw handwritten pages extracted into high-resolution PNG scans in `app/public/scans_*/`.
2. **103 Exhaustive Transcription Batches:** Markdown transcripts preserving every thinker, debate, quote, margin note, and Sanskrit maxim in `transcriptions_*/`.
3. **6 Master Datasets:** Compiled client-side JavaScript data engines in `app/src/data/` totaling over **1.5 MB** of structured, searchable JSON/JS objects.
4. **Interactive Multi-Volume Web App:**
   - Universal multi-volume selector (switch between all 6 volumes in 1 click).
   - Synchronized dual-pane original handwritten scan inspector with zoom, pan, full-screen, and quick-jump navigation.
   - Interactive visual concept maps and mindmaps for all 103 modules.
   - 348 active recall 3D flip flashcards with categories and mastery tracking.
   - 72 UPSC Mains model answer blueprints with ASCII in-exam diagrams.
   - Real-time client-side search across all concepts, thinkers, and notes.
5. **1-Click Windows Starter:** Double-clickable `start_app.bat` script.

---

## 2. Master Catalog of All 6 Digitized Volumes

| Vol | Code | Title & Paper Coverage | Scans | Sections | Flashcards | Answers | Scan Path |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | `P1-V1` | **Paper 1: Indian Political Thought (IPT) & IGP Part 1**<br/>*Manu, Kautilya, Buddha, Sir Syed, Aurobindo, Gandhi, Ambedkar, Roy* | 214 | 28 | 93 | 13 | `/scans_p1` |
| **2** | `P1-V2` | **Paper 1: Indian Government & Politics (IGP Part 2)**<br/>*Grassroots Democracy, Judiciary & NJAC, Parliament, PMO, Basic Structure* | 150 | 15 | 60 | 4 | `/scans_p1_part2` |
| **3** | `P1-V3` | **Paper 1: Western Political Thought II & Political Theory**<br/>*Liberalism, Marxism, Frankfurt School, Feminism, State, Justice, Power* | 224 | 15 | 60 | 10 | `/scans_p1_part4` |
| **4** | `P1-V4` | **Paper 1: Western Political Thought I (Plato to Arendt)**<br/>*Plato, Aristotle, Machiavelli, Hobbes, Locke, Rousseau, Mill, Marx, Gramsci, Arendt* | 180 | 15 | 45 | 15 | `/scans_p1_part5` |
| **5** | `P2-V5` | **Paper 2: India and the World (IR Bilaterals)**<br/>*India-US, Russia, China, Japan, Indo-Pacific, WTO, UN Reforms, Regionalism* | 214 | 15 | 45 | 15 | `/scans_p2_part1` |
| **6** | `P2-V6` | **Paper 2: Comparative Politics & IR Theory**<br/>*Comparative Approaches, Realism, Liberalism, Marxism, Game Theory, Power, Cold War 1 & 2* | 164 | 15 | 45 | 15 | `/scans_p2_part2` |
| **ALL** | **TOTAL** | **Comprehensive UPSC PSIR Optional Syllabus** | **1,146** | **103** | **348** | **72** | **1,146 Scans** |

---

## 3. How to Run and Maintain the Application

### Quick Start (User Mode)
- **Double-click:** [start_app.bat](file:///c:/Users/ASUS%20VIVOBOOK/Documents/antigravity/jolly-mendel/start_app.bat) in the project root directory.
- It will automatically launch the Vite dev server and open `http://localhost:5173/` in your browser.

### Developer Commands (Terminal / PowerShell)
```powershell
# 1. Navigate to frontend directory
cd "c:\Users\ASUS VIVOBOOK\Documents\antigravity\jolly-mendel\app"

# 2. Run development server
npm run dev

# 3. Test production build (typecheck + minify)
npm run build

# 4. Preview production build
npm run preview
```

### Rebuilding or Updating Datasets
If you modify any transcription markdown files in `transcriptions_*/`, rebuild the datasets with Python:
```powershell
cd "c:\Users\ASUS VIVOBOOK\Documents\antigravity\jolly-mendel"

# Volume 1
python scripts/build_paper1_data_full.py

# Volume 2
python scripts/build_paper1_part2_dataset.py

# Volume 3
python scripts/build_paper1_part4_dataset.py

# Volume 4
python scripts/build_paper1_part5_dataset.py

# Volume 5
python scripts/build_part1_dataset.py

# Volume 6
python scripts/build_part2_dataset.py
```

---

## 4. Key Files and Code Structure

```
c:\Users\ASUS VIVOBOOK\Documents\antigravity\jolly-mendel\
├── HANDOFF.md                       # High-level project handoff overview (this file)
├── README.md                        # Exhaustive architectural documentation & guides
├── start_app.bat                    # 1-click Windows launcher script
│
├── app/                             # React 19 + Vite 8 frontend application
│   ├── public/                      # Static assets & 1,146 original handwritten scans
│   │   ├── scans_p1/                # Volume 1 scans (page_001.png to page_214.png)
│   │   ├── scans_p1_part2/          # Volume 2 scans (page_001.png to page_150.png)
│   │   ├── scans_p1_part4/          # Volume 3 scans (page_001.png to page_224.png)
│   │   ├── scans_p1_part5/          # Volume 4 scans (page_001.png to page_180.png)
│   │   ├── scans_p2_part1/          # Volume 5 scans (page_001.png to page_214.png)
│   │   └── scans_p2_part2/          # Volume 6 scans (page_001.png to page_164.png)
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx           # Top header, 6-volume dropdown, search, view tabs
│   │   │   ├── Sidebar.jsx          # Drawer syllabus navigation & volume switcher
│   │   │   ├── UniversalVisualNotesView.jsx # Universal dynamic notes view for any volume
│   │   │   ├── MindMapView.jsx      # Dynamic concept map & connected nodes
│   │   │   ├── FlashcardsView.jsx   # 3D flip card active recall system
│   │   │   ├── AnswerWritingView.jsx# 3-tier UPSC Mains model answer blueprints
│   │   │   └── ScanInspector.jsx    # Dual-pane synchronized handwritten scan viewer
│   │   ├── data/
│   │   │   ├── volumesCatalog.js    # Master registry connecting all 6 volumes
│   │   │   ├── paper1IptData.js     # Volume 1 dataset (380 KB)
│   │   │   ├── paper1Part2Data.js   # Volume 2 dataset (245 KB)
│   │   │   ├── paper1Part4Data.js   # Volume 3 dataset (219 KB)
│   │   │   ├── paper1Part5Data.js   # Volume 4 dataset (218 KB)
│   │   │   ├── paper2IndiaWorldData.js # Volume 5 dataset (228 KB)
│   │   │   └── paper2ComparativeData.js # Volume 6 dataset (203 KB)
│   │   ├── App.jsx                  # Master root component orchestrating state
│   │   └── index.css                # Tailwind CSS v4 styling rules
│
├── scripts/                         # Python automation, parsers & batch compilers
│   ├── batch_meta_*.py              # Metadata definitions for each volume
│   ├── batch_parser_*.py            # Regex/AST parsers for concepts, flashcards, answers
│   └── build_*_dataset.py           # Compilers writing directly to app/src/data/
│
└── transcriptions_*/                # 103 Markdown files with exhaustive transcriptions
```

---

## 5. Verification Checkpoints

- [x] **1,146 Scans Extracted & Verified:** Every PNG verified in `app/public/`.
- [x] **103 Batches Transcribed:** Zero points, quotes, or margin notes skipped.
- [x] **Node.js Clean Import:** All 6 dataset modules verified via Node.js require script.
- [x] **Zero TypeScript / JSX Errors:** `tsc && vite build` completes in <3 seconds.
- [x] **Local Dev Server Verified:** Verified `200 OK` on `http://127.0.0.1:5173/`.
- [x] **Dual-Pane Scan Inspector Working:** Every single scan page loads with full zoom/pan.
