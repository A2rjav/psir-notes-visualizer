import React from 'react';
import { CheckCircle2, Quote, Lightbulb, Sparkles } from 'lucide-react';

// Motion-graphics scenes for the lesson player. Every scene is plain React + SVG + CSS keyframes
// (index.css, "lp-*"), so labels are exact and nothing needs rendering by an image model.
// `dur` is the narration length in seconds: items are staggered across it so each appears
// roughly when the narrator gets to it.

const BASE = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : `${import.meta.env.BASE_URL}/`;
export const asset = (p) => (p ? `${BASE}${p.replace(/^\/+/, '')}` : p);

const stagger = (i, n, dur, start = 0.4) => `${(start + (i * Math.max(0.5, dur * 0.7)) / Math.max(1, n)).toFixed(2)}s`;
const A = (cls, delay) => ({ className: `lp-anim ${cls}`, style: { animationDelay: delay } });

// Greedy word wrap for SVG labels, `max` characters per line.
const wrapWords = (text, max) => String(text || '').split(/\s+/).filter(Boolean).reduce((lines, word) => {
  const last = lines[lines.length - 1];
  if (last && (last + ' ' + word).length <= max) lines[lines.length - 1] = `${last} ${word}`;
  else lines.push(word);
  return lines;
}, []);

const Heading = ({ children, delay = '0.05s' }) => (
  <h3 {...A('lp-fade-up', delay)} className="lp-anim lp-fade-up text-lg sm:text-2xl font-extrabold text-white text-center tracking-tight">
    {children}
  </h3>
);

const TONES = {
  self: { fill: '#f59e0b', text: '#1e1b4b', stroke: '#fbbf24' },
  enemy: { fill: '#7f1d1d', text: '#fecaca', stroke: '#ef4444' },
  friend: { fill: '#064e3b', text: '#a7f3d0', stroke: '#10b981' },
  neutral: { fill: '#1e293b', text: '#cbd5e1', stroke: '#64748b' },
};

export function HookScene({ scene }) {
  return (
    <div className="h-full flex flex-col items-center justify-center text-center gap-5 px-4">
      <span {...A('lp-pop', '0.1s')} className="lp-anim lp-pop w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-amber-500 text-slate-950 text-4xl sm:text-5xl font-black flex items-center justify-center lp-pulse">?</span>
      <span {...A('lp-fade-up', '0.3s')} className="lp-anim lp-fade-up text-[11px] uppercase tracking-[0.25em] text-amber-300 font-bold">The big question</span>
      <p {...A('lp-fade-up', '0.55s')} className="lp-anim lp-fade-up max-w-3xl text-xl sm:text-3xl font-extrabold text-white leading-snug">{scene.text}</p>
    </div>
  );
}

export function AnalogyScene({ scene }) {
  return (
    <div className="h-full flex flex-col sm:flex-row items-center justify-center gap-5 sm:gap-10 px-4">
      <span {...A('lp-pop', '0.1s')} className="lp-anim lp-pop text-6xl sm:text-8xl"><span className="inline-block lp-float">{scene.emoji || '💡'}</span></span>
      <div {...A('lp-slide-right', '0.45s')} className="lp-anim lp-slide-right max-w-xl p-5 rounded-2xl bg-sky-500/10 border border-sky-400/40">
        <div className="flex items-center gap-1.5 text-[11px] uppercase tracking-[0.2em] text-sky-300 font-bold mb-2">
          <Lightbulb className="w-3.5 h-3.5" /> Think of it like this
        </div>
        <p className="text-base sm:text-2xl font-bold text-white leading-snug">{scene.text}</p>
      </div>
    </div>
  );
}

