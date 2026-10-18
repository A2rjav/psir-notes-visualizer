import os
import json
import re

from batch_meta_p1_part4 import get_paper1_part4_metadata
from batch_parser_p1_part4 import parse_markdown_to_concepts, parse_flashcards, parse_model_answers

def build_paper1_part4():
    target_file = "app/src/data/paper1Part4Data.js"
    
    meta = {
        "paper": "Paper 1 (WPT Part II & Political Theory)",
        "topicTitle": "Paper 1 (Section A): Western Political Thought (Part II) & Political Theory",
        "summary": "Exhaustive, 100% zero-loss digital knowledge repository of Shubhra Ranjan IAS lecture notes covering Political Ideologies (Idealism, Classical Liberalism, Modern Liberalism, Neo-Liberalism, Social Liberalism), Multiculturalism (Will Kymlicka, Bhikhu Parekh, Charles Taylor), Socialism & Classical Marxism, Neo-Marxism & Frankfurt School Critical Theory, Totalitarianism & Fascism, Feminism (Waves, Schools & Intersectionality), Theories of the State (Liberal, Instrumental vs Structural Marxism, Pluralist, Post-Colonial), Concept of Power (Lukes Three Dimensions, Weber, Foucault Power/Knowledge), Hegemony, Ideology & Legitimacy, Theories of Democracy (Elitist, Pluralist, Participatory, Deliberative), Concept of Rights & Human Rights Generations, Concept of Justice (John Rawls, Nozick, Sen, Communitarians), Concept of Equality (Dworkin, Sen, Walzer), and Decline & Resurgence of Political Theory.",
        "notebookPages": "Notebook Pages 88 to 205 (224 Scan Pages: 001 to 224)",
        "scanStart": 1,
        "scanEnd": 224,
        "scanBasePath": "/scans_p1_part4"
    }
    
    batches = get_paper1_part4_metadata()
    sections = []
    flashcards = []
    answers = []
    
    fc_id_counter = 1
    ans_id_counter = 1
    
    for b in batches:
        md_path = os.path.join("transcriptions_paper1_part4", b["batch_file"])
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
        print(f"Batch {b['number']} ({b['batch_file']}): {len(concepts)} concepts extracted.")
        
    # Generate 224-page scansCatalog
    page_catalog_titles = {
        1: "WPT Part II & Political Theory Volume Title & Cover (Shubhra Ranjan 2017)",
        2: "Volume Front Leaf / Blank",
        3: "Volume Table of Contents: Ideologies, State, Power, Democracy, Rights, Justice, Equality",
        4: "Course Syllabus Roadmap: Political Theory Syllabus Framework",
        5: "Political Ideologies: Idealism (Socrates, Plato, Aristotle, Rousseau, Hegel, Kant, Green)",
        6: "Schools of Idealism: Hegelian German Tradition vs Kantian vs British Oxford Idealists",
        7: "Divine Right of Kings vs Rational Idealism on State Absolutism",
        8: "Classical Liberalism: Historical Genesis, Feudalism Collapse & Commercial Bourgeoisie",
        9: "Classical Liberal Assumptions: Atomistic Individualism & Rational Self-Interest",
        10: "John Locke: Father of Classical Liberalism & Natural Rights Theory",
        11: "C.B. Macpherson: Theory of Possessive Individualism Explained",
        12: "Classical Liberal State: Negative Liberty & Nightwatchman / Laissez-Faire State",
        13: "Adam Smith: Wealth of Nations, Division of Labour & Market Invisible Hand",
        14: "Jeremy Bentham: Classical Utilitarianism (Greatest Happiness of the Greatest Number)",
        15: "Utilitarian Quantitative Hedonism: Felicific Calculus & Panopticon",
        16: "Modern Liberalism (Positive Liberalism): Genesis in Industrial Misery",
        17: "J.S. Mill: Revision of Utilitarianism (Qualitative Pleasure & Harm Principle)",
        18: "J.S. Mill on Individuality & Liberty as Engine of Human Progress",
        19: "T.H. Green: Idealist Liberalism & Positive Concept of Liberty",
        20: "T.H. Green: State as Hindrance to Hindrances & Common Good",
        21: "Harold Laski: Welfare State, Economic Planning & Pluralist Sovereignty",
        22: "John Maynard Keynes: General Theory & State Demand Management",
        23: "The Welfare State in Crisis: Stagflation of the 1970s",
        24: "Neo-Liberalism (Libertarianism): Revival of Negative Liberty & Free Markets",
        25: "Friedrich Hayek: The Road to Serfdom & Market as Spontaneous Order (Catallaxy)",
        26: "Hayek's Mirage of Social Justice: Market Distribution Cannot Be Just or Unjust",
        27: "Robert Nozick: Anarchy, State, and Utopia & Self-Ownership Principle",
        28: "Nozick's Entitlement Theory: Just Acquisition, Just Transfer & Rectification",
        29: "Milton Friedman: Capitalism and Freedom & Monetarist Economic Policy",
        30: "Social Liberalism: Rawls, Dworkin & Amartya Sen Synthesis",
        31: "Multiculturalism: Emergence in Plural Post-Colonial Societies",
        32: "Critique of Universal Assimilation: Melting Pot vs Salad Bowl / Mosaic",
        33: "Iris Marion Young: Justice and the Politics of Difference",
        34: "Will Kymlicka: Multicultural Citizenship & Liberal Theory of Minority Rights",
        35: "Kymlicka's Typology: National Minorities vs Immigrant Polyethnic Groups",
        36: "Group-Differentiated Rights: Self-Government, Polyethnic & Special Representation",
        37: "Internal Restrictions vs External Protections in Multicultural Rights",
        38: "Bhikhu Parekh: Rethinking Multiculturalism & Cultural Embeddedness of Humans",
        39: "Parekh's Theory of Intercultural Dialogue & Dialogue between Equals",
        40: "Charles Taylor: Politics of Recognition & Human Need for Recognition",
        41: "Dignity vs Authenticity: Historical Transition from Feudal Honour",
        42: "Feminist Critique of Multiculturalism: Susan Moller Okin",
        43: "Is Multiculturalism Bad for Women: Patriarchal Cultural Practices",
        44: "Liberal Universalist Counter-Critique: Brian Barry's Culture and Equality",
        45: "Synthesis of Multiculturalism Debates in Contemporary Global Politics",
        46: "Socialism: Core Philosophy, Community & Rejection of Capitalist Egoism",
        47: "Utopian Socialists: Robert Owen (New Lanark Cooperatives)",
        48: "Saint-Simon & Charles Fourier (Phalansteries & Social Cooperation)",
        49: "Evolutionary Socialism: Eduard Bernstein & Revisionism",
        50: "Fabian Socialism: Sidney & Beatrice Webb, G.B. Shaw (Inevitability of Gradualness)",
        51: "Guild Socialism: G.D.H. Cole & Workers' Control of Industry",
        52: "Syndicalism: Direct Industrial Action, General Strike & Stateless Production",
        53: "Scientific Socialism (Marxism): Genesis & Critique of Utopian Thought",
        54: "Dialectical Materialism: Hegel's Dialectic Placed on Materialist Feet",
        55: "Historical Materialism: Forces of Production, Relations of Production & Base-Superstructure",
        56: "Five Historical Modes of Production: Primitive, Slavery, Feudal, Capitalist, Communist",
        57: "Theory of Surplus Value: Absolute vs Relative Surplus Value",
        58: "Theory of Class Struggle: 'History of all hitherto existing society is history of class struggles'",
        59: "Theory of Alienation (Economic and Philosophic Manuscripts of 1844)",
        60: "Four Dimensions of Alienation: Product, Nature/Labour, Species-Essence, Fellow Men",
        61: "Dictatorship of the Proletariat & Withering Away of the State (Engels)",
        62: "Western Marxism: Critique of Soviet Economism & Dialectical Dogmatism",
        63: "György Lukács: History and Class Consciousness & Concept of Reification",
        64: "Antonio Gramsci: Life in Fascist Prison & Prison Notebooks",
        65: "Gramsci's Hegemony: Intellectual and Moral Leadership (Direzione)",
        66: "Gramsci's Civil Society vs Political Society: Dual Hegemony Framework",
        67: "Organic Intellectuals vs Traditional Intellectuals in Class Struggle",
        68: "War of Position (Trench Warfare) vs War of Movement (Frontal Assault)",
        69: "Frankfurt School Critical Theory: Max Horkheimer & Critical vs Traditional Theory",
        70: "Theodor Adorno: Negative Dialectics & Culture Industry as Mass Stupefaction",
        71: "Adorno & Horkheimer: Dialectic of Enlightenment (Reason Turned into Domination)",
        72: "Herbert Marcuse: One-Dimensional Man & Erosion of Critical Thought",
        73: "Repressive Desublimation: Controlled Liberation Serving Corporate Consumption",
        74: "Jürgen Habermas: The Structural Transformation of the Public Sphere",
        75: "Fascism & Nazism: Totalitarian Anti-Enlightenment Reaction",
        76: "Fascist Philosophy: Anti-Rationalism, Vitalism (Bergson/Nietzsche) & Statism",
        77: "Benito Mussolini: 'Everything in the State, nothing outside, nothing against'",
        78: "Nazism: Racial Chauvinism, Social Darwinism & Third Reich Totalitarianism",
        79: "Hannah Arendt: The Origins of Totalitarianism (Terror, Ideology & Atomised Masses)",
        80: "Arendt's Banality of Evil: Adolf Eichmann and Thoughtless Bureaucracy",
        81: "Feminism: Historical Trajectory & Core Conceptual Architecture",
        82: "Sex vs Gender: Biological Fact vs Sociological Construct (Simone de Beauvoir)",
        83: "The Concept of Patriarchy: Institutionalised Male Hegemony over Women",
        84: "The Public-Private Divide: Men in the Agora, Women in the Oikos",
        85: "'The Personal is Political': Carol Hanisch, Kate Millett & Sexual Politics",
        86: "First Wave Feminism: Legal Suffrage & Civil Equality (Wollstonecraft, Mill)",
        87: "Second Wave Feminism: Betty Friedan (The Feminine Mystique) & Workplace Rights",
        88: "Radical Feminism: Shulamith Firestone (Dialectic of Sex & Biological Revolution)",
        89: "Catherine MacKinnon: State Power as Male Power & Pornography as Discrimination",
        90: "Socialist/Marxist Feminism: Domestic Labour Debate & Triple Burden",
        91: "Ecofeminism: Vandana Shiva & Maria Mies (Ecology and Women's Nurturing Role)",
        92: "Post-Modern Feminism: Judith Butler (Gender Trouble & Gender Performativity)",
        93: "Third & Fourth Wave Feminism: Intersectionality (Kimberlé Crenshaw & bell hooks)",
        94: "Post-Colonial Feminism: Chandra Talpade Mohanty ('Under Western Eyes')",
        95: "Theories of the State: Evolution, Sovereignty & Legitimate Coercion",
        96: "Liberal Theory of State: Social Contract and Limited Constitutional Powers",
        97: "Nightwatchman State vs Modern Social Democratic Welfare State",
        98: "Classical Marxist Theory of State: State as Executive Committee of Bourgeoisie",
        99: "V.I. Lenin: State and Revolution & Need for Smashing the Bourgeois State Machinery",
        100: "Relative Autonomy of the State: Karl Marx's Eighteenth Brumaire of Louis Bonaparte",
        101: "The Miliband-Poulantzas Debate on the Capitalist State (1969-1976)",
        102: "Ralph Miliband: Instrumentalism & Class Background of State Elites",
        103: "Nicos Poulantzas: Structuralism & Objective Function of the Capitalist State",
        104: "Pluralist Theory of the State: Robert Dahl & Polyarchy",
        105: "State as Neutral Umpire: Balancing Fragmented Interest Coalitions",
        106: "Post-Colonial State Theory: Hamza Alavi & The Overdeveloped State",
        107: "Bureaucratic-Military Oligarchy Mediating Three Propertied Classes",
        108: "Gunnar Myrdal: The Soft State Hypothesis & Law Enforcement Deficits",
        109: "Pranab Bardhan: The Political Economy of Development in India (Dominant Coalition)",
        110: "Sudipta Kaviraj: Passive Revolution & Epilogue to the Theory of State",
        111: "The Concept of Power: Classical Formulations (Hobbes, Machiavelli)",
        112: "Power as Decision-Making (First Dimension): Robert Dahl's Behavioral Power",
        113: "Power as Non-Decision Making (Second Dimension): Bachrach and Baratz",
        114: "Steven Lukes: Power: A Radical View (The Third Dimension Explained)",
        115: "Preference-Shaping Power: Manipulating Real Interests & Manufactured Consent",
        116: "Zero-Sum vs Non-Zero-Sum Power: Talcott Parsons & Hannah Arendt (Power as Acting in Concert)",
        117: "Max Weber: Concept of Power (Macht) vs Legitimate Authority (Herrschaft)",
        118: "Weber's Tripartite Typology of Authority: Traditional, Charismatic, Legal-Rational",
        119: "Bureaucracy as Ideal Type of Legal-Rational Authority",
        120: "Michel Foucault: The Radical Post-Modern Paradigm of Power",
        121: "Foucault: Power is Capillary, Relational, Ubiquitous, and Micro-Physical",
        122: "Disciplinary Power & The Panopticon: Surveillance, Normalisation & Examination",
        123: "Power/Knowledge Symbiosis: 'There is no power relation without knowledge'",
        124: "Biopower: Power over Life, Demographics, Health & Reproduction",
        125: "Governmentality: The Art of Governing Conduct of Conduct",
        126: "The Concept of Hegemony: Cultural & Intellectual Domination (Gramsci)",
        127: "Gramsci's Hegemonic Apparatus: Schools, Church, Media & Civil Society",
        128: "The Historic Bloc (Blocco Storico): Cohesion between Structure and Superstructure",
        129: "The Concept of Ideology: Etymology & Destutt de Tracy (Science of Ideas)",
        130: "Karl Marx on Ideology: The German Ideology (Camera Obscura & Inverted Reality)",
        131: "Louis Althusser: Ideology and Ideological State Apparatuses (ISAs)",
        132: "Althusser's Concept of Interpellation: Ideology Hails Individuals as Subjects",
        133: "Karl Mannheim: Ideology and Utopia (Total vs Particular Ideology & Relationism)",
        134: "Daniel Bell: The End of Ideology (1960) & Post-Industrial Consensus",
        135: "Francis Fukuyama: The End of History and the Last Man (1992)",
        136: "The Concept of Legitimacy: Voluntary Compliance & Moral Authority",
        137: "David Beetham: The Legitimation of Power (Rules, Justification, Consent)",
        138: "Jürgen Habermas: Legitimation Crisis in Late Capitalist Polities",
        139: "Four Crises in Capitalism: Economic, Rationality, Legitimation, Motivation",
        140: "Theories of Democracy: Etymology (*Demos* + *Kratos*) & Direct Classical Athens",
        141: "Representative Democracy vs Direct Democracy: Rousseau's General Will",
        142: "Classical Elitist Theory: Vilfredo Pareto (The Mind and Society & Governing Elites)",
        143: "Pareto: Circulation of Elites (Residues of Combination vs Group Persistence / Foxes & Lions)",
        144: "Gaetano Mosca: The Ruling Class & Organised Minority Ruling Disorganised Majority",
        145: "Robert Michels: Political Parties & The Iron Law of Oligarchy",
        146: "Joseph Schumpeter: Capitalism, Socialism and Democracy (Competitive Elitism)",
        147: "Schumpeter's Market Model of Democracy: Voters Choose Rulers, Not Policies",
        148: "Pluralist Theory of Democracy: Robert Dahl's Polyarchy (Multiple Minorities Rule)",
        149: "C.B. Macpherson: The Real World of Democracy (Developmental vs Extractive Power)",
        150: "Participatory Democracy: Carole Pateman & Democratic Decentralisation",
        151: "Deliberative Democracy: Jürgen Habermas & Theory of Communicative Action",
        152: "Habermas: The Ideal Speech Situation, Unforced Force of Better Argument",
        153: "Joshua Cohen & Amy Gutmann: Deliberative Democratic Institutions",
        154: "The Concept of Rights: Meaning, Nature & Claim on Society and State",
        155: "Theories of Rights: Natural Rights (John Locke - Life, Liberty, Estate)",
        156: "Utilitarian & Positivist Critique of Natural Rights: Bentham ('Nonsense upon Stilts')",
        157: "Legal Rights Theory: John Austin & Rights as State-Granted Privileges",
        158: "Historical Theory of Rights: Edmund Burke & Rights as Inherited Traditions",
        159: "Social Welfare Theory of Rights: Harold Laski ('A Grammar of Politics')",
        160: "Universal Declaration of Human Rights (UDHR 1948) & International Covenants",
        161: "Karel Vasak: Three Generations of Human Rights (Blue, Red, Green Rights)",
        162: "First Generation: Civil and Political Liberty Rights (Negative Rights)",
        163: "Second Generation: Economic, Social and Cultural Equality Rights (Positive Rights)",
        164: "Third Generation: Collective Solidarity & Environmental Rights (Fraternity)",
        165: "Universalism vs Cultural Relativism: Western Imperialism vs Asian Values Debate",
        166: "The Concept of Justice: Etymology (*Jus*) & The First Virtue of Social Institutions",
        167: "Procedural Justice vs Substantive / Distributive Justice Comparison",
        168: "John Rawls: A Theory of Justice (1971) & Revival of Normative Political Philosophy",
        169: "Rawlsian Rejection of Utilitarianism: 'Justice denies that the loss of freedom for some is made right by a greater good shared by others'",
        170: "The Original Position & The Veil of Ignorance as Thought Experiment",
        171: "Primary Social Goods: Rights, Liberties, Opportunities, Income, Wealth, Self-Respect",
        172: "Rational Choice under Uncertainty: The Maximin Rule of Decision-Making",
        173: "First Principle of Justice: Greatest Equal Basic Liberty Principle",
        174: "Second Principle (Part A): Fair Equality of Opportunity Principle",
        175: "Second Principle (Part B): The Difference Principle (Benefiting the Least Advantaged)",
        176: "Lexical Ordering / Priority of Liberties over Socio-Economic Advantages",
        177: "Reflective Equilibrium: Coherence between Principles and Considered Judgments",
        178: "The Just Savings Principle: Inter-Generational Justice in Rawls",
        179: "Rawlsian Transition: Political Liberalism (1993) & Overlapping Consensus",
        180: "The Law of Peoples (1999): Global Justice & Realistic Utopia",
        181: "Libertarian Critique of Rawls: Robert Nozick's Anarchy, State, and Utopia (1974)",
        182: "Nozick's Entitlement Theory: Principle of Just Acquisition and Transfer",
        183: "The Wilt Chamberlain Example: Liberty Upsets Patterns",
        184: "Nozick: Taxation of Earnings from Labour is on a Par with Forced Labour",
        185: "Communitarian Critique of Rawls: Michael Sandel (Liberalism and the Limits of Justice)",
        186: "Sandel: The Unencumbered Self vs The Situated, Community-Embedded Self",
        187: "Michael Walzer: Spheres of Justice (1983) & Concept of Complex Equality",
        188: "Walzer: Preventing Conversion of Power across Distinct Spheres of Goods",
        189: "Alasdair MacIntyre: After Virtue & The Loss of Moral Teleology in Liberalism",
        190: "Charles Taylor: Atomism and Communitarian Autonomy",
        191: "Marxist Critique of Rawls: Gerald Cohen (If You're an Egalitarian, How Come You're So Rich?)",
        192: "Cohen's Critique of the Difference Principle: Incentives as Talented Blackmail",
        193: "Feminist Critique: Susan Moller Okin (Justice, Gender, and the Family)",
        194: "Amartya Sen: The Idea of Justice (2009) & Critique of Transcendental Institutionalism",
        195: "Sen's Formulation: Niti (Institutional Perfection) vs Nyaya (Realised Justice) & Flute Parable",
        196: "The Concept of Equality: Foundational Equality & Moral Worth of Humans",
        197: "Formal Equality: Equality before Law and Non-Discrimination",
        198: "Equality of Opportunity: Career Open to Talents vs Fair Equality of Opportunity",
        199: "Equality of Outcome: Radical Egalitarianism & Socialist Levelling",
        200: "Ronald Dworkin: Sovereign Virtue & Theory of Equality of Resources",
        201: "Dworkin's Thought Experiment: The Desert Island Shipwreck Auction & Envy Test",
        202: "Dworkin: Option Luck vs Brute Luck & Hypothetical Insurance Market",
        203: "Amartya Sen: 'Equality of What?' & The Capability Approach to Well-Being",
        204: "Functionings vs Capabilities: Substantive Freedom to Lead Life One Has Reason to Value",
        205: "Conversion Factors: Personal, Social, and Environmental Differences in Transforming Goods",
        206: "Martha Nussbaum: Central Human Capabilities List & Constitutional Entitlements",
        207: "Relationship between Liberty and Equality: The Incompatibility Thesis (Acton, Tocqueville, Hayek)",
        208: "The Compatibility Thesis: R.H. Tawney ('Equality') & Harold Laski",
        209: "Affirmative Action Debates: Formal Merit vs Substantive Compensatory Justice",
        210: "Synthesis of Equality Discourses: From Formal Neutrality to Transformative Justice",
        211: "Nature and Scope of Political Theory: Normative vs Empirical Traditions",
        212: "The Debate on the Decline of Political Theory (1950s-1960s)",
        213: "David Easton: 'The Decline of Modern Political Theory' & Hyper-Factualism",
        214: "Alfred Cobban: The Decline of Political Theory into Mere History of Ideas",
        215: "Dante Germino: Beyond Ideology (Loss of Philosophical Openness to Transcendence)",
        216: "The Behavioural Revolution: Scientific Method, Quantification, Value-Free Inquiry",
        217: "The Post-Behavioural Revolution (1969): David Easton's Credo of Relevance and Action",
        218: "The Resurgence of Political Theory: Leo Strauss ('What is Political Philosophy?')",
        219: "Hannah Arendt: The Human Condition (Labor, Work, Action & The Polis)",
        220: "Michael Oakeshott: Rationalism in Politics & Tradition of Conversation",
        221: "Isaiah Berlin: Does Political Theory Still Exist? & Two Concepts of Liberty (1958)",
        222: "Rawlsian Renaissance: 1971 Theory of Justice Restoring Systematic Normative Theory",
        223: "The Cambridge Contextualist School: Quentin Skinner & J.G.A. Pocock (Intentionality & Historical Speech Acts)",
        224: "Grand Epilogue: Comprehensive Synthesis of Western Political Thought Part II"
    }
    
    scans_catalog = []
    for p in range(1, 225):
        scans_catalog.append({
            "page": p,
            "scanFile": f"page_{p:03d}.png",
            "notebookPage": f"Notebook Page {87 + (p // 2)}",
            "title": page_catalog_titles.get(p, f"WPT Part II Page {p}")
        })
        
    full_data = {
        "meta": meta,
        "sections": sections,
        "flashcards": flashcards,
        "answers": answers,
        "scansCatalog": scans_catalog
    }
    
    out_content = f"export const paper1Part4Data = {json.dumps(full_data, indent=2)};\n"
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
    build_paper1_part4()
