import os
import json
import re

TRANSCRIPTIONS_DIR = "transcriptions_part2"

def get_part2_metadata():
    batches = [
        {
            "batch_file": "batch_1_comparative_politics_systems_structural.md",
            "id": "p2a-comparative-politics-systems",
            "number": "01",
            "title": "Comparative Politics: Evolution, Systems & Structural-Functional Approaches",
            "subtitle": "Aristotle to Modern Era | Traditional vs Modern Comparative Politics | David Easton's Systems Model | Gabriel Almond's Structural-Functionalism",
            "scanPages": list(range(1, 13)),
            "notebookPages": "Pages 1 to 6",
            "lecture": "Comparative Politics Master Series (Lecture 31/03/2017)",
            "keyScholars": ["Aristotle", "David Easton", "Gabriel Almond", "G. Bingham Powell", "Jean Blondel"],
            "coreTheories": ["Aristotle as Father of Comparative Politics (Study of 158 Constitutions)", "Traditional Comparative Politics: Eurocentric, Descriptive, Legalistic, Parochial", "David Easton's Systems Approach: Demands, Supports, Black Box Conversion, Feedback Loop", "Gabriel Almond's Structural-Functional Approach: Input Functions vs Output Functions", "Political Development and Institutional Differentiation"]
        },
        {
            "batch_file": "batch_2_comparative_sociology_economy_culture.md",
            "id": "p2a-sociology-economy-culture",
            "number": "02",
            "title": "Approaches to Comparative Politics: Sociology, Economy & Political Culture",
            "subtitle": "Political Sociology (Lipset & Rokkan) | Political Economy (Modern & Dependency) | Political Culture (Almond & Verba: Civic Culture)",
            "scanPages": list(range(13, 25)),
            "notebookPages": "Pages 7 to 12",
            "lecture": "Approaches to Comparative Politics Series",
            "keyScholars": ["Gabriel Almond", "Sidney Verba", "Seymour Martin Lipset", "Stein Rokkan", "Lucian Pye"],
            "coreTheories": ["Political Sociology: Social Cleavages, Class Stratification, and Political Power", "Political Economy Approach: Interaction between State Authority and Market Dynamics", "Almond and Verba's Civic Culture Typology: Parochial, Subject, and Participant Cultures", "Congruence Theory: Alignment between Political Culture and Constitutional Structure", "Lucian Pye's Political Development Syndrome: Equality, Capacity, and Differentiation"]
        },
        {
            "batch_file": "batch_3_nature_of_state_advanced_developing.md",
            "id": "p2a-nature-of-state",
            "number": "03",
            "title": "Nature of the State in Advanced Industrial & Developing Societies",
            "subtitle": "The Welfare State & Post-Industrial Society | Corporatism & Pluralism | Post-Colonial State (Hamza Alavi: Overdeveloped State) | Failed & Fragile States",
            "scanPages": list(range(25, 36)),
            "notebookPages": "Pages 13 to 15",
            "lecture": "State in Comparative Perspective Series",
            "keyScholars": ["Hamza Alavi", "Gunnar Myrdal", "Claus Offe", "Philippe Schmitter", "Joel Migdal"],
            "coreTheories": ["Welfare State in Advanced Capitalism: Legitimation Crisis vs Capital Accumulation (Claus Offe)", "Corporatism: State-Mediated Tripartite Bargaining between Capital, Labour, and State", "Hamza Alavi's Post-Colonial State: The Overdeveloped Bureaucratic-Military Oligarchy", "Gunnar Myrdal's Soft State: Institutional Indiscipline and Pervasive Corruption", "Joel Migdal's State in Society: Strong Societies and Weak States"]
        },
        {
            "batch_file": "batch_4_representation_participation_parties_pressure_groups.md",
            "id": "p2a-parties-pressure-groups",
            "number": "04",
            "title": "Politics of Representation & Participation: Parties & Pressure Groups",
            "subtitle": "Duverger's Law | Sartori's Party Typology | Catch-All Parties (Kirchheimer) | Pressure Groups (Interest Articulation) | Iron Triangles",
            "scanPages": list(range(36, 46)),
            "notebookPages": "Pages 16 to 20",
            "lecture": "Representation & Participation Series",
            "keyScholars": ["Maurice Duverger", "Giovanni Sartori", "Otto Kirchheimer", "Robert Michels", "Mancur Olson"],
            "coreTheories": ["Maurice Duverger's Law: First-Past-The-Post Producing Two-Party Systems; PR Producing Multiparty Systems", "Giovanni Sartori's Typology: Moderate vs Polarized Pluralism", "Otto Kirchheimer's Catch-All Party: Ideological Dilution and Electoral Pragmatism", "Pressure Groups vs Political Parties: Interest Articulation vs Interest Aggregation", "Mancur Olson's Logic of Collective Action: Free Rider Problem and Selective Incentives"]
        },
        {
            "batch_file": "batch_5_globalisation_transnational_governance.md",
            "id": "p2a-globalisation-sovereignty",
            "number": "05",
            "title": "Globalisation, State Sovereignty & Transnational Civil Society",
            "subtitle": "Hyper-Globalists vs Skeptics vs Transformationalists (Held) | Erosion vs Resilience of Westphalian State | Global Civil Society & INGOs",
            "scanPages": list(range(46, 57)),
            "notebookPages": "Pages 21 to 24",
            "lecture": "Globalisation & Comparative Perspectives",
            "keyScholars": ["David Held", "Kenichi Ohmae", "Paul Hirst", "Grahame Thompson", "Susan Strange"],
            "coreTheories": ["The Three Schools of Globalisation (David Held): Hyper-globalists, Skeptics, and Transformationalists", "Kenichi Ohmae's Borderless World: The Eclipse of the Nation-State by Market Forces", "Susan Strange's The Retreat of the State: Diffusion of Sovereign Authority to Non-State Actors", "Hirst and Thompson's Skeptical Counter-Thesis: Internationalization not Globalisation; State Resilience", "Transformationalist Synthesis: Re-articulation, Re-regulation, and Adaptation of State Sovereignty"]
        },
        {
            "batch_file": "batch_6_intro_international_relations_classical_realism.md",
            "id": "p2a-intro-ir-classical-realism",
            "number": "06",
            "title": "International Relations & Classical Realism: Hans Morgenthau",
            "subtitle": "Nature & Scope of IR | Anarchy & Self-Help | Hans Morgenthau's Six Principles of Political Realism | National Interest Defined as Power",
            "scanPages": list(range(57, 69)),
            "notebookPages": "Pages 25 to 30",
            "lecture": "International Relations Theory Master Series",
            "keyScholars": ["Hans Morgenthau", "Thucydides", "Niccolò Machiavelli", "Thomas Hobbes", "E.H. Carr"],
            "coreTheories": ["E.H. Carr's The Twenty Years' Crisis (1939): Utopianism vs Realism", "Hans Morgenthau's Politics Among Nations (1948): Foundational Bible of Realism", "Six Principles of Political Realism: Objective Laws Rooted in Human Nature", "National Interest Defined in Terms of Power (Interest is Eternal, Power is Contextual)", "Autonomy of the Political Sphere: Separation of International Politics from Private Moralism"]
        },
        {
            "batch_file": "batch_7_structural_realism_offensive_defensive.md",
            "id": "p2a-structural-realism-offensive-defensive",
            "number": "07",
            "title": "Structural Realism (Neo-Realism): Waltz & Mearsheimer",
            "subtitle": "Kenneth Waltz: Theory of International Politics | Systemic Anarchy & Polarities | Defensive Realism vs Offensive Realism (Mearsheimer)",
            "scanPages": list(range(69, 80)),
            "notebookPages": "Pages 31 to 40",
            "lecture": "Neo-Realism & Structural Realism Master Series",
            "keyScholars": ["Kenneth Waltz", "John Mearsheimer", "Robert Jervis", "Stephen Walt"],
            "coreTheories": ["Kenneth Waltz's Theory of International Politics (1979): Structural Shift from Human Nature to Systemic Anarchy", "Three Structural Dimensions: Ordering Principle (Anarchy), Differentiation of Units (Functional Like-Units), Distribution of Capabilities", "Bipolarity vs Multipolarity: Waltz's Defense of Bipolar Stability (Predictability, Reduced Miscalculation)", "Defensive Realism (Waltz, Jervis): Security Dilemma; States Seek Appropriate Power for Survival, not Hegemony", "Offensive Realism (John Mearsheimer): Anarchy Compels States to Maximize Relative Power toward Regional Hegemony"]
        },
        {
            "batch_file": "batch_8_liberal_theories_complex_interdependence.md",
            "id": "p2a-liberalism-complex-interdependence",
            "number": "08",
            "title": "Liberal Theories of IR: Interdependence, Institutions & Democratic Peace",
            "subtitle": "Complex Interdependence (Keohane & Nye) | Neo-Liberal Institutionalism | Democratic Peace Theory (Michael Doyle) | Liberal World Order",
            "scanPages": list(range(80, 92)),
            "notebookPages": "Pages 41 to 49",
            "lecture": "Liberal International Relations Theory Series",
            "keyScholars": ["Robert Keohane", "Joseph Nye", "Michael Doyle", "Immanuel Kant", "Francis Fukuyama"],
            "coreTheories": ["Keohane and Nye's Complex Interdependence (Power and Interdependence, 1977)", "Three Core Characteristics: Multiple Channels, Absence of Hierarchy among Issues, Minor Role of Military Force", "Neo-Liberal Institutionalism: Institutions Mitigating Anarchy, Reducing Transaction Costs, Enabling Compliance", "Michael Doyle's Democratic Peace Theory (Rooted in Kant's Perpetual Peace): Democracies Do Not Fight Each Other", "The Liberal International World Order: Free Trade, Freedom of Navigation, Rule of Law, and Multilateralism"]
        },
        {
            "batch_file": "batch_9_marxist_critical_approaches_dependency_world_systems.md",
            "id": "p2a-marxist-critical-dependency",
            "number": "09",
            "title": "Marxist & Critical Approaches to IR: Dependency & World Systems",
            "subtitle": "Lenin's Imperialism | Dependency Theory (Andre Gunder Frank: Development of Underdevelopment) | Wallerstein World Systems Theory | Feminist IR (Tickner)",
            "scanPages": list(range(92, 103)),
            "notebookPages": "Pages 50 to 52",
            "lecture": "Marxist & Critical IR Theories Series",
            "keyScholars": ["Immanuel Wallerstein", "Andre Gunder Frank", "V.I. Lenin", "J. Ann Tickner", "Robert Cox"],
            "coreTheories": ["V.I. Lenin's Imperialism, the Highest Stage of Capitalism (1916): Monopoly Capital and Territorial Partition", "Andre Gunder Frank's Dependency Theory: The Development of Underdevelopment and Metropolis-Satellite Exploitation", "Immanuel Wallerstein's World Systems Theory: Tripartite Global Structure (Core, Periphery, Semi-Periphery)", "Robert Cox's Critical Theory: 'Theory is always for someone and for some purpose'; Problem-Solving vs Critical Theory", "J. Ann Tickner's Feminist Reformulation of Morgenthau's Six Principles of Political Realism"]
        },
        {
            "batch_file": "batch_10_scientific_approaches_systems_game_theory.md",
            "id": "p2a-scientific-approaches-game-theory",
            "number": "10",
            "title": "Scientific Approaches to IR: Morton Kaplan's Systems & Game Theory",
            "subtitle": "Morton Kaplan's Six International System Models | Game Theory (Prisoner's Dilemma, Chicken Game, Stag Hunt) | Decision-Making Models (Allison)",
            "scanPages": list(range(103, 114)),
            "notebookPages": "Pages 53 to 56",
            "lecture": "Scientific Methods & Behavioural IR Series",
            "keyScholars": ["Morton Kaplan", "Graham Allison", "Thomas Schelling", "Robert Axelrod"],
            "coreTheories": ["Morton Kaplan's System and Process in International Politics (1957): Six Heuristic System Models", "Kaplan's Typology: Balance of Power, Loose Bipolar, Tight Bipolar, Universal International, Hierarchical, Unit Veto Systems", "Game Theory in Strategic Studies: Rational Choice, Payoff Matrices, Zero-Sum vs Non-Zero-Sum Games", "The Prisoner's Dilemma: Structural Barriers to Cooperation under Anarchy; Axelrod's Tit-for-Tat Evolution", "Graham Allison's Decision-Making Models (Essence of Decision): Rational Actor, Organizational Behavior, Bureaucratic Politics"]
        },
        {
            "batch_file": "batch_11_concept_of_power_hard_soft_smart.md",
            "id": "p2a-concept-of-power",
            "number": "11",
            "title": "Concept of Power in IR: Hard, Soft, Smart & Sharp Power",
            "subtitle": "Elements of National Power (Tangible vs Intangible) | Joseph Nye: Soft Power & Co-optive Attraction | Smart Power | Sharp Power & Disinformation",
            "scanPages": list(range(114, 125)),
            "notebookPages": "Pages 57 to 59",
            "lecture": "Concept of Power in International Relations",
            "keyScholars": ["Joseph Nye", "Hans Morgenthau", "E.H. Carr", "Christopher Walker"],
            "coreTheories": ["Morgenthau's Elements of National Power: Geography, Natural Resources, Industrial Capacity, Military Preparedness, National Character", "Joseph Nye's Soft Power (Bound to Lead, 1990): The Ability to Affect Others through Co-optive Attraction rather than Coercion", "Three Resources of Soft Power: Culture, Political Values, and Legitimate Foreign Policy", "Smart Power (Nye): Strategic Synthesis of Hard Coercive Military/Economic Force and Soft Persuasive Appeal", "Sharp Power: Authoritarian Deployment of Disinformation, Subversion, and Digital Censorship to Pierce Democratic Publics"]
        },
        {
            "batch_file": "batch_12_management_of_power_balance_collective_security.md",
            "id": "p2a-management-of-power",
            "number": "12",
            "title": "Management of Power: Balance of Power & Collective Security",
            "subtitle": "Balance of Power Techniques (Internal vs External Balancing) | Collective Security Paradigm | League of Nations & UN Charter Chapter VII Failures",
            "scanPages": list(range(125, 135)),
            "notebookPages": "Pages 60 to 70",
            "lecture": "Management of Power Master Series",
            "keyScholars": ["Inis Claude", "Hans Morgenthau", "Kenneth Waltz", "Woodrow Wilson", "Jawaharlal Nehru"],
            "coreTheories": ["Balance of Power: Core Mechanisms (Alliances, Counter-Alliances, Armaments, Buffer Zones, Partitioning)", "Internal Balancing (Domestic Mobilization & Economic Growth) vs External Balancing (Alliances & Coalitions)", "Liberal Critique of Balance of Power: Woodrow Wilson's Rejection; Nehru's Dictum ('Nervous state of peace')", "Collective Security (One for All, All for One): Universal Legal Guarantee against Aggression", "Inherent Structural Contradictions of Collective Security: Veto Paralysis, Free-Riding, and Failure to Define Aggression"]
        },
        {
            "batch_file": "batch_13_cold_war_origins_evolution_detente.md",
            "id": "p2a-cold-war-detente",
            "number": "13",
            "title": "The Cold War: Origins, Evolution & The Era of Détente",
            "subtitle": "Orthodox vs Revisionist vs Post-Revisionist Schools | Truman Doctrine & Marshall Plan | Cuban Missile Crisis 1962 | Détente & Helsinki Accords 1975",
            "scanPages": list(range(135, 146)),
            "notebookPages": "Pages 71 to 90",
            "lecture": "The Cold War Historical Master Series",
            "keyScholars": ["George Kennan", "John Lewis Gaddis", "William Appleman Williams", "Henry Kissinger"],
            "coreTheories": ["Historiography of the Cold War: Orthodox/Traditionalist, Revisionist (Economic Imperialism), and Post-Revisionist Synthesis (Gaddis)", "George Kennan's 'Long Telegram' (1946) & Mr. X Article: Ideological Insecurity and the Containment Doctrine", "The Truman Doctrine (1947) & Marshall Plan: Institutional Division of Europe (NATO vs Warsaw Pact)", "The Cuban Missile Crisis (1962): Brinkmanship, Nuclear Parity, and the Inception of the Hotline", "The Era of Détente (1969–1979): Strategic Arms Limitation Talks (SALT I & II), Anti-Ballistic Missile (ABM) Treaty, Helsinki Final Act (1975)"]
        },
        {
            "batch_file": "batch_14_second_cold_war_collapse_soviet_union.md",
            "id": "p2a-second-cold-war-soviet-collapse",
            "number": "14",
            "title": "Second Cold War, Nuclear Arms Control & The Soviet Disintegration",
            "subtitle": "Soviet Invasion of Afghanistan (1979) | Reagan's Star Wars (SDI) | Gorbachev's Glasnost & Perestroika | INF Treaty 1987 | Fall of Berlin Wall & USSR Collapse (1991)",
            "scanPages": list(range(146, 156)),
            "notebookPages": "Pages 91 to 110",
            "lecture": "End of Cold War & Nuclear Regimes Series",
            "keyScholars": ["Mikhail Gorbachev", "Ronald Reagan", "John Lewis Gaddis", "Francis Fukuyama", "Stephen Cohen"],
            "coreTheories": ["The Outbreak of the Second Cold War: Soviet Intervention in Afghanistan (1979) and Death of Détente", "Reagan's Confrontational Strategy: Strategic Defense Initiative (SDI / Star Wars) and the 'Evil Empire' Rhetoric", "Mikhail Gorbachev's 'New Political Thinking': Perestroika (Economic Restructuring) and Glasnost (Political Openness)", "Nuclear Disarmament Breakthrough: Intermediate-Range Nuclear Forces (INF) Treaty (1987) Abolishing an Entire Class of Weapons", "The Sinatra Doctrine & The Fall of the Berlin Wall (1989): Unraveling of the Eastern Bloc and the Disintegration of the USSR (1991)"]
        },
        {
            "batch_file": "batch_15_post_cold_war_order_new_cold_war_synthesis.md",
            "id": "p2a-post-cold-war-new-cold-war",
            "number": "15",
            "title": "Post-Cold War Order, Emerging Multipolarity & Cold War 2.0",
            "subtitle": "Charles Krauthammer's Unipolar Moment | Francis Fukuyama's End of History | Rise of Revisionist Powers | Dmitri Trenin's Cold War 2.0 | Volume Synthesis",
            "scanPages": list(range(156, 165)),
            "notebookPages": "Pages 111 to 125",
            "lecture": "Post-Cold War Global Order & Master IR Synthesis",
            "keyScholars": ["Charles Krauthammer", "Francis Fukuyama", "Dmitri Trenin", "John Ikenberry", "S. Jaishankar"],
            "coreTheories": ["Charles Krauthammer's Unipolar Moment (1990): Unprecedented American Preponderance and Liberal Imperialism", "Francis Fukuyama's The End of History and the Last Man (1992): Universal Triumphalism of Western Liberal Democracy", "Structural Resurgence of Revisionism: Russia's Annexation of Crimea (2014) and China's Maritime Assertiveness", "Dmitri Trenin's Cold War 2.0 Thesis: Geopolitical and Technological Polarized Competition without Ideological Universalism", "Master Cross-Linkage Matrix: Integrating Comparative Politics, IR Theories, and 21st-Century Multipolarity"]
        }
    ]
    return batches

if __name__ == "__main__":
    b = get_part2_metadata()
    print(f"Loaded {len(b)} batch metadata definitions for Part 2 Notes (Paper 2 Section A).")
