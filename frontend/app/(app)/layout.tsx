"use client";

import "../globals.css";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  Users, 
  GitCommit, 
  Settings, 
  LogOut, 
  Sparkles, 
  MessageSquare, 
  Play, 
  RotateCcw, 
  Database,
  ChevronUp,
  ChevronDown,
  Info
} from "lucide-react";
import { LeadProvider, useLeads } from "../../lib/lead-context";
import { useState } from "react";

function SidebarNav() {
  const pathname = usePathname();

  const menuItems = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { name: "Leads", href: "/leads", icon: Users },
    { name: "Conversations", href: "/conversations", icon: MessageSquare },
    { name: "Pipeline", href: "/pipeline", icon: GitCommit },
    { name: "Settings", href: "/settings", icon: Settings },
  ];

  return (
    <nav className="mt-6 px-3 space-y-1">
      {menuItems.map((item) => {
        const Icon = item.icon;
        const isActive = pathname === item.href;
        return (
          <Link
            key={item.name}
            href={item.href}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 ${
              isActive
                ? "bg-white/5 text-[#6366f1] border-l-2 border-[#6366f1] shadow-[inset_4px_0_12px_rgba(99,102,241,0.06)]"
                : "text-gray-400 hover:text-white hover:bg-white/5"
            }`}
          >
            <Icon className={`w-4 h-4 ${isActive ? "text-[#6366f1]" : "text-gray-400"}`} strokeWidth={2} />
            <span>{item.name}</span>
          </Link>
        );
      })}
    </nav>
  );
}

function DemoControllerPanel() {
  const { demoScriptStep, triggerDemoStep, generate50DemoLeads, resetDatabase, isBackendOnline } = useLeads();
  const [isOpen, setIsOpen] = useState(true);

  const steps = [
    { num: 1, name: "New Lead Inbound", desc: "Ingest Avery/Sarah Jenkins raw prospect" },
    { num: 2, name: "AI Qualify & Score", desc: "Analyze tech gaps & diagnose latency pain (HOT)" },
    { num: 3, name: "AI Outreach Sent", desc: "Generate outbound pitch targeting checkout issues" },
    { num: 4, name: "Customer Reply Received", desc: "Simulate incoming query requesting pricing/demo" },
    { num: 5, name: "AI Reply Sentiment", desc: "Parse response, update conversion odds to 95%" },
    { num: 6, name: "Followup Task Set", desc: "Auto-schedule reminder & draft calendar link" },
    { num: 7, name: "Deal Converted!", desc: "Mark lead as Converted & book demo successfully" },
  ];

  const handleNextStep = () => {
    const next = demoScriptStep < 7 ? demoScriptStep + 1 : 1;
    triggerDemoStep(next);
  };

  return (
    <div className="fixed bottom-4 right-4 z-50 max-w-sm w-80 bg-slate-900/95 border border-indigo-500/30 text-white rounded-2xl shadow-[0_10px_30px_rgba(99,102,241,0.2)] backdrop-blur-md overflow-hidden font-sans transition-all duration-300">
      <div 
        onClick={() => setIsOpen(!isOpen)} 
        className="flex items-center justify-between px-4 py-3 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 border-b border-indigo-500/20 cursor-pointer select-none"
      >
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-indigo-400 animate-pulse" />
          <span className="text-xs font-bold font-display uppercase tracking-wider text-indigo-200">Demo Control Hub</span>
        </div>
        {isOpen ? <ChevronDown className="w-4 h-4 text-slate-400" /> : <ChevronUp className="w-4 h-4 text-slate-400" />}
      </div>

      {isOpen && (
        <div className="p-4 space-y-4 text-xs">
          {/* Quick Setup Actions */}
          <div className="grid grid-cols-2 gap-2 border-b border-slate-800 pb-3">
            <button
              onClick={generate50DemoLeads}
              className="flex items-center justify-center gap-1.5 px-3 py-2 bg-indigo-600/90 hover:bg-indigo-600 text-white rounded-lg font-medium transition-all shadow-[0_2px_8px_rgba(99,102,241,0.2)] font-display"
            >
              <Database className="w-3.5 h-3.5" />
              <span>Load 50 Leads</span>
            </button>
            <button
              onClick={resetDatabase}
              className="flex items-center justify-center gap-1.5 px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 rounded-lg font-medium transition-all"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset State</span>
            </button>
          </div>

          {/* Demo Script Walkthrough */}
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="font-semibold text-indigo-300">2-Min Sales Story</span>
              <span className="text-[10px] bg-indigo-900/60 border border-indigo-500/30 text-indigo-300 px-2 py-0.5 rounded font-mono font-bold">
                Step {demoScriptStep}/7
              </span>
            </div>
            
            <p className="text-[10px] text-slate-400 leading-normal">
              Click &quot;Play Next Step&quot; to simulate a live end-to-end sales automation flow.
            </p>

            {/* Steps Stepper Tracker */}
            <div className="max-h-36 overflow-y-auto space-y-1.5 pr-1 bg-slate-950/40 p-2 rounded-lg border border-slate-800">
              {steps.map((st) => (
                <div 
                  key={st.num}
                  onClick={() => triggerDemoStep(st.num)}
                  className={`p-1.5 rounded transition-all cursor-pointer flex items-center gap-2 border ${
                    demoScriptStep === st.num 
                      ? "bg-indigo-600/20 border-indigo-500 text-white font-semibold"
                      : demoScriptStep > st.num
                      ? "bg-emerald-500/5 border-emerald-500/20 text-emerald-400/80"
                      : "bg-transparent border-transparent text-slate-500 hover:text-slate-300"
                  }`}
                >
                  <span className={`w-4 h-4 rounded-full flex items-center justify-center text-[10px] border shrink-0 ${
                    demoScriptStep === st.num 
                      ? "bg-indigo-500 border-indigo-400 text-white"
                      : demoScriptStep > st.num
                      ? "bg-emerald-500 border-emerald-400 text-white"
                      : "border-slate-700 text-slate-500"
                  }`}>
                    {st.num}
                  </span>
                  <div className="flex flex-col min-w-0">
                    <span className="text-[10px] truncate">{st.name}</span>
                    <span className="text-[8px] text-slate-500 truncate leading-none mt-0.5">{st.desc}</span>
                  </div>
                </div>
              ))}
            </div>

            <button
              onClick={handleNextStep}
              className="w-full flex items-center justify-center gap-1.5 px-3 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-semibold transition-all shadow-[0_2px_8px_rgba(16,185,129,0.2)] font-display"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>{demoScriptStep === 0 ? "Start Demo Script" : demoScriptStep === 7 ? "Restart Script" : "Play Next Step"}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function MainLayoutContent({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { isBackendOnline, leads } = useLeads();

  const getPageTitle = () => {
    switch (pathname) {
      case "/dashboard": return "Dashboard";
      case "/leads": return "Leads Page";
      case "/conversations": return "Conversations";
      case "/pipeline": return "Sales Pipeline";
      case "/settings": return "Settings";
      default: return "Command Center";
    }
  };

  return (
    <div className="flex h-screen bg-[#F8FAFC] text-[#131b2e] font-sans antialiased overflow-hidden">
      {/* Sidebar */}
      <aside className="w-[240px] bg-[#0f172a] border-r border-white/5 flex flex-col justify-between shrink-0">
        <div>
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 px-6 py-6 border-b border-white/5 hover:opacity-90 transition-opacity">
            <img src="/logo.jpg" alt="LeadFlow Logo" className="w-6 h-6 rounded-md shadow-[0_0_10px_rgba(99,102,241,0.5)] shrink-0 object-cover" />
            <span className="font-semibold text-lg tracking-tight font-display text-white inline-flex items-center gap-1">
              LeadFlow <span className="text-[10px] bg-[#10b981]/15 text-[#10b981] border border-[#10b981]/30 px-1.5 py-0.5 rounded font-bold inline-flex items-center h-5">AI</span>
            </span>
          </Link>

          {/* Navigation Menu */}
          <SidebarNav />
        </div>

        {/* Sidebar Footer / User Profile & Logout */}
        <div className="p-4 border-t border-white/5 space-y-3">
          <div className="flex items-center gap-3 px-2 py-1">
            <div className="w-8 h-8 rounded-full bg-[#6366f1] flex items-center justify-center font-bold text-white shadow-inner">
              U
            </div>
            <div className="flex flex-col">
              <span className="text-xs font-semibold text-white">Sales Administrator</span>
              <span className="text-[10px] text-gray-500">admin@leadflow.ai</span>
            </div>
          </div>
          <Link
            href="/"
            className="flex items-center gap-3 px-4 py-2.5 w-full rounded-lg text-sm font-medium text-rose-400 hover:bg-rose-500/10 hover:text-rose-300 transition-all duration-200"
          >
            <LogOut className="w-4 h-4" strokeWidth={2} />
            <span>Logout to Web</span>
          </Link>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Header */}
        <header className="h-16 bg-white/80 backdrop-blur-md border-b border-slate-200/80 flex items-center justify-between px-8 shrink-0">
          <div className="flex items-center gap-3">
            <h2 className="text-sm font-semibold font-display text-slate-800 uppercase tracking-wider">
              {getPageTitle()}
            </h2>
            <div className="flex items-center ml-1">
              {isBackendOnline ? (
                <span className="relative flex h-2.5 w-2.5" title="Backend Live">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                </span>
              ) : (
                <span className="h-2.5 w-2.5 rounded-full bg-slate-300 inline-block" title="Local Simulator" />
              )}
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* Quick stats glow */}
            <div className="hidden sm:flex items-center gap-2 bg-indigo-50 text-[#6366f1] border border-indigo-100 px-3 py-1 rounded-full text-xs font-semibold shadow-sm">
              <Sparkles className="w-3.5 h-3.5" />
              <span>AI Agents Active: 3 / 3</span>
            </div>
          </div>
        </header>

        {/* Content Body */}
        <main className="flex-1 overflow-y-auto p-8 bg-[#F8FAFC] relative">
          {children}
        </main>
      </div>

      {/* Demo Script Controller */}
      <DemoControllerPanel />
    </div>
  );
}

export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <LeadProvider>
      <MainLayoutContent>{children}</MainLayoutContent>
    </LeadProvider>
  );
}
