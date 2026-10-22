import React, { useState } from 'react';
import { Network, Eye, Users, Lightbulb, Star } from 'lucide-react';

// Concept map for one topic at a time: the topic in the centre, three branches (key thinkers, core
// ideas, and the lesson's three things to remember), then the topic's pages in order. Clicking a
// thinker or idea opens the first scan page that mentions it.

const GRID_COLS = { 1: 'md:grid-cols-1', 2: 'md:grid-cols-2', 3: 'md:grid-cols-3' };

const BRANCH_STYLE = {
  thinkers: { icon: Users, head: 'border-sky-500/70 text-sky-200 bg-sky-500/10', chip: 'border-sky-500/30 text-sky-100 hover:border-sky-400' },
  ideas: { icon: Lightbulb, head: 'border-amber-500/70 text-amber-200 bg-amber-500/10', chip: 'border-amber-500/30 text-amber-100 hover:border-amber-400' },
  remember: { icon: Star, head: 'border-emerald-500/70 text-emerald-200 bg-emerald-500/10', chip: 'border-emerald-500/30 text-emerald-100' },
};

// First page of the topic whose title or transcript mentions the term (by its last, most specific word).
const findPage = (concepts, term) => {
  const words = String(term).split(/\s+/).filter((w) => w.length >= 4);
  const key = (words[words.length - 1] || term).toLowerCase();
  const hit = concepts.find((c) => `${c.title} ${c.verbatim || ''}`.toLowerCase().includes(key));
  return hit?.scanPage;
};

const isFront = (title) => /^contents\b|front matter/i.test(title || '');

export default function MindMapView({ onSelectScanPage, currentDataset, currentVolume }) {
  const sections = currentDataset?.sections || [];
  const [activeId, setActiveId] = useState((sections.find((s) => !isFront(s.title)) || sections[0])?.id || '');
  const sec = sections.find((s) => s.id === activeId) || sections[0];

  if (!sec) {
    return <div className="p-8 text-center text-slate-500 text-sm">No topics in this volume yet.</div>;
  }

  const concepts = sec.concepts || [];
  const recap = (sec.lesson?.scenes || []).find((s) => s.type === 'recap')?.items || [];
  const branches = [
    { key: 'thinkers', label: 'Key thinkers', items: sec.keyScholars || [] },
    { key: 'ideas', label: 'Core ideas', items: sec.coreTheories || [] },
    { key: 'remember', label: 'Remember', items: recap },
  ].filter((b) => b.items.length);
  const n = branches.length;

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-16">
      {/* Header */}
      <div className="p-5 sm:p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl">
        <div className="flex items-center gap-2 mb-1">
          <Network className="w-5 h-5 text-amber-400" />
          <h2 className="text-xl font-bold text-white">Concept Map</h2>
        </div>
        <p className="text-xs text-slate-400">
          {currentVolume?.shortTitle || 'PSIR Notes'} • One topic at a time: who, what, and the three things to remember. Tap a name or idea to see it in the notes.
        </p>
      </div>

      {/* Topic picker */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
        {sections.filter((s) => !isFront(s.title)).map((s) => (
          <button key={s.id} onClick={() => setActiveId(s.id)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium transition whitespace-nowrap cursor-pointer ${
              s.id === sec.id
                ? 'bg-amber-500 text-slate-950 font-bold shadow-md shadow-amber-500/10'
                : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800'
            }`}>
            {s.number}. {s.title.length > 36 ? `${s.title.slice(0, 35).trim()}…` : s.title}
          </button>
        ))}
      </div>

      {/* The map */}
      <div key={sec.id} className="relative p-5 sm:p-8 rounded-3xl bg-slate-900/90 border border-slate-800 shadow-2xl overflow-hidden">
        <div className="mx-auto w-fit max-w-xl text-center px-5 py-3 rounded-2xl bg-gradient-to-br from-amber-400 to-orange-600 text-slate-950 shadow-lg shadow-amber-500/20 lp-anim lp-pop">
          <p className="text-[10px] font-mono font-bold uppercase tracking-wider opacity-70">Topic {sec.number}</p>
          <p className="text-base sm:text-lg font-extrabold leading-snug">{sec.title}</p>
        </div>

        {n > 0 && (
          <>
            <div className="mx-auto w-0.5 h-6 bg-slate-600" />
            <div className={`relative grid gap-6 md:gap-4 ${GRID_COLS[n]}`}>
              {/* the bar joining the branches, from the first column's centre to the last's */}
              {n > 1 && (
                <span className="hidden md:block absolute top-0 h-0.5 bg-slate-600"
                  style={{ left: `${50 / n}%`, right: `${50 / n}%` }} />
              )}
              {branches.map((b, bi) => {
                const st = BRANCH_STYLE[b.key];
                const Icon = st.icon;
                return (
                  <div key={b.key} className="relative flex flex-col items-center md:pt-6">
                    <span className="hidden md:block absolute top-0 left-1/2 w-0.5 h-6 bg-slate-600" />
                    <div className={`lp-anim lp-pop flex items-center gap-1.5 px-3 py-1.5 rounded-xl border-2 text-xs sm:text-sm font-bold ${st.head}`}
                      style={{ animationDelay: `${0.15 + bi * 0.15}s` }}>
                      <Icon className="w-4 h-4" /> {b.label}
                    </div>
                    <div className="w-0.5 h-3 bg-slate-700" />
                    <div className={`flex ${b.key === 'remember' ? 'flex-col items-stretch' : 'flex-wrap justify-center'} gap-1.5 w-full`}>
                      {b.items.map((item, i) => {
                        const page = b.key === 'remember' ? null : findPage(concepts, item);
                        const cls = `lp-anim lp-fade-up px-2.5 py-1.5 rounded-lg border bg-slate-950/70 text-xs text-left transition ${st.chip}`;
                        const style = { animationDelay: `${0.35 + bi * 0.15 + i * 0.06}s` };
                        return page ? (
                          <button key={i} onClick={() => onSelectScanPage(page)} title={`Open scan page ${page}`}
                            className={`${cls} cursor-pointer inline-flex items-center gap-1`} style={style}>
                            {item} <Eye className="w-3 h-3 opacity-60" />
                          </button>
                        ) : (
                          <span key={i} className={cls} style={style}>{b.key === 'remember' ? `${i + 1}. ` : ''}{item}</span>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>
          </>
        )}
      </div>

      {/* Page by page */}
      <div className="space-y-3">
        <h3 className="text-sm font-bold text-slate-300">Page by page <span className="text-slate-500 font-normal">({concepts.length} pages, {sec.notebookPages})</span></h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {concepts.map((c, i) => (
            <button key={i} onClick={() => onSelectScanPage(c.scanPage)}
              className="text-left p-4 rounded-2xl bg-slate-950/80 border border-slate-800 hover:border-amber-500/40 transition space-y-1.5 group cursor-pointer">
              <div className="flex items-center gap-2">
                <span className="px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 font-mono text-[10px] font-bold border border-amber-500/20 shrink-0">p.{c.scanPage}</span>
                <span className="text-xs sm:text-sm font-bold text-white group-hover:text-amber-300 transition">{c.title}</span>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed">{c.summary}</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
