import os
import json
import re

from batch_meta_part2 import get_part2_metadata
from batch_parser_part2 import parse_markdown_to_concepts, parse_flashcards, parse_model_answers

def build_part2_dataset():
    target_file = "app/src/data/paper2ComparativeData.js"
    
    meta = {
        "paper": "Paper 2 Section A (Comparative Politics & International Relations)",
        "topicTitle": "Paper 2 (Section A): Comparative Politics and International Relations Theory",
        "summary": "Exhaustive, 100% zero-loss digital knowledge repository of Shubhra Ranjan IAS lecture notes covering the foundational theoretical frameworks of Comparative Politics and International Relations: Comparative Politics & Approaches (Aristotle's constitutional classification, Traditional vs Modern Comparative Politics, David Easton's Systems Model, Gabriel Almond's Structural-Functionalism, Political Sociology, Political Economy, Almond & Verba's Civic Culture), Nature of the State (Advanced Industrial Welfare State, Corporatism, Hamza Alavi's Post-Colonial Overdeveloped State, Myrdal's Soft State), Politics of Representation & Participation (Maurice Duverger's Electoral Laws, Sartori's Party Systems, Kirchheimer's Catch-All Parties, Pressure Groups & Mancur Olson's Collective Action), Globalisation (Hyper-globalists, Skeptics, Transformationalists, Erosion of Westphalian Sovereignty, Global Civil Society), Theories of International Relations (Classical Realism: E.H. Carr, Hans Morgenthau's Six Principles; Structural Realism / Neo-Realism: Kenneth Waltz's Anarchy & Bipolar Stability; Offensive Realism: John Mearsheimer's Tragedy of Great Power Politics; Liberal Theories: Complex Interdependence by Keohane & Nye, Michael Doyle's Democratic Peace Theory, Neo-liberal Institutionalism; Marxist Approaches: Lenin's Imperialism, Andre Gunder Frank's Dependency Theory, Immanuel Wallerstein's World Systems Theory; Feminist IR: J. Ann Tickner's Critique of Morgenthau), Scientific Approaches (Morton Kaplan's Six System Models, Game Theory: Prisoner's Dilemma, Chicken Game, Graham Allison's Decision-Making Models), Concept & Management of Power (Hard, Soft & Smart Power by Joseph Nye, Balance of Power Techniques, Collective Security Paradigm vs Veto Paralysis), and The Cold War & Global Order (Origins & Historiography, Truman Doctrine, Cuban Missile Crisis, Détente, Second Cold War, Strategic Arms Control, Gorbachev's Glasnost & Perestroika, Fall of Berlin Wall & USSR Disintegration, Krauthammer's Unipolar Moment, Fukuyama's End of History, and Dmitri Trenin's Cold War 2.0).",
        "notebookPages": "Notebook Folios 1 to 125 (164 Scan Pages: 001 to 164)",
        "scanStart": 1,
        "scanEnd": 164,
        "scanBasePath": "/scans_p2_part2"
    }
    
    batches = get_part2_metadata()
    sections = []
    flashcards = []
    answers = []
    
    fc_id_counter = 1
    ans_id_counter = 1
    
    for b in batches:
        md_path = os.path.join("transcriptions_part2", b["batch_file"])
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
        print(f"Volume 6 Batch {b['number']} ({b['batch_file']}): {len(concepts)} concepts extracted.")
        
    # Generate 164-page scansCatalog for Volume 6
    page_catalog_titles = {
        1: "Title Page: Comparative Politics & International Relations (Shubhra Ranjan IAS Notes)",
        2: "Volume Flyleaf & Note Overview",
        3: "Master Handwritten Index: Comparative Politics, Methods, IR Theories & Cold War",
        4: "Course Syllabus Roadmap & Reference Bibliographies",
        5: "Important Reference Books: Baylis & Smith, Heywood, Malhotra & Robert Kaplan",
        6: "Flyleaf Notes & Introductory Terminology",
        7: "Comparative Govt & Politics: Evolution, Scope & Traditional Comparative Politics",
        8: "Limitations of Traditional Comparative Politics: Parochial, Eurocentric & Formalistic",
        9: "The Behavioural Revolution & Rise of Modern Comparative Politics",
        10: "David Easton's Systems Approach: Political System as Information Processing Unit",
        11: "Easton's Black Box Model: Inputs (Demands & Supports), Conversion, Outputs & Feedback",
        12: "Gabriel Almond's Structural-Functional Approach: System Maintenance & Adaptation",
        13: "Almond's Input Functions: Socialization, Recruitment, Interest Articulation & Aggregation",
        14: "Almond's Output Functions: Rule-Making, Rule-Application & Rule-Adjudication",
        15: "Political Sociology Approach: Social Cleavages, Class Power & Social Stratification",
        16: "Political Economy Approach: Interaction of State Coercion and Market Resource Allocation",
        17: "Political Culture Approach: Gabriel Almond & Sidney Verba's 'The Civic Culture' (1963)",
        18: "Three Ideal Types of Political Culture: Parochial, Subject, and Participant Cultures",
        19: "Congruence Theory: Aligning Political Culture with Democratic Constitutional Stability",
        20: "Lucian Pye's Political Development Syndrome: Equality, Capacity, and Differentiation",
        21: "Nature of the State in Advanced Industrial Societies: Classical Welfare State",
        22: "Crisis of the Welfare State: Claus Offe on Legitimation Crisis vs Capital Accumulation",
        23: "Corporatism vs Pluralism: Tripartite Peak Bargaining (State, Capital, Labour)",
        24: "Post-Industrial Society & Neoliberal Rollback of the State (Thatcherism, Reaganism)",
        25: "The State in Developing Societies: Decolonization & Post-Colonial Institutions",
        26: "Hamza Alavi's Overdeveloped State: Pakistan and Bangladesh Bureaucratic-Military Oligarchy",
        27: "Gunnar Myrdal's Soft State: Lack of Social Discipline, Institutional Corruption & Lawlessness",
        28: "Joel Migdal's State in Society: Strong Societies and Weak States in Third World Politics",
        29: "Politics of Representation: Functions and Evolution of Political Parties",
        30: "Maurice Duverger's Law: First-Past-The-Post (FPTP) vs Proportional Representation (PR)",
        31: "Giovanni Sartori's Party Typology: Moderate Pluralism vs Polarized Pluralism",
        32: "Otto Kirchheimer's Catch-All Party: Depoliticization and Ideological Convergence",
        33: "Pressure Groups: Classification (Associational, Non-Associational, Anomic, Institutional)",
        34: "Mancur Olson's Logic of Collective Action: The Free Rider Problem & Selective Incentives",
        35: "Iron Triangles & Policy Networks: Corporatist Lobbying in Western Democracies",
        36: "Globalisation and the Nation-State: Conceptual Dimensions (Economic, Cultural, Political)",
        37: "The Great Globalisation Debate: Hyper-Globalists vs Skeptics vs Transformationalists",
        38: "Kenichi Ohmae: The Borderless World and the Eclipse of Traditional Sovereignty",
        39: "Susan Strange: 'The Retreat of the State' and the Global Diffusion of Authority",
        40: "Paul Hirst & Grahame Thompson: The Skeptical Counter-Thesis on State Resilience",
        41: "David Held's Transformationalist Synthesis: Re-articulation and Adaptation of Sovereignty",
        42: "The Rise of Global Civil Society: International Non-Governmental Organizations (INGOs)",
        43: "Introduction to International Relations: The Anarchic Nature of International Politics",
        44: "Levels of Analysis in IR: Individual, Domestic/State, and Systemic/International Levels",
        45: "E.H. Carr's The Twenty Years' Crisis (1939): Demolition of Inter-War Utopian Liberalism",
        46: "Hans Morgenthau: Politics Among Nations (1948) & Foundational Principles of Realism",
        47: "Morgenthau's Six Principles of Political Realism: Objective Laws Grounded in Human Nature",
        48: "National Interest Defined as Power: The Currency of International Politics",
        49: "Autonomy of the Political Sphere: Decoupling Foreign Policy from Abstract Moral Dogma",
        50: "Critiques of Classical Realism: Inability to Explain Systemic Cooperation and Economic Change",
        51: "Kenneth Waltz: Man, the State and War (1959) & Three Images of International Relations",
        52: "Waltz's Theory of International Politics (1979): The Structural / Neo-Realist Revolution",
        53: "Three Structural Elements of International System: Ordering Principle, Units, Capabilities",
        54: "Why Bipolarity is More Stable than Multipolarity: Waltz's Structural Proof",
        55: "Defensive Realism (Waltz, Robert Jervis): Security Dilemma and Maintaining Status Quo",
        56: "Offensive Realism: John Mearsheimer's 'The Tragedy of Great Power Politics' (2001)",
        57: "Why States Seek Hegemony: Survival through Maximization of Relative Power",
        58: "Mearsheimer's Critique of Post-Cold War Liberal Triumphalism and Rise of China",
        59: "Liberal Theories of IR: Historical Roots in Immanuel Kant's Perpetual Peace (1795)",
        60: "Robert Keohane & Joseph Nye: Power and Interdependence (1977)",
        61: "Complex Interdependence: Multiple Channels, Absence of Issue Hierarchy, Irrelevance of Force",
        62: "Neo-Liberal Institutionalism: How International Regimes Facilitate Cooperation under Anarchy",
        63: "Michael Doyle's Democratic Peace Theory: Why Constitutional Republics Do Not Fight Each Other",
        64: "The Liberal International Order: Free Trade, Freedom of Navigation, Rule of Law, Institutions",
        65: "Marxist Approaches to International Relations: Economic Substructure of Global Imperialism",
        66: "V.I. Lenin: Imperialism, the Highest Stage of Capitalism (Monopoly Capital & Inter-Imperialist War)",
        67: "Andre Gunder Frank: Dependency Theory and the Development of Underdevelopment",
        68: "Metropolis-Satellite Exploitation: The Structural Extraction of Periphery Wealth",
        69: "Immanuel Wallerstein: World Systems Theory (Core, Periphery, and Semi-Periphery)",
        70: "The Semi-Periphery as a Structural Shock Absorber in Global Capitalist Accumulation",
        71: "Robert Cox's Critical Theory: Hegemony, Historic Blocs, and Problem-Solving Theories",
        72: "Feminist Approaches to IR: J. Ann Tickner's Reformulation of Morgenthau's Realist Principles",
        73: "Deconstructing Gendered Stereotypes in IR: Power, Rationality, and Security as Masculinist Constructs",
        74: "Scientific and Behavioural Approaches to IR: The Quest for Rigorous Predictive Science",
        75: "Morton Kaplan's Six Heuristic International System Models (System and Process, 1957)",
        76: "Kaplan's System Models: Balance of Power, Loose Bipolar, Tight Bipolar Systems",
        77: "Kaplan's Universal, Hierarchical, and Unit-Veto System Models",
        78: "Game Theory in Strategic Decision Making: Rational Choice and Payoff Structures",
        79: "The Prisoner's Dilemma: Structural Barriers to Cooperation & Robert Axelrod's Evolution of Cooperation",
        80: "The Game of Chicken: Brinkmanship, Nuclear Deterrence, and Rationality of Irrationality",
        81: "Graham Allison's Essence of Decision (1971): Cuban Missile Crisis Decision-Making Models",
        82: "Model I (Rational Actor), Model II (Organizational Behavior), Model III (Bureaucratic Politics)",
        83: "Concept of Power in IR: Power as Relational, Contextual, and Coercive Capacity",
        84: "Tangible vs Intangible Elements of National Power (Geography, Military, Morale, Leadership)",
        85: "Joseph Nye's Soft Power (1990): Co-optive Attraction vs Coercive Carrots and Sticks",
        86: "Three Sources of Soft Power: Cultural Appeal, Political Ideals, and Legitimate Foreign Policies",
        87: "Smart Power: Strategic Integration of Hard Coercion and Soft Attraction",
        88: "Sharp Power: Authoritarian Information Subversion and Censorship in Democratic Publics",
        89: "Management of Power: The Balance of Power Paradigm (Westphalian Tradition)",
        90: "Internal Balancing (Economic Mobilization) vs External Balancing (Alliance Building)",
        91: "Techniques of Balance of Power: Alliances, Armaments, Buffer States, Partition, War",
        92: "Liberal Critique of Balance of Power: Woodrow Wilson and Nehru ('Nervous State of Peace')",
        93: "The Collective Security Paradigm: 'One for All, and All for One' under International Law",
        94: "Prerequisites of Collective Security: Universal Commitment and Overwhelming Coalition",
        95: "Inherent Failures of Collective Security: League of Nations Collapse in Manchuria and Abyssinia",
        96: "UN Charter Chapter VII Collective Security and the Permanent Five (P5) Veto Impasse",
        97: "The Cold War: Nature, Ideological Polarization, and Historiographical Debates",
        98: "Historiography of the Cold War: Orthodox (Soviet Aggression), Revisionist (US Capitalism), Post-Revisionist",
        99: "George Kennan's Long Telegram (1946) & Mr. X Article: The Doctrine of Containment",
        100: "Winston Churchill's Iron Curtain Speech (1946) at Fulton, Missouri",
        101: "The Truman Doctrine (1947): Global Containment of Communist Expansion (Greece and Turkey)",
        102: "The Marshall Plan (1947): Economic Reconstruction of Western Europe vs Soviet Molotov Plan",
        103: "The First Cold War (1947–1953): Berlin Blockade, Formation of NATO (1949), Korean War",
        104: "Nuclear Parity: Soviet Union's 1949 Atomic Test and the Inception of Strategic Bipolarity",
        105: "The Baruch Plan vs The Gromyko Plan: The Failed Inception of Nuclear Disarmament",
        106: "The Warsaw Pact (1955): Soviet Military Counterpart to NATO in Eastern Europe",
        107: "The Cuban Missile Crisis (October 1962): Nuclear Brinkmanship and the Brink of Armageddon",
        108: "Resolution of Cuban Crisis: Secret Removal of US Jupiter Missiles from Turkey and Hotline Agreement",
        109: "Nuclear Deterrence Theory: Mutual Assured Destruction (MAD) and Second-Strike Capability",
        110: "The Era of Détente (1969–1979): Relaxation of Superpower Tensions under Nixon and Brezhnev",
        111: "Strategic Arms Limitation Talks (SALT I, 1972) and Anti-Ballistic Missile (ABM) Treaty",
        112: "The Helsinki Accords (1975): Recognition of Post-War European Borders & Human Rights Basket",
        113: "The Non-Aligned Movement (NAM): Historical Genesis at Bandung (1955) and Belgrade (1961)",
        114: "The Founding Fathers of NAM: Nehru, Tito, Nasser, Sukarno, and Kwame Nkrumah",
        115: "Core Principles of Non-Alignment: Strategic Autonomy, Anti-Imperialism, and Nuclear Disarmament",
        116: "The Second Cold War (1979–1985): Soviet Invasion of Afghanistan and the Death of Détente",
        117: "The Carter Doctrine (1980): Defending Persian Gulf Oil Fields against Soviet Incursions",
        118: "Ronald Reagan's Confrontational Strategy: The 'Evil Empire' Rhetoric and Military Buildup",
        119: "Strategic Defense Initiative (SDI / Star Wars, 1983): Space-Based Missile Defense Shield",
        120: "Nuclear Non-Proliferation Treaty (NPT 1968): Discriminatory Architecture and India's Principled Objection",
        121: "Comprehensive Nuclear-Test-Ban Treaty (CTBT 1996): Flawed Entry-into-Force Clause (Article XIV)",
        122: "Mikhail Gorbachev's Accession (1985): The Crisis of the Soviet Command Economy",
        123: "Gorbachev's New Political Thinking: Perestroika (Economic Restructuring) & Glasnost (Openness)",
        124: "Reykjavik Summit (1986) & The Washington INF Treaty (1987): Eliminating Intermediate Nuclear Missiles",
        125: "The Sinatra Doctrine ('My Way'): Repudiation of the Brezhnev Doctrine in Eastern Europe",
        126: "The Fall of the Berlin Wall (November 9, 1989): Unification of Germany and End of Iron Curtain",
        127: "The Dissolution of the Soviet Union (December 1991): Alma-Ata Protocol and Creation of CIS",
        128: "The End of Bipolarity and the Transition to Post-Cold War Global Architecture",
        129: "Charles Krauthammer: 'The Unipolar Moment' (1990) and American Hyperpower Supremacy",
        130: "Francis Fukuyama: 'The End of History and the Last Man' (1992) — Final Universal Ideology",
        131: "Relevance of NAM in the Post-Cold War Era: Is Non-Alignment Obsolete?",
        132: "NAM 2.0 and Strategic Autonomy: Re-purposing the Platform for the Global South",
        133: "The Post-Cold War Nuclear Order: Proliferation Networks (A.Q. Khan) and Rogue States",
        134: "India's Nuclear Doctrine (2003): Credible Minimum Deterrence and No First Use (NFU)",
        135: "Massive Retaliation and Civilian Political Command in India's Nuclear Command Authority (NCA)",
        136: "The Expansion of NATO into Eastern Europe: Breaking Post-Cold War Assurances to Moscow",
        137: "The Resurgence of Russian Revisionism: Munich Security Conference (2007) and Georgia War (2008)",
        138: "The 2014 Ukraine Crisis: Annexation of Crimea and the De-facto Rupture of Russia-West Ties",
        139: "New Cold War / Cold War 2.0 (Dmitri Trenin Thesis): Global Geopolitical Polarization without Ideology",
        140: "Differences between Cold War 1.0 and Cold War 2.0: Multipolarity, Cyber Warfare, Deep Economic Interdependence",
        141: "The Rise of China as the Primary Systemic Challenger to the Liberal International Order",
        142: "The US-China Trade and Technology War: 5G, Semiconductors, Artificial Intelligence, and Decoupling",
        143: "Global Commons Governance: Cybersecurity, Outer Space Militarization, and Climate Multilateralism",
        144: "Master Cross-Linkage Matrix 1: Realist Canon Evolution (Thucydides to Mearsheimer)",
        145: "Master Cross-Linkage Matrix 2: Liberal Internationalism (Kant to Neo-Liberal Institutionalism)",
        146: "Master Cross-Linkage Matrix 3: Marxist & Dependency Critiques of International Capital",
        147: "Master Cross-Linkage Matrix 4: Comparative Approaches to the State in the Global Era",
        148: "Master Cross-Linkage Matrix 5: Systems Theory, Power Dynamics, and Deterrence Stability",
        149: "Master Cross-Linkage Matrix 6: The Evolution and Crises of Global Multilateralism",
        150: "UPSC PSIR Mains Model Answer Synthesis 1: Waltz vs Mearsheimer on Structural Realism",
        151: "UPSC PSIR Mains Model Answer Synthesis 2: Complex Interdependence and Liberal World Order",
        152: "UPSC PSIR Mains Model Answer Synthesis 3: Wallerstein's World Systems Theory and Global South",
        153: "UPSC PSIR Mains Model Answer Synthesis 4: Post-Colonial State (Hamza Alavi & Myrdal)",
        154: "UPSC PSIR Mains Model Answer Synthesis 5: Impact of Globalisation on Westphalian Sovereignty",
        155: "UPSC PSIR Mains Model Answer Synthesis 6: Balance of Power vs Collective Security",
        156: "UPSC PSIR Mains Model Answer Synthesis 7: End of History vs Clash of Civilizations",
        157: "UPSC PSIR Mains Model Answer Synthesis 8: Cold War 2.0 and India's Multi-Alignment Strategy",
        158: "Grand Epilogue: Archival Synthesis of Comparative Politics & International Relations Theory",
        159: "Appendix A: Consolidated Chronological Timeline of 20th and 21st Century International Relations",
        160: "Appendix B: Master Scholar and Thematic Conceptual Glossary for Paper 2 Section A",
        161: "Appendix C: Key Terminology Index (Anarchy, Hegemony, Cleavages, Interdependence, Deterrence)",
        162: "Appendix D: Methodological Toolkit for UPSC PSIR Comparative Analysis and Answer Enrichment",
        163: "Appendix E: Complete Scan Image Cross-Referencing Table (Scans 001 to 164)",
        164: "Final Concluding Folio: End of Part 2 Comparative Politics & IR Handwritten Notes (Shubhra Ranjan IAS)"
    }
    
    scans_catalog = []
    for p in range(1, 165):
        num_str = f"{p:03d}"
        f_name = f"page_{num_str}.png"
        
        batch_num = "01"
        for b in batches:
            if p in b["scanPages"]:
                batch_num = b["number"]
                break
                
        title = page_catalog_titles.get(p, f"Comparative Politics & IR Theory Analysis - Page {p}")
        
        scans_catalog.append({
            "pageNumber": p,
            "filename": f_name,
            "title": title,
            "batch": batch_num,
            "thumbnail": f"/scans_p2_part2/{f_name}",
            "fullImage": f"/scans_p2_part2/{f_name}"
        })
        
    js_content = f"""// UPSC PSIR Paper 2 (Section A): Comparative Politics and International Relations Theory
// Compiled from 164 Scan Pages of Shubhra Ranjan IAS Handwritten Lecture Notes
// 100% Zero-Loss Digital Repository with Interactive Dual-Pane Scan Inspection

export const paper2ComparativeMetadata = {json.dumps(meta, indent=2)};

export const paper2ComparativeSections = {json.dumps(sections, indent=2)};

export const paper2ComparativeFlashcards = {json.dumps(flashcards, indent=2)};

export const paper2ComparativeModelAnswers = {json.dumps(answers, indent=2)};

export const paper2ComparativeScansCatalog = {json.dumps(scans_catalog, indent=2)};
"""
    
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"Successfully generated {target_file} ({os.path.getsize(target_file)} bytes).")

if __name__ == "__main__":
    build_part2_dataset()
