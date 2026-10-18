# scripts/build_full_sections.py
import json

print("Reading base data...")
with open('app/src/data/paper1IptData.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = 'export const paper1IptData = '
js_obj = text[len(prefix):].rstrip(';\n')
data = json.loads(js_obj)

# Keep sections 0-4 (Intro, Manu, Kautilya Saptanga, Kautilya Mandala, Buddha)
base_sections = data['sections'][:5]

# Expand Section 6: Sir Syed Ahmed Khan (Pages 28 to 30)
sec_sir_syed = {
  "id": "modern-ipt-sir-syed",
  "number": "06",
  "title": "Modern Indian Political Thought: Sir Syed Ahmed Khan",
  "subtitle": "Muslim Modernism | Rationalism & Scientific Temper | Aligarh Movement & Genesis of Two-Nation Theory",
  "scanPages": [28, 29, 30],
  "notebookPages": "Pages 13 & 14",
  "lecture": "Lecture 51 & 52 (16/02/2017 & 17/02/2017)",
  "keyScholars": [
    "Sir Syed Ahmed Khan (1817–1898)",
    "Altaf Husain Hali",
    "Prof. Bipan Chandra",
    "Francis Robinson",
    "Shan Mohammad"
  ],
  "coreTheories": [
    "Post-1857 Muslim Regeneration & Trauma",
    "Rationalism & Scientific Temper (Tahzib-ul-Akhlaq)",
    "Aligarh Movement & MAO College (1875)",
    "Loyalty to British Crown as Pragmatic Survival (Asbab-e-Baghawat-e-Hind)",
    "Critique of Indian National Congress & Majoritarian Democracy",
    "Evolution from 'Two Beautiful Eyes of a Bride' to Two-Nation Roots"
  ],
  "concepts": [
    {
      "title": "Historical Context & Socio-Political Trauma (Post-1857)",
      "scanPage": 28,
      "badge": "Historical Catalyst",
      "summary": "Following the 1857 Revolt, Muslims faced acute imperial retribution, economic dispossession, and intellectual alienation from modern Western education.",
      "details": [
        "British Revenge: The British held Muslims primarily responsible for the 1857 revolt, systematically excluding them from colonial administrative posts and civil services.",
        "Orthodox Resistance: Ulema and traditional madrasas rejected English education as Christian subversion, causing Muslims to lag severely behind the Western-educated Hindu middle class.",
        "Sir Syed's Pragmatic Mission: Reconcile Muslims with British rule to ensure socio-economic survival, arguing loyalty was the sole pathway to security."
      ]
    },
    {
      "title": "Scientific Rationalism & Educational Modernization",
      "scanPage": 28,
      "badge": "Intellectual Renaissance",
      "summary": "Sir Syed championed a modern scientific temper, insisting true religious revelation must conform to laws of nature.",
      "details": [
        "Scientific Society (1864): Established at Ghazipur/Aligarh to translate Western scientific works into Urdu.",
        "Journal 'Tahzib-ul-Akhlaq': Advocated social reform, moral awakening, and purging superstitions from Indian Muslim life.",
        "Muhammadan Anglo-Oriental (MAO) College (1875): Modeled on Oxford and Cambridge, later elevated to Aligarh Muslim University (AMU) in 1920."
      ]
    },
    {
      "title": "Dual Front of Criticism & Defense of Loyalty",
      "scanPage": 29,
      "badge": "Ideological Polemics",
      "summary": "Sir Syed operated under intense crossfire from both conservative Islamic orthodoxy and British imperial suspicion.",
      "details": [
        "Attack by Orthodox Ulema: Clerics issued fatwas declaring him a 'Kafir' (apostate), heretic, and agent of Western imperialism.",
        "Asbab-e-Baghawat-e-Hind (Causes of Indian Revolt, 1858): Courageously argued British failure to admit Indians into legislative bodies caused 1857.",
        "The Loyal Muhammadans of India (1860): Defended Muslim loyalty to the British Crown, countering William Hunter's thesis in 'The Indian Musalmans'."
      ]
    },
    {
      "title": "Political Philosophy: From Composite Nationalism to Two-Nation Genesis",
      "scanPage": 30,
      "badge": "Communal Transformation",
      "summary": "Sir Syed's political trajectory shifted decisively from composite Indian nationalism to minority identity politics.",
      "details": [
        "Early Composite View: Famously proclaimed Hindus and Muslims are the 'two beautiful eyes of a bride' (India); harm to one disfigures the other.",
        "Hindi-Urdu Controversy (1867): The demand in UP to replace Urdu with Hindi in courts convinced Sir Syed that Hindu-Muslim joint political action was unviable.",
        "Boycott of Indian National Congress (1885): Strongly discouraged Muslims from joining INC, labeling it a Bengali-Hindu-dominated body whose majoritarian democratic demands would permanently subordinate the Muslim minority."
      ]
    }
  ]
}

# Section 7: Sri Aurobindo Ghosh (Pages 31 to 38)
sec_aurobindo = {
  "id": "modern-ipt-aurobindo",
  "number": "07",
  "title": "Sri Aurobindo Ghosh: Spiritual Nationalism, Passive Resistance & Integral Yoga",
  "subtitle": "Prophet of Indian Nationalism | Mother India (Bhavani Bharati) | 'New Lamps for Old' | Passive Resistance & Purna Yoga",
  "scanPages": [31, 32, 33, 34, 35, 36, 37, 38],
  "notebookPages": "Pages 14 to 17",
  "lecture": "Lecture 52 & 53 (17/02/2017 & 18/02/2017)",
  "keyScholars": [
    "Sri Aurobindo Ghosh (1872–1950)",
    "Rabindranath Tagore ('The sun of your glory...')",
    "Bankim Chandra Chatterjee (Anandamath)",
    "Prof. Bipan Chandra",
    "Sisir Kumar Ghose"
  ],
  "coreTheories": [
    "Spiritual Theory of Nationalism (Neo-Vedantism & Sanatana Dharma)",
    "Nation as Mother (Bhavani Bharati / Atma of the Collectivity)",
    "Critique of Moderates in 'New Lamps for Old' (Induprakash, 1893)",
    "Swaraj as Absolute Independence (End in Itself)",
    "Doctrine of Passive Resistance (Comparison with Gandhi's Satyagraha)",
    "Philosophy of Freedom (Spiritual Freedom vs Mechanical State Coercion)",
    "Ideal of Human Unity (World Union of Free Nations)",
    "Integral Yoga (Purna Yoga & Descent of the Supermind)"
  ],
  "concepts": [
    {
      "title": "Spiritual Theory of Nationalism & The Living Mother",
      "scanPage": 31,
      "badge": "Metaphysical Nationalism",
      "summary": "Aurobindo transfigured nationalism from a mere political programme into a living religion and divine spiritual mission.",
      "details": [
        "Tagore's Homage: Rabindranath Tagore declared: 'Aurobindo, accept the salutation from Rabindranath... you have the word and we are waiting to accept it from you.'",
        "Nation as Divine Being: Rejected Western contractual and territorial definitions. India is not a piece of earth; she is Mother India (Bhavani Bharati), a living divine spirit (*Shakti*).",
        "Sanatana Dharma as Nationalism: Declared at Uttarpara (1909) that Sanatana Dharma itself is Indian nationalism; India rises not for herself, but to give spiritual light to humanity."
      ]
    },
    {
      "title": "Critique of Moderates: 'New Lamps for Old' (1893)",
      "scanPage": 33,
      "badge": "Radical Critique",
      "summary": "In his revolutionary essays in the journal Induprakash, Aurobindo tore into the mendicant politics of the Early Nationalist leadership.",
      "details": [
        "Intellectual Bankruptcy: Accused Moderates of suffering from intellectual blindness and playing a futile game of 'prayers, petitions, and protests'.",
        "Barking Without Biting: Denounced Moderate politics as 'politics of mendicancy' and timid imitation of British constitutional forms without real power.",
        "Swaraj as Absolute Independence: Unlike Moderates seeking Dominion status within the British Empire, Aurobindo was among the very first to demand complete independence (Poorna Swaraj) as an inalienable right."
      ]
    },
    {
      "title": "Doctrine of Passive Resistance & Strategic Fourfold Boycott",
      "scanPage": 35,
      "badge": "Resistance Praxis",
      "summary": "Preceding Gandhi, Aurobindo formulated the tactical doctrine of Passive Resistance during the 1905 Swadeshi movement.",
      "details": [
        "Fourfold Boycott: (1) Economic boycott of foreign goods, (2) Educational boycott of government schools, (3) Judicial boycott in favor of voluntary arbitration courts, (4) Administrative boycott of executive offices.",
        "Comparison with Gandhi: Aurobindo viewed non-violence as a pragmatic strategy and policy, permitting armed self-defense if state repression becomes intolerable; Gandhi viewed Ahimsa as an absolute, inviolable creed and moral religion."
      ]
    },
    {
      "title": "Integral Yoga (Purna Yoga) & Ideal of Human Unity",
      "scanPage": 38,
      "badge": "Cosmic Evolution",
      "summary": "In Pondicherry, Aurobindo developed Integral Yoga to transform fragmented human ego into the supramental cosmic consciousness.",
      "details": [
        "Evolution of Consciousness: Matter -> Life -> Mind -> Supermind -> Sachchidananda (Sat-Chit-Ananda).",
        "Purna Yoga: Synthesis of Karma Yoga (Action), Jnana Yoga (Knowledge), Bhakti Yoga (Devotion), Raja Yoga (Meditation), and Hatha Yoga.",
        "Ideal of Human Unity: Rejects centralized World State or imperial aggregation in favor of a free, voluntary World Union / Federation of autonomous self-determining nations."
      ]
    }
  ]
}

# Section 8: Mahatma Gandhi: Moral Politics, Satyagraha, Swaraj & Hind Swaraj (Pages 39 to 44)
sec_gandhi_core = {
  "id": "modern-ipt-gandhi-core",
  "number": "08",
  "title": "Mahatma Gandhi: Moral Politics, Satyagraha, Swaraj & Hind Swaraj",
  "subtitle": "Ahimsa as Active Love | Satyagraha vs Passive Resistance | 4 Dimensions of Swaraj | Hind Swaraj (1909) Civilisational Critique",
  "scanPages": [39, 40, 41, 42, 43, 44],
  "notebookPages": "Pages 18 to 21",
  "lecture": "Lecture 53 & 54 (18/02/2017 & 21/02/2017)",
  "keyScholars": [
    "Mahatma Gandhi (1869–1948)",
    "Prof. Humayun Kabir",
    "Prof. Bipan Chandra",
    "John Ruskin ('Unto This Last')",
    "Leo Tolstoy ('The Kingdom of God Is Within You')",
    "Henry David Thoreau ('Civil Disobedience')"
  ],
  "coreTheories": [
    "Ahimsa (Non-violence) as Active Love & Weapon of the Brave",
    "Satyagraha (Truth-Force) vs Passive Resistance (Soul-Force vs Weak Weapon)",
    "Four Dimensions of Swaraj (Political, Economic, Social, Moral/Atma-Swaraj)",
    "Sarvodaya (Welfare of All & Rejection of Utilitarianism)",
    "Bread Labour (Sharir-Shrama) & Khadi Economics",
    "Critique of Modern Industrial Civilisation (Hind Swaraj 1909)",
    "Critique of Parliament ('Sterile Woman & Prostitute'), Lawyers, Doctors, Machinery",
    "Ecological Sustainability ('Earth provides enough for every man's need, but not for every man's greed')"
  ],
  "concepts": [
    {
      "title": "Philosophical Profile & Master Strategist",
      "scanPage": 39,
      "badge": "Leadership Axiom",
      "summary": "Gandhi fused spiritual saintliness with unmatched mass political strategy, transforming India's freedom struggle into the largest mass movement in history.",
      "details": [
        "Experiments with Truth: 'My life is my message' and 'Experiments with Truth'—refused to create an dogmatic '-ism' (Gandhism), emphasizing living moral praxis.",
        "Prof. Humayun Kabir: Characterized Gandhi as a politician endowed with deep understanding of mass psychology.",
        "Bipan Chandra: Analyzed Gandhi as a master strategist who understood the finite endurance capacity of the masses, pioneering Struggle-Truce-Struggle (S-T-S)."
      ]
    },
    {
      "title": "Ahimsa: Active Love & The Weapon of the Brave",
      "scanPage": 40,
      "badge": "Core Ethic",
      "summary": "Ahimsa in Gandhian thought is not mere passive non-killing; it is positive, active love and absolute fearlessness.",
      "details": [
        "Weapon of the Brave: Rejects cowardice. Gandhi famously declared: 'Where there is only a choice between cowardice and violence, I would advise violence.'",
        "Active Love: Ahimsa means resisting evil without hatred for the evildoer; conquering anger through love and falsehood through truth."
      ]
    },
    {
      "title": "Satyagraha vs. Passive Resistance",
      "scanPage": 40,
      "badge": "Epistemic Contrast",
      "summary": "Gandhi drew an absolute qualitative distinction between Satyagraha (Soul-Force) and Western Passive Resistance.",
      "details": [
        "Satyagraha: Soul-force based on absolute truth and love. Never inflicts suffering on the adversary; invites suffering on oneself to appeal to the opponent's moral conscience.",
        "Passive Resistance: A weapon of the weak used when violent means are unavailable. Characterized by latent hatred and willingness to use force if opportunity arises."
      ]
    },
    {
      "title": "Four Dimensions of Swaraj",
      "scanPage": 41,
      "badge": "Holistic Freedom",
      "summary": "Swaraj is not merely the transfer of power from white hands to brown hands; it is four-dimensional emancipation.",
      "details": [
        "Political Swaraj: Complete national independence and radical democratic decentralization into village republics.",
        "Economic Swaraj: Self-reliance (*Swadeshi*), decentralized cottage industry, revival of the charkha, and eradication of rural poverty.",
        "Social Swaraj: Eradication of untouchability, communal harmony between Hindus and Muslims, and gender equality.",
        "Moral / Atma-Swaraj: Mastery over one's own senses, desires, and passions—true freedom is self-rule."
      ]
    },
    {
      "title": "Sarvodaya & Bread Labour: Rejection of Utilitarianism",
      "scanPage": 42,
      "badge": "Political Economy",
      "summary": "Influenced by John Ruskin's 'Unto This Last', Gandhi rejected Jeremy Bentham's utilitarianism ('greatest good of the greatest number').",
      "details": [
        "Welfare of All: Utilitarianism justifies sacrificing the minority 49% for the 51%. Sarvodaya insists on the welfare of all, starting with the last and lowest (*Antyodaya*).",
        "Bread Labour (Sharir-Shrama): Every individual must perform physical bodily labour to earn their daily bread; intellectual work gives no right to exploit others."
      ]
    },
    {
      "title": "Critique of Modern Civilisation: Hind Swaraj (1909)",
      "scanPage": 43,
      "badge": "Radical Civilisational Critique",
      "summary": "Written aboard the ship *Kildonan Castle*, Hind Swaraj delivers an uncompromising indictment of modern Western industrialism.",
      "details": [
        "Critique of Parliament: Denounced the British Parliament as a 'sterile woman and a prostitute'—sterile because it cannot act without outside pressure, prostitute because it is under the sway of ministers.",
        "Critique of Professions: Lawyers deepen disputes and entrench British courts; modern doctors promote bodily indulgence and weaken moral self-control; railways facilitate the rapid spread of famine and exploitation.",
        "Ecological Warning: Gandhi warned that if India with its vast population imitated British industrialism, it would strip the globe bare like a swarm of locusts: '9 more earths would be required'."
      ]
    }
  ]
}

# Section 9: Mahatma Gandhi: Theory of State, Trusteeship, Ends & Means, Rights & Duties (Pages 45 to 49)
sec_gandhi_state = {
  "id": "modern-ipt-gandhi-state",
  "number": "09",
  "title": "Mahatma Gandhi: Theory of State, Trusteeship, Ends & Means & Educational Philosophy",
  "subtitle": "Philosophical Anarchism | Ramrajya & Oceanic Circles | Moral Trusteeship | Organic Ends-Means | Nayee Taalim",
  "scanPages": [45, 46, 47, 48, 49],
  "notebookPages": "Pages 21 to 23",
  "lecture": "Lecture 54 (21/02/2017)",
  "keyScholars": [
    "Mahatma Gandhi",
    "Leo Tolstoy ('Kingdom of God Is Within You')",
    "Gopal Krishna Gokhale (Spiritualisation of Politics)",
    "Edward Carpenter ('Civilisation: Its Cause and Cure')",
    "Ashis Nandy ('The Intimate Enemy')",
    "Prof. Bhikhu Parekh",
    "Ramachandra Guha",
    "Dennis Dalton"
  ],
  "coreTheories": [
    "Theory of the State: Philosophical Anarchism & Stateless Ramrajya",
    "The State as a 'Soulless Machine' based on Concentrated Violence",
    "Oceanic Circles of Power vs Hierarchical Pyramids",
    "Doctrine of Trusteeship (Capital as Social Production, Rejection of Class War)",
    "Organic Inseparability of Ends and Means (Sadhan-Sadhya Unity)",
    "Critique of Machiavellianism (Politics without Ethics is a Death Trap)",
    "Rights Embryonic within Duties (Bhagavad Gita & Nishkama Karma)",
    "Feminist Hermeneutics (Sita & Draupadi as Moral Soul-Force)",
    "Nayee Taalim (Wardha Scheme of Basic Education: Earning while Learning)"
  ],
  "concepts": [
    {
      "title": "Theory of the State: Philosophical Anarchism & Ramrajya",
      "scanPage": 47,
      "badge": "Political Theory",
      "summary": "Gandhi was a philosophical anarchist who regarded the state as fundamentally incompatible with Ahimsa.",
      "details": [
        "State as Soulless Machine: The state represents concentrated, organized violence. While an individual has a soul, the state is a soulless machine.",
        "Ramrajya as Stateless Democracy: An enlightened anarchy where everyone rules themselves in such a manner that they are never a hindrance to their neighbor.",
        "Oceanic Circles of Power: Life will not be a pyramid with the apex sustained by the bottom; it will be an oceanic circle whose center will be the individual, ever expanding into self-reliant village republics."
      ]
    },
    {
      "title": "Doctrine of Trusteeship & Political Economy",
      "scanPage": 45,
      "badge": "Economic Ethics",
      "summary": "Gandhi rejected Marxist class struggle, asserting that wealth is created collectively by society and must be held in moral trust.",
      "details": [
        "Capitalist as Trustee: Wealthy industrialists must consider themselves trustees of society's wealth, retaining only what is reasonably necessary for their upkeep and using the rest for the public good.",
        "Rejection of Expropriation: Forcible dispossession destroys the productive genius of individuals; change must come through moral conversion (*Hridaya Parivartan*)."
      ]
    },
    {
      "title": "Absolute Inseparability of Ends and Means",
      "scanPage": 48,
      "badge": "Moral Epistemology",
      "summary": "Gandhi rejected Machiavellian realpolitik, insisting that the means determine the ultimate nature of the end achieved.",
      "details": [
        "Seed and Tree Analogy: The means may be likened to a seed, the end to a tree. One cannot sow the seed of a thorny babul and expect a fragrant rose.",
        "Spiritualization of Politics: Inherited from Gokhale; declared that 'politics without ethics and religion is a death trap, because it kills the soul'."
      ]
    },
    {
      "title": "Rights and Duties: The Nishkama Karma Paradigm",
      "scanPage": 49,
      "badge": "Deontological Ethics",
      "summary": "Gandhi grounded human rights entirely within the performance of fundamental moral duties.",
      "details": [
        "Embryonic Rights: Rights that are not preceded by duties performed are illegitimate. All rights are embryonic within duty.",
        "Bhagavad Gita: Inspired by *Nishkama Karma*—focus on right action without anxiety over fruits."
      ]
    },
    {
      "title": "Feminism & Basic Education (Nayee Taalim)",
      "scanPage": 49,
      "badge": "Social Pedagogy",
      "summary": "Gandhi reinterpreted female figures as symbols of moral courage and designed an experiential model of schooling.",
      "details": [
        "Women as Incarnations of Ahimsa: Reinterpreted Sita and Draupadi not as passive victims, but as titans of moral soul-force who resisted supreme tyranny.",
        "Nayee Taalim (1937): Wardha Scheme of education combining head, heart, and hand; learning through manual productive crafts (earning while learning)."
      ]
    }
  ]
}

# Section 10: M.N. Roy: Revolutionary, Marxist & Radical Humanist (Pages 50 to 56)
sec_mn_roy = {
  "id": "modern-ipt-mn-roy",
  "number": "10",
  "title": "M.N. Roy: Revolutionary, Marxist, Radical Humanist & Partyless Democracy",
  "subtitle": "Lenin-Roy Colonial Debates (1920) | 5-Point Critique of Marxism | Triad of Freedom, Reason & Ethics | People's Plan (1944)",
  "scanPages": [50, 51, 52, 53, 54, 55, 56],
  "notebookPages": "Pages 24 to 26",
  "lecture": "Lecture 54 (21/02/2017)",
  "keyScholars": [
    "M.N. Roy (1887–1954)",
    "V.I. Lenin (2nd Comintern Congress 1920)",
    "Sudipto Kaviraj ('Remarkable Failure' verdict)",
    "Sibnarayan Ray ('The Erasmus of Modern India')",
    "Thomas Hobbes, John Locke, Jeremy Bentham, Baruch Spinoza"
  ],
  "coreTheories": [
    "Phase I: Revolutionary Nationalist (Anushilan Samiti & Bagha Jatin)",
    "Phase II: Marxist Comintern Leader & Historic Lenin-Roy Debates (1920)",
    "Roy's Critique of Gandhi as Bourgeois Leader & Charkha as Medieval Fetish",
    "Expulsion from Comintern (1929) & League of Radical Congressmen (1939)",
    "5-Point Critique of Orthodox Marxism (Ideas, Dialectics, Class, Surplus, Revolution)",
    "Phase III: Radical Humanism / New Humanism (Man in Original Sense)",
    "Triad of Radical Humanism: Reason (Biological), Freedom, Ethics (Secular)",
    "Partyless Democracy (Organized Democracy via People's Committees / Lok Samitis)",
    "People's Plan (1944) for Post-War Economic Reconstruction",
    "8-Point Comprehensive Comparative Matrix: Mahatma Gandhi vs M.N. Roy"
  ],
  "concepts": [
    {
      "title": "Evolutionary Odyssey: Revolutionary to Comintern Leader",
      "scanPage": 50,
      "badge": "Intellectual Trajectory",
      "summary": "M.N. Roy was the only Indian thinker to play a frontline role in both the Russian and Mexican revolutions before pioneering Radical Humanism.",
      "details": [
        "Sudipto Kaviraj's Evaluation: Termed Roy a 'remarkable failure'—a profound philosopher who failed to connect with the Indian masses because he lacked Gandhi's cultural vernacular.",
        "Lenin-Roy Debates (1920): At the 2nd Comintern Congress, Lenin argued communists should support bourgeois nationalist movements (INC). Roy countered with his 'Supplementary Theses', asserting Gandhi was an elite bourgeois leader who would betray the revolution."
      ]
    },
    {
      "title": "Five-Point Critique of Orthodox Marxism",
      "scanPage": 52,
      "badge": "Philosophical Inversion",
      "summary": "While continuing to admire Marx's emancipatory passion, Roy systematically dismantled orthodox Marxist dogma.",
      "details": [
        "1. Historical Materialism: Marx grossly underestimated the autonomous, creative power of ideas in driving human history.",
        "2. Dialectical Materialism: Smuggled Hegelian teleology into nature; dialectics is idealist, not genuine materialist science.",
        "3. Class Struggle: Cohesion and social cooperation, not ceaseless class war, are the primary drivers of human survival and evolution.",
        "4. Surplus Value: Surplus value itself is essential for social reinvestment; the evil lies solely in unequal distribution.",
        "5. Nature of Revolution: True revolution requires changing the 'mode of thinking' (a mental, cultural renaissance), not merely the 'mode of production'."
      ]
    },
    {
      "title": "Radical Humanism: Freedom, Reason, Ethics",
      "scanPage": 54,
      "badge": "Philosophical Synthesis",
      "summary": "Roy defined 'Radical' in its etymological root: Man as the supreme, sovereign measure of all things.",
      "details": [
        "Freedom: Integral emancipation from poverty, fear, state terror, and supernatural religious superstitions.",
        "Reason: Has biological origins in man's evolutionary struggle for survival; provides the universal foundation for human solidarity.",
        "Ethics: Grounded in secular, existential human reason; ethics requires neither divine scriptures nor God."
      ]
    },
    {
      "title": "Partyless Democracy & The People's Plan (1944)",
      "scanPage": 55,
      "badge": "Institutional Blueprint",
      "summary": "Roy repudiated representative parliamentary democracy as an oligarchical fraud and proposed decentralized grassroots democracy.",
      "details": [
        "Critique of Parties: Political parties pursue power through corruption and demagoguery. In 1948, Roy disbanded his own Radical Democratic Party.",
        "Radical Democracy: Direct democracy through local People's Committees (*Lok Samitis*) exercising initiative, referendum, and recall.",
        "People's Plan (1944): A 10-year reconstruction blueprint prioritizing agricultural development, consumer goods, and cooperative socialized ownership."
      ]
    }
  ]
}

# Section 11: Dr. B.R. Ambedkar: Subaltern Emancipation, Caste Annihilation & Endogamy (Pages 57 to 64)
sec_ambedkar_caste = {
  "id": "modern-ipt-ambedkar-caste",
  "number": "11",
  "title": "Dr. B.R. Ambedkar: Subaltern Emancipation, Caste Annihilation & Endogamy",
  "subtitle": "Arun Shourie vs Christophe Jaffrelot | Broken Men Hypothesis | Division of Labourers | Twin Pillars of Endogamy & Purity-Pollution",
  "scanPages": [57, 58, 59, 60, 61, 62, 63, 64],
  "notebookPages": "Pages 27 to 30",
  "lecture": "Lecture 55 (22/02/2017)",
  "keyScholars": [
    "Dr. B.R. Ambedkar (1891–1956)",
    "Christophe Jaffrelot",
    "Arun Shourie ('Worshipping False Gods')",
    "Dhananjay Keer (Biographer)",
    "Jyotiba Phule",
    "Prof. M.N. Srinivas (Sanskritisation)"
  ],
  "coreTheories": [
    "Subaltern Emancipation & Leadership of the Bahujan Samaj",
    "Jaffrelot's Defense against Arun Shourie's 'Anti-National' Allegations",
    "Jyotiba Phule's Legacy: British Rule vs Peshwa Raj",
    "Critique of the Myth of India as an Existing Nation",
    "Anthropological Origin of Shudras ('Who Were the Shudras?')",
    "The 'Broken Men' Hypothesis & Origin of Untouchability",
    "Caste as 'Division of Labourers' (Annihilation of Caste 1936)",
    "Twin Pillars of Brahmanism: Endogamy & Ritual Purity-Pollution",
    "Dietary Shift: Vegetarianism as Brahmin Strategy of Exclusivity",
    "The Imperative to 'Dynamite' Hindu Shastras (Manusmriti Dahan 1927)"
  ],
  "concepts": [
    {
      "title": "Subaltern Agency & The Nationalism Controversy",
      "scanPage": 57,
      "badge": "Subaltern Historiography",
      "summary": "Ambedkar prioritized the dignity and survival of the depressed classes over elite-dominated political independence.",
      "details": [
        "Arun Shourie's Critique: Accused Ambedkar of collaboration with the British, opposing Quit India, and demanding separate electorates.",
        "Christophe Jaffrelot's Defense: Absurd to label Ambedkar anti-national; he represented the *Bahujan Samaj* (the vast demographic majority consisting of Dalits, Shudras, Tribals, and workers).",
        "Nationalism as Elite Weapon: Ambedkar showed how upper-caste elites used nationalism to delegitimize subaltern protests against caste oppression."
      ]
    },
    {
      "title": "Origin of Untouchability: The 'Broken Men' Hypothesis",
      "scanPage": 61,
      "badge": "Historical Sociology",
      "summary": "Ambedkar rejected divine origins of caste (Rigveda's Purushasukta), presenting a historical-materialist explanation.",
      "details": [
        "Broken Men: Pastoral tribes in conflict produced displaced, defeated groups ('broken men') who guarded the periphery of settled villages.",
        "Buddhism and Beef-Eating: These peripheral broken men adhered to Buddhism and continued eating carrion/beef, leading Brahmins to treat them as untouchable outcasts."
      ]
    },
    {
      "title": "Caste as Division of Labourers: Annihilation of Caste (1936)",
      "scanPage": 61,
      "badge": "Master Thesis",
      "summary": "Ambedkar shattered the defense that caste is merely a benign, functional division of labour.",
      "details": [
        "Division of Labourers: Caste is not merely division of labour; it is a graded, hierarchical division of labourers into water-tight compartments based on birth, destroying economic mobility and dignity.",
        "Dynamiting the Shastras: Caste cannot be reformed from within because it is religiously sanctified by the Shastras. One must put dynamite on Vedas and Smritis."
      ]
    },
    {
      "title": "Deconstructing Brahmanism: Endogamy & Sanskritisation",
      "scanPage": 63,
      "badge": "Structural Sociology",
      "summary": "Ambedkar identified endogamy (in-group marriage) as the central mechanism preserving the caste order.",
      "details": [
        "Endogamy: Castes maintain purity through strict prohibition of inter-marriage. Inter-caste dining and inter-marriage are essential to destroy caste.",
        "Purity and Pollution: Brahmins adopted strict vegetarianism to assert moral superiority over beef-eating Buddhists, launching the dynamic M.N. Srinivas termed Sanskritisation."
      ]
    }
  ]
}

# Section 12: The Historic Gandhi-Ambedkar Debate & Transition to National Movement (Pages 65 to 72)
sec_ambedkar_gandhi = {
  "id": "modern-ipt-ambedkar-gandhi",
  "number": "12",
  "title": "The Historic Gandhi-Ambedkar Debate & Early Nationalist Strategy",
  "subtitle": "Varna vs Caste | Harijan vs Dalit & The Putana Allegory | Village Republics vs Den of Ignorance | Poona Pact (1932) | Constitutionalism of Moderates",
  "scanPages": [65, 66, 67, 68, 69, 70, 71, 72],
  "notebookPages": "Pages 31 to 34",
  "lecture": "Lecture 55 & 56 (22/02/2017 & 23/02/2017)",
  "keyScholars": [
    "Dr. B.R. Ambedkar",
    "Mahatma Gandhi",
    "Arundhati Roy ('The Doctor and the Saint')",
    "Bal Gangadhar Tilak",
    "Sri Aurobindo Ghosh",
    "Gopal Krishna Gokhale",
    "Prof. Bipin Chandra"
  ],
  "coreTheories": [
    "Varna (Ideal/Textual) vs Caste (Real/Contextual)",
    "Gandhi's Performative Contradiction (Vaishya acting as Brahmin/Kshatriya)",
    "'Harijan' vs 'Dalit': Ambedkar's Rejection of Paternalistic Nomenclature",
    "Harijan Sevak Sangh Critique: The 'Putana' Allegory of Poisoned Milk",
    "Village Republics: Romanticized Gram Swaraj vs 'Den of Localism & Ignorance'",
    "Poona Pact (1932): Separate Electorates vs Reserved Seats & Fast Unto Death",
    "Exit to Navayana Buddhism (1956) as Rejection of Inequality",
    "Ambedkar vs Marx: Inversion of Historical Materialism & Defense of Democratic State",
    "Early Nationalist Movement: Moderates' 3Ps (Prayer, Petition, Protest)",
    "Tilak's Critique ('Constitutionalism before Alien Bureaucracy is Political Suicide')",
    "Aurobindo's Critique ('Intellectual Bankruptcy of Moderates')"
  ],
  "concepts": [
    {
      "title": "Varna vs Caste & Gandhi's Performative Contradiction",
      "scanPage": 65,
      "badge": "Ideological Clash",
      "summary": "Ambedkar criticized Gandhi's defense of the ideal Varna system as completely divorced from the brutal reality of caste.",
      "details": [
        "Textual vs Contextual: Gandhi defended Varna as an ideal division of labour based on worth; Ambedkar showed caste in practice is based strictly on birth and untouchability.",
        "Gandhi's Contradiction: Gandhi himself, born into a Vaishya trader caste, acted as political ruler (Kshatriya) and moral teacher (Brahmin), violating the very Varna dharma he defended."
      ]
    },
    {
      "title": "The 'Harijan' Term & The Putana Allegory",
      "scanPage": 65,
      "badge": "Nomenclature & Patronage",
      "summary": "Ambedkar vehemently rejected Gandhi's patronizing term 'Harijan' ('children of God') and his Harijan Sevak Sangh.",
      "details": [
        "Harijan Rejected: Term was condescending; Dalits were not favored by God, but were the most oppressed members of Hindu society.",
        "The Putana Allegory: Ambedkar compared Gandhi's Harijan Sevak Sangh to the mythological demoness Putana, who sought to kill infant Krishna by offering poisoned milk disguised as maternal care—soothing Dalits to keep them within the oppressive Hindu fold."
      ]
    },
    {
      "title": "The Village Question: Gram Swaraj vs. Den of Ignorance",
      "scanPage": 66,
      "badge": "Spatial Sociological Divide",
      "summary": "One of the most profound divides in modern Indian thought concerns the moral character of the Indian village.",
      "details": [
        "Gandhi's Gram Swaraj: Revered the Indian village as an idyllic, self-sufficient, harmonious republic of moral virtue.",
        "Ambedkar's Indictment: Declared in the Constituent Assembly: 'What is a village but a sink of localism, a den of ignorance, narrow-mindedness, and communalism?' The village ghettoizes Dalits; only modern cities and the constitutional state offer emancipation."
      ]
    },
    {
      "title": "Ambedkar vs. Karl Marx: Ideology as Basic Structure",
      "scanPage": 67,
      "badge": "Theoretical Divergence",
      "summary": "Ambedkar agreed with Marx on the evil of exploitation, but inverted Marxian historical materialism.",
      "details": [
        "Ideological Superstructure as Base: In India, Brahmanical religious ideology is the real basic structure; economic restructuring alone cannot liberate Dalits without destroying caste consciousness.",
        "Role of the State: While Marx saw the state as an executive committee of the bourgeoisie, Ambedkar saw the constitutional democratic state as the vital instrument for social reform and rights."
      ]
    },
    {
      "title": "Early National Movement: Moderates vs Extremist Critique",
      "scanPage": 71,
      "badge": "Nationalist Historiography",
      "summary": "The early phase of the National Movement was dominated by constitutional Moderates, fiercely criticized by Extremists.",
      "details": [
        "Moderates' 3Ps: Reliance on Prayer, Petition, and Protest; belief in British providential mission and fair play.",
        "Tilak's Verdict: 'Constitutionalism in front of an alien bureaucracy is political suicide.' Swaraj is my birthright and I shall have it.",
        "Aurobindo's Verdict: Denounced Moderate politics as 'intellectual bankruptcy' and 'mendicant politics' in his famous essays 'New Lamps for Old'."
      ]
    }
  ]
}

# Section 13: Indian National Movement: Bipin Chandra & Gandhian Mass Movement Strategy (Pages 73 to 80)
sec_national_movement = {
  "id": "modern-igp-national-movement",
  "number": "13",
  "title": "Indian National Movement: Bipin Chandra & Gandhian Mass Movement Strategy",
  "subtitle": "Bipin Chandra's Master Thesis | War of Position vs Maneuver | Struggle-Truce-Struggle (S-T-S) | Non-Cooperation & Civil Disobedience",
  "scanPages": [73, 74, 75, 76, 77, 78, 79, 80],
  "notebookPages": "Pages 35 to 38",
  "lecture": "Lecture 56 (23/02/2017)",
  "keyScholars": [
    "Prof. Bipin Chandra ('India's Struggle for Independence')",
    "Mahatma Gandhi",
    "Antonio Gramsci (War of Position Concept)",
    "Henry David Thoreau",
    "Bal Gangadhar Tilak",
    "Jawaharlal Nehru",
    "M.N. Roy"
  ],
  "coreTheories": [
    "Bipin Chandra's Evaluation of Moderates: Economic Critique & Ideological Foundation",
    "Extremist Phase: Lal-Bal-Pal, Tilak's 'Praja Droh', British Regressive Acts",
    "Unique Features of Indian National Movement: Largest Protracted Mass Struggle",
    "Gramscian Framework: War of Position against the Semi-Hegemonic Colonial State",
    "Struggle-Truce-Struggle (S-T-S) vs Struggle-Victory (S-V) Strategy",
    "Master Psychologist: Gandhi's Recognition of Mass Exhaustion Limits",
    "Non-Cooperation Movement (1920–22): Nagpur Session, Swaraj in 1 Year, Chauri Chaura",
    "Civil Disobedience Movement (1930–31): Thoreau's Influence, 11-Point Demands & Dandi Salt March"
  ],
  "concepts": [
    {
      "title": "Bipin Chandra's Evaluation of the Moderates",
      "scanPage": 73,
      "badge": "Historiographical Defense",
      "summary": "Bipin Chandra defended early Moderates against charges of cowardice, demonstrating they laid the indispensable intellectual foundations of Indian nationalism.",
      "details": [
        "Economic Drain Theory: Dadabhai Naoroji, R.C. Dutt, and Ranade thoroughly dismantled the colonial myth of the 'civilizing mission' by exposing colonial economic exploitation.",
        "Ranade's Insight: Memorials were ostensibly addressed to the British government, but were really meant to educate and awaken the Indian masses.",
        "Gokhale's Dedication: 'Let us serve India through our failures'—early failures built the institutional capacity for subsequent mass mobilization."
      ]
    },
    {
      "title": "Gandhian Mass Movement Strategy: Gramscian War of Position",
      "scanPage": 75,
      "badge": "Gramscian Framework",
      "summary": "The Indian National Movement was a protracted, controlled mass movement fighting a semi-hegemonic colonial state.",
      "details": [
        "War of Position: The British ruled not purely by brute force, but through manufactured hegemony (rule of law, English education, benevolent despotism). Gandhi fought a protracted War of Position to dismantle British moral legitimacy.",
        "Master Psychologist: Gandhi recognized that the masses cannot fight indefinitely at peak intensity. Movements were called off at opportune moments before exhaustion and state repression broke mass morale."
      ]
    },
    {
      "title": "Struggle-Truce-Struggle (S-T-S) Strategy",
      "scanPage": 76,
      "badge": "Grand Strategic Cycle",
      "summary": "Gandhian strategy alternated between phases of vigorous extra-legal mass struggle and phases of constitutional truce.",
      "details": [
        "The S-T-S Cycle: Struggle (Active mass mobilization) -> Truce (Consolidation through Constructive Programme: khadi, Harijan uplift, national education) -> Struggle (Higher phase).",
        "Contrast with Marxist S-V: Marxists advocate Struggle-Victory (continuous escalation until state collapse); Gandhi knew this would invite crushing colonial violence against unarmed masses."
      ]
    },
    {
      "title": "Non-Cooperation vs. Civil Disobedience Movement",
      "scanPage": 80,
      "badge": "Tactical Comparison",
      "summary": "Gandhi calibrated each successive mass movement with increasing offensive pressure against the colonial state.",
      "details": [
        "Non-Cooperation (1920–22): Mild and defensive; targeted the economic base and administrative cooperation (boycotting schools, courts, titles, foreign clothes).",
        "Civil Disobedience (1930–31): Highly offensive; directly violated colonial laws (salt laws, forest laws, no-revenue campaigns), placing Congress on equal diplomatic footing with the British Crown (Gandhi-Irwin Pact 1931).",
        "11-Point Demands: Addressed all social classes (salt tax abolition, 50% military spending cut, 50% land revenue cut, protective tariffs, release of political prisoners)."
      ]
    }
  ]
}

# Combine all sections
data['sections'] = base_sections + [
    sec_sir_syed,
    sec_aurobindo,
    sec_gandhi_core,
    sec_gandhi_state,
    sec_mn_roy,
    sec_ambedkar_caste,
    sec_ambedkar_gandhi,
    sec_national_movement
]

print("Total sections compiled:", len(data['sections']))

# Let's write this back to app/src/data/paper1IptData.js safely
with open('app/src/data/paper1IptData.js', 'w', encoding='utf-8') as f:
    f.write('export const paper1IptData = ' + json.dumps(data, indent=2) + ';\n')

print("paper1IptData.js successfully written with 13 comprehensive sections!")
