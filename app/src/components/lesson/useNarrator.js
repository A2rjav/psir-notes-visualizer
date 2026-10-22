import { useCallback, useEffect, useRef, useState } from 'react';

// Voice-over for the lesson player, using the browser's own speech engine (no audio files).
// Each narration is spoken sentence by sentence: Chrome cuts off single utterances after ~15 s.
// With voice off, or no speech engine, a timer stands in so scenes still advance with captions.
const synth = typeof window !== 'undefined' && 'speechSynthesis' in window ? window.speechSynthesis : null;
const PREF_KEY = 'psir-narrator-v1';

const readPrefs = () => {
  try { return JSON.parse(window.localStorage.getItem(PREF_KEY) || '{}'); } catch { return {}; }
};

// Prefer Indian English, then natural/neural voices, then any English voice.
const scoreVoice = (v) =>
  (/en[-_]IN/i.test(v.lang) ? 40 : 0) +
  (/natural|neural|online/i.test(v.name) ? 30 : 0) +
  (/google|microsoft/i.test(v.name) ? 8 : 0) +
  (/^en/i.test(v.lang) ? 5 : 0);

const splitSentences = (text) =>
  (String(text).match(/[^.!?]+[.!?]+["')\]]*|[^.!?]+$/g) || [String(text)]).map((s) => s.trim()).filter(Boolean);

export const estimateSeconds = (text, rate = 1) =>
  Math.max(2.5, String(text || '').split(/\s+/).filter(Boolean).length / (2.6 * rate)) + 0.6;

export default function useNarrator() {
  const prefs = readPrefs();
  const [voices, setVoices] = useState([]);
  const [voiceURI, setVoiceURI] = useState(prefs.voiceURI || '');
  const [enabled, setEnabled] = useState(synth ? prefs.enabled !== false : false);
  const [rate, setRate] = useState(prefs.rate || 1);
  const [spoken, setSpoken] = useState({ text: '', charIndex: -1 }); // for caption highlighting
  const runRef = useRef(0); // bumps on every speak/cancel so stale callbacks are ignored
  const timerRef = useRef(null);

  useEffect(() => {
    if (!synth) return undefined;
    const load = () => setVoices(synth.getVoices().filter((v) => /^en/i.test(v.lang)));
    load();
    synth.addEventListener?.('voiceschanged', load);
    return () => synth.removeEventListener?.('voiceschanged', load);
  }, []);

  useEffect(() => {
    try { window.localStorage.setItem(PREF_KEY, JSON.stringify({ voiceURI, enabled, rate })); } catch { /* ignore */ }
  }, [voiceURI, enabled, rate]);

  const voice = voices.find((v) => v.voiceURI === voiceURI) || [...voices].sort((a, b) => scoreVoice(b) - scoreVoice(a))[0] || null;

  const cancel = useCallback(() => {
    runRef.current += 1;
    clearTimeout(timerRef.current);
    if (synth) synth.cancel();
    setSpoken({ text: '', charIndex: -1 });
  }, []);

  // Resolves true when the narration finished, false if it was cancelled.
  const speak = useCallback((text) => {
    cancel();
    const run = runRef.current;
    if (!enabled || !synth || !voice) {
      return new Promise((resolve) => {
        timerRef.current = setTimeout(() => resolve(run === runRef.current), estimateSeconds(text, rate) * 1000);
      });
    }
    const parts = splitSentences(text);
    let offset = 0;
    return new Promise((resolve) => {
      const next = (i) => {
        if (run !== runRef.current) { resolve(false); return; }
        if (i >= parts.length) { setSpoken({ text: '', charIndex: -1 }); resolve(true); return; }
        const u = new SpeechSynthesisUtterance(parts[i]);
        u.voice = voice;
        u.lang = voice.lang;
        u.rate = rate;
        const base = offset;
        u.onboundary = (e) => { if (run === runRef.current) setSpoken({ text, charIndex: base + e.charIndex }); };
        u.onend = () => { offset += parts[i].length + 1; next(i + 1); };
        u.onerror = () => { offset += parts[i].length + 1; next(i + 1); };
        synth.speak(u);
      };
      next(0);
    });
  }, [cancel, enabled, rate, voice]);

  useEffect(() => cancel, [cancel]);

  return {
    supported: !!synth,
    voices,
    voice,
    setVoiceURI,
    enabled,
    setEnabled,
    rate,
    setRate,
    speak,
    cancel,
    spoken,
  };
}
