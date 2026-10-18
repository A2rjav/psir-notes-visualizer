import os
import json
import re

from batch_meta_p1_part5 import get_paper1_part5_metadata
from batch_parser_p1_part5 import parse_markdown_to_concepts, parse_flashcards, parse_model_answers

def build_paper1_part5():
    target_file = "app/src/data/paper1Part5Data.js"
    
    meta = {
        "paper": "Paper 1 (WPT Part I: Plato to Hannah Arendt)",
        "topicTitle": "Paper 1 (Section A): Western Political Thought (Part I) — Classical to Contemporary",
        "summary": "Exhaustive, 100% zero-loss digital knowledge repository of Shubhra Ranjan IAS lecture notes covering the seminal foundations of Western Political Thought from Ancient Greece to 20th Century Critical Philosophy: Plato (Theory of Forms, Cave Allegory, Philosopher King, Justice, Communism, Popper's Critique), Aristotle (Teleology, State as Natural, Citizenship, Slavery, Property, Revolution, Polity & Rule of Law), Niccolò Machiavelli (Renaissance Realism, Lion & Fox, Virtù vs Fortuna, Separation of Politics & Ethics), Thomas Hobbes (Scientific Materialism, State of Nature, Leviathan, Sovereignty, Individualism), John Locke (Natural Rights to Life, Liberty & Estate, Labour Theory of Property, Limited Government, Constitutionalism), Jean-Jacques Rousseau (Discourse on Inequality, General Will, Direct Democracy, Forced to be Free), J.S. Mill (Revision of Utilitarianism, On Liberty, Harm Principle, Representative Government, Subjection of Women), Karl Marx (Alienation, Historical Materialism, Surplus Value, Class Struggle, Communism), Antonio Gramsci (Hegemony, Civil vs Political Society, Organic Intellectuals, War of Position), and Hannah Arendt (Vita Activa, Labor-Work-Action, Public Realm, Power in Concert, Totalitarianism & Banality of Evil).",
        "notebookPages": "Notebook Pages 1 to 116 (180 Scan Pages: 001 to 180)",
        "scanStart": 1,
        "scanEnd": 180,
        "scanBasePath": "/scans_p1_part5"
    }
    
    batches = get_paper1_part5_metadata()
    sections = []
    flashcards = []
    answers = []
    
    fc_id_counter = 1
    ans_id_counter = 1
    
    for b in batches:
        md_path = os.path.join("transcriptions_paper1_part5", b["batch_file"])
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
        print(f"Part 5 Batch {b['number']} ({b['batch_file']}): {len(concepts)} concepts extracted.")
        
    # Generate 180-page scansCatalog
    page_catalog_titles = {
        1: "Western Political Thought Part I Title Page & Cover (Shubhra Ranjan IAS)",
        2: "Volume Flyleaf & Syllabus Overview: Plato to Hannah Arendt",
        3: "Table of Contents & Thinker Roadmap: Ancient, Medieval, Modern & Critical Canon",
        4: "Introduction to Western Philosophy: Dialectics, Epistemology & Normative Theory",
        5: "Socrates: Knowledge is Virtue, Dialectical Method & Socratic Irony",
        6: "Plato's Problematique: Crisis of Athens & Search for the Ideal State",
        7: "Plato's Theory of Ideas / Forms: World of Matter vs World of Pure Forms",
        8: "Allegory of the Cave: Shadows, Liberation, Sun & Epistemic Ascent",
        9: "The Tripartite Soul: Reason (Gold), Courage (Silver), Appetite (Copper/Bronze)",
        10: "Virtue Ethics: Wisdom, Courage, Temperance & Harmonious Justice",
        11: "Plato's Theory of Justice: Architectonic Principle of Functional Specialization",
        12: "The Philosopher King: Unchallenged Rule of Reason & Wisdom",
        13: "Philosopher King: Absolute Power Barring Constitutional Change",
        14: "Plato's Scheme of Education: Elementary, Secondary & Higher Dialectics",
        15: "Communism of Property & Family: Emancipating Guardians from Private Bias",
        16: "Plato's Feminism: Equality of Women Guardians & Republic Book V",
        17: "The Decline of the Ideal State: Timocracy, Oligarchy, Democracy, Tyranny",
        18: "Karl Popper's Indictment: The Open Society and Its Enemies (Plato as Totalitarian)",
        19: "Barker, Sabine & Levinson Defenses: Plato as Utopian Moral Reformer",
        20: "Plato's The Statesman & The Laws: Sub-Ideal State & Nocturnal Council",
        21: "Transition to Aristotle: From Utopian Idealism to Empirical Realism",
        22: "Aristotle: Father of Political Science & Common Sense Philosophy",
        23: "Critique of Plato's Extreme Unity, Radical Communism & Philosopher King",
        24: "Aristotle's Teleology: Potentiality, Actuality & Final Cause of the State",
        25: "State Originating for Bare Life, Continuing for the Good Life",
        26: "Man is by Nature a Political Animal (Zoon Politikon)",
        27: "State as Prior to Man: Organic Analogy & Teleological Priority",
        28: "Aristotle's Theory of Citizenship: Civic Deliberation & Judicial Participation",
        29: "Exclusion of Women, Slaves, Mechanics, Labourers & Elderly from Citizenship",
        30: "Aristotle's Defense of Natural Slavery: Mental vs Physical Superiority",
        31: "Aristotle's Defense of Private Property: Instinctive, Generous & Efficient",
        32: "Aristotle's Theory of Justice: General Justice vs Particular Justice",
        33: "Distributive Justice (Proportionate to Merit) vs Corrective/Rectificatory Justice",
        34: "Aristotle on Revolutions (Stasis): General, Specific & Particular Causes",
        35: "Preventive Measures against Revolutions: Civic Moderation & Law Observance",
        36: "Classification of Constitutions: Quantitative vs Qualitative (Pure vs Corrupt Forms)",
        37: "Polity as the Best Practicable State: Rule of Middle Class & Golden Mean",
        38: "Aristotle on Rule of Law: Reason Free from All Passion",
        39: "Aristotle vs Plato: Comparative Synthesis & UPSC Mains Analytical Matrix",
        40: "Medieval Political Thought Overview: St. Augustine & St. Thomas Aquinas (Two Swords)",
        41: "Transition to Modernity: Renaissance, Secularisation & Rise of Sovereign State",
        42: "Niccolò Machiavelli: Child of Renaissance & Father of Modern Realpolitik",
        43: "Machiavelli's Problematique: Fragmentation of Italy & Foreign Invasions",
        44: "Autonomy of Politics: Emancipation of Politics from Church & Christian Ethics",
        45: "Pessimistic Anthropology: Human Nature as Ungrateful, Fickle, Deceitful & Greedy",
        46: "Men Forget Death of Father Sooner Than Loss of Patrimony",
        47: "Double Standard of Morality: Statecraft Morality vs Private Conscience",
        48: "The Prince: Combining the Cunning of the Fox and the Ferocity of the Lion",
        49: "Virtù vs Fortuna: Overcoming Unpredictable Fortune through Bold Audacity",
        50: "Machiavelli on Religion: Instrumentum Regni (Religion as Tool of State Stability)",
        51: "Machiavelli's Discourses on Livy: Republicanism, Civic Virtue & Mixed Constitution",
        52: "Scholarly Debates on Machiavelli: Leo Strauss, Benedetto Croce, Quentin Skinner, Gramsci",
        53: "Machiavelli & Kautilya: Comparative Analysis in Realpolitik & Diplomacy",
        54: "Social Contract Tradition Overview: Hobbes, Locke, Rousseau Foundations",
        55: "Thomas Hobbes: Historical Context of the English Civil War (1642-1651)",
        56: "Scientific Materialism: Motion of Atoms, Appetites, Aversions & Geometry of Passion",
        57: "Resolutive-Compositive Method: Deconstructing Society to Individual Atoms",
        58: "Hobbesian Human Nature: Perpetual and Restless Desire of Power after Power",
        59: "State of Nature: Equality of Vulnerability & War of All Against All (Bellum Omnium)",
        60: "Life of Man as Solitary, Poor, Nasty, Brutish, and Short",
        61: "Natural Law in Hobbes: Prudence of Self-Preservation & Articles of Peace",
        62: "The Social Contract: Surrender of All Natural Rights Save Self-Preservation",
        63: "Covenants Without Swords Are But Words: Need for Absolute Coercive Sovereign",
        64: "The Leviathan: Absolute, Indivisible, Inalienable & Irrevocable Sovereignty",
        65: "Liberty of Subjects in Hobbes: Silence of the Law & Right of Resistance",
        66: "Hobbes as the Greatest Individualist: Macpherson & Oakeshott Interpretations",
        67: "Hobbes' Legacy: First Modern Theorist of Sovereign State & Positivist Law",
        68: "Transition from Hobbes to Locke: Glorious Revolution (1688) & Constitutionalism",
        69: "John Locke: Two Treatises of Civil Government Problematique",
        70: "First Treatise: Refutation of Sir Robert Filmer's Patriarcha (Divine Right of Kings)",
        71: "Second Treatise: Locke's Theory of Human Nature as Rational, Moral & Benevolent",
        72: "Lockean State of Nature: State of Peace, Goodwill, Mutual Assistance & Preservation",
        73: "Inconveniences of State of Nature: Lack of Established Law, Judge & Executive",
        74: "Natural Rights: Inalienable Rights to Life, Liberty, and Estate (Property)",
        75: "Labour Theory of Property: Mixing Bodily Labour with Unowned Natural Bounty",
        76: "Lockean Provisos: Enough and as Good Left for Others, Non-Spoilage Proviso",
        77: "Invention of Money & Legitimisation of Unlimited Capital Accumulation (Macpherson)",
        78: "Two Contracts: Civil Society Creation & Formation of Fiduciary Government",
        79: "Limited Government: Government as Trustee, Legislative Supremacy & Rule of Law",
        80: "Doctrine of Toleration & Separation of Church from Civil Magistrate",
        81: "Right to Revolution: Appeal to Heaven against Sovereign Breach of Fiduciary Trust",
        82: "Locke as Father of Classical Liberalism: Constitutionalism & Individual Rights",
        83: "Transition to Jean-Jacques Rousseau: Enlightenment & Romantic Revolt",
        84: "Rousseau's First Discourse: Has Progress in Arts and Sciences Corrupted Morals?",
        85: "Rousseau's Second Discourse: Origin and Foundations of Inequality Among Men",
        86: "The Noble Savage: Self-Love (Amour de Soi) vs Pity/Compassion (Pitié)",
        87: "Emergence of Private Property: 'The first man who fenced off a plot of land...'",
        88: "Degeneration into Amour Propre (Vanity), Deception, Class Conflict & Misery",
        89: "The Fraudulent Social Contract: Rich Entrenching Inequality via Law and State",
        90: "The Legitimate Social Contract: 'Man is born free, and everywhere he is in chains'",
        91: "Surrender to the Entire Community: Alienation of All Rights to Gain Equal Moral Liberty",
        92: "The General Will (Volonté Générale): Synthesis of Real Wills Oriented to Common Good",
        93: "General Will vs Will of All (Volonté de Tous): Quality vs Mere Numerical Aggregation",
        94: "Properties of the General Will: Inalienable, Indivisible, Infallible & Absolute",
        95: "Direct Democracy & Rejection of Representative Government (English Only Free on Election Day)",
        96: "Paradox of Freedom: 'Forced to be Free' & Jacob Talmon's Totalitarian Critique",
        97: "Rousseau's Enduring Legacy: Father of Romanticism, Radical Democracy & Communitarianism",
        98: "Social Contract Trio: Hobbes vs Locke vs Rousseau Comparative Synthesis",
        99: "Transition to Utilitarianism & Classical Liberalism: Bentham to J.S. Mill",
        100: "Jeremy Bentham: Quantitative Utilitarianism (Pleasure vs Pain, Felicific Calculus)",
        101: "Pushpin is as Good as Poetry: Benthamite Egalitarian Hedonism & Rights as Nonsense",
        102: "J.S. Mill: Crisis of Faith & Revision of Benthamite Utilitarian Dogma",
        103: "Qualitative Pleasures: 'Better to be a human dissatisfied than a pig satisfied'",
        104: "On Liberty (1859): Defending Individuality against Social Conformity",
        105: "Tyranny of the Majority: Public Opinion as More Oppressive than Political Despotism",
        106: "Absolute Freedom of Speech: 'If all mankind minus one were of one opinion...'",
        107: "The Harm Principle: Self-Regarding vs Other-Regarding Actions",
        108: "Mill's Exceptions to Liberty: Children, Backward Societies (Barbarism), Self-Harm",
        109: "Considerations on Representative Government: Mill as a 'Reluctant Democrat' (Wayper)",
        110: "Defense of Plural Voting, Proportional Representation & Open Ballot",
        111: "Subjection of Women (1869): First Male Feminist & Legal Emancipation of Women",
        112: "Transition from Liberalism to Scientific Socialism: Karl Marx",
        113: "Young Marx & Left Hegelianism: Feuerbach's Materialist Inversion of Hegel",
        114: "Economic and Philosophic Manuscripts of 1844: Theory of Alienation (Entfremdung)",
        115: "Four Dimensions of Alienation: From Product, Process, Species-Being, Fellow Workers",
        116: "Historical Materialism: Dialectical Development of Productive Forces",
        117: "Base and Superstructure Model: Economic Substructure Determining Consciousness",
        118: "Forces of Production vs Relations of Production: Engine of Historical Transformation",
        119: "Four Epochs of Human History: Primitive Communism, Ancient, Feudal, Capitalist",
        120: "The Communist Manifesto (1848): 'The history of all hitherto existing society is class struggle'",
        121: "Class Polarization: Bourgeoisie vs Proletariat & Destruction of Middle Strata",
        122: "Labour Theory of Value & Theory of Surplus Value (Das Kapital)",
        123: "Exploitation & Absolute vs Relative Surplus Value Extraction",
        124: "Internal Contradictions of Capitalism: Tendency of the Rate of Profit to Fall",
        125: "Class-in-itself (Klasse an sich) to Class-for-itself (Klasse für sich)",
        126: "The State in Marxist Theory: Executive Committee of the Ruling Bourgeoisie",
        127: "Relative Autonomy of the State: The 18th Brumaire of Louis Bonaparte",
        128: "Dictatorship of the Proletariat: Transitory Stage of Socialism",
        129: "Withering Away of the State & Stateless, Classless Communist Society",
        130: "Marxian Critiques: Karl Popper (Historicist Pseudoscience), Max Weber, Frankfurt School",
        131: "Transition to Western Marxism: Antonio Gramsci & Cultural Hegemony",
        132: "Gramsci's Prison Notebooks: Critique of Crude Economic Determinism",
        133: "Gramsci as Theorist of Superstructure: Philosophy of Praxis",
        134: "Two Tiers of Superstructure: Political Society (Force) vs Civil Society (Consent)",
        135: "Concept of Hegemony (Egemonia): Cultural, Moral & Intellectual Leadership",
        136: "Manufacturing Consent: Common Sense (Sensata) vs Good Sense (Buon Senso)",
        137: "Organic Intellectuals vs Traditional Intellectuals in Sustaining Hegemony",
        138: "The Modern Prince: The Communist Party as Collective Intellectual",
        139: "Historic Bloc (Blocco Storico): Dialectical Fusion of Base and Superstructure",
        140: "Revolutionary Strategy: War of Movement (Direct Attack) vs War of Position (Cultural Siege)",
        141: "Gramsci's Relevance in Contemporary Cultural Politics & Subaltern Studies",
        142: "Transition to 20th Century Phenomenological Politics: Hannah Arendt",
        143: "Hannah Arendt's Intellectual Milieu: Existentialism, Nazism & Holocaust",
        144: "Rejection of the Label 'Political Philosopher': Theorist of the Political",
        145: "The Human Condition (1958): Vita Activa vs Vita Contemplativa",
        146: "Three Modalities of Vita Activa: Labor (Animal Laborans / Biological Necessity)",
        147: "Work (Homo Faber / Fabrication of Worldly Durability & Artifacts)",
        148: "Action (Zoon Politikon / Highest Realization of Freedom and Human Plurality)",
        149: "Two Attributes of Action: Speech (Lexis) and Deed (Praxis)",
        150: "Natality: The Human Capacity for New Beginnings and Spontaneity",
        151: "Plurality: 'Men, not Man, live on the earth and inhabit the world'",
        152: "The Public Realm: The Space of Appearance, Agonistic Polis & Glory",
        153: "The Rise of the 'Social': Colonization of the Public Sphere by Economic Concerns",
        154: "Arendt's Conception of Power: Power as Acting in Concert (Non-Zero-Sum)",
        155: "Power vs Strength, Force, Authority, and Violence (On Violence, 1969)",
        156: "Violence Destroys Power: Totalitarian Rule Can Never Rest on Genuine Power",
        157: "The Origins of Totalitarianism (1951): Antisemitism, Imperialism, Totalitarian Terror",
        158: "Totalitarianism as Novel Tyranny: Ideology and Terror Total Subjugation",
        159: "The Atomised Mass Man: Loneliness as Groundwork for Totalitarian Domination",
        160: "Eichmann in Jerusalem (1963): Report on the Banality of Evil",
        161: "The Banality of Evil: Thoughtlessness, Inability to Judge & Bureaucratic Obedience",
        162: "Moral Responsibility vs Collective Guilt: Thinking and Judging for Oneself",
        163: "Hannah Arendt on Revolution: American Revolution vs French Revolution",
        164: "Council Democracy & Participatory Public Spheres vs Representative Party Oligarchies",
        165: "Arendt's Contemporary Resonance: Democratic Deficits, Post-Truth & Authoritarianism",
        166: "Master Cross-Linkage Matrix 1: Ancient vs Modern Notions of Justice & Citizenship",
        167: "Master Cross-Linkage Matrix 2: Social Contract Traditions (Hobbes, Locke, Rousseau)",
        168: "Master Cross-Linkage Matrix 3: Theories of Liberty (Negative, Positive, Republican)",
        169: "Master Cross-Linkage Matrix 4: Marxist Canon Evolution (Marx to Gramsci to Arendt)",
        170: "Master Cross-Linkage Matrix 5: The Concept of the State across 2,400 Years of Western Thought",
        171: "Master Cross-Linkage Matrix 6: Epistemology & Political Action (Plato Cave to Arendt Polis)",
        172: "UPSC PSIR Mains Model Answer Synthesis 1: Plato vs Karl Popper",
        173: "UPSC PSIR Mains Model Answer Synthesis 2: Aristotle's Teleology & Rule of Law",
        174: "UPSC PSIR Mains Model Answer Synthesis 3: Machiavelli's Autonomous Statecraft",
        175: "UPSC PSIR Mains Model Answer Synthesis 4: Hobbes's Leviathan as Peak Individualism",
        176: "UPSC PSIR Mains Model Answer Synthesis 5: Locke's Property Rights & Constitutionalism",
        177: "UPSC PSIR Mains Model Answer Synthesis 6: Rousseau's General Will & Paradox of Freedom",
        178: "UPSC PSIR Mains Model Answer Synthesis 7: J.S. Mill's Liberty & Harm Principle",
        179: "UPSC PSIR Mains Model Answer Synthesis 8: Gramsci's Hegemony vs Arendt's Vita Activa",
        180: "Grand Epilogue: Complete Thematic Archival Index of Western Political Thought Part I"
    }
    
    scans_catalog = []
    for p in range(1, 181):
        num_str = f"{p:03d}"
        f_name = f"page_{num_str}.png"
        
        batch_num = "01"
        for b in batches:
            if p in b["scanPages"]:
                batch_num = b["number"]
                break
                
        title = page_catalog_titles.get(p, f"WPT Part I Lecture Discussion - Page {p}")
        
        scans_catalog.append({
            "pageNumber": p,
            "filename": f_name,
            "title": title,
            "batch": batch_num,
            "thumbnail": f"/scans_p1_part5/{f_name}",
            "fullImage": f"/scans_p1_part5/{f_name}"
        })
        
    js_content = f"""// UPSC PSIR Paper 1 (Section A): Western Political Thought Part I (Plato to Hannah Arendt)
// Compiled from 180 Scan Pages of Shubhra Ranjan IAS Handwritten Lecture Notes
// 100% Zero-Loss Digital Repository with Interactive Dual-Pane Scan Inspection

export const paper1Part5Metadata = {json.dumps(meta, indent=2)};

export const paper1Part5Sections = {json.dumps(sections, indent=2)};

export const paper1Part5Flashcards = {json.dumps(flashcards, indent=2)};

export const paper1Part5ModelAnswers = {json.dumps(answers, indent=2)};

export const paper1Part5ScansCatalog = {json.dumps(scans_catalog, indent=2)};
"""
    
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"Successfully generated {target_file} ({os.path.getsize(target_file)} bytes).")

if __name__ == "__main__":
    build_paper1_part5()
