import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  X, Play, Pause, SkipBack, SkipForward, Volume2, VolumeX, Captions, CaptionsOff,
  RotateCcw, CheckCircle2, PenTool, Trophy, XCircle, Maximize2, Minimize2,
} from 'lucide-react';
import { SCENES } from './scenes';
import useNarrator, { estimateSeconds } from './useNarrator';

const firstSentence = (t) => (String(t).match(/^[^.!?]+[.!?]/) || [String(t)])[0];

// Deterministic shuffle (mulberry32 seeded from a string) so quiz options are stable per question
// but the right answer lands in a different place each time.
const hash = (str) => {
  let h = 2166136261;
  for (let i = 0; i < str.length; i += 1) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
};
const rng = (seed) => () => {
  let t = (seed += 0x6d2b79f5);
  t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
const shuffle = (arr, key) => {
  const a = [...arr];
  const r = rng(hash(String(key)));
  for (let i = a.length - 1; i > 0; i -= 1) {
    const j = Math.floor(r() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
};

const clip = (t, n = 150) => (t.length > n ? `${t.slice(0, n - 1).trimEnd()}…` : t);

// Lesson scenes + the topic's picture/clip + a 3-question quiz + a finish screen.
function buildScenes(lesson, explainers, topicCards, otherCards) {
  const scenes = [...(lesson?.scenes || [])];
  const visuals = [];
  explainers.forEach((ex) => {
    const beats = (ex.beats || ex.variants?.[0]?.beats || []).filter((b) => typeof b.x === 'number');
    visuals.push({
      type: 'visual', explainer: ex,
      narration: `Now look at this picture. ${beats.slice(0, 3).map((b, i) => `Number ${i + 1}, ${b.label}. ${firstSentence(b.text)}`).join(' ')}`,
    });
    if (ex.video) {
      const vb = ex.videoBeats || [];
      visuals.push({ type: 'visual', explainer: ex, useVideo: true, narration: vb.length ? `Watch it move. ${vb.map((b) => firstSentence(b.text)).join(' ')}` : 'Watch it move.' });
    }
  });
  if (visuals.length) {
    const at = Math.min(scenes.length - 1, Math.max(1, scenes.findIndex((s) => s.type === 'analogy') + 1));
    scenes.splice(at, 0, ...visuals.slice(0, 2));
  }
  // Topic quiz written and checked by agy_review.py: one question mid-lesson, the rest at the end.
  if (lesson?.quiz?.length) {
    const qs = lesson.quiz.map((q) => ({ type: 'quiz', ...q }));
    const mid = Math.max(2, Math.floor(scenes.length / 2));
    if (qs.length > 3) scenes.splice(mid, 0, qs.shift());
    return [...scenes, ...qs, { type: 'complete' }];
  }
  // Fallback: quick checks built from the topic's flashcards, wrong options from other topics.
  const quiz = shuffle(topicCards, `${lesson?.title}|quiz`).slice(0, 3).map((c) => {
    const wrong = shuffle(otherCards.filter((o) => o.back !== c.back), `${c.front}|wrong`).slice(0, 2).map((o) => clip(o.back));
    const options = shuffle([clip(c.back), ...wrong], `${c.front}|options`);
    return { type: 'quiz', q: c.front, options, answer: options.indexOf(clip(c.back)), scanPage: c.scanPage };
  });
  return [...scenes, ...quiz, { type: 'complete' }];
}

function Caption({ text, spoken }) {
  if (!text) return null;
  if (spoken.text === text && spoken.charIndex >= 0) {
    const i = spoken.charIndex;
    const end = text.indexOf(' ', i);
    const j = end === -1 ? text.length : end;
    return (
      <p className="text-sm sm:text-base text-slate-200 leading-relaxed">
        {text.slice(0, i)}<span className="text-amber-300 font-bold">{text.slice(i, j)}</span>{text.slice(j)}
      </p>
    );
  }
  return <p className="text-sm sm:text-base text-slate-200 leading-relaxed">{text}</p>;
}

function QuizScene({ scene, n, of, picked, onPick, onNext, onSelectScanPage }) {
  return (
    <div className="h-full overflow-y-auto">
    <div className="min-h-full flex flex-col justify-center gap-3 sm:gap-4 px-3 sm:px-10 py-3">
      <p className="lp-anim lp-fade-up text-[11px] uppercase tracking-[0.25em] text-sky-300 font-bold text-center">Quick check {n} of {of}</p>
      <p className="lp-anim lp-fade-up text-base sm:text-2xl font-extrabold text-white text-center leading-snug" style={{ animationDelay: '0.15s' }}>{scene.q}</p>
      <div className="grid gap-2 max-w-3xl mx-auto w-full">
        {scene.options.map((o, i) => {
          const state = picked == null ? 'idle' : i === scene.answer ? 'right' : i === picked ? 'wrong' : 'dim';
          return (
            <button key={i} disabled={picked != null} onClick={() => onPick(i)}
              className={`lp-anim lp-slide-left text-left p-2.5 sm:p-3.5 rounded-xl border-2 text-xs sm:text-base font-semibold transition cursor-pointer flex items-start gap-2 ${
                state === 'right' ? 'bg-emerald-500/20 border-emerald-400 text-white'
                  : state === 'wrong' ? 'bg-red-500/20 border-red-400 text-white'
                    : state === 'dim' ? 'bg-slate-900/60 border-slate-800 text-slate-500'
                      : 'bg-slate-900/80 border-slate-700 text-slate-100 hover:border-amber-400'
              }`}
              style={{ animationDelay: `${0.3 + i * 0.15}s` }}>
              <span className="w-6 h-6 rounded-full bg-slate-800 text-xs font-black flex items-center justify-center shrink-0">{'ABCD'[i]}</span>
              <span className="flex-1">{o}</span>
              {state === 'right' && <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />}
              {state === 'wrong' && <XCircle className="w-5 h-5 text-red-400 shrink-0" />}
            </button>
          );
        })}
      </div>
      {picked != null && scene.why && (
        <p className="lp-anim lp-fade-up max-w-3xl mx-auto w-full text-xs sm:text-sm text-slate-200 bg-slate-900/80 border border-slate-700 rounded-xl px-3 py-2">
          <strong className="text-amber-300">Why: </strong>{scene.why}
        </p>
      )}
      {picked != null && (
        <div className="flex flex-wrap items-center justify-center gap-3">
          <span className={`text-sm font-bold ${picked === scene.answer ? 'text-emerald-300' : 'text-red-300'}`}>
            {picked === scene.answer ? 'Correct!' : 'Not quite. The green one is right.'}
          </span>
          <button onClick={onNext} className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 text-sm font-bold cursor-pointer">Continue</button>
          {scene.scanPage && (
            <button onClick={() => onSelectScanPage(scene.scanPage)} className="text-xs text-amber-300 hover:text-amber-200 underline cursor-pointer">
              See it in the notes
            </button>
          )}
        </div>
      )}
    </div>
    </div>
  );
}

function CompleteScene({ score, total, onDone, done, onAnswer, onReplay, onNext, nextTitle }) {
  return (
    <div className="h-full relative overflow-hidden flex flex-col items-center justify-center gap-4 text-center px-4">
      {Array.from({ length: 24 }).map((_, i) => (
        <span key={i} className="absolute top-0 w-2 h-3 rounded-sm"
          style={{ left: `${(i * 37) % 100}%`, background: ['#f59e0b', '#38bdf8', '#34d399', '#f472b6'][i % 4], animation: `lp-confetti ${2.2 + (i % 5) * 0.4}s ${(i % 7) * 0.15}s ease-in both` }} />
      ))}
      <Trophy className="lp-anim lp-pop w-14 h-14 sm:w-20 sm:h-20 text-amber-400" />
      <p className="lp-anim lp-fade-up text-2xl sm:text-4xl font-extrabold text-white" style={{ animationDelay: '0.2s' }}>Lesson complete!</p>
      {total > 0 && (
        <p className="lp-anim lp-fade-up text-sm sm:text-lg text-slate-300" style={{ animationDelay: '0.35s' }}>
          You got <strong className="text-amber-300">{score} of {total}</strong> quick checks right.
        </p>
      )}
      {onNext && (
        <button onClick={onNext} className="lp-anim lp-pop max-w-full inline-flex items-center gap-2 px-5 py-3 rounded-2xl bg-gradient-to-r from-amber-400 to-orange-500 hover:from-amber-300 hover:to-orange-400 text-slate-950 font-extrabold text-sm sm:text-base shadow-lg shadow-amber-500/20 cursor-pointer"
          style={{ animationDelay: '0.45s' }} title="Marks this topic done and plays the next lesson">
          <Play className="w-4 h-4 fill-current shrink-0" />
          <span className="truncate">Next lesson: {nextTitle}</span>
        </button>
      )}
      <div className="lp-anim lp-fade-up flex flex-wrap justify-center gap-2" style={{ animationDelay: '0.5s' }}>
        {!done && (
          <button onClick={onDone} className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm cursor-pointer">
            <CheckCircle2 className="w-4 h-4" /> Mark topic done
          </button>
        )}
        {onAnswer && (
          <button onClick={onAnswer} className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-sky-500/20 hover:bg-sky-500/30 text-sky-100 border border-sky-400/40 font-semibold text-sm cursor-pointer">
            <PenTool className="w-4 h-4" /> Practice an answer
          </button>
        )}
        <button onClick={onReplay} className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-sm cursor-pointer">
          <RotateCcw className="w-4 h-4" /> Watch again
        </button>
      </div>
    </div>
  );
}

export default function LessonPlayer({
  lesson, topicTitle, explainers = [], topicCards = [], otherCards = [],
  onClose, onMarkDone, isDone, onPracticeAnswer, onSelectScanPage, onNextLesson, nextTitle,
}) {
  // Built once per lesson: the parent passes freshly filtered card arrays on every render, and a new
  // scene object would restart the narration mid-scene. Cards and explainers follow from the lesson.
  const scenes = useMemo(() => buildScenes(lesson, explainers, topicCards, otherCards), [lesson]);
  const narrator = useNarrator();
  const { speak, cancel } = narrator;
  const [idx, setIdx] = useState(0);
  const [playing, setPlaying] = useState(true);
  const [captions, setCaptions] = useState(true);
  const [answers, setAnswers] = useState({});
  const [full, setFull] = useState(false);
  const rootRef = useRef(null);
  const scene = scenes[idx];
  const Comp = SCENES[scene.type];
  const quizScenes = scenes.filter((s) => s.type === 'quiz');
  const score = quizScenes.filter((s) => answers[scenes.indexOf(s)] === s.answer).length;

  const go = useCallback((i) => {
    cancel();
    setIdx(Math.max(0, Math.min(scenes.length - 1, i)));
  }, [cancel, scenes.length]);

  // Narrate the scene; auto-advance when the narration ends (quiz and finish wait for the student).
  useEffect(() => {
    if (!playing) { cancel(); return undefined; }
    let alive = true;
    const text = scene.type === 'quiz' ? scene.q : scene.narration;
    if (!text) return undefined;
    speak(text).then((finished) => {
      if (!alive || !finished) return;
      if (scene.type !== 'quiz' && scene.type !== 'complete') setTimeout(() => { if (alive) setIdx((i) => Math.min(scenes.length - 1, i + 1)); }, 500);
    });
    return () => { alive = false; };
  }, [idx, playing, scene, speak, cancel, scenes.length]);

  useEffect(() => {
    const onKey = (e) => {
      if (e.key === 'Escape') onClose();
      else if (e.key === ' ') { e.preventDefault(); setPlaying((p) => !p); }
      else if (e.key === 'ArrowRight') go(idx + 1);
      else if (e.key === 'ArrowLeft') go(idx - 1);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [go, idx, onClose]);

  useEffect(() => {
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = prev; };
  }, []);

  const toggleFull = () => {
    if (!document.fullscreenElement) rootRef.current?.requestFullscreen?.().then(() => setFull(true)).catch(() => {});
    else document.exitFullscreen?.().then(() => setFull(false)).catch(() => {});
  };

  const dur = estimateSeconds(scene.narration || '', narrator.rate);
  const quizN = scene.type === 'quiz' ? quizScenes.indexOf(scene) + 1 : 0;
  const btn = 'p-2 rounded-lg bg-slate-800/90 hover:bg-slate-700 text-slate-200 hover:text-white transition cursor-pointer disabled:opacity-40';

  return (
    <div ref={rootRef} className="fixed inset-0 z-[70] bg-slate-950/95 backdrop-blur-sm flex flex-col">
      {/* Top bar */}
      <div className="flex items-center gap-3 px-3 sm:px-5 py-2.5 border-b border-slate-800">
        <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-amber-500/20 text-amber-300 border border-amber-500/30 shrink-0">Lesson</span>
        <p className="text-xs sm:text-sm font-bold text-white truncate flex-1">{lesson?.title || topicTitle}</p>
        <button onClick={toggleFull} className={`${btn} hidden sm:inline-flex`} title="Full screen">{full ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}</button>
        <button onClick={onClose} className={btn} title="Close (Esc)"><X className="w-4 h-4" /></button>
      </div>

      {/* Stage */}
      <div className="flex-1 min-h-0 flex items-center justify-center p-2 sm:p-5">
        {/* Phones get a tall stage (a 16:9 box would be ~210px high); wider screens get 16:9. */}
        <div data-stage className={`relative w-full max-w-6xl h-full sm:h-auto sm:aspect-video max-h-full rounded-2xl overflow-hidden border border-slate-800 bg-gradient-to-br from-slate-900 via-[#0b1226] to-[#1a0f2e] shadow-2xl ${playing ? '' : 'lp-paused'}`}>
          <span className="absolute -top-10 -left-10 w-48 h-48 rounded-full bg-amber-500/10 blur-2xl lp-float" />
          <span className="absolute -bottom-12 right-10 w-56 h-56 rounded-full bg-sky-500/10 blur-2xl lp-float" style={{ animationDelay: '-3s' }} />
          <div key={idx} className="relative h-full">
            {scene.type === 'quiz' ? (
              <QuizScene scene={scene} n={quizN} of={quizScenes.length} picked={answers[idx]}
                onPick={(i) => setAnswers((a) => ({ ...a, [idx]: i }))} onNext={() => go(idx + 1)} onSelectScanPage={onSelectScanPage} />
            ) : scene.type === 'complete' ? (
              <CompleteScene score={score} total={quizScenes.length} done={isDone} onDone={() => { onMarkDone(); onClose(); }}
                onNext={onNextLesson} nextTitle={nextTitle}
                onAnswer={onPracticeAnswer} onReplay={() => { setAnswers({}); go(0); setPlaying(true); }} />
            ) : Comp ? (
              <Comp scene={scene} dur={dur} />
            ) : null}
          </div>
        </div>
      </div>

      {/* Captions */}
      {captions && scene.narration && (
        <div className="px-4 sm:px-8 max-w-4xl mx-auto w-full min-h-[3.5rem]">
          <Caption text={scene.narration} spoken={narrator.spoken} />
        </div>
      )}

      {/* Controls */}
      <div className="px-3 sm:px-5 py-3 border-t border-slate-800 space-y-2.5">
        <div className="flex gap-1 max-w-6xl mx-auto">
          {scenes.map((s, i) => (
            <button key={i} onClick={() => go(i)} title={s.type}
              className={`h-1.5 flex-1 rounded-full transition cursor-pointer ${i < idx ? 'bg-amber-500' : i === idx ? 'bg-amber-300' : s.type === 'quiz' ? 'bg-sky-900' : 'bg-slate-700'}`} />
          ))}
        </div>
        <div className="flex items-center justify-center gap-2 flex-wrap">
          <button onClick={() => go(idx - 1)} disabled={idx === 0} className={btn} title="Previous (←)"><SkipBack className="w-4 h-4" /></button>
          <button onClick={() => setPlaying((p) => !p)} className="p-3 rounded-full bg-amber-500 hover:bg-amber-400 text-slate-950 cursor-pointer" title="Play / pause (space)">
            {playing ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
          </button>
          <button onClick={() => go(idx + 1)} disabled={idx === scenes.length - 1} className={btn} title="Next (→)"><SkipForward className="w-4 h-4" /></button>
          <span className="w-2" />
          {narrator.supported && (
            <button onClick={() => { narrator.setEnabled(!narrator.enabled); cancel(); }} className={btn} title={narrator.enabled ? 'Voice on' : 'Voice off'}>
              {narrator.enabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
            </button>
          )}
          <button onClick={() => setCaptions(!captions)} className={btn} title="Captions">{captions ? <Captions className="w-4 h-4" /> : <CaptionsOff className="w-4 h-4" />}</button>
          <select value={narrator.rate} onChange={(e) => { narrator.setRate(Number(e.target.value)); cancel(); }}
            className="bg-slate-800 border border-slate-700 rounded-lg px-2 py-1.5 text-xs text-slate-200" title="Speed">
            {[0.85, 1, 1.15, 1.3].map((r) => <option key={r} value={r}>{r}×</option>)}
          </select>
          {narrator.enabled && narrator.voices.length > 1 && (
            <select value={narrator.voice?.voiceURI || ''} onChange={(e) => { narrator.setVoiceURI(e.target.value); cancel(); }}
              className="bg-slate-800 border border-slate-700 rounded-lg px-2 py-1.5 text-xs text-slate-200 max-w-[11rem] truncate" title="Voice">
              {narrator.voices.map((v) => <option key={v.voiceURI} value={v.voiceURI}>{v.name.replace(/^Microsoft |^Google /, '')}</option>)}
            </select>
          )}
        </div>
      </div>
    </div>
  );
}
