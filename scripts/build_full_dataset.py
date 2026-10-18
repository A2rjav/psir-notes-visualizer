import os
import json
import re

from batch_meta import get_batch_metadata
from batch_parser import parse_markdown_to_concepts, parse_flashcards, parse_model_answers

def generate_full_paper1_data():
    base_file = "app/src/data/paper1IptData.js"
    content = open(base_file, encoding='utf-8').read()
    
    match = re.search(r'export const paper1IptData = (\{.*?\});\s*$', content, re.DOTALL)
    if not match:
        print("Error: Could not extract base JSON from paper1IptData.js")
        return
        
    data = json.loads(match.group(1))
    
    # Update meta
    data["meta"]["notebookPages"] = "Pages 1 to 104 (214 Scan Pages: 001 to 214)"
    data["meta"]["scanEnd"] = 214
    data["meta"]["topicTitle"] = "Paper 1 (Part 1): Indian Political Thought & Indian Government and Politics (Complete 214 Pages)"
    data["meta"]["summary"] = "Exhaustive, 100% zero-loss digital knowledge repository of Shubhra Ranjan IAS lecture notes covering ancient to modern Indian Political Thought (Manu, Kautilya, Buddhism, Sir Syed, Aurobindo, Gandhi, Ambedkar, M.N. Roy) and Indian Government & Politics (Perspectives on National Movement, Constituent Assembly Debates, Preamble & Globalisation, Secularism & Communalism, Uniform Civil Code, Caste Politics & The Silent Revolution, Affirmative Action, Ethnicity, Party System & Coalition Politics, Rise of BJP & Left Decline, Anti-Defection 10th Schedule, Electoral Behaviour, Changing Profile of MPs, Federalism Theories, Politics of State Formation, Centre-State Relations, Governor's Office, Article 356, Bommai Landmark, Water Disputes Tribunals, Fiscal Federalism, 101st Amendment GST, and NITI Aayog)."
    
    # Keep the first 13 sections
    existing_sections = data["sections"][:13]
    print(f"Preserved {len(existing_sections)} initial sections.")
    
    # Ingest new batches 13 to 27
    new_batches = get_batch_metadata()
    flashcards = data.get("flashcards", [])
    answers = data.get("answers", [])
    fc_id_counter = len(flashcards) + 1
    ans_id_counter = len(answers) + 1
    
    for b in new_batches:
        md_path = os.path.join("transcriptions_paper1", b["batch_file"])
        if not os.path.exists(md_path):
            print(f"Warning: File not found {md_path}")
            continue
            
        md_text = open(md_path, encoding='utf-8').read()
        concepts = parse_markdown_to_concepts(md_text, b["scanPages"][0])
        
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
        existing_sections.append(section_obj)
        
        # Add flashcards
        new_fc = parse_flashcards(md_text, b["title"], fc_id_counter)
        flashcards.extend(new_fc)
        fc_id_counter += len(new_fc)
        
        # Add model answers
        new_ans = parse_model_answers(md_text, b["title"], ans_id_counter)
        answers.extend(new_ans)
        ans_id_counter += len(new_ans)
        
        print(f"Processed Section {b['number']}: {b['title']} ({len(concepts)} concepts, {len(new_fc)} cards, {len(new_ans)} answers)")
        
    data["sections"] = existing_sections
    data["flashcards"] = flashcards
    data["answers"] = answers
    
    # Generate complete scansCatalog for all 214 pages
    scans_catalog = []
    
    # Page to section/title mapping
    page_titles = {
        1: ("Syllabus Overview & Paper 1 Structure", 1),
        2: ("IPT Methodological Debate: Western Denial vs Existence", 1),
        3: ("Distinctive Features of Ancient IPT: Purusharthas & Rta", 1),
        4: ("Ancient Texts Overview: Dharmashastra vs Arthashastra", 2),
        5: ("Origins of State: Matsya Nyaya (State of Nature)", 2),
        6: ("Saptanga Sthiti & Kingship in Classical Statecraft", 2),
        7: ("Debate on Indian Political Thought & Distinctive Features", 2),
        8: ("Western Denial vs Indian Political Realities (Prof. V.R. Mehta)", 2),
        9: ("Dichotomy vs Continuity in Indian Philosophical Tradition", 3),
        10: ("Four Purusharthas & Cosmic Order (Rta & Dharma)", 3),
        11: ("Manu & Manusmriti: Origin of State & Quasi-Contract", 4),
        12: ("Varna Dharma & Asymmetric Penology in Dharmashastra", 4),
        13: ("Danda: The Instrument of Social Order & Coercion", 5),
        14: ("Kautilya: Arthashastra, Pragmatism & Statecraft", 6),
        15: ("Kautilya: Organic Theory & Saptanga Framework", 6),
        16: ("Saptanga: Swami, Amatya, Janapada & Durga", 7),
        17: ("Saptanga: Kosha, Danda & Mitra (Seven Prakritis)", 7),
        18: ("Yogakshema: Welfare Concept & Citizen Well-Being", 8),
        19: ("State Administration & Espionage Networks in Arthashastra", 8),
        20: ("Mandala Theory: Ring Geometry of 12 Kings", 8),
        21: ("The 4 Upayas: Sama, Dana, Bheda & Danda", 9),
        22: ("Shadgunya Niti: 6-Fold Foreign Policy Principles", 9),
        23: ("Kautilya on Corruption: 40 Modes of Embezzlement", 10),
        24: ("Kautilya vs Niccolò Machiavelli: Realpolitik Comparison", 10),
        25: ("Buddhist Political Thought: Rejection of Varna & Heterodoxy", 11),
        26: ("Agganna Sutta: Social Contract & Mahasammata King", 11),
        27: ("Dhamma vs Danda & The Republican Sangha Democracy", 12),
        28: ("Sir Syed Ahmed Khan: Aligarh Movement & Muslim Modernisation", 13),
        29: ("Sir Syed: Scientific Rationalism & Western Education", 13),
        30: ("Sir Syed: Views on Indian National Congress & Pluralism", 14),
        31: ("Sri Aurobindo Ghosh: Spiritual Nationalism & Sanatan Dharma", 14),
        32: ("Aurobindo: Cultural Renaissance & Critique of Moderates", 15),
        33: ("Aurobindo: Doctrine of Passive Resistance", 15),
        34: ("Aurobindo: Boycott, National Education & Swadeshi", 16),
        35: ("Aurobindo: Synthesis of Eastern & Western Thought", 16),
        36: ("Aurobindo: Integral Yoga & Evolution of Human Consciousness", 17),
        37: ("Aurobindo: The Ideal of Human Unity & World State", 18),
        38: ("Aurobindo: Nation as Mother / Bhavani Bharati", 19),
        39: ("Mahatma Gandhi: Moral Foundations of Politics", 20),
        40: ("Gandhi: Ahimsa (Non-Violence) as Truth in Action", 20),
        41: ("Gandhi: Satyagraha: Soul Force vs Brute Physical Force", 21),
        42: ("Gandhi: Swaraj: From National Independence to Self-Control", 21),
        43: ("Gandhi: Sarvodaya (Welfare of All) & Ruskin's Unto This Last", 22),
        44: ("Gandhi: Hind Swaraj (1909) & Critique of Modern Civilization", 22),
        45: ("Gandhi: Critique of Modern Institutions (Railways, Doctors, Lawyers)", 23),
        46: ("Gandhi: Theory of State: Enlightened Anarchy", 23),
        47: ("Gandhi: Trusteeship Doctrine: Equitable Wealth Custodianship", 24),
        48: ("Gandhi: Inseparable Connection of Ends and Means", 24),
        49: ("Gandhi: Rights vs Duties: Priority of Moral Duty", 25),
        50: ("M.N. Roy: Revolutionary Phase & Transition to Marxism", 25),
        51: ("M.N. Roy: 2nd Comintern & Lenin-Roy Debate on Colonies", 26),
        52: ("M.N. Roy: Critique of Gandhian Politics as Bourgeois Feudalism", 26),
        53: ("M.N. Roy: Philosophical Critique of Orthodox Marxism", 27),
        54: ("M.N. Roy: Radical Humanism (New Humanism) & 22 Theses", 27),
        55: ("M.N. Roy: Reason, Freedom & Morality as Triad of Liberation", 28),
        56: ("M.N. Roy: Partyless Democracy, People's Committees & People's Plan", 28),
        57: ("Dr. B.R. Ambedkar: Subaltern Life, Phule's Influence & Biography", 29),
        58: ("Ambedkar: Arun Shourie Critique vs Christophe Jaffrelot Defense", 29),
        59: ("Ambedkar on Nation & Nationalism: Why India is Not Yet a Nation", 30),
        60: ("Ambedkar: Caste as Division of Labourers (Not Division of Labour)", 30),
        61: ("Ambedkar: Origins of Untouchability & Broken Men Theory", 31),
        62: ("Ambedkar: Endogamy (Inter-Marriage Prohibition) as Core of Caste", 31),
        63: ("Ambedkar: Annihilation of Caste (1936) & Critique of Shastras", 32),
        64: ("Ambedkar: Constitutional Morality & State Socialism (States & Minorities)", 32),
        65: ("Gandhi-Ambedkar Debate: Varna vs Caste Conceptual Divide", 33),
        66: ("Gandhi-Ambedkar Debate: Harijan vs Dalit Self-Assertion", 33),
        67: ("Gandhi-Ambedkar Debate: Village Republics vs Den of Local Ignorance", 34),
        68: ("Ambedkar: The Poona Pact (1932) & Struggle for Representation", 34),
        69: ("Ambedkar: Conversion to Buddhism (1956) & Navayana Philosophy", 34),
        70: ("Ambedkar vs Karl Marx: Social Justice vs Economic Determinism", 34),
        71: ("Early National Movement: Moderates' 3Ps (Prayer, Petition, Protest)", 34),
        72: ("Extremist Critique: Tilak 'Political Suicide' & Aurobindo 'Bankruptcy'", 34),
        73: ("Bipin Chandra: Assessment of Moderates & Historical Service", 35),
        74: ("Rise of Extremists: Tilak's Praja Droh & Swadeshi Mobilisation", 35),
        75: ("Gandhian Mass Movement Strategy: Gramscian War of Position", 36),
        76: ("Gandhian Strategy: S-T-S vs S-V & Mass Psychological Endurance", 36),
        77: ("Non-Cooperation Movement (1920-22): Causes & Nagpur Mandate", 37),
        78: ("Non-Cooperation Movement: Chauri Chaura Withdrawal & Defense", 37),
        79: ("Non-Cooperation Movement: Multi-Class Base & Overcoming Fear", 38),
        80: ("Civil Disobedience Movement (1930-31): Salt March & 11 Demands", 38),
        81: ("Civil Disobedience Strategy: Moral Dilemma for Colonial State", 39),
        82: ("Gandhi-Irwin Pact (1931): Equal Footing with the British Empire", 39),
        83: ("Quit India Movement (1942): August Revolution & Militant Energy", 40),
        84: ("Quit India Movement: Why Called the Most Un-Gandhian Movement", 40),
        85: ("Quit India Movement: 'Do or Die' & Spontaneous Underground Action", 41),
        86: ("Evaluation of Gandhian Movements: Bipin Chandra's Master Defense", 41),
        87: ("Perspectives on Indian Nationalism: Colonial & Cambridge School", 42),
        88: ("Perspectives on Indian Nationalism: Nationalist Historiography", 42),
        89: ("Marxist Perspective: R. Palme Dutt ('India Today') & Class Theory", 43),
        90: ("Marxist Perspective: A.R. Desai ('Social Background of Nationalism')", 43),
        91: ("Subaltern Perspective: Ranajit Guha ('Subaltern Studies')", 44),
        92: ("Subaltern Perspective: Dominance Without Hegemony & Peasant Agency", 44),
        93: ("Partha Chatterjee: 'The Nation and Its Fragments' & Cultural Realm", 45),
        94: ("Feminist Historiography: Gendered Erasure in Nationalist Movement", 45),
        95: ("Constituent Assembly: Cabinet Mission Plan & Composition Debates", 46),
        96: ("Constituent Assembly: Winston Churchill's Critique & Austin's Defense", 46),
        97: ("Major Constituent Assembly Debates: System of Government Choice", 47),
        98: ("Constituent Assembly: Presidential vs Parliamentary Governance", 47),
        99: ("Constituent Assembly: Fundamental Rights vs DPSPs Relationship", 48),
        100: ("Constituent Assembly: Right to Property (Article 31 Controversy)", 48),
        101: ("Constituent Assembly: Appointment of Judges & Judicial Independence", 49),
        102: ("Constituent Assembly: Uniform Civil Code (Article 44 Clashes)", 49),
        103: ("The Preamble to Constitution: Philosophy, Identity & Key Terms", 50),
        104: ("Globalisation and State Sovereignty: David Held's Analysis", 50),
        105: ("Preamble Values: Justice, Liberty, Equality and Fraternity", 51),
        106: ("Is Preamble Part of Constitution: Berubari (1960) vs Kesavananda (1973)", 51),
        107: ("Indian Secularism: Donald Eugene Smith's Three-Pillar Model", 52),
        108: ("Marc Galanter: Rejection of American Strict Wall Separation in India", 52),
        109: ("Rajeev Bhargava: Doctrine of Principled Distance", 53),
        110: ("Sarva Dharma Sambhava vs Dharma Nirapekshata Comparison", 53),
        111: ("Secularism Flashpoints: Essential Religious Practices Doctrine", 54),
        112: ("Minority Rights vs Pseudo-Secularism Debate (L.K. Advani)", 54),
        113: ("Anti-Secularist Critique: Ashis Nandy's 'Anti-Secularist Manifesto'", 55),
        114: ("T.N. Madan: Secularism as Act of Modern Arrogance in South Asia", 55),
        115: ("Communalism Defined: Religious Consciousness vs Communalism", 56),
        116: ("Bipan Chandra's Three Stages of Communalism in Modern India", 56),
        117: ("Colonial Roots: Divide and Rule & Separate Electorates Evolution", 57),
        118: ("Ideological Communalism: V.D. Savarkar's Hindutva (1923)", 57),
        119: ("Ideological Communalism: Sir Muhammad Iqbal & Muslim Nationalism", 58),
        120: ("Post-Independence Communalism: Phases from Nehru to 1960s", 58),
        121: ("Phases of Communalism: 1980s Sikh Militancy, Shah Bano & Ayodhya", 59),
        122: ("Paul Brass: Institutionalised Riot System (IRS) & Riot Producers", 59),
        123: ("Dipankar Gupta: 'Picnic Riots' & Political Mobilisation", 60),
        124: ("Sachar Committee Report (2006): Socio-Economic Status of Muslims", 60),
        125: ("Uniform Civil Code: Article 44 Constitutional Philosophy", 61),
        126: ("Landmark UCC Jurisprudence: Shah Bano Case (1985) & Backlash", 61),
        127: ("Judicial Push for UCC: Sarla Mudgal (1995) & Shayara Bano (2017)", 62),
        128: ("UCC Reform Debates: Law Commission Recommendations & Gender Justice", 62),
        129: ("Caste in Indian Politics: Classical Modernisation Theory vs Reality", 63),
        130: ("Rajni Kothari: Politicisation of Caste Leads to Secularisation", 63),
        131: ("Three Forms of Caste in Politics: Entrenched, Ascendant & Integrated", 64),
        132: ("M.N. Srinivas: The Concept of Dominant Caste & Agrarian Power", 64),
        133: ("Christophe Jaffrelot: The 'Silent Revolution' in North India", 65),
        134: ("North vs South Anti-Caste Movements: Periyar/Phule vs Mandal Era", 65),
        135: ("Yogendra Yadav: Second Democratic Upsurge & Plebeianisation", 66),
        136: ("Caste Coalitions in State Politics: KHAM, AJGAR & Bullock Capitalists", 66),
        137: ("Affirmative Action in India: Articles 15(4) & 16(4) Constitutional Scheme", 67),
        138: ("Kaka Kalelkar & Mandal Commission (1979-80) 27% OBC Quota", 67),
        139: ("Indra Sawhney Case (1992): 50% Ceiling & Creamy Layer Exclusion", 68),
        140: ("Sub-Categorisation of OBCs: Justice Rohini Commission & Caste Census", 68),
        141: ("Dalit Politics: Kanshi Ram & Bahujan Samaj Party (BSP) Phenomenon", 69),
        142: ("Dalit Assertion: 'Political Power is the Master Key' Philosophy", 69),
        143: ("Ethnicity in Indian Politics: Donald Horowitz & Comparative Theories", 70),
        144: ("James Manor: Cross-Cutting Cleavages & Stability of Indian Republic", 70),
        145: ("Ethnicity & Conflict Management: S.D. Muni & Charles Taylor", 71),
        146: ("Atul Kohli: Democratic Accommodation of Sub-National Movements", 71),
        147: ("Theories of Party System: Maurice Duverger's Stasiology", 72),
        148: ("Giovanni Sartori: Relevant Parties & Polarization Index", 72),
        149: ("Pathologies of Indian Parties: Zoya Hasan & Paul Brass Paradoxes", 73),
        150: ("W.H. Morris-Jones: One-Party Dominance with Democratic Consent", 73),
        151: ("Rajni Kothari's Seminal Model: The 'Congress System' Explained", 74),
        152: ("Breakdown of Congress System: 1967 General Elections & De-institutionalisation", 74),
        153: ("Internal & External Challenges to Congress Dominance Post-1967", 75),
        154: ("Sociological Decomposition of Congress Support Base (1989-2014)", 75),
        155: ("Fragmentation vs Regionalisation of Indian Party System", 76),
        156: ("E. Sridharan's 7 Factors for the Rise of Regional Parties", 76),
        157: ("William H. Riker: Definition of Coalition & Power-Sharing", 77),
        158: ("Chronology of Coalition Governments in India (1989-2014)", 77),
        159: ("Coalition by Design vs Coalitions by Political Calculation", 78),
        160: ("Managing Coalitions: Constructive No-Confidence Vote & CMP", 78),
        161: ("Rise of the BJP: Bharatiya Jana Sangh to Pan-Indian Dominance", 79),
        162: ("Deendayal Upadhyay: Integral Humanism & Cultural Nationalism", 79),
        163: ("Decline of the Left in India: Praful Bidwai's 'Phoenix Moment'", 80),
        164: ("Third Front Politics: Instability, Parochialism & Structural Limits", 80),
        165: ("Rise of Aam Aadmi Party (AAP): Globalisation, IAC & Swaraj", 81),
        166: ("Anti-Defection Law (10th Schedule, 52nd & 91st Amendments)", 81),
        167: ("Kihoto Hollohan (1992): Judicial Review of Speaker's Discretion", 82),
        168: ("Election Commission of India (Article 324) & T.N. Seshan Era Reforms", 82),
        169: ("Pressure Groups in India: Myron Weiner's 'Politics of Scarcity'", 83),
        170: ("Rudolph & Rudolph: Demand Groups vs Institutional Groups", 83),
        171: ("Corporate Pressure Groups in Post-1990s: CII, FICCI, ASSOCHAM", 84),
        172: ("Socio-Economic Profile of Indian Legislators: Historical Evolution", 85),
        173: ("B.L. Shankar & Valerian Rodrigues: The Three Phases of Parliament", 85),
        174: ("16th Lok Sabha Profile: High Education, Ageing & Criminalisation", 85),
        175: ("Electoral Behaviour: Mukulika Banerjee's 'Why India Votes'", 86),
        176: ("Strategic Voting of the Poor & Democratic Power Inversion Ritual", 86),
        177: ("Yogendra Yadav: Identity Plus Politics & Turnout Convergence", 87),
        178: ("Transition Leaf: From Electoral Dynamics to Federal Governance", 87),
        179: ("Master Blueprint of Federalism: 11 Core PSIR Syllabus Questions", 87),
        180: ("Federalism Concept: Etymology (*Foedus*) & Dual Polity Essentials", 88),
        181: ("Genesis of Indian Federalism: Dual vs Cooperative Federalism", 88),
        182: ("K.C. Wheare's 'Quasi-Federal' Thesis & 11 Unitary Features", 88),
        183: ("Granville Austin: Defense of Cooperative Federalism in India", 89),
        184: ("Impact of Party System on Federal Dynamics (1950 to Present)", 89),
        185: ("Economic Reforms & Globalisation: States as Independent Economic Actors", 90),
        186: ("Article 3: Indestructible Union of Destructible States Analysis", 90),
        187: ("Politics of State Formation: 1956 SRC & Nehru's Initial Resistance", 91),
        188: ("Louise Tillin: Three Waves of State Formation in Independent India", 91),
        189: ("The Debate on Smaller States: Arguments FOR Better Governance", 92),
        190: ("Arguments AGAINST Smaller States: Prof. M.P. Singh & Sudha Pai", 92),
        191: ("Centre-State Legislative Relations: Seventh Schedule Distribution", 93),
        192: ("Residuary Powers under Article 248 & Centre Legislative Dominance", 93),
        193: ("Exceptional Peacetime Legislative Powers: Articles 249, 252 & 253", 94),
        194: ("Centre-State Administrative Relations: Articles 256, 257 & 365", 94),
        195: ("All India Services (Article 312) & Inter-State Coordination Issues", 95),
        196: ("Deployment of Central Armed Police Forces in States Controversy", 95),
        197: ("Inter-State Boundary Disputes: Belgaum, Chandigarh & Fazilka", 96),
        198: ("Inter-State River Water Disputes: Article 262 & ISRWD Act 1956", 96),
        199: ("Water Tribunals: Delays, Non-Compliance & Judicial Overreach", 97),
        200: ("Case Studies: Cauvery Water Dispute & Sutlej-Yamuna Link (SYL)", 97),
        201: ("Institution of Governor: Dual Role ('Wearing Two Hats on One Head')", 98),
        202: ("Paul Brass: Governor as the Product of Partition Insecurity", 98),
        203: ("Controversy of Governor's Discretionary Powers under Article 163", 99),
        204: ("Historical Misuse of Governor's Office: Madras 1952 to Arunachal 2016", 99),
        205: ("Manner of Appointment (Art 155) & Removal (Art 156 Doctrine of Pleasure)", 100),
        206: ("B.P. Singhal Case (2010): Limits on the Arbitrary Removal of Governors", 100),
        207: ("Landmark Rulings on Governor: Shamsher Singh & Hargovind Pant", 101),
        208: ("Nabam Rebia (2016): SC Censures Governor's Discretionary Overreach", 101),
        209: ("Centre-State Financial Relations: Philosophy & Core Imbalances", 102),
        210: ("State Grievances: Borrowing Caps (Art 293) & Surcharges (Art 271)", 102),
        211: ("Transition from Planning Commission to NITI Aayog ('Team India')", 103),
        212: ("Goods and Services Tax (GST) & 101st Constitutional Amendment Act", 103),
        213: ("GST Council (Article 279A): Composition & 3/4th Weighted Voting Formula", 104),
        214: ("Seventh Schedule Amendments by 101st CA & Grand Summary of Paper 1 Part 1", 104)
    }
    
    for page_num in range(1, 215):
        scan_file = f"page_{page_num:03d}.png"
        title, nb_page = page_titles.get(page_num, (f"Handwritten Notes Page {page_num}", (page_num // 2) + 1))
        scans_catalog.append({
            "page": page_num,
            "scanFile": scan_file,
            "notebookPage": nb_page,
            "title": title
        })
        
    data["scansCatalog"] = scans_catalog
    
    # Write back to paper1IptData.js
    out_content = f"export const paper1IptData = {json.dumps(data, indent=2)};\n"
    open(base_file, 'w', encoding='utf-8').write(out_content)
    
    print("\nSUCCESS: Compiled complete paper1IptData.js!")
    print(f"Total Sections: {len(data['sections'])}")
    print(f"Total Flashcards: {len(data['flashcards'])}")
    print(f"Total Model Answers: {len(data['answers'])}")
    print(f"Total Scans in Catalog: {len(data['scansCatalog'])}")
    print(f"New File Size: {os.path.getsize(base_file):,} bytes")

if __name__ == "__main__":
    generate_full_paper1_data()
