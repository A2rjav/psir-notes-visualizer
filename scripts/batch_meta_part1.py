import os
import json
import re

TRANSCRIPTIONS_DIR = "transcriptions_part1"

def get_part1_metadata():
    batches = [
        {
            "batch_file": "batch_1_india_usa_relations.md",
            "id": "p2b-india-usa-relations",
            "number": "01",
            "title": "India-USA Relations: From Estranged to Engaged Democracies",
            "subtitle": "Cold War Distrust | Post-1991 Rapprochement | Civil Nuclear Agreement 123 | Strategic Partnership & Shared Values",
            "scanPages": list(range(1, 16)),
            "notebookPages": "Pages 1 to 15",
            "lecture": "India-USA Lecture Series",
            "keyScholars": ["C. Raja Mohan", "Dennis Kux", "Ashley Tellis", "Strobe Talbott"],
            "coreTheories": ["Dennis Kux Thesis: Estranged Democracies to Engaged Democracies", "The 123 Civil Nuclear Agreement: De-facto Nuclear Legitimacy", "Structural Realist Convergence vs Democratic Peace Theory", "Strategic Autonomy vs Alliance Entanglement", "Next Steps in Strategic Partnership (NSSP)"]
        },
        {
            "batch_file": "batch_2_india_usa_defense_economic_architecture.md",
            "id": "p2b-india-usa-defense-economic",
            "number": "02",
            "title": "India-USA Defense Agreements & Economic Architecture",
            "subtitle": "Foundational Defense Pacts (LEMOA, COMCASA, BECA) | 2+2 Ministerial Dialogue | Major Defense Partner | Trade & H1B Frictions",
            "scanPages": list(range(16, 31)),
            "notebookPages": "Pages 16 to 30",
            "lecture": "India-USA Defense Architecture",
            "keyScholars": ["Ashley Tellis", "C. Raja Mohan", "S. Jaishankar", "Shivshankar Menon"],
            "coreTheories": ["Foundational Defense Agreements (GSOMIA, LEMOA, COMCASA, BECA)", "Major Defense Partner (MDP) Status & DTTI", "2+2 Ministerial Dialogue: Institutionalizing High-Level Strategic Consensus", "Trade Frictions: Generalized System of Preferences (GSP), Tariffs, and H1B Visas", "Indo-Pacific Reorientation: Countering Revisionist Hegemony in Maritime Asia"]
        },
        {
            "batch_file": "batch_3_india_russia_strategic_partnership.md",
            "id": "p2b-india-russia-strategic-partnership",
            "number": "03",
            "title": "India-Russia Strategic Partnership: All-Weather Friendship to Multipolarity",
            "subtitle": "1971 Indo-Soviet Treaty | Special & Privileged Strategic Partnership | Defense Co-production (BrahMos, S-400) | Eurasian Geopolitics",
            "scanPages": list(range(31, 42)),
            "notebookPages": "Pages 31 to 41",
            "lecture": "India-Russia Lectures",
            "keyScholars": ["C. Raja Mohan", "Harsh V. Pant", "Dmitri Trenin", "Kanwal Sibal"],
            "coreTheories": ["The 1971 Treaty of Peace, Friendship and Co-operation: Diplomatic Shield", "Special and Privileged Strategic Partnership (Annual Summits)", "Defense Interdependence: Transfer of Technology, BrahMos, S-400, and Submarines", "Civil Nuclear Energy: Kudankulam Nuclear Power Plant", "Geopolitical Headwinds: Russia-China-Pakistan Axis vs Quad Dynamics"]
        },
        {
            "batch_file": "batch_4_india_china_historical_border_dispute.md",
            "id": "p2b-india-china-border-dispute",
            "number": "04",
            "title": "India-China Relations: Historical Ties, Panchsheel & The Border Dispute",
            "subtitle": "Hindi-Chini Bhai Bhai | Panchsheel 1954 | Tibet Issue & Dalai Lama | 1962 Border War | McMahon Line & Line of Actual Control (LAC)",
            "scanPages": list(range(42, 57)),
            "notebookPages": "Pages 42 to 56",
            "lecture": "India-China Lectures",
            "keyScholars": ["Neville Maxwell", "John Garver", "Shivshankar Menon", "Shyam Saran"],
            "coreTheories": ["Panchsheel Agreement 1954: Five Principles of Peaceful Coexistence", "The Tibet Question: Buffer State Demise, Dalai Lama's Asylum (1959)", "The 1962 Border Conflict: Forward Policy vs Chinese Pre-emptive Strike", "Line of Actual Control (LAC): Western (Aksai Chin), Middle, and Eastern Sectors (McMahon Line)", "Peace and Tranquillity Agreements (1993, 1996, 2005): Confidence Building Measures (CBMs)"]
        },
        {
            "batch_file": "batch_5_india_china_strategic_rivalry_geopolitics.md",
            "id": "p2b-india-china-strategic-rivalry",
            "number": "05",
            "title": "India-China: Strategic Rivalry, CPEC, Doklam & Economic Asymmetry",
            "subtitle": "Belt and Road Initiative (BRI) | CPEC Sovereignty Violation | Doklam Standoff | String of Pearls vs SAGAR | Trade Deficit",
            "scanPages": list(range(57, 74)),
            "notebookPages": "Pages 57 to 73",
            "lecture": "India-China Geopolitics",
            "keyScholars": ["Brahma Chellaney", "C. Raja Mohan", "Shyam Saran", "Alastair Iain Johnston"],
            "coreTheories": ["China-Pakistan Economic Corridor (CPEC): India's Territorial Sovereignty in PoK", "The String of Pearls Hypothesis vs Project Mausam and Sagarmala", "The Doklam Standoff (2017): Trilateral Junction and the Siliguri Corridor (Chicken's Neck)", "Economic Asymmetry: Unfavorable Trade Balance and Critical Raw Material Dependency", "Wuhan and Chennai Informal Summits: Asthana Consensus and Managing Competition"]
        },
        {
            "batch_file": "batch_6_india_japan_partnership_indopacific.md",
            "id": "p2b-india-japan-partnership",
            "number": "06",
            "title": "India-Japan Special Strategic Partnership & Indo-Pacific Convergence",
            "subtitle": "Confluence of the Two Seas (Shinzo Abe) | Civil Nuclear Agreement | Bullet Train (MAHSR) | Asia-Africa Growth Corridor (AAGC) | 2+2 Dialogue",
            "scanPages": list(range(74, 86)),
            "notebookPages": "Pages 74 to 85",
            "lecture": "India-Japan Lectures",
            "keyScholars": ["Shinzo Abe", "C. Raja Mohan", "Harsh V. Pant", "K.V. Kesavan"],
            "coreTheories": ["Shinzo Abe's Historic Speech: 'Confluence of the Two Seas' (2007)", "Special Strategic and Global Partnership: Institutional Alignment", "Civil Nuclear Cooperation Agreement (2016): Japan's Historic Concession to Non-NPT State", "Asia-Africa Growth Corridor (AAGC): A Democratic Alternative to China's BRI", "Infrastructure Diplomacy: North-East Connectivity and Western Dedicated Freight Corridor"]
        },
        {
            "batch_file": "batch_7_hegemonic_stability_rise_of_china.md",
            "id": "p2b-hegemonic-stability-rise-china",
            "number": "07",
            "title": "Hegemonic Stability Theory, The Rise of China & The Asian Century",
            "subtitle": "Kindleberger & Keohane | US Decline vs Chinese Power | Clash of Civilizations (Huntington) | Thucydides Trap (Graham Allison) | Balance of Power",
            "scanPages": list(range(86, 97)),
            "notebookPages": "Pages 86 to 96",
            "lecture": "Global Geopolitics Lectures",
            "keyScholars": ["Charles Kindleberger", "Robert Keohane", "Samuel Huntington", "Graham Allison", "John Mearsheimer"],
            "coreTheories": ["Hegemonic Stability Theory: The Hegemon Providing Global Public Goods", "The Thucydides Trap: Rising Power (China) Challenging Ruling Hegemon (USA)", "Samuel Huntington's Clash of Civilizations: Sinic-Confucian and Islamic vs Western Values", "Offensive Realism (Mearsheimer): Can China Rise Peacefully?", "India's Swing State Role: Net Security Provider in the Indian Ocean"]
        },
        {
            "batch_file": "batch_8_look_east_to_act_east_policy.md",
            "id": "p2b-look-east-act-east",
            "number": "08",
            "title": "India's Look East to Act East Policy: Southeast Asian Engagement",
            "subtitle": "Narasimha Rao 1991 Genesis | Shift to Act East (2014) | 3Cs: Commerce, Connectivity, Culture | Northeast India as Gateway | Security Architecture",
            "scanPages": list(range(97, 112)),
            "notebookPages": "Pages 97 to 111",
            "lecture": "Act East Policy Lectures",
            "keyScholars": ["C. Raja Mohan", "Prabhash Ranjan", "S.D. Muni", "S. Jaishankar"],
            "coreTheories": ["Look East Policy (1991): Post-Cold War Economic Reorientation by P.V. Narasimha Rao", "Act East Policy (2014): Transition from Economic Engagement to Strategic Security Partnership", "The 3Cs Framework: Commerce (Free Trade), Connectivity (Physical & Digital), Culture (Civilizational Buddhist ties)", "Northeast India as the Springboard: Kaladan Multi-Modal & India-Myanmar-Thailand Trilateral Highway", "Strategic Deepening: ADMM-Plus, East Asia Summit (EAS), and Maritime Domain Awareness"]
        },
        {
            "batch_file": "batch_9_southeast_asia_indopacific_maritime_security.md",
            "id": "p2b-southeast-asia-maritime-security",
            "number": "09",
            "title": "Southeast Asia, South China Sea & Indo-Pacific Maritime Security",
            "subtitle": "Freedom of Navigation (FONOPs) | UNCLOS Violations | Choke Points (Malacca Strait) | The Quad (India, USA, Japan, Australia) | SAGAR Vision",
            "scanPages": list(range(112, 120)),
            "notebookPages": "Pages 112 to 119",
            "lecture": "Indo-Pacific Maritime Security",
            "keyScholars": ["C. Raja Mohan", "Rory Medcalf", "David Brewster", "Abhijit Singh"],
            "coreTheories": ["Indo-Pacific as a Geopolitical Concept: Expanding from Asia-Pacific to Maritime Continuum", "South China Sea Disputes: Nine-Dash Line, UNCLOS Arbitral Award (2016), and FONOPs", "The Malacca Dilemma: Vulnerability of Energy Lifelines and Chokepoint Geopolitics", "The Quad (Quadrilateral Security Dialogue): Shared Vision of Free, Open, and Inclusive Indo-Pacific", "SAGAR (Security and Growth for All in the Region): India's Consultative Indian Ocean Vision"]
        },
        {
            "batch_file": "batch_10_united_nations_reforms_global_governance.md",
            "id": "p2b-un-reforms-global-governance",
            "number": "10",
            "title": "United Nations Reforms: UNSC Expansion & India's Permanent Seat",
            "subtitle": "1945 Anachronism | G4 Coalition (India, Brazil, Germany, Japan) | Coffee Club / Uniting for Consensus | UN Peacekeeping | Multilateralism Crisis",
            "scanPages": list(range(120, 133)),
            "notebookPages": "Pages 120 to 132",
            "lecture": "Lecture 23: United Nations & Global Governance",
            "keyScholars": ["Shashi Tharoor", "Ramesh Thakur", "Kishore Mahbubani", "Syed Akbaruddin"],
            "coreTheories": ["Anachronistic Architecture of the UN Security Council: 1945 Post-War Settlement vs 21st Century Multipolarity", "India's Legitimate Claim: Democracy, Population, Economic Weight, and Peacekeeping Contributions", "The G4 Coalition: Mutual Support for Permanent Membership with or without Veto", "Opposition Dynamics: The Coffee Club (Uniting for Consensus) and Chinese Tactical Blocking", "UN Peacekeeping Operations (UNPKO): India as Historic Troop-Contributing Nation"]
        },
        {
            "batch_file": "batch_11_wto_doha_round_food_security.md",
            "id": "p2b-wto-doha-round-food-security",
            "number": "11",
            "title": "World Trade Organization (WTO): Doha Round & India's Food Security",
            "subtitle": "Doha Development Agenda | Agricultural Subsidies (Green, Blue, Amber Boxes) | Bali Peace Clause | Trade Facilitation Agreement (TFA) | Dispute Settlement Crisis",
            "scanPages": list(range(133, 152)),
            "notebookPages": "Pages 133 to 151",
            "lecture": "Lecture 24 (01/05/2017): WTO & Global Trade Architecture",
            "keyScholars": ["Biswajit Dhar", "Jagdish Bhagwati", "Dani Rodrik", "Prabhash Ranjan"],
            "coreTheories": ["Doha Development Round Stalemate: Developed vs Developing World Divide", "Agricultural Subsidy Architecture: Green Box (Non-trade distorting), Blue Box (Production limiting), Amber Box (Trade distorting)", "Public Stockholding for Food Security: MSP Operations and the 10% De Minimis Ceiling", "The Bali Package (2013) & The Perpetual Peace Clause: Legal Shield for National Food Security Act", "Appellate Body Paralysis: US Unilateralism and the Crisis of Multilateral Dispute Settlement"]
        },
        {
            "batch_file": "batch_12_european_union_brexit_india_relations.md",
            "id": "p2b-european-union-brexit-india",
            "number": "12",
            "title": "The European Union, Eurozone Crisis, Brexit & India-EU Partnership",
            "subtitle": "Maastricht Treaty 1993 | Supranational Integration | Eurozone Sovereign Debt Crisis | Brexit Implications | India-EU BTIA Negotiations",
            "scanPages": list(range(152, 165)),
            "notebookPages": "Pages 152 to 164",
            "lecture": "European Union & Regional Blocs",
            "keyScholars": ["Babu Mathew", "Gulshan Sachdeva", "C. Raja Mohan", "Ulrich Beck"],
            "coreTheories": ["Theory of Regional Integration: Neo-functionalism and Spillover (Ernst Haas)", "The Eurozone Crisis: Monetary Union without Fiscal and Political Union", "Brexit and the Crisis of European Unity: Resurgence of Sovereignty and Right-Wing Populism", "India-EU Broad-based Trade and Investment Agreement (BTIA): Tariff and Data Security Hurdles", "Strategic Convergence: India and EU as Natural Partners in a Multipolar, Rules-Based Order"]
        },
        {
            "batch_file": "batch_13_asean_modi_diplomatic_doctrines.md",
            "id": "p2b-asean-modi-diplomatic-doctrines",
            "number": "13",
            "title": "ASEAN & Modi's Foreign Policy Doctrines: Neighbourhood First & SAGAR",
            "subtitle": "The ASEAN Way | ZOPFAN | 3 Community Pillars | Neighbourhood First | SAGAR | Fast-Track Diplomacy & Paradiplomacy",
            "scanPages": list(range(165, 181)),
            "notebookPages": "Pages 165 to 180",
            "lecture": "ASEAN & Contemporary Indian Foreign Policy Doctrines",
            "keyScholars": ["Amitav Acharya", "C. Raja Mohan", "S. Jaishankar", "S.D. Muni"],
            "coreTheories": ["The ASEAN Way: Consensus-building, Non-interference, and Informal Deliberation", "ZOPFAN (Zone of Peace, Freedom and Neutrality): Preventing Great Power Hegemony", "Three Pillars of ASEAN Community: Political-Security, Economic, and Socio-Cultural", "Neighbourhood First Policy: Asymmetric Concessions to Immediate South Asian Neighbors", "Modi's Foreign Policy Paradigms: Panchamrit, SAGAR, Fast-Track Diplomacy, and Paradiplomacy"]
        },
        {
            "batch_file": "batch_14_south_asian_regionalism_saarc_bimstec.md",
            "id": "p2b-saarc-bimstec-india-pakistan",
            "number": "14",
            "title": "South Asian Regionalism: SAARC Stagnation vs BIMSTEC Revival",
            "subtitle": "SAFTA Shortcomings | Pakistan's Obstructionism | Motor Vehicles Agreement (BBIN) | BIMSTEC as Bay of Bengal Bridge | Kashmir & Cross-Border Terrorism",
            "scanPages": list(range(181, 198)),
            "notebookPages": "Pages 181 to 197",
            "lecture": "South Asian Regionalism & India-Pakistan",
            "keyScholars": ["S.D. Muni", "C. Raja Mohan", "Constantino Xavier", "Happymon Jacob"],
            "coreTheories": ["Structural Asymmetry in South Asia: India's Centrality and Preponderance", "The Tragedy of SAARC: Consensus Rule Weaponized for Bilateral Spoilers", "Sub-Regional Alternatives: BBIN (Bangladesh, Bhutan, India, Nepal) Motor Vehicles Agreement", "BIMSTEC Revival: Integrating South Asia with Southeast Asia via the Bay of Bengal", "India-Pakistan Stalemate: Terrorism as an Instrument of State Policy and Uri/Pulwama Response"]
        },
        {
            "batch_file": "batch_15_india_pakistan_flashpoints_extended_neighbourhood.md",
            "id": "p2b-pakistan-flashpoints-extended-neighbourhood",
            "number": "15",
            "title": "India-Pakistan Flashpoints, Central Asia & West Asia De-hyphenation",
            "subtitle": "Indus Waters Treaty 1960 | Siachen & Sir Creek | Chabahar Port | Connect Central Asia | Link West & West Asia Triple Entente",
            "scanPages": list(range(198, 215)),
            "notebookPages": "Pages 198 to 214",
            "lecture": "Lecture 04/05/2017: Extended Neighbourhood & Strategic Synthesis",
            "keyScholars": ["Happymon Jacob", "C. Raja Mohan", "Brahma Chellaney", "S. Jaishankar"],
            "coreTheories": ["The Indus Waters Treaty (1960): World Bank Mediation and Current Geopolitical Pressures", "Border Flashpoints: Siachen Glacier Strategic Height and Sir Creek Marshland Delimitation", "Chabahar Port: Bypassing Pakistan to Unlock Access to Afghanistan and Central Asia", "Connect Central Asia Policy: 4Cs (Commerce, Connectivity, Consensual Security, Culture) & INSTC", "West Asia De-hyphenation: Simultaneous Strategic Engagement with Israel, Saudi Arabia, and Iran"]
        }
    ]
    return batches

if __name__ == "__main__":
    b = get_part1_metadata()
    print(f"Loaded {len(b)} batch metadata definitions for Part 1 Notes (Paper 2 Section B).")
