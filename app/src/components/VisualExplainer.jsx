import React, { useState } from 'react';
import { Clapperboard, Image as ImageIcon, Eye, Lightbulb, PenLine, HelpCircle } from 'lucide-react';

// Media paths in visualExplainers.js are written from the site root ('/explainers/x.jpg'). On GitHub
// Pages the app lives under /psir-notes-visualizer/, so resolve them against Vite's base URL.
const BASE = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : `${import.meta.env.BASE_URL}/`;
const asset = (p) => (p ? `${BASE}${p.replace(/^\/+/, '')}` : p);

// One AI-generated visual (image or short video) for a topic students find hard.
// Labels are NOT baked into the media (AI art garbles text); numbered hotspots and the
// "what you're seeing" beats are drawn here, so they stay exact and editable.
export default function VisualExplainer({ explainer, onSelectScanPage, compact = false }) {
  const [activeBeat, setActiveBeat] = useState(null);
  const [variantIdx, setVariantIdx] = useState(0);
  const [mode, setMode] = useState('image'); // 'image' (still + hotspots) | 'video' (the clip)
  // `variants` = two or more stills to compare (e.g. Hobbes vs Rousseau); each may carry its own beats.
  // A clip can sit on the explainer (shared by all variants) or on one variant.
  const variant = explainer.variants?.[variantIdx];
  const e = variant ? { ...explainer, ...variant, video: variant.video ?? explainer.video } : explainer;
  const isVideo = mode === 'video' && !!e.video;
  const beats = isVideo ? (e.videoBeats || e.beats || []) : (e.beats || []);
  const hotspots = isVideo ? [] : beats.filter((b) => typeof b.x === 'number' && typeof b.y === 'number');

  return (
    <div className="rounded-2xl border border-sky-500/30 bg-gradient-to-br from-sky-950/50 via-slate-900 to-slate-900 shadow-xl overflow-hidden">
      {/* Header */}
      <div className="px-5 pt-4 pb-3 flex flex-wrap items-start justify-between gap-2">
        <div className="space-y-1 min-w-0">
          <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-sky-500/20 text-sky-300 border border-sky-500/30">
            {isVideo ? <Clapperboard className="w-3 h-3" /> : <ImageIcon className="w-3 h-3" />}
            Visual explainer
          </span>
          <h3 className="text-base sm:text-lg font-bold text-white">{e.title}</h3>
          {e.whyHard && !compact && (
            <p className="text-xs text-slate-400 flex items-start gap-1.5">
              <HelpCircle className="w-3.5 h-3.5 mt-0.5 shrink-0 text-sky-400" />
              <span><strong className="text-slate-300">Why this feels hard:</strong> {e.whyHard}</span>
            </p>
          )}
        </div>
      </div>

      {(explainer.variants?.length > 1 || e.video) && (
        <div className="px-5 pb-3 flex flex-wrap items-center gap-1.5">
          {explainer.variants?.length > 1 && explainer.variants.map((v, i) => (
            <button
              key={v.label}
              onClick={() => { setVariantIdx(i); setMode('image'); setActiveBeat(null); }}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
                i === variantIdx && !isVideo ? 'bg-sky-500 text-slate-950' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              {v.label}
            </button>
          ))}
          {e.video && (
            <>
              {!explainer.variants?.length && (
                <button
                  onClick={() => { setMode('image'); setActiveBeat(null); }}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer inline-flex items-center gap-1.5 ${
                    !isVideo ? 'bg-sky-500 text-slate-950' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                  }`}
                >
                  <ImageIcon className="w-3.5 h-3.5" /> Picture (tap the numbers)
                </button>
              )}
              <button
                onClick={() => { setMode('video'); setActiveBeat(null); }}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer inline-flex items-center gap-1.5 ${
                  isVideo ? 'bg-amber-500 text-slate-950' : 'bg-slate-800 text-amber-300 hover:bg-slate-700'
                }`}
              >
                <Clapperboard className="w-3.5 h-3.5" /> {e.videoLabel || 'Watch the 8-second clip'}
              </button>
            </>
          )}
        </div>
      )}

      {/* Media with numbered hotspots */}
      <div className="relative bg-black">
        {isVideo ? (
          <video
            src={asset(e.video)}
            poster={asset(e.image)}
            key={asset(e.video)}
            controls
            autoPlay
            loop
            muted
            playsInline
            preload="metadata"
            className="w-full h-auto block"
          />
        ) : (
          <img src={asset(e.image)} alt={e.alt || e.title} loading="lazy" className="w-full h-auto block select-none" draggable={false} />
        )}
        {!isVideo && hotspots.map((b) => {
          const n = beats.indexOf(b) + 1;
          const on = activeBeat === n;
          return (
            <button
              key={n}
              onClick={() => setActiveBeat(on ? null : n)}
              style={{ left: `${b.x}%`, top: `${b.y}%` }}
              className={`absolute -translate-x-1/2 -translate-y-1/2 w-7 h-7 rounded-full text-xs font-bold border-2 shadow-lg transition cursor-pointer ${
                on ? 'bg-amber-400 text-slate-950 border-white scale-110' : 'bg-slate-950/80 text-amber-300 border-amber-400 hover:bg-amber-500 hover:text-slate-950'
              }`}
              title={b.label}
            >
              {n}
            </button>
          );
        })}
        {!isVideo && activeBeat && (
          <div className="absolute left-3 right-3 bottom-3 sm:left-auto sm:max-w-sm p-3 rounded-xl bg-slate-950/90 border border-amber-500/40 text-xs text-slate-200 shadow-2xl">
            <strong className="text-amber-300">{activeBeat}. {beats[activeBeat - 1].label}</strong>
            <p className="mt-1 leading-relaxed">{beats[activeBeat - 1].text}</p>
          </div>
        )}
      </div>

      {/* Beats: what each part of the picture means */}
      <div className="p-5 space-y-4">
        {beats.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Eye className="w-3.5 h-3.5 text-sky-400" /> {isVideo ? "What happens in the clip" : "What you're seeing"}
            </h4>
            <ol className="space-y-1.5">
              {beats.map((b, i) => (
                <li
                  key={i}
                  onMouseEnter={() => !isVideo && hotspots.includes(b) && setActiveBeat(i + 1)}
                  className={`text-xs sm:text-sm flex items-start gap-2.5 p-2 rounded-lg border transition ${
                    activeBeat === i + 1 ? 'bg-amber-500/10 border-amber-500/40' : 'bg-slate-950/30 border-slate-800/60'
                  }`}
                >
                  <span className="w-5 h-5 shrink-0 rounded-full bg-amber-500/15 text-amber-300 text-[11px] font-bold flex items-center justify-center">{i + 1}</span>
                  <span className="text-slate-300 leading-relaxed"><strong className="text-white">{b.label}:</strong> {b.text}</span>
                </li>
              ))}
            </ol>
          </div>
        )}

        {(e.remember || e.examUse) && (
          <div className="grid gap-3 sm:grid-cols-2">
            {e.remember && (
              <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/30">
                <div className="text-[11px] font-bold uppercase tracking-wider text-amber-300 flex items-center gap-1.5 mb-1">
                  <Lightbulb className="w-3.5 h-3.5" /> Remember it as
                </div>
                <p className="text-xs sm:text-sm text-slate-200 leading-relaxed">{e.remember}</p>
              </div>
            )}
            {e.examUse && (
              <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30">
                <div className="text-[11px] font-bold uppercase tracking-wider text-emerald-300 flex items-center gap-1.5 mb-1">
                  <PenLine className="w-3.5 h-3.5" /> Use it in the exam
                </div>
                <p className="text-xs sm:text-sm text-slate-200 leading-relaxed">{e.examUse}</p>
              </div>
            )}
          </div>
        )}

        {e.anchorPages?.length > 0 && onSelectScanPage && (
          <div className="flex flex-wrap items-center gap-1.5 text-[11px] text-slate-400">
            <span>From your notes:</span>
            {e.anchorPages.map((p) => (
              <button
                key={p}
                onClick={() => onSelectScanPage(p)}
                className="px-2 py-0.5 rounded bg-slate-800 hover:bg-amber-500 hover:text-slate-950 text-slate-300 font-mono transition border border-slate-700 cursor-pointer"
              >
                Scan P.{p}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
