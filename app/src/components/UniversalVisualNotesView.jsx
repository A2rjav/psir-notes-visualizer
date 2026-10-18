import React, { useEffect, useState } from 'react';
import {
  BookOpen,
  Sparkles,
  Eye,
  Feather,
  Search,
  GraduationCap,
  ScrollText
} from 'lucide-react';

export default function UniversalVisualNotesView({ 
  currentVolume, 
  currentDataset, 
  onSelectScanPage, 
  searchQuery,
  jumpTarget,
  onJumpHandled
}) {
  const [activeSectionId, setActiveSectionId] = useState('all');

  // Sidebar "jump to section": drop any section filter so the target is rendered, then scroll.
  useEffect(() => {
    if (!jumpTarget) return undefined;
    setActiveSectionId('all');
    const t = setTimeout(() => {
      document.getElementById(jumpTarget.id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      onJumpHandled?.();
    }, 120);
    return () => clearTimeout(t);
  }, [jumpTarget, onJumpHandled]);

  const meta = currentDataset?.meta || {};
  const sections = currentDataset?.sections || [];
  const flashcards = currentDataset?.flashcards || [];
  const answers = currentDataset?.answers || [];
  const scans = currentDataset?.scansCatalog || [];

  const totalConcepts = sections.reduce((acc, sec) => acc + (sec.concepts ? sec.concepts.length : 0), 0);

  const renderScanPill = (scanPage, notebookPage = null) => (
    <button
      onClick={() => onSelectScanPage(scanPage)}
      className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-mono font-bold bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 hover:text-amber-200 border border-amber-500/30 transition shadow-sm ml-2 cursor-pointer shrink-0"
      title={`Open Original Handwritten Scan ${scanPage} in split inspector`}
    >
      <Eye className="w-3 h-3 text-amber-400" />
      Scan P.{scanPage} {notebookPage ? `[Note P.${notebookPage}]` : ''}
    </button>
  );

  const q = (searchQuery || '').trim().toLowerCase();
  const has = (v) => (v || '').toLowerCase().includes(q);
  const conceptMatches = (c) =>
    has(c.title) || has(c.summary) || has(c.verbatim) || (c.details || []).some(has);
  const sectionMetaMatches = (sec) =>
    has(sec.title) || has(sec.subtitle) ||
    (sec.keyScholars || []).some(has) || (sec.coreTheories || []).some(has);

  // With a query: a section whose own title/scholars match shows in full; otherwise only the
  // concepts that match are kept, so the result narrows to what was searched for.
  const visibleSections = sections
    .filter(sec => activeSectionId === 'all' || sec.id === activeSectionId)
    .map(sec => {
      if (!q || sectionMetaMatches(sec)) return { sec, concepts: sec.concepts || [] };
      return { sec, concepts: (sec.concepts || []).filter(conceptMatches) };
    })
    .filter(({ concepts }) => !q || concepts.length > 0);
  const matchedConceptTotal = visibleSections.reduce((a, v) => a + v.concepts.length, 0);

  return (
    <div className="space-y-12 max-w-5xl mx-auto pb-20">
      
      {/* Hero Banner */}
      <section className="relative p-6 sm:p-8 rounded-2xl bg-gradient-to-br from-slate-900 via-slate-900 to-amber-950/30 border border-amber-500/20 shadow-2xl overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-10 pointer-events-none">
          <BookOpen className="w-64 h-64 text-amber-400" />
        </div>

        <div className="relative z-10 space-y-4">
          <div className="flex flex-wrap items-center gap-2">
            <span className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-amber-500/20 text-amber-300 border border-amber-500/40">
              {currentVolume.paperNumber} • {currentVolume.sectionName}
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-mono bg-slate-800 text-slate-300 border border-slate-700">
              {meta.notebookPages || `Folios 1 to ${currentVolume.totalPages}`}
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-mono bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
              Shubhra Ranjan IAS Notes
            </span>
            <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              ✓ {scans.length || currentVolume.totalPages} pages transcribed
            </span>
          </div>

          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
              <span>{currentVolume.icon}</span> {meta.topicTitle || currentVolume.title}
            </h1>
            <p className="mt-2 text-sm text-slate-300 leading-relaxed max-w-3xl">
              {meta.summary || currentVolume.subtitle}
            </p>
          </div>

          {/* Quick Stats Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 border-t border-slate-800">
            <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80">
              <span className="text-[11px] uppercase tracking-wider text-amber-400 font-bold block">Archival Scans</span>
              <span className="text-sm text-slate-100 font-bold mt-0.5">{scans.length || currentVolume.totalPages} Pages Catalogued</span>
            </div>
            <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80">
              <span className="text-[11px] uppercase tracking-wider text-amber-400 font-bold block">Thematic Modules</span>
              <span className="text-sm text-slate-100 font-bold mt-0.5">{sections.length} Core Sections</span>
            </div>
            <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80">
              <span className="text-[11px] uppercase tracking-wider text-amber-400 font-bold block">Key Concepts</span>
              <span className="text-sm text-slate-100 font-bold mt-0.5">{totalConcepts} Detailed Models</span>
            </div>
            <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80">
              <span className="text-[11px] uppercase tracking-wider text-amber-400 font-bold block">Recall & Blueprints</span>
              <span className="text-sm text-slate-100 font-bold mt-0.5">{flashcards.length} Cards • {answers.length} Answers</span>
            </div>
          </div>

          {/* Verification Banner */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-200 text-xs">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-amber-400 shrink-0" />
              <span>
                <strong>Page-by-page transcription:</strong> every handwritten page (001 to {String(currentVolume.totalPages).padStart(3, '0')}) is transcribed below by an AI vision model. Open the original scan to verify any line.
              </span>
            </div>
            <button
              onClick={() => onSelectScanPage(currentVolume.defaultScan || 1)}
              className="px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-[11px] transition shrink-0 self-start sm:self-auto cursor-pointer"
            >
              Inspect Scan P.{currentVolume.defaultScan || 1}
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
          All Topics ({sections.length})
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

      {q && visibleSections.length > 0 && (
        <p className="text-xs text-slate-400 font-mono">
          {matchedConceptTotal} concept{matchedConceptTotal === 1 ? '' : 's'} in {visibleSections.length} section{visibleSections.length === 1 ? '' : 's'} match "{searchQuery}"
        </p>
      )}

      {/* Topics Content Sections */}
      <div className="space-y-16">
        {visibleSections.map(({ sec, concepts }) => (
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
                {(sec.scanPages || []).map(page => (
                  <button
                    key={page}
                    onClick={() => onSelectScanPage(page)}
                    className="px-2 py-1 rounded bg-slate-800 hover:bg-amber-500 hover:text-slate-950 text-slate-300 font-mono text-[11px] transition border border-slate-700 cursor-pointer"
                    title={`View Scan Page ${page}`}
                  >
                    P.{page}
                  </button>
                ))}
              </div>
            </div>

            {/* Core Scholars & Theories Pills */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {sec.keyScholars && sec.keyScholars.length > 0 && (
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-amber-400 uppercase tracking-wider">
                    <GraduationCap className="w-4 h-4" />
                    <span>Key Thinkers & Commentators</span>
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {sec.keyScholars.map((scholar, sIdx) => (
                      <span key={sIdx} className="px-2 py-0.5 rounded text-xs bg-slate-900 text-slate-300 border border-slate-800">
                        {scholar}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {sec.coreTheories && sec.coreTheories.length > 0 && (
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-indigo-400 uppercase tracking-wider">
                    <Sparkles className="w-4 h-4" />
                    <span>Core Theoretical Doctrines</span>
                  </div>
                  <ul className="space-y-1">
                    {sec.coreTheories.slice(0, 4).map((theory, tIdx) => (
                      <li key={tIdx} className="text-xs text-slate-300 flex items-start gap-1.5">
                        <span className="text-indigo-400 mt-0.5">▸</span>
                        <span className="line-clamp-1">{theory}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Concepts in this Section */}
            <div className="space-y-8">
              {concepts.map((concept, cIdx) => (
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

                  {/* Detailed Bullet Points */}
                  {concept.details && concept.details.length > 0 && (
                    <div className="space-y-2 pt-1">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                        <Feather className="w-3.5 h-3.5 text-amber-400" />
                        <span>Lecture Notes Breakdown & Margin Annotations:</span>
                      </h4>
                      <ul className="space-y-2.5">
                        {concept.details.map((bullet, bIdx) => (
                          <li key={bIdx} className="text-xs sm:text-sm text-slate-300 flex items-start gap-2.5 bg-slate-950/20 p-2.5 rounded-lg border border-slate-800/40">
                            <span className="text-amber-400 mt-0.5 font-bold">•</span>
                            <span className="leading-relaxed">{bullet}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Verbatim handwritten transcription (collapsed unless it is the page's only content) */}
                  {concept.verbatim && (
                    <details
                      open={!(concept.details && concept.details.length > 3)}
                      className="rounded-xl border border-slate-800/80 bg-slate-950/50 group"
                    >
                      <summary className="cursor-pointer select-none px-4 py-2.5 text-xs font-bold uppercase tracking-wider text-slate-400 hover:text-amber-300 flex items-center gap-1.5">
                        <ScrollText className="w-3.5 h-3.5 text-amber-400" />
                        <span>Verbatim handwritten transcription</span>
                      </summary>
                      <pre className="px-4 pb-4 pt-1 text-xs sm:text-[13px] leading-relaxed text-slate-300 whitespace-pre-wrap break-words font-sans">
                        {concept.verbatim}
                      </pre>
                    </details>
                  )}
                </div>
              ))}
            </div>

          </section>
        ))}

        {visibleSections.length === 0 && (
          <div className="p-12 text-center rounded-2xl bg-slate-900/50 border border-slate-800 space-y-3">
            <Search className="w-8 h-8 text-slate-500 mx-auto" />
            <h3 className="text-base font-bold text-slate-300">No matching concepts found</h3>
            <p className="text-xs text-slate-500">
              Try searching for different terms or clear the search query.
            </p>
          </div>
        )}
      </div>

    </div>
  );
}
