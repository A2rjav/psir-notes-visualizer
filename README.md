# UPSC PSIR 6-Volume Handwritten Notes Visualizer & Active Recall System

> **A 100% Zero-Loss, Offline-First, Highly Visual Web Application for UPSC Civil Services Examination (PSIR Optional)**  
> Digitizing all **6 Volumes (1,146 Total Pages)** of Shubhra Ranjan IAS Classroom Handwritten Lecture Notes.  
> 
> 🌐 **Live Web App:** [https://a2rjav.github.io/psir-notes-visualizer/](https://a2rjav.github.io/psir-notes-visualizer/)  
> 📦 **GitHub Repository:** [https://github.com/A2rjav/psir-notes-visualizer](https://github.com/A2rjav/psir-notes-visualizer)

---

## Table of Contents
1. [Project Overview & Core Mission](#1-project-overview--core-mission)
2. [Complete 6-Volume Syllabus Breakdown](#2-complete-6-volume-syllabus-breakdown)
3. [The Zero-Information-Loss Standard](#3-the-zero-information-loss-standard)
4. [End-to-End System Architecture](#4-end-to-end-system-architecture)
5. [Directory & File Organization](#5-directory--file-organization)
6. [Interactive Application Modules](#6-interactive-application-modules)
   - [Universal Visual Notes View](#universal-visual-notes-view)
   - [Synchronized Dual-Pane Scan Inspector](#synchronized-dual-pane-scan-inspector)
   - [Interactive Concept Mindmaps](#interactive-concept-mindmaps)
   - [Active Recall Flashcards Engine](#active-recall-flashcards-engine)
   - [UPSC Mains Model Answer Blueprints](#upsc-mains-model-answer-blueprints)
   - [Universal Client-Side Search](#universal-client-side-search)
7. [How to Run the Application Manually](#7-how-to-run-the-application-manually)
8. [Data Compilation & Pipeline Automation](#8-data-compilation--pipeline-automation)
9. [How to Modify, Update, or Add New Content](#9-how-to-modify-update-or-add-new-content)
10. [Performance & Zero-Cost Infrastructure](#10-performance--zero-cost-infrastructure)

---

## 1. Project Overview & Core Mission

### The Problem
UPSC Political Science and International Relations (PSIR) optional aspirants typically rely on dense, multi-volume handwritten lecture notes (such as those from Shubhra Ranjan IAS). These notes suffer from several critical learning bottlenecks:
- **Length & Fatigue:** Hundreds of pages of cursive handwriting are tiring to read and slow to revise.
- **Memorization Barrier:** Dense text makes active recall difficult; students struggle to recall specific quotes, Sanskrit maxims, and scholar debates under exam pressure.
- **Answer-Writing Gap:** Notes present raw lecture flows rather than structured 10-, 15-, and 20-marker Mains frameworks with clear introductions, body pillars, and balanced conclusions.
- **Fear of Information Loss:** Standard digital summaries often discard margin notes, secondary thinkers, and case nuances.

### The Solution
This web application transforms all **6 volumes (1,146 handwritten pages)** into an offline, interactive, high-detail knowledge repository:
- **100% Zero Information Loss:** Every single scholar citation, theoretical paradigm, Sanskrit term, and margin annotation is preserved.
- **Zero Paid APIs:** Built entirely on open-source, client-side technologies (React 19, Vite 8, Tailwind CSS v4) with zero API keys, subscriptions, or external requests.
- **Dual-Pane Scan Inspector:** At any moment, students can click a single button to view the original handwritten page side-by-side with the digital notes for verification.
- **Active Recall & Exam Structuring:** Embedded flashcards, concept maps, and 3-tier Mains answer blueprints bridge the gap between reading and writing high-scoring answers.

---

## 2. Complete 6-Volume Syllabus Breakdown

The application organizes all 1,146 pages into 6 dedicated volumes covering both Paper 1 and Paper 2 of the UPSC PSIR syllabus:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           UPSC PSIR OPTIONAL SYLLABUS                            │
├────────────────────────────────────────┬─────────────────────────────────────────┤
│                PAPER 1                 │                 PAPER 2                 │
│   (Political Theory & Indian Govt)     │   (Comparative Politics & Int'l Rel)    │
├────────────────────────────────────────┼─────────────────────────────────────────┤
│ • Volume 1 (214 Scans): IPT & IGP 1    │ • Volume 5 (214 Scans): India & World   │
│ • Volume 2 (150 Scans): IGP Part 2     │ • Volume 6 (164 Scans): Comparative/IR  │
│ • Volume 3 (224 Scans): WPT II/Theory  │                                         │
│ • Volume 4 (180 Scans): WPT I (Plato)  │                                         │
└────────────────────────────────────────┴─────────────────────────────────────────┘
```

### Detailed Volume Registry:

#### Volume 1 (`P1-V1`): Indian Political Thought (IPT) & IGP Part 1
- **File:** `paper1_part1.pdf` | **Scans:** 214 Pages (`scans_p1/page_001.png` to `page_214.png`)
- **Key Themes:** Ancient statecraft (*Dharmashastra*, Manu, *Matsyanyaya*, *Ashta-Lokapala*); Kautilya's *Arthashastra* (*Saptanga* organic state, *Yogakshema*, 12-King *Mandala*, anti-corruption chain); Buddhist political thought (*Agganna Sutta*, *Mahasammata*, *Dhamma-Chakka* vs *Danda-Chakra*, Sangha democracy); Modern IPT Renaissance (Sir Syed Ahmed Khan, Sri Aurobindo's spiritual nationalism, Mahatma Gandhi's *Swaraj/Sarvodaya*, Dr. B.R. Ambedkar's social justice & annihilation of caste, M.N. Roy's radical humanism).
- **Dataset:** `app/src/data/paper1IptData.js` (380 KB; 28 thematic modules, 93 flashcards, 13 model answers).

#### Volume 2 (`P1-V2`): Indian Government & Politics: Grassroots to Sovereignty (IGP Part 2)
- **File:** `paper1_part2.pdf` | **Scans:** 150 Pages (`scans_p1_part2/page_001.png` to `page_150.png`)
- **Key Themes:** Grassroots democracy (Panchayati Raj, 73rd/74th Amendments, PESA Act 1996, 3Fs deficit, 2nd ARC); Judiciary (Judicial Review, Judicial Activism, PIL/SAL, Upendra Baxi vs Pratap Bhanu Mehta, Three Judges Cases, Collegium vs NJAC 99th CA); Union Parliament & Executive (Decline of Parliament, Parliamentary Committees, President's discretionary powers, PMO vs Cabinet Secretariat); Social Movements & Planning (Environmental struggles, Dalit Panthers, Peasant movements, Nehru-Mahalanobis model to NITI Aayog); Constitutionalism & Basic Structure Doctrine (*Kesavananda Bharati*, *Minerva Mills*, *I.R. Coelho*).
- **Dataset:** `app/src/data/paper1Part2Data.js` (245 KB; 15 thematic modules, 60 flashcards, 4 model answers).

#### Volume 3 (`P1-V3`): Western Political Thought II & Political Theory
- **File:** `paper1_part4.pdf` | **Scans:** 224 Pages (`scans_p1_part4/page_001.png` to `page_224.png`)
- **Key Themes:** Political Ideologies (Idealism, Classical Liberalism, Modern Liberalism, Neo-Liberalism, Social Liberalism); Multiculturalism (Will Kymlicka, Bhikhu Parekh, Charles Taylor); Socialism & Classical Marxism; Neo-Marxism & Frankfurt School Critical Theory; Totalitarianism & Fascism; Feminism (Waves, Radical/Liberal/Socialist schools, Intersectionality); Theories of the State (Liberal, Instrumental vs Structural Marxism, Pluralist, Post-Colonial); Concept of Power (Steven Lukes' Three Dimensions, Max Weber, Michel Foucault's Power/Knowledge); Concept of Justice (John Rawls' *Theory of Justice*, Robert Nozick's Entitlement Theory, Amartya Sen's Realization-Focused Comparison); Concept of Rights & Equality.
- **Dataset:** `app/src/data/paper1Part4Data.js` (219 KB; 15 thematic modules, 60 flashcards, 10 model answers).

#### Volume 4 (`P1-V4`): Western Political Thought I: Plato to Hannah Arendt
- **File:** `paper1_part5.pdf` | **Scans:** 180 Pages (`scans_p1_part5/page_001.png` to `page_180.png`)
- **Key Themes:** Plato (Theory of Forms/Ideas, Cave Allegory, Philosopher King, Tripartite Soul, Justice as Functional Specialization, Communism of Wives and Property, Karl Popper's critique); Aristotle (Teleology, State as Natural and Prior to Individual, Citizenship, Theory of Slavery, Property, Constitutional Typology, Causes and Remedies of Revolution, Golden Mean & Rule of Law); Niccolò Machiavelli (*The Prince*, Separation of Politics from Ethics, Lion and Fox, *Virtù* vs *Fortuna*); Thomas Hobbes (Scientific Materialism, State of Nature as Solitary/Poor/Nasty/Brutish/Short, Social Contract, *Leviathan*, Absolute Sovereignty, Individualism); John Locke (Natural Rights to Life, Liberty, and Estate, Social Contract, Limited Government, Right to Revolution); Jean-Jacques Rousseau (Discourse on Inequality, Noble Savage, Social Contract, General Will, Direct Democracy, "Forced to be Free"); J.S. Mill (Revision of Benthamite Utilitarianism, *On Liberty*, Harm Principle, Self-regarding vs Other-regarding actions, Tyranny of the Majority, Subjection of Women); Karl Marx (Historical Materialism, Dialectics, Base and Superstructure, Theory of Alienation, Surplus Value, Class Struggle, Communism); Antonio Gramsci (Hegemony, Civil Society vs Political Society, War of Position vs War of Movement, Organic Intellectuals); Hannah Arendt (*Vita Activa*, Labor-Work-Action, Public Realm vs Private Realm, Power in Concert vs Violence, Totalitarianism & Banality of Evil).
- **Dataset:** `app/src/data/paper1Part5Data.js` (218 KB; 15 thematic modules, 45 flashcards, 15 model answers).

#### Volume 5 (`P2-V5`): India and the World: Foreign Policy & Bilaterals
- **File:** `part1_notes.pdf` | **Scans:** 214 Pages (`scans_p2_part1/page_001.png` to `page_214.png`)
- **Key Themes:** India-USA Strategic Convergence (Estranged to Engaged Democracies, 123 Civil Nuclear Agreement, LEMOA, COMCASA, BECA, 2+2 Ministerial Dialogue); India-Russia Strategic Partnership (1971 Treaty of Friendship, Special and Privileged Partnership, S-400 Triumf, Nuclear Energy, Eurasian Dynamics); India-China Relations (Historical evolution, Panchsheel 1954, 1962 War, LAC Boundary Disputes, CPEC/BRI, Doklam Standoff, String of Pearls vs SAGAR); India-Japan Special Strategic Partnership (Shinzo Abe's *Confluence of the Two Seas*, High-Speed Rail, Asia-Africa Growth Corridor, Quad); Hegemonic Stability Theory & The Rise of China (Kindleberger, Thucydides' Trap, Clash of Civilizations); India's Look East to Act East Policy (Narasimha Rao to Modi, 3Cs: Commerce-Connectivity-Culture, Northeast as Gateway); Southeast Asia & Indo-Pacific Maritime Security (UNCLOS, Malacca Dilemma, Quad, SAGAR); United Nations Reforms (Anachronistic 1945 Architecture, UNSC Expansion, G4, Coffee Club, Peacekeeping Contributions); World Trade Organization (Doha Development Round, Green/Blue/Amber Boxes, Bali Peace Clause, Public Stockholding for Food Security, Dispute Settlement Crisis); European Union (Regional Integration, Eurozone Crisis, Brexit, BTIA negotiations); ASEAN & Modi's Diplomatic Doctrines (The ASEAN Way, Neighbourhood First, Panchamrit, Paradiplomacy); South Asian Regionalism (SAARC Stagnation vs BIMSTEC Revival, BBIN, Cross-border terrorism); India-Pakistan Flashpoints & Extended Neighbourhood (Indus Waters Treaty, Siachen, Sir Creek, Chabahar Port, Connect Central Asia, West Asia De-hyphenation).
- **Dataset:** `app/src/data/paper2IndiaWorldData.js` (228 KB; 15 thematic modules, 45 flashcards, 15 model answers).

#### Volume 6 (`P2-V6`): Comparative Politics & International Relations Theory
- **File:** `part2_notes.pdf` | **Scans:** 164 Pages (`scans_p2_part2/page_001.png` to `page_164.png`)
- **Key Themes:** Comparative Politics: Evolution, Systems & Structural-Functional Approaches (Aristotle to Modern Era, Traditional vs Modern Comparative Politics, David Easton's Systems Model, Gabriel Almond's Structural-Functionalism); Political Sociology, Economy & Civic Culture (Social cleavages, Political economy of state vs market, Almond & Verba's *The Civic Culture*, Lucian Pye's political development syndrome); Nature of the State in Advanced Industrial & Developing Polities (Welfare state, Claus Offe's legitimation crisis, Corporatism, Hamza Alavi's post-colonial *Overdeveloped State*, Gunnar Myrdal's *Soft State*, Joel Migdal's *Strong Societies and Weak States*); Politics of Representation & Participation (Maurice Duverger's Electoral Laws, Sartori's Party Typology, Otto Kirchheimer's Catch-All Party, Pressure groups & Mancur Olson's *Logic of Collective Action*); Globalisation and the Nation-State (Hyper-globalists, Skeptics, Transformationalists, Kenichi Ohmae's Borderless World, Susan Strange's Retreat of the State); Theories of International Relations (Classical Realism: E.H. Carr, Hans Morgenthau's Six Principles; Structural Realism / Neo-Realism: Kenneth Waltz's Systemic Anarchy & Bipolar Stability; Offensive Realism: John Mearsheimer's Tragedy of Great Power Politics; Liberal Theories: Keohane & Nye's Complex Interdependence, Michael Doyle's Democratic Peace Theory, Neo-liberal Institutionalism; Marxist Approaches: Lenin's Imperialism, Andre Gunder Frank's Dependency Theory, Immanuel Wallerstein's World Systems Theory; Feminist IR: J. Ann Tickner's Critique of Morgenthau); Scientific Approaches (Morton Kaplan's Six International System Models, Game Theory: Prisoner's Dilemma, Chicken Game, Graham Allison's Decision-Making Models); Concept & Management of Power (Hard, Soft, Smart & Sharp Power by Joseph Nye, Susan Strange's Structural Power, Balance of Power Techniques, Collective Security Paradigm vs Veto Paralysis); The Cold War & Global Order (Origins & Historiography, Kennan's Long Telegram, Truman Doctrine, Cuban Missile Crisis, Détente, Second Cold War, Strategic Arms Control INF, Gorbachev's Glasnost & Perestroika, Fall of Berlin Wall & USSR Disintegration, Krauthammer's Unipolar Moment, Fukuyama's End of History, and Dmitri Trenin's Cold War 2.0).
- **Dataset:** `app/src/data/paper2ComparativeData.js` (203 KB; 15 thematic modules, 45 flashcards, 15 model answers).

---

## 3. The Zero-Information-Loss Standard

A major failure mode in digital note-taking is aggressive summarization that strips out the precise keywords, citations, and margin comments that award marks in the UPSC Civil Services Examination.

To ensure **100% Zero Information Loss**, the transcription and compilation process adhered to five non-negotiable rules:

1. **Every Scholar & Commentary Preserved:** Whether it is Alasdair MacIntyre on Western ethnocentrism, Bhikhu Parekh on Hindu continuity, Claus Offe on the welfare state, or Dmitri Trenin on Cold War 2.0, every single commentator mentioned in class is captured with their exact theoretical context.
2. **Every Sanskrit Maxim & Technical Term Retained:** Concepts like *Matsyanyaya*, *Ashta-Lokapala*, *Yogakshema*, *Prajasukhe sukham rajnah*, *Upadha*, *Shadgunya Niti*, *Bherighosa*, *Novoye Myshleniye*, and *Animus Dominandi* are included with English translations.
3. **Every Margin Note & Didactic Metaphor Preserved:** Shubhra Ranjan's famous classroom metaphors (e.g., honey on the tongue, fish swimming in water drinking water without notice, Frank Sinatra's "My Way" doctrine, the 13 days of Cuban Missile Crisis brinkmanship) are preserved verbatim.
4. **Complete Scan Cataloging:** All 1,146 scan pages are indexed with their physical page numbers, notebook folios, and topic summaries in the underlying metadata.
5. **Direct Source Traceability:** Every concept card in the web app provides a one-click link to view the exact original handwritten scan page from which it was transcribed.

---

## 4. End-to-End System Architecture

```mermaid
flowchart TD
    subgraph Sources ["1. Source Notes (6 Volumes / 1,146 Pages)"]
        P1["paper1_part1.pdf (214p)"]
        P2["paper1_part2.pdf (150p)"]
        P3["paper1_part4.pdf (224p)"]
        P4["paper1_part5.pdf (180p)"]
        P5["part1_notes.pdf (214p)"]
        P6["part2_notes.pdf (164p)"]
    end

    subgraph Extraction ["2. Scan Extraction Engine"]
        MuPDF["Python / PyMuPDF High-Res Extraction (150 DPI)"]
        P1 & P2 & P3 & P4 & P5 & P6 --> MuPDF
        MuPDF --> PublicScans["app/public/scans_*/ (1,146 PNG Images)"]
    end

    subgraph Transcription ["3. Zero-Loss Transcription Engine"]
        Batches["103 Thematic Markdown Files in transcriptions_*/"]
        PublicScans --> Batches
    end

    subgraph Parsers ["4. Python Data Compilers"]
        ParsersCode["scripts/build_*_dataset.py + batch_parser_*.py"]
        Batches --> ParsersCode
    end

    subgraph Datasets ["5. JavaScript Master Data Engines"]
        JSData["app/src/data/*.js (1.5 MB Clean Structured ES Modules)"]
        ParsersCode --> JSData
        Registry["volumesCatalog.js (Unified Registry)"]
        JSData --> Registry
    end

    subgraph Frontend ["6. Interactive Web Application (React 19 + Vite 8)"]
        App["App.jsx (Master Orchestrator)"]
        Registry --> App
        App --> Nav["Navbar (Volume & View Switcher)"]
        App --> Side["Sidebar (Syllabus & Volume Drawer)"]
        App --> Canvas["UniversalVisualNotesView (Notes, Mindmaps, Cards)"]
        App --> DualPane["ScanInspector (Synchronized Original Handwritten Scan)"]
    end
```

---

## 5. Directory & File Organization

```
c:\Users\ASUS VIVOBOOK\Documents\antigravity\jolly-mendel\
├── HANDOFF.md                       # Project handoff summary & deliverables
├── README.md                        # Comprehensive system documentation (this file)
├── start_app.bat                    # 1-click Windows desktop starter script
│
├── app/                             # React 19 + Vite 8 web application
│   ├── index.html                   # HTML entry point with modern typography
│   ├── package.json                 # Project dependencies (Tailwind 4, Lucide, Vite)
│   ├── vite.config.ts               # Vite configuration with React & Tailwind plugins
│   ├── tsconfig.json                # TypeScript & JSX configuration
│   ├── public/                      # Static assets & 1,146 handwritten scan images
│   │   ├── scans_p1/                # Volume 1: IPT & IGP Part 1 (214 PNGs)
│   │   ├── scans_p1_part2/          # Volume 2: IGP Part 2 (150 PNGs)
│   │   ├── scans_p1_part4/          # Volume 3: WPT Part II & Theory (224 PNGs)
│   │   ├── scans_p1_part5/          # Volume 4: WPT Part I Classical (180 PNGs)
│   │   ├── scans_p2_part1/          # Volume 5: India and the World (214 PNGs)
│   │   └── scans_p2_part2/          # Volume 6: Comparative Politics & IR (164 PNGs)
│   └── src/
│       ├── main.jsx                 # React root renderer
│       ├── App.jsx                  # Root container orchestrating volumes & views
│       ├── index.css                # Global styles & Tailwind v4 `@import`
│       ├── components/              # UI Component Library
│       │   ├── Navbar.jsx           # Top header, 6-volume dropdown, search bar
│       │   ├── Sidebar.jsx          # Flyout drawer for syllabus & 6 volumes
│       │   ├── UniversalVisualNotesView.jsx # Universal dynamic renderer for all 6 volumes
│       │   ├── ScanInspector.jsx    # Dual-pane synchronized handwritten scan viewer
│       │   ├── MindMapView.jsx      # Dynamic concept map & connected nodes
│       │   ├── FlashcardsView.jsx   # 3D active recall flip card system
│       │   └── AnswerWritingView.jsx# 3-tier UPSC Mains model answer blueprints
│       └── data/                    # Compiled master datasets (1.5 MB JS)
│           ├── volumesCatalog.js    # Master registry of all 6 volumes
│           ├── paper1IptData.js     # Volume 1 dataset (28 modules, 93 cards, 13 answers)
│           ├── paper1Part2Data.js   # Volume 2 dataset (15 modules, 60 cards, 4 answers)
│           ├── paper1Part4Data.js   # Volume 3 dataset (15 modules, 60 cards, 10 answers)
│           ├── paper1Part5Data.js   # Volume 4 dataset (15 modules, 45 cards, 15 answers)
│           ├── paper2IndiaWorldData.js # Volume 5 dataset (15 modules, 45 cards, 15 answers)
│           └── paper2ComparativeData.js # Volume 6 dataset (15 modules, 45 cards, 15 answers)
│
├── scripts/                         # Python automation, parsers & batch compilers
│   ├── batch_meta_*.py              # Structural metadata per volume
│   ├── batch_parser_*.py            # Regex/AST parsers for concepts, flashcards, answers
│   └── build_*_dataset.py           # Compilers writing directly to app/src/data/
│
├── transcriptions_paper1/           # Volume 1 markdown transcriptions (27 batches)
├── transcriptions_paper1_part2/     # Volume 2 markdown transcriptions (15 batches)
├── transcriptions_paper1_part4/     # Volume 3 markdown transcriptions (15 batches)
├── transcriptions_paper1_part5/     # Volume 4 markdown transcriptions (15 batches)
├── transcriptions_part1/            # Volume 5 markdown transcriptions (15 batches)
└── transcriptions_part2/            # Volume 6 markdown transcriptions (15 batches)
```

---

## 6. Interactive Application Modules

### Universal Visual Notes View
The core reading environment renders the transcribed lecture notes with maximum visual clarity:
- **Hero Banner:** Displays paper name, section, notebook folio range, total scans, and quick statistics.
- **Section Filter Bar:** Fast horizontal pill bar allowing students to jump immediately to any thematic section or view all sections at once.
- **Key Thinkers & Commentators Card:** Highlighting scholars to cite in Mains answers.
- **Core Theoretical Doctrines Card:** Highlighting foundational models.
- **Detailed Concept Blocks:** Formatted with custom badges (e.g., *IR Theory*, *Comparative Approach*, *Strategic Concept*), executive summaries, and bulleted breakdowns of classroom points, margin notes, and Sanskrit maxims.
- **Direct Scan Buttons:** Every single concept card contains a `Scan P.XX` button that opens that exact original handwritten page in the split inspector.

### Synchronized Dual-Pane Scan Inspector
Located on the right-hand side of the screen (or in a full-screen modal on mobile):
- **Live Image Rendering:** High-resolution scans loaded directly from local storage with sub-millisecond latency.
- **Zoom & Pan Controls:** Zoom in up to 2.5× to inspect tight cursive margin notes; zoom out to 0.75× for full-page overview; 1-click zoom reset.
- **Pagination & Navigation:** Next/Previous buttons and a quick-jump dropdown listing all pages with their lecture titles.
- **Full-Screen Mode:** Toggle full-screen inspection mode with one click.
- **Zero Internet Requirement:** All 1,146 images are hosted locally in `app/public/`.

### Interactive Concept Mindmaps
- **Cluster Visualization:** Dynamically generates visual concept clusters for all 103 modules across all 6 volumes.
- **Central Topic Node:** Outlines the core problematique, historical epoch, and primary texts.
- **Radiating Sub-Nodes:** Visual cards detailing competing schools of thought, theoretical tensions, and practical applications.
- **Instant Scan Cross-Referencing:** Every sub-node links directly to its archival scan page.

### Active Recall Flashcards Engine
- **348 Total High-Yield Flashcards:** Distributed across all 6 volumes.
- **3D Flip Card Interaction:** Click anywhere on the card to flip between Question/Prompt and Answer/Explanation.
- **Category Filtering & Shuffle:** Filter by theoretical categories or shuffle the deck for random active recall testing.
- **Mastery Tracking:** "Mark as Mastered" button saves mastered cards to local session state with a live mastery counter.
- **Mnemonics & Key Dictums:** Prominently displays memory hooks and theoretical dictums.

### UPSC Mains Model Answer Blueprints
- **72 Complete Model Answer Frameworks:** Covering 10-, 15-, and 20-marker questions across all 6 volumes.
- **Rigorous 3-Tier Structure:**
  1. *Introduction (30–40 words):* Conceptual genesis, core problematique, and historical context.
  2. *Core Body Arguments (150–170 words):* Numbered analytical pillars evaluating competing perspectives (Liberal, Realist, Marxist, Communitarian, Feminist).
  3. *Scholars & Judicial Authorities:* Explicit list of thinkers, texts, and committee reports to cite for value addition.
  4. *In-Exam Visual Flowcharts:* High-scoring ASCII diagram schematics (e.g., V.R. Mehta's Paradigm, Manu's Constitutional Limits, Saptanga Hub-and-Spoke, Kaplan's Polarity Matrix) designed to be drawn in the exam hall.
  5. *Balanced Conclusion (30–40 words):* Forward-looking synthesis linking the theoretical debate to modern Indian constitutionalism or global governance.

### Universal Client-Side Search
- **Instant Live Search:** Filters across all section titles, subtitles, concepts, summaries, bullet points, and thinkers in real time.
- **Keyboard Friendly:** Press `Escape` or click the clear button to instantly reset.

---

## 7. How to Run the Application Manually

### Option 1: 1-Click Launch (Recommended for Daily Use)
Double-click the batch file located in the project root:
- **[start_app.bat](file:///c:/Users/ASUS%20VIVOBOOK/Documents/antigravity/jolly-mendel/start_app.bat)**  
It will automatically launch the server and open your default browser to `http://localhost:5173/`.

### Option 2: Running via Terminal (PowerShell / Command Prompt)
```powershell
# 1. Open PowerShell and navigate to the app directory
cd "c:\Users\ASUS VIVOBOOK\Documents\antigravity\jolly-mendel\app"

# 2. Start the Vite development server
npm run dev

# 3. Open your browser and navigate to:
# http://localhost:5173/
```

### Option 3: Production Build & Preview
If you want to run the optimized, minified production build:
```powershell
cd "c:\Users\ASUS VIVOBOOK\Documents\antigravity\jolly-mendel\app"

# Build the production bundle
npm run build

# Preview the production build
npm run preview
```

---

## 8. Data Compilation & Pipeline Automation

All transcribed markdown files in `transcriptions_*/` are converted into structured JavaScript datasets using automated Python scripts in `scripts/`:

```
transcriptions_*/batch_XX.md
         │
         ▼  (scripts/batch_parser_*.py)
    • Regex concept extractor (### Heading, bullets)
    • Flashcard extractor (**Q1:** / **A1:**)
    • Model answer extractor (### Model Answer:)
         │
         ▼  (scripts/build_*_dataset.py)
app/src/data/*.js (Clean ES Module exports)
```

### Compiler Scripts Reference:
- **Volume 1:** `python scripts/build_paper1_data_full.py` $\rightarrow$ `app/src/data/paper1IptData.js`
- **Volume 2:** `python scripts/build_paper1_part2_dataset.py` $\rightarrow$ `app/src/data/paper1Part2Data.js`
- **Volume 3:** `python scripts/build_paper1_part4_dataset.py` $\rightarrow$ `app/src/data/paper1Part4Data.js`
- **Volume 4:** `python scripts/build_paper1_part5_dataset.py` $\rightarrow$ `app/src/data/paper1Part5Data.js`
- **Volume 5:** `python scripts/build_part1_dataset.py` $\rightarrow$ `app/src/data/paper2IndiaWorldData.js`
- **Volume 6:** `python scripts/build_part2_dataset.py` $\rightarrow$ `app/src/data/paper2ComparativeData.js`

---

## 9. How to Modify, Update, or Add New Content

### To edit existing concepts, quotes, or notes:
1. Open the relevant markdown file in `transcriptions_*/` (e.g., `transcriptions_paper1/batch_1_intro_manu.md`).
2. Make your edits or add new bullet points under the appropriate `### Concept Title` heading.
3. Run the corresponding Python compiler script:
   ```powershell
   python scripts/build_paper1_data_full.py
   ```
4. The web application will immediately reflect the updated content via Vite's Hot Module Replacement (HMR).

### Formatting Rules for Transcriptions:
- **Concepts:** Use `### Concept Title` followed by at least two bullet points (`- ...`).
- **Scans:** Include an archival reference like `page_014.png` in the text so the compiler links the concept to that scan.
- **Flashcards:** Format as:
  ```markdown
  ### Active Recall Flashcards
  - **Q1:** Your question here?
    **A1:** Your detailed answer here.
  ```
- **Model Answers:** Format as:
  ```markdown
  ### Model Answer: Your Question Title Here (20 Marks)
  - **Question:** "Full question prompt..."
  - **Structure:**
    - **Introduction:** ...
    - **Body Paragraph 1:** ...
    - **Conclusion:** ...
  ```

---

## 10. Performance & Zero-Cost Infrastructure

| Parameter | Performance Metric / Design Choice |
| :--- | :--- |
| **API Costs** | **\$0.00 (Zero paid APIs, zero subscriptions)** |
| **Network Dependency** | **100% Offline Capable** (All assets and images stored locally) |
| **Build Time** | `tsc && vite build` completes in **<3 seconds** (1,935 modules transformed) |
| **Client Bundle Size** | Gzipped JS: **444 kB**; Gzipped CSS: **8.7 kB** |
| **Runtime Latency** | Sub-millisecond page and scan switching (Pure client-side state) |
| **Browser Compatibility** | Chrome, Edge, Firefox, Safari, Brave, Opera |

---

*Project successfully compiled, verified, and handed over.*
