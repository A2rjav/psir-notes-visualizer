import os
import json
import re

TRANSCRIPTIONS_DIR = "transcriptions_paper1"

def extract_between(text, start_pattern, end_pattern):
    m = re.search(f"{start_pattern}(.*?){end_pattern}", text, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""

def get_batch_metadata():
    # Defined mapping of batch to section data
    batches = [
        # Batches 1 to 12 are already in the existing data or can be preserved/enhanced
        # Batches 13 to 27:
        {
            "batch_file": "batch_13_quit_india_nationalism_perspectives.md",
            "id": "modern-igp-quit-india",
            "number": "14",
            "title": "Quit India Movement & Perspectives on Indian Nationalism",
            "subtitle": "August Kranti 1942 | Do or Die | S-T-S vs S-V Debate | Colonial, Nationalist & Marxist Schools",
            "scanPages": [81, 82, 83, 84, 85, 86, 87, 88],
            "notebookPages": "Pages 39 to 42",
            "lecture": "Lecture 57 (25/02/2017)",
            "keyScholars": ["Bipin Chandra", "Prof. Sumit Sarkar", "Dr. Tara Chand", "R.C. Majumdar", "Benedict Anderson"],
            "coreTheories": ["Struggle-Truce-Struggle (S-T-S) Paradigm", "Gramscian War of Position", "Colonial/Cambridge School Interests", "Nationalist Cultural Paradigm", "Marxist Mode of Production Historiography"]
        },
        {
            "batch_file": "batch_14_historiography_nationalism.md",
            "id": "modern-igp-historiography-constituent-assembly",
            "number": "15",
            "title": "Historiography of Nationalism & Constituent Assembly Foundations",
            "subtitle": "Marxist & Subaltern Schools | Ranajit Guha | Partha Chatterjee | Granville Austin's Defense",
            "scanPages": [89, 90, 91, 92, 93, 94, 95, 96],
            "notebookPages": "Pages 43 to 46",
            "lecture": "Lecture 57 & 58 (25/02/2017 & 27/02/2017)",
            "keyScholars": ["R. Palme Dutt", "A.R. Desai", "Ranajit Guha", "Partha Chatterjee", "Granville Austin", "Winston Churchill"],
            "coreTheories": ["Subaltern Autonomous Domain of Politics", "Dominance without Hegemony", "Elite Collaborationist Theory", "Cornerstone of a Nation Thesis", "Representative Character of Constituent Assembly"]
        },
        {
            "batch_file": "batch_15_constituent_assembly_preamble.md",
            "id": "modern-igp-constituent-debates-preamble",
            "number": "16",
            "title": "Constituent Assembly Debates, Preamble & Globalisation",
            "subtitle": "Presidential vs Parliamentary | FR vs DPSP | Judicial Appointments | UCC Debates | David Held",
            "scanPages": [97, 98, 99, 100, 101, 102, 103, 104],
            "notebookPages": "Pages 47 to 50",
            "lecture": "Lecture 58 & 59 (27/02/2017 & 28/02/2017)",
            "keyScholars": ["Dr. B.R. Ambedkar", "Pt. Jawaharlal Nehru", "K.M. Munshi", "N.A. Palkhivala", "David Held"],
            "coreTheories": ["Accountability vs Stability in System of Govt", "Constitutional Morality", "Harmonious Construction of FR and DPSP", "Preamble as Identity Card", "Globalisation & Dilution of State Sovereignty"]
        },
        {
            "batch_file": "batch_16_secularism_debates.md",
            "id": "modern-igp-secularism-debates",
            "number": "17",
            "title": "Secularism in India & Nature of the State",
            "subtitle": "Principled Distance | D.E. Smith 1962 | Marc Galanter | Sarva Dharma Sambhava vs Dharma Nirapekshata",
            "scanPages": [105, 106, 107, 108, 109, 110, 111, 112],
            "notebookPages": "Pages 51 to 54",
            "lecture": "Lecture 59 & 60 (28/02/2017 & 01/03/2017)",
            "keyScholars": ["Donald Eugene Smith", "Marc Galanter", "Prof. Rajeev Bhargava", "Amartya Sen", "Neera Chandhoke"],
            "coreTheories": ["Principled Distance Theory", "Three-Pillar Secular State Model", "Equal Respect vs Strict Wall of Separation", "Essential Religious Practices Doctrine", "Minority Protection vs Pseudo-Secularism Critique"]
        },
        {
            "batch_file": "batch_17_secularism_communalism.md",
            "id": "modern-igp-anti-secularism-communalism",
            "number": "18",
            "title": "Anti-Secularist Critique & Roots of Communalism",
            "subtitle": "Ashis Nandy | T.N. Madan | Bipan Chandra's Three Stages | Savarkar, Iqbal & Colonial Divide-and-Rule",
            "scanPages": [113, 114, 115, 116, 117, 118, 119, 120],
            "notebookPages": "Pages 55 to 58",
            "lecture": "Lecture 60 (01/03/2017)",
            "keyScholars": ["Ashis Nandy", "T.N. Madan", "Prof. Bipan Chandra", "V.D. Savarkar", "Sir Muhammad Iqbal"],
            "coreTheories": ["Anti-Secularist Manifesto", "South Asian Religious Tolerance Paradigm", "Three Stages of Communalism", "Hindutva & Pitribhumi-Punyabhumi", "Separate Electorates & Institutional Communalism"]
        },
        {
            "batch_file": "batch_18_ucc_minorities_communalism.md",
            "id": "modern-igp-ucc-minorities",
            "number": "19",
            "title": "Communal Riots, Minoritism & Uniform Civil Code (UCC)",
            "subtitle": "Paul Brass's IRS | Dipankar Gupta | Article 44 | Shah Bano, Sarla Mudgal & Shayara Bano Rulings",
            "scanPages": [121, 122, 123, 124, 125, 126, 127, 128],
            "notebookPages": "Pages 59 to 62",
            "lecture": "Lecture 60 & 61 (01/03/2017 & 02/03/2017)",
            "keyScholars": ["Paul Brass", "Dipankar Gupta", "Asghar Ali Engineer", "Justice Rohinton Nariman", "Flavia Agnes"],
            "coreTheories": ["Institutionalised Riot System (IRS)", "Picnic Riots Theory", "Uniform Civil Code vs Gender Justice", "Substantive Gender Equality vs Communal Polarisation", "Sachar Committee Deprivation Findings"]
        },
        {
            "batch_file": "batch_19_caste_politics_silent_revolution.md",
            "id": "modern-igp-caste-silent-revolution",
            "number": "20",
            "title": "Caste in Indian Politics & The Silent Revolution",
            "subtitle": "Rajni Kothari | M.N. Srinivas Dominant Caste | Christophe Jaffrelot | Yogendra Yadav's Upsurge",
            "scanPages": [129, 130, 131, 132, 133, 134, 135, 136],
            "notebookPages": "Pages 63 to 66",
            "lecture": "Lecture 61 (02/03/2017)",
            "keyScholars": ["Rajni Kothari", "M.N. Srinivas", "Christophe Jaffrelot", "Yogendra Yadav", "Rudolph & Rudolph"],
            "coreTheories": ["Politicisation & Secularisation of Caste", "Dominant Caste Concept", "The Silent Revolution in North India", "Second Democratic Upsurge & Plebeianisation", "Bullock Capitalists & Caste Coalitions (KHAM, AJGAR)"]
        },
        {
            "batch_file": "batch_20_affirmative_action_ethnicity.md",
            "id": "modern-igp-affirmative-action-ethnicity",
            "number": "21",
            "title": "Affirmative Action, Dalit Politics & Ethnicity in India",
            "subtitle": "Mandal Commission | Indra Sawhney 1992 | Kanshi Ram BSP | Donald Horowitz | James Manor",
            "scanPages": [137, 138, 139, 140, 141, 142, 143, 144],
            "notebookPages": "Pages 67 to 70",
            "lecture": "Lecture 62 (03/03/2017)",
            "keyScholars": ["Donald Horowitz", "James Manor", "Kanshi Ram", "Justice Rohini", "Atul Kohli"],
            "coreTheories": ["50% Ceiling & Creamy Layer Exclusion", "Political Power as Master Key", "Cross-Cutting Cleavages vs Cumulative Cleavages", "Inverted U-Curve of Regionalism", "Democratic Accommodation of Sub-Nationalism"]
        },
        {
            "batch_file": "batch_21_party_system_congress_system.md",
            "id": "modern-igp-party-system-congress",
            "number": "22",
            "title": "Party System in India & The Congress System",
            "subtitle": "Maurice Duverger | W.H. Morris-Jones | Rajni Kothari's Congress System | Suhas Palshikar's Life Cycle",
            "scanPages": [145, 146, 147, 148, 149, 150, 151, 152],
            "notebookPages": "Pages 71 to 74",
            "lecture": "Lecture 62 & 63 (03/03/2017)",
            "keyScholars": ["Maurice Duverger", "Giovanni Sartori", "W.H. Morris-Jones", "Rajni Kothari", "Suhas Palshikar", "Zoya Hasan"],
            "coreTheories": ["One-Party Dominant Democratic System", "Party of Consensus vs Parties of Pressure", "Internal Factions as Thermostats", "Congress Hegemony to De-institutionalisation", "Pathological Features of Indian Parties"]
        },
        {
            "batch_file": "batch_22_coalition_politics_bjp_system.md",
            "id": "modern-igp-coalition-politics-bjp",
            "number": "23",
            "title": "Coalition Politics & Rise of Second Dominant Party System",
            "subtitle": "1989-2014 Coalition Era | E. Sridharan | William Riker | Palshikar on BJP Dominance | Presidentialism Debate",
            "scanPages": [153, 154, 155, 156, 157, 158, 159, 160],
            "notebookPages": "Pages 75 to 78",
            "lecture": "Lecture 63 (03/03/2017)",
            "keyScholars": ["E. Sridharan", "William H. Riker", "Vidyut Chakrabarty", "Pratap Bhanu Mehta", "Juan Linz"],
            "coreTheories": ["7 Factors for Rise of Regional Parties", "Oversized Coalitions vs Minimum Winning Coalition", "Coalition by Design vs Coalitions by Political Calculation", "Constructive Vote of No-Confidence", "Perils of Presidentialism in Plural Societies"]
        },
        {
            "batch_file": "batch_23_electoral_reforms_anti_defection.md",
            "id": "modern-igp-electoral-reforms-pressure-groups",
            "number": "24",
            "title": "Rise of BJP, Left Decline, 10th Schedule & Pressure Groups",
            "subtitle": "Integral Humanism | Praful Bidwai | AAP Phenomenon | 10th Schedule Disqualification | Corporate Lobbying",
            "scanPages": [161, 162, 163, 164, 165, 166, 167, 168, 169, 170],
            "notebookPages": "Pages 79 to 83",
            "lecture": "Lecture 64 & 65 (06/03/2017)",
            "keyScholars": ["Deendayal Upadhyay", "Praful Bidwai", "Milan Vaishnav", "Myron Weiner", "Rudolph & Rudolph", "Robert Hardgrave"],
            "coreTheories": ["Integral Humanism & Positive Secularism", "Decline of Left & Phoenix Moment", "AAP Bottom-Up Swaraj Model", "Kihoto Hollohan Judicial Review of Speaker", "Politics of Scarcity & Demand Groups"]
        },
        {
            "batch_file": "batch_24_federalism_theories_constitutional_scheme.md",
            "id": "modern-igp-civil-society-federalism-blueprint",
            "number": "25",
            "title": "Civil Society, Electoral Behaviour & Master Federalism Blueprint",
            "subtitle": "Mukulika Banerjee Why India Votes | Changing MP Profiles | 11 PSIR Federalism Blueprint Questions",
            "scanPages": [171, 172, 173, 174, 175, 176, 177, 178, 179],
            "notebookPages": "Pages 84 to 87",
            "lecture": "Lecture 65 (06/03/2017)",
            "keyScholars": ["Mukulika Banerjee", "B.L. Shankar & Valerian Rodrigues", "Prannoy Roy", "Granville Austin", "K.C. Wheare"],
            "coreTheories": ["Power Inversion Ritual on Polling Day", "Plebeianisation of Parliament", "Strategic Voting of the Poor", "Three-Tier Federalism Architecture", "Master 11-Dimension Federalism Syllabus Blueprint"]
        },
        {
            "batch_file": "batch_25_federalism_state_formation.md",
            "id": "modern-igp-federalism-state-formation",
            "number": "26",
            "title": "Nature of Indian Federalism & Politics of State Formation",
            "subtitle": "K.C. Wheare vs Granville Austin | Article 3 Non-Federal Feature | Louise Tillin 3 Waves | Smaller States Debate",
            "scanPages": [181, 182, 183, 184, 185, 186, 187, 188, 189, 190],
            "notebookPages": "Pages 88 to 92",
            "lecture": "Lecture 66 (07/03/2017)",
            "keyScholars": ["K.C. Wheare", "Granville Austin", "Louise Tillin", "Prof. M.P. Singh", "Prof. Sudha Pai", "Dr. B.R. Ambedkar"],
            "coreTheories": ["Quasi-Federal Ethnocentric Fallacy", "Indestructible Union of Destructible States", "3 Waves of State Formation", "Administrative vs Political Viability of Smaller States", "Democratic Decentralisation via 73rd/74th Amendments"]
        },
        {
            "batch_file": "batch_26_governor_centre_state_relations.md",
            "id": "modern-igp-governor-centre-state-relations",
            "number": "27",
            "title": "Governor's Office & Centre-State Legislative/Admin Relations",
            "subtitle": "Lynchpin vs Agent of Centre | Residuary Powers Art 248 | All India Services | Sarkaria & Punchhi Commissions",
            "scanPages": [191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202],
            "notebookPages": "Pages 93 to 98",
            "lecture": "Lecture 67 (09/03/2017)",
            "keyScholars": ["Soli Sorabjee", "Paul Brass", "Justice R.S. Sarkaria", "Justice M.M. Punchhi", "H.M. Seervai"],
            "coreTheories": ["Dual Role: Constitutional Head vs Union Agent", "Constitution as Product of Partition Insecurity", "Legislative Centralisation via Articles 249/252/253", "Administrative Hegemony & Article 365 Penal Sanction", "Punchhi Commission Reform Roadmap"]
        },
        {
            "batch_file": "batch_27_bommai_water_disputes_niti_aayog.md",
            "id": "modern-igp-bommai-water-disputes-gst",
            "number": "28",
            "title": "Article 356, Bommai Landmark, Water Tribunals, GST & NITI Aayog",
            "subtitle": "S.R. Bommai 1994 | Article 262 Water Tribunals | Fiscal Federalism | 101st Amendment GST Council | NITI Aayog",
            "scanPages": [203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214],
            "notebookPages": "Pages 99 to 104",
            "lecture": "Lectures 68 & 69 (10/03/2017 & 11/03/2017 - Concluding Lectures)",
            "keyScholars": ["Justice P.B. Sawant (Bommai)", "Soli Sorabjee", "Ramaswamy R. Iyer", "B.P. Singhal", "Dr. Y.V. Reddy (14th FC)"],
            "coreTheories": ["Federalism as Basic Structure (Bommai)", "Mandatory Floor Test & Judicial Restoration", "Article 262 Tribunal Bottlenecks (Cauvery, SYL)", "GST Shared Sovereignty & Weighted Voting (Art 279A)", "Team India Platform vs Directive Planning (NITI Aayog)"]
        }
    ]
    return batches

print("Metadata definitions loaded successfully.")
