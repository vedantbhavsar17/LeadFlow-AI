"use client";

import { useState } from "react";
import { ArrowLeft, ArrowRight, Trophy } from "lucide-react";

interface PipelineCard {
  id: string;
  name: string;
  desc: string;
  score: number;
  stage: "NEW" | "QUALIFIED" | "PITCHED" | "REPLIED" | "MEETING_NEEDED" | "WON";
  status: "HOT" | "WARM" | "COLD";
}

const INITIAL_CARDS: PipelineCard[] = [
  {
    id: "1",
    name: "TechCorp",
    desc: "Inbound WebForm",
    score: 32,
    stage: "NEW",
    status: "COLD",
  },
  {
    id: "2",
    name: "Delta Inc",
    desc: "CSV Import Pipeline",
    score: 58,
    stage: "NEW",
    status: "WARM",
  },
  {
    id: "3",
    name: "Alpha Media",
    desc: "SaaS Dev Agency",
    score: 88,
    stage: "QUALIFIED",
    status: "HOT",
  },
  {
    id: "4",
    name: "Nova Studio",
    desc: "Outbound Sent Email",
    score: 90,
    stage: "PITCHED",
    status: "HOT",
  },
  {
    id: "5",
    name: "Scale Digital",
    desc: "Diagnostic Pain Pitch",
    score: 76,
    stage: "PITCHED",
    status: "WARM",
  },
  {
    id: "6",
    name: "Acme Corp",
    desc: "Interested (Reply Q3)",
    score: 91,
    stage: "REPLIED",
    status: "HOT",
  },
  {
    id: "7",
    name: "Zeta Logistics",
    desc: "Calendar Invite Sent",
    score: 94,
    stage: "MEETING_NEEDED",
    status: "HOT",
  },
  {
    id: "8",
    name: "Vortex Co",
    desc: "Contract Signed",
    score: 99,
    stage: "WON",
    status: "HOT",
  },
];

const COLUMNS = [
  { stage: "NEW", label: "New Leads", color: "bg-indigo-500/5 text-indigo-700 border-indigo-200" },
  { stage: "QUALIFIED", label: "Qualified", color: "bg-emerald-500/5 text-emerald-700 border-emerald-200" },
  { stage: "PITCHED", label: "Pitched", color: "bg-amber-500/5 text-amber-700 border-amber-200" },
  { stage: "REPLIED", label: "Replied", color: "bg-purple-500/5 text-purple-700 border-purple-200" },
  { stage: "MEETING_NEEDED", label: "Meeting Needed", color: "bg-rose-500/5 text-rose-700 border-rose-200" },
  { stage: "WON", label: "Won", color: "bg-sky-500/10 text-sky-700 border-sky-200" },
] as const;

export default function PipelinePage() {
  const [cards, setCards] = useState<PipelineCard[]>(INITIAL_CARDS);

  const moveCard = (id: string, direction: "prev" | "next") => {
    const stages: PipelineCard["stage"][] = [
      "NEW",
      "QUALIFIED",
      "PITCHED",
      "REPLIED",
      "MEETING_NEEDED",
      "WON",
    ];

    setCards((prev) =>
      prev.map((card) => {
        if (card.id !== id) return card;
        const currentIdx = stages.indexOf(card.stage);
        let nextIdx = currentIdx;

        if (direction === "next" && currentIdx < stages.length - 1) {
          nextIdx++;
        } else if (direction === "prev" && currentIdx > 0) {
          nextIdx--;
        }

        return { ...card, stage: stages[nextIdx] };
      })
    );
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto h-[calc(100vh-10rem)] flex flex-col">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold font-display text-slate-800 tracking-tight">Interactive CRM Sales Pipeline</h1>
        <p className="text-sm text-slate-500 mt-1">Move qualified deals along the sales funnel stages manually using card control nodes.</p>
      </div>

      {/* Board Scrollable Container */}
      <div className="flex-1 overflow-x-auto pb-4 flex gap-4 items-start select-none">
        {COLUMNS.map((col) => {
          const colCards = cards.filter((card) => card.stage === col.stage);
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
                {colCards.map((card) => (
                  <div
                    key={card.id}
                    className={`border p-4 rounded-xl shadow-[0_2px_8px_rgba(0,0,0,0.01)] relative transition-all duration-200 hover:shadow-[0_4px_12px_rgba(0,0,0,0.03)] bg-white ${col.color}`}
                  >
                    <div className="flex justify-between items-start gap-2">
                      <h4 className="text-xs font-bold text-slate-800 leading-snug font-display">{card.name}</h4>
                      <span
                        className={`text-[9px] font-bold px-1.5 py-0.5 rounded border leading-none shrink-0 ${
                          card.status === "HOT"
                            ? "bg-emerald-500/10 text-emerald-600 border-emerald-500/20"
                            : card.status === "WARM"
                            ? "bg-blue-500/10 text-blue-500 border-blue-500/20"
                            : "bg-slate-500/10 text-slate-500 border-slate-500/20"
                        }`}
                      >
                        {card.score}
                      </span>
                    </div>
                    <p className="text-[10px] text-slate-500 mt-2 font-sans">{card.desc}</p>

                    {/* Progress indicators inside cards */}
                    <div className="mt-4 pt-3 border-t border-slate-100 flex justify-between items-center gap-2">
                      <button
                        onClick={() => moveCard(card.id, "prev")}
                        disabled={card.stage === "NEW"}
                        className="text-slate-400 hover:text-slate-800 disabled:opacity-20 p-1 hover:bg-slate-100 rounded transition-colors"
                      >
                        <ArrowLeft className="w-3.5 h-3.5" />
                      </button>

                      <div className="flex items-center gap-1">
                        {card.stage === "WON" ? (
                          <span className="text-[10px] text-emerald-600 font-bold tracking-wider flex items-center gap-1 uppercase font-display">
                            <Trophy className="w-3 h-3 text-[#10b981]" /> Won
                          </span>
                        ) : (
                          <span className="text-[9px] text-slate-400 uppercase tracking-widest font-semibold font-display">
                            Move Deal
                          </span>
                        )}
                      </div>

                      <button
                        onClick={() => moveCard(card.id, "next")}
                        disabled={card.stage === "WON"}
                        className="text-slate-400 hover:text-slate-800 disabled:opacity-20 p-1 hover:bg-slate-100 rounded transition-colors"
                      >
                        <ArrowRight className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                ))}

                {colCards.length === 0 && (
                  <div className="border-2 border-dashed border-slate-200 rounded-xl py-8 flex flex-col items-center justify-center text-center text-slate-400 text-[10px] bg-slate-50/20">
                    <span>Drag/Drop or Move</span>
                    <span>Deals here</span>
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
