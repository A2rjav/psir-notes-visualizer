import React, { useState } from 'react';
import { 
  BookOpen, 
  Shield, 
  Scale, 
  Crown, 
  Compass, 
  Users, 
  AlertTriangle, 
  CheckCircle2, 
  Sparkles, 
  Quote, 
  Eye, 
  ExternalLink, 
  ChevronDown, 
  ChevronUp, 
  Network, 
  Flame, 
  Feather, 
  Building2, 
  Coins, 
  Search,
  BookMarked
} from 'lucide-react';
import { paper1IptData } from '../data/paper1IptData';

export default function Paper1VisualNotesView({ onSelectScanPage, searchQuery }) {
  const [activeSectionId, setActiveSectionId] = useState('all');
  const [expandedConcept, setExpandedConcept] = useState('all');

  const { meta, keyMetrics, sections } = paper1IptData;

  const renderScanPill = (scanPage, notebookPage = null) => (
    <button
      onClick={() => onSelectScanPage(scanPage)}
      className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-mono font-bold bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 hover:text-amber-200 border border-amber-500/30 transition shadow-sm ml-2 cursor-pointer"
      title={`Open Original Handwritten Scan ${scanPage} in split inspector`}
    >
      <Eye className="w-3 h-3 text-amber-400" />
      Scan P.{scanPage} {notebookPage ? `[Note P.${notebookPage}]` : ''}
    </button>
  );

  const filteredSections = sections.filter(sec => {
    if (activeSectionId !== 'all' && sec.id !== activeSectionId) return false;
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    const matchTitle = sec.title.toLowerCase().includes(q);
    const matchSubtitle = sec.subtitle.toLowerCase().includes(q);
    const matchConcepts = sec.concepts.some(c => 
      c.title.toLowerCase().includes(q) || 
      c.summary.toLowerCase().includes(q) ||
      (c.details && c.details.some(d => d.toLowerCase().includes(q)))
    );
    return matchTitle || matchSubtitle || matchConcepts;
  });

  return (
    <div className="space-y-12 max-w-5xl mx-auto pb-20">
      
      {/* Hero Banner */}
      <section className="relative p-6 sm:p-8 rounded-2xl bg-gradient-to-br from-slate-900 via-amber-950/30 to-slate-900 border border-amber-500/20 shadow-2xl overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-10 pointer-events-none">
          <Crown className="w-64 h-64 text-amber-400" />
        </div>

        <div className="relative z-10 space-y-4">
          <div className="flex flex-wrap items-center gap-2">
            <span className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-amber-500/20 text-amber-300 border border-amber-500/40">
              {meta.paperName}
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-mono bg-slate-800 text-slate-300 border border-slate-700">
              {meta.section}
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-mono bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
              {meta.lectures} ({meta.dates})
            </span>
          </div>

          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
              <span>🏛️</span> {meta.topicTitle}
            </h1>
            <p className="mt-2 text-sm text-slate-300 leading-relaxed max-w-3xl">
              {meta.summary}
            </p>
          </div>

          {/* Quick Stats Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 border-t border-slate-800">
            {keyMetrics.map((metric, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80">
                <span className="text-[11px] uppercase tracking-wider text-amber-400 font-bold block">{metric.label}</span>
                <span className="text-xs text-slate-200 font-medium mt-0.5 line-clamp-2">{metric.value}</span>
              </div>
            ))}
          </div>

          {/* Verification Banner */}
          <div className="flex items-center justify-between p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-200 text-xs">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-amber-400 shrink-0" />
              <span>
                <strong>100% Zero-Information-Loss Guarantee:</strong> All 22 original handwritten lecture scans (Pages 007 to 028) transcribed and verified.
              </span>
            </div>
            <button
              onClick={() => onSelectScanPage(7)}
              className="px-3 py-1 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-[11px] transition shrink-0 ml-3"
            >
              Inspect Scan P.7
            </button>
          </div>
        </div>
      </section>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
        <button
          onClick={() => setActiveSectionId('all')}
          className={`px-3 py-1.5 rounded-lg text-xs font-bold transition whitespace-nowrap ${
            activeSectionId === 'all' 
              ? 'bg-amber-500 text-slate-950 shadow-md' 
              : 'bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700'
          }`}
        >
          All Topics (6)
        </button>
        {sections.map(sec => (
          <button
            key={sec.id}
            onClick={() => setActiveSectionId(sec.id)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition whitespace-nowrap ${
              activeSectionId === sec.id 
                ? 'bg-amber-500 text-slate-950 font-bold shadow-md' 
                : 'bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700'
            }`}
          >
            {sec.number}. {sec.title.split(':')[0]}
          </button>
        ))}
      </div>

      {/* Topics Content Sections */}
      <div className="space-y-16">
        {filteredSections.map(sec => (
          <section key={sec.id} id={sec.id} className="space-y-8">
            
            {/* Section Header */}
            <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded text-[11px] font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                    Topic {sec.number}
                  </span>
                  <span className="text-xs text-slate-400 font-mono">Notebook {sec.notebookPages} • {sec.lecture}</span>
                </div>
                <h2 className="text-xl font-bold text-white tracking-tight">{sec.title}</h2>
                <p className="text-xs text-slate-400">{sec.subtitle}</p>
              </div>

              {/* Scan Page Launchers */}
              <div className="flex flex-wrap items-center gap-1.5">
                <span className="text-[11px] text-slate-400 font-semibold mr-1">Scans:</span>
                {sec.scanPages.map(page => (
                  <button
                    key={page}
                    onClick={() => onSelectScanPage(page)}
                    className="px-2 py-1 rounded bg-slate-800 hover:bg-amber-500 hover:text-slate-950 text-slate-300 font-mono text-[11px] transition border border-slate-700"
                    title={`View Scan Page ${page}`}
                  >
                    P.{page}
                  </button>
                ))}
              </div>
            </div>

            {/* Concepts in this Section */}
            <div className="space-y-8">
              {sec.concepts.map((concept, cIdx) => (
                <div 
                  key={cIdx} 
                  className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800/90 shadow-xl space-y-6 hover:border-slate-700 transition"
                >
                  {/* Concept Header */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-slate-800">
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                        {concept.badge}
                      </span>
                      <h3 className="text-lg font-bold text-amber-400">{concept.title}</h3>
                    </div>
                    {renderScanPill(concept.scanPage)}
                  </div>

                  {/* Summary */}
                  <p className="text-sm text-slate-200 leading-relaxed bg-slate-950/40 p-4 rounded-xl border border-slate-800/60">
                    {concept.summary}
                  </p>

                  {/* Bullet Details */}
                  {concept.details && (
                    <ul className="space-y-2.5">
                      {concept.details.map((det, dIdx) => (
                        <li key={dIdx} className="flex items-start gap-2.5 text-xs text-slate-300 leading-relaxed">
                          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                          <span>{det}</span>
                        </li>
                      ))}
                    </ul>
                  )}

                  {/* Core Cultural Values (Intro IPT) */}
                  {concept.coreValues && (
                    <div className="space-y-3">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        Indian Cultural & Civilisational Values
                      </h4>
                      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                        {concept.coreValues.map((val, vIdx) => (
                          <div key={vIdx} className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                            <span className="text-xs font-bold text-amber-300 block">{val.name}</span>
                            <span className="text-[11px] text-slate-400 mt-1 block leading-normal">{val.desc}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Scholars Rebuttal (Intro IPT) */}
                  {concept.scholars && (
                    <div className="space-y-3">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        Scholarly Rebuttal & Western Critique
                      </h4>
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        {concept.scholars.map((sch, sIdx) => (
                          <div key={sIdx} className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-col justify-between">
                            <div>
                              <span className="text-xs font-bold text-white block mb-1">{sch.name}</span>
                              {sch.quote && (
                                <blockquote className="text-[11px] italic text-amber-300/90 border-l-2 border-amber-500 pl-2 my-2">
                                  "{sch.quote}"
                                </blockquote>
                              )}
                              <p className="text-[11px] text-slate-300 mt-1">{sch.argument}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* V.R. Mehta Comparison Table */}
                  {concept.comparisonTable && (
                    <div className="space-y-3 overflow-x-auto">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400">
                        {concept.comparisonTable.title}
                      </h4>
                      <table className="w-full text-left text-xs border border-slate-800 rounded-xl overflow-hidden">
                        <thead className="bg-slate-950 text-slate-300 uppercase text-[10px] tracking-wider border-b border-slate-800">
                          <tr>
                            {concept.comparisonTable.headers.map((h, hIdx) => (
                              <th key={hIdx} className="p-3 font-bold">{h}</th>
                            ))}
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800 bg-slate-900/60">
                          {concept.comparisonTable.rows.map((row, rIdx) => (
                            <tr key={rIdx} className="hover:bg-slate-800/40 transition">
                              <td className="p-3 font-semibold text-amber-300">{row[0]}</td>
                              <td className="p-3 text-rose-300/90">{row[1]}</td>
                              <td className="p-3 text-emerald-300/90 font-medium">{row[2]}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}

                  {/* Purusharthas Grid */}
                  {concept.fourPurusharthas && (
                    <div className="space-y-3">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        The Four Purusharthas (Balanced Aims of Human Life)
                      </h4>
                      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                        {concept.fourPurusharthas.map((p, pIdx) => (
                          <div key={pIdx} className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
                            <span className="text-xs font-bold text-amber-400 block">{p.name}</span>
                            <span className="text-[10px] font-mono text-indigo-400 block">{p.role}</span>
                            <p className="text-[11px] text-slate-300 mt-1">{p.desc}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Four Ashramas */}
                  {concept.fourAshramas && (
                    <div className="space-y-3">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        The Four Ashramas (Life-Stage Duties)
                      </h4>
                      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                        {concept.fourAshramas.map((a, aIdx) => (
                          <div key={aIdx} className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
                            <span className="text-xs font-bold text-white block">{a.name}</span>
                            <p className="text-[11px] text-slate-400 mt-1">{a.desc}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Ashta-Lokapalas (Manu's King) */}
                  {concept.lokapalas && (
                    <div className="space-y-3">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400">
                        Ashta-Lokapala: 8 Deities Blended into King's Divine Personality
                      </h4>
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                        {concept.lokapalas.map((l, lIdx) => (
                          <div key={lIdx} className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                            <span className="text-xs font-bold text-amber-300 block">⚡ {l.deity}</span>
                            <span className="text-[11px] text-slate-400 mt-0.5 block">{l.quality}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Divine Rights Denial & Prohibitions */}
                  {concept.divineRightsDenial && (
                    <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-200 space-y-2 text-xs">
                      <span className="font-bold text-rose-400 uppercase tracking-wider block">
                        Crucial Constitutional Distinction: Subordinate to Dharma
                      </span>
                      <ul className="space-y-1.5 list-disc list-inside">
                        {concept.divineRightsDenial.map((item, iIdx) => (
                          <li key={iIdx}>{item}</li>
                        ))}
                      </ul>
                      {concept.vyasanas && (
                        <p className="mt-2 text-[11px] text-rose-300/90 font-mono bg-rose-950/40 p-2 rounded">
                          <strong>10 Prohibited Vyasanas (Vices):</strong> {concept.vyasanas}
                        </p>
                      )}
                    </div>
                  )}

                  {/* Graded Taxation & Penology */}
                  {concept.taxationRates && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                        <span className="text-xs font-bold text-amber-400 uppercase tracking-wider block">
                          Graded Taxation in Manusmriti
                        </span>
                        <div className="space-y-2 text-xs">
                          {concept.taxationRates.map((t, tIdx) => (
                            <div key={tIdx} className="flex justify-between border-b border-slate-800/80 pb-1">
                              <span className="text-slate-300">{t.source}</span>
                              <span className="font-mono font-bold text-amber-300">{t.rate}</span>
                            </div>
                          ))}
                        </div>
                      </div>

                      {concept.penology && (
                        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                          <span className="text-xs font-bold text-rose-400 uppercase tracking-wider block">
                            Asymmetric Varna Penology
                          </span>
                          <p className="text-xs text-slate-300 leading-relaxed font-semibold">
                            {concept.penology.principle}
                          </p>
                          <p className="text-[11px] text-slate-400">{concept.penology.dandaFunction}</p>
                          <p className="text-[11px] text-rose-400/90 bg-rose-950/30 p-2 rounded border border-rose-900/50">
                            {concept.penology.shudraOppression}
                          </p>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Scholarly Critiques (Ambedkar, Periyar, Radhakrishnan) */}
                  {concept.critiques && (
                    <div className="space-y-3">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        Modern Critical Assessment (Traditionalist vs. Subaltern vs. Feminist)
                      </h4>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {concept.critiques.map((crit, cIdx) => (
                          <div key={cIdx} className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                            <span className="text-xs font-bold text-amber-300 block">{crit.scholar}</span>
                            <p className="text-[11px] text-slate-300 leading-relaxed">{crit.stance}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Saptanga 7 Limbs (Kautilya) */}
                  {concept.limbs && (
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400">
                          The 7 Limbs of Organic Sovereignty (Saptanga Theory)
                        </h4>
                        <span className="text-[11px] font-mono text-slate-400">
                          {concept.hubAndSpokeModel}
                        </span>
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                        {concept.limbs.map((limb) => (
                          <div key={limb.number} className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5 hover:border-amber-500/50 transition">
                            <div className="flex items-center justify-between">
                              <span className="text-xs font-bold text-amber-300">{limb.number}. {limb.name}</span>
                              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/20 text-amber-300">{limb.organ}</span>
                            </div>
                            <p className="text-[11px] text-slate-300 leading-relaxed">{limb.attributes}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Sacred Aphorism & Yogakshema */}
                  {concept.sacredAphorism && (
                    <div className="p-5 rounded-xl bg-amber-500/10 border border-amber-500/30 space-y-2">
                      <div className="flex items-center gap-2">
                        <Sparkles className="w-4 h-4 text-amber-400" />
                        <span className="text-xs font-bold text-amber-300 uppercase tracking-wider">
                          The Sacred Aphorism of Kautilyan Paternalistic Governance
                        </span>
                      </div>
                      <p className="text-sm font-serif font-bold text-amber-200">
                        {concept.sacredAphorism.sanskrit}
                      </p>
                      <p className="text-xs italic text-amber-300/80">
                        {concept.sacredAphorism.transliteration}
                      </p>
                      <p className="text-xs text-slate-200 leading-relaxed pt-1 border-t border-amber-500/20">
                        <strong>Translation:</strong> "{concept.sacredAphorism.meaning}"
                      </p>
                    </div>
                  )}

                  {/* Upadha Testing (Kautilya) */}
                  {concept.amatyaTesting && (
                    <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                      <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider block">
                        Four Upadha Integrity Tests for Bureaucrats & Council Architecture
                      </span>
                      <ul className="space-y-1 text-xs text-slate-300">
                        {concept.amatyaTesting.map((item, atIdx) => (
                          <li key={atIdx} className="leading-relaxed">{item}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* 12 Kings Raja-Mandala */}
                  {concept.twelveKings && (
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400">
                          The 12 Kings of Raja-Mandala (Concentric Geostrategic Rings)
                        </h4>
                        <span className="text-[11px] font-mono text-emerald-400 font-bold">
                          {concept.mathematicalFormula}
                        </span>
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                        {concept.twelveKings.map((king, kIdx) => (
                          <div key={kIdx} className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                            <span className="text-xs font-bold text-amber-300 block">{king.role}</span>
                            <span className="text-[11px] text-slate-400 mt-1 block">{king.desc}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* 4 Upayas & Shadgunya Niti */}
                  {concept.fourUpayas && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {/* Upayas */}
                      <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                        <span className="text-xs font-bold text-amber-400 uppercase tracking-wider block">
                          Four Upayas (Methods of Influence)
                        </span>
                        <div className="space-y-2 text-xs">
                          {concept.fourUpayas.map((u, uIdx) => (
                            <div key={uIdx} className="border-b border-slate-800/80 pb-1.5">
                              <span className="font-bold text-amber-300">{u.name}: </span>
                              <span className="text-slate-300">{u.desc}</span>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Shadgunya Niti */}
                      <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                        <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider block">
                          Shadgunya Niti (Six-Fold Foreign Policy)
                        </span>
                        <div className="space-y-2 text-xs">
                          {concept.shadgunyaNiti.map((s, sIdx) => (
                            <div key={sIdx} className="border-b border-slate-800/80 pb-1.5">
                              <span className="font-bold text-indigo-300">{s.policy}: </span>
                              <span className="text-slate-300">{s.trigger}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Typology of Wars & Victories */}
                  {concept.typologyOfWar && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                        <span className="text-xs font-bold text-rose-400 uppercase tracking-wider block">
                          3 Types of Warfare (Yuddha)
                        </span>
                        <div className="space-y-2 text-xs">
                          {concept.typologyOfWar.map((w, wIdx) => (
                            <div key={wIdx}>
                              <span className="font-bold text-rose-300">{w.type}: </span>
                              <span className="text-slate-400">{w.desc}</span>
                            </div>
                          ))}
                        </div>
                      </div>

                      {concept.typologyOfVictories && (
                        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                          <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider block">
                            3 Types of Conquest (Vijaya)
                          </span>
                          <div className="space-y-2 text-xs">
                            {concept.typologyOfVictories.map((v, vIdx) => (
                              <div key={vIdx}>
                                <span className="font-bold text-emerald-300">{v.type}: </span>
                                <span className="text-slate-400">{v.desc}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Corruption Metaphors & Remedies */}
                  {concept.corruptionMetaphors && (
                    <div className="space-y-4">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400">
                        Kautilya's Immortal Aphorisms on Administrative Corruption
                      </h4>
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        {concept.corruptionMetaphors.map((cm, cmIdx) => (
                          <div key={cmIdx} className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                            <blockquote className="text-[11px] italic text-amber-300/90 border-l-2 border-amber-500 pl-2">
                              "{cm.quote}"
                            </blockquote>
                            <p className="text-[11px] text-slate-400">{cm.meaning}</p>
                          </div>
                        ))}
                      </div>

                      {concept.sevenTierRemedies && (
                        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">
                              7-Tier Anti-Corruption Architecture & Tripartite Culpability Chain
                            </span>
                            <span className="text-[10px] font-mono bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded">
                              Dayak • Pratigrahak • Nidhayak
                            </span>
                          </div>
                          <p className="text-xs text-slate-300 font-semibold">{concept.fortyWays}</p>
                          <ul className="space-y-1 text-xs text-slate-400">
                            {concept.sevenTierRemedies.map((rem, rIdx) => (
                              <li key={rIdx}>{rem}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Kautilya vs Machiavelli */}
                  {concept.tenSimilarities && (
                    <div className="space-y-4">
                      <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30">
                        <span className="text-xs font-bold text-amber-300 uppercase tracking-wider block">
                          {concept.maxWeberQuote.source}
                        </span>
                        <blockquote className="text-xs italic text-amber-200 mt-1">
                          "{concept.maxWeberQuote.quote}"
                        </blockquote>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                          <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider block">
                            10 Core Similarities (The Realist Kinship)
                          </span>
                          <ul className="space-y-1.5 text-xs text-slate-300">
                            {concept.tenSimilarities.map((sim, sIdx) => (
                              <li key={sIdx}>{sim}</li>
                            ))}
                          </ul>
                        </div>

                        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                          <span className="text-xs font-bold text-rose-400 uppercase tracking-wider block">
                            Fundamental Philosophical Divergences
                          </span>
                          <div className="space-y-3 text-xs">
                            {concept.criticalDifferences.map((diff, dIdx) => (
                              <div key={dIdx} className="border-b border-slate-800 pb-2">
                                <span className="font-bold text-amber-300 block mb-1">{diff.parameter}</span>
                                <div className="space-y-0.5 text-[11px]">
                                  <p className="text-emerald-300/90"><strong>Kautilya:</strong> {diff.kautilya}</p>
                                  <p className="text-rose-300/90"><strong>Machiavelli:</strong> {diff.machiavelli}</p>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Buddhist 3 Principles & 4 Truths */}
                  {concept.threePrinciples && (
                    <div className="space-y-4">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400">
                        The Three Metaphysical Principles & Their Political Imprint
                      </h4>
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        {concept.threePrinciples.map((tp, tpIdx) => (
                          <div key={tpIdx} className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                            <span className="text-xs font-bold text-amber-300 block">{tp.name}</span>
                            <p className="text-[11px] text-slate-300 leading-relaxed">{tp.desc}</p>
                          </div>
                        ))}
                      </div>

                      {concept.fourNobleTruths && (
                        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                          <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider block">
                            Four Noble Truths & Noble Eightfold Path (Ashtangika Marga)
                          </span>
                          <ul className="space-y-1 text-xs text-slate-300">
                            {concept.fourNobleTruths.map((nt, ntIdx) => (
                              <li key={ntIdx}>{nt}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Buddhist Chakkavatti Comparison */}
                  {concept.comparisonChakravarti && (
                    <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3">
                      <span className="text-xs font-bold text-amber-400 uppercase tracking-wider block">
                        {concept.comparisonChakravarti.title}
                      </span>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                        <div className="p-3 rounded-lg bg-rose-950/20 border border-rose-900/40">
                          <span className="font-bold text-rose-300 block mb-1">Hindu Chakravarti Samrat</span>
                          <p className="text-slate-300 text-[11px]">{concept.comparisonChakravarti.hindu}</p>
                        </div>
                        <div className="p-3 rounded-lg bg-emerald-950/20 border border-emerald-900/40">
                          <span className="font-bold text-emerald-300 block mb-1">Buddhist Chakkavatti (World Monarch)</span>
                          <p className="text-slate-300 text-[11px]">{concept.comparisonChakravarti.buddhist}</p>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Deliberative Procedures (Sangha) */}
                  {concept.deliberativeProcedures && (
                    <div className="space-y-3">
                      <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider block">
                        Parliamentary Procedures within the Buddhist Sangha (Cited by Dr. B.R. Ambedkar)
                      </span>
                      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                        {concept.deliberativeProcedures.map((dp, dpIdx) => (
                          <div key={dpIdx} className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                            <span className="text-xs font-mono font-bold text-amber-300 block">{dp.term}</span>
                            <span className="text-[11px] text-slate-400 mt-1 block">{dp.desc}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Sir Syed Ahmed Khan */}
                  {concept.institutionalReforms && (
                    <div className="space-y-4">
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        {concept.institutionalReforms.map((ir, irIdx) => (
                          <div key={irIdx} className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                            <span className="text-xs font-bold text-amber-300 block">{ir.name}</span>
                            <p className="text-[11px] text-slate-400">{ir.desc}</p>
                          </div>
                        ))}
                      </div>

                      {concept.politicalDuality && (
                        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                          <span className="text-xs font-bold text-rose-400 uppercase tracking-wider block">
                            Political Evolution & The Two-Nation Theory Debate
                          </span>
                          <ul className="space-y-1.5 text-xs text-slate-300">
                            {concept.politicalDuality.map((pd, pdIdx) => (
                              <li key={pdIdx}>{pd}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}

                </div>
              ))}
            </div>

          </section>
        ))}
      </div>

    </div>
  );
}
