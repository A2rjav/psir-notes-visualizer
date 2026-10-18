// Master Volumes Catalog for UPSC PSIR 6-Volume Knowledge System
// Shubhra Ranjan IAS Handwritten Lecture Notes
// 100% Zero-Loss Digital Conversion (1,146 Total Pages)

import { paper1IptData } from './paper1IptData';
import { paper1Part2Data } from './paper1Part2Data';
import { paper1Part4Data } from './paper1Part4Data';
import { paper1Part5Data } from './paper1Part5Data';
import { paper2IndiaWorldData } from './paper2IndiaWorldData';
import { paper2ComparativeData } from './paper2ComparativeData';

export const volumesCatalog = [
  {
    id: 'p1_part1',
    paperNumber: 'Paper 1',
    sectionName: 'Section A & B (Part 1)',
    shortCode: 'P1-V1',
    volumeNumber: 1,
    title: 'Indian Political Thought & IGP Part 1',
    shortTitle: 'Indian Political Thought (IPT)',
    subtitle: 'Manu • Kautilya • Buddhist Thought • Modern Renaissance • Sir Syed • Gandhi • Ambedkar • M.N. Roy',
    totalPages: 214,
    scanBasePath: '/scans_p1',
    defaultScan: 7,
    dataset: paper1IptData,
    badgeColor: 'amber',
    icon: '🏛️',
    status: '100% Complete'
  },
  {
    id: 'p1_part2',
    paperNumber: 'Paper 1',
    sectionName: 'Section B (Part 2)',
    shortCode: 'P1-V2',
    volumeNumber: 2,
    title: 'Indian Government & Politics: Grassroots to Sovereignty',
    shortTitle: 'Grassroots, Judiciary & Executive (IGP)',
    subtitle: 'Panchayati Raj • Judicial Review & NJAC • Parliament • PMO • Social Movements • Basic Structure Doctrine',
    totalPages: 150,
    scanBasePath: '/scans_p1_part2',
    defaultScan: 1,
    dataset: paper1Part2Data,
    badgeColor: 'emerald',
    icon: '📜',
    status: '100% Complete'
  },
  {
    id: 'p1_part4',
    paperNumber: 'Paper 1',
    sectionName: 'Section A & B (Part 4)',
    shortCode: 'P1-V3',
    volumeNumber: 3,
    title: 'Western Political Thought II & Political Theory',
    shortTitle: 'Political Theory & Ideologies (WPT II)',
    subtitle: 'Liberalism • Marxism & Frankfurt School • Multiculturalism • Feminism • Theories of State, Power, Justice & Rights',
    totalPages: 224,
    scanBasePath: '/scans_p1_part4',
    defaultScan: 1,
    dataset: paper1Part4Data,
    badgeColor: 'indigo',
    icon: '⚖️',
    status: '100% Complete'
  },
  {
    id: 'p1_part5',
    paperNumber: 'Paper 1',
    sectionName: 'Section A (Part 5)',
    shortCode: 'P1-V4',
    volumeNumber: 4,
    title: 'Western Political Thought I: Plato to Hannah Arendt',
    shortTitle: 'Classical WPT: Plato to Arendt (WPT I)',
    subtitle: 'Plato • Aristotle • Machiavelli • Hobbes • Locke • Rousseau • J.S. Mill • Marx • Gramsci • Hannah Arendt',
    totalPages: 180,
    scanBasePath: '/scans_p1_part5',
    defaultScan: 1,
    dataset: paper1Part5Data,
    badgeColor: 'violet',
    icon: '🧠',
    status: '100% Complete'
  },
  {
    id: 'p2_part1',
    paperNumber: 'Paper 2',
    sectionName: 'Section B (Part 1)',
    shortCode: 'P2-V5',
    volumeNumber: 5,
    title: 'India and the World: Foreign Policy & Bilaterals',
    shortTitle: 'India & The World (IR Bilaterals)',
    subtitle: 'India-USA • India-Russia • India-China • Indo-Pacific • UN Reforms • WTO • Regionalism (SAARC/BIMSTEC)',
    totalPages: 214,
    scanBasePath: '/scans_p2_part1',
    defaultScan: 1,
    dataset: paper2IndiaWorldData,
    badgeColor: 'sky',
    icon: '🌐',
    status: '100% Complete'
  },
  {
    id: 'p2_part2',
    paperNumber: 'Paper 2',
    sectionName: 'Section A (Part 2)',
    shortCode: 'P2-V6',
    volumeNumber: 6,
    title: 'Comparative Politics & International Relations Theory',
    shortTitle: 'Comparative Politics & IR Theory',
    subtitle: 'Comparative Approaches • Realism • Liberalism • Marxism • Game Theory • Balance of Power • Cold War to Cold War 2.0',
    totalPages: 164,
    scanBasePath: '/scans_p2_part2',
    defaultScan: 1,
    dataset: paper2ComparativeData,
    badgeColor: 'rose',
    icon: '🎯',
    status: '100% Complete'
  }
];

export const getVolumeById = (id) => {
  return volumesCatalog.find(v => v.id === id) || volumesCatalog[0];
};
