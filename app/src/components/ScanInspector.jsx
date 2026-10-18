import React, { useEffect, useRef, useState } from 'react';
import {
  X,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  ChevronLeft,
  ChevronRight,
  Maximize2,
  FileSearch,
  Sparkles
} from 'lucide-react';

const MIN_ZOOM = 0.5;
const MAX_ZOOM = 3;
const ZOOM_STEP = 0.25;

const pageOf = (s) => s.page ?? s.pageNumber;

export default function ScanInspector({
  activeScanPage,
  setActiveScanPage,
  onClose,
  currentVolume,
  currentDataset
}) {
  const [zoom, setZoom] = useState(1);
  const [isFullModal, setIsFullModal] = useState(false);
  const [imageFailed, setImageFailed] = useState(false);
  const canvasRef = useRef(null);
  const dragRef = useRef(null);

  const scans = currentDataset?.scansCatalog || [];
  const pageList = scans.map(pageOf);
  const currentIdx = pageList.indexOf(activeScanPage);
  const currentScan = scans[currentIdx] || {
    page: activeScanPage,
    notebookPage: activeScanPage,
    title: `Archival Lecture Scan Page ${activeScanPage}`
  };
  const notebookPageNum = currentScan.notebookPage || activeScanPage;

  const minPage = pageList.length ? pageList[0] : 1;
  const maxPage = pageList.length ? pageList[pageList.length - 1] : (currentVolume?.totalPages || 200);

  const goTo = (page) => {
    setActiveScanPage(page);
    setZoom(1);
  };
  const handleNext = () => {
    if (currentIdx >= 0 && currentIdx < pageList.length - 1) goTo(pageList[currentIdx + 1]);
    else if (currentIdx < 0 && activeScanPage < maxPage) goTo(activeScanPage + 1);
  };
  const handlePrev = () => {
    if (currentIdx > 0) goTo(pageList[currentIdx - 1]);
    else if (currentIdx < 0 && activeScanPage > minPage) goTo(activeScanPage - 1);
  };

  const rawFolder = currentVolume?.scanBasePath || currentDataset?.meta?.scanBasePath || 'scans_p1';
  const cleanFolder = rawFolder.replace(/^\/+/, '');
  const basePrefix = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : `${import.meta.env.BASE_URL}/`;
  const imageSrc = `${basePrefix}${cleanFolder}/page_${String(activeScanPage).padStart(3, '0')}.png`;

  useEffect(() => {
    setImageFailed(false);
    if (canvasRef.current) canvasRef.current.scrollTo({ top: 0, left: 0 });
  }, [imageSrc]);

  // Esc leaves the full-screen modal; arrow keys page through scans (not while typing).
  useEffect(() => {
    const onKey = (e) => {
      const tag = (e.target?.tagName || '').toLowerCase();
      if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
      if (e.key === 'Escape' && isFullModal) setIsFullModal(false);
      else if (e.key === 'ArrowRight') handleNext();
      else if (e.key === 'ArrowLeft') handlePrev();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  // Drag-to-pan: the image is sized by width, so scrolling the canvas pans the whole page.
  const onPointerDown = (e) => {
    if (e.button !== 0 || !canvasRef.current) return;
    dragRef.current = {
      x: e.clientX,
      y: e.clientY,
      left: canvasRef.current.scrollLeft,
      top: canvasRef.current.scrollTop
    };
    canvasRef.current.setPointerCapture(e.pointerId);
  };
  const onPointerMove = (e) => {
    const d = dragRef.current;
    if (!d || !canvasRef.current) return;
    canvasRef.current.scrollLeft = d.left - (e.clientX - d.x);
    canvasRef.current.scrollTop = d.top - (e.clientY - d.y);
  };
  const endDrag = () => { dragRef.current = null; };

  const zoomIn = () => setZoom((z) => Math.min(+(z + ZOOM_STEP).toFixed(2), MAX_ZOOM));
  const zoomOut = () => setZoom((z) => Math.max(+(z - ZOOM_STEP).toFixed(2), MIN_ZOOM));

  const btn = 'p-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition cursor-pointer disabled:opacity-40 disabled:pointer-events-none';

  return (
    <div className={`flex flex-col bg-slate-900 border-l border-slate-800 text-slate-100 ${
      isFullModal ? 'fixed inset-0 z-[60] p-4 bg-slate-950/95' : 'h-full'
    }`}>

      {/* Top Header */}
      <div className="p-3 border-b border-slate-800 flex items-center justify-between bg-slate-950/80">
        <div className="flex items-center gap-2 min-w-0">
          <FileSearch className="w-4 h-4 text-indigo-400 shrink-0" />
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-white">Original Handwritten Scan</span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                Scan #{activeScanPage} / Note P.{notebookPageNum}
              </span>
            </div>
            <p className="text-[11px] text-slate-400 truncate">{currentScan.title}</p>
          </div>
        </div>

        {/* Controls */}
        <div className="flex items-center gap-1.5">
          <button onClick={zoomIn} disabled={zoom >= MAX_ZOOM} className={btn} title="Zoom In">
            <ZoomIn className="w-4 h-4" />
          </button>
          <button onClick={zoomOut} disabled={zoom <= MIN_ZOOM} className={btn} title="Zoom Out">
            <ZoomOut className="w-4 h-4" />
          </button>
          <button onClick={() => setZoom(1)} className={btn} title="Reset Zoom">
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
          <button onClick={() => setIsFullModal(!isFullModal)} className={btn} title="Expand Full Screen (Esc to exit)">
            <Maximize2 className="w-4 h-4" />
          </button>
          <button
            onClick={onClose}
            className="p-1 rounded bg-slate-800 hover:bg-red-500/20 text-slate-400 hover:text-red-400 transition cursor-pointer"
            title="Close Scan Inspector"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Page Selector Strip */}
      <div className="px-3 py-2 border-b border-slate-800/80 bg-slate-900/60 flex items-center justify-between text-xs">
        <div className="flex items-center gap-1">
          <button onClick={handlePrev} disabled={activeScanPage <= minPage} className={btn} title="Previous page (←)">
            <ChevronLeft className="w-3.5 h-3.5" />
          </button>
          <span className="font-mono text-slate-300 px-1">
            Page {activeScanPage} of {maxPage}
          </span>
          <button onClick={handleNext} disabled={activeScanPage >= maxPage} className={btn} title="Next page (→)">
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
          <span className="font-mono text-slate-500 pl-1">{Math.round(zoom * 100)}%</span>
        </div>

        {/* Quick Jump Dropdown */}
        <select
          value={activeScanPage}
          onChange={(e) => goTo(Number(e.target.value))}
          className="bg-slate-800 border border-slate-700 rounded px-2 py-0.5 text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-indigo-500 max-w-[200px] truncate"
        >
          {scans.map((s) => {
            const p = pageOf(s);
            const np = s.notebookPage || p;
            const t = s.title || '';
            return (
              <option key={p} value={p}>
                Scan {p} (Note P.{np}) — {t.length > 24 ? `${t.slice(0, 24)}...` : t}
              </option>
            );
          })}
        </select>
      </div>

      {/* Image Viewing Canvas: width-based zoom + native scroll, so every edge stays reachable */}
      <div
        ref={canvasRef}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={endDrag}
        onPointerCancel={endDrag}
        className={`flex-1 overflow-auto p-4 bg-slate-950 ${zoom > 1 ? 'cursor-grab active:cursor-grabbing' : ''}`}
        style={{ touchAction: zoom > 1 ? 'none' : 'auto' }}
      >
        <div className="mx-auto" style={{ width: `${zoom * 100}%` }}>
          {imageFailed ? (
            <div className="p-8 text-center text-xs text-slate-400 border border-slate-800 rounded-lg">
              Scan file not found: <span className="font-mono text-amber-400">{imageSrc}</span>
            </div>
          ) : (
            <img
              src={imageSrc}
              alt={`Handwritten scan ${activeScanPage}`}
              draggable={false}
              onError={() => setImageFailed(true)}
              className="w-full h-auto rounded-lg shadow-2xl border border-slate-800 bg-white select-none"
            />
          )}
        </div>
      </div>

      {/* Footer Banner */}
      <div className="p-2 border-t border-slate-800 bg-slate-950 text-[11px] text-slate-400 flex items-center justify-between">
        <span className="flex items-center gap-1.5 text-amber-400">
          <Sparkles className="w-3 h-3" /> {currentVolume?.shortTitle || 'Shubhra Ranjan IAS Lecture Notes'}
        </span>
        <span className="text-slate-500 font-mono text-[10px]">{baseFolder}</span>
      </div>

    </div>
  );
}
