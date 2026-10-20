import React, { useState } from 'react';
import { 
  X, 
  BookMarked, 
  CheckCircle2, 
  Clock, 
  ChevronDown, 
  ChevronRight, 
  ExternalLink, 
  GraduationCap, 
  Sparkles, 
  ArrowRight, 
  Crown, 
  Globe,
  Layers,
  FileText
} from 'lucide-react';
import { volumesCatalog, volumesByStep, isFrontMatter, topicNumber } from '../data/volumesCatalog';

export default function Sidebar({ 
  isOpen, 
  onClose, 
  activeVolumeId, 
  setActiveVolumeId, 
  currentVolume, 
  currentDataset, 
  scrollToSection,
  onSelectScanPage,
  study
}) {
  const [activeTab, setActiveTab] = useState('sections'); // 'sections' | 'volumes'

  const sections = currentDataset?.sections || [];

  return (
    <>
      {/* Backdrop */}
      {isOpen && (
        <div 
          onClick={onClose}
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 transition-opacity"
        />
      )}

      {/* Drawer */}
      <aside className={`fixed top-0 left-0 bottom-0 w-80 sm:w-96 bg-slate-900 border-r border-slate-800 z-50 transform transition-transform duration-300 ease-in-out flex flex-col shadow-2xl ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        
        {/* Header */}
        <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/80">
          <div className="flex items-center gap-2">
            <BookMarked className="w-5 h-5 text-amber-400" />
            <div>
              <h2 className="text-sm font-bold text-white">Study plan</h2>
              <p className="text-[11px] text-slate-400 truncate max-w-[200px]">
                {currentVolume?.shortTitle || 'PSIR Notes'}
              </p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Toggle */}
        <div className="grid grid-cols-2 p-2 bg-slate-950/60 border-b border-slate-800 gap-1.5 text-xs font-semibold">
          <button
            onClick={() => setActiveTab('sections')}
            className={`py-1.5 rounded-lg transition cursor-pointer flex items-center justify-center gap-1.5 ${
              activeTab === 'sections' 
                ? 'bg-amber-500 text-slate-950 font-bold shadow' 
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <span>Topics</span>
            <span className="px-1.5 py-0.2 rounded text-[10px] bg-slate-900/60 font-mono">
              {sections.length}
            </span>
          </button>
          <button
            onClick={() => setActiveTab('volumes')}
            className={`py-1.5 rounded-lg transition cursor-pointer flex items-center justify-center gap-1.5 ${
              activeTab === 'volumes' 
                ? 'bg-amber-500 text-slate-950 font-bold shadow' 
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <span>6 Steps</span>
            <span className="px-1.5 py-0.2 rounded text-[10px] bg-slate-900/60 font-mono">
              6
            </span>
          </button>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          
          {/* TAB 1: Sections of Active Volume */}
          {activeTab === 'sections' && (
            <div className="space-y-1.5">
              <span className="text-[10px] uppercase font-bold tracking-wider text-slate-500 block px-1 mb-2">
                Step {currentVolume?.step} • {study.doneCount(activeVolumeId)} of {sections.filter((x) => !isFrontMatter(x)).length} topics done
              </span>
              {sections.map((sec) => (
                <div
                  key={sec.id}
                  className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80 hover:border-amber-500/40 hover:bg-slate-800/40 transition group"
                >
                  <div className="flex items-start justify-between gap-2">
                    <button
                      onClick={() => {
                        scrollToSection(sec.id);
                        onClose();
                      }}
                      className="text-left flex-1 cursor-pointer"
                    >
                      <div className="flex items-center gap-1.5 mb-1">
                        <span className={`px-1.5 py-0.2 rounded text-[10px] font-mono font-bold ${
                          study.isDone(activeVolumeId, sec.id) ? 'bg-emerald-500/20 text-emerald-300' : 'bg-amber-500/20 text-amber-300'
                        }`}>
                          {study.isDone(activeVolumeId, sec.id) ? '✓' : (topicNumber(sections, sec) || '·')}
                        </span>
                        <span className="text-[10px] font-mono text-slate-400">
                          {sec.scanPages ? `P.${sec.scanPages[0]}–${sec.scanPages[sec.scanPages.length - 1]}` : ''}
                        </span>
                      </div>
                      <h4 className="text-xs font-semibold text-slate-200 group-hover:text-amber-300 transition line-clamp-2">
                        {isFrontMatter(sec) ? 'Cover, contents and reading list' : sec.title}
                      </h4>
                    </button>
                    
                    {sec.scanPages && sec.scanPages.length > 0 && (
                      <button
                        onClick={() => {
                          scrollToSection(sec.id);
                          onSelectScanPage(sec.scanPages[0]);
                          onClose();
                        }}
                        className="p-1 rounded bg-slate-900 hover:bg-amber-500 hover:text-slate-950 text-slate-400 text-[10px] font-mono transition shrink-0 border border-slate-800 cursor-pointer"
                        title={`Open Scan P.${sec.scanPages[0]}`}
                      >
                        P.{sec.scanPages[0]}
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* TAB 2: All 6 Volumes Switcher */}
          {activeTab === 'volumes' && (
            <div className="space-y-2.5">
              <span className="text-[10px] uppercase font-bold tracking-wider text-slate-500 block px-1 mb-1">
                Suggested order: thinkers first, current affairs last
              </span>
              {volumesByStep.map((vol) => {
                const isActive = activeVolumeId === vol.id;
                const done = study.doneCount(vol.id);
                const total = vol.sectionCount;
                return (
                  <button
                    key={vol.id}
                    onClick={() => {
                      setActiveVolumeId(vol.id);
                      setActiveTab('sections');
                    }}
                    className={`w-full text-left p-3 rounded-xl border transition flex items-start gap-3 cursor-pointer ${
                      isActive
                        ? 'bg-amber-500/10 border-amber-500 text-white shadow-lg'
                        : 'bg-slate-950/60 border-slate-800/80 text-slate-300 hover:bg-slate-800/50 hover:border-slate-700'
                    }`}
                  >
                    <span className="text-xl shrink-0 p-1 rounded-lg bg-slate-900 border border-slate-800">
                      {vol.icon}
                    </span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-1 mb-0.5">
                        <span className="text-[10px] font-mono font-bold text-amber-400">
                          Step {vol.step} • {vol.paperNumber}
                        </span>
                        <span className={`text-[10px] font-mono px-1.5 py-0.2 rounded border ${
                          done >= total ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30' : 'bg-slate-900 text-slate-400 border-slate-800'
                        }`}>
                          {done}/{total} topics
                        </span>
                      </div>
                      <h4 className="text-xs font-bold text-white leading-tight truncate">
                        {vol.title}
                      </h4>
                      <p className="text-[11px] text-slate-400 line-clamp-2 mt-0.5">
                        {vol.whyNow}
                      </p>
                      <div className="mt-1.5 h-1 rounded-full bg-slate-800 overflow-hidden">
                        <div className="h-full bg-emerald-500" style={{ width: `${Math.min(100, Math.round((done / total) * 100))}%` }} />
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          )}

        </div>

        {/* Footer Guarantee Badge */}
        <div className="p-3 border-t border-slate-800 bg-slate-950 text-[11px] text-slate-400 flex items-center justify-between">
          <div className="flex items-center gap-1.5 text-amber-400">
            <Sparkles className="w-3.5 h-3.5" />
            <span className="font-semibold text-xs">{volumesCatalog.reduce((a, v) => a + v.totalPages, 0).toLocaleString()} scanned pages</span>
          </div>
          <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
            AI-transcribed
          </span>
        </div>

      </aside>
    </>
  );
}
