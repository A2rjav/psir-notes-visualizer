import { useCallback, useEffect, useState } from 'react';

// Study progress lives in this browser only (localStorage): which topics are done, and where the
// student last was, so "Continue" can pick up from there. Storage can be unavailable (private
// mode); then progress simply lasts for the session.
const KEY = 'psir-progress-v1';

const read = () => {
  try {
    const raw = window.localStorage.getItem(KEY);
    const p = raw ? JSON.parse(raw) : {};
    return { done: p.done || {}, lastVolumeId: p.lastVolumeId || null, lastSection: p.lastSection || {} };
  } catch {
    return { done: {}, lastVolumeId: null, lastSection: {} };
  }
};

export default function useProgress() {
  const [progress, setProgress] = useState(read);

  useEffect(() => {
    try {
      window.localStorage.setItem(KEY, JSON.stringify(progress));
    } catch {
      /* storage unavailable: keep progress in memory for this session */
    }
  }, [progress]);

  const isDone = useCallback((volId, secId) => (progress.done[volId] || []).includes(secId), [progress]);

  const toggleDone = useCallback((volId, secId) => {
    setProgress((p) => {
      const cur = new Set(p.done[volId] || []);
      if (cur.has(secId)) cur.delete(secId);
      else cur.add(secId);
      return { ...p, done: { ...p.done, [volId]: [...cur] } };
    });
  }, []);

  const doneCount = useCallback((volId) => (progress.done[volId] || []).length, [progress]);

  const setLastVolume = useCallback((volId) => {
    setProgress((p) => (p.lastVolumeId === volId ? p : { ...p, lastVolumeId: volId }));
  }, []);

  const setLastSection = useCallback((volId, secId) => {
    setProgress((p) => (p.lastSection[volId] === secId ? p : { ...p, lastSection: { ...p.lastSection, [volId]: secId } }));
  }, []);

  return { progress, isDone, toggleDone, doneCount, setLastVolume, setLastSection };
}
