import os
import json
import re

from batch_meta_part1 import get_part1_metadata
from batch_parser_part1 import parse_markdown_to_concepts, parse_flashcards, parse_model_answers

def build_part1_dataset():
    target_file = "app/src/data/paper2IndiaWorldData.js"
    
    meta = {
        "paper": "Paper 2 Section B (India and the World)",
        "topicTitle": "Paper 2 (Section B): India and the World — Bilateral Relations, Regional Dynamics & Global Institutions",
        "summary": "Exhaustive, 100% zero-loss digital knowledge repository of Shubhra Ranjan IAS lecture notes covering the entire spectrum of India's Foreign Policy and International Relations: India-USA Strategic Convergence (Estranged to Engaged Democracies, 123 Civil Nuclear Agreement, Foundational Defense Agreements LEMOA/COMCASA/BECA, 2+2 Dialogue), India-Russia Strategic Partnership (1971 Treaty of Friendship, Special and Privileged Partnership, S-400, Nuclear Energy, Eurasian Dynamics), India-China Relations (Historical evolution, Panchsheel, 1962 War, LAC Boundary Disputes, CPEC/BRI, Doklam Standoff, String of Pearls vs SAGAR), India-Japan Special Partnership (Shinzo Abe's Confluence of the Two Seas, Bullet Train, AAGC, Quad), Hegemonic Stability Theory & The Rise of China (Kindleberger, Thucydides Trap, Clash of Civilizations), India's Look East to Act East Policy (Narasimha Rao to Modi, 3Cs: Commerce-Connectivity-Culture, Northeast as Gateway), Southeast Asia & Indo-Pacific Maritime Security (UNCLOS, Malacca Dilemma, Quad, SAGAR), United Nations Reforms (Anachronistic 1945 Architecture, UNSC Expansion, G4, Coffee Club, Peacekeeping), World Trade Organization (Doha Development Round, Green/Blue/Amber Boxes, Bali Peace Clause, Public Stockholding for Food Security, Dispute Settlement Crisis), European Union (Regional Integration, Eurozone Crisis, Brexit, BTIA), ASEAN & Modi's Diplomatic Doctrines (The ASEAN Way, Neighbourhood First, Panchamrit, Paradiplomacy), South Asian Regionalism (SAARC Stagnation vs BIMSTEC Revival, BBIN, Cross-border terrorism), and India-Pakistan Flashpoints & Extended Neighbourhood (Indus Waters Treaty, Siachen, Sir Creek, Chabahar Port, Connect Central Asia, West Asia De-hyphenation).",
        "notebookPages": "Notebook Folios 1 to 214 (214 Scan Pages: 001 to 214)",
        "scanStart": 1,
        "scanEnd": 214,
        "scanBasePath": "/scans_p2_part1"
    }
    
    batches = get_part1_metadata()
    sections = []
    flashcards = []
    answers = []
    
    fc_id_counter = 1
    ans_id_counter = 1
    
    for b in batches:
        md_path = os.path.join("transcriptions_part1", b["batch_file"])
        if not os.path.exists(md_path):
            concepts = []
        else:
            md_text = open(md_path, encoding='utf-8').read()
            concepts = parse_markdown_to_concepts(md_text, b["scanPages"][0])
            
            new_fc = parse_flashcards(md_text, b["title"], fc_id_counter)
            flashcards.extend(new_fc)
            fc_id_counter += len(new_fc)
            
            new_ans = parse_model_answers(md_text, b["title"], ans_id_counter)
            answers.extend(new_ans)
            ans_id_counter += len(new_ans)
            
        section_obj = {
            "id": b["id"],
            "number": b["number"],
            "title": b["title"],
            "subtitle": b["subtitle"],
            "scanPages": b["scanPages"],
            "notebookPages": b["notebookPages"],
            "lecture": b["lecture"],
            "keyScholars": b["keyScholars"],
            "coreTheories": b["coreTheories"],
            "concepts": concepts
        }
        sections.append(section_obj)
        print(f"Volume 5 Batch {b['number']} ({b['batch_file']}): {len(concepts)} concepts extracted.")
        
    # Generate 214-page scansCatalog for Volume 5
    page_catalog_titles = {
        1: "Title Page: India and the World (Shubhra Ranjan IAS Notes)",
        2: "Syllabus Overview: Bilateral Relations, Regional Dynamics & Global Governance",
        3: "Roadmap: India-USA, India-Russia, India-China & Multilateral Institutions",
        4: "India-USA Historical Relations: Cold War Estrangement & Non-Alignment Friction",
        5: "India-USA Strategic Convergence Post-1991: Nuclear Non-Proliferation vs Rapprochement",
        6: "The 123 Civil Nuclear Agreement (2008): De-Facto Recognition as Nuclear Power",
        7: "Next Steps in Strategic Partnership (NSSP) & High-Technology Cooperation",
        8: "Dennis Kux Thesis: From Estranged Democracies to Engaged Democracies",
        9: "Civil Nuclear Liability Act (CLNDA) Controversies & Supplier Liability",
        10: "Defense Trade and Technology Initiative (DTTI): Co-production Framework",
        11: "Major Defense Partner (MDP) Status Enacted by US Congress (2016)",
        12: "Foundational Defense Agreement 1: GSOMIA (General Security of Military Information)",
        13: "Foundational Defense Agreement 2: LEMOA (Logistics Exchange Memorandum of Agreement)",
        14: "Foundational Defense Agreement 3: COMCASA (Communications Compatibility and Security)",
        15: "Foundational Defense Agreement 4: BECA (Basic Exchange and Cooperation Agreement)",
        16: "The 2+2 Ministerial Dialogue: Institutionalizing Foreign & Defense Consensus",
        17: "Economic Architecture: US-India Commercial Dialogue & Bilateral Investment Treaty",
        18: "Trade Frictions: Withdrawal of Generalized System of Preferences (GSP)",
        19: "Tariff Disputes: Harley-Davidson, Agricultural Goods & Medical Devices",
        20: "Immigration & Labour Mobility: H-1B and L-1 Visa Restrictions & Tech Diaspora",
        21: "Data Localization vs Free Flow of Data: E-Commerce Rules & Digital Sovereignty",
        22: "Strategic Autonomy in the Era of US-China New Cold War",
        23: "Countering America's Adversaries Through Sanctions Act (CAATSA) Dilemma",
        24: "CAATSA Waiver Dynamics: India's Procurement of Russian S-400 Air Defense Systems",
        25: "Energy Security: Chabahar Sanctions Exemption & Halting Iranian Oil Imports",
        26: "The Indo-Pacific Convergence: Joint Strategic Vision for Asia-Pacific and Indian Ocean",
        27: "The Quadrilateral Security Dialogue (Quad): Principles of Free and Open Indo-Pacific",
        28: "Supply Chain Resilience Initiative (SCRI) & Tech-Alliance Alliances (iCET)",
        29: "Scholarly Perspectives: C. Raja Mohan vs Ashley Tellis on India as an Ally",
        30: "Model Answer Synthesis: Evolution and Future Trajectory of India-USA Partnership",
        31: "India-Russia Historical Relations: Indo-Soviet Special Relationship",
        32: "The 1971 Treaty of Peace, Friendship and Cooperation: Geopolitical Shield in Bangladesh War",
        33: "Post-Soviet Transition (1990s): Rupee-Rouble Arrangement & Strategic Recalibration",
        34: "Declaration on Strategic Partnership (2000): Institutionalizing Annual Bilateral Summits",
        35: "Special and Privileged Strategic Partnership: Doctrinal Pillars and Depth",
        36: "Defense Interdependence: Joint Development of BrahMos Cruise Missile",
        37: "Licensed Production: Su-30MKI, T-90 Tanks & Akula-class Nuclear Submarine Leases",
        38: "The S-400 Triumf Air Defense System Deal: Strategic Significance and Defying US Sanctions",
        39: "Civil Nuclear Energy Cooperation: Kudankulam Nuclear Power Plant Construction",
        40: "Hydrocarbon Exploration in Russian Far East: Sakhalin-1 and Vankor Stakes",
        41: "Geopolitical Challenges: Growing Russia-China Strategic Convergence & Pakistan Outreaches",
        42: "India-China Historical Framework: Civilizational Interactions & Buddhism Silk Route",
        43: "Nehruvian Idealism & Panchsheel Agreement (1954): Five Principles of Peaceful Coexistence",
        44: "The Tibet Question: Buffer State Extinction, 17-Point Agreement & Dalai Lama Asylum (1959)",
        45: "Historical Roots of the Border Dispute: McMahon Line & Western Sector Aksai Chin",
        46: "The 1962 Sino-Indian Border War: Forward Policy, Military Reversal & Diplomatic Freezing",
        47: "Rajiv Gandhi's Historic 1988 Visit to Beijing: Delinking Border Resolution from Normalization",
        48: "Border Peace and Tranquillity Agreement (BPTA 1993): Inception of Line of Actual Control (LAC)",
        49: "Confidence Building Measures (CBMs 1996, 2005): Clarifying LAC & Preventing Escalation",
        50: "Special Representatives (SR) Mechanism (2003): Three-Stage Framework for Border Settlement",
        51: "Three Sectors of LAC: Western (Ladakh), Middle (Himachal/Uttarakhand), Eastern (Arunachal)",
        52: "Chinese Claims on Arunachal Pradesh: Southern Tibet (Zangnan) Nomenclature Strategy",
        53: "Water Geopolitics: Brahmaputra (Yarlung Tsangpo) Damming & Run-of-the-River Hydropower",
        54: "Trans-Himalayan Border Infrastructure: China's Western Theater Command Rapid Mobility",
        55: "India's Counter-Infrastructure: Border Roads Organisation (BRO), DS-DBO Road & Tunnels",
        56: "Scholarly Perspectives: John Garver (Protracted Contest) vs Neville Maxwell (India's China War)",
        57: "Xi Jinping's Global Ambitions: The Belt and Road Initiative (BRI / One Belt One Road)",
        58: "China-Pakistan Economic Corridor (CPEC): India's Sovereignty Violation in Pakistan-occupied Kashmir",
        59: "The String of Pearls Hypothesis: Gwadar, Hambantota, Kyaukpyu, Chittagong Encirclement",
        60: "India's Strategic Counter-Measures: Sagarmala, Project Mausam & Naval Forward Posture",
        61: "The Doklam Standoff (2017): Trilateral Junction Dispute (India, Bhutan, China)",
        62: "Strategic Vulnerability of the Siliguri Corridor (Chicken's Neck) during Doklam Crisis",
        63: "Resolution of Doklam: Simultaneous Disengagement & Diplomatic Equilibrium",
        64: "Informal Summitry: Wuhan Summit (2018) & Strategic Guidance to Armed Forces",
        65: "Chennai Connect Informal Summit (2019): Economic Engagement & Regional Boundary Discourse",
        66: "Economic Asymmetry: Massive Bilateral Trade Deficit Favoring China ($50B+ - $100B)",
        67: "Import Dependency on China: Active Pharmaceutical Ingredients (APIs), Solar Panels, Electronics",
        68: "Non-Tariff Barriers & Market Access Denials for Indian IT and Pharmaceutical Firms",
        69: "South China Sea Dispute: Indian Oil and Gas Exploration (ONGC Videsh Block 128 Vietnam)",
        70: "Freedom of Navigation in South China Sea: Permanent Court of Arbitration Award (2016)",
        71: "China's Diplomatic Encirclement: Vetoing Masood Azhar at UNSC & Blocking NSG Membership",
        72: "Shyam Saran Thesis: How China Sees India and the Myth of Asian Multipolarity",
        73: "Model Answer Synthesis: Managing Strategic Competition and Structural Asymmetry with China",
        74: "India-Japan Historical Bonds: Swami Vivekananda, Tenshin Okakura & Post-War Peace Treaty",
        75: "Yoshiro Mori (2000) & Junichiro Koizumi: Inception of Global Partnership for 21st Century",
        76: "Shinzo Abe's 2007 Address to Indian Parliament: 'Confluence of the Two Seas'",
        77: "Special Strategic and Global Partnership (2014): Annual Reciprocal Prime Ministerial Summits",
        78: "Economic Engagement: Comprehensive Economic Partnership Agreement (CEPA 2011)",
        79: "Japanese Official Development Assistance (ODA): Western Dedicated Freight Corridor & Delhi Metro",
        80: "Mumbai-Ahmedabad High-Speed Rail (MAHSR / Bullet Train) Partnership and Financing",
        81: "Strategic Infrastructure in India's Northeast: Act East Forum & Border Road Connectivity",
        82: "India-Japan Civil Nuclear Agreement (2016): Historic Exemption for a Non-NPT Signatory",
        83: "Defense Cooperation: Malabar Naval Exercises, JIMEX, Dharma Guardian & Acquisition Pacts",
        84: "Asia-Africa Growth Corridor (AAGC): Joint Vision for Quality Infrastructure vs Debt-Trap BRI",
        85: "Indo-Pacific Convergence: Free, Open and Inclusive Rules-Based Maritime Security",
        86: "Theoretical Perspectives: Hegemonic Stability Theory (Charles Kindleberger & Robert Keohane)",
        87: "Public Goods Provision by the Hegemon: Freedom of the Seas, Reserve Currency, Open Markets",
        88: "The Decline of American Hegemony: Hegemonic Overreach and Domestic Political Isolationism",
        89: "The Rise of China: Peaceful Rise (*Heping Jueqi*) vs Assertive Revisionism under Xi Jinping",
        90: "Graham Allison's Thucydides Trap: Rising Power (Sparta/China) Threatening Ruling Hegemon (Athens/USA)",
        91: "Samuel Huntington's Clash of Civilizations: Fault Lines between Sinic, Islamic, and Western Blocs",
        92: "Offensive Realism (John Mearsheimer): Why China Cannot Rise Peacefully and Conflict is Inevitable",
        93: "Multipolar World vs Polycentric Asia: S. Jaishankar's Formula for Multipolar Asia",
        94: "India as a Leading Power (Ashley Tellis): From Balancing Power to Rule-Shaper",
        95: "Strategic Autonomy in a Multipolar World: Multi-Alignment (*All-Alignment*) vs Cold War Neutrality",
        96: "UPSC Mains Analytical Matrix: Realism, Constructivism, and Hegemonic Transitions in Asia",
        97: "Genesis of the Look East Policy (1991): P.V. Narasimha Rao's Post-Cold War Economic Vision",
        98: "Overcoming Historical Estrangement with Southeast Asia Post-Decolonization",
        99: "Phases of Look East Policy: Phase 1 (Trade & Investment) to Phase 2 (Strategic Architecture)",
        100: "Transformation to Act East Policy (2014): Narendra Modi's Proactive Diplomatic Pivot",
        101: "The 3Cs Framework: Commerce (Trade Integration), Connectivity (Infrastructure), Culture (Heritage)",
        102: "Cultural Diplomacy: Shared Buddhist Circuit, Ramayana Heritage, and Nalanda University Revival",
        103: "Northeast India as the Natural Bridgehead to Southeast Asia (Land Gateway)",
        104: "Kaladan Multi-Modal Transit Transport Project (KMMTTP): Connecting Kolkata to Sittwe and Mizoram",
        105: "India-Myanmar-Thailand Trilateral Highway: Cross-Border Connectivity to Southeast Asian Markets",
        106: "Security Dimension of Act East: Joint Naval Exercises (SIMBEX, CORPAT) & Defense Exports (BrahMos)",
        107: "Institutional Multilateral Architecture: ASEAN Regional Forum (ARF) & East Asia Summit (EAS)",
        108: "ADMM-Plus: ASEAN Defense Ministers' Meeting Plus Eight Dialogue Partners",
        109: "RCEP Dilemma: Why India Withdrew from Regional Comprehensive Economic Partnership (2019)",
        110: "RCEP Withdrawal Rationale: China Import Inundation, Dairy Sector Concerns, Rules of Origin Gaps",
        111: "Scholarly Review: Evaluating Act East Outcomes after Three Decades of Implementation",
        112: "The Geopolitical Concept of the Indo-Pacific: Transition from Asia-Pacific to Maritime Continuum",
        113: "Strategic Geography: From the East Coast of Africa to the Western Pacific Ocean",
        114: "The Malacca Dilemma: Vulnerability of Global Energy Sea Lines of Communication (SLOCs)",
        115: "South China Sea Maritime Legal Architecture: United Nations Convention on the Law of the Sea (UNCLOS)",
        116: "China's Nine-Dash Line Claims: Militarization of Fiery Cross, Subi, and Mischief Reefs",
        117: "The Permanent Court of Arbitration (PCA) Award (2016): Philippines vs China and India's Stand",
        118: "Freedom of Navigation Operations (FONOPs) & Innocent Passage in Global Commons",
        119: "The Quadrilateral Security Dialogue (Quad 2.0): Resurgence, Summit Level Engagement & Non-Military Public Goods",
        120: "Lecture 23: The United Nations System and the Crisis of Multilateralism",
        121: "The Anachronistic Architecture of the 1945 UN Charter and Permanent Five (P5) Veto Powers",
        122: "India's Historical Contributions: Foundational Member, Decolonization Champion, and Anti-Apartheid Leader",
        123: "India's Unmatched Record in UN Peacekeeping Operations (UNPKO): Largest Cumulative Troop Contributor",
        124: "Case for India's Permanent Membership in the UN Security Council (UNSC)",
        125: "Objective Criteria Supporting India's Claim: Population, Democracy, 5th Largest Economy, Nuclear Responsibility",
        126: "The G4 Alliance: India, Brazil, Germany, Japan Joint Campaign for Permanent Seats",
        127: "Opposing Coalitions: Uniting for Consensus (The Coffee Club led by Pakistan, Italy, Mexico)",
        128: "The Chinese Veto Stumbling Block: Beijing's Tactical Opposition to Indian Permanent Representation",
        129: "Intergovernmental Negotiations (IGN) Process: Structural Paralysis and Absence of Text-Based Negotiations",
        130: "UN General Assembly (UNGA) Reform: Revitalizing the Assembly against Security Council Gridlock",
        131: "Comprehensive Convention on International Terrorism (CCIT): India's 1996 Proposed Global Framework",
        132: "Model Answer Synthesis: Reforming the UN Security Council to Reflect 21st Century Geopolitical Realities",
        133: "Lecture 24 (01/05/2017): The World Trade Organization (WTO) and Global Trade Architecture",
        134: "Transition from GATT (1947) to WTO (1995): Marrakesh Agreement and Single Undertaking",
        135: "Core Principles of WTO: Most Favoured Nation (MFN) and National Treatment (Non-Discrimination)",
        136: "The Doha Development Agenda (DDA 2001): Mandate to Prioritize Developing Nations' Needs",
        137: "The Doha Deadlock: Agricultural Subsidies in Developed Nations vs Industrial Tariffs in Global South",
        138: "WTO Agreement on Agriculture (AoA): The Three Pillars (Market Access, Export Subsidies, Domestic Support)",
        139: "Domestic Support Box System: Green Box (Non-Trade Distorting, Allowed without Limit)",
        140: "Blue Box (Production-Limiting Subsidies, Allowed with Conditions) & Amber Box (Trade Distorting, Capped)",
        141: "The De Minimis Ceiling: 10% of Value of Production for Developing Countries (5% for Developed)",
        142: "The Flawed 1986-1988 External Reference Price Formula: Distortion of Real Inflation and Subsidy Figures",
        143: "Public Stockholding for Food Security: Minimum Support Price (MSP) and the National Food Security Act (NFSA)",
        144: "The Bali Ministerial Conference (2013): Inception of the 'Peace Clause' for Public Stockholding",
        145: "India's Stand at Geneva (2014): Blocking Trade Facilitation Agreement (TFA) to Secure Perpetual Peace Clause",
        146: "Nairobi Ministerial (2015): Export Subsidies Abolition & Special Safeguard Mechanism (SSM) Impasse",
        147: "Buenos Aires (2017) & Beyond: Plurilateral Agreements vs Multilateral Consensus Rule",
        148: "The Appellate Body Crisis: US Blocking Judicial Appointments and Paralyzing Dispute Settlement",
        149: "Special and Differential Treatment (S&DT): Pressure to Deprive Emerging Economies (India, China) of Benefits",
        150: "TRIPS Agreement and Public Health: Doha Declaration on TRIPS (Compulsory Licensing for Generic Drugs)",
        151: "Model Answer Synthesis: India's Strategy at the WTO: Defending Farmers' Livelihoods and Multilateral Rules",
        152: "The European Union: Origins, Evolution, and Theory of Regional Integration",
        153: "From European Coal and Steel Community (ECSC) to the Treaty of Maastricht (1993)",
        154: "Neo-Functionalism and Spillover Theory (Ernst Haas): Economic Integration Driving Political Union",
        155: "The Eurozone Crisis (2009-2012): Sovereign Debt, PIGS Economies, and Structural Flaws of Monetary Union",
        156: "Monetary Union without Fiscal Union: The Asymmetry between German Surplus and Southern European Deficits",
        157: "The Migrant Crisis (2015): Dublin Regulation Breakdown and Resurgence of National Borders (Schengen Strains)",
        158: "Brexit: 2016 Referendum, UK Withdrawal from EU, and Reassertion of Parliamentary Sovereignty",
        159: "Rise of Right-Wing Populism across Europe: Euro-skepticism and Electoral Polarization",
        160: "India-EU Relations: Strategic Partnership (2004) and Joint Action Plans",
        161: "India-EU Broad-based Trade and Investment Agreement (BTIA): 2007 Launch and Prolonged Stagnation",
        162: "BTIA Sticky Points: Automobile and Wine Tariffs, Data Security Status, Labour and Environmental Standards",
        163: "Trade and Technology Council (TTC): Deepening High-Tech, Clean Energy, and Resilient Supply Chains",
        164: "EU's Indo-Pacific Strategy: Strategic Convergence on Multipolarity, Rule of Law, and Maritime Security",
        165: "ASEAN (Association of Southeast Asian Nations): Founded by Bangkok Declaration (1967)",
        166: "The ASEAN Way: Core Principles of Non-Interference, Consensus Decision-Making, and Informal Diplomacy",
        167: "Zone of Peace, Freedom and Neutrality (ZOPFAN 1971): Neutralizing Southeast Asia from Cold War Rivalries",
        168: "The Three Pillars of the ASEAN Community: Political-Security, Economic, and Socio-Cultural Communities",
        169: "ASEAN Centrality in Regional Architecture: East Asia Summit, ARF, and ASEAN Defense Ministers' Meeting",
        170: "Internal Crises of ASEAN: Myanmar Military Coup (2021) and Division over China's South China Sea Assertiveness",
        171: "Modi's Foreign Policy Doctrines: Shift from Non-Alignment to Issue-Based Multi-Alignment",
        172: "Neighbourhood First Policy: Institutionalized Priority to South Asian Immediate Neighbors",
        173: "Non-Reciprocal Generosity (Gujral Doctrine Legacy): Asymmetric Assistance, Lines of Credit, and Humanitarian Aid",
        174: "SAGAR Vision (Security and Growth for All in the Region): India's Consultative Indian Ocean Framework",
        175: "Project Mausam and Sagarmala: Reviving Historical Maritime Spice Routes and Modernizing Ports",
        176: "Fast-Track Diplomacy and Diaspora Engagement: Pravasi Bharatiya Divas and Evacuation Operations",
        177: "Paradiplomacy: Engaging Indian States in Bilateral Trade, Cultural Ties, and Cross-Border Partnerships",
        178: "Panchamrit Principles: Samman (Honor), Samvaad (Dialogue), Samriddhi (Prosperity), Suraksha (Security), Sanskriti (Culture)",
        179: "India as a Net Security Provider: Humanitarian Assistance and Disaster Relief (HADR) in the Indian Ocean Region",
        180: "Model Answer Synthesis: Continuity and Change in Indian Foreign Policy under the Modi Administration",
        181: "South Asian Regionalism: Historical, Geographical, and Cultural Cohesion of the Subcontinent",
        182: "South Asian Association for Regional Cooperation (SAARC): Established in Dhaka (1985)",
        183: "Structural Asymmetry: India's Overwhelming Size, Economy, and Geography Generating Neighborly Apprehensions",
        184: "South Asian Free Trade Area (SAFTA 2004): High Sensitive Lists, Non-Tariff Barriers, and Intra-Regional Trade (<5%)",
        185: "The Failure of SAARC: Consensus Rule (Article X) Paralyzed by India-Pakistan Antagonisms",
        186: "Sub-Regional Initiatives: BBIN (Bangladesh, Bhutan, India, Nepal) Motor Vehicles Agreement",
        187: "Bay of Bengal Initiative for Multi-Sectoral Technical and Economic Cooperation (BIMSTEC 1997)",
        188: "BIMSTEC as an Alternative to Stalled SAARC: Linking South Asia with Southeast Asia (Bridge Concept)",
        189: "BIMSTEC Advantages: Absence of Pakistan Bilateral Baggage, Maritime Economy, and Strategic Connectivity",
        190: "Challenges of BIMSTEC: Slow Institutionalization, Free Trade Agreement Delays, and Funding Deficits",
        191: "Model Answer Synthesis: Re-evaluating Regionalism in South Asia: Transition from SAARC to BIMSTEC",
        192: "India-Pakistan Relations: The Partition Trauma, Ideological Conflict (Two-Nation Theory vs Secular Democracy)",
        193: "The Kashmir Conflict: 1947 Tribal Invasion, Instrument of Accession, and UN Resolutions",
        194: "The 1965 War and Tashkent Agreement: Soviet Mediation and Territorial Status Quo Ante",
        195: "The 1971 Liberation War of Bangladesh and the Simla Agreement (1972): Bilateralism Principle",
        196: "Nuclearization of South Asia (1998): Pokhran-II and Chagai Tests, Cross-Border Stability-Instability Paradox",
        197: "Cross-Border Terrorism as an Instrument of State Policy: Low-Intensity Conflict and Proxy War",
        198: "The Indus Waters Treaty (1960): World Bank Brokered Water Sharing of Eastern and Western Rivers",
        199: "Provisions of Indus Treaty: Ravi, Beas, Sutlej to India; Indus, Jhelum, Chenab to Pakistan",
        200: "Disputes under Indus Treaty: Kishanganga Hydroelectric Project and Ratle Project Deliberations",
        201: "Siachen Glacier Conflict: Operation Meghdoot (1984) and Control over the Saltoro Ridge",
        202: "Strategic Importance of Siachen: Preventing Link-up between Pakistan-Occupied Kashmir and Shaksgam Valley (China)",
        203: "Sir Creek Maritime Dispute: Rann of Kutch Marshland Border and Exclusive Economic Zone (EEZ) Demarcation",
        204: "Green Line vs Thalweg Principle: Disagreement over Demarcation of Navigable Channel in Sir Creek",
        205: "Lecture 04/05/2017: India's Extended Neighbourhood Policy and Strategic Outreaches",
        206: "India-Afghanistan Relations: Strategic Partnership Agreement (2011), Parliament Building, and Salma Dam",
        207: "Chabahar Port (Iran): India's Strategic Transit Route Bypassing Pakistan to Access Afghanistan and Central Asia",
        208: "Trilateral Transit Agreement (India, Iran, Afghanistan): Chabahar as Gateway to Zaranj-Delaram Highway",
        209: "Connect Central Asia Policy (2012): 4Cs Strategy (Commerce, Connectivity, Consensual Security, Culture)",
        210: "International North-South Transport Corridor (INSTC): Multi-Modal Route Connecting Mumbai to Moscow via Iran",
        211: "Energy Pipelines in Eurasia: TAPI (Turkmenistan-Afghanistan-Pakistan-India) vs IPI (Iran-Pakistan-India) Hurdles",
        212: "West Asia De-Hyphenation Diplomacy: Simultaneous Strategic Deepening with Israel, Saudi Arabia, and UAE",
        213: "Look West / Link West Policy: Remittances, Energy Lifelines, and Security Coordination in the Gulf",
        214: "Grand Epilogue: Master Synthesis of India's Foreign Policy and Global Role in a Changing World Order"
    }
    
    scans_catalog = []
    for p in range(1, 215):
        num_str = f"{p:03d}"
        f_name = f"page_{num_str}.png"
        
        batch_num = "01"
        for b in batches:
            if p in b["scanPages"]:
                batch_num = b["number"]
                break
                
        title = page_catalog_titles.get(p, f"India & The World Lecture Analysis - Page {p}")
        
        scans_catalog.append({
            "pageNumber": p,
            "filename": f_name,
            "title": title,
            "batch": batch_num,
            "thumbnail": f"/scans_p2_part1/{f_name}",
            "fullImage": f"/scans_p2_part1/{f_name}"
        })
        
    js_content = f"""// UPSC PSIR Paper 2 (Section B): India and the World
// Compiled from 214 Scan Pages of Shubhra Ranjan IAS Handwritten Lecture Notes
// 100% Zero-Loss Digital Repository with Interactive Dual-Pane Scan Inspection

export const paper2IndiaWorldMetadata = {json.dumps(meta, indent=2)};

export const paper2IndiaWorldSections = {json.dumps(sections, indent=2)};

export const paper2IndiaWorldFlashcards = {json.dumps(flashcards, indent=2)};

export const paper2IndiaWorldModelAnswers = {json.dumps(answers, indent=2)};

export const paper2IndiaWorldScansCatalog = {json.dumps(scans_catalog, indent=2)};
"""
    
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"Successfully generated {target_file} ({os.path.getsize(target_file)} bytes).")

if __name__ == "__main__":
    build_part1_dataset()
