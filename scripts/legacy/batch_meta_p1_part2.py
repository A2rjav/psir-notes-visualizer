import os
import json
import re

TRANSCRIPTIONS_DIR = "transcriptions_paper1_part2"

def get_paper1_part2_metadata():
    batches = [
        {
            "batch_file": "batch_1_grassroots_democracy_intro.md",
            "id": "igp2-grassroots-intro",
            "number": "01",
            "title": "Grassroots Democracy: Foundations & Constitutional Genesis",
            "subtitle": "Gandhi Swaraj | Roy Radical Democracy | Upadhyay Antyodaya | 73rd/74th CA | Balwant Rai Mehta",
            "scanPages": list(range(1, 11)),
            "notebookPages": "Pages 115 to 117",
            "lecture": "Lecture 3 (17/03/2017)",
            "keyScholars": ["Mahatma Gandhi", "M.N. Roy", "Pt. Deendayal Upadhyay", "Alexis de Tocqueville", "Dr. B.R. Ambedkar", "Mani Shankar Aiyar"],
            "coreTheories": ["Oceanic Circles of Power", "Radical & Partyless Democracy", "Antyodaya & Integral Humanism", "Modernist vs Gandhian Constitutional Clash", "Decentralisation of Corruption Critique"]
        },
        {
            "batch_file": "batch_2_pesa_gram_sabha_evaluation.md",
            "id": "igp2-pesa-gram-sabha",
            "number": "02",
            "title": "Gram Sabha, PESA Act 1996 & PRI Critical Evaluation",
            "subtitle": "Bhuria Committee | Direct Democracy | 3Fs Deficit | Sarpanch Pati | 2nd ARC Recommendations",
            "scanPages": list(range(11, 21)),
            "notebookPages": "Pages 118 to 122",
            "lecture": "Lecture 3 & 4 (17/03/2017 & 18/03/2017)",
            "keyScholars": ["Dilip Singh Bhuria", "Sudha Pai", "George Mathew", "Jean Drèze & Amartya Sen", "Elinor Ostrom"],
            "coreTheories": ["Direct Deliberative Democracy vs Representation", "Tribal Customary Self-Rule (PESA)", "The 3Fs Structural Deficit (Funds, Functions, Functionaries)", "Elite Capture & Sarpanch-Pati Syndrome", "Fiscal Federalism at the Third Tier"]
        },
        {
            "batch_file": "batch_3_grassroot_movements_judiciary_intro.md",
            "id": "igp2-urban-civil-society-judiciary-intro",
            "number": "03",
            "title": "Urban Governance, Grassroots Micro-Movements & Judiciary Blueprint",
            "subtitle": "74th CAA & Smart Cities | Women in PRIs | Rajni & Smitu Kothari | 7 Core Judiciary Questions | Article 142",
            "scanPages": list(range(21, 31)),
            "notebookPages": "Pages 123 to 127",
            "lecture": "Lecture 4 (18/03/2017)",
            "keyScholars": ["Lord Bryce", "Rajni Kothari", "Smitu Kothari", "Amrita Basu", "Ranjitha Mohanty", "Dr. Isher Judge Ahluwalia"],
            "coreTheories": ["Non-Party Political Formations (NPPFs)", "Democratic Deficit in Smart City SPVs", "Women Political Agency vs Proxy Rule", "Judiciary as Sentinel on the Qui Vive", "Counter-Majoritarian Transformative Constitutionalism"]
        },
        {
            "batch_file": "batch_4_judicial_activism_pil_mehta.md",
            "id": "igp2-judicial-review-activism-pil",
            "number": "04",
            "title": "Judicial Review, Judicial Activism & Public Interest Litigation",
            "subtitle": "Marbury v Madison | Gopalan to Maneka Gandhi | Justice Bhagwati & Krishna Iyer | Baxi's SAL | Mehta Paradox",
            "scanPages": list(range(31, 41)),
            "notebookPages": "Pages 128 to 132",
            "lecture": "Lecture 5 (20/03/2017)",
            "keyScholars": ["Chief Justice John Marshall", "Justice P.N. Bhagwati", "Justice V.R. Krishna Iyer", "Prof. Upendra Baxi", "Pratap Bhanu Mehta"],
            "coreTheories": ["Procedure Established by Law vs Due Process of Law", "Post-Emergency Judicial Penitence & Redemption", "Epistolary Jurisdiction & Social Action Litigation (SAL)", "Self-Appointed Guardian & Paradoxical Institution", "Creative Expansion of Article 21 Rights"]
        },
        {
            "batch_file": "batch_5_judges_appointment_njac_overreach.md",
            "id": "igp2-judges-appointment-njac-overreach",
            "number": "05",
            "title": "Judicial Appointments, Collegium System, NJAC & Overreach",
            "subtitle": "1st, 2nd, 3rd Judges Cases | 99th CAA & 4th Judges Case | Montesquieu Separation of Powers | Judicial Accountability",
            "scanPages": list(range(41, 51)),
            "notebookPages": "Pages 133 to 137",
            "lecture": "Lecture 5 & 6 (20/03/2017 & 21/03/2017)",
            "keyScholars": ["Dr. B.R. Ambedkar", "Justice J.S. Khehar", "Justice J. Chelameswar", "Baron de Montesquieu", "Fali S. Nariman"],
            "coreTheories": ["Primacy vs Concurrence in Appointments", "Judicial Independence as Basic Structure", "Collegium Democratic Deficit & Uncle Judges", "Judicial Overreach vs Governance Vacuum", "Institutional Balance and Constitutional Morality"]
        },
        {
            "batch_file": "batch_6_parliament_decline_committees.md",
            "id": "igp2-parliament-decline-committees",
            "number": "06",
            "title": "Union Parliament: Performance, Decline & Committee System",
            "subtitle": "World Bank 6 Parameters | Subhash Kashyap | D.C. Wadhwa Ordinances | DRSCs Scrutiny | Bicameral Continuity",
            "scanPages": list(range(51, 61)),
            "notebookPages": "Pages 138 to 141",
            "lecture": "Lecture 6 (21/03/2017)",
            "keyScholars": ["Subhash Kashyap", "Dr. B.R. Ambedkar", "Walter Bagehot", "Granville Austin", "World Bank Governance Experts"],
            "coreTheories": ["World Bank Six Parameters of Legislative Performance", "Decline of Parliament & Disruptive Opposition", "Ordinance Raj & Fraud on the Constitution (D.C. Wadhwa)", "Departmentally Related Standing Committees (DRSCs) Consensus", "Peter Drunk vs Peter Sober Bicameral Deliberation"]
        },
        {
            "batch_file": "batch_7_president_prime_minister_pmo.md",
            "id": "igp2-president-prime-minister-pmo",
            "number": "07",
            "title": "Union Executive: President, Prime Minister & PMO",
            "subtitle": "Articles 53, 74(1), 75, 78 | Walter Bagehot | K.R. Narayanan Working President | PMO vs Cabinet Secretariat",
            "scanPages": list(range(61, 71)),
            "notebookPages": "Pages 142 to 146",
            "lecture": "Lecture 7 (22/03/2017)",
            "keyScholars": ["Walter Bagehot", "Dr. Rajendra Prasad", "K.R. Narayanan", "Dr. A.P.J. Abdul Kalam", "Ivor Jennings"],
            "coreTheories": ["Dignified vs Efficient Executive Roles", "Presidential Discretion in Hung Parliaments", "Working President Paradigm (Moral Authority)", "Primus Inter Pares vs Prime Ministerial Hegemony", "De-institutionalisation of Cabinet via PMO Centralisation"]
        },
        {
            "batch_file": "batch_8_environmental_movements_guha.md",
            "id": "igp2-environmental-movements-guha",
            "number": "08",
            "title": "Environmental Movements & Political Ecology in India",
            "subtitle": "Guha & Gadgil | Empty Stomach vs Full Stomach | Chipko, Silent Valley & Narmada Bachao | NGT & FRA 2006",
            "scanPages": list(range(71, 81)),
            "notebookPages": "Pages 147 to 151",
            "lecture": "Lecture 7 & 8 (22/03/2017 & 23/03/2017)",
            "keyScholars": ["Ramachandra Guha", "Madhav Gadgil", "Joan Martinez-Alier", "Medha Patkar", "Ronald Inglehart", "Sunderlal Bahuguna"],
            "coreTheories": ["Environmentalism of the Poor vs Post-Materialist Green Politics", "Three Strands: Crusading Gandhian, Ecological Marxist, Appropriate Technologist", "Displacement, Rehabilitation & Human Rights in Mega Dams", "Ecological Destruction as Byproduct of Capitalist Development", "Forest Rights Act 2006 & Ecological Justice"]
        },
        {
            "batch_file": "batch_9_women_dalit_peasant_movements.md",
            "id": "igp2-women-dalit-peasant-movements",
            "number": "09",
            "title": "Women, Dalit & Peasant Social Movements",
            "subtitle": "Towards Equality 1974 | Dalit Panthers & Gail Omvedt | Old vs New Peasant Struggles | Sharad Joshi & Tikait",
            "scanPages": list(range(81, 91)),
            "notebookPages": "Pages 152 to 156",
            "lecture": "Lecture 8 (23/03/2017)",
            "keyScholars": ["Gail Omvedt", "Neera Desai & Maithreyi Krishnaraj", "Namdeo Dhasal", "Kanshi Ram", "Sharad Joshi"],
            "coreTheories": ["Shift from Colonial Social Reform to Autonomous Feminist Agency", "Dalit Panthers Radical Assertion vs Electoral Politics", "Old Class-based Agrarian Unrest vs New Peasant Market Demands", "Bharat vs India Contradiction", "Intersectionality of Caste, Gender, and Agrarian Labour"]
        },
        {
            "batch_file": "batch_10_planning_economic_development.md",
            "id": "igp2-planning-economic-development",
            "number": "10",
            "title": "Planning Models, 1991 LPG Reforms & NITI Aayog",
            "subtitle": "Nehru-Mahalanobis Strategy | BoP Crisis & Washington Consensus | Tendulkar vs Rangarajan | Cooperative Federalism",
            "scanPages": list(range(91, 101)),
            "notebookPages": "Pages 157 to 161",
            "lecture": "Lecture 9 (24/03/2017)",
            "keyScholars": ["P.C. Mahalanobis", "Dr. Manmohan Singh", "Suresh Tendulkar", "C. Rangarajan", "Amartya Sen", "Jagdish Bhagwati"],
            "coreTheories": ["Commanding Heights of the Economy & Heavy Industrialisation", "Washington Consensus & Structural Adjustment Programme", "Jobless Growth & Widening Regional/Social Disparities", "Bhagwati vs Sen Debate on Growth vs Redistribution", "Cooperative & Competitive Federalism via NITI Aayog"]
        },
        {
            "batch_file": "batch_11_land_reforms_green_revolution.md",
            "id": "igp2-land-reforms-green-revolution",
            "number": "11",
            "title": "Land Reforms, Green Revolution & Agrarian Crisis",
            "subtitle": "4 Pillars of Land Reforms | Operation Barga | Bullock Capitalists | Ecological Fallout | Second Green Revolution",
            "scanPages": list(range(101, 111)),
            "notebookPages": "Pages 162 to 166",
            "lecture": "Lecture 9 & 10 (24/03/2017 & 25/03/2017)",
            "keyScholars": ["P.C. Joshi", "Daniel Thorner", "Rudolph & Rudolph", "M.S. Swaminathan", "Utsa Patnaik"],
            "coreTheories": ["Institutional vs Technological Solutions to Rural Stagnation", "Operation Barga & Political Will in Land Reforms", "Rise of Intermediate Classes & Bullock Capitalists", "Ecological & Social Crises of the Green Revolution", "Agrarian Distress and Terms of Trade Imbalance"]
        },
        {
            "batch_file": "batch_12_basic_structure_constitutionalism.md",
            "id": "igp2-basic-structure-constitutionalism",
            "number": "12",
            "title": "Constitutionalism & The Basic Structure Doctrine",
            "subtitle": "Shankari Prasad to Golaknath | 24th/25th CA | Kesavananda Bharati 1973 | Minerva Mills & I.R. Coelho",
            "scanPages": list(range(111, 121)),
            "notebookPages": "Pages 167 to 171",
            "lecture": "Lecture 10 (25/03/2017)",
            "keyScholars": ["Chief Justice S.M. Sikri", "N.A. Palkhivala", "Justice H.R. Khanna", "Granville Austin", "Upendra Baxi"],
            "coreTheories": ["Constitutionalism as Limited Government", "Parliamentary Constituent Power vs Judicial Review", "Basic Identity and Essential Features Doctrine", "Golden Triangle (Articles 14, 19, 21)", "Harmonious Balance between Fundamental Rights and DPSPs"]
        },
        {
            "batch_file": "batch_13_affirmative_action_deprivation_index.md",
            "id": "igp2-affirmative-action-deprivation-index",
            "number": "13",
            "title": "Affirmative Action, Caste Reservations & Deprivation Index",
            "subtitle": "Articles 15(4), 16(4) | Ronald Dworkin | Backwardness Contestations | Dalit Christian/Muslim Debates | Yogendra Yadav",
            "scanPages": list(range(121, 131)),
            "notebookPages": "Pages 172 to 176",
            "lecture": "Lecture 11 (27/03/2017)",
            "keyScholars": ["Ronald Dworkin", "Marc Galanter", "Yogendra Yadav", "Justice Rohini", "Andre Beteille"],
            "coreTheories": ["Equal Treatment vs Treatment as Equals (Substantive Equality)", "Compensatory Discrimination Doctrine", "Race to the Bottom for Backwardness Status", "Secularisation of Caste vs Religious Exclusions", "Multi-layered Evidence-based Deprivation Index"]
        },
        {
            "batch_file": "batch_14_bku_shetkari_farmers_pressure_groups.md",
            "id": "igp2-farmers-pressure-groups-bku-shetkari",
            "number": "14",
            "title": "Farmers' Pressure Groups: BKU vs Shetkari Sangathan",
            "subtitle": "Sharad Joshi 'Bharat vs India' | Mahendra Singh Tikait Clan Mobilisation | Direct Action Tactics | Limitations",
            "scanPages": list(range(131, 141)),
            "notebookPages": "Pages 177 to 181",
            "lecture": "Lecture 11 & 12 (27/03/2017 & 28/03/2017)",
            "keyScholars": ["Sharad Joshi", "Mahendra Singh Tikait", "Ghanshyam Shah", "Tom Brass", "Zoya Hasan"],
            "coreTheories": ["New Farmers' Movement (NFM) as Non-Party Demand Group", "Internal Colonialism: Bharat vs India Paradigm", "Khap & Clan Mobilisation in Agrarian Politics", "Direct Action: Rasta Roko, Gherao & Produce Withholding", "Structural Marginalisation of Landless Agricultural Labourers"]
        },
        {
            "batch_file": "batch_15_sovereignty_rss_pressure_group_synthesis.md",
            "id": "igp2-sovereignty-rss-synthesis",
            "number": "15",
            "title": "Theories of Sovereignty & RSS as Pressure Group",
            "subtitle": "Austin Monism vs Laski Pluralism | RSS Organisational Matrix | Christophe Jaffrelot | IGP Part 2 Master Synthesis",
            "scanPages": list(range(141, 151)),
            "notebookPages": "Pages 182 to 186",
            "lecture": "Lecture 12 (28/03/2017 - Concluding Session of IGP Part 2)",
            "keyScholars": ["John Austin", "Harold Laski", "J.N. Figgis", "R.M. MacIver", "Christophe Jaffrelot"],
            "coreTheories": ["Monistic Legal Sovereignty vs Pluralist Associational Autonomy", "Society is Federal, Authority Must Be Federal", "RSS Shakha Network as Cultural-Political Pressure Group", "Sangh Parivar Affiliate Transmission Belts (VHP, ABVP, BMS)", "Grand Synthesis of Indian Constitutional & Political Dynamics"]
        }
    ]
    return batches

if __name__ == "__main__":
    b = get_paper1_part2_metadata()
    print(f"Loaded {len(b)} batch metadata definitions for Paper 1 Part 2.")
