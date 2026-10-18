import os
import json
import re

TRANSCRIPTIONS_DIR = "transcriptions_paper1_part4"

def get_paper1_part4_metadata():
    batches = [
        {
            "batch_file": "batch_1_idealism_classical_liberalism.md",
            "id": "wpt2-idealism-classical-liberalism",
            "number": "01",
            "title": "Political Ideologies: Idealism & Classical Liberalism",
            "subtitle": "Socrates, Plato & Hegel | Kantian vs British Idealists | Atomistic Individualism | Possessive Individualism | Nightwatchman State",
            "scanPages": list(range(1, 16)),
            "notebookPages": "Pages 88 to 92",
            "lecture": "WPT Part II Introductory Sessions",
            "keyScholars": ["Socrates", "Plato", "G.W.F. Hegel", "Immanuel Kant", "T.H. Green", "John Locke", "Adam Smith", "Jeremy Bentham", "C.B. Macpherson"],
            "coreTheories": ["Idealist Primacy of State & Organic Society", "German vs Kantian vs Oxford Idealism", "Classical Liberal Negative Liberty", "Possessive Individualism", "Market Mechanism as Invisible Hand"]
        },
        {
            "batch_file": "batch_2_modern_neoliberalism_social_liberalism.md",
            "id": "wpt2-modern-neoliberalism-social-liberalism",
            "number": "02",
            "title": "Modern Liberalism, Neo-Liberalism & Social Liberalism",
            "subtitle": "J.S. Mill Individuality | T.H. Green Positive Liberty | Laski Welfare State | Hayek & Nozick Libertarianism | Rawls & Sen",
            "scanPages": list(range(16, 31)),
            "notebookPages": "Pages 93 to 99",
            "lecture": "Liberalism Lecture Series",
            "keyScholars": ["J.S. Mill", "T.H. Green", "Harold Laski", "John Maynard Keynes", "Friedrich Hayek", "Robert Nozick", "Milton Friedman", "John Rawls"],
            "coreTheories": ["Harm Principle & Developmental Individuality", "Positive Freedom & State Removing Hindrances", "Keynesian Demand Management & Welfare State", "Spontaneous Market Order (Catallaxy)", "Entitlement Theory & Self-Ownership"]
        },
        {
            "batch_file": "batch_3_multiculturalism_kymlicka_parekh.md",
            "id": "wpt2-multiculturalism",
            "number": "03",
            "title": "Multiculturalism & The Politics of Recognition",
            "subtitle": "Will Kymlicka Differentiated Rights | Bhikhu Parekh Cultural Embeddedness | Charles Taylor Recognition | Okin Feminist Critique",
            "scanPages": list(range(31, 46)),
            "notebookPages": "Pages 100 to 104",
            "lecture": "Multiculturalism Sessions",
            "keyScholars": ["Will Kymlicka", "Bhikhu Parekh", "Charles Taylor", "Iris Marion Young", "Susan Moller Okin", "Brian Barry"],
            "coreTheories": ["Mosaic/Salad Bowl vs Melting Pot Assimilation", "Group-Differentiated Rights (Self-Government, Polyethnic, Representation)", "Human Beings as Culturally Embedded (Parekh)", "Politics of Recognition & Human Dignity", "Feminist Paradox: Minority Rights vs Women's Rights"]
        },
        {
            "batch_file": "batch_4_socialism_classical_marxism.md",
            "id": "wpt2-socialism-classical-marxism",
            "number": "04",
            "title": "Socialism & Classical Scientific Marxism",
            "subtitle": "Utopian Socialists | Fabianism & Inevitability of Gradualness | Historical Materialism | Surplus Value | Theory of Alienation",
            "scanPages": list(range(46, 61)),
            "notebookPages": "Pages 105 to 111",
            "lecture": "Socialism & Marxism Series",
            "keyScholars": ["Robert Owen", "Charles Fourier", "Sidney & Beatrice Webb", "G.B. Shaw", "Karl Marx", "Friedrich Engels", "V.I. Lenin"],
            "coreTheories": ["Utopian vs Scientific Socialism", "Fabian Evolutionism & Inevitability of Gradualness", "Dialectical & Historical Materialism (Base-Superstructure)", "Surplus Value & Capitalist Exploitation", "Four Forms of Alienation (1844 Manuscripts)"]
        },
        {
            "batch_file": "batch_5_neomarxism_frankfurt_fascism.md",
            "id": "wpt2-neomarxism-frankfurt-fascism",
            "number": "05",
            "title": "Neo-Marxism, Frankfurt School Critical Theory & Fascism",
            "subtitle": "Gramsci Hegemony | Lukacs Reification | Adorno & Horkheimer Culture Industry | Marcuse One-Dimensional Man | Arendt Totalitarianism",
            "scanPages": list(range(61, 76)),
            "notebookPages": "Pages 112 to 115",
            "lecture": "Critical Theory & Fascism Series",
            "keyScholars": ["György Lukács", "Antonio Gramsci", "Theodor Adorno", "Max Horkheimer", "Herbert Marcuse", "Jürgen Habermas", "Hannah Arendt", "Benito Mussolini"],
            "coreTheories": ["Western Marxism Cultural Turn", "Reification & False Consciousness", "Culture Industry & Mass Deception", "One-Dimensional Man & Consumer Sublimation", "Totalitarianism & Banality of Evil (Arendt)"]
        },
        {
            "batch_file": "batch_6_feminism_schools_waves.md",
            "id": "wpt2-feminism-schools-waves",
            "number": "06",
            "title": "Feminism: Waves, Schools of Thought & Gender Politics",
            "subtitle": "Sex vs Gender | Personal is Political | Liberal, Radical, Socialist & Ecofeminism | Judith Butler Performativity | Intersectionality",
            "scanPages": list(range(76, 91)),
            "notebookPages": "Pages 116 to 121",
            "lecture": "Feminism Lectures",
            "keyScholars": ["Simone de Beauvoir", "Mary Wollstonecraft", "Betty Friedan", "Kate Millett", "Shulamith Firestone", "Catherine MacKinnon", "Judith Butler", "Kimberlé Crenshaw", "Vandana Shiva"],
            "coreTheories": ["Social Construction of Gender ('One is not born a woman')", "Public-Private Dichotomy & 'Personal is Political'", "Patriarchy as Universal System of Domination", "Radical Dialectic of Sex & Reproductive Biology", "Intersectionality of Gender, Race, and Class"]
        },
        {
            "batch_file": "batch_7_theories_of_state.md",
            "id": "wpt2-theories-of-state",
            "number": "07",
            "title": "Theories of the State: Liberal, Marxist, Pluralist & Post-Colonial",
            "subtitle": "Instrumental vs Structural Marxism | Miliband-Poulantzas Debate | Robert Dahl Polyarchy | Hamza Alavi Overdeveloped State",
            "scanPages": list(range(91, 106)),
            "notebookPages": "Pages 122 to 134",
            "lecture": "State Theory Sessions",
            "keyScholars": ["Thomas Hobbes", "John Locke", "Karl Marx", "Ralph Miliband", "Nicos Poulantzas", "Robert Dahl", "Hamza Alavi", "Gunnar Myrdal"],
            "coreTheories": ["Social Contract & State as Neutral Arbiter", "State as Executive Committee of Ruling Class", "Instrumentalism vs Structuralism (Miliband vs Poulantzas)", "Relative Autonomy of the Capitalist State", "Post-Colonial Overdeveloped State & Bureaucratic-Military Oligarchy"]
        },
        {
            "batch_file": "batch_8_concept_of_power_lukes_foucault.md",
            "id": "wpt2-concept-of-power",
            "number": "08",
            "title": "The Concept of Power: Steven Lukes & Michel Foucault",
            "subtitle": "Three Dimensions of Power (Lukes) | Max Weber Authority Typology | Foucault Power/Knowledge, Biopower & Governmentality",
            "scanPages": list(range(106, 121)),
            "notebookPages": "Pages 135 to 140",
            "lecture": "Power & Authority Lectures",
            "keyScholars": ["Steven Lukes", "Robert Dahl", "Peter Bachrach & Morton Baratz", "Max Weber", "Michel Foucault", "Hannah Arendt"],
            "coreTheories": ["Lukes Three Faces of Power (Decision, Agenda, Preference Shaping)", "Weber Tripartite Authority (Traditional, Charismatic, Legal-Rational)", "Foucault Capillary Power & Disciplinary Society", "Power/Knowledge Symbiosis", "Biopower & Regulation of Populations"]
        },
        {
            "batch_file": "batch_9_hegemony_ideology_legitimacy.md",
            "id": "wpt2-hegemony-ideology-legitimacy",
            "number": "09",
            "title": "Hegemony, Ideology & Legitimation Crisis",
            "subtitle": "Gramsci Manufacturing Consent | Althusser Ideological State Apparatuses | Mannheim Ideology & Utopia | Habermas Crisis",
            "scanPages": list(range(121, 136)),
            "notebookPages": "Pages 141 to 148",
            "lecture": "Ideology & Hegemony Lectures",
            "keyScholars": ["Antonio Gramsci", "Louis Althusser", "Karl Mannheim", "David Beetham", "Jürgen Habermas", "Francis Fukuyama"],
            "coreTheories": ["Hegemony: Consent Armoured by Coercion", "Repressive vs Ideological State Apparatuses (RSAs vs ISAs)", "Total vs Particular Conception of Ideology", "Legitimation Crisis in Late Capitalism", "End of History & Ideology Debates"]
        },
        {
            "batch_file": "batch_10_theories_of_democracy.md",
            "id": "wpt2-theories-of-democracy",
            "number": "10",
            "title": "Theories of Democracy: Elitist, Pluralist, Participatory & Deliberative",
            "subtitle": "Pareto & Mosca Classical Elitism | Schumpeter Procedural Democracy | Macpherson Developmental Democracy | Habermas Deliberation",
            "scanPages": list(range(136, 151)),
            "notebookPages": "Pages 149 to 159",
            "lecture": "Democracy Theory Series",
            "keyScholars": ["Vilfredo Pareto", "Gaetano Mosca", "Robert Michels", "Joseph Schumpeter", "Robert Dahl", "C.B. Macpherson", "Jürgen Habermas", "Carole Pateman"],
            "coreTheories": ["Circulation of Elites (Lions and Foxes)", "Iron Law of Oligarchy in Political Parties", "Competitive Elitism & Market Model of Democracy", "Macpherson Critique of Possessive Individualist Democracy", "Communicative Rationality & Ideal Speech Situation"]
        },
        {
            "batch_file": "batch_11_concept_of_rights_human_rights.md",
            "id": "wpt2-concept-of-rights",
            "number": "11",
            "title": "The Concept of Rights & Three Generations of Human Rights",
            "subtitle": "Natural, Legal, Historical & Welfare Rights | Bentham 'Nonsense upon Stilts' | Karel Vasak Three Generations | Universalism vs Relativism",
            "scanPages": list(range(151, 166)),
            "notebookPages": "Pages 160 to 164",
            "lecture": "Rights & Human Rights Sessions",
            "keyScholars": ["John Locke", "Jeremy Bentham", "Edmund Burke", "Harold Laski", "Karel Vasak", "Jack Donnelly", "Amartya Sen"],
            "coreTheories": ["Natural Rights as Moral Trumps (Locke)", "Legal Positivist Critique of Natural Rights (Bentham)", "Social Welfare Basis of Functional Rights (Laski)", "Three Generations of Human Rights (Blue, Red, Green)", "Asian Values vs Universal Human Rights Debate"]
        },
        {
            "batch_file": "batch_12_rawls_theory_of_justice.md",
            "id": "wpt2-rawls-theory-of-justice",
            "number": "12",
            "title": "The Concept of Justice: John Rawls' A Theory of Justice",
            "subtitle": "Original Position & Veil of Ignorance | Rejection of Utilitarianism | Lexical Priority | Difference Principle | Reflective Equilibrium",
            "scanPages": list(range(166, 181)),
            "notebookPages": "Pages 165 to 170",
            "lecture": "Rawlsian Justice Lectures",
            "keyScholars": ["John Rawls", "Immanuel Kant", "Brian Barry", "Thomas Pogge", "Norman Daniels"],
            "coreTheories": ["Justice as Fairness (Pure Procedural Justice)", "Veil of Ignorance & Original Position", "Maximin Strategy of Rational Choice", "Equal Basic Liberties & Fair Equality of Opportunity", "The Difference Principle: Benefiting the Least Advantaged"]
        },
        {
            "batch_file": "batch_13_justice_critiques_nozick_sen_communitarians.md",
            "id": "wpt2-justice-critiques-nozick-sen",
            "number": "13",
            "title": "Critiques of Rawls: Nozick, Amartya Sen & Communitarianism",
            "subtitle": "Robert Nozick Entitlement Theory | Michael Sandel Unencumbered Self | Walzer Spheres of Justice | Sen Niti vs Nyaya",
            "scanPages": list(range(181, 196)),
            "notebookPages": "Pages 171 to 180",
            "lecture": "Debates on Justice Series",
            "keyScholars": ["Robert Nozick", "Michael Sandel", "Michael Walzer", "Alasdair MacIntyre", "Amartya Sen", "Gerald Cohen", "Susan Moller Okin"],
            "coreTheories": ["Libertarian Historical Entitlement Theory (Nozick)", "Communitarian Critique of Unencumbered Self (Sandel)", "Complex Equality & Autonomous Spheres of Justice (Walzer)", "Transcendental Institutionalism vs Realization-Focused Comparison (Sen)", "Niti vs Nyaya in Indian Jurisprudence"]
        },
        {
            "batch_file": "batch_14_concept_of_equality_dworkin_sen.md",
            "id": "wpt2-concept-of-equality",
            "number": "14",
            "title": "The Concept of Equality: Resources, Capabilities & Opportunity",
            "subtitle": "Dworkin Equality of Resources (Envy Test, Option vs Brute Luck) | Sen Capability Approach | Liberty vs Equality Debate | Affirmative Action",
            "scanPages": list(range(196, 211)),
            "notebookPages": "Pages 181 to 195",
            "lecture": "Equality & Affirmative Action Series",
            "keyScholars": ["Ronald Dworkin", "Amartya Sen", "R.H. Tawney", "Harold Laski", "Friedrich Hayek", "Bernard Williams"],
            "coreTheories": ["Formal Equality vs Fair Equality of Opportunity", "Equality of Resources: Shipwreck Auction & Envy Test (Dworkin)", "Brute Luck vs Option Luck Distinction", "Sen Capability Metric (Functionings & Well-Being Freedom)", "Compatibility of Liberty and Equality (Tawney & Laski)"]
        },
        {
            "batch_file": "batch_15_decline_resurgence_political_theory_synthesis.md",
            "id": "wpt2-political-theory-methodology-synthesis",
            "number": "15",
            "title": "Methodological Debates: Decline & Resurgence of Political Theory",
            "subtitle": "David Easton Behavioural Revolution | Positivism & Hyper-Factualism | Strauss, Arendt & Rawls Resurgence | Skinner Cambridge School",
            "scanPages": list(range(211, 225)),
            "notebookPages": "Pages 196 to 205",
            "lecture": "WPT Part II Master Synthesis & Concluding Lectures",
            "keyScholars": ["David Easton", "Alfred Cobban", "Dante Germino", "Leo Strauss", "Hannah Arendt", "Quentin Skinner", "J.G.A. Pocock", "John Rawls"],
            "coreTheories": ["Decline of Political Theory Thesis (Easton & Cobban)", "Behaviouralism & Scientific Positivist Turn", "Post-Behavioural Credo of Relevance & Action", "Resurgence of Normative Political Philosophy", "Contextualist Historiography: Intentionality & Illocutionary Force"]
        }
    ]
    return batches

if __name__ == "__main__":
    b = get_paper1_part4_metadata()
    print(f"Loaded {len(b)} batch metadata definitions for Paper 1 Part 4.")
