"use client";

import { useState, useEffect } from "react";
import {
  Users,
  CheckCircle2,
  MessageCircle,
  Target,
  ArrowUpRight,
  Send,
  Check,
  Star,
  Sparkles,
  ChevronRight,
  Calendar,
  ChevronDown,
  ArrowRight,
} from "lucide-react";
import {
  AreaChart,
  Area,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from "recharts";

// Sparkline Mock Data
const leadsSparkline = [
  { v: 10 }, { v: 18 }, { v: 12 }, { v: 24 }, { v: 20 }, { v: 30 }, { v: 35 },
];
const qualifiedSparkline = [
  { v: 8 }, { v: 12 }, { v: 10 }, { v: 18 }, { v: 15 }, { v: 22 }, { v: 28 },
];
const conversationsSparkline = [
  { v: 12 }, { v: 10 }, { v: 16 }, { v: 14 }, { v: 20 }, { v: 18 }, { v: 24 },
];
const rateSparkline = [
  { v: 15 }, { v: 18 }, { v: 16 }, { v: 20 }, { v: 19 }, { v: 22 }, { v: 24.6 },
];

// Donut Chart Data
const channelsData = [
  { name: "Web Forms", value: 40, color: "#3B82F6" },
  { name: "Ads", value: 30, color: "#10B981" },
  { name: "Email", value: 20, color: "#8B5CF6" },
  { name: "Referrals", value: 10, color: "#F59E0B" },
];

// AI Insight Sparkline Data
const insightSparkline = [
  { v: 10 }, { v: 12 }, { v: 15 }, { v: 13 }, { v: 18 }, { v: 16 }, { v: 22 }, { v: 20 }, { v: 25 }, { v: 28 },
];

export default function DashboardPage() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="w-8 h-8 border-4 border-[#6366f1] border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Header Row */}
      <div className="flex justify-between items-center">
        <h1 className="text-xl font-bold font-display text-slate-800 tracking-tight">Dashboard</h1>
        <button className="flex items-center gap-2 px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-semibold text-slate-600 shadow-sm hover:bg-slate-50 transition-colors">
          <Calendar className="w-3.5 h-3.5 text-slate-400" />
          <span>This Month</span>
          <ChevronDown className="w-3 h-3 text-slate-400" />
        </button>
      </div>

      {/* Metrics Row with Sparklines */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Metric 1 - Total Leads */}
        <div className="bg-white border border-slate-200/80 p-6 rounded-2xl shadow-[0_4px_20px_rgba(0,0,0,0.015)] hover:shadow-[0_8px_30px_rgba(0,0,0,0.03)] transition-all flex flex-col">
          <div className="flex justify-between items-start mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider font-display">Total Leads</span>
          </div>
          <div className="flex items-center justify-between mb-4">
            <span className="text-3xl font-bold font-display text-slate-800 tracking-tight">1,248</span>
            <div className="p-2 bg-blue-50 rounded-full">
              <Users className="w-4 h-4 text-[#3B82F6]" />
            </div>
          </div>
          <div className="h-[40px] w-full mb-3">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={leadsSparkline} margin={{ top: 2, bottom: 2, left: 2, right: 2 }}>
                <defs>
                  <linearGradient id="blueSpark" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#3B82F6" stopOpacity={0.15} />
                    <stop offset="100%" stopColor="#3B82F6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <Area type="monotone" dataKey="v" stroke="#3B82F6" strokeWidth={1.5} fill="url(#blueSpark)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <span className="text-xs text-emerald-600 flex items-center gap-1 font-semibold">
            <ArrowUpRight className="w-3 h-3" /> 18.6% <span className="text-slate-400 font-medium">vs last month</span>
          </span>
        </div>

        {/* Metric 2 - Qualified Leads */}
        <div className="bg-white border border-slate-200/80 p-6 rounded-2xl shadow-[0_4px_20px_rgba(0,0,0,0.015)] hover:shadow-[0_8px_30px_rgba(0,0,0,0.03)] transition-all flex flex-col">
          <div className="flex justify-between items-start mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider font-display">Qualified Leads</span>
          </div>
          <div className="flex items-center justify-between mb-4">
            <span className="text-3xl font-bold font-display text-slate-800 tracking-tight">312</span>
            <div className="p-2 bg-emerald-50 rounded-full">
              <CheckCircle2 className="w-4 h-4 text-[#10B981]" />
            </div>
          </div>
          <div className="h-[40px] w-full mb-3">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={qualifiedSparkline} margin={{ top: 2, bottom: 2, left: 2, right: 2 }}>
                <defs>
                  <linearGradient id="greenSpark" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#10B981" stopOpacity={0.15} />
                    <stop offset="100%" stopColor="#10B981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <Area type="monotone" dataKey="v" stroke="#10B981" strokeWidth={1.5} fill="url(#greenSpark)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <span className="text-xs text-emerald-600 flex items-center gap-1 font-semibold">
            <ArrowUpRight className="w-3 h-3" /> 21.3% <span className="text-slate-400 font-medium">vs last month</span>
          </span>
        </div>

        {/* Metric 3 - Conversations */}
        <div className="bg-white border border-slate-200/80 p-6 rounded-2xl shadow-[0_4px_20px_rgba(0,0,0,0.015)] hover:shadow-[0_8px_30px_rgba(0,0,0,0.03)] transition-all flex flex-col">
          <div className="flex justify-between items-start mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider font-display">Conversations</span>
          </div>
          <div className="flex items-center justify-between mb-4">
            <span className="text-3xl font-bold font-display text-slate-800 tracking-tight">128</span>
            <div className="p-2 bg-purple-50 rounded-full">
              <MessageCircle className="w-4 h-4 text-[#8B5CF6]" />
            </div>
          </div>
          <div className="h-[40px] w-full mb-3">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={conversationsSparkline} margin={{ top: 2, bottom: 2, left: 2, right: 2 }}>
                <defs>
                  <linearGradient id="purpleSpark" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#8B5CF6" stopOpacity={0.15} />
                    <stop offset="100%" stopColor="#8B5CF6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <Area type="monotone" dataKey="v" stroke="#8B5CF6" strokeWidth={1.5} fill="url(#purpleSpark)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <span className="text-xs text-emerald-600 flex items-center gap-1 font-semibold">
            <ArrowUpRight className="w-3 h-3" /> 15.7% <span className="text-slate-400 font-medium">vs last month</span>
          </span>
        </div>

        {/* Metric 4 - Conversion Rate */}
        <div className="bg-white border border-slate-200/80 p-6 rounded-2xl shadow-[0_4px_20px_rgba(0,0,0,0.015)] hover:shadow-[0_8px_30px_rgba(0,0,0,0.03)] transition-all flex flex-col">
          <div className="flex justify-between items-start mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider font-display">Conversion Rate</span>
          </div>
          <div className="flex items-center justify-between mb-4">
            <span className="text-3xl font-bold font-display text-slate-800 tracking-tight">24.6%</span>
            <div className="p-2 bg-indigo-50 rounded-full">
              <Target className="w-4 h-4 text-[#6366f1]" />
            </div>
          </div>
          <div className="h-[40px] w-full mb-3">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={rateSparkline} margin={{ top: 2, bottom: 2, left: 2, right: 2 }}>
                <defs>
                  <linearGradient id="indigoSpark" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#6366f1" stopOpacity={0.15} />
                    <stop offset="100%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <Area type="monotone" dataKey="v" stroke="#6366f1" strokeWidth={1.5} fill="url(#indigoSpark)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <span className="text-xs text-emerald-600 flex items-center gap-1 font-semibold">
            <ArrowUpRight className="w-3 h-3" /> 6.4% <span className="text-slate-400 font-medium">vs last month</span>
          </span>
        </div>
      </div>

      {/* Lead Pipeline Chevron Diagram */}
      <div className="bg-white border border-slate-200/80 p-6 rounded-2xl shadow-[0_4px_20px_rgba(0,0,0,0.015)]">
        <h3 className="text-sm font-semibold font-display text-slate-800 uppercase tracking-wider mb-6">Lead Pipeline</h3>
        
        <div className="flex flex-col lg:flex-row items-center gap-3">
          {/* Step 1: Raw Leads */}
          <div className="w-full flex-1 relative bg-blue-50/50 border border-blue-100/50 rounded-xl p-5 flex flex-col items-center justify-center transition-all hover:bg-blue-50">
            <span className="text-xs font-semibold text-blue-500 uppercase tracking-wider font-display mb-1">Raw Leads</span>
            <span className="text-2xl font-bold text-slate-800 font-display mb-3">1,248</span>
            <div className="p-2 bg-blue-500/10 rounded-full text-blue-500">
              <Users className="w-4 h-4" />
            </div>
          </div>

          <ChevronRight className="w-5 h-5 text-slate-300 hidden lg:block shrink-0" />

          {/* Step 2: Qualified */}
          <div className="w-full flex-1 relative bg-emerald-50/50 border border-emerald-100/50 rounded-xl p-5 flex flex-col items-center justify-center transition-all hover:bg-emerald-50">
            <span className="text-xs font-semibold text-emerald-600 uppercase tracking-wider font-display mb-1">Qualified</span>
            <span className="text-2xl font-bold text-slate-800 font-display mb-3">312</span>
            <div className="p-2 bg-emerald-500/10 rounded-full text-emerald-500">
              <CheckCircle2 className="w-4 h-4" />
            </div>
          </div>

          <ChevronRight className="w-5 h-5 text-slate-300 hidden lg:block shrink-0" />

          {/* Step 3: Engaged */}
          <div className="w-full flex-1 relative bg-purple-50/50 border border-purple-100/50 rounded-xl p-5 flex flex-col items-center justify-center transition-all hover:bg-purple-50">
            <span className="text-xs font-semibold text-purple-600 uppercase tracking-wider font-display mb-1">Engaged</span>
            <span className="text-2xl font-bold text-slate-800 font-display mb-3">128</span>
            <div className="p-2 bg-purple-500/10 rounded-full text-purple-500">
              <MessageCircle className="w-4 h-4" />
            </div>
          </div>

          <ChevronRight className="w-5 h-5 text-slate-300 hidden lg:block shrink-0" />

          {/* Step 4: Converted */}
          <div className="w-full flex-1 relative bg-teal-50/50 border border-teal-100/50 rounded-xl p-5 flex flex-col items-center justify-center transition-all hover:bg-teal-50">
            <span className="text-xs font-semibold text-teal-600 uppercase tracking-wider font-display mb-1">Converted</span>
            <span className="text-2xl font-bold text-slate-800 font-display mb-3">78</span>
            <div className="p-2 bg-teal-500/10 rounded-full text-teal-500">
              <Star className="w-4 h-4 fill-current" />
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Grid: Activity, Channels, AI Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Activity */}
        <div className="bg-white border border-slate-200/80 p-6 rounded-2xl shadow-[0_4px_20px_rgba(0,0,0,0.015)] flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-semibold font-display text-slate-800 uppercase tracking-wider mb-6">Recent Activity</h3>
            <div className="space-y-6">
              <div className="flex gap-4 items-start">
                <div className="w-8 h-8 rounded-full bg-blue-50 text-[#3B82F6] flex items-center justify-center shrink-0">
                  <Send className="w-3.5 h-3.5" />
                </div>
                <div>
                  <p className="text-xs font-semibold text-slate-800">AI outreach sent to 45 new leads</p>
                  <span className="text-[10px] text-slate-400 mt-1 block">2 min ago</span>
                </div>
              </div>

              <div className="flex gap-4 items-start">
                <div className="w-8 h-8 rounded-full bg-emerald-50 text-[#10B981] flex items-center justify-center shrink-0">
                  <Check className="w-3.5 h-3.5" strokeWidth={3} />
                </div>
                <div>
                  <p className="text-xs font-semibold text-slate-800">12 leads qualified automatically</p>
                  <span className="text-[10px] text-slate-400 mt-1 block">15 min ago</span>
                </div>
              </div>

              <div className="flex gap-4 items-start">
                <div className="w-8 h-8 rounded-full bg-purple-50 text-[#8B5CF6] flex items-center justify-center shrink-0">
                  <MessageCircle className="w-3.5 h-3.5" />
                </div>
                <div>
                  <p className="text-xs font-semibold text-slate-800">3 new conversations started</p>
                  <span className="text-[10px] text-slate-400 mt-1 block">1 hour ago</span>
                </div>
              </div>

              <div className="flex gap-4 items-start">
                <div className="w-8 h-8 rounded-full bg-amber-50 text-amber-500 flex items-center justify-center shrink-0">
                  <Star className="w-3.5 h-3.5" />
                </div>
                <div>
                  <p className="text-xs font-semibold text-slate-800">New deal added: BrightFuture Inc.</p>
                  <span className="text-[10px] text-slate-400 mt-1 block">2 hours ago</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-8 pt-4 border-t border-slate-100">
            <button className="text-xs font-semibold text-[#6366f1] hover:text-[#4f46e5] transition-colors flex items-center gap-1.5">
              <span>View all activity</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Top Channels Donut Chart */}
        <div className="bg-white border border-slate-200/80 p-6 rounded-2xl shadow-[0_4px_20px_rgba(0,0,0,0.015)] flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-semibold font-display text-slate-800 uppercase tracking-wider mb-6">Top Channels</h3>
            
            <div className="flex items-center gap-4 py-3">
              {/* Donut Canvas */}
              <div className="relative w-[150px] h-[150px] shrink-0">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={channelsData}
                      cx="50%"
                      cy="50%"
                      innerRadius={50}
                      outerRadius={70}
                      paddingAngle={2}
                      dataKey="value"
                    >
                      {channelsData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
                {/* Center Labels */}
                <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                  <span className="text-2xl font-bold font-display text-slate-800 leading-none">1,248</span>
                  <span className="text-[9px] text-slate-400 font-semibold uppercase tracking-wider mt-1">Total Leads</span>
                </div>
              </div>

              {/* Legends list */}
              <div className="flex-1 space-y-2 text-xs">
                {channelsData.map((chan) => (
                  <div key={chan.name} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="w-2.5 h-2.5 rounded shrink-0" style={{ backgroundColor: chan.color }}></span>
                      <span className="text-slate-500 font-medium">{chan.name}</span>
                    </div>
                    <span className="font-bold text-slate-700 font-display">{chan.value}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="mt-8 pt-4 border-t border-slate-100">
            <button className="text-xs font-semibold text-[#6366f1] hover:text-[#4f46e5] transition-colors flex items-center gap-1.5">
              <span>View full report</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* AI Insight Card */}
        <div className="bg-white border border-slate-200/80 p-6 rounded-2xl shadow-[0_4px_20px_rgba(0,0,0,0.015)] flex flex-col justify-between overflow-hidden relative">
          <div>
            <div className="flex items-center gap-3 mb-6">
              <div className="w-8 h-8 rounded-full bg-indigo-50 text-[#6366f1] flex items-center justify-center">
                <Sparkles className="w-4 h-4 fill-current" />
              </div>
              <h3 className="text-sm font-semibold font-display text-slate-800 uppercase tracking-wider">AI Insight</h3>
            </div>
            
            <p className="text-sm text-slate-500 leading-relaxed font-sans pr-2">
              Your conversion rate is up <strong className="text-slate-700">18%</strong> this month. <br />
              Keep engaging! 🚀
            </p>
          </div>

          {/* Bottom Graph with floating badge */}
          <div className="relative mt-8 pt-4">
            {/* Green bubble +18% */}
            <div className="absolute top-0 right-4 z-10 bg-emerald-50 text-emerald-600 border border-emerald-100 px-2 py-0.5 rounded-full text-[10px] font-bold shadow-sm flex items-center gap-0.5">
              <span>+18%</span>
            </div>

            <div className="h-[90px] w-full translate-y-3">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={insightSparkline} margin={{ top: 10, bottom: 2, left: 2, right: 2 }}>
                  <defs>
                    <linearGradient id="insightGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#3B82F6" stopOpacity={0.15} />
                      <stop offset="100%" stopColor="#3B82F6" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <Area type="monotone" dataKey="v" stroke="#3B82F6" strokeWidth={2} fill="url(#insightGrad)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
