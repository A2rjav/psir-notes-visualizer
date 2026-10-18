import React, { useState } from 'react';
import { 
  Shield, 
  Zap, 
  Cpu, 
  HeartPulse, 
  GraduationCap, 
  BookOpen, 
  Scale, 
  AlertTriangle, 
  CheckCircle2, 
  ExternalLink, 
  Sparkles, 
  Quote, 
  Anchor, 
  Plane, 
  FileText, 
  ChevronDown, 
  ChevronUp, 
  HelpCircle,
  Eye,
  Info
} from 'lucide-react';
import { indiaUsData } from '../data/indiaUsData';

export default function VisualNotesView({ onSelectScanPage, searchQuery }) {
  const [expandedPillar, setExpandedPillar] = useState('pillar-1');
  const [expandedPhase, setExpandedPhase] = useState(3); // Phase III
  const [activeClndaSection, setActiveClndaSection] = useState('Section 17(b) [The Most Contentious Clause]');

  const iconMap = {
    Shield,
    Zap,
    Cpu,
    HeartPulse,
    GraduationCap
  };

  // Helper for clicking a scan reference
  const renderScanPill = (scanPage, notebookPage) => (
    <button
      onClick={() => onSelectScanPage(scanPage)}
      className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-400 hover:text-indigo-300 border border-indigo-500/30 transition shadow-sm ml-1.5 cursor-pointer"
      title={`Open Original Handwritten Scan ${scanPage} (Notebook Page ${notebookPage})`}
    >
      <Eye className="w-2.5 h-2.5" />
      Scan P.{scanPage} [Note P.{notebookPage}]
    </button>
  );

  return (
    <div className="space-y-12 max-w-5xl mx-auto pb-16">
      
      {/* Hero Banner */}
      <section id="status-pillars" className="relative p-6 sm:p-8 rounded-2xl bg-gradient-to-br from-slate-900 via-slate-900 to-amber-950/40 border border-slate-800 shadow-xl overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-10 pointer-events-none">
          <BookOpen className="w-64 h-64 text-amber-500" />
        </div>

        <div className="relative z-10 space-y-4">
          <div className="flex flex-wrap items-center gap-2">
            <span className="px-2.5 py-1 rounded-md text-xs font-bold uppercase tracking-wider bg-amber-500/20 text-amber-400 border border-amber-500/30">
              {indiaUsData.meta.paper}
            </span>
            <span className="px-2.5 py-1 rounded-md text-xs font-semibold bg-slate-800 text-slate-300 border border-slate-700">
              {indiaUsData.meta.lectureInfo}
            </span>
            <span className="px-2.5 py-1 rounded-md text-xs font-mono bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
              {indiaUsData.meta.notebookPages}
            </span>
          </div>

          <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
            {indiaUsData.meta.title}
          </h1>
          <p className="text-sm sm:text-base text-amber-300/90 font-medium">
            "{indiaUsData.meta.theme}"
          </p>

          <div className="pt-2 grid sm:grid-cols-2 gap-3 text-xs">
            <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
              <span className="text-slate-400 block mb-0.5">Official Status:</span>
              <span className="text-slate-100 font-semibold">{indiaUsData.meta.officialStatus}</span>
            </div>
            <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
              <span className="text-slate-400 block mb-0.5">Institutional Mechanism:</span>
              <span className="text-slate-100 font-semibold">{indiaUsData.meta.institutionalMechanism}</span>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 1: The Five Pillars of Strategic Partnership */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-5 bg-amber-500 rounded-full" />
            <h2 className="text-lg font-bold text-white tracking-tight">
              The Five Pillars of Strategic Partnership
            </h2>
            {renderScanPill(5, 80)}
          </div>
          <span className="text-xs text-slate-400 hidden sm:inline">Institutionalised Strategic & Commercial Dialogue</span>
        </div>

        <div className="grid sm:grid-cols-5 gap-3">
          {indiaUsData.fivePillars.map((pillar) => {
            const Icon = iconMap[pillar.icon] || Shield;
            const isSelected = expandedPillar === pillar.id;

            return (
              <div 
                key={pillar.id}
                onClick={() => setExpandedPillar(pillar.id)}
                className={`p-4 rounded-xl border cursor-pointer transition-all ${
                  isSelected 
                    ? 'bg-amber-500/10 border-amber-500/60 shadow-lg shadow-amber-500/10 sm:col-span-3' 
                    : 'bg-slate-900/80 border-slate-800 hover:border-slate-700 hover:bg-slate-800/60 sm:col-span-2 lg:col-span-1'
                }`}
              >
                <div className="flex items-center gap-2 mb-2">
                  <div className={`p-2 rounded-lg ${isSelected ? 'bg-amber-500 text-slate-950' : 'bg-slate-800 text-amber-400'}`}>
                    <Icon className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="text-[10px] font-mono text-slate-400 uppercase">Pillar ({pillar.number})</span>
                    <h3 className="text-xs font-bold text-white leading-tight">{pillar.title}</h3>
                  </div>
                </div>

                {isSelected ? (
                  <div className="mt-3 pt-3 border-t border-amber-500/20 text-xs space-y-2">
                    <p className="text-slate-300 leading-relaxed">{pillar.description}</p>
                    <div>
                      <span className="text-[11px] font-semibold text-amber-400 block mb-1">Key Initiatives & Forums:</span>
                      <ul className="space-y-1">
                        {pillar.initiatives.map((init, idx) => (
                          <li key={idx} className="flex items-start gap-1.5 text-slate-300">
                            <span className="text-amber-500 font-bold">•</span>
                            <span>{init}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ) : (
                  <p className="text-[11px] text-slate-400 line-clamp-2 mt-1">
                    {pillar.description}
                  </p>
                )}
              </div>
            );
          })}
        </div>
      </section>

      {/* SECTION 2: How Leaders Explain the Relationship */}
      <section id="leaders-quotes" className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-5 bg-amber-500 rounded-full" />
            <h2 className="text-lg font-bold text-white tracking-tight">
              How Leaders Characterize the Relationship
            </h2>
            {renderScanPill(5, 80)}
          </div>
          <span className="text-xs text-slate-400">Verbatim Quotes in Notes</span>
        </div>

        <div className="grid md:grid-cols-3 gap-3">
          {indiaUsData.leadersCharacterizations.map((item, idx) => (
            <div 
              key={idx}
              className="p-4 rounded-xl bg-slate-900/90 border border-slate-800/90 hover:border-slate-700 space-y-2.5 transition flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-xs font-bold text-amber-400">{item.leader}</span>
                  {renderScanPill(item.scanPage, item.notebookPage)}
                </div>
                <span className="text-[10px] text-slate-400 block mb-2">{item.role}</span>
                <blockquote className="font-serif-quote italic text-sm text-slate-200 border-l-2 border-amber-500/80 pl-2.5 my-2">
                  "{item.quote}"
                </blockquote>
              </div>
              <p className="text-[11px] text-slate-400 pt-2 border-t border-slate-800/80 leading-snug">
                {item.context}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* SECTION 3: Directory of Scholars & Thinkers */}
      <section id="thinkers-matrix" className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-5 bg-amber-500 rounded-full" />
            <h2 className="text-lg font-bold text-white tracking-tight">
              Thinkers & Scholarly Debates Matrix
            </h2>
            {renderScanPill(6, 81)}
          </div>
          <span className="text-xs text-amber-400 font-semibold">12 Core Scholars</span>
        </div>

        <div className="grid sm:grid-cols-2 gap-3.5">
          {indiaUsData.thinkersDirectory.map((t, idx) => (
            <div 
              key={idx}
              className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 hover:border-amber-500/40 transition space-y-2 group"
            >
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-sm font-bold text-white group-hover:text-amber-400 transition">
                    {t.name}
                  </h3>
                  <span className="text-[10px] text-slate-400 block">{t.designation}</span>
                </div>
                {renderScanPill(t.scanPage, t.notebookPage)}
              </div>

              <div className="inline-block px-2 py-0.5 rounded text-[11px] font-semibold bg-amber-500/10 text-amber-300 border border-amber-500/20">
                Key Concept: {t.concept}
              </div>

              <p className="text-xs text-slate-300 leading-relaxed pt-1">
                {t.coreArgument}
              </p>

              {t.work && (
                <div className="text-[11px] text-slate-400 pt-1 flex items-center gap-1 font-mono">
                  <span className="text-slate-500">Source/Work:</span> {t.work}
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* SECTION 4: Chronological Evolution (6 Epochs) */}
      <section id="evolution-timeline" className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-5 bg-amber-500 rounded-full" />
            <h2 className="text-lg font-bold text-white tracking-tight">
              Evolution of India-USA Relations (6 Historical Epochs)
            </h2>
            {renderScanPill(11, 83)}
          </div>
          <span className="text-xs text-slate-400">Pre-1947 to Present Day</span>
        </div>

        <div className="space-y-3">
          {indiaUsData.evolutionTimeline.map((epoch, idx) => {
            const isExpanded = expandedPhase === idx;

            return (
              <div 
                key={idx}
                className="rounded-xl border border-slate-800 bg-slate-900/80 overflow-hidden transition"
              >
                <button
                  onClick={() => setExpandedPhase(isExpanded ? null : idx)}
                  className="w-full p-4 text-left flex items-center justify-between hover:bg-slate-800/40 transition"
                >
                  <div className="flex items-center gap-3">
                    <span className="px-2 py-1 rounded text-xs font-mono font-bold bg-slate-800 text-amber-400 border border-slate-700">
                      {epoch.period}
                    </span>
                    <div>
                      <span className="text-[10px] text-slate-400 block uppercase font-mono">{epoch.phase}</span>
                      <h3 className="text-sm font-bold text-white">{epoch.title}</h3>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    {renderScanPill(epoch.scanPage, epoch.notebookPage)}
                    {isExpanded ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
                  </div>
                </button>

                {isExpanded && (
                  <div className="p-4 border-t border-slate-800 bg-slate-950/60 space-y-2 text-xs">
                    <ul className="space-y-2">
                      {epoch.details.map((point, pIdx) => (
                        <li key={pIdx} className="flex items-start gap-2 text-slate-300 leading-relaxed">
                          <span className="text-amber-500 font-bold shrink-0 mt-0.5">•</span>
                          <span>{point}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>

      {/* SECTION 5: Civil Nuclear Deal & CLNDA 2010 Breakdown */}
      <section id="nuclear-deal" className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-5 bg-amber-500 rounded-full" />
            <h2 className="text-lg font-bold text-white tracking-tight">
              Indo-US Civil Nuclear Cooperation & CLNDA 2010
            </h2>
            {renderScanPill(19, 87)}
          </div>
          <span className="text-xs text-amber-400 font-semibold">Historic Watershed</span>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-6">
          
          {/* Core Strategic Gains */}
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-amber-400 mb-2">
              Why the Deal Mattered: Strategic Gains for India
            </h3>
            <div className="grid sm:grid-cols-2 gap-2 text-xs">
              {indiaUsData.civilNuclearDealDeepDive.significanceForIndia.map((sig, sIdx) => (
                <div key={sIdx} className="p-2.5 rounded-lg bg-slate-950/80 border border-slate-800 flex items-start gap-2 text-slate-300">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                  <span>{sig}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Legal Controversy: CLNDA 2010 Clauses */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-xs font-bold uppercase tracking-wider text-amber-400">
                CLNDA 2010: Section-by-Section Legal Breakdown
              </h3>
              <span className="text-[11px] text-slate-400">Lecture 16 (19/04/2017)</span>
            </div>

            <div className="grid sm:grid-cols-3 gap-2 mb-3">
              {indiaUsData.civilNuclearDealDeepDive.clndaBreakdown.clauses.map((c) => (
                <button
                  key={c.section}
                  onClick={() => setActiveClndaSection(c.section)}
                  className={`p-2 rounded-lg text-left text-xs font-medium border transition ${
                    activeClndaSection === c.section
                      ? 'bg-amber-500 text-slate-950 font-bold border-amber-400 shadow-md'
                      : 'bg-slate-950 border-slate-800 text-slate-300 hover:border-slate-700'
                  }`}
                >
                  <span className="block text-[10px] uppercase font-mono opacity-80">{c.section.split(' ')[0]} {c.section.split(' ')[1]}</span>
                  <span className="truncate block">{c.title}</span>
                </button>
              ))}
            </div>

            {/* Selected Clause Detail */}
            {(() => {
              const active = indiaUsData.civilNuclearDealDeepDive.clndaBreakdown.clauses.find(c => c.section === activeClndaSection);
              if (!active) return null;
              return (
                <div className="p-4 rounded-xl bg-amber-500/5 border border-amber-500/30 text-xs space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-amber-300 text-sm">{active.section}: {active.title}</span>
                    {renderScanPill(19, 87)}
                  </div>
                  <p className="text-slate-200 leading-relaxed">{active.content}</p>
                </div>
              );
            })()}
          </div>

          {/* Solution & Implementation Paradox */}
          <div className="grid sm:grid-cols-2 gap-3 pt-2 text-xs">
            <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 space-y-2">
              <h4 className="font-bold text-amber-400 flex items-center gap-1.5">
                <Shield className="w-3.5 h-3.5 text-amber-400" />
                The Modi Govt Solution: INIP
              </h4>
              <p className="text-slate-300 leading-relaxed">
                {indiaUsData.civilNuclearDealDeepDive.clndaBreakdown.solutionsCrafted[0].detail}
              </p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 space-y-2">
              <h4 className="font-bold text-red-400 flex items-center gap-1.5">
                <AlertTriangle className="w-3.5 h-3.5 text-red-400" />
                Implementation Hurdles: Private vs State
              </h4>
              <p className="text-slate-300 leading-relaxed">
                {indiaUsData.civilNuclearDealDeepDive.clndaBreakdown.implementationReality.russiaVsUsa}
              </p>
              <p className="text-slate-400 text-[11px]">
                {indiaUsData.civilNuclearDealDeepDive.clndaBreakdown.implementationReality.westinghouseBankruptcy}
              </p>
            </div>
          </div>

        </div>
      </section>

      {/* SECTION 6: Economic, IPR & Trade Frictions */}
      <section id="economic-frictions" className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-5 bg-amber-500 rounded-full" />
            <h2 className="text-lg font-bold text-white tracking-tight">
              Economic, IPR & Trade Fault Lines
            </h2>
            {renderScanPill(22, 88)}
          </div>
          <span className="text-xs text-slate-400">BIT, Patents, Totalisation</span>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          
          {/* IPR & Bayer vs NATCO Case */}
          <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-amber-400 flex items-center gap-1.5">
                <Scale className="w-4 h-4 text-amber-400" />
                IPR Battles: Sections 3(d) & 84
              </h3>
              {renderScanPill(23, 89)}
            </div>

            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-xs space-y-1.5">
              <span className="font-bold text-slate-200">Anti-Evergreening [Section 3(d)]:</span>
              <p className="text-slate-400 leading-relaxed">
                {indiaUsData.economicTradeFrictions[1].section3.issue}
              </p>
            </div>

            {/* Landmark Case Card */}
            <div className="p-3.5 rounded-xl bg-gradient-to-r from-amber-500/10 to-transparent border border-amber-500/30 text-xs space-y-1">
              <span className="text-[10px] uppercase font-mono font-bold text-amber-400">Landmark Compulsory License Case</span>
              <h4 className="font-bold text-white">Bayer vs. NATCO (2012)</h4>
              <p className="text-slate-300 leading-relaxed">
                Generic <strong>SORANIB</strong> manufactured at ₹8,800/month vs Bayer's patented <strong>NEXAVER</strong> at ₹2,80,000/month. Upheld across all Indian courts.
              </p>
            </div>

            <div className="text-[11px] text-slate-400 font-mono">
              USTR Special 301: India on Priority Watch List | Margin note: Basmati, Haldi, Neem biopiracy.
            </div>
          </div>

          {/* Model BIT & Totalisation */}
          <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-3 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-bold text-indigo-400 flex items-center gap-1.5">
                  <FileText className="w-4 h-4 text-indigo-400" />
                  Model BIT Deadlock & Totalisation
                </h3>
                {renderScanPill(21, 88)}
              </div>

              <div className="space-y-2 text-xs">
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <span className="font-bold text-slate-200 block mb-1">Indian Model BIT (2015) vs US Model BIT (2012):</span>
                  <p className="text-slate-400 leading-relaxed">
                    India mandates <strong>Enterprise-based definition</strong> (physical capital, domestic jobs) vs US <strong>Asset-based definition</strong> (IPR, derivatives). India excludes retrospective taxation and requires 5-year exhaustion of domestic remedies.
                  </p>
                </div>

                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-slate-200">The Totalisation Issue:</span>
                    <span className="font-mono text-amber-400 font-bold">$28 Billion</span>
                  </div>
                  <p className="text-slate-400 leading-relaxed">
                    Indian tech workers pay ~15% US Social Security contributions without receiving pensions due to 10-year vesting rules. Precedent: Australia signed Totalisation with India; US refuses.
                  </p>
                </div>
              </div>
            </div>

            <div className="text-[11px] text-slate-400 pt-1 border-t border-slate-800 font-mono">
              WTO Solar Panel Dispute: US challenged India's Domestic Content Requirement (DCR).
            </div>
          </div>

        </div>
      </section>

      {/* SECTION 7: Defense Partnership & Foundational Pacts */}
      <section id="defense-partnership" className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-5 bg-amber-500 rounded-full" />
            <h2 className="text-lg font-bold text-white tracking-tight">
              Defense Partnership: The Brightest Spot
            </h2>
            {renderScanPill(24, 90)}
          </div>
          <span className="text-xs text-amber-400 font-semibold">$18 Billion Trade Volume</span>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-6">
          
          {/* Procured Platforms Grid */}
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
              Key US Defense Platforms in Indian Arsenal
            </h3>
            <div className="grid sm:grid-cols-3 gap-2 text-xs">
              {indiaUsData.defencePartnership.procuredPlatforms.map((plat, pIdx) => (
                <div key={pIdx} className="p-2.5 rounded-lg bg-slate-950 border border-slate-800">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-amber-300">{plat.name}</span>
                    <span className="text-[10px] font-mono px-1 rounded bg-slate-800 text-slate-300">{plat.qty}</span>
                  </div>
                  <p className="text-[11px] text-slate-400">{plat.role}</p>
                </div>
              ))}
            </div>
          </div>

          {/* 4 Foundational Agreements Matrix */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-xs font-bold uppercase tracking-wider text-amber-400">
                The Four Foundational Defense Agreements
              </h3>
              {renderScanPill(26, 91)}
            </div>

            <div className="grid sm:grid-cols-2 gap-3">
              {indiaUsData.defencePartnership.foundationalAgreements.map((pact) => (
                <div key={pact.acronym} className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white text-sm">{pact.acronym}</span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                      pact.status.includes('Signed') 
                        ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' 
                        : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                    }`}>
                      {pact.status}
                    </span>
                  </div>
                  <span className="text-[11px] text-slate-400 block">{pact.name}</span>
                  <p className="text-slate-300 leading-relaxed pt-1">
                    {pact.details}
                  </p>
                </div>
              ))}
            </div>
          </div>

        </div>
      </section>

      {/* SECTION 8: Six Geopolitical Concerns */}
      <section id="geopolitical-concerns" className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-5 bg-amber-500 rounded-full" />
            <h2 className="text-lg font-bold text-white tracking-tight">
              Six Key Geopolitical Concerns
            </h2>
            {renderScanPill(26, 91)}
          </div>
          <span className="text-xs text-slate-400">Notebook Page 91</span>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
          {indiaUsData.geopoliticalConcerns.map((geo) => (
            <div key={geo.num} className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 space-y-1.5">
              <span className="px-1.5 py-0.5 rounded font-mono text-[10px] font-bold bg-slate-800 text-amber-400">
                Concern {geo.num}
              </span>
              <h3 className="font-bold text-white text-sm">{geo.title}</h3>
              <p className="text-slate-400 leading-relaxed pt-1">
                {geo.divergence}
              </p>
            </div>
          ))}
        </div>
      </section>

    </div>
  );
}
