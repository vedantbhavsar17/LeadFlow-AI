"use client";

import { useLeads } from "@/lib/lead-context";
import { Lead } from "@/services/api-client";
import { ArrowLeft, ArrowRight, Trophy, Sparkles } from "lucide-react";
import { useRouter } from "next/navigation";

const COLUMNS = [
  { stage: "new", label: "New Leads", color: "bg-indigo-500/5 text-indigo-700 border-indigo-200" },
  { stage: "qualified", label: "Qualified", color: "bg-blue-500/5 text-blue-700 border-blue-200" },
  { stage: "outreach_sent", label: "Outreach Sent", color: "bg-amber-500/5 text-amber-700 border-amber-200" },
  { stage: "customer_replied", label: "Customer Replied", color: "bg-purple-500/5 text-purple-700 border-purple-200" },
  { stage: "followup_scheduled", label: "Followup Scheduled", color: "bg-rose-500/5 text-rose-700 border-rose-200" },
  { stage: "converted", label: "Converted", color: "bg-emerald-500/10 text-emerald-700 border-emerald-200" },
] as const;

export default function PipelinePage() {
  const { leads, updateLeadStage } = useLeads();
  const router = useRouter();

  const moveCard = (id: number, direction: "prev" | "next") => {
    const stages = [
      "new",
      "qualified",
      "outreach_sent",
      "customer_replied",
      "followup_scheduled",
      "converted",
    ];

    const lead = leads.find((l) => l.id === id);
    if (!lead) return;

    const currentIdx = stages.indexOf(lead.stage);
    let nextIdx = currentIdx;

    if (direction === "next" && currentIdx < stages.length - 1) {
      nextIdx++;
    } else if (direction === "prev" && currentIdx > 0) {
      nextIdx--;
    }

    if (nextIdx !== currentIdx) {
      updateLeadStage(id, stages[nextIdx]);
    }
  };

  const getLeadScore = (lead: any) => {
    if (lead.id === 999) return lead.stage === "new" ? 72 : 94;
    return (lead.id % 20) * 3 + 40;
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto h-[calc(100vh-10rem)] flex flex-col font-sans">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold font-display text-slate-800 tracking-tight">Interactive CRM Sales Pipeline</h1>
        <p className="text-sm text-slate-500 mt-1">Move qualified deals along the sales funnel stages manually using card controls.</p>
      </div>

      {/* Board Scrollable Container */}
      <div className="flex-1 overflow-x-auto pb-4 flex gap-4 items-start select-none">
        {COLUMNS.map((col) => {
          const colCards = leads.filter((lead) => lead.stage === col.stage);
          return (
            <div
              key={col.stage}
              className="w-72 shrink-0 bg-white border border-slate-200/80 p-4 rounded-2xl flex flex-col max-h-full shadow-sm"
            >
              {/* Column Header */}
              <div className="flex justify-between items-center mb-4 pb-2 border-b border-slate-100 shrink-0">
                <span className="text-xs font-bold text-slate-800 uppercase tracking-wider font-display">{col.label}</span>
                <span className="text-[10px] bg-slate-100 border border-slate-200 px-2.5 py-0.5 rounded-full font-bold text-slate-500">
                  {colCards.length}
                </span>
              </div>

              {/* Cards List */}
              <div className="space-y-3 overflow-y-auto flex-1 pr-1">
                {colCards.map((card) => {
                  const score = getLeadScore(card);
                  return (
                    <div
                      key={card.id}
                      className={`border p-4 rounded-xl shadow-[0_2px_8px_rgba(0,0,0,0.01)] relative transition-all duration-200 hover:shadow-[0_4px_12px_rgba(0,0,0,0.03)] bg-white ${col.color}`}
                    >
                      <div className="flex justify-between items-start gap-2">
                        <h4 
                          onClick={() => router.push(`/leads/${card.id}`)}
                          className="text-xs font-bold text-slate-800 leading-snug font-display hover:text-[#6366f1] cursor-pointer transition-colors"
                        >
                          {card.company}
                        </h4>
                        <span
                          className={`text-[9px] font-bold px-1.5 py-0.5 rounded border leading-none shrink-0 ${
                            card.status === "HOT"
                              ? "bg-emerald-500/10 text-emerald-600 border-emerald-500/20"
                              : card.status === "WARM"
                              ? "bg-blue-500/10 text-blue-500 border-blue-500/20"
                              : "bg-slate-500/10 text-slate-500 border-slate-500/20"
                          }`}
                        >
                          {score}
                        </span>
                      </div>
                      <p className="text-[10px] text-slate-500 mt-2 font-sans">
                        {card.first_name} {card.last_name} | {card.industry}
                      </p>

                      {/* Progress indicators inside cards */}
                      <div className="mt-4 pt-3 border-t border-slate-100 flex justify-between items-center gap-2">
                        <button
                          onClick={() => moveCard(card.id, "prev")}
                          disabled={card.stage === "new"}
                          className="text-slate-400 hover:text-slate-800 disabled:opacity-20 p-1 hover:bg-slate-100 rounded transition-colors"
                        >
                          <ArrowLeft className="w-3.5 h-3.5" />
                        </button>

                        <div className="flex items-center gap-1">
                          {card.stage === "converted" ? (
                            <span className="text-[10px] text-emerald-600 font-bold tracking-wider flex items-center gap-1 uppercase font-display">
                              <Trophy className="w-3 h-3 text-[#10b981]" /> Won
                            </span>
                          ) : (
                            <span className="text-[9px] text-slate-400 uppercase tracking-widest font-semibold font-display">
                              Move Stage
                            </span>
                          )}
                        </div>

                        <button
                          onClick={() => moveCard(card.id, "next")}
                          disabled={card.stage === "converted"}
                          className="text-slate-400 hover:text-slate-800 disabled:opacity-20 p-1 hover:bg-slate-100 rounded transition-colors"
                        >
                          <ArrowRight className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  );
                })}

                {colCards.length === 0 && (
                  <div className="border-2 border-dashed border-slate-200 rounded-xl py-8 flex flex-col items-center justify-center text-center text-slate-400 text-[10px] bg-slate-50/20">
                    <span>No leads in</span>
                    <span>this stage</span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
