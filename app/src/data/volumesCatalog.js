// Master catalogue of the six volumes of Shubhra Ranjan IAS PSIR lecture notes.
//
// Datasets are loaded on demand (`load()`), so opening the app downloads one volume, not all six.
// `step` is the suggested study order for a beginner: thinkers first (every Section A concept was
// invented by a thinker), then theory, then Indian thought and government, then comparative/IR
// theory, and India's foreign relations last because that part changes with current affairs.

export const volumesCatalog = [
  {
    id: 'p1_part1',
    paperNumber: 'Paper 1',
    sectionName: 'Section A & B (Part 1)',
    shortCode: 'P1-V1',
    volumeNumber: 1,
    step: 3,
    title: 'Indian Political Thought & IGP Part 1',
    shortTitle: 'Indian Political Thought (IPT)',
    subtitle: 'Manu • Kautilya • Buddhist thought • Sir Syed • Aurobindo • Gandhi • Ambedkar • M.N. Roy • National Movement • Constitution',
    whyNow: "Once Western thinkers are familiar, India's own thinkers are easier to compare and remember.",
    totalPages: 214,
    sectionCount: 23,
    scanBasePath: '/scans_p1',
    defaultScan: 7,
    load: () => import('./paper1IptData.js').then((m) => m.paper1IptData),
    icon: '🏛️',
  },
  {
    id: 'p1_part2',
    paperNumber: 'Paper 1',
    sectionName: 'Section B (Part 2)',
    shortCode: 'P1-V2',
    volumeNumber: 2,
    step: 4,
    title: 'Indian Government & Politics: Grassroots to Sovereignty',
    shortTitle: 'Grassroots, Judiciary & Executive (IGP)',
    subtitle: 'Panchayati Raj • Judicial review & NJAC • Parliament • PMO • Social movements • Basic structure',
    whyNow: 'Institutions and cases are factual; with the theory in place they become examples, not lists.',
    totalPages: 150,
    sectionCount: 17,
    scanBasePath: '/scans_p1_part2',
    defaultScan: 1,
    load: () => import('./paper1Part2Data.js').then((m) => m.paper1Part2Data),
    icon: '📜',
  },
  {
    id: 'p1_part4',
    paperNumber: 'Paper 1',
    sectionName: 'Section A & B (Part 4)',
    shortCode: 'P1-V3',
    volumeNumber: 3,
    step: 2,
    title: 'Western Political Thought II & Political Theory',
    shortTitle: 'Political Theory & Ideologies (WPT II)',
    subtitle: 'Liberalism • Marxism & Frankfurt School • Multiculturalism • Feminism • State, power, justice, rights',
    whyNow: 'Concepts like power, justice and rights build directly on the thinkers from Step 1.',
    totalPages: 224,
    sectionCount: 23,
    scanBasePath: '/scans_p1_part4',
    defaultScan: 1,
    load: () => import('./paper1Part4Data.js').then((m) => m.paper1Part4Data),
    icon: '⚖️',
  },
  {
    id: 'p1_part5',
    paperNumber: 'Paper 1',
    sectionName: 'Section A (Part 5)',
    shortCode: 'P1-V4',
    volumeNumber: 4,
    step: 1,
    title: 'Western Political Thought I: Plato to Hannah Arendt',
    shortTitle: 'Classical WPT: Plato to Arendt (WPT I)',
    subtitle: 'Plato • Aristotle • Machiavelli • Hobbes • Locke • Rousseau • J.S. Mill • Marx • Gramsci • Hannah Arendt',
    whyNow: 'Start here: almost every idea in Paper 1 Section A was first argued by one of these thinkers.',
    totalPages: 180,
    sectionCount: 17,
    scanBasePath: '/scans_p1_part5',
    defaultScan: 1,
    load: () => import('./paper1Part5Data.js').then((m) => m.paper1Part5Data),
    icon: '🧠',
  },
  {
    id: 'p2_part1',
    paperNumber: 'Paper 2',
    sectionName: 'Section B (Part 1)',
    shortCode: 'P2-V5',
    volumeNumber: 5,
    step: 6,
    title: 'India and the World: Foreign Policy & Bilaterals',
    shortTitle: 'India & The World (IR Bilaterals)',
    subtitle: 'India-USA • India-Russia • India-China • Indo-Pacific • UN reforms • WTO • SAARC & BIMSTEC',
    whyNow: 'Do this last and keep it fresh: it is the part of the syllabus that moves with current affairs.',
    totalPages: 214,
    sectionCount: 20,
    scanBasePath: '/scans_p2_part1',
    defaultScan: 1,
    load: () => import('./paper2IndiaWorldData.js').then((m) => m.paper2IndiaWorldData),
    icon: '🌐',
  },
  {
    id: 'p2_part2',
    paperNumber: 'Paper 2',
    sectionName: 'Section A (Part 2)',
    shortCode: 'P2-V6',
    volumeNumber: 6,
    step: 5,
    title: 'Comparative Politics & International Relations Theory',
    shortTitle: 'Comparative Politics & IR Theory',
    subtitle: 'Comparative approaches • Realism • Liberalism • Marxism • Game theory • Balance of power • Cold War',
    whyNow: 'IR theory is the lens for every India-and-the-world answer in Step 6.',
    totalPages: 164,
    sectionCount: 19,
    scanBasePath: '/scans_p2_part2',
    defaultScan: 1,
    load: () => import('./paper2ComparativeData.js').then((m) => m.paper2ComparativeData),
    icon: '🎯',
  },
];

export const volumesByStep = [...volumesCatalog].sort((a, b) => a.step - b.step);

export const getVolumeById = (id) => volumesCatalog.find((v) => v.id === id) || volumesByStep[0];

// "Contents & Front Matter" sections hold the cover, index and reading list: not study material.
export const isFrontMatter = (sec) => /^contents\b|front matter/i.test(sec?.title || '');

// Topic number shown to the student: study topics count from 1, skipping the front-matter section.
export const topicNumber = (sections, sec) => {
  const i = sections.filter((s) => !isFrontMatter(s)).findIndex((s) => s.id === sec?.id);
  return i === -1 ? null : String(i + 1).padStart(2, '0');
};

// Flashcards and answers are tagged by the builder: card.category = section title cut to 40
// characters; answer.id = "ans-v<volume>-<section number>-<k>".
export const sectionCardCategory = (sec) => {
  const t = (sec?.title || '').trim();
  return t.length <= 40 ? t : `${t.slice(0, 39).trimEnd()}…`;
};
export const sectionAnswerMatch = (sec) => (a) => String(a.id || '').includes(`-${sec.number}-`);
