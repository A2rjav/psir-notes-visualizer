import os
import json
import re

TRANSCRIPTIONS_DIR = "transcriptions_paper1_part5"

def get_paper1_part5_metadata():
    batches = [
        {
            "batch_file": "batch_1_intro_plato_forms.md",
            "id": "wpt1-intro-plato-forms",
            "number": "01",
            "title": "Introduction to WPT & Plato: Theory of Ideas and Forms",
            "subtitle": "Socrates & Dialectics | Theory of Forms/Ideas | Allegory of the Cave | Reality as Shadow of Ideas | Knowledge as Virtue",
            "scanPages": list(range(1, 13)),
            "notebookPages": "Pages 1 to 10",
            "lecture": "WPT Part I Introductory Sessions",
            "keyScholars": ["Socrates", "Plato", "A.N. Whitehead", "Karl Popper", "Ernest Barker"],
            "coreTheories": ["Entire Western Tradition as Footnotes to Plato (Whitehead)", "Theory of Forms/Ideas: World of Becoming vs World of Being", "Allegory of the Cave & Liberation of Consciousness", "Knowledge is Virtue & Rejection of Sophist Relativism", "The Tripartite Soul (Reason, Courage, Appetite)"]
        },
        {
            "batch_file": "batch_2_plato_philosopher_king_justice.md",
            "id": "wpt1-plato-philosopher-king",
            "number": "02",
            "title": "Plato: The Philosopher King, Communism & Justice",
            "subtitle": "Theory of Justice in Republic | Communism of Property & Wives | Scheme of Education | Karl Popper Critique: Open Society Enemy",
            "scanPages": list(range(13, 25)),
            "notebookPages": "Pages 11 to 20",
            "lecture": "Plato Lectures",
            "keyScholars": ["Plato", "Karl Popper", "Ernest Barker", "Sabine", "Levinson"],
            "coreTheories": ["Architectonic Theory of Justice (Proper Stationing of Classes)", "Rule of Philosopher King: Unchallenged Rule of Reason", "Communism of Property & Family: Freeing Guardians from Private Interest", "State-Sponsored Rigid Curriculum of Higher Dialectics", "Popper's Indictment: Plato as Father of Totalitarianism"]
        },
        {
            "batch_file": "batch_3_aristotle_state_citizenship_slavery.md",
            "id": "wpt1-aristotle-state-citizenship",
            "number": "03",
            "title": "Aristotle: Father of Political Science, State & Citizenship",
            "subtitle": "Critique of Plato | State as Natural & Prior to Man | Theory of Citizenship | Defense of Slavery & Property",
            "scanPages": list(range(25, 37)),
            "notebookPages": "Pages 21 to 28",
            "lecture": "Aristotle Lecture Series",
            "keyScholars": ["Aristotle", "Plato", "Ernest Barker", "W.D. Ross", "Hannah Arendt"],
            "coreTheories": ["Aristotle's Teleological Realism & Common Sense", "State Originating for Bare Life, Continuing for Good Life", "Man is by Nature a Political Animal (Zoon Politikon)", "Deliberative & Judicial Definition of Citizenship", "Functional & Natural Justification of Slavery and Private Property"]
        },
        {
            "batch_file": "batch_4_aristotle_revolution_polity.md",
            "id": "wpt1-aristotle-revolution-polity",
            "number": "04",
            "title": "Aristotle: Theory of Justice, Revolution & The Best Practicable State",
            "subtitle": "Distributive vs Rectificatory Justice | Causes & Cures of Revolutions | Classification of Constitutions | Rule of Law & Polity",
            "scanPages": list(range(37, 49)),
            "notebookPages": "Pages 29 to 35",
            "lecture": "Aristotle & Transition to Machiavelli",
            "keyScholars": ["Aristotle", "Polybius", "Cicero", "Machiavelli"],
            "coreTheories": ["Distributive Justice: Proportionate Equality to Merit", "Psychological & Material Causes of Stasis (Revolution)", "Six-fold Classification of Constitutions (Rule by One, Few, Many)", "Polity: Golden Mean & Rule by the Middle Class", "Rule of Law as Reason Free from Passion"]
        },
        {
            "batch_file": "batch_5_machiavelli_prince_statecraft.md",
            "id": "wpt1-machiavelli-renaissance-prince",
            "number": "05",
            "title": "Niccolò Machiavelli: The Prince, Statecraft & Political Realism",
            "subtitle": "Child of Renaissance | Secularisation of Politics | Human Nature (Ungrateful, Fickle, Greedy) | Lion & Fox | Virtù vs Fortuna",
            "scanPages": list(range(49, 61)),
            "notebookPages": "Pages 36 to 42",
            "lecture": "Machiavelli Lectures",
            "keyScholars": ["Niccolò Machiavelli", "Benedetto Croce", "Leo Strauss", "Quentin Skinner", "Gramsci"],
            "coreTheories": ["Autonomy of Politics: Separation of Politics from Christian Morality", "Double Standard of Morality (Ruler vs Citizen)", "Pessimistic Theory of Human Nature (Men forget father's death before loss of patrimony)", "Statecraft: Combination of Cunning of Fox & Bravery of Lion", "Virtù Overcoming Fortuna (Fortune as Woman)"]
        },
        {
            "batch_file": "batch_6_hobbes_leviathan_sovereignty.md",
            "id": "wpt1-hobbes-leviathan-sovereignty",
            "number": "06",
            "title": "Thomas Hobbes: Scientific Materialism, State of Nature & Leviathan",
            "subtitle": "Resolutive-Compositive Method | Mechanical View of Man | State of Nature (Nasty, Brutish, Short) | Social Contract | Absolute Sovereign",
            "scanPages": list(range(61, 73)),
            "notebookPages": "Pages 43 to 48",
            "lecture": "Thomas Hobbes Lectures",
            "keyScholars": ["Thomas Hobbes", "C.B. Macpherson", "Michael Oakeshott", "Leo Strauss"],
            "coreTheories": ["Scientific Materialism: Motion of Matter & Human Psychology", "State of Nature: Perpetual War of All against All (Bellum Omnium)", "Fear of Violent Death as Primary Rational Passion", "Social Contract: Covenants without Swords are but Words", "Absolute, Indivisible, Inalienable Leviathan Sovereignty"]
        },
        {
            "batch_file": "batch_7_hobbes_individualism_locke_intro.md",
            "id": "wpt1-hobbes-individualism-locke-intro",
            "number": "07",
            "title": "Hobbes' Individualism & John Locke's Two Treatises",
            "subtitle": "Hobbes as Greatest Individualist (Oakeshott) | Right to Self-Preservation | Locke Two Treatises | Rejection of Filmer's Patriarcha",
            "scanPages": list(range(73, 85)),
            "notebookPages": "Pages 49 to 54",
            "lecture": "Hobbes Conclusion & Locke Lectures",
            "keyScholars": ["Thomas Hobbes", "John Locke", "Sir Robert Filmer", "C.B. Macpherson", "Peter Laslett"],
            "coreTheories": ["Paradox of Hobbes: Leviathan Built upon Extreme Individualism", "Absolute Obligation Conditioned by Right to Life", "Locke's First Treatise: Demolition of Divine Right of Kings (Filmer)", "Locke's Rational Humanitarian Anthropology", "State of Nature as State of Peace, Goodwill, Mutual Assistance"]
        },
        {
            "batch_file": "batch_8_locke_natural_rights_limited_government.md",
            "id": "wpt1-locke-rights-limited-government",
            "number": "08",
            "title": "John Locke: Natural Rights, Social Contract & Limited Government",
            "subtitle": "Natural Rights: Life, Liberty & Estate | Labour Theory of Property & Provisos | Two Contracts | Constitutionalism & Right to Revolt",
            "scanPages": list(range(85, 97)),
            "notebookPages": "Pages 55 to 60",
            "lecture": "Locke Lectures",
            "keyScholars": ["John Locke", "Jeremy Waldron", "C.B. Macpherson", "Robert Nozick"],
            "coreTheories": ["Natural Rights as Inalienable Property (Life, Liberty, Estate)", "Labour Theory of Property: Mixing Labour with Nature", "Lockean Provisos: As Much and As Good, Non-Spoilage", "Two Contracts: Creation of Civil Society & Fiduciary Government Trust", "Right to Revolution: Appeal to Heaven against Tyranny"]
        },
        {
            "batch_file": "batch_9_rousseau_general_will_democracy.md",
            "id": "wpt1-rousseau-general-will",
            "number": "09",
            "title": "Jean-Jacques Rousseau: Inequality, General Will & Direct Democracy",
            "subtitle": "Noble Savage | Discourse on Inequality | Man Born Free but Everywhere in Chains | Actual Will vs Real Will | Forced to be Free",
            "scanPages": list(range(97, 109)),
            "notebookPages": "Pages 61 to 68",
            "lecture": "Rousseau Lectures",
            "keyScholars": ["Jean-Jacques Rousseau", "Jacob Talmon", "Isaiah Berlin", "Ernest Cassirer"],
            "coreTheories": ["Noble Savage: Pure Sentiment, Amour de Soi vs Amour Propre", "Private Property as Root of Civilization & Moral Corruption", "Social Contract: 'Man is born free and everywhere he is in chains'", "The General Will: Synthesis of Real Wills Oriented to Common Good", "Paradox of Liberty: Citizens 'Forced to be Free' (Talmon Totalitarian Critique)"]
        },
        {
            "batch_file": "batch_10_mill_liberty_representative_government.md",
            "id": "wpt1-mill-liberty-women",
            "number": "10",
            "title": "J.S. Mill: Liberty, Freedom of Speech & Subjection of Women",
            "subtitle": "Revision of Bentham Utilitarianism | On Liberty & Harm Principle | Self-Regarding vs Other-Regarding | Tyranny of Majority | Plural Voting",
            "scanPages": list(range(109, 121)),
            "notebookPages": "Pages 69 to 76",
            "lecture": "J.S. Mill Lectures",
            "keyScholars": ["J.S. Mill", "Jeremy Bentham", "Harriet Taylor", "Isaiah Berlin", "C.L. Wayper"],
            "coreTheories": ["Mill as 'Reluctant Democrat' (Wayper)", "Revision of Utilitarianism: Socrates Dissatisfied vs Pig Satisfied", "Absolute Freedom of Speech and Expression (Even if all mankind minus one...)", "Harm Principle: Preventing Harm to Others as Sole Ground of Coercion", "Subjection of Women: Pioneer of Feminist Gender Equality"]
        },
        {
            "batch_file": "batch_11_marx_alienation_historical_materialism.md",
            "id": "wpt1-marx-alienation-materialism",
            "number": "11",
            "title": "Karl Marx: Theory of Alienation & Historical Materialism",
            "subtitle": "Young Hegelian Phase | Alienation in 1844 Manuscripts | Historical Materialism (Base & Superstructure) | Forces vs Relations of Production",
            "scanPages": list(range(121, 133)),
            "notebookPages": "Pages 77 to 84",
            "lecture": "Marxist Philosophy Lectures",
            "keyScholars": ["Karl Marx", "Friedrich Engels", "G.W.F. Hegel", "Ludwig Feuerbach", "Louis Althusser"],
            "coreTheories": ["Feuerbach's Materialist Reversal of Hegel's Idealism", "Human Species-Essence (Gattungswesen) & Unalienated Labour", "Four Dimensions of Estranged Labour under Capitalism", "Historical Materialism: Material Conditions Determining Consciousness", "Dialectic of Productive Forces and Outmoded Production Relations"]
        },
        {
            "batch_file": "batch_12_marx_class_struggle_communist_society.md",
            "id": "wpt1-marx-class-struggle-revolution",
            "number": "12",
            "title": "Karl Marx: Class Struggle, Surplus Value & Communist Utopia",
            "subtitle": "The Communist Manifesto | Class-in-itself vs Class-for-itself | Labour Theory of Value & Surplus Value | Revolution & Stateless Communism",
            "scanPages": list(range(133, 145)),
            "notebookPages": "Pages 85 to 92",
            "lecture": "Capital & Communist Manifesto Lectures",
            "keyScholars": ["Karl Marx", "Friedrich Engels", "V.I. Lenin", "David Harvey", "Eric Hobsbawm"],
            "coreTheories": ["Class Polarization: Bourgeoisie vs Proletariat", "Transformation: Class-in-itself to Class-for-itself Consciousness", "Extraction of Surplus Value & Falling Rate of Profit Crisis", "Inevitable Collapse of Capitalism through Inherent Contradictions", "Two Stages of Post-Revolutionary Society: Socialism to Communism"]
        },
        {
            "batch_file": "batch_13_gramsci_hegemony_civil_society.md",
            "id": "wpt1-gramsci-hegemony-intellectuals",
            "number": "13",
            "title": "Antonio Gramsci: Hegemony, Civil Society & Revolutionary Strategy",
            "subtitle": "Critique of Crude Economism | The Prison Notebooks | Dual Hegemony: Civil Society vs Political Society | War of Position vs Movement",
            "scanPages": list(range(145, 157)),
            "notebookPages": "Pages 93 to 100",
            "lecture": "Antonio Gramsci Lectures",
            "keyScholars": ["Antonio Gramsci", "Niccolò Machiavelli", "Perry Anderson", "Norberto Bobbio"],
            "coreTheories": ["Gramsci as Theorist of Superstructure", "Hegemony: Ethical, Cultural, and Ideological Consent", "Organic Intellectuals as Functionaries of Hegemony", "Historic Bloc (Inseparable Unity of Material Forces and Ideology)", "War of Position: Cultural Trench Warfare Preceding Political Takeover"]
        },
        {
            "batch_file": "batch_14_arendt_human_condition_action.md",
            "id": "wpt1-arendt-human-condition-action",
            "number": "14",
            "title": "Hannah Arendt: The Human Condition & Theory of Action",
            "subtitle": "Phenomenological Method | Vita Activa vs Vita Contemplativa | Labor, Work, Action | The Public Realm & The Polis | Power as Acting in Concert",
            "scanPages": list(range(157, 169)),
            "notebookPages": "Pages 101 to 108",
            "lecture": "Hannah Arendt Lectures",
            "keyScholars": ["Hannah Arendt", "Aristotle", "Martin Heidegger", "Jürgen Habermas"],
            "coreTheories": ["Critique of Traditional Metaphysics: Recovery of the Political", "Vita Activa: Labor (Biological), Work (Artificial), Action (Freedom)", "Action as Highest Realm: Speech, Deed, Natality, Plurality", "Public Sphere as Space of Appearance and Intersubjective Disclosure", "Power as Non-Coercive Capacity of People Acting in Concert"]
        },
        {
            "batch_file": "batch_15_arendt_totalitarianism_wpt1_synthesis.md",
            "id": "wpt1-arendt-totalitarianism-synthesis",
            "number": "15",
            "title": "Hannah Arendt: Totalitarianism, Banality of Evil & Volume 1 Synthesis",
            "subtitle": "The Origins of Totalitarianism | Terror & Ideology | Eichmann in Jerusalem & Banality of Evil | Grand Epilogue: Master WPT Part 1 Synthesis",
            "scanPages": list(range(169, 181)),
            "notebookPages": "Pages 109 to 116",
            "lecture": "Arendt Conclusion & Master WPT 1 Synthesis",
            "keyScholars": ["Hannah Arendt", "Karl Jaspers", "Seyla Benhabib", "Margaret Canovan"],
            "coreTheories": ["Totalitarianism as Novel Form of Tyranny (Total Domination of Psyche)", "The Loneliness and Atomisation of Modern Mass Man", "Banality of Evil: Thoughtlessness and Bureaucratic Normalisation", "Responsibility vs Collective Guilt", "Grand Comparative Matrix of Western Political Philosophy (Plato to Arendt)"]
        }
    ]
    return batches

if __name__ == "__main__":
    b = get_paper1_part5_metadata()
    print(f"Loaded {len(b)} batch metadata definitions for Paper 1 Part 5.")
