import React, { useState } from 'react';
import { 
  Network, 
  Sparkles, 
  Eye, 
  Shield, 
  Scale, 
  Zap, 
  Globe, 
  ArrowRight,
  Info,
  Crown,
  BookOpen
} from 'lucide-react';

export default function MindMapView({ onSelectScanPage, currentDataset, currentVolume }) {
  const sections = currentDataset?.sections || [];

  const colors = ['amber', 'emerald', 'sky', 'indigo', 'rose', 'purple'];

  const clusters = sections.map((sec, idx) => ({
    id: sec.id,
    title: `${sec.number}. ${sec.title.split(':')[0]}`,
    fullTitle: sec.title,
    subtitle: sec.subtitle,
    scanPage: sec.scanPages ? sec.scanPages[0] : 1,
    notebookPage: sec.notebookPages,
    color: colors[idx % colors.length],
    nodes: (sec.concepts || []).map(c => ({
      label: c.title,
      desc: c.summary,
      badge: c.badge,
      scanPage: c.scanPage
    }))
  }));

  const [activeClusterId, setActiveClusterId] = useState(
    (clusters.find((c) => !/^contents|front matter/i.test(c.fullTitle || '')) || clusters[0])?.id || ''
  );
  const current = clusters.find(c => c.id === activeClusterId) || clusters[0] || {
    title: 'Concept Cluster',
    nodes: [],
    scanPage: 1
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-16">
      
      {/* Header */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Network className="w-5 h-5 text-amber-400" />
            <h2 className="text-xl font-bold text-white">Interactive Concept & Mindmap Nodes</h2>
          </div>
          <p className="text-xs text-slate-400">
            {currentVolume?.shortTitle || 'PSIR Notes'} • Structural visualization of actors, doctrines, and philosophical paradigms.
          </p>
        </div>

        {/* Scan Pill */}
        {current.scanPage && (
          <button
            onClick={() => onSelectScanPage(current.scanPage)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 transition shrink-0 self-start sm:self-auto cursor-pointer"
          >
            <Eye className="w-3.5 h-3.5" />
            <span>View Scan #{current.scanPage} (Note {current.notebookPage})</span>
          </button>
        )}
      </div>

      {/* Cluster Navigation Pills */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
        {clusters.map((cluster) => (
          <button
            key={cluster.id}
            onClick={() => setActiveClusterId(cluster.id)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium transition whitespace-nowrap cursor-pointer ${
              (current.id === cluster.id)
                ? 'bg-amber-500 text-slate-950 font-bold shadow-md shadow-amber-500/10'
                : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800'
            }`}
          >
            {cluster.title}
          </button>
        ))}
      </div>

      {/* Mindmap Hub Canvas */}
      <div className="relative p-6 sm:p-10 rounded-3xl bg-slate-900/90 border border-slate-800 shadow-2xl overflow-hidden">
        
        {/* Background Network Graphic Overlay */}
        <div className="absolute inset-0 opacity-5 pointer-events-none flex items-center justify-center">
          <Network className="w-96 h-96 text-white" />
        </div>

        {/* Central Core Concept Node */}
        <div className="text-center max-w-xl mx-auto space-y-2 relative z-10 mb-8 sm:mb-12">
          <span className="px-3 py-1 rounded-full text-[11px] font-mono font-bold uppercase tracking-wider bg-amber-500/20 text-amber-300 border border-amber-500/30">
            {current.title}
          </span>
          <h3 className="text-lg sm:text-xl font-bold text-white tracking-tight">
            {current.fullTitle || current.title}
          </h3>
          <p className="text-xs text-slate-400">
            {current.subtitle || 'Connected theoretical nodes and analytical pillars from lecture notes.'}
          </p>
        </div>

        {/* Radiating Sub-Nodes Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 relative z-10">
          {(current.nodes || []).map((node, nIdx) => (
            <div 
              key={nIdx}
              className="p-4 sm:p-5 rounded-2xl bg-slate-950/80 border border-slate-800 hover:border-amber-500/40 transition-all duration-300 shadow-lg space-y-2 group"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="w-6 h-6 rounded-lg bg-amber-500/10 text-amber-400 font-mono text-xs font-bold flex items-center justify-center border border-amber-500/20">
                    {nIdx + 1}
                  </span>
                  <span className="text-xs sm:text-sm font-bold text-white group-hover:text-amber-300 transition">
                    {node.label}
                  </span>
                </div>
                {node.scanPage && (
                  <button
                    onClick={() => onSelectScanPage(node.scanPage)}
                    className="p-1 rounded text-slate-500 hover:text-amber-400 transition"
                    title={`View Scan P.${node.scanPage}`}
                  >
                    <Eye className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>

              {node.badge && (
                <span className="inline-block px-2 py-0.5 rounded text-[10px] font-mono bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  {node.badge}
                </span>
              )}

              <p className="text-xs text-slate-300 leading-relaxed pl-8">
                {node.desc}
              </p>
            </div>
          ))}
        </div>

        {(!current.nodes || current.nodes.length === 0) && (
          <div className="p-8 text-center text-slate-500 text-xs">
            No sub-nodes available for this cluster.
          </div>
        )}

      </div>

    </div>
  );
}
