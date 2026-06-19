"use client";

import { useState } from "react";
import { Search, FileUp, Filter, Check, MoreVertical, Plus, Sparkles } from "lucide-react";

interface Lead {
  id: string;
  name: string;
  company: string;
  industry: string;
  revenue: string;
  score: number;
  status: "HOT" | "WARM" | "COLD";
  diagnosedPain: string;
}

const INITIAL_LEADS: Lead[] = [
  {
    id: "1",
    name: "John Doe",
    company: "Acme Corp",
    industry: "SaaS Agency",
    revenue: "$10M",
    score: 91,
    status: "HOT",
    diagnosedPain: "Website speed 6.4s, no capture mechanism",
  },
  {
    id: "2",
    name: "Jane Smith",
    company: "Apex Global",
    industry: "E-Commerce",
    revenue: "$2.5M",
    score: 74,
    status: "WARM",
    diagnosedPain: "SEO canonical errors, poor page indexing",
  },
  {
    id: "3",
    name: "Robert Johnson",
    company: "Local Bistro",
    industry: "Restaurant",
    revenue: "$200k",
    score: 35,
    status: "COLD",
    diagnosedPain: "Missing mobile menu responsiveness",
  },
  {
    id: "4",
    name: "Alice Williams",
    company: "Delta Logistics",
    industry: "Logistics",
    revenue: "$15M",
    score: 88,
    status: "HOT",
    diagnosedPain: "Slow form submission response latency",
  },
  {
    id: "5",
    name: "Charlie Brown",
    company: "Nova Studios",
    industry: "Marketing",
    revenue: "$1.2M",
    score: 58,
    status: "WARM",
    diagnosedPain: "Missing social meta tags configuration",
  },
];

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>(INITIAL_LEADS);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState<"ALL" | "HOT" | "WARM" | "COLD">("ALL");
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);

  const handleUploadMock = () => {
    const newLeads: Lead[] = [
      {
        id: (leads.length + 1).toString(),
        name: "Marcus Aurelius",
        company: "Roman Tech",
        industry: "Enterprise SaaS",
        revenue: "$40M",
        score: 95,
        status: "HOT",
        diagnosedPain: "Missing secure TLS certificate, outdated SSL",
      },
      {
        id: (leads.length + 2).toString(),
        name: "Seneca",
        company: "Stoic Consulting",
        industry: "E-Learning",
        revenue: "$500k",
        score: 62,
        status: "WARM",
        diagnosedPain: "Failed core web vitals performance scores",
      },
    ];

    setLeads((prev) => [...newLeads, ...prev]);
    setUploadSuccess(true);
    setTimeout(() => {
      setShowUploadModal(false);
      setUploadSuccess(false);
    }, 1500);
  };

  const filteredLeads = leads.filter((lead) => {
    const matchesSearch =
      lead.name.toLowerCase().includes(search.toLowerCase()) ||
      lead.company.toLowerCase().includes(search.toLowerCase()) ||
      lead.industry.toLowerCase().includes(search.toLowerCase());
    const matchesFilter = filter === "ALL" || lead.status === filter;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-xl font-bold font-display text-slate-800 tracking-tight">Lead Ingestion &amp; Repository</h1>
          <p className="text-sm text-slate-500 mt-1">Review raw prospect matrices and automated diagnostic results.</p>
        </div>

        <div className="flex gap-3">
          <button
            onClick={() => setShowUploadModal(true)}
            className="flex items-center gap-2 px-4 py-2.5 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] hover:brightness-105 text-white rounded-lg text-sm font-medium transition-all shadow-[0_4px_12px_rgba(99,102,241,0.2)] font-display"
          >
            <FileUp className="w-4 h-4" />
            <span>Upload CSV</span>
          </button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row justify-between gap-4 bg-white border border-slate-200/80 p-4 rounded-xl shadow-sm">
        <div className="relative flex-1">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search prospect name, company, or industry..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-sans"
          />
        </div>

        <div className="flex items-center gap-2 overflow-x-auto">
          <Filter className="w-4 h-4 text-slate-400 shrink-0" />
          <span className="text-xs font-semibold text-slate-500 mr-2 shrink-0 font-display">Filter Status:</span>
          {(["ALL", "HOT", "WARM", "COLD"] as const).map((opt) => (
            <button
              key={opt}
              onClick={() => setFilter(opt)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                filter === opt
                  ? "bg-indigo-50 text-[#6366f1] border-indigo-200"
                  : "bg-transparent text-slate-500 border-slate-200 hover:text-slate-800 hover:bg-slate-50"
              }`}
            >
              {opt}
            </button>
          ))}
        </div>
      </div>

      {/* Leads Table */}
      <div className="bg-white border border-slate-200/80 rounded-2xl shadow-[0_4px_20px_rgba(0,0,0,0.02)] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 text-slate-400 text-xs font-semibold uppercase tracking-wider bg-slate-50/50">
                <th className="px-6 py-4 font-display">Prospect</th>
                <th className="px-6 py-4 font-display">Industry / Rev</th>
                <th className="px-6 py-4 font-display">Score</th>
                <th className="px-6 py-4 font-display">Diagnosed Pain Point</th>
                <th className="px-6 py-4 font-display">Status</th>
                <th className="px-6 py-4 text-right font-display">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-sm text-slate-600 font-sans">
              {filteredLeads.map((lead) => (
                <tr key={lead.id} className="hover:bg-slate-50/50 transition-colors">
                  <td className="px-6 py-4">
                    <div className="flex flex-col">
                      <span className="font-semibold text-slate-800">{lead.company}</span>
                      <span className="text-xs text-slate-400 mt-0.5">{lead.name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex flex-col">
                      <span>{lead.industry}</span>
                      <span className="text-xs text-slate-400 mt-0.5">Est. Rev: {lead.revenue}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 rounded-lg bg-[#faf8ff] border border-slate-200 flex items-center justify-center text-xs font-bold text-slate-700 font-display">
                        {lead.score}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-xs bg-rose-50 text-rose-700 border border-rose-100 px-2.5 py-1.5 rounded-lg inline-block font-sans">
                      {lead.diagnosedPain}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`text-[10px] font-bold px-2.5 py-1 rounded-full border leading-none inline-flex items-center uppercase ${
                        lead.status === "HOT"
                          ? "bg-[#10b981]/10 text-[#10b981] border-[#10b981]/20"
                          : lead.status === "WARM"
                          ? "bg-blue-500/10 text-blue-500 border-blue-500/20"
                          : "bg-slate-500/10 text-slate-500 border-slate-500/20"
                      }`}
                    >
                      {lead.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-slate-400 hover:text-slate-800 p-1 rounded hover:bg-slate-100 transition-colors">
                      <MoreVertical className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
              {filteredLeads.length === 0 && (
                <tr>
                  <td colSpan={6} className="text-center py-8 text-slate-400 text-xs">
                    No matching prospects found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Upload CSV Modal Simulation */}
      {showUploadModal && (
        <div
          className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={() => setShowUploadModal(false)}
        >
          <div
            className="bg-white border border-slate-200 max-w-md w-full rounded-2xl p-6 shadow-2xl space-y-6"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-base font-bold text-slate-800 flex items-center gap-2 font-display">
                  <FileUp className="w-5 h-5 text-[#6366f1]" /> Import Prospect CSV Registry
                </h3>
                <p className="text-xs text-slate-500 mt-1">
                  Upload spreadsheet files to run automated AI diagnostics and scoring.
                </p>
              </div>
              <button
                className="text-slate-400 hover:text-slate-800 text-lg font-bold"
                onClick={() => setShowUploadModal(false)}
              >
                &times;
              </button>
            </div>

            <div className="border-2 border-dashed border-slate-200 rounded-xl p-8 flex flex-col items-center justify-center bg-slate-50/50 cursor-pointer hover:bg-slate-50 hover:border-[#6366f1]/30 transition-all">
              <FileUp className="w-8 h-8 text-slate-400 animate-bounce mb-3" />
              <span className="text-xs font-semibold text-slate-800">Select leads_export.csv</span>
              <span className="text-[10px] text-slate-500 mt-1">Supports standard CSV sheets up to 10MB</span>
            </div>

            <div className="flex gap-3 justify-end pt-2">
              <button
                onClick={() => setShowUploadModal(false)}
                className="px-4 py-2 border border-slate-200 rounded-lg text-xs font-semibold text-slate-500 hover:bg-slate-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleUploadMock}
                className="px-4 py-2 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-[0_4px_12px_rgba(99,102,241,0.25)] font-display"
              >
                {uploadSuccess ? (
                  <>
                    <Check className="w-3.5 h-3.5" /> Imported!
                  </>
                ) : (
                  <>
                    <Sparkles className="w-3.5 h-3.5" /> Start AI Diagnostics
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
