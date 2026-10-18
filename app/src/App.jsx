import React, { useEffect, useState } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import UniversalVisualNotesView from './components/UniversalVisualNotesView';
import MindMapView from './components/MindMapView';
import FlashcardsView from './components/FlashcardsView';
import AnswerWritingView from './components/AnswerWritingView';
import ScanInspector from './components/ScanInspector';
import { getVolumeById } from './data/volumesCatalog';
import { Eye } from 'lucide-react';

const DESKTOP_QUERY = '(min-width: 1024px)';

function useIsDesktop() {
  const [matches, setMatches] = useState(() => window.matchMedia(DESKTOP_QUERY).matches);
  useEffect(() => {
    const mq = window.matchMedia(DESKTOP_QUERY);
    const onChange = (e) => setMatches(e.matches);
    mq.addEventListener('change', onChange);
    return () => mq.removeEventListener('change', onChange);
  }, []);
  return matches;
}

export default function App() {
  const [activeVolumeId, setActiveVolumeId] = useState('p1_part1');
  const [viewMode, setViewMode] = useState('notes'); // 'notes' | 'mindmap' | 'flashcards' | 'answers'
  // The split-pane inspector is desktop-only; on phones it opens as a full-screen overlay on demand.
  const isDesktop = useIsDesktop();
  const [showScanInspector, setShowScanInspector] = useState(isDesktop);
  const [activeScanPage, setActiveScanPage] = useState(7);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  // { id, nonce } - set by the sidebar, consumed by the notes view once it has scrolled.
  const [jumpTarget, setJumpTarget] = useState(null);

  const currentVolume = getVolumeById(activeVolumeId);
  const currentDataset = currentVolume.dataset;

  const handleSelectVolume = (newVolId) => {
    setActiveVolumeId(newVolId);
    setSearchQuery('');
    setJumpTarget(null);
    const targetVol = getVolumeById(newVolId);
    setActiveScanPage(targetVol.defaultScan || 1);
  };

  const handleSelectScanPage = (pageNum) => {
    setActiveScanPage(pageNum);
    setShowScanInspector(true);
  };

  const scrollToSection = (sectionId) => {
    setViewMode('notes');
    setSearchQuery('');
    setJumpTarget({ id: sectionId, nonce: Date.now() });
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">

      {/* Top Navbar */}
      <Navbar
        activeVolumeId={activeVolumeId}
        setActiveVolumeId={handleSelectVolume}
        currentVolume={currentVolume}
        currentDataset={currentDataset}
        viewMode={viewMode}
        setViewMode={setViewMode}
        showScanInspector={showScanInspector}
        setShowScanInspector={setShowScanInspector}
        toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        activeScanPage={activeScanPage}
      />

      {/* Slideout Syllabus & In-page Sidebar */}
      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        activeVolumeId={activeVolumeId}
        setActiveVolumeId={handleSelectVolume}
        currentVolume={currentVolume}
        currentDataset={currentDataset}
        scrollToSection={scrollToSection}
        onSelectScanPage={handleSelectScanPage}
      />

      {/* Main Workspace: Split View with Original Scan Inspector */}
      <div className="flex-1 flex overflow-hidden relative">

        {/* Left / Center: Interactive Learning Canvas.
            Every view is keyed by volume so per-volume UI state (section filter, card index,
            selected answer, active cluster) resets instead of leaking into the next volume. */}
        <main className={`flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 transition-all duration-300 ${
          showScanInspector && isDesktop ? 'lg:max-w-[58%] xl:max-w-[62%]' : 'max-w-7xl mx-auto w-full'
        }`}>
          {viewMode === 'notes' && (
            <UniversalVisualNotesView
              key={activeVolumeId}
              currentVolume={currentVolume}
              currentDataset={currentDataset}
              onSelectScanPage={handleSelectScanPage}
              searchQuery={searchQuery}
              jumpTarget={jumpTarget}
              onJumpHandled={() => setJumpTarget(null)}
            />
          )}

          {viewMode === 'mindmap' && (
            <MindMapView
              key={activeVolumeId}
              currentVolume={currentVolume}
              currentDataset={currentDataset}
              onSelectScanPage={handleSelectScanPage}
            />
          )}

          {viewMode === 'flashcards' && (
            <FlashcardsView
              key={activeVolumeId}
              currentVolume={currentVolume}
              currentDataset={currentDataset}
              onSelectScanPage={handleSelectScanPage}
            />
          )}

          {viewMode === 'answers' && (
            <AnswerWritingView
              key={activeVolumeId}
              currentVolume={currentVolume}
              currentDataset={currentDataset}
              onSelectScanPage={handleSelectScanPage}
            />
          )}
        </main>

        {/* Right Pane: Original Handwritten Scan Inspector (desktop split-screen) */}
        {showScanInspector && isDesktop && (
          <aside className="flex flex-col w-[42%] xl:w-[38%] border-l border-slate-800 bg-slate-900 shadow-2xl z-20">
            <ScanInspector
              activeScanPage={activeScanPage}
              setActiveScanPage={setActiveScanPage}
              onClose={() => setShowScanInspector(false)}
              currentVolume={currentVolume}
              currentDataset={currentDataset}
            />
          </aside>
        )}

      </div>

      {/* Mobile: full-screen scan overlay (the split pane above is hidden below lg) */}
      {showScanInspector && !isDesktop && (
        <div className="fixed inset-0 z-50 bg-slate-950">
          <ScanInspector
            activeScanPage={activeScanPage}
            setActiveScanPage={setActiveScanPage}
            onClose={() => setShowScanInspector(false)}
            currentVolume={currentVolume}
            currentDataset={currentDataset}
          />
        </div>
      )}

      {/* Mobile Floating Scan Button */}
      {!showScanInspector && !isDesktop && (
        <div className="fixed bottom-4 right-4 z-40">
          <button
            onClick={() => setShowScanInspector(true)}
            className="flex items-center gap-2 px-4 py-2.5 rounded-full bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs shadow-2xl border border-amber-400 cursor-pointer"
          >
            <Eye className="w-4 h-4" />
            <span>View Scan P.{activeScanPage}</span>
          </button>
        </div>
      )}

    </div>
  );
}