export function PointsScene({ scene, dur }) {
  const items = scene.items || [];
  return (
    <div className="h-full flex flex-col justify-center gap-4 sm:gap-6 px-4 sm:px-10">
      <Heading>{scene.heading}</Heading>
      <ul className="space-y-2.5 sm:space-y-3 max-w-2xl mx-auto w-full">
        {items.map((t, i) => (
          <li key={i} {...A('lp-slide-left', stagger(i, items.length, dur))}
            className="lp-anim lp-slide-left flex items-start gap-3 p-3 sm:p-3.5 rounded-xl bg-slate-900/80 border border-slate-700/80">
            <CheckCircle2 className="w-5 h-5 sm:w-6 sm:h-6 text-emerald-400 shrink-0" />
            <span className="text-sm sm:text-lg text-slate-100 font-semibold leading-snug">{t}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function ThinkerScene({ scene, portrait }) {
  const initials = String(scene.name || '?').split(/\s+/).filter((w) => /^[A-Z]/.test(w)).slice(0, 2).map((w) => w[0]).join('');
  return (
    <div className="h-full flex flex-col sm:flex-row items-center justify-center gap-5 sm:gap-10 px-4">
      <div {...A('lp-pop', '0.1s')} className="lp-anim lp-pop relative">
        <svg viewBox="0 0 120 120" className="w-28 h-28 sm:w-40 sm:h-40">
          <circle cx="60" cy="60" r="56" fill="none" stroke="#f59e0b" strokeWidth="3" className="lp-draw" style={{ '--lp-len': 352 }} />
        </svg>
        <div className="absolute inset-3 rounded-full overflow-hidden bg-gradient-to-br from-amber-500 to-orange-700 flex items-center justify-center text-3xl sm:text-5xl font-black text-white">
          {portrait ? <img src={asset(portrait)} alt={scene.name} className="w-full h-full object-cover" /> : initials}
        </div>
      </div>
      <div className="max-w-xl text-center sm:text-left space-y-3">
        <p {...A('lp-fade-up', '0.35s')} className="lp-anim lp-fade-up text-2xl sm:text-4xl font-extrabold text-white">{scene.name}</p>
        {scene.work && (
          <span {...A('lp-fade-up', '0.55s')} className="lp-anim lp-fade-up inline-block px-2.5 py-1 rounded-full text-xs sm:text-sm font-semibold bg-indigo-500/20 text-indigo-200 border border-indigo-400/30">{scene.work}</span>
        )}
        <p {...A('lp-fade-up', '0.8s')} className="lp-anim lp-fade-up text-base sm:text-xl text-amber-100 leading-snug font-medium">“{scene.idea}”</p>
      </div>
    </div>
  );
}

export function CompareScene({ scene, dur }) {
  const cols = (scene.columns || []).slice(0, 3);
  const palette = ['border-amber-400/60 bg-amber-500/10', 'border-sky-400/60 bg-sky-500/10', 'border-emerald-400/60 bg-emerald-500/10'];
  return (
    <div className="h-full flex flex-col justify-center gap-4 px-3 sm:px-8">
      <Heading>{scene.heading}</Heading>
      <div className={`grid gap-3 sm:gap-5 ${cols.length === 3 ? 'grid-cols-3' : 'grid-cols-2'} relative`}>
        {cols.map((c, ci) => (
          <div key={ci} {...A(ci === 0 ? 'lp-slide-left' : 'lp-slide-right', `${0.3 + ci * 0.35}s`)}
            className={`lp-anim ${ci === 0 ? 'lp-slide-left' : 'lp-slide-right'} rounded-2xl border-2 p-3 sm:p-4 ${palette[ci]}`}>
            <p className="text-sm sm:text-xl font-extrabold text-white text-center mb-2">{c.title}</p>
            <ul className="space-y-1.5">
              {(c.items || []).map((t, i) => (
                <li key={i} {...A('lp-fade-up', stagger(i + ci * 3, cols.length * 3, dur, 0.9))}
                  className="lp-anim lp-fade-up text-xs sm:text-base text-slate-100 leading-snug flex gap-1.5">
                  <span className="text-amber-300">•</span><span>{t}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
        {cols.length === 2 && (
          <span {...A('lp-pop', '0.75s')} className="lp-anim lp-pop absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-slate-950 border-2 border-white/70 text-white text-xs sm:text-sm font-black flex items-center justify-center">VS</span>
        )}
      </div>
    </div>
  );
}

export function TimelineScene({ scene, dur }) {
  const ev = (scene.events || []).slice(0, 6);
  return (
    <div className="h-full flex flex-col justify-center gap-6 px-3 sm:px-8">
      <Heading>{scene.heading}</Heading>
      <div className="relative pt-14 pb-14">
        <div className="lp-grow-x absolute left-0 right-0 top-1/2 h-1 rounded bg-gradient-to-r from-amber-500 via-sky-400 to-emerald-400" style={{ animationDelay: '0.2s' }} />
        <div className="relative flex justify-between">
          {ev.map((e, i) => {
            const d = stagger(i, ev.length, dur, 0.6);
            const up = i % 2 === 0;
            return (
              <div key={i} className="relative flex flex-col items-center" style={{ width: `${100 / ev.length}%` }}>
                <span {...A('lp-pop', d)} className="lp-anim lp-pop w-4 h-4 sm:w-5 sm:h-5 rounded-full bg-white border-4 border-amber-500 z-10" />
                <div {...A('lp-fade-up', d)} className={`lp-anim lp-fade-up absolute ${up ? 'bottom-6' : 'top-6'} w-full px-1 text-center`}>
                  <p className="text-xs sm:text-base font-extrabold text-amber-300">{e.when}</p>
                  <p className="text-[10px] sm:text-sm text-slate-200 leading-tight">{e.what}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export function CycleScene({ scene, dur }) {
  const nodes = (scene.nodes || []).slice(0, 6);
  const n = nodes.length;
  const R = 120;
  const pos = nodes.map((_, i) => {
    const a = -Math.PI / 2 + (i * 2 * Math.PI) / n;
    return [200 + R * Math.cos(a), 160 + R * Math.sin(a)];
  });
  return (
    <div className="h-full flex flex-col justify-center gap-2 px-2">
      <Heading>{scene.heading}</Heading>
      <svg viewBox="0 0 400 320" className="w-full max-h-[70%]">
        <circle cx="200" cy="160" r={R} fill="none" stroke="#334155" strokeWidth="2" />
        <circle cx="200" cy="160" r={R} fill="none" stroke="#f59e0b" strokeWidth="3" className="lp-dash-flow" />
        <circle r="7" fill="#fbbf24">
          <animateMotion dur="4s" repeatCount="indefinite" path={`M200,${160 - R} a${R},${R} 0 1,1 -0.1,0`} />
        </circle>
        {pos.map(([x, y], i) => {
          // SVG text does not wrap: break long labels into lines and size the box to fit them.
          const lines = wrapWords(nodes[i], 14).slice(0, 3);
          const w = Math.max(110, Math.max(...lines.map((l) => l.length)) * 8.4 + 22);
          const h = lines.length * 17 + 18;
          return (
            <g key={i} className="lp-anim lp-pop" style={{ animationDelay: stagger(i, n, dur), transformOrigin: `${x}px ${y}px` }}>
              <rect x={x - w / 2} y={y - h / 2} width={w} height={h} rx="12" fill="#0f172a" stroke="#38bdf8" strokeWidth="2" />
              {lines.map((l, k) => (
                <text key={k} x={x} y={y - ((lines.length - 1) * 17) / 2 + k * 17 + 5} textAnchor="middle" fill="#e2e8f0" fontSize="14" fontWeight="700">{l}</text>
              ))}
            </g>
          );
        })}
      </svg>
    </div>
  );
}

export function FlowScene({ scene, dur }) {
  const steps = (scene.steps || []).slice(0, 5);
  return (
    <div className="h-full flex flex-col justify-center gap-5 px-3 sm:px-8">
      <Heading>{scene.heading}</Heading>
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-center gap-2 sm:gap-1">
        {steps.map((s, i) => (
          <React.Fragment key={i}>
            <div {...A('lp-pop', stagger(i, steps.length, dur))}
              className="lp-anim lp-pop flex-1 min-w-0 p-2.5 sm:p-3 rounded-xl bg-gradient-to-br from-indigo-500/25 to-slate-900 border border-indigo-400/50 text-center">
              <span className="block text-[10px] font-mono text-indigo-300">STEP {i + 1}</span>
              <span className="block text-xs sm:text-base font-bold text-white leading-snug">{s}</span>
            </div>
            {i < steps.length - 1 && (
              <span {...A('lp-fade-up', stagger(i + 0.5, steps.length, dur))} className="lp-anim lp-fade-up text-amber-400 text-xl sm:text-2xl font-black text-center rotate-90 sm:rotate-0">➜</span>
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}

export function RingsScene({ scene, dur }) {
  const rings = (scene.rings || []).slice(0, 6);
  const n = rings.length;
  const maxR = 140;
  return (
    <div className="h-full flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-8 px-3">
      <svg viewBox="0 0 320 320" className="w-[78%] sm:w-auto sm:h-[88%] max-h-full">
        {[...rings].map((r, i) => i).reverse().map((i) => {
          const rad = maxR * ((i + 1) / n);
          const t = TONES[rings[i].tone] || TONES.neutral;
          return (
            <circle key={i} cx="160" cy="160" r={rad} fill={t.fill} stroke={t.stroke} strokeWidth="2"
              className="lp-anim lp-ring-in" style={{ animationDelay: stagger(i, n, dur), transformOrigin: '160px 160px' }} />
          );
        })}
        {(() => {
          // Label the centre only when it fits inside the innermost circle; the legend names it anyway.
          const inner = (2 * maxR * 0.78) / n; // usable width inside the centre circle
          const lines = wrapWords(rings[0]?.label, Math.floor(inner / 7.2));
          if (!lines.length || lines.length > 3) return null;
          const size = Math.min(13, inner / (Math.max(...lines.map((l) => l.length)) * 0.62)); // shrink a long single word
          return lines.map((l, k) => (
            <text key={k} x="160" y={160 - ((lines.length - 1) * (size + 2)) / 2 + k * (size + 2) + size * 0.38} textAnchor="middle" fill="#1e1b4b" fontSize={size.toFixed(1)} fontWeight="800">{l}</text>
          ));
        })()}
      </svg>
      <div className="space-y-1.5 w-full sm:w-auto">
        <Heading>{scene.heading}</Heading>
        {rings.map((r, i) => {
          const t = TONES[r.tone] || TONES.neutral;
          return (
            <div key={i} {...A('lp-slide-right', stagger(i, n, dur))} className="lp-anim lp-slide-right flex items-center gap-2 text-xs sm:text-base">
              <span className="w-3.5 h-3.5 rounded-full shrink-0" style={{ background: t.stroke }} />
              <span className="text-slate-400 font-mono text-[0.8em] w-14 shrink-0 whitespace-nowrap">{i === 0 ? 'centre' : `ring ${i}`}</span>
              <span className="font-bold text-white">{r.label}</span>
              <span className="text-[10px] uppercase tracking-wider" style={{ color: t.stroke }}>{r.tone}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export function MatrixScene({ scene, dur }) {
  const [hr, hc] = scene.highlight || [-1, -1];
  return (
    <div className="h-full flex flex-col justify-center gap-4 px-3 sm:px-10">
      <Heading>{scene.heading}</Heading>
      <div className="grid grid-cols-[auto_1fr_1fr] gap-2 sm:gap-3 max-w-2xl mx-auto w-full">
        <span />
        {(scene.cols || []).map((c, j) => (
          <span key={j} {...A('lp-fade-up', '0.3s')} className="lp-anim lp-fade-up text-center text-[11px] sm:text-sm font-bold text-sky-300 uppercase tracking-wider">{c}</span>
        ))}
        {(scene.rows || []).map((r, i) => (
          <React.Fragment key={i}>
            <span {...A('lp-fade-up', '0.3s')} className="lp-anim lp-fade-up self-center text-right text-[11px] sm:text-sm font-bold text-amber-300 uppercase tracking-wider pr-1">{r}</span>
            {(scene.cells?.[i] || []).map((cell, j) => {
              const hot = i === hr && j === hc;
              return (
                <div key={j} {...A('lp-pop', stagger(i * 2 + j, 4, dur, 0.6))}
                  className={`lp-anim lp-pop p-3 sm:p-5 rounded-xl text-center text-xs sm:text-lg font-bold leading-snug border-2 ${
                    hot ? 'bg-amber-500 text-slate-950 border-amber-300 lp-pulse' : 'bg-slate-900/80 text-slate-100 border-slate-700'
                  }`}>
                  {cell}
                </div>
              );
            })}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}

export function PyramidScene({ scene, dur }) {
  const levels = (scene.levels || []).slice(0, 4);
  const n = levels.length;
  const colors = ['from-amber-400 to-amber-600', 'from-sky-400 to-sky-600', 'from-indigo-400 to-indigo-600', 'from-emerald-500 to-emerald-700'];
  return (
    <div className="h-full flex flex-col justify-center gap-3 px-3">
      <Heading>{scene.heading}</Heading>
      <div className="flex flex-col items-center gap-1.5">
        {levels.map((l, i) => (
          <div key={i} {...A('lp-fade-up', stagger(n - 1 - i, n, dur))}
            className={`lp-anim lp-fade-up bg-gradient-to-r ${colors[i % 4]} text-slate-950 font-extrabold text-center py-2.5 sm:py-3.5 rounded-lg text-xs sm:text-lg shadow-lg`}
            style={{ width: `${38 + (i * 58) / Math.max(1, n - 1)}%` }}>
            {l}
          </div>
        ))}
      </div>
    </div>
  );
}

// One pan of the balance: a label box sitting on its string at y=112, growing upward with the text.
function Pan({ cx, label, stroke, delay }) {
  const lines = wrapWords(label, 15).slice(0, 3);
  const h = lines.length * 17 + 16;
  return (
    <g className="lp-anim lp-pop" style={{ animationDelay: delay, transformOrigin: `${cx}px 90px` }}>
      <rect x={cx - 70} y={112 - h} width="140" height={h} rx="10" fill="#0f172a" stroke={stroke} strokeWidth="2" />
      {lines.map((l, k) => (
        <text key={k} x={cx} y={112 - h + 22 + k * 17} textAnchor="middle" fill="#e2e8f0" fontSize="14" fontWeight="700">{l}</text>
      ))}
    </g>
  );
}

export function BalanceScene({ scene }) {
  const tilt = scene.tilt === 'left' ? 'lp-tilt-left' : scene.tilt === 'right' ? 'lp-tilt-right' : null;
  return (
    <div className="h-full flex flex-col justify-center gap-2 px-2">
      <Heading>{scene.heading}</Heading>
      <svg viewBox="0 0 400 240" className="w-full max-h-[72%]">
        <polygon points="200,150 175,215 225,215" fill="#475569" />
        <g style={{ transformOrigin: '200px 150px', animation: tilt ? `${tilt} 1.4s 0.9s cubic-bezier(.3,1.4,.5,1) both` : undefined }}>
          <rect x="40" y="144" width="320" height="10" rx="5" fill="#f59e0b" />
          <line x1="70" y1="150" x2="70" y2="110" stroke="#94a3b8" strokeWidth="2" />
          <line x1="330" y1="150" x2="330" y2="110" stroke="#94a3b8" strokeWidth="2" />
          <Pan cx={70} label={scene.left} stroke="#38bdf8" delay="0.3s" />
          <Pan cx={330} label={scene.right} stroke="#34d399" delay="0.55s" />
        </g>
      </svg>
    </div>
  );
}

export function QuoteScene({ scene }) {
  return (
    <div className="h-full flex flex-col items-center justify-center text-center gap-4 px-6">
      <Quote {...A('lp-pop', '0.1s')} className="lp-anim lp-pop w-12 h-12 sm:w-16 sm:h-16 text-amber-400" />
      <p {...A('lp-fade-up', '0.35s')} className="lp-anim lp-fade-up font-serif-quote italic text-xl sm:text-3xl text-white leading-snug max-w-3xl">“{scene.quote}”</p>
      <p {...A('lp-fade-up', '0.8s')} className="lp-anim lp-fade-up text-sm sm:text-lg text-amber-300 font-bold">— {scene.by}</p>
    </div>
  );
}

export function RecapScene({ scene, dur }) {
  const items = (scene.items || []).slice(0, 3);
  return (
    <div className="h-full flex flex-col justify-center gap-4 px-3 sm:px-8">
      <p {...A('lp-fade-up', '0.05s')} className="lp-anim lp-fade-up text-center text-[11px] uppercase tracking-[0.25em] text-emerald-300 font-bold flex items-center justify-center gap-1.5">
        <Sparkles className="w-3.5 h-3.5" /> Remember these three
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 sm:gap-4">
        {items.map((t, i) => (
          <div key={i} {...A('lp-pop', stagger(i, items.length, dur))}
            className="lp-anim lp-pop p-3 sm:p-5 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-slate-900 border border-emerald-400/50 flex sm:flex-col items-center sm:items-start gap-3">
            <span className="w-9 h-9 sm:w-11 sm:h-11 rounded-full bg-emerald-400 text-slate-950 text-lg sm:text-xl font-black flex items-center justify-center shrink-0">{i + 1}</span>
            <span className="text-sm sm:text-lg font-bold text-white leading-snug">{t}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// The topic's AI picture (Ken Burns pan) with its numbered points appearing one by one, or its clip.
export function VisualScene({ scene, dur }) {
  const ex = scene.explainer;
  const still = ex.image || ex.variants?.[0]?.image;
  const beats = (ex.beats || ex.variants?.[0]?.beats || []).filter((b) => typeof b.x === 'number').slice(0, 5);
  if (scene.useVideo && ex.video) {
    return (
      <div className="h-full flex items-center justify-center bg-black">
        <video src={asset(ex.video)} poster={asset(still)} autoPlay muted loop playsInline className="max-h-full max-w-full" />
      </div>
    );
  }
  const legend = (cls) => (
    <div className={cls}>
      {beats.map((b, i) => (
        <span key={i} className="lp-anim lp-fade-up px-2 py-1 rounded-lg bg-slate-950/85 border border-amber-400/40 text-[11px] sm:text-xs text-amber-100 font-semibold"
          style={{ animationDelay: stagger(i, beats.length, dur) }}>
          {i + 1}. {b.label}
        </span>
      ))}
    </div>
  );
  // The picture keeps its 16:9 frame so the numbered hotspots stay on the right spots. On a phone's
  // tall stage the legend sits under the picture instead of covering it.
  return (
    <div className="h-full flex flex-col justify-center gap-3 bg-black">
      <div className="relative w-full aspect-video sm:aspect-auto sm:h-full overflow-hidden">
        <img src={asset(still)} alt={ex.alt || ex.title} className="absolute inset-0 w-full h-full object-cover lp-ken-burns" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-black/30" />
        {beats.map((b, i) => (
          <span key={i}
            className="lp-anim lp-pop absolute -translate-x-1/2 -translate-y-1/2 w-7 h-7 sm:w-9 sm:h-9 rounded-full bg-amber-400 text-slate-950 text-xs sm:text-sm font-black border-2 border-white shadow-lg flex items-center justify-center"
            style={{ left: `${b.x}%`, top: `${b.y}%`, animationDelay: stagger(i, beats.length, dur) }}>
            {i + 1}
          </span>
        ))}
        {legend('hidden sm:flex absolute left-5 right-5 bottom-3 flex-wrap gap-1.5')}
      </div>
      {legend('sm:hidden flex flex-wrap gap-1.5 px-3')}
    </div>
  );
}

export const SCENES = {
  hook: HookScene,
  analogy: AnalogyScene,
  points: PointsScene,
  thinker: ThinkerScene,
  compare: CompareScene,
  timeline: TimelineScene,
  cycle: CycleScene,
  flow: FlowScene,
  rings: RingsScene,
  matrix: MatrixScene,
  pyramid: PyramidScene,
  balance: BalanceScene,
  quote: QuoteScene,
  recap: RecapScene,
  visual: VisualScene,
};
