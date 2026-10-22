# scripts/enrich_paper1_features.py
import json

print("Reading paper1IptData.js...")
with open('app/src/data/paper1IptData.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = 'export const paper1IptData = '
js_obj = text[len(prefix):].rstrip(';\n')
data = json.loads(js_obj)

# 1. Update Mindmap Data
data['mindmap'] = [
  {
    "id": "root-ipt",
    "label": "PSIR Paper 1 Master Knowledge Graph",
    "color": "from-amber-500 to-indigo-600",
    "children": [
      {
        "id": "branch-ancient-ipt",
        "label": "Ancient Indian Political Thought",
        "color": "from-amber-600 to-orange-700",
        "children": [
          {
            "id": "mm-manu",
            "label": "Manu & Manusmriti",
            "children": [
              { "id": "mm-manu-origin", "label": "Quasi-Contract & Matsyanyaya" },
              { "id": "mm-manu-danda", "label": "Divine Personality & Danda" },
              { "id": "mm-manu-varna", "label": "Varna Dharma & Graded Inequality" }
            ]
          },
          {
            "id": "mm-kautilya",
            "label": "Kautilya's Arthashastra",
            "children": [
              { "id": "mm-k-saptanga", "label": "Saptanga Organic State (7 Limbs)" },
              { "id": "mm-k-mandala", "label": "Mandala Geopolitics (12 Kings)" },
              { "id": "mm-k-upayas", "label": "4 Upayas & 6-Fold Shadgunya Niti" },
              { "id": "mm-k-corruption", "label": "40 Modes of Corruption (Honey on Tongue)" },
              { "id": "mm-k-machiavelli", "label": "Kautilya vs Machiavelli (Weber 1919)" }
            ]
          },
          {
            "id": "mm-buddha",
            "label": "Buddhist Political Thought",
            "children": [
              { "id": "mm-b-metaphysics", "label": "Anicca, Anatta, Dukkha" },
              { "id": "mm-b-contract", "label": "Agganna Sutta & Mahasammata Social Contract" },
              { "id": "mm-b-dhamma", "label": "Ashokan Dhamma vs Kautilyan Danda" },
              { "id": "mm-b-sangha", "label": "Deliberative Sangha Democracy" }
            ]
          }
        ]
      },
      {
        "id": "branch-modern-ipt",
        "label": "Modern Indian Political Thought",
        "color": "from-blue-600 to-indigo-800",
        "children": [
          {
            "id": "mm-sir-syed",
            "label": "Sir Syed Ahmed Khan",
            "children": [
              { "id": "mm-ss-context", "label": "Post-1857 Trauma & MAO College" },
              { "id": "mm-ss-rationalism", "label": "Scientific Temper & Tahzib-ul-Akhlaq" },
              { "id": "mm-ss-politics", "label": "From 'Two Eyes of Bride' to Two-Nation Genesis" }
            ]
          },
          {
            "id": "mm-aurobindo",
            "label": "Sri Aurobindo Ghosh",
            "children": [
              { "id": "mm-a-nationalism", "label": "Nation as Living Mother (Bhavani Bharati)" },
              { "id": "mm-a-moderates", "label": "Critique in 'New Lamps for Old' & Swaraj" },
              { "id": "mm-a-passive-res", "label": "Doctrine of 4-Fold Passive Resistance" },
              { "id": "mm-a-yoga", "label": "Integral Yoga (Purna Yoga) & Supermind" }
            ]
          },
          {
            "id": "mm-gandhi",
            "label": "Mahatma Gandhi",
            "children": [
              { "id": "mm-g-satyagraha", "label": "Ahimsa as Active Love & Satyagraha Soul-Force" },
              { "id": "mm-g-swaraj", "label": "Four Dimensions of Swaraj" },
              { "id": "mm-g-hind-swaraj", "label": "Hind Swaraj (1909) Modernity Critique" },
              { "id": "mm-g-state", "label": "Philosophical Anarchism & Oceanic Circles" },
              { "id": "mm-g-trusteeship", "label": "Trusteeship & Bread Labour" },
              { "id": "mm-g-ends-means", "label": "Seed & Tree (Ends-Means Organic Unity)" }
            ]
          },
          {
            "id": "mm-ambedkar",
            "label": "Dr. B.R. Ambedkar",
            "children": [
              { "id": "mm-amb-subaltern", "label": "Bahujan Samaj & Jaffrelot vs Shourie" },
              { "id": "mm-amb-caste", "label": "Division of Labourers & Broken Men" },
              { "id": "mm-amb-brahmanism", "label": "Twin Pillars: Endogamy & Purity-Pollution" },
              { "id": "mm-amb-gandhi-debate", "label": "Debate on Varna, Harijan, Villages & Poona Pact" },
              { "id": "mm-amb-marx", "label": "Inversion of Marx & Constitutional Morality" }
            ]
          },
          {
            "id": "mm-mn-roy",
            "label": "M.N. Roy",
            "children": [
              { "id": "mm-roy-odyssey", "label": "Revolutionary -> Comintern (Lenin Debate 1920)" },
              { "id": "mm-roy-marxism", "label": "5-Point Critique of Marxism (Ideas vs Production)" },
              { "id": "mm-roy-humanism", "label": "Radical Humanism: Freedom, Reason, Ethics" },
              { "id": "mm-roy-democracy", "label": "Partyless Democracy & People's Plan 1944" }
            ]
          }
        ]
      },
      {
        "id": "branch-national-movement",
        "label": "Indian National Movement (Bipin Chandra)",
        "color": "from-emerald-600 to-teal-800",
        "children": [
          { "id": "mm-nm-moderates", "label": "Moderates' Drain of Wealth & 3Ps" },
          { "id": "mm-nm-extremists", "label": "Extremists: Tilak's Praja Droh & Aurobindo" },
          { "id": "mm-nm-strategy", "label": "Gandhian S-T-S vs S-V Strategy" },
          { "id": "mm-nm-gramsci", "label": "Gramscian War of Position against Raj" },
          { "id": "mm-nm-ncm", "label": "Non-Cooperation Movement (1920–22)" },
          { "id": "mm-nm-cdm", "label": "Civil Disobedience & 11 Demands (1930–31)" },
          { "id": "mm-nm-quit-india", "label": "Quit India 1942: Most Un-Gandhian Movement" }
        ]
      }
    ]
  }
]

# 2. Add 25+ New High-Yield Flashcards (making 50+ total)
new_flashcards = [
  {
    "id": "fc-25",
    "category": "Sir Syed",
    "front": "What was Sir Syed Ahmed Khan's 'Two Beautiful Eyes of a Bride' metaphor, and why did it shift?",
    "back": "Early in his life, Sir Syed described Hindus and Muslims as the 'two beautiful eyes of a lovely bride' (India), where harming one disfigures the other. However, following the 1867 Hindi-Urdu controversy in UP and the 1885 founding of the Congress, he feared Western majoritarian democracy would reduce Muslims to permanent subjugation under Hindu numerical dominance.",
    "mnemonic": "Two Eyes -> Minority Survival -> Two-Nation Genesis",
    "scanPage": 30,
    "badge": "Communal Thought"
  },
  {
    "id": "fc-26",
    "category": "Aurobindo",
    "front": "How did Sri Aurobindo define the Indian Nation in his spiritual theory of nationalism?",
    "back": "Sri Aurobindo rejected the Western territorial/contractual concept of a nation. For him, India is not a piece of land, but a living divine spirit and Mother—Bhavani Bharati (*Atma* of the collectivity). Nationalism is not a political game, but a profound religion and spiritual sadhana.",
    "mnemonic": "India is Bhavani Bharati (Living Mother)",
    "scanPage": 31,
    "badge": "Spiritual Nationalism"
  },
  {
    "id": "fc-27",
    "category": "Aurobindo",
    "front": "What was Aurobindo's critique of the Moderates in 'New Lamps for Old' (1893)?",
    "back": "In 'New Lamps for Old' (Induprakash), Aurobindo denounced Moderate politics as 'politics of mendicancy' and intellectual bankruptcy. He argued their 'prayers, petitions, and protests' were barking without biting, and demanded complete independence (Poorna Swaraj) as an absolute end in itself.",
    "mnemonic": "New Lamps for Old = Mendicancy & Blindness",
    "scanPage": 33,
    "badge": "Radical Critique"
  },
  {
    "id": "fc-28",
    "category": "Aurobindo",
    "front": "What are the four components of Aurobindo's Doctrine of Passive Resistance?",
    "back": "1. Economic Boycott of British foreign goods (Swadeshi).\n2. Educational Boycott of government schools (National Education).\n3. Judicial Boycott of British courts (People's Arbitration Courts).\n4. Executive/Administrative Boycott of civil offices.",
    "mnemonic": "EEJE (Economy, Education, Judiciary, Executive)",
    "scanPage": 35,
    "badge": "Boycott Strategy"
  },
  {
    "id": "fc-29",
    "category": "Aurobindo",
    "front": "How did Aurobindo's view of non-violence differ from Mahatma Gandhi's?",
    "back": "Aurobindo viewed non-violence as a strategic policy and tactical weapon that could be discarded in favor of armed resistance if British oppression exceeded endurance. Gandhi viewed Ahimsa as an inviolable, universal creed and moral religion that could never be compromised under any circumstances.",
    "mnemonic": "Aurobindo: Policy/Strategy | Gandhi: Moral Creed/Religion",
    "scanPage": 35,
    "badge": "Crucial Distinction"
  },
  {
    "id": "fc-30",
    "category": "Aurobindo",
    "front": "Explain Aurobindo's concept of Integral Yoga (Purna Yoga) and the Supermind.",
    "back": "Integral Yoga synthesizes Karma, Jnana, Bhakti, Raja, and Hatha Yoga. Rather than escaping the world to seek individual Moksha, its goal is the descent of the Supramental divine consciousness into physical matter to divinize human life on Earth.",
    "mnemonic": "Ascent to Supermind + Descent into Matter",
    "scanPage": 38,
    "badge": "Cosmic Yoga"
  },
  {
    "id": "fc-31",
    "category": "Gandhi",
    "front": "Why did Gandhi declare that 'Ahimsa is the weapon of the brave'?",
    "back": "Ahimsa requires mastering fear, anger, and ego. It is not cowardice; non-violence out of fear is unnatural. Gandhi declared: 'Where there is only a choice between cowardice and violence, I would advise violence.' True Ahimsa comes from supreme moral and spiritual strength (*Atma-Bal*).",
    "mnemonic": "Courage > Cowardice | Non-violence = Active Love",
    "scanPage": 40,
    "badge": "Moral Core"
  },
  {
    "id": "fc-32",
    "category": "Gandhi",
    "front": "What are the four integral dimensions of Gandhian Swaraj?",
    "back": "1. Political Swaraj: National independence & decentralized village republics.\n2. Economic Swaraj: Khadi, cottage self-reliance, and eradication of poverty.\n3. Social Swaraj: Eradication of untouchability, communal harmony & gender dignity.\n4. Moral/Atma-Swaraj: Mastery over one's own senses and passions (true self-rule).",
    "mnemonic": "PESM: Political, Economic, Social, Moral",
    "scanPage": 41,
    "badge": "Swaraj Matrix"
  },
  {
    "id": "fc-33",
    "category": "Gandhi",
    "front": "Why did Gandhi attack modern civilization in Hind Swaraj (1909)?",
    "back": "Gandhi argued modern Western civilization was purely materialistic, elevating bodily appetites while starving the human soul. He attacked the British Parliament as a 'sterile woman and prostitute', denounced modern lawyers and doctors for encouraging litigation and physical indulgence, and warned against machine industrialism.",
    "mnemonic": "Hind Swaraj: Material Appetite vs Soul-Mastery",
    "scanPage": 43,
    "badge": "Civilisational Critique"
  },
  {
    "id": "fc-34",
    "category": "Gandhi",
    "front": "Explain Gandhi's vision of 'Oceanic Circles of Power'.",
    "back": "Gandhi rejected top-down pyramidal state hierarchies. In his envisioned society, life is an oceanic circle with the individual at the center, expanding outward into village republics. Each circle blends harmoniously into the wider commonwealth without dominating or exploiting another.",
    "mnemonic": "No Hierarchical Pyramid | Ever-expanding Oceanic Circle",
    "scanPage": 47,
    "badge": "Decentralized State"
  },
  {
    "id": "fc-35",
    "category": "Gandhi",
    "front": "What is Gandhi's Doctrine of Trusteeship?",
    "back": "Gandhi held that capitalists must consider themselves moral trustees of society's wealth. Because wealth is produced socially, owners should take only what is needed for personal maintenance and hold the rest for the welfare of workers and the community, avoiding violent class war.",
    "mnemonic": "Capital as Social Trust | Rejection of Class War",
    "scanPage": 45,
    "badge": "Political Economy"
  },
  {
    "id": "fc-36",
    "category": "Gandhi",
    "front": "Explain the organic unity of Ends and Means in Gandhian thought.",
    "back": "Gandhi insisted that means and ends are organically convertible like seed and tree: 'As is the seed, so is the tree. One cannot sow the seed of babul and reap rose flowers.' Using unethical or violent means corrupts the final end achieved, completely repudiating Machiavellian realpolitik.",
    "mnemonic": "Seed = Means | Tree = End",
    "scanPage": 48,
    "badge": "Sadhan-Sadhya"
  },
  {
    "id": "fc-37",
    "category": "M.N. Roy",
    "front": "What was the famous 1920 Lenin-Roy debate at the 2nd Comintern Congress?",
    "back": "Lenin argued that the Communist International must support bourgeois nationalist movements (like Gandhi's INC) in colonial countries. Roy countered in his Supplementary Theses that the colonial bourgeoisie would compromise with imperialism, and that communists must directly support autonomous worker and peasant struggles.",
    "mnemonic": "Lenin: Support Bourgeois INC | Roy: Direct Worker/Peasant Movement",
    "scanPage": 51,
    "badge": "Comintern Debate"
  },
  {
    "id": "fc-38",
    "category": "M.N. Roy",
    "front": "What are M.N. Roy's five core critiques of orthodox Marxism?",
    "back": "1. Historical Materialism: Grossly underestimated the power of ideas.\n2. Dialectical Materialism: Smuggled Hegelian teleology/idealism into physical nature.\n3. Class Struggle: Social cooperation, not class war, drives human history.\n4. Surplus Value: Surplus is essential for progress; the flaw is distribution.\n5. Theory of Revolution: Requires changing the 'mode of thinking' (mental revolution), not just the 'mode of production'.",
    "mnemonic": "Ideas, Dialectics, Cooperation, Surplus, Mental Revolution",
    "scanPage": 52,
    "badge": "Marxist Critique"
  },
  {
    "id": "fc-39",
    "category": "M.N. Roy",
    "front": "What are the three pillars of M.N. Roy's Radical Humanism?",
    "back": "1. Freedom: Absolute emancipation from state terror, economic want, and religious superstition.\n2. Reason: Biological attribute developed in man's evolutionary struggle for survival; universal ground of human solidarity.\n3. Ethics: Secular, existential moral values grounded in reason, independent of divine scriptures.",
    "mnemonic": "FRE: Freedom, Reason, Ethics",
    "scanPage": 54,
    "badge": "Radical Humanism"
  },
  {
    "id": "fc-40",
    "category": "Ambedkar",
    "front": "Why did Christophe Jaffrelot defend Ambedkar against Arun Shourie's anti-national charge?",
    "back": "Arun Shourie accused Ambedkar of being anti-national for collaborating with the British Viceroy's council and opposing Quit India. Jaffrelot defended Ambedkar, proving he was the authentic leader of the *Bahujan Samaj* (Dalits, Shudras, Tribals, workers)—the overwhelming demographic majority of India. Working for the majority cannot be called anti-national.",
    "mnemonic": "Shourie: Elite Nationalist | Jaffrelot: Majority Bahujan Leader",
    "scanPage": 58,
    "badge": "Historiographical Defense"
  },
  {
    "id": "fc-41",
    "category": "Ambedkar",
    "front": "Explain Ambedkar's 'Broken Men' hypothesis on the origin of Untouchability.",
    "back": "Ambedkar rejected divine origin theories. He theorized that in ancient tribal warfare, defeated and shattered clan members ('broken men') settled on the outskirts of agrarian villages as guards. Because they adhered to Buddhism and ate beef/carrion, they were ostracized by Brahmins as untouchables.",
    "mnemonic": "Broken Men = Tribal Outcasts + Buddhism + Beef-Eating",
    "scanPage": 61,
    "badge": "Untouchability Origin"
  },
  {
    "id": "fc-42",
    "category": "Ambedkar",
    "front": "Why did Ambedkar declare that caste is a 'division of labourers'?",
    "back": "In *Annihilation of Caste* (1936), Ambedkar refuted the apology that caste is merely a functional division of labour. He demonstrated that caste is a graded, involuntary division of *labourers*, locking individuals into hereditary professions regardless of aptitude and subordinating one worker to another.",
    "mnemonic": "Division of Labourers (Not Division of Labour)",
    "scanPage": 61,
    "badge": "Master Concept"
  },
  {
    "id": "fc-43",
    "category": "Ambedkar",
    "front": "What are the twin pillars of Brahmanism according to Dr. Ambedkar?",
    "back": "1. Endogamy: Compulsory marriage within one's own sub-caste, which created artificial enclosures and prevented social fusion.\n2. Ritual Purity and Pollution: Reinforced by dietary taboos (Brahmins renouncing beef and embracing strict vegetarianism to assert ritual supremacy over lower castes).",
    "mnemonic": "Endogamy + Purity/Pollution Hierarchy",
    "scanPage": 63,
    "badge": "Sociological Pillars"
  },
  {
    "id": "fc-44",
    "category": "Gandhi vs Ambedkar",
    "front": "What was Ambedkar's critique of the Indian village compared to Gandhi's Gram Swaraj?",
    "back": "Gandhi idolized the Indian village as a self-sufficient, harmonious moral republic of *Gram Swaraj*. Ambedkar denounced the Indian village in the Constituent Assembly as 'a sink of localism, a den of ignorance, narrow-mindedness, and communalism', arguing it held Dalits in perpetual servitude.",
    "mnemonic": "Gandhi: Moral Republic | Ambedkar: Den of Localism & Ignorance",
    "scanPage": 66,
    "badge": "Spatial Divide"
  },
  {
    "id": "fc-45",
    "category": "Gandhi vs Ambedkar",
    "front": "Why did Ambedkar use the mythological 'Putana' allegory for Gandhi's Harijan Sevak Sangh?",
    "back": "Ambedkar compared the Harijan Sevak Sangh to the demoness Putana, who sought to kill baby Krishna with poisoned milk under the guise of maternal love. He argued Gandhi's organization was managed by upper-caste Hindus to offer paternalistic charity and distract Dalits from demanding structural political power.",
    "mnemonic": "Putana = Poisoned Milk of Upper-Caste Charity",
    "scanPage": 65,
    "badge": "Subaltern Critique"
  },
  {
    "id": "fc-46",
    "category": "National Movement",
    "front": "What is Bipin Chandra's Struggle-Truce-Struggle (S-T-S) thesis of Gandhian strategy?",
    "back": "Bipin Chandra showed that Gandhi understood the psychological limit of mass endurance; masses cannot participate in active street protest indefinitely. Gandhi utilized the S-T-S strategy: active mass confrontation (Struggle), followed by a strategic pause (Truce) filled with constructive socio-economic work, leading to a higher phase of Struggle.",
    "mnemonic": "S-T-S: Struggle -> Truce -> Higher Struggle",
    "scanPage": 76,
    "badge": "Grand Strategy"
  },
  {
    "id": "fc-47",
    "category": "National Movement",
    "front": "How does Antonio Gramsci's 'War of Position' explain the Indian National Movement?",
    "back": "The British colonial state ruled through manufactured semi-hegemony ('Rule of Law', benevolent administration). In a Gramscian sense, Gandhi fought a protracted War of Position across the trenches of civil society to undermine the moral legitimacy of the Raj before launching decisive mass movements.",
    "mnemonic": "Gramsci: War of Position dismantles Hegemony",
    "scanPage": 75,
    "badge": "Theoretical Analogy"
  },
  {
    "id": "fc-48",
    "category": "National Movement",
    "front": "Why is the Quit India Movement (1942) considered the 'most un-Gandhian' movement?",
    "back": "1. It abandoned gradualism with the uncompromising mantra 'Do or Die' (*Karo ya Maro*).\n2. Gandhi allowed the use of arms in self-defense against brute state violence.\n3. He refused to call off the movement despite widespread violent attacks on police stations and post offices, attributing violence to the Raj's 'leonine violence'.",
    "mnemonic": "Do or Die + Armed Self-Defense + No Withdrawal",
    "scanPage": 81,
    "badge": "Quit India"
  }
]

# Merge flashcards
data['flashcards'] = data['flashcards'] + new_flashcards

# 3. Add 4 New UPSC Mains Model Answers
new_answers = [
  {
    "id": "ans-p1-06",
    "year": "UPSC PSIR Paper 1 Section A (20 Marks)",
    "marks": 20,
    "question": "Critically evaluate Sri Aurobindo's concept of Passive Resistance and compare it with Gandhian Satyagraha.",
    "dimensions": [
      "Genealogy of Passive Resistance in Aurobindo's Thought",
      "The 4-Fold Boycott Structure (Economic, Educational, Judicial, Executive)",
      "Aurobindo's Pragmatic/Instrumental Stance on Violence vs Gandhi's Moral Absolutism",
      "Satyagraha as Soul-Force (Atma-Bal) vs Weapon of Resistance",
      "Contemporary Relevance in Mass Protest Praxis"
    ],
    "structure": {
      "intro": "Sri Aurobindo Ghosh was among the earliest visionary leaders of the Extremist phase of the Indian National Movement to articulate a rigorous theory of direct mass action. Formulated in a series of articles in *Bande Mataram* in 1907 during the Anti-Partition agitation in Bengal, Aurobindo's 'Doctrine of Passive Resistance' provided the strategic blueprint that transitioned the national struggle from mendicant constitutionalism to aggressive extra-legal mobilization.",
      "body": "Aurobindo's passive resistance rested upon the structural insight that British imperial rule in India was maintained by the voluntary acquiescence and administrative collaboration of Indians themselves. If Indians refused to cooperate, the imperial edifice would collapse. His strategy outlined a comprehensive fourfold boycott: economic (Swadeshi), educational (national schools), judicial (people's arbitration courts), and executive/administrative (refusal to assist imperial taxation and police). However, the critical divergence between Aurobindo and Gandhi lies in the ontological status of non-violence. For Aurobindo, passive resistance was a strategic policy and pragmatic instrument. He explicitly recognized that if the state met peaceful boycott with unprovoked, brutal terror, citizens possessed the sovereign moral right to abandon passive resistance and adopt defensive violent resistance. In contrast, Mahatma Gandhi elevated Ahimsa to an inviolable metaphysical creed and moral religion. For Gandhi, Satyagraha is soul-force (*Atma-Bal*); it renounces all violence in thought, word, and deed, inviting self-suffering to melt the moral conscience of the adversary rather than coercing them.",
      "conclusion": "In sum, while Aurobindo's passive resistance was a tactical war of position designed to extract political independence (Poorna Swaraj), Gandhian Satyagraha was an existential spiritual hermeneutic aimed at transforming the human soul. Both strategies, however, permanently ruptured the illusion of British moral hegemony, laying the groundwork for mass non-cooperation.",
      "scholarQuotes": [
        "Aurobindo: 'Under certain circumstances a nation is justified in taking up arms for its freedom.'",
        "Gandhi: 'Satyagraha is soul-force pure and simple; where there is only a choice between cowardice and violence, I would advise violence, but non-violence is infinitely superior.'",
        "Bipan Chandra: 'Aurobindo provided the radical transition from the 3Ps of the Moderates to the mass direct action refined by Gandhi.'"
      ]
    }
  },
  {
    "id": "ans-p1-07",
    "year": "UPSC PSIR Paper 1 Section A (20 Marks)",
    "marks": 20,
    "question": "Examine the Gandhi-Ambedkar debate on Caste and the Village Republic. Whose vision has proved more durable in post-independence India?",
    "dimensions": [
      "Philosophical Foundations: Textual Varna (Gandhi) vs Contextual Division of Labourers (Ambedkar)",
      "The Village Question: Idyllic Gram Swaraj vs 'Den of Localism, Ignorance and Communalism'",
      "Methods of Emancipation: Moral Penitence (Harijan Sevak Sangh) vs Rights & Constitutional Morality",
      "Post-Colonial Trajectory: 73rd Amendment, Panchayati Raj, Urbanization & Dalit Emancipation"
    ],
    "structure": {
      "intro": "The ideological encounter between Mahatma Gandhi and Dr. B.R. Ambedkar represents the most profound internal debate within modern Indian social and political thought. As Arundhati Roy observed in *The Doctor and the Saint*, this confrontation pitted an enlightened moral reformism seeking to spiritualize tradition against a radical subaltern modernist demanding the structural annihilation of sacred hierarchies.",
      "body": "The debate hinged upon two irreconcilable axes: the nature of caste and the character of the Indian village. On caste, Gandhi drew a distinction between an idealized Varna system (which he defended as a natural, hereditary division of labour based on worth) and untouchability (which he condemned as a sinful excrescence on Hinduism). In stark contrast, Ambedkar demonstrated in *Annihilation of Caste* (1936) that caste is not a division of labour, but a graded 'division of labourers' sustained by endogamy and ritual purity. For Ambedkar, caste could not be reformed from within because it was sanctified by Hindu Shastras; hence, one had to 'dynamite the Vedas and Manusmriti'. On the spatial question of the village, Gandhi celebrated the village as a harmonious, self-reliant moral republic (*Gram Swaraj*). Ambedkar vehemently rejected this romanticization, declaring in the Constituent Assembly that the Indian village was 'a sink of localism, a den of ignorance, narrow-mindedness, and communalism' where Dalits were ghettoized on the periphery without basic civic dignity. Ambedkar insisted that true emancipation lay in urbanization, modern industrialization, and a centralized constitutional state guaranteeing fundamental civil rights.",
      "conclusion": "In independent India, both visions have demonstrated enduring yet tension-ridden relevance. Ambedkar's constitutional morality, affirmative action policies, and subaltern political assertion have become the bedrock of Dalit dignity and democracy. Meanwhile, 73rd Constitutional Amendment institutionalized Gandhian Panchayati Raj, yet empirical evidence across rural India confirms Ambedkar's warning that local dominant castes often weaponize local institutions unless counter-balanced by constitutional law. Thus, Ambedkar's modernist legal rights provide the indispensable shield, while Gandhi's moral fraternity provides the ultimate ethical goal for a caste-free society.",
      "scholarQuotes": [
        "Ambedkar: 'What is a village but a sink of localism, a den of ignorance, narrow-mindedness, and communalism?'",
        "Gandhi: 'If the village perishes, India will perish too.'",
        "Arundhati Roy: 'The debate between Gandhi and Ambedkar is not merely historical; it is a battle for the soul of contemporary India.'"
      ]
    }
  },
  {
    "id": "ans-p1-08",
    "year": "UPSC PSIR Paper 1 Section A (15 Marks)",
    "marks": 15,
    "question": "Explain M.N. Roy's critique of orthodox Marxism and elucidate his philosophy of Radical Humanism.",
    "dimensions": [
      "M.N. Roy's Intellectual Journey (Comintern to Radical Humanism)",
      "Five-Point Critique of Orthodox Marxism (Economic Determinism, Dialectics, Class War)",
      "The Triad of Radical Humanism: Reason, Freedom, Ethics",
      "Partyless Democracy (Lok Samitis) and Relevance Today"
    ],
    "structure": {
      "intro": "Manabendra Nath Roy (1887–1954), described by Sibnarayan Ray as the 'Erasmus of Modern India', occupies a unique position in global political philosophy. Having founded the Mexican Communist Party and debated Lenin at the 1920 Comintern Congress, Roy's intellectual evolution culminated in a complete philosophical departure from orthodox Marxism toward Radical Humanism (or New Humanism).",
      "body": "Roy's break with Marxism was rooted in an epistemology that rejected economic determinism. He presented a five-fold critique: first, historical materialism underestimated the autonomous power of ideas, whereas human history is driven primarily by ideational revolutions; second, dialectical materialism was an unscientific teleological relic of Hegelian idealism; third, class struggle was an oversimplified dogma, since social cooperation and mutual aid are the primary biological drivers of human evolution; fourth, surplus value is essential for civilizational progress, and exploitation lies in unequal distribution rather than the surplus itself; and fifth, genuine revolution requires changing the 'mode of thinking' (a philosophical renaissance) rather than merely changing the 'mode of production'. In place of Marxism, Roy formulated Radical Humanism centered on the sovereign individual. 'Radical' implied tracing human affairs back to their root—man himself. His system rested upon a secular triad: Freedom (integral liberation from state coercion and religious superstition), Reason (grounded biologically in man's evolutionary struggle for survival), and Ethics (grounded in secular rationalism, independent of divine scripture). Politically, Roy repudiated parliamentary party politics as an oligarchy of vote-catchers, proposing 'Radical Democracy' organized around grassroots People's Committees (*Lok Samitis*).",
      "conclusion": "Though Sudipto Kaviraj characterized Roy's political career as a 'remarkable failure' due to his inability to connect with Indian mass sentiments, Roy's Radical Humanism remains an indispensable critique of both capitalist consumerism and totalitarian collectivism, asserting the primacy of individual reason and dignity.",
      "scholarQuotes": [
        "M.N. Roy: 'Man is the measure of all things; individual is the only conscious entity in the cosmos.'",
        "Sudipto Kaviraj: 'Roy was a remarkable failure in practical politics, but a profound success in speculative political philosophy.'",
        "Sibnarayan Ray: 'Roy brought the critical spirit of the European Enlightenment directly into modern Indian thought.'"
      ]
    }
  },
  {
    "id": "ans-p1-09",
    "year": "UPSC PSIR Paper 1 Section B (15 Marks)",
    "marks": 15,
    "question": "Discuss Bipin Chandra's assessment of the Indian National Movement as a 'Gramscian War of Position' based on the Struggle-Truce-Struggle (S-T-S) strategy.",
    "dimensions": [
      "Bipin Chandra's Master Thesis in 'India's Struggle for Independence'",
      "Gramscian Framework: The Semi-Hegemonic Colonial State & War of Position",
      "Struggle-Truce-Struggle (S-T-S) vs Marxist Struggle-Victory (S-V)",
      "Role of the Constructive Programme during Truce Phases"
    ],
    "structure": {
      "intro": "In his seminal historiography *India's Struggle for Independence*, Prof. Bipin Chandra conceptualized the Indian National Movement under Mahatma Gandhi as the largest protracted, non-violent mass movement in world history, analyzing its dynamics through the theoretical framework of Antonio Gramsci's 'War of Position'.",
      "body": "Chandra argued that the British colonial state in India was not an absolute military dictatorship like Tsarist Russia; it was a 'semi-hegemonic' state that ruled through a combination of constitutionalism, rule of law, modern education, and the myth of a 'civilizing mission'. Because the Raj operated with manufactured legitimacy in civil society, a direct insurrectionary seizure of power (Gramsci's 'War of Maneuver' or Marxist 'Struggle-Victory') was tactically impossible and would have invited devastating military retaliation against unarmed masses. Instead, Gandhi orchestrated a prolonged 'War of Position'. This strategy operated on the Struggle-Truce-Struggle (S-T-S) cycle. Gandhi recognized that the masses possess a finite psychological capacity for intense street confrontation. When mass exhaustion set in, Gandhi strategically negotiated truces (such as the Gandhi-Irwin Pact of 1931). During the 'Truce' phase, the movement did not surrender; rather, it shifted into civil society via the Constructive Programme (khadi promotion, Harijan upliftment, national schooling, and Hindu-Muslim unity). This allowed the national movement to recoup mass energy, build institutional depth, and dismantle the moral hegemony of the British Raj brick by brick before launching the next, higher phase of struggle.",
      "conclusion": "Bipin Chandra's S-T-S analysis successfully resolves the Marxist criticism (e.g. R.P. Dutt) that Gandhi called off movements to protect bourgeois interests. By viewing Gandhian strategy as a Gramscian War of Position, Chandra demonstrates how Gandhi systematically eroded British moral legitimacy, ensuring that by 1947, the British could no longer rule India without massive physical coercion.",
      "scholarQuotes": [
        "Bipin Chandra: 'The Indian National Movement was a war of position where the trenches were the minds of the people and the battlefield was civil society.'",
        "Antonio Gramsci: 'In a war of position, civil society resists the direct assault of the war of movement; victory requires deep moral-intellectual reform.'",
        "Judith Brown: 'Gandhi's truces were not capitulations, but calculated breathing spaces for an army of moral satyagrahis.'"
      ]
    }
  }
]

data['answers'] = data.get('answers', []) + new_answers

# 4. Expand scanThumbnails up to scan 80
scan_titles = {
  29: "Sir Syed Ahmed Khan: Asbab-e-Baghawat-e-Hind & Defense of Muslim Loyalty",
  30: "Sir Syed Ahmed Khan: Two Beautiful Eyes of a Bride & Two-Nation Genesis",
  31: "Sri Aurobindo: Spiritual Theory of Nationalism & Mother India (Bhavani Bharati)",
  32: "Sri Aurobindo: Sanatana Dharma as Nationalism & Uttarpara Speech (1909)",
  33: "Sri Aurobindo: Critique of Moderates in 'New Lamps for Old' (Induprakash)",
  34: "Sri Aurobindo: Swaraj as Absolute Independence & Radical Extremism",
  35: "Sri Aurobindo: Doctrine of Passive Resistance & Fourfold Boycott",
  36: "Sri Aurobindo: Passive Resistance vs Satyagraha & Defensive Violence",
  37: "Sri Aurobindo: Philosophy of Freedom & The Gospel of Humanity",
  38: "Sri Aurobindo: Integral Yoga (Purna Yoga), Descent of Supermind & Human Unity",
  39: "Mahatma Gandhi: Experiments with Truth, Humayun Kabir & Master Strategist",
  40: "Mahatma Gandhi: Ahimsa as Active Love, Weapon of Brave & Satyagraha vs Passive Resistance",
  41: "Mahatma Gandhi: Four Dimensions of Swaraj (Political, Economic, Social, Moral)",
  42: "Mahatma Gandhi: Sarvodaya, Ruskin's Unto This Last & Bread Labour (Sharir-Shrama)",
  43: "Mahatma Gandhi: Hind Swaraj (1909) & Critique of Modern Civilisation",
  44: "Mahatma Gandhi: Critique of Parliament, Lawyers, Doctors & 9 Earths Warning",
  45: "Mahatma Gandhi: Doctrine of Trusteeship, Social Capital & Rejection of Class War",
  46: "Mahatma Gandhi: Stateless Democracy, Ramrajya & Oceanic Circles of Power",
  47: "Mahatma Gandhi: State as Soulless Machine & Philosophical Anarchism",
  48: "Mahatma Gandhi: Ends and Means Organic Unity (Sadhan-Sadhya) & Spiritual Politics",
  49: "Mahatma Gandhi: Rights Embryonic in Duties, Nishkama Karma & Nayee Taalim",
  50: "M.N. Roy: Intellectual Odyssey, Sudipto Kaviraj 'Remarkable Failure' & Mexico",
  51: "M.N. Roy: Marxist Phase, Critique of Gandhi Bourgeoisie & Lenin-Roy 1920 Debate",
  52: "M.N. Roy: Expulsion from Comintern & 5-Point Critique of Orthodox Marxism",
  53: "M.N. Roy: Ideas vs Production, Class Cooperation & Mental Revolution",
  54: "M.N. Roy: Radical Humanism (New Humanism), Freedom, Biological Reason & Secular Ethics",
  55: "M.N. Roy: Partyless Democracy (Lok Samitis), People's Committees & People's Plan (1944)",
  56: "M.N. Roy: Philosophical Influences & 8-Point Comprehensive Comparison with Gandhi",
  57: "Dr. B.R. Ambedkar: Tallest Dalit Leader, Dhananjay Keer & Arun Shourie Critique",
  58: "Dr. B.R. Ambedkar: Christophe Jaffrelot Defense, Bahujan Samaj Majority & Elite Nationalism",
  59: "Dr. B.R. Ambedkar: Columbia, LSE, Mahad Satyagraha 1927 & Formation of Parties",
  60: "Dr. B.R. Ambedkar: Major Works (Annihilation of Caste, Who Were Shudras, The Untouchables)",
  61: "Dr. B.R. Ambedkar: Origin of Shudras, Broken Men Hypothesis & Division of Labourers",
  62: "Dr. B.R. Ambedkar: Dynamiting Hindu Shastras & Conversion to Navayana Buddhism (1956)",
  63: "Dr. B.R. Ambedkar: What is Brahmanism? Twin Pillars of Endogamy & Purity-Pollution",
  64: "Dr. B.R. Ambedkar: Vegetarianism Dietary Shift, Sanskritisation & Gandhi-Ambedkar Debate Intro",
  65: "Gandhi-Ambedkar Debate: Varna vs Caste, Harijan vs Dalit & The Putana Allegory",
  66: "Gandhi-Ambedkar Debate: Village Republics as Den of Ignorance & Poona Pact (1932)",
  67: "Ambedkar vs Karl Marx: Inversion of Historical Materialism & Role of State",
  68: "Ambedkar vs Karl Marx: Constitutional Morality vs Proletarian Dictatorship",
  69: "Revision: Dharmashastra vs Arthashastra Continuum & Bhikhu Parekh Thesis",
  70: "Transition to National Movement: Historiographical Perspectives & Constitutionalism",
  71: "Early National Movement: Moderates' 3Ps (Prayer, Petition, Protest) & Drain of Wealth",
  72: "Extremist Critique: Tilak 'Political Suicide' & Aurobindo 'Intellectual Bankruptcy'",
  73: "Bipin Chandra: Assessment of Moderates, Ranade & Gokhale's Historical Service",
  74: "Rise of Extremists: Tilak's Praja Droh, Calcutta Corporation Act & Swadeshi",
  75: "Gandhian Mass Movement Strategy: Unique Features & Gramscian War of Position",
  76: "Gandhian Strategy: S-T-S vs S-V & Gandhi as Master Psychologist of Mass Endurance",
  77: "Non-Cooperation Movement (1920–22): Causes, Nagpur Session & Extra-Constitutional Action",
  78: "Non-Cooperation Movement: Programme, Chauri Chaura Withdrawal & Bipin Chandra Defense",
  79: "Non-Cooperation Movement: Real Achievements, Multi-Class Base & Exploding Minority Myth",
  80: "Civil Disobedience Movement (1930–31): Thoreau's Influence, 11 Demands & Dandi Salt March"
}

# Add thumbnails
existing_pages = {t['page'] for t in data['scansCatalog']}
for p in range(29, 81):
    if p not in existing_pages:
        nb_page = (p - 7) // 2 + 2 # Approximate notebook page
        data['scansCatalog'].append({
            "page": p,
            "scanFile": f"page_{p:03d}.png",
            "notebookPage": nb_page,
            "title": scan_titles.get(p, f"Lecture Scan Page {p:03d}")
        })

# Sort scansCatalog by page
data['scansCatalog'].sort(key=lambda x: x['page'])

# Save updated data
with open('app/src/data/paper1IptData.js', 'w', encoding='utf-8') as f:
    f.write('export const paper1IptData = ' + json.dumps(data, indent=2) + ';\n')

print(f"paper1IptData.js successfully enriched! Total flashcards: {len(data['flashcards'])}, Model Answers: {len(data['answers'])}, Thumbnails: {len(data['scansCatalog'])}")
