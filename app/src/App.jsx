import React, { useCallback, useEffect, useState } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import UniversalVisualNotesView from './components/UniversalVisualNotesView';
import MindMapView from './components/MindMapView';
import FlashcardsView from './components/FlashcardsView';
import AnswerWritingView from './components/AnswerWritingView';
import ScanInspector from './components/ScanInspector';
import { getVolumeById, volumesByStep } from './data/volumesCatalog';
import useProgress from './useProgress';
import { Eye, Loader2 } from 'lucide-react';

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
  const study = useProgress();
  // First visit opens Step 1 of the suggested order; later visits reopen the last volume.
  const [activeVolumeId, setActiveVolumeId] = useState(
    () => getVolumeById(study.progress.lastVolumeId || volumesByStep[0].id).id
  );
  const [viewMode, setViewMode] = useState('notes'); // 'notes' | 'mindmap' | 'flashcards' | 'answers'
  const isDesktop = useIsDesktop();
  // The scan pane opens when a "Scan P.x" button is pressed, so the first screen is the study guide.
  const [showScanInspector, setShowScanInspector] = useState(false);
  const [activeScanPage, setActiveScanPage] = useState(() => getVolumeById(activeVolumeId).defaultScan || 1);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  // { id, nonce } - set by the sidebar or "Continue", consumed by the notes view once it has scrolled.
  const [jumpTarget, setJumpTarget] = useState(null);
  // { category, answerId, nonce } - "Test yourself" / "Practice answer" from a topic.
  const [studyTarget, setStudyTarget] = useState(null);

  // Volumes are loaded on demand and cached, so the first visit downloads one volume, not six.
  const [datasets, setDatasets] = useState({});
  const [loadError, setLoadError] = useState(null);
  const currentVolume = getVolumeById(activeVolumeId);
  const currentDataset = datasets[activeVolumeId] || null;

  useEffect(() => {
    if (datasets[activeVolumeId]) return undefined;
    let cancelled = false;
    setLoadError(null);
    currentVolume.load()
      .then((d) => { if (!cancelled) setDatasets((all) => ({ ...all, [activeVolumeId]: d })); })
      .catch((e) => { if (!cancelled) setLoadError(String(e?.message || e)); });
    return () => { cancelled = true; };
  }, [activeVolumeId, currentVolume, datasets]);

  const { setLastVolume } = study;
  useEffect(() => { setLastVolume(activeVolumeId); }, [activeVolumeId, setLastVolume]);

  const handleSelectVolume = (newVolId) => {
    setActiveVolumeId(newVolId);
    setSearchQuery('');
    setJumpTarget(null);
    setStudyTarget(null);
    setViewMode('notes');
    setActiveScanPage(getVolumeById(newVolId).defaultScan || 1);
    window.scrollTo({ top: 0 });
  };

  const handleSelectScanPage = (pageNum) => {
    setActiveScanPage(pageNum);
    setShowScanInspector(true);
  };

  const scrollToSection = useCallback((sectionId) => {
    setViewMode('notes');
    setSearchQuery('');
    setJumpTarget({ id: sectionId, nonce: Date.now() });
  }, []);

  const clearJump = useCallback(() => setJumpTarget(null), []);

  const startStudy = useCallback((mode, target) => {
    setStudyTarget({ ...target, nonce: Date.now() });
    setViewMode(mode);
    window.scrollTo({ top: 0 });
  }, []);

  const changeView = (mode) => {
    setStudyTarget(null);
    setViewMode(mode);
  };

  const renderInspector = () => (
    <ScanInspector
      activeScanPage={activeScanPage}
      setActiveScanPage={setActiveScanPage}
      onClose={() => setShowScanInspector(false)}
      currentVolume={currentVolume}
      currentDataset={currentDataset}
    />
  );
  const globalPaneVisible = showScanInspector && isDesktop && viewMode !== 'notes' && !!currentDataset;
  const studyKey = `${activeVolumeId}-${studyTarget?.nonce || 0}`;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">

      <Navbar
        activeVolumeId={activeVolumeId}
        setActiveVolumeId={handleSelectVolume}
        currentVolume={currentVolume}
        currentDataset={currentDataset}
        viewMode={viewMode}
        setViewMode={changeView}
        showScanInspector={showScanInspector}
        setShowScanInspector={setShowScanInspector}
        toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        activeScanPage={activeScanPage}
      />

      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        activeVolumeId={activeVolumeId}
        setActiveVolumeId={handleSelectVolume}
        currentVolume={currentVolume}
        currentDataset={currentDataset}
        scrollToSection={scrollToSection}
        onSelectScanPage={handleSelectScanPage}
        study={study}
      />

      <div className="flex-1 flex relative">

        {/* Every view is keyed by volume so per-volume UI state resets instead of leaking into the next volume. */}
        <main className={`flex-1 min-w-0 p-4 sm:p-6 lg:p-8 transition-all duration-300 ${
          globalPaneVisible ? 'lg:max-w-[58%] xl:max-w-[62%]' : 'max-w-7xl mx-auto w-full'
        }`}>
          {!currentDataset ? (
            <div className="max-w-5xl mx-auto p-12 text-center rounded-2xl bg-slate-900/60 border border-slate-800 text-slate-400 text-sm">
              {loadError ? (
                <span className="text-red-300">Could not load this volume: {loadError}. Check your connection and reload.</span>
              ) : (
                <span className="inline-flex items-center gap-2"><Loader2 className="w-4 h-4 animate-spin text-amber-400" /> Loading {currentVolume.shortTitle}…</span>
              )}
            </div>
          ) : (
            <>
              {viewMode === 'notes' && (
                <UniversalVisualNotesView
                  key={activeVolumeId}
                  currentVolume={currentVolume}
                  currentDataset={currentDataset}
                  onSelectScanPage={handleSelectScanPage}
                  searchQuery={searchQuery}
                  jumpTarget={jumpTarget}
                  onJumpHandled={clearJump}
                  onJumpTo={scrollToSection}
                  activeScanPage={activeScanPage}
                  inspectorOpen={showScanInspector && isDesktop}
                  renderInspector={renderInspector}
                  study={study}
                  onStudy={startStudy}
                  onSwitchVolume={handleSelectVolume}
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
                  key={studyKey}
                  currentVolume={currentVolume}
                  currentDataset={currentDataset}
                  onSelectScanPage={handleSelectScanPage}
                  initialCategory={studyTarget?.category}
                />
              )}

              {viewMode === 'answers' && (
                <AnswerWritingView
                  key={studyKey}
                  currentVolume={currentVolume}
                  currentDataset={currentDataset}
                  onSelectScanPage={handleSelectScanPage}
                  initialAnswerId={studyTarget?.answerId}
                />
              )}
            </>
          )}
        </main>

        {/* Right pane (mind map / flashcards / answers): sticky and one viewport tall. In the notes view
            the inspector is embedded in the section being read instead (see UniversalVisualNotesView). */}
        {globalPaneVisible && (
          <aside className="flex flex-col w-[42%] xl:w-[38%] sticky top-16 self-start h-[calc(100vh-4rem)] border-l border-slate-800 bg-slate-900 shadow-2xl z-20">
            {renderInspector()}
          </aside>
        )}

      </div>

      {/* Mobile: full-screen scan overlay (there is no split pane below lg) */}
      {showScanInspector && !isDesktop && currentDataset && (
        <div className="fixed inset-0 z-50 bg-slate-950">
          {renderInspector()}
        </div>
      )}

      {!showScanInspector && !isDesktop && currentDataset && viewMode !== 'notes' && (
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
