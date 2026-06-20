"use client";

import { useState } from "react";
import { Search, FileUp, Filter, Check, MoreVertical, Sparkles, ChevronRight } from "lucide-react";
import { useLeads } from "@/lib/lead-context";
import { useRouter } from "next/navigation";
import { ApiClient, Lead } from "@/services/api-client";

export default function LeadsPage() {
  const { leads, addLead, isBackendOnline, refreshData } = useLeads();
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState<"ALL" | "HOT" | "WARM" | "COLD">("ALL");
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [csvContent, setCsvContent] = useState("");
  const [importing, setImporting] = useState(false);
  const router = useRouter();

  const handleUploadMock = async () => {
    setImporting(true);
    
    // If user provided custom CSV content, let's import it
    if (csvContent.trim()) {
      if (isBackendOnline) {
        try {
          await ApiClient.importCsvLeads(csvContent);
          await refreshData();
          setUploadSuccess(true);
        } catch (err) {
          console.error(err);
          alert("Failed to parse CSV. Make sure headers contain name, email, company.");
        }
      } else {
        // Fallback manual parser
        const lines = csvContent.split("\n");
        let added = 0;
        for (let i = 1; i < lines.length; i++) {
          const cols = lines[i].split(",");
          if (cols.length >= 2) {
            const name = cols[0]?.trim();
            const email = cols[1]?.trim();
            const company = cols[2]?.trim() || "";
            const industry = cols[3]?.trim() || "SaaS";
            if (name && email) {
              const names = name.split(" ");
              await addLead({
                first_name: names[0] || "Imported",
                last_name: names.slice(1).join(" ") || "Prospect",
                email,
                company,
                industry,
                source: "CSV Import",
                stage: "new",
                status: "WARM",
                priority: "normal"
              });
              added++;
            }
          }
        }
        if (added > 0) {
          setUploadSuccess(true);
        } else {
          alert("Could not extract leads. Format: name,email,company,industry");
        }
      }
    } else {
      // Default sample ingest
      await addLead({
        first_name: "Marcus",
        last_name: "Aurelius",
        email: "marcus@romantech.com",
        phone: "+1-555-0955",
        company: "Roman Tech",
        industry: "Enterprise SaaS",
        source: "CSV Import",
        stage: "qualified",
        status: "HOT",
        priority: "high",
        notes: "Missing secure TLS certificate, outdated SSL. High budget."
      });
      await addLead({
        first_name: "Lucius",
        last_name: "Seneca",
        email: "seneca@stoic.edu",
        phone: "+1-555-0966",
        company: "Stoic Consulting",
        industry: "E-Learning",
        source: "CSV Import",
        stage: "new",
        status: "WARM",
        priority: "normal",
        notes: "Failed core web vitals performance scores."
      });
      setUploadSuccess(true);
    }

    setImporting(false);
    setTimeout(() => {
      setShowUploadModal(false);
      setUploadSuccess(false);
      setCsvContent("");
    }, 1500);
  };

  const filteredLeads = leads.filter((lead) => {
    const fullName = `${lead.first_name} ${lead.last_name}`.toLowerCase();
    const matchesSearch =
      fullName.includes(search.toLowerCase()) ||
      lead.company.toLowerCase().includes(search.toLowerCase()) ||
      (lead.industry || "").toLowerCase().includes(search.toLowerCase());
    const matchesFilter = filter === "ALL" || lead.status === filter;
    return matchesSearch && matchesFilter;
  });

  const getStagePercentage = (stage: string) => {
    switch (stage) {
      case "new": return 16.6;
      case "qualified": return 33.3;
      case "outreach_sent": return 50;
      case "customer_replied": return 66.6;
      case "followup_scheduled": return 83.3;
      case "converted": return 100;
      default: return 10;
    }
  };

  const getStageColor = (stage: string) => {
    switch (stage) {
      case "new": return "bg-slate-400";
      case "qualified": return "bg-blue-500";
      case "outreach_sent": return "bg-indigo-500";
      case "customer_replied": return "bg-purple-500";
      case "followup_scheduled": return "bg-amber-500";
      case "converted": return "bg-emerald-500";
      default: return "bg-slate-400";
    }
  };

  const getStageLabel = (stage: string) => {
    return stage.replace("_", " ").toUpperCase();
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-xl font-bold font-display text-slate-800 tracking-tight">Lead Ingestion &amp; Repository</h1>
          <p className="text-sm text-slate-500 mt-1">Review prospect profiles, diagnostic scoring, and active engagement stages.</p>
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
                <th className="px-6 py-4 font-display">Industry</th>
                <th className="px-6 py-4 font-display">Stage &amp; Progress</th>
                <th className="px-6 py-4 font-display">Status</th>
                <th className="px-6 py-4 text-right font-display">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-sm text-slate-600 font-sans">
              {filteredLeads.map((lead) => (
                <tr 
                  key={lead.id} 
                  onClick={() => router.push(`/leads/${lead.id}`)}
                  className="hover:bg-slate-50/50 cursor-pointer transition-colors group"
                >
                  <td className="px-6 py-4">
                    <div className="flex flex-col">
                      <span className="font-semibold text-slate-800 group-hover:text-[#6366f1] transition-colors">
                        {lead.company}
                      </span>
                      <span className="text-xs text-slate-400 mt-0.5">{lead.first_name} {lead.last_name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex flex-col">
                      <span>{lead.industry}</span>
                      <span className="text-xs text-slate-400 mt-0.5">{lead.email}</span>
                    </div>
                  </td>
                  {/* Lead Status Progress Bar */}
                  <td className="px-6 py-4">
                    <div className="flex flex-col w-56 space-y-1.5">
                      <div className="flex justify-between items-center text-[10px]">
                        <span className="font-bold text-slate-500">{getStageLabel(lead.stage)}</span>
                        <span className="font-semibold text-slate-400">{Math.round(getStagePercentage(lead.stage))}%</span>
                      </div>
                      <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden border border-slate-200/50">
                        <div 
                          className={`h-full rounded-full transition-all duration-500 ${getStageColor(lead.stage)}`}
                          style={{ width: `${getStagePercentage(lead.stage)}%` }}
                        ></div>
                      </div>
                    </div>
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
                  <td className="px-6 py-4 text-right" onClick={(e) => e.stopPropagation()}>
                    <button 
                      onClick={() => router.push(`/leads/${lead.id}`)}
                      className="text-slate-400 hover:text-slate-800 p-1.5 rounded-lg hover:bg-slate-100 transition-colors flex items-center gap-1 text-xs font-semibold ml-auto"
                    >
                      <span>View details</span>
                      <ChevronRight className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              ))}
              {filteredLeads.length === 0 && (
                <tr>
                  <td colSpan={5} className="text-center py-12 text-slate-400 text-xs">
                    No matching prospects found in database.
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
            className="bg-white border border-slate-200 max-w-lg w-full rounded-2xl p-6 shadow-2xl space-y-6"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-base font-bold text-slate-800 flex items-center gap-2 font-display">
                  <FileUp className="w-5 h-5 text-[#6366f1]" /> Import Prospect CSV Registry
                </h3>
                <p className="text-xs text-slate-500 mt-1">
                  Upload spreadsheet or paste CSV rows below to run diagnostic intelligence on new leads.
                </p>
              </div>
              <button
                className="text-slate-400 hover:text-slate-800 text-lg font-bold"
                onClick={() => setShowUploadModal(false)}
              >
                &times;
              </button>
            </div>

            <div className="space-y-3">
              <label className="text-xs font-semibold text-slate-500">Paste CSV Content (Format: name,email,company,industry)</label>
              <textarea
                placeholder="Marcus Aurelius,marcus@romantech.com,Roman Tech,Software
Lucius Seneca,seneca@stoic.edu,Stoic Consulting,Education"
                value={csvContent}
                onChange={(e) => setCsvContent(e.target.value)}
                rows={4}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-mono focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
              />
              <span className="text-[10px] text-slate-400 block">Leave textarea empty to import default sample prospects.</span>
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
                disabled={importing}
                className="px-4 py-2 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-[0_4px_12px_rgba(99,102,241,0.25)] font-display"
              >
                {uploadSuccess ? (
                  <>
                    <Check className="w-3.5 h-3.5" /> Imported!
                  </>
                ) : (
                  <>
                    <Sparkles className="w-3.5 h-3.5" /> {importing ? "Processing..." : "Start AI Diagnostics"}
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
