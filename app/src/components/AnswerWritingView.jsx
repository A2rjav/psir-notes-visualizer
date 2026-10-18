import React, { useState } from 'react';
import { 
  FileText, 
  Sparkles, 
  PenTool, 
  CheckCircle2, 
  ChevronRight, 
  BookOpen, 
  Eye, 
  Layout,
  Share2,
  GraduationCap,
  Layers
} from 'lucide-react';

// Datasets are not uniform: `body` is an array in most volumes but a single paragraph string in
// some V1 answers, and questions may carry stray markdown. Normalise before rendering.
const toList = (v) => {
  if (Array.isArray(v)) return v.map(String).filter(Boolean);
  if (typeof v !== 'string' || !v.trim()) return [];
  const numbered = v
    .split(/\n+\s*(?=(?:\d+[.)]|[-•*])\s)/)
    .map((x) => x.replace(/^\s*(?:\d+[.)]|[-•*])\s+/, '').trim())
    .filter(Boolean);
  if (numbered.length > 1) return numbered;
  const paragraphs = v.split(/\n{2,}/).map((x) => x.trim()).filter(Boolean);
  return paragraphs.length ? paragraphs : [v.trim()];
};

const cleanQuestion = (q) =>
  String(q || '').replace(/^[-*#\s"“]+/, '').replace(/[*"”\s]+$/, '');

const formatMarks = (m) => (typeof m === 'number' ? `${m} Marks` : m || '20 Marks (250 Words)');

export default function AnswerWritingView({ onSelectScanPage, currentDataset, currentVolume }) {
  const [selectedQuestionIndex, setSelectedQuestionIndex] = useState(0);

  const frameworks = currentDataset?.answers || [];
  const current = frameworks[selectedQuestionIndex] || frameworks[0] || {
    question: 'No model answers available for this volume.',
    marks: '20 Marks',
    topic: 'PSIR Answer Blueprint',
    structure: {
      intro: 'Analytical introduction contextualizing the question within political theory and constitutional jurisprudence.',
      body: ['Body pillar analyzing theoretical and empirical dimensions.'],
      scholars: ['Key Scholars and Commission Reports'],
      conclusion: 'Balanced UPSC conclusion.'
    }
  };

  const struct = current.structure || {};
  const introText = current.introduction || struct.introduction || struct.intro;
  const bodyList = toList(current.bodyPillars || struct.body);
  const scholarsList = toList(struct.scholars || current.scholars);
  const dimensionsList = toList(current.dimensions);
  const conclText = current.conclusion || struct.conclusion;
  const currentQuestion = cleanQuestion(current.question);

  // Custom exam diagram templates for Paper 1 & Paper 2
  const isKaplanQuestion = /kaplan|polarity|bipolar|multipolar|international system/i.test(
    `${current.question || ''} ${current.topic || ''}`
  );
  const getExamDiagram = (qIdx) => {
    if (currentVolume?.id === 'p1_part1') {
      if (qIdx === 0) {
        return `
            PROF. V.R. MEHTA'S PARADIGM: DICHOTOMY VS. CONTINUITY
            ──────────────────────────────────────────────────────

       [ WESTERN PARADIGM ]                 [ INDIAN PARADIGM ]
          (Dichotomies / विभाजन)                   (Continuity / सातत्य)
   • Individual vs. Community           • Individual integrated in Community
   • Nature vs. Culture (Conquest)       • Nature in harmony with Culture
   • Self-interest vs. Others (Zero-sum) • Enlightened Self-interest (Dharma)
   • Ethics separated from Politics     • Dharma & Rajniti Inseparable
              │                                      │
              ▼                                      ▼
     [ Machiavellian Realism ]             [ Dharma-Danda Co-presence ]
        `;
      } else if (qIdx === 1) {
        return `
                 MANU'S CONSTITUTIONAL LIMITS ON KING
                 ────────────────────────────────────

                  [ ASHTA-LOKAPALA NATURE ]
       Indra (Power) • Agni (Wrath) • Yama (Justice) • Surya (Taxes)
                              │
                              ▼
                [ KING IS SUBORDINATE TO DHARMA ]
            - Possesses Divine Personality (8 Deities)
            - Has NO Divine Rights (Unlike James I of UK)
                              │
               Violates Rajdharma? / Misuses Danda?
                              │
                              ▼
                 [ DANDA DESTROYS THE KING ]
            "Danda is a double-edged sword; if abused,
             it kills the King along with his kingdom."
        `;
      }
    } else if (currentVolume?.id === 'p2_part2' && isKaplanQuestion) {
      return `
             MORTON KAPLAN'S SYSTEMIC HEURISTICS & POLARITY
             ──────────────────────────────────────────────

    [ CLASSICAL MULTIPOLAR ]             [ TIGHT BIPOLARITY ]
      (Balance of Power)                    (Cold War Era)
    • Flexible Alliances                 • Rigid Bloc Discipline
    • Shiftable Alignments               • High Cohesion, Nuclear MAD
    • Traditional Balancer               • Zero-sum proxy contestation
             │                                     │
             └─────────────────┬───────────────────┘
                               │
                               ▼
                 [ NEW COLD WAR / MULTIPOLARITY ]
             • Variable geometry & Issue-based alignments
             • Strategic Autonomy & Regional Minilaterals
      `;
    }

    return `
           UPSC PSIR 3-TIER ANSWER STRUCTURING MATRIX
           ──────────────────────────────────────────

  [ TIER 1: CONCEPTUAL GENESIS ] ──► Thinkers, Texts & Problematique
                │
  [ TIER 2: DIALECTICAL CRITIQUE ] ─► Realist, Liberal, Marxist, Feminist Debates
                │
  [ TIER 3: CONTEMPORARY SYNTHESIS ] ─► Indian Constitutionalism & Global Governance
    `;
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-16">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <PenTool className="w-5 h-5 text-amber-400" />
            <h2 className="text-xl font-bold text-white">UPSC PSIR Mains Model Answer Blueprints</h2>
          </div>
          <p className="text-xs text-slate-400">
            {currentVolume?.title || 'PSIR Notes'} • 15 & 20 Markers Structuring Frameworks
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
            {frameworks.length} Frameworks Available
          </span>
        </div>
      </div>

      {/* Main Framework Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Question Selector List */}
        <div className="lg:col-span-4 space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400 block px-1">
            Select Question ({frameworks.length})
          </span>
          <div className="space-y-2 max-h-[600px] overflow-y-auto pr-1">
            {frameworks.map((fw, idx) => (
              <button
                key={idx}
                onClick={() => setSelectedQuestionIndex(idx)}
                className={`w-full text-left p-3.5 rounded-xl border transition flex items-start gap-3 cursor-pointer ${
                  selectedQuestionIndex === idx
                    ? 'bg-amber-500/10 border-amber-500/50 text-white shadow-lg shadow-amber-500/5'
                    : 'bg-slate-900/60 border-slate-800/80 text-slate-300 hover:bg-slate-800 hover:border-slate-700'
                }`}
              >
                <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold shrink-0 mt-0.5 ${
                  selectedQuestionIndex === idx ? 'bg-amber-500 text-slate-950' : 'bg-slate-800 text-slate-400'
                }`}>
                  Q{idx + 1}
                </span>
                <div className="min-w-0">
                  <h4 className="text-xs font-semibold leading-snug line-clamp-2">
                    {cleanQuestion(fw.question)}
                  </h4>
                  <span className="text-[10px] text-slate-500 mt-1 block">
                    {typeof fw.marks === 'number' ? `${fw.marks} Marks` : (fw.marks || '20 Marks')} • {fw.topic ? (fw.topic.length > 25 ? fw.topic.slice(0, 25) + '...' : fw.topic) : 'Model Answer'}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Right Column: Active Blueprint Workspace */}
        <div className="lg:col-span-8 space-y-6">
          
          {/* Question Card */}
          <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 shadow-xl space-y-4">
            <div className="flex items-center justify-between">
              <span className="px-2.5 py-1 rounded text-xs font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                Question {selectedQuestionIndex + 1} • {formatMarks(current.marks)}
              </span>
              <span className="text-xs text-slate-400 font-mono">
                {current.topic || 'UPSC Mains'}
              </span>
            </div>
            {current.scanPage && (
              <button
                onClick={() => onSelectScanPage(current.scanPage)}
                className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-mono font-bold bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 transition cursor-pointer"
                title="Open the scanned page this answer is drawn from"
              >
                <Eye className="w-3 h-3" /> Source: Scan P.{current.scanPage}
              </button>
            )}
            <h3 className="text-base sm:text-lg font-bold text-white leading-relaxed">
              "{currentQuestion}"
            </h3>
          </div>

          {/* Structuring Blueprint */}
          <div className="space-y-4">
            
            {dimensionsList.length > 0 && (
              <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
                <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-sky-400">
                  <Layout className="w-4 h-4" />
                  <span>Dimensions to Cover</span>
                </div>
                <ul className="flex flex-wrap gap-2 pt-1">
                  {dimensionsList.map((d, i) => (
                    <li key={i} className="px-2.5 py-1 rounded-lg text-xs bg-sky-500/10 text-sky-300 border border-sky-500/20">{d}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Introduction Pillar */}
            <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
              <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-amber-400">
                <span className="w-2 h-2 rounded-full bg-amber-400"></span>
                <span>1. Introduction (30–40 Words)</span>
              </div>
              <p className="text-xs sm:text-sm text-slate-200 leading-relaxed bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80">
                {introText || 'Introduce through the core problematique, foundational thinker, and philosophical context.'}
              </p>
            </div>

            {/* Body Pillars */}
            <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-3">
              <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-indigo-400">
                <span className="w-2 h-2 rounded-full bg-indigo-400"></span>
                <span>2. Core Body Arguments & Thinkers (150–170 Words)</span>
              </div>
              <div className="space-y-2">
                {bodyList.map((pillar, pIdx) => (
                  <div key={pIdx} className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-start gap-2.5">
                    <span className="text-indigo-400 font-mono text-xs font-bold shrink-0 mt-0.5">2.{pIdx + 1}</span>
                    <p className="text-xs sm:text-sm text-slate-200 leading-relaxed">
                      {pillar}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Scholars to Cite */}
            {scholarsList && scholarsList.length > 0 && (
              <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
                <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-emerald-400">
                  <GraduationCap className="w-4 h-4" />
                  <span>Thinkers, Scholars & Judicial Authorities to Cite</span>
                </div>
                <div className="flex flex-wrap gap-2 pt-1">
                  {scholarsList.map((sc, sIdx) => (
                    <span key={sIdx} className="px-2.5 py-1 rounded-lg text-xs bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 font-medium">
                      {sc}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* In-Exam Diagram Schematic */}
            <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
              <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-sky-400">
                <Layout className="w-4 h-4" />
                <span>Value-Addition: In-Exam Visual Flowchart / Diagram</span>
              </div>
              <pre className="p-4 rounded-xl bg-slate-950 border border-slate-800/90 text-[11px] sm:text-xs font-mono text-amber-300/90 overflow-x-auto leading-tight select-all">
                {getExamDiagram(selectedQuestionIndex)}
              </pre>
            </div>

            {/* Conclusion Pillar */}
            <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
              <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-emerald-400">
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                <span>3. Balanced Conclusion & Contemporary Relevance (30–40 Words)</span>
              </div>
              <p className="text-xs sm:text-sm text-slate-200 leading-relaxed bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80">
                {conclText || 'Conclude with a forward-looking synthesis linking the core debate with modern constitutionalism and global governance.'}
              </p>
            </div>

          </div>

        </div>

      </div>

    </div>
  );
}
