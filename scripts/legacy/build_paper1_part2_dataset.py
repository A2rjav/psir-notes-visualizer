import os
import json
import re

from batch_meta_p1_part2 import get_paper1_part2_metadata
from batch_parser_p1_part2 import parse_markdown_to_concepts, parse_flashcards, parse_model_answers

def build_paper1_part2():
    target_file = "app/src/data/paper1Part2Data.js"
    
    meta = {
        "paper": "Paper 1 (Part 2)",
        "topicTitle": "Paper 1 (Part 2): Indian Government and Politics (Grassroots to Sovereignty)",
        "summary": "Exhaustive, 100% zero-loss digital repository of Shubhra Ranjan IAS lecture notes covering Grassroots Democracy (Panchayati Raj, 73rd/74th CA, PESA Act 1996, 3Fs deficit, 2nd ARC), Judiciary (Judicial Review, Judicial Activism, PIL/SAL, Upendra Baxi vs Pratap Bhanu Mehta, Judges Cases, Collegium vs NJAC 99th CA, Judicial Overreach), Union Parliament (World Bank 6 Parameters, Decline of Parliament, DRSCs, Bicameralism), Union Executive (President, Prime Minister, PMO vs Cabinet Secretariat), Social Movements (Ramachandra Guha, Environmental Struggles, Women's Movement, Dalit Panthers & Kanshi Ram, Peasant Struggles), Planning and Economic Development (Nehru-Mahalanobis, 1991 LPG, Tendulkar vs Rangarajan, NITI Aayog), Land Reforms & Green Revolution, Constitutionalism & Basic Structure Doctrine (Kesavananda to Minerva Mills, I.R. Coelho), Affirmative Action & Deprivation Index, Farmers' Movements as Pressure Groups (BKU vs Shetkari Sangathan), and Theories of Sovereignty (Austin Monism vs Laski Pluralism) & RSS Pressure Group Analysis.",
        "notebookPages": "Pages 115 to 186 (150 Scan Pages: 001 to 150)",
        "scanStart": 1,
        "scanEnd": 150,
        "scanBasePath": "/scans_p1_part2"
    }
    
    batches = get_paper1_part2_metadata()
    sections = []
    flashcards = []
    answers = []
    
    fc_id_counter = 1
    ans_id_counter = 1
    
    for b in batches:
        md_path = os.path.join("transcriptions_paper1_part2", b["batch_file"])
        if not os.path.exists(md_path):
            print(f"Pending batch: {b['batch_file']}")
            concepts = []
        else:
            md_text = open(md_path, encoding='utf-8').read()
            concepts = parse_markdown_to_concepts(md_text, b["scanPages"][0])
            
            # Flashcards
            new_fc = parse_flashcards(md_text, b["title"], fc_id_counter)
            flashcards.extend(new_fc)
            fc_id_counter += len(new_fc)
            
            # Model answers
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
        print(f"Batch {b['number']} ({b['batch_file']}): {len(concepts)} concepts extracted.")
        
    # Generate 150-page scansCatalog
    page_catalog_titles = {
        1: "Part II Notes Title & Cover (Vajiram & Ravi, Shubhra Ranjan)",
        2: "Table of Contents: Grassroot Democracy, Judiciary, Parliament, Executive",
        3: "Table of Contents: Social Movements, Planning & Economic Development",
        4: "Course Syllabus Overview & Structural Roadmap",
        5: "Grassroots Democracy: Definition, Swaraj, Radical Democracy & Antyodaya",
        6: "Why Grassroots Democracy: Good Governance, Sustainable Development & Civic Education",
        7: "Constituent Assembly Clashes: Gandhian Village Republics vs Ambedkar Modernism",
        8: "Neglect of Urban Local Bodies & Article 40 DPSP Compromise",
        9: "Evolution of Panchayati Raj: Phase I (1950s) to Phase IV (Disillusionment)",
        10: "Balwant Rai Mehta Committee (1957) & Inauguration at Nagaur, Rajasthan",
        11: "Ashok Mehta Committee (1977): 2-Tier Model & Political Party Participation",
        12: "L.M. Singhvi Committee (1986): Constitutional Recognition Mandate",
        13: "73rd Constitutional Amendment Act (1992): Salient Features & Architecture",
        14: "Three-Tier Structure: Gram Panchayat, Panchayat Samiti & Zilla Parishad",
        15: "Reservation of Seats: 33% Women & SC/ST Proportional Quotas",
        16: "Gram Sabha as Pillar of Direct Deliberative Democracy",
        17: "PESA Act 1996: Bhuria Committee & Tribal Customary Self-Rule",
        18: "Evaluation of PRIs: The 3Fs Deficit (Funds, Functions, Functionaries)",
        19: "Sociological Realities: Sarpanch-Pati Syndrome & Dominant Caste Capture",
        20: "2nd ARC Recommendations on Local Governance & Fiscal Devolution",
        21: "74th Constitutional Amendment: Urban Local Bodies & Municipalities",
        22: "Smart Cities & Parastatal Agencies: Democratic Deficit (Ahluwalia)",
        23: "Women Empowerment in PRIs: Empirical Impact & Rohini Pande Studies",
        24: "Grassroots Micro-Movements: National Alliance of People's Movements (NAPM)",
        25: "Rajni Kothari: Non-Party Political Formations (NPPFs) as Countervailing Force",
        26: "Smitu Kothari & Amrita Basu: Grassroots Resistance to Globalisation",
        27: "Judiciary Blueprint: Lord Bryce's Dictum on Judicial Excellence",
        28: "7 Core UPSC PSIR Examination Questions on Indian Judiciary",
        29: "Transformative Constitutionalism & Granville Austin's Social Revolution",
        30: "Supreme Court Jurisdiction: Original, Appellate, Advisory & Article 142",
        31: "Judicial Review: Marbury v. Madison (1803) & Articles 13, 32, 226",
        32: "Procedure Established by Law vs Due Process of Law (A.K. Gopalan 1950)",
        33: "Maneka Gandhi Landmark (1978): Just, Fair & Reasonable Due Process",
        34: "Genesis of Judicial Activism: Post-Emergency Penitence & Article 39A",
        35: "Public Interest Litigation (PIL): Relaxation of Locus Standi & Epistolary Writ",
        36: "Upendra Baxi: Social Action Litigation (SAL) for the Impoverished",
        37: "Creative Expansion of Article 21: Right to Clean Air, Privacy & Livelihood",
        38: "Pratap Bhanu Mehta's Critique: Judiciary as Self-Appointed Guardian",
        39: "Paradoxical Institution: Most Trusted yet Least Transparent",
        40: "Judicial Activism vs Judicial Overreach: The Thin Dividing Line",
        41: "Judges Appointment Framework: Article 124(2) & 217(1) Intent",
        42: "First Judges Case (1981 - S.P. Gupta): Executive Primacy Upheld",
        43: "Second Judges Case (1993 - SCAORA): Birth of the Collegium System",
        44: "Third Judges Case (1998 - Special Reference): CJI + 4 Senior-Most Judges",
        45: "Pathologies of Collegium: Uncle Judges Syndrome & Lack of Transparency",
        46: "National Judicial Appointments Commission (NJAC) & 99th CA (2014)",
        47: "Fourth Judges Case (2015): NJAC Struck Down 4:1 by Supreme Court",
        48: "Separation of Powers (Montesquieu) vs Judicial Supremacy in India",
        49: "Judicial Standards & Accountability Bill & Pendency of Cases Crisis",
        50: "Judicial Reforms Roadmap: Memorandum of Procedure (MoP) & All India Judicial Service",
        51: "Union Parliament: World Bank Six Parameters of Legislative Performance",
        52: "Decline of Parliament Thesis: Subhash Kashyap on Reduced Sittings & Disruptions",
        53: "Ordinance Raj: Article 123 & D.C. Wadhwa Case (Fraud on the Constitution)",
        54: "Anti-Defection Law (10th Schedule) Reducing MPs to Voting Automations",
        55: "Departmentally Related Standing Committees (DRSCs): Genesis & Working",
        56: "Decline in Bill Referral to Committees: Governance Consequences",
        57: "Bicameralism: Lok Sabha vs Rajya Sabha Dynamics",
        58: "Rajya Sabha: House of Federal Continuity & Second Look (Peter Sober Analogy)",
        59: "Financial Accountability: Public Accounts Committee (PAC) & CAG Reports",
        60: "Parliamentary Privileges: Codification Dilemma vs Freedom of Speech",
        61: "Union Executive: Constitutional Position of President (Articles 52, 53, 74)",
        62: "42nd vs 44th Constitutional Amendments: President Bound by CoM Advice",
        63: "Presidential Discretion: Hung Parliament, Dissolution & Dismissal",
        64: "Walter Bagehot's Triad: Right to be Consulted, Encourage, and Warn",
        65: "Activist Presidents: K.R. Narayanan ('Working President') & APJ Abdul Kalam",
        66: "Prime Minister: Primus Inter Pares vs Prime Ministerial Hegemony",
        67: "Article 78: PM's Constitutional Obligation to Communicate with President",
        68: "Coalition PMs vs Single-Party Dominant PMs: Institutional Contrast",
        69: "Prime Minister's Office (PMO): Evolution under Nehru, Shastri & Indira",
        70: "PMO vs Cabinet Secretariat: Centralisation of Executive Power",
        71: "Social Movements in India: Historical Context & Shift to New Social Movements",
        72: "Environmental Movements: Ramachandra Guha & Madhav Gadgil ('Ecology and Equity')",
        73: "Empty Stomach Environmentalism (India) vs Full Stomach (West / Inglehart)",
        74: "Three Environmental Strands: Crusading Gandhian, Ecological Marxist, Appropriate Tech",
        75: "Chipko Movement: Forests as Soil, Water and Clean Air (Bahuguna & Bhatt)",
        76: "Silent Valley Movement: Saving Rainforests from Hydroelectric Inundation",
        77: "Narmada Bachao Andolan (NBA): Medha Patkar on Mega Dams & Human Displacement",
        78: "Tribal Resistance to Resource Extraction: Niyamgiri / Vedanta & POSCO",
        79: "National Green Tribunal (NGT) & Forest Rights Act 2006 (FRA) Framework",
        80: "Development vs Ecological Sustainability Dilemma in the Neoliberal Era",
        81: "Women's Movement in India: Pre-Independence Social Reform (Roy, Phule, Gandhi)",
        82: "Post-Independence Autonomous Women's Groups: Towards Equality Report (1974)",
        83: "Mathura Rape Case (1979) & Campaign Against Dowry and Custodial Violence",
        84: "Shift from Welfare Approach to Empowerment & Rights (73rd CA 33% Quota)",
        85: "Women's Reservation Bill Debate: Sub-Quotas and Patriarchal Resistance",
        86: "Dalit Movement: Dr. Ambedkar's Radical Mobilisation vs Gandhian Reform",
        87: "Rise of Dalit Panthers (1972): Namdeo Dhasal & Militant Cultural Resistance",
        88: "Gail Omvedt: 'Dalits and the Democratic Revolution' & Political Autonomy",
        89: "Peasant Struggles: Old Peasant Movements (Tebhaga, Telangana, Naxalbari)",
        90: "New Farmers' Movements (NFMs): Non-Party Character & Market Demands",
        91: "Planning Models in India: Nehru-Mahalanobis Industrialisation Strategy",
        92: "Public Sector Commanding Heights & Import Substitution Industrialisation (ISI)",
        93: "Crisis of 1991: Balance of Payments (BoP) Shock & Washington Consensus",
        94: "LPG Reforms: Liberalisation, Privatisation and Globalisation Transition",
        95: "25 Years of Economic Reforms: High Growth vs Jobless Growth Reality",
        96: "Widening Regional & Social Inequalities: Bhagwati vs Amartya Sen Debate",
        97: "Poverty Estimation Debates: Lakdawala, Tendulkar & Rangarajan Committees",
        98: "Human Development Deficits: Malnutrition, Education & Health Spendings",
        99: "NITI Aayog (1 Jan 2015): Cooperative & Competitive Federalism Roadmap",
        100: "SDG India Index & Aspirational Districts Programme Evaluation",
        101: "Land Reforms in Independent India: Objectives of Equity & Productivity",
        102: "Four Pillars: Zamindari Abolition, Tenancy Reforms, Land Ceilings, Consolidation",
        103: "Success in Kerala & West Bengal (Operation Barga) vs Nationwide Failure",
        104: "Causes of Failure: Lack of Political Will, Benami Holdings & Judicial Obstacles",
        105: "Green Revolution: Shift from Structural Reforms to Technological Solutions",
        106: "Achievements: Food Self-Sufficiency & End of PL-480 Ship-to-Mouth Existence",
        107: "Adverse Fallout: Regional Imbalances (North-West vs Rest of India)",
        108: "Ecological Degradation: Groundwater Depletion & Chemical Contamination",
        109: "Rise of 'Bullock Capitalists' (Rudolph & Rudolph) & Agrarian Power",
        110: "Ongoing Agrarian Crisis: Farmer Suicides & Need for Second Green Revolution",
        111: "Concept of Constitutionalism: Government of Laws, Not of Men",
        112: "Core Pillars: Limited Government, Separation of Powers & Fundamental Rights",
        113: "Judicial Supremacy vs Parliamentary Sovereignty Clash (Articles 13 vs 368)",
        114: "From Shankari Prasad (1951) to Sajjan Singh (1965) to Golaknath (1967)",
        115: "Golaknath Ruling: Parliament Cannot Abridge Fundamental Rights",
        116: "24th and 25th Constitutional Amendments (1971): Parliament Asserts Power",
        117: "Kesavananda Bharati Case (1973): 13-Judge Bench & Basic Structure Doctrine",
        118: "Essential Identity Test: Power to Amend is Not Power to Destroy",
        119: "Indira Nehru Gandhi (1975) & Minerva Mills (1980): Golden Harmony of FR/DPSP",
        120: "I.R. Coelho (2007): Ninth Schedule Laws Subject to Basic Structure Review",
        121: "Philosophy of Affirmative Action: Compensatory Justice & Level Playing Field",
        122: "Substantive Equality (Ronald Dworkin): Equal Treatment vs Treatment as Equals",
        123: "Constitutional Mandate: Articles 15(4), 16(4), 46 for Socially Backward Classes",
        124: "Time Frame of Affirmative Action: Enabling Policy vs Permanent Vested Interest",
        125: "Competitive Backwardness: 'Race to the Bottom' (Patidars, Jats, Marathas)",
        126: "Dalit Christians and Muslims Debate: Denial of SC Status upon Conversion",
        127: "K.P.S. Manu Case: Re-conversion and Social Acceptance Conditions",
        128: "Sub-Categorisation of Backward Classes: Justice Rohini Commission",
        129: "Yogendra Yadav's Proposal: Evidence-based Multi-layered Deprivation Index",
        130: "Synthesising Caste, Gender, Schooling & Geography in Affirmative Action",
        131: "Pressure Groups in India: Evolution from Communal to Socio-Economic Formations",
        132: "New Farmers' Movements (NFM) as Powerful Interest Groups",
        133: "Bharatiya Kisan Union (BKU): Western UP & Haryana (Mahendra Singh Tikait)",
        134: "Shetkari Sangathan: Maharashtra (Sharad Joshi) & Free-Market Philosophy",
        135: "Sharad Joshi's 'Bharat vs India': Rural Exploitation by Industrial Metropolises",
        136: "Methods of Agitation: Boat Club Rallies, Gherao, Rasta Roko, Withholding Crops",
        137: "Internal Contradictions: Neglect of Landless Agricultural Labourers & Dalits",
        138: "Impact of 1991 LPG on Farmers' Movements: Fragmentation & Subsidy Defense",
        139: "Contemporary Farm Protests (2020-21): Revival of Non-Party Farmer Coalitions",
        140: "Corporate Lobbying & FICCI/CII Influence on Economic Policy",
        141: "The Concept of Sovereignty: Classical Etymology (*Superanus*) & Definitions",
        142: "Internal vs External Sovereignty: Juristic & Realist Frameworks",
        143: "John Austin's Monistic Theory of Sovereignty: Absolute, Indivisible, Inalienable",
        144: "Austin's Command Theory of Law: Sovereign Commands Backed by Sanctions",
        145: "Pluralist Critique of Monism: Harold Laski, Figgis, MacIver & Barker",
        146: "Laski's Thesis: 'Society is Federal, Authority Must Be Federal'",
        147: "Role of RSS as Socio-Cultural and Political Pressure Group in India",
        148: "Christophe Jaffrelot: RSS Shakha Organisational Structure & Sangh Parivar",
        149: "Transmission Belts: VHP, ABVP, Bharatiya Mazdoor Sangh & Relation to BJP",
        150: "Grand Synthesis of Paper 1 Part 2: Grassroots Democracy to Modern Statehood"
    }
    
    scans_catalog = []
    for p in range(1, 151):
        scans_catalog.append({
            "page": p,
            "scanFile": f"page_{p:03d}.png",
            "notebookPage": f"Notebook Page {114 + (p // 2)}",
            "title": page_catalog_titles.get(p, f"IGP Part 2 Page {p}")
        })
        
    full_data = {
        "meta": meta,
        "sections": sections,
        "flashcards": flashcards,
        "answers": answers,
        "scansCatalog": scans_catalog
    }
    
    out_content = f"export const paper1Part2Data = {json.dumps(full_data, indent=2)};\n"
    open(target_file, 'w', encoding='utf-8').write(out_content)
    
    print("\n==========================================")
    print(f"SUCCESS: Generated {target_file}")
    print(f"Total Sections: {len(sections)}")
    print(f"Total Flashcards: {len(flashcards)}")
    print(f"Total Model Answers: {len(answers)}")
    print(f"Total Scans in Catalog: {len(scans_catalog)}")
    print(f"File Size: {os.path.getsize(target_file):,} bytes")
    print("==========================================\n")

if __name__ == "__main__":
    build_paper1_part2()
