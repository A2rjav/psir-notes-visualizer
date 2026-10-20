import React from 'react';
import { 
  BookOpen, 
  Network, 
  Layers, 
  FileText, 
  Eye, 
  Menu, 
  Search,
  Sparkles,
  ChevronRight,
  ChevronDown
} from 'lucide-react';
import { volumesByStep } from '../data/volumesCatalog';

export default function Navbar({ 
  activeVolumeId,
  setActiveVolumeId,
  currentVolume,
  currentDataset,
  viewMode, 
  setViewMode, 
  showScanInspector, 
  setShowScanInspector, 
  toggleSidebar,
  searchQuery,
  setSearchQuery,
  activeScanPage
}) {
  const flashcardCount = currentDataset?.flashcards?.length || 0;
  const answerCount = currentDataset?.answers?.length || 0;

  const navTabs = [
    { id: 'notes', label: 'Visual Notes', icon: BookOpen, badge: 'Zero-Loss' },
    { id: 'mindmap', label: 'Concept Map', icon: Network, badge: 'Interactive' },
    { id: 'flashcards', label: 'Flashcards', icon: Layers, badge: `${flashcardCount} Cards` },
    { id: 'answers', label: 'Answer Blueprints', icon: FileText, badge: `${answerCount} Answers` },
  ];

  const searchBox = (
    <>
      <Search className="w-4 h-4 text-slate-400 absolute left-3 pointer-events-none" />
      <input
        type="text"
        placeholder={`Search ${currentVolume?.shortTitle || 'concepts, scholars, theories'}...`}
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        onKeyDown={(e) => { if (e.key === 'Escape') setSearchQuery(''); }}
        className="w-full bg-slate-950/80 border border-slate-800 focus:border-amber-500/50 focus:ring-1 focus:ring-amber-500/50 rounded-xl pl-9 pr-12 py-1.5 text-xs text-slate-200 placeholder-slate-500 transition focus:outline-none"
      />
      {searchQuery && (
        <button
          onClick={() => setSearchQuery('')}
          className="absolute right-2.5 text-[10px] font-mono bg-slate-800 text-slate-400 hover:text-white px-1.5 py-0.5 rounded cursor-pointer"
          title="Clear search (Esc)"
        >
          esc
        </button>
      )}
    </>
  );

  return (
    <header className="sticky top-0 z-40 bg-slate-900/95 backdrop-blur-md border-b border-slate-800 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 gap-2 sm:gap-4">
          
          {/* Left: Syllabus Menu & Multi-Volume Selector */}
          <div className="flex items-center gap-2 sm:gap-3 min-w-0">
            <button 
              onClick={toggleSidebar}
              className="p-2 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-white transition flex items-center gap-1.5 shrink-0 cursor-pointer"
              title="Open Syllabus & All 6 Volumes Drawer"
            >
              <Menu className="w-5 h-5 text-amber-400" />
              <span className="hidden md:inline text-xs font-semibold uppercase tracking-wider text-slate-300">Syllabus</span>
            </button>

            {/* Multi-Volume Quick Selector Dropdown */}
            <div className="relative flex items-center shrink-0">
              <select
                value={activeVolumeId}
                onChange={(e) => setActiveVolumeId(e.target.value)}
                className="bg-slate-950 border border-slate-800 hover:border-amber-500/50 rounded-xl px-2.5 py-1.5 text-xs font-bold text-amber-400 focus:outline-none focus:ring-1 focus:ring-amber-500 cursor-pointer shadow-inner max-w-[150px] sm:max-w-[220px] md:max-w-[280px] truncate"
                title="Switch between all 6 digitized volumes"
              >
                {volumesByStep.map((vol) => (
                  <option key={vol.id} value={vol.id} className="bg-slate-900 text-slate-100">
                    Step {vol.step} · {vol.icon} {vol.shortTitle}
                  </option>
                ))}
              </select>
            </div>

            {/* Active Volume Quick Stats (Desktop) */}
            <div className="hidden xl:flex flex-col min-w-0">
              <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider truncate">
                {currentVolume?.paperNumber} • {currentVolume?.sectionName}
              </span>
              <h1 className="text-xs font-bold text-slate-200 truncate max-w-[200px]">
                {currentVolume?.shortTitle}
              </h1>
            </div>
          </div>

          {/* Center: Search Bar (desktop; phones get a second row below) */}
          <div className="hidden lg:flex items-center flex-1 max-w-xs relative">
            {searchBox}
          </div>

          {/* Right: View Tabs & Scan Inspector Toggle */}
          <div className="flex items-center gap-1.5 sm:gap-2 shrink-0">
            
            {/* View Mode Tabs */}
            <div className="flex items-center bg-slate-950/90 p-1 rounded-xl border border-slate-800">
              {navTabs.map((tab) => {
                const Icon = tab.icon;
                const isActive = viewMode === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setViewMode(tab.id)}
                    className={`px-2.5 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1.5 cursor-pointer ${
                      isActive 
                        ? 'bg-amber-500 text-slate-950 font-bold shadow-md shadow-amber-500/10' 
                        : 'text-slate-400 hover:text-white hover:bg-slate-900'
                    }`}
                  >
                    <Icon className="w-3.5 h-3.5" />
                    <span className="hidden sm:inline">{tab.label}</span>
                  </button>
                );
              })}
            </div>

            {/* Split Screen Scan Inspector Toggle Button */}
            <button
              onClick={() => setShowScanInspector(!showScanInspector)}
              className={`p-2 rounded-xl text-xs font-semibold transition flex items-center gap-1.5 border cursor-pointer ${
                showScanInspector 
                  ? 'bg-amber-500/20 text-amber-300 border-amber-500/40 shadow-sm' 
                  : 'bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-white border-slate-700'
              }`}
              title={showScanInspector ? "Hide Scan Inspector" : "Open Original Scan Inspector"}
            >
              <Eye className="w-4 h-4 text-amber-400" />
              <span className="hidden md:inline font-mono text-xs">P.{activeScanPage}</span>
            </button>

          </div>

        </div>

        {/* Search row for screens below lg */}
        <div className="lg:hidden pb-3">
          <div className="relative flex items-center">
            {searchBox}
          </div>
        </div>
      </div>
    </header>
  );
}
