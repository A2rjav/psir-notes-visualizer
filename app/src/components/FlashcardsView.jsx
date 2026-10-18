import React, { useEffect, useMemo, useState } from 'react';
import { 
  Layers, 
  RotateCw, 
  ChevronLeft, 
  ChevronRight, 
  Shuffle, 
  CheckCircle, 
  Eye, 
  Sparkles, 
  BookOpen
} from 'lucide-react';

// The deck is grouped by `category` (V1), else the section/topic stored in `mnemonic`
// (V2-V6), else the card badge. `badge` alone is the same label on every card in V2-V6.
const cardCategory = (c) => c.category || c.mnemonic || c.badge || 'Core Theory';
const cardKey = (c, i) => c.id ?? `idx-${i}`;

const loadMastered = (volId) => {
  try {
    const raw = window.localStorage.getItem(`psir-mastered-${volId}`);
    return new Set(raw ? JSON.parse(raw) : []);
  } catch {
    return new Set();
  }
};

export default function FlashcardsView({ onSelectScanPage, currentDataset, currentVolume }) {
  const allCards = currentDataset?.flashcards || [];
  const volId = currentVolume?.id || 'vol';
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [masteredIds, setMasteredIds] = useState(() => loadMastered(volId));

  useEffect(() => {
    try {
      window.localStorage.setItem(`psir-mastered-${volId}`, JSON.stringify([...masteredIds]));
    } catch {
      /* storage unavailable (private mode): mastery stays in-session only */
    }
  }, [masteredIds, volId]);

  const categories = useMemo(
    () => ['All', ...new Set(allCards.map(cardCategory))],
    [allCards]
  );

  const filteredCards = selectedCategory === 'All'
    ? allCards
    : allCards.filter(c => cardCategory(c) === selectedCategory);

  const safeIndex = filteredCards.length ? Math.min(currentIndex, filteredCards.length - 1) : 0;
  const currentCard = filteredCards[safeIndex] || {
    front: 'No flashcards available for this section.',
    back: 'Please select another section or volume.'
  };
  const currentKey = cardKey(currentCard, safeIndex);

  const qText = currentCard?.front || currentCard?.question;
  const aText = currentCard?.back || currentCard?.answer;

  const handleNext = () => {
    setIsFlipped(false);
    if (filteredCards.length > 0) {
      setCurrentIndex(prev => (prev + 1) % filteredCards.length);
    }
  };

  const handlePrev = () => {
    setIsFlipped(false);
    if (filteredCards.length > 0) {
      setCurrentIndex(prev => (prev - 1 + filteredCards.length) % filteredCards.length);
    }
  };

  const handleShuffle = () => {
    setIsFlipped(false);
    if (filteredCards.length > 0) {
      setCurrentIndex(prev => {
        if (filteredCards.length < 2) return 0;
        let next = prev;
        while (next === prev) next = Math.floor(Math.random() * filteredCards.length);
        return next;
      });
    }
  };

  const toggleMastered = (id) => {
    setMasteredIds(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  return (
    <div className="space-y-8 max-w-3xl mx-auto pb-16">
      
      {/* Header */}
      <div className="text-center space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20">
          <Layers className="w-3.5 h-3.5" /> Active Recall Mode • {currentVolume?.shortTitle || 'PSIR Notes'}
        </div>
        <h2 className="text-2xl font-extrabold text-white">High-Yield Flashcards ({allCards.length})</h2>
        <p className="text-xs text-slate-400">
          Reinforce key thinkers, doctrines, quotes, and comparative frameworks through active recall.
        </p>
      </div>

      {/* Category Pills */}
      <div className="flex items-center justify-center gap-1.5 flex-wrap">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => {
              setSelectedCategory(cat);
              setCurrentIndex(0);
              setIsFlipped(false);
            }}
            className={`px-3 py-1.5 rounded-full text-xs font-medium transition cursor-pointer ${
              selectedCategory === cat
                ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/20 font-bold'
                : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Progress & Actions Bar */}
      <div className="flex items-center justify-between text-xs text-slate-400 px-2">
        <span>
          Card <strong className="text-white">{filteredCards.length > 0 ? safeIndex + 1 : 0}</strong> of <strong className="text-white">{filteredCards.length}</strong>
        </span>
        
        <div className="flex items-center gap-2">
          <button
            onClick={handleShuffle}
            className="flex items-center gap-1 text-slate-400 hover:text-white transition px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 cursor-pointer"
          >
            <Shuffle className="w-3.5 h-3.5" />
            <span>Shuffle</span>
          </button>
          <span className="font-mono text-[11px] text-emerald-400">
            {masteredIds.size} Mastered
          </span>
        </div>
      </div>

      {/* Interactive 3D Flip Card */}
      <div 
        onClick={() => setIsFlipped(!isFlipped)}
        className="w-full min-h-[340px] sm:min-h-[380px] p-6 sm:p-8 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900 to-slate-950 border border-slate-800 hover:border-amber-500/40 shadow-2xl cursor-pointer transition-all duration-300 flex flex-col justify-between relative group select-none"
      >
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded text-[11px] font-semibold bg-amber-500/10 text-amber-300 border border-amber-500/20">
              {cardCategory(currentCard)}
            </span>
            {currentCard?.mnemonic && currentCard.mnemonic !== cardCategory(currentCard) && (
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-indigo-500/20 text-indigo-300">
                {currentCard.mnemonic}
              </span>
            )}
          </div>
          <span className="text-[11px] text-slate-500 flex items-center gap-1">
            <RotateCw className="w-3.5 h-3.5 group-hover:rotate-180 transition-transform duration-500" /> Click to flip
          </span>
        </div>

        {/* Card Content (Question or Answer) */}
        <div className="my-auto py-6 text-center space-y-4">
          {!isFlipped ? (
            <div className="space-y-3">
              <span className="text-xs uppercase tracking-widest text-slate-500 font-mono block">Question / Prompt</span>
              <p className="text-lg sm:text-2xl font-bold text-white leading-relaxed">
                {qText}
              </p>
            </div>
          ) : (
            <div className="space-y-3 text-left bg-slate-950/40 p-5 rounded-2xl border border-slate-800/80">
              <span className="text-xs uppercase tracking-widest text-amber-400 font-mono block text-center">Core Concept & Explanation</span>
              <p className="text-sm sm:text-base text-slate-200 leading-relaxed font-sans">
                {aText}
              </p>
            </div>
          )}
        </div>

        {/* Card Footer: Scan Ref & Mastered Button */}
        <div className="flex items-center justify-between text-xs pt-4 border-t border-slate-800/80">
          <div>
            {currentCard?.scanPage && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onSelectScanPage(currentCard.scanPage);
                }}
                className="flex items-center gap-1 text-[11px] font-mono text-amber-400 hover:text-amber-300 transition"
              >
                <Eye className="w-3 h-3" /> Scan P.{currentCard.scanPage}
              </button>
            )}
          </div>

          <button
            onClick={(e) => {
              e.stopPropagation();
              toggleMastered(currentKey);
            }}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold transition ${
              masteredIds.has(currentKey)
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                : 'bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white'
            }`}
          >
            <CheckCircle className="w-3.5 h-3.5" />
            <span>{masteredIds.has(currentKey) ? 'Mastered ✓' : 'Mark as Mastered'}</span>
          </button>
        </div>
      </div>

      {/* Navigation Buttons */}
      <div className="flex items-center justify-center gap-4">
        <button
          onClick={handlePrev}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 text-white font-medium text-xs transition cursor-pointer shadow-lg"
        >
          <ChevronLeft className="w-4 h-4" />
          <span>Previous</span>
        </button>
        <button
          onClick={handleNext}
          className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs transition cursor-pointer shadow-lg shadow-amber-500/10"
        >
          <span>Next Card</span>
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>

    </div>
  );
}
