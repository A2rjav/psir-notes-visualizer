import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  Eye,
  Search,
  GraduationCap,
  Sparkles,
  ScrollText,
  CheckCircle2,
  Circle,
  ChevronDown,
  ChevronRight,
  PlayCircle,
  Layers,
  PenTool,
  BookOpen,
  ArrowRight,
} from 'lucide-react';
import VisualExplainer from './VisualExplainer';
import { visualExplainers } from '../data/visualExplainers';
import { volumesByStep, isFrontMatter, sectionCardCategory, sectionAnswerMatch, topicNumber } from '../data/volumesCatalog';

// One handwritten page: the plain-English summary first, the verbatim transcript one tap away.
// The transcript is only rendered when opened, which keeps a 200-page volume light to scroll.
function PageCard({ concept, onSelectScanPage, query }) {
  const [open, setOpen] = useState(false);
  const verbatimHit = !!query && (concept.verbatim || '').toLowerCase().includes(query);
  const show = open || verbatimHit;
  return (
    <div className="p-4 sm:p-5 rounded-xl bg-slate-900/80 border border-slate-800/90 hover:border-slate-700 transition space-y-2.5">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <h4 className="text-sm sm:text-base font-bold text-amber-300 leading-snug min-w-0">{concept.title}</h4>
        <button
          onClick={() => onSelectScanPage(concept.scanPage)}
          className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-mono font-bold bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 transition cursor-pointer shrink-0"
          title="Open the original handwritten page"
        >
          <Eye className="w-3 h-3" /> Scan P.{concept.scanPage}
        </button>
      </div>
      {concept.summary && (
        <p className="text-sm text-slate-200 leading-relaxed">{concept.summary}</p>
      )}
      {concept.verbatim && (
        <div>
          <button
            onClick={() => setOpen(!open)}
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-amber-300 transition cursor-pointer"
          >
            {show ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
            <ScrollText className="w-3.5 h-3.5 text-amber-400" />
            {show ? 'Hide the original notes' : 'Read the original notes for this page'}
          </button>
          {show && (
            <pre className="mt-2 p-3 rounded-lg bg-slate-950/60 border border-slate-800/80 text-xs sm:text-[13px] leading-relaxed text-slate-300 whitespace-pre-wrap break-words font-sans">
              {concept.verbatim}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}

const STEPS = [
  { icon: BookOpen, title: 'Read the page summaries', text: 'Two minutes per topic. Open the original notes only when you want the detail.' },
  { icon: Sparkles, title: 'Look at the picture', text: 'Hard topics have a visual explainer. Tap the numbers on it.' },
  { icon: Layers, title: 'Test yourself', text: 'Flashcards for just this topic. Mark the ones you know.' },
  { icon: PenTool, title: 'Write one answer', text: 'Use the model answer outline, then mark the topic done.' },
];

export default function UniversalVisualNotesView({
  currentVolume,
  currentDataset,
  onSelectScanPage,
  searchQuery,
  jumpTarget,
  onJumpHandled,
  onJumpTo,
  activeScanPage,
  inspectorOpen,
  renderInspector,
  study,
  onStudy,
  onSwitchVolume,
}) {
  const volId = currentVolume.id;
  const { setLastSection } = study;
  const sections = useMemo(() => currentDataset?.sections || [], [currentDataset]);
  const flashcards = currentDataset?.flashcards || [];
  const answers = currentDataset?.answers || [];
  const studySections = sections.filter((s) => !isFrontMatter(s));
  const doneN = studySections.filter((s) => study.isDone(volId, s.id)).length;
  const pct = studySections.length ? Math.round((doneN / studySections.length) * 100) : 0;

  // The topic to study next: the last one opened if it is not done, else the first not done.
  const nextSection = useMemo(() => {
    const last = study.progress.lastSection[volId];
    const lastSec = studySections.find((s) => s.id === last);
    if (lastSec && !study.isDone(volId, lastSec.id)) return lastSec;
    return studySections.find((s) => !study.isDone(volId, s.id)) || null;
  }, [studySections, study, volId]);

  const [openIds, setOpenIds] = useState(() => new Set(nextSection ? [nextSection.id] : []));
  const toggleOpen = (id) => {
    const willOpen = !openIds.has(id);
    setOpenIds((s) => {
      const n = new Set(s);
      if (willOpen) n.add(id);
      else n.delete(id);
      return n;
    });
    if (willOpen) setLastSection(volId, id);
  };

  const scrollToSec = (id) => setTimeout(() => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 80);

  // Sidebar / "Continue" jumps: open the topic, then scroll to it.
  useEffect(() => {
    if (!jumpTarget) return undefined;
    setOpenIds((s) => (s.has(jumpTarget.id) ? s : new Set([...s, jumpTarget.id])));
    setLastSection(volId, jumpTarget.id);
    const t = setTimeout(() => {
      document.getElementById(jumpTarget.id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      onJumpHandled?.();
    }, 120);
    return () => clearTimeout(t);
  }, [jumpTarget, onJumpHandled, setLastSection, volId]);

  const q = (searchQuery || '').trim().toLowerCase();
  const has = (v) => (v || '').toLowerCase().includes(q);
  const conceptMatches = (c) => has(c.title) || has(c.summary) || has(c.verbatim);
  const sectionMetaMatches = (sec) =>
    has(sec.title) || has(sec.subtitle) || (sec.keyScholars || []).some(has) || (sec.coreTheories || []).some(has);

  // With a query every matching topic opens; a topic whose own title/thinkers match shows in full,
  // otherwise only the pages that match.
  const visibleSections = sections
    .map((sec) => {
      if (!q || sectionMetaMatches(sec)) return { sec, concepts: sec.concepts || [] };
      return { sec, concepts: (sec.concepts || []).filter(conceptMatches) };
    })
    .filter(({ concepts }) => !q || concepts.length > 0);
  const matchedConceptTotal = visibleSections.reduce((a, v) => a + v.concepts.length, 0);
  const isOpen = (id) => !!q || openIds.has(id);

  const volumeExplainers = visualExplainers.filter(
    (x) => x.volumeId === volId && (x.image || x.video || x.variants?.some((v) => v.image)) &&
      (!q || has(x.title) || (x.beats || []).some((b) => has(b.label) || has(b.text)))
  );
  const explainersFor = (sec) => volumeExplainers.filter((x) => (sec.scanPages || []).includes(x.anchorPages[0]));
  const explainerSlots = (sec, concepts) => {
    const slots = {};
    explainersFor(sec).forEach((x) => {
      const i = concepts.findIndex((c) => x.anchorPages.includes(c.scanPage));
      const at = i === -1 ? 0 : i;
      (slots[at] = slots[at] || []).push(x);
    });
    return slots;
  };

  // The scan pane sits inside the open topic that contains the scan page, sticky beside its text.
  const openVisible = visibleSections.filter(({ sec }) => isOpen(sec.id));
  const paneSectionId = inspectorOpen && openVisible.length
    ? (openVisible.find(({ sec }) => (sec.scanPages || []).includes(activeScanPage)) || openVisible[0]).sec.id
    : null;
  const prevPaneSection = useRef(paneSectionId);
  useEffect(() => {
    const prev = prevPaneSection.current;
    prevPaneSection.current = paneSectionId;
    if (!prev || !paneSectionId || prev === paneSectionId) return;
    const el = document.getElementById(paneSectionId);
    if (el) {
      const r = el.getBoundingClientRect();
      if (r.bottom < 80 || r.top > window.innerHeight - 80) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, [paneSectionId]);

  const finishTopic = (sec) => {
    if (!study.isDone(volId, sec.id)) study.toggleDone(volId, sec.id);
    const idx = studySections.findIndex((s) => s.id === sec.id);
    const next = studySections.slice(idx + 1).find((s) => !study.isDone(volId, s.id));
    setOpenIds((s) => { const n = new Set(s); n.delete(sec.id); if (next) n.add(next.id); return n; });
    if (next) { setLastSection(volId, next.id); scrollToSec(next.id); }
    else scrollToSec('study-guide');
  };

  const nextVolume = volumesByStep.find((v) => v.step === currentVolume.step + 1);

  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-20">

      {/* Study guide: where this volume sits, how far you are, what to do next */}
      <section id="study-guide" className="scroll-mt-20 relative p-5 sm:p-7 rounded-2xl bg-gradient-to-br from-slate-900 via-slate-900 to-amber-950/30 border border-amber-500/20 shadow-2xl space-y-5">
        <div className="flex flex-wrap items-center gap-2 text-[11px]">
          <span className="px-2.5 py-1 rounded-full font-bold uppercase tracking-wider bg-amber-500/20 text-amber-300 border border-amber-500/40">
            Step {currentVolume.step} of 6
          </span>
          <span className="px-2.5 py-1 rounded-full font-mono bg-slate-800 text-slate-300 border border-slate-700">
            {currentVolume.paperNumber} • {currentVolume.sectionName}
          </span>
          <span className="px-2.5 py-1 rounded-full font-mono bg-slate-800 text-slate-300 border border-slate-700">
            {studySections.length} topics • {currentVolume.totalPages} handwritten pages
          </span>
        </div>

        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-start gap-3">
            <span>{currentVolume.icon}</span> <span>{currentVolume.title}</span>
          </h1>
          <p className="mt-2 text-sm text-slate-300 leading-relaxed max-w-3xl">{currentVolume.whyNow}</p>
        </div>

        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs">
            <span className="font-semibold text-slate-300">Your progress</span>
            <span className="font-mono text-emerald-300">{doneN} of {studySections.length} topics done</span>
          </div>
          <div className="h-2 rounded-full bg-slate-800 overflow-hidden">
            <div className="h-full bg-gradient-to-r from-emerald-500 to-amber-400 transition-all" style={{ width: `${pct}%` }} />
          </div>
        </div>

        <div className="flex flex-wrap gap-2">
          {nextSection ? (
            <button
              onClick={() => onJumpTo(nextSection.id)}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-sm transition cursor-pointer shadow-lg"
            >
              <PlayCircle className="w-4 h-4" />
              {doneN === 0 ? 'Start' : 'Continue'}: Topic {topicNumber(sections, nextSection)}, {nextSection.title.split(':')[0]}
            </button>
          ) : (
            <span className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-emerald-500/15 text-emerald-300 font-bold text-sm border border-emerald-500/30">
              <CheckCircle2 className="w-4 h-4" /> Every topic in this volume is done
            </span>
          )}
          {!nextSection && nextVolume && (
            <button
              onClick={() => onSwitchVolume(nextVolume.id)}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-sm transition cursor-pointer"
            >
              Go to Step {nextVolume.step}: {nextVolume.shortTitle} <ArrowRight className="w-4 h-4" />
            </button>
          )}
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-2 sm:gap-2.5 pt-1">
          {STEPS.map((s, i) => (
            <div key={s.title} className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
              <div className="flex items-center gap-2 text-[11px] sm:text-xs font-bold text-white leading-tight">
                <span className="w-5 h-5 rounded-full bg-amber-500/20 text-amber-300 text-[11px] flex items-center justify-center">{i + 1}</span>
                <s.icon className="w-3.5 h-3.5 text-amber-400" /> {s.title}
              </div>
              <p className="mt-1 text-[11px] text-slate-400 leading-relaxed hidden sm:block">{s.text}</p>
            </div>
          ))}
        </div>

        <p className="text-[11px] text-slate-500 leading-relaxed">
          The summaries, flashcards and answers are written by AI from the handwritten notes, and every page
          links to its original scan. Check the scan whenever a line matters for your answer.
        </p>
      </section>

      {q && (
        <p className="text-xs text-slate-400 font-mono">
          {visibleSections.length
            ? `${matchedConceptTotal} page${matchedConceptTotal === 1 ? '' : 's'} in ${visibleSections.length} topic${visibleSections.length === 1 ? '' : 's'} match "${searchQuery}"`
            : ''}
        </p>
      )}

      {/* Course outline: one row per topic; the open topic shows its pages and study actions */}
      <div className="space-y-3">
        {visibleSections.map(({ sec, concepts }) => {
          const front = isFrontMatter(sec);
          const done = study.isDone(volId, sec.id);
          const open = isOpen(sec.id);
          const hasPane = sec.id === paneSectionId;
          const cat = sectionCardCategory(sec);
          const nCards = flashcards.filter((c) => c.category === cat).length;
          const secAnswers = answers.filter(sectionAnswerMatch(sec));
          const nVisuals = explainersFor(sec).length;
          const slots = open ? explainerSlots(sec, concepts) : {};
          return (
            <section key={sec.id} id={sec.id} className={`scroll-mt-20 rounded-2xl border transition ${
              open ? 'bg-slate-950/40 border-amber-500/30' : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
            }`}>
              {/* Topic row */}
              <button
                onClick={() => toggleOpen(sec.id)}
                className="w-full text-left p-4 sm:p-5 flex items-start gap-3 cursor-pointer"
              >
                <span className="mt-0.5 shrink-0">
                  {done
                    ? <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                    : <Circle className={`w-5 h-5 ${front ? 'text-slate-700' : 'text-slate-500'}`} />}
                </span>
                <span className="min-w-0 flex-1">
                  <span className="flex flex-wrap items-center gap-x-2 gap-y-1 text-[11px] font-mono text-slate-500">
                    <span className="text-amber-400/90 font-bold">{front ? 'Before you start' : `Topic ${topicNumber(sections, sec)}`}</span>
                    <span>{concepts.length} page{concepts.length === 1 ? '' : 's'}</span>
                    {nVisuals > 0 && <span className="text-sky-300">• {nVisuals} visual{nVisuals === 1 ? '' : 's'}</span>}
                    {nCards > 0 && <span>• {nCards} cards</span>}
                    {secAnswers.length > 0 && <span>• {secAnswers.length} answer{secAnswers.length === 1 ? '' : 's'}</span>}
                  </span>
                  <span className={`block mt-0.5 text-base sm:text-lg font-bold leading-snug ${done ? 'text-slate-400' : 'text-white'}`}>
                    {front ? 'Cover, contents and reading list' : sec.title}
                  </span>
                  {!front && sec.subtitle && (
                    <span className="block mt-0.5 text-xs text-slate-400 line-clamp-2">{sec.subtitle}</span>
                  )}
                </span>
                <ChevronDown className={`w-5 h-5 shrink-0 mt-1 text-slate-500 transition ${open ? 'rotate-180' : ''}`} />
              </button>

              {open && (
                <div className={`px-4 sm:px-5 pb-5 ${hasPane ? 'flex items-start gap-6' : ''}`}>
                  <div className="min-w-0 flex-1 space-y-4">
                    {!front && ((sec.keyScholars || []).length > 0 || (sec.coreTheories || []).length > 0) && (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {(sec.keyScholars || []).length > 0 && (
                          <div className="p-3 rounded-xl bg-slate-900/70 border border-slate-800 space-y-2">
                            <div className="flex items-center gap-1.5 text-[11px] font-bold text-amber-400 uppercase tracking-wider">
                              <GraduationCap className="w-4 h-4" /> Thinkers to quote
                            </div>
                            <div className="flex flex-wrap gap-1.5">
                              {sec.keyScholars.map((s) => (
                                <span key={s} className="px-2 py-0.5 rounded text-xs bg-slate-950 text-slate-300 border border-slate-800">{s}</span>
                              ))}
                            </div>
                          </div>
                        )}
                        {(sec.coreTheories || []).length > 0 && (
                          <div className="p-3 rounded-xl bg-slate-900/70 border border-slate-800 space-y-1.5">
                            <div className="flex items-center gap-1.5 text-[11px] font-bold text-indigo-300 uppercase tracking-wider">
                              <Sparkles className="w-4 h-4" /> Big ideas in this topic
                            </div>
                            <ul className="space-y-1">
                              {sec.coreTheories.map((t) => (
                                <li key={t} className="text-xs text-slate-300 flex items-start gap-1.5">
                                  <span className="text-indigo-400">▸</span><span>{t}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    )}

                    {front && (
                      <p className="text-xs text-slate-400">
                        These pages are the notebook's cover, table of contents and reading list. Skim them once, then start Topic 01 below.
                      </p>
                    )}

                    {concepts.map((concept, cIdx) => (
                      <React.Fragment key={concept.scanPage ?? cIdx}>
                        {(slots[cIdx] || []).map((x) => (
                          <VisualExplainer key={x.id} explainer={x} onSelectScanPage={onSelectScanPage} />
                        ))}
                        <PageCard concept={concept} onSelectScanPage={onSelectScanPage} query={q} />
                      </React.Fragment>
                    ))}

                    {!front && (
                      <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-800/80">
                        {nCards > 0 && (
                          <button
                            onClick={() => onStudy('flashcards', { category: cat })}
                            className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-indigo-500/15 hover:bg-indigo-500/25 text-indigo-200 border border-indigo-500/30 text-xs font-semibold transition cursor-pointer"
                          >
                            <Layers className="w-4 h-4" /> Test yourself ({nCards} cards)
                          </button>
                        )}
                        {secAnswers.length > 0 && (
                          <button
                            onClick={() => onStudy('answers', { answerId: secAnswers[0].id })}
                            className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-sky-500/15 hover:bg-sky-500/25 text-sky-200 border border-sky-500/30 text-xs font-semibold transition cursor-pointer"
                          >
                            <PenTool className="w-4 h-4" /> Practice an answer ({secAnswers.length})
                          </button>
                        )}
                        <span className="flex-1" />
                        {done ? (
                          <button
                            onClick={() => study.toggleDone(volId, sec.id)}
                            className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-emerald-300 hover:text-white text-xs font-semibold transition cursor-pointer"
                          >
                            <CheckCircle2 className="w-4 h-4" /> Done (undo)
                          </button>
                        ) : (
                          <button
                            onClick={() => finishTopic(sec)}
                            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-bold transition cursor-pointer"
                          >
                            <CheckCircle2 className="w-4 h-4" /> Mark done, next topic
                          </button>
                        )}
                      </div>
                    )}
                  </div>

                  {hasPane && (
                    <aside className="w-[42%] shrink-0 sticky top-[4.5rem] h-[calc(100vh-5.5rem)] rounded-2xl overflow-hidden border border-slate-800 shadow-2xl">
                      {renderInspector()}
                    </aside>
                  )}
                </div>
              )}
            </section>
          );
        })}

        {visibleSections.length === 0 && (
          <div className="p-12 text-center rounded-2xl bg-slate-900/50 border border-slate-800 space-y-3">
            <Search className="w-8 h-8 text-slate-500 mx-auto" />
            <h3 className="text-base font-bold text-slate-300">Nothing in this volume matches "{searchQuery}"</h3>
            <p className="text-xs text-slate-500">Try a thinker's surname or a key term, or clear the search.</p>
          </div>
        )}
      </div>
    </div>
  );
}
