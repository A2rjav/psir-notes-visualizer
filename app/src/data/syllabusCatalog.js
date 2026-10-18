// Master Syllabus Catalog for UPSC PSIR Paper 1 and Paper 2 Notes (Shubhra Ranjan IAS)

export const syllabusCatalog = {
  paper1: {
    title: "Paper 1: Political Theory & Indian Politics",
    sectionA: {
      title: "Paper 1, Section A: Indian Political Thought (IPT)",
      description: "Classical, heterodox, and modern traditions of Indian political philosophy from ancient statecraft to modern renaissance.",
      topics: [
        { 
          id: 'ipt-intro', 
          number: 1, 
          title: 'Debate on IPT & Distinctive Features (V.R. Mehta, Max Müller, Rta, Purusharthas)', 
          pageRange: '2 – 3', 
          scanStart: 7, 
          scanEnd: 10, 
          status: 'completed', 
          lectures: 'Lectures 49 & 50' 
        },
        { 
          id: 'ipt-manu', 
          number: 2, 
          title: 'Manu & Manusmriti (Matsya Nyaya, Divine Personality, Varna Dharma, Asymmetric Penology)', 
          pageRange: '4 – 5', 
          scanStart: 11, 
          scanEnd: 13, 
          status: 'completed', 
          lectures: 'Lecture 50' 
        },
        { 
          id: 'ipt-kautilya-saptanga', 
          number: 3, 
          title: 'Kautilya: Arthashastra, Saptanga (Organic) Theory of State & Yogakshema', 
          pageRange: '6 – 8', 
          scanStart: 14, 
          scanEnd: 19, 
          status: 'completed', 
          lectures: 'Lecture 50' 
        },
        { 
          id: 'ipt-kautilya-mandala', 
          number: 4, 
          title: 'Kautilya: Mandala Theory, Foreign Policy, Anti-Corruption & Machiavelli Comparison', 
          pageRange: '8 – 10', 
          scanStart: 20, 
          scanEnd: 24, 
          status: 'completed', 
          lectures: 'Lecture 51' 
        },
        { 
          id: 'ipt-buddhist-thought', 
          number: 5, 
          title: 'Buddhist Political Thought: Agganna Sutta, Mahasammata, Dhamma vs Danda, Sangha Democracy', 
          pageRange: '11 – 12', 
          scanStart: 25, 
          scanEnd: 27, 
          status: 'completed', 
          lectures: 'Ancient IPT Notes' 
        },
        { 
          id: 'ipt-sir-syed', 
          number: 6, 
          title: 'Modern Indian Political Thought: Sir Syed Ahmed Khan (Aligarh Movement & Modernisation)', 
          pageRange: '13', 
          scanStart: 28, 
          scanEnd: 28, 
          status: 'completed', 
          lectures: 'Modern IPT Transition' 
        },
        { id: 'ipt-aurobindo', number: 7, title: 'Sri Aurobindo: Spiritual Nationalism & Passive Resistance', pageRange: '14 – 19', scanStart: 29, scanEnd: 40, status: 'queued', lectures: 'Modern IPT' },
        { id: 'ipt-gandhi', number: 8, title: 'Mahatma Gandhi: Swaraj, Sarvodaya, Satyagraha & Critique of Modernity', pageRange: '20 – 35', scanStart: 41, scanEnd: 70, status: 'queued', lectures: 'Modern IPT' },
        { id: 'ipt-ambedkar', number: 9, title: 'B.R. Ambedkar: Social Justice, Critique of Caste, Constitutionalism & State Socialism', pageRange: '36 – 48', scanStart: 71, scanEnd: 95, status: 'queued', lectures: 'Modern IPT' },
        { id: 'ipt-mn-roy', number: 10, title: 'M.N. Roy: Radical Humanism & Critique of Congress Nationalism', pageRange: '49 – 55', scanStart: 96, scanEnd: 110, status: 'queued', lectures: 'Modern IPT' }
      ]
    }
  },

  paper2: {
    title: "Paper 2: Comparative Politics & International Relations",
    sectionB: {
      title: "Part 1 File: India and the World (Section 2B)",
      description: "Foreign policy doctrines, bilateral relationships, multilateral organizations, and regional groupings.",
      topics: [
        { id: 'india-usa', number: 13, title: 'India – USA Relations', pageRange: '80 – 91', scanStart: 5, scanEnd: 26, status: 'completed', lectures: 'Lectures 15 & 16' },
        { id: 'india-russia', number: 14, title: 'India – Russia Relations', pageRange: '91 – 98', scanStart: 27, scanEnd: 45, status: 'ready', lectures: 'Lecture 17' },
        { id: 'india-china', number: 15, title: 'India – China Relations', pageRange: '99 – 114', scanStart: 46, scanEnd: 75, status: 'queued', lectures: 'Lecture 18 & 19' },
        { id: 'india-japan', number: 16, title: 'India – Japan Relations', pageRange: '115 – 117', scanStart: 76, scanEnd: 81, status: 'queued', lectures: 'Lecture 20' },
        { id: 'india-eu', number: 17, title: 'India – EU Relations', pageRange: '118 – 120', scanStart: 82, scanEnd: 87, status: 'queued', lectures: 'Lecture 20' },
        { id: 'us-hegemony', number: 18, title: 'US Hegemony & Post-Cold War Order', pageRange: '121 – 129', scanStart: 88, scanEnd: 104, status: 'queued', lectures: 'Lecture 21' },
        { id: 'brics', number: 19, title: 'BRICS & New Development Bank', pageRange: '130', scanStart: 105, scanEnd: 106, status: 'queued', lectures: 'Lecture 22' },
        { id: 'global-south', number: 20, title: 'India and the Global South (IBSA)', pageRange: '131 – 135', scanStart: 107, scanEnd: 116, status: 'queued', lectures: 'Lecture 22' },
        { id: 'nam-foreign-policy', number: 21, title: 'Non-Alignment (NAM) as Foreign Policy', pageRange: '136 – 137', scanStart: 117, scanEnd: 120, status: 'queued', lectures: 'Lecture 23' },
        { id: 'united-nations', number: 22, title: 'United Nations & Reforms', pageRange: '138 – 144', scanStart: 121, scanEnd: 134, status: 'queued', lectures: 'Lecture 23 & 24' },
        { id: 'wto', number: 23, title: 'World Trade Organization (WTO)', pageRange: '145 – 150', scanStart: 135, scanEnd: 146, status: 'queued', lectures: 'Lecture 25' },
        { id: 'imf', number: 24, title: 'International Monetary Fund (IMF)', pageRange: '151 – 152', scanStart: 147, scanEnd: 150, status: 'queued', lectures: 'Lecture 26' },
        { id: 'world-bank', number: 25, title: 'World Bank Group', pageRange: '153', scanStart: 151, scanEnd: 152, status: 'queued', lectures: 'Lecture 26' },
        { id: 'european-union', number: 26, title: 'European Union (Integration & Crisis)', pageRange: '154 – 159', scanStart: 153, scanEnd: 164, status: 'queued', lectures: 'Lecture 27' },
        { id: 'asean', number: 27, title: 'ASEAN & India\'s Act East Policy', pageRange: '160 – 165', scanStart: 165, scanEnd: 176, status: 'queued', lectures: 'Lecture 28' },
        { id: 'apec', number: 28, title: 'Asia-Pacific Economic Cooperation (APEC)', pageRange: '166', scanStart: 177, scanEnd: 178, status: 'queued', lectures: 'Lecture 29' },
        { id: 'nafta', number: 29, title: 'NAFTA & Regional Trade Blocs', pageRange: '167', scanStart: 179, scanEnd: 180, status: 'queued', lectures: 'Lecture 29' },
        { id: 'saarc', number: 30, title: 'SAARC (South Asian Regionalism)', pageRange: '168 – 170', scanStart: 181, scanEnd: 186, status: 'queued', lectures: 'Lecture 30' },
        { id: 'bimstec', number: 31, title: 'BIMSTEC & Bay of Bengal Integration', pageRange: '171', scanStart: 187, scanEnd: 188, status: 'queued', lectures: 'Lecture 30' },
        { id: 'india-pakistan', number: 32, title: 'India – Pakistan Relations', pageRange: '172 – 180', scanStart: 189, scanEnd: 206, status: 'queued', lectures: 'Lecture 31 & 32' },
        { id: 'india-afghanistan', number: 33, title: 'India – Afghanistan Relations', pageRange: '181 – 185', scanStart: 207, scanEnd: 214, status: 'queued', lectures: 'Lecture 33' }
      ]
    },
    sectionA: {
      title: "Part 2 File: Comparative & International Politics (Section 2A)",
      description: "Theories of IR, approaches to comparative politics, power, deterrence, and cold war dynamics.",
      topics: [
        { id: 'comparative-politics', number: 1, title: 'Comparative Politics and Government', pageRange: '1 – 2', status: 'queued' },
        { id: 'methods-approaches', number: 2, title: 'Methods & Approaches (Systems, Structural-Functional, Political Sociology)', pageRange: '3 – 12', status: 'queued' },
        { id: 'state-nature', number: 3, title: 'Nature of State in Advanced Industrial Societies', pageRange: '13 – 15', status: 'queued' },
        { id: 'representation', number: 4, title: 'Politics of Representation & Participation', pageRange: '16 – 17', status: 'queued' },
        { id: 'pressure-groups', number: 5, title: 'Pressure Groups & Social Movements', pageRange: '18 – 20', status: 'queued' },
        { id: 'globalisation-theories', number: 6, title: 'Globalisation & Nation-State', pageRange: '21 – 24', status: 'queued' },
        { id: 'international-relations', number: 7, title: 'International Relations Discipline & Evolution', pageRange: '25 – 28', status: 'queued' },
        { id: 'theories-ir', number: 8, title: 'Theories of IR (Realism, Liberalism, Marxism, Constructivism)', pageRange: '29 – 52', status: 'queued' },
        { id: 'scientific-approach', number: 9, title: 'Scientific & Behavioural Approaches in IR', pageRange: '53 – 56', status: 'queued' },
        { id: 'power-concept', number: 10, title: 'Concept of Power & National Interest', pageRange: '57 – 59', status: 'queued' },
        { id: 'power-management', number: 11, title: 'Management of Power (Balance of Power, Collective Security, Deterrence)', pageRange: '60 – 70', status: 'queued' },
        { id: 'cold-war', number: 12, title: 'Cold War Origins, Cuban Missile Crisis & Détente', pageRange: '71 – 79', status: 'queued' }
      ]
    }
  }
};
