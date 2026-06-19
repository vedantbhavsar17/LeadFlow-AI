"use client";

import "../globals.css";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Users, GitCommit, Settings, LogOut, Sparkles } from "lucide-react";

export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  const menuItems = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { name: "Leads", href: "/leads", icon: Users },
    { name: "Pipeline", href: "/pipeline", icon: GitCommit },
    { name: "Settings", href: "/settings", icon: Settings },
  ];

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
              {menuItems.find((item) => item.href === pathname)?.name || "Command Center"}
            </h2>
            <span className="text-[10px] text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full border border-slate-200 font-medium">
              Production Env
            </span>
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
        <main className="flex-1 overflow-y-auto p-8 bg-[#F8FAFC]">
          {children}
        </main>
      </div>
    </div>
  );
}
