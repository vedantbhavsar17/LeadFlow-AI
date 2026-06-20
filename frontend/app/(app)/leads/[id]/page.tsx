"use client";

import { use, useState } from "react";
import { 
  ArrowLeft, 
  Sparkles, 
  Send, 
  Check, 
  Calendar, 
  Plus, 
  AlertTriangle, 
  TrendingUp, 
  UserCheck, 
  Clock, 
  MessageSquare,
  BadgeAlert,
  HelpCircle,
  Play
} from "lucide-react";
import { useLeads, Message, Followup } from "@/lib/lead-context";
import { Lead, LeadActivity } from "@/services/api-client";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function LeadDetailsPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const leadId = parseInt(id);
  const router = useRouter();
  
  const { 
    leads, 
    updateLeadStage, 
    updateLeadStatus,
    getLeadMessages, 
    getLeadFollowups, 
    getLeadTimeline, 
    getLeadSuggestedReply,
    getDealCoachRecommendations,
    addMessage,
    sendSuggestedReply,
    addFollowupTask,
    completeFollowupTask
  } = useLeads();

  const [messageInput, setMessageInput] = useState("");
  const [followupReason, setFollowupReason] = useState("");
  const [followupChannel, setFollowupChannel] = useState<"email" | "phone" | "linkedin">("email");
  const [followupDays, setFollowupDays] = useState(2);
  const [showCoachRecommendation, setShowCoachRecommendation] = useState(false);
  const [coachLoading, setCoachLoading] = useState(false);

  const lead = leads.find((l: Lead) => l.id === leadId);

  if (!lead) {
    return (
      <div className="space-y-6 max-w-4xl mx-auto text-center py-12">
        <h2 className="text-lg font-bold text-slate-800">Lead not found</h2>
        <p className="text-sm text-slate-500">The requested lead ID {id} does not exist in the database.</p>
        <Link href="/leads" className="inline-flex items-center gap-2 text-sm text-[#6366f1] font-semibold mt-4">
          <ArrowLeft className="w-4 h-4" /> Back to Leads
        </Link>
      </div>
    );
  }

  const messages = getLeadMessages(lead.id);
  const followups = getLeadFollowups(lead.id);
  const timeline = getLeadTimeline(lead.id);
  const suggestedReply = getLeadSuggestedReply(lead.id);
  const coachRecommendations = getDealCoachRecommendations(lead.id);

  // Phase 2: Progress stages list
  const STAGES = [
    { key: "new", label: "New Lead" },
    { key: "qualified", label: "Qualified" },
    { key: "outreach_sent", label: "Outreach Sent" },
    { key: "customer_replied", label: "Customer Replied" },
    { key: "followup_scheduled", label: "Followup Scheduled" },
    { key: "converted", label: "Converted" }
  ];

  const currentStageIndex = STAGES.findIndex(s => s.key === lead.stage);

  // AI Mock Predictions (Dynamic based on lead parameters)
  const isSarahDemo = lead.id === 999;
  const rawScore = lead.stage === "new" ? 72 : 94;
  const conversionProb = isSarahDemo 
    ? (lead.stage === "converted" ? 100 : lead.stage === "customer_replied" || lead.stage === "followup_scheduled" ? 95 : 60)
    : (lead.stage === "converted" ? 100 : lead.stage === "customer_replied" ? 88 : Math.max(30, Math.min(98, 98 - (lead.id % 20) * 3)));
  
  const aiConfidence = 85;

  const getAIReasons = () => {
    if (lead.stage === "converted") return ["Deal successfully closed.", "Demo completed successfully.", "Contract finalized."];
    if (conversionProb > 80) {
      return [
        "Inbound interest specifies checkout speed optimization needs.",
        "Prospect holds decision-making title (CTO / VP Operations).",
        "Clear budget alignment indicated in initial telemetry logs."
      ];
    }
    return [
      "Inbound webform submitted without detailed requirements.",
      "Awaiting direct response to SEO/latency diagnostic report.",
      "Medium priority status with traditional response timelines."
    ];
  };

  const getAIRisks = () => {
    if (lead.stage === "converted") return [];
    if (conversionProb > 80) {
      return [
        "Competitor evaluation in progress for latency tools.",
        "Timeline constraints due to deployment freeze next month."
      ];
    }
    return [
      "Response latency currently exceeding 3 days.",
      "No direct phone call completed yet.",
      "Low initial website capture telemetry scores."
    ];
  };

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!messageInput.trim()) return;
    addMessage(lead.id, "user", messageInput);
    setMessageInput("");
  };

  const handleAddFollowup = (e: React.FormEvent) => {
    e.preventDefault();
    if (!followupReason.trim()) return;
    addFollowupTask(lead.id, followupChannel, followupReason, followupDays);
    setFollowupReason("");
  };

  const handleAskDealCoach = () => {
    setCoachLoading(true);
    setTimeout(() => {
      setCoachLoading(false);
      setShowCoachRecommendation(true);
    }, 800);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header Profile */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white border border-slate-200/80 p-6 rounded-2xl shadow-sm">
        <div className="flex gap-4 items-center">
          <button 
            onClick={() => router.push("/leads")}
            className="p-2 border border-slate-200 rounded-xl hover:bg-slate-50 transition-colors shrink-0"
          >
            <ArrowLeft className="w-4 h-4 text-slate-600" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold font-display text-slate-800 tracking-tight">{lead.company}</h1>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border leading-none uppercase ${
                lead.status === "HOT"
                  ? "bg-[#10b981]/10 text-[#10b981] border-[#10b981]/20"
                  : lead.status === "WARM"
                  ? "bg-blue-500/10 text-blue-500 border-blue-500/20"
                  : "bg-slate-500/10 text-slate-500 border-slate-500/20"
              }`}>
                {lead.status}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">Prospect Owner: {lead.first_name} {lead.last_name} | Est. Rev: {lead.notes?.includes("Rev:") ? lead.notes.split("Rev:")[1].split(".")[0].trim() : "$1.5M"}</p>
          </div>
        </div>

        <div className="flex items-center gap-2 self-stretch sm:self-auto">
          <span className="text-xs font-semibold text-slate-500 mr-1 font-display">Update Stage:</span>
          <select
            value={lead.stage}
            onChange={(e) => updateLeadStage(lead.id, e.target.value)}
            className="px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:border-[#6366f1] transition-all font-semibold font-display cursor-pointer"
          >
            {STAGES.map((s) => (
              <option key={s.key} value={s.key}>{s.label}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Phase 2: Lead Status Progress Bar */}
      <div className="bg-white border border-slate-200/80 p-6 rounded-2xl shadow-sm">
        <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider font-display mb-6">Visual Stage Progress</h3>
        <div className="relative">
          {/* Progress Line */}
          <div className="absolute top-1/2 left-0 w-full h-1 bg-slate-100 -translate-y-1/2 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-[#6366f1] to-[#10b981] rounded-full transition-all duration-700"
              style={{ width: `${(currentStageIndex / (STAGES.length - 1)) * 100}%` }}
            ></div>
          </div>

          {/* Stepper Nodes */}
          <div className="relative flex justify-between">
            {STAGES.map((s, idx) => {
              const isActive = idx <= currentStageIndex;
              const isCurrent = idx === currentStageIndex;
              return (
                <div key={s.key} className="flex flex-col items-center select-none">
                  <div 
                    onClick={() => updateLeadStage(lead.id, s.key)}
                    className={`w-8 h-8 rounded-full border flex items-center justify-center text-xs font-bold transition-all duration-300 cursor-pointer ${
                      isCurrent
                        ? "bg-[#6366f1] text-white border-[#6366f1] ring-4 ring-[#6366f1]/15 shadow-md scale-110"
                        : isActive
                        ? "bg-emerald-500 text-white border-emerald-500"
                        : "bg-white text-slate-400 border-slate-200 hover:border-slate-400"
                    }`}
                  >
                    {isActive && idx < currentStageIndex ? (
                      <Check className="w-3.5 h-3.5 stroke-[3]" />
                    ) : (
                      idx + 1
                    )}
                  </div>
                  <span className={`text-[10px] mt-2.5 font-bold tracking-tight font-display text-center hidden md:block ${
                    isCurrent ? "text-[#6366f1]" : isActive ? "text-slate-800" : "text-slate-400"
                  }`}>
                    {s.label}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        {/* Left Columns (Details, Conversations, Timeline) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Lead Info Details */}
          <div className="bg-white border border-slate-200/80 p-6 rounded-2xl shadow-sm space-y-4">
            <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider font-display border-b border-slate-100 pb-3">Lead Information</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-sans">
              <div>
                <span className="text-slate-400 block mb-0.5">Contact Email</span>
                <span className="font-semibold text-slate-800">{lead.email}</span>
              </div>
              <div>
                <span className="text-slate-400 block mb-0.5">Contact Phone</span>
                <span className="font-semibold text-slate-800">{lead.phone}</span>
              </div>
              <div>
                <span className="text-slate-400 block mb-0.5">Industry Segment</span>
                <span className="font-semibold text-slate-800">{lead.industry}</span>
              </div>
              <div>
                <span className="text-slate-400 block mb-0.5">Telemetry Inbound Source</span>
                <span className="font-semibold text-slate-800">{lead.source}</span>
              </div>
            </div>
            <div className="pt-2">
              <span className="text-xs text-slate-400 block mb-1">System Internal Notes</span>
              <p className="text-xs bg-slate-50 border border-slate-100 p-3 rounded-xl leading-relaxed text-slate-700 font-sans">
                {lead.notes || "No special internal administration notes provided."}
              </p>
            </div>
          </div>

          {/* Conversation Thread */}
          <div className="bg-white border border-slate-200/80 p-6 rounded-2xl shadow-sm space-y-4">
            <div className="flex justify-between items-center border-b border-slate-100 pb-3">
              <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider font-display flex items-center gap-1.5">
                <MessageSquare className="w-4 h-4 text-indigo-500" /> Conversation Thread
              </h3>
              <span className="text-[10px] text-slate-400 font-mono">Channel: Email Integration</span>
            </div>

            {/* Message History Bubble List */}
            <div className="h-60 overflow-y-auto space-y-4 p-3 bg-slate-50/50 rounded-xl border border-slate-200/50">
              {messages.length === 0 ? (
                <div className="h-full flex flex-col justify-center items-center text-center text-slate-400 p-4">
                  <MessageSquare className="w-8 h-8 text-slate-300 mb-2 animate-bounce" />
                  <span className="text-xs font-semibold">No emails sent yet</span>
                  <span className="text-[10px] mt-1">Initiate conversation via outreach generation or wait for step 3 in the Demo Hub.</span>
                </div>
              ) : (
                messages.map((msg) => {
                  const isUser = msg.sender === "user";
                  return (
                    <div key={msg.id} className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
                      <div className={`max-w-[80%] p-3.5 rounded-2xl text-xs leading-normal shadow-[0_2px_6px_rgba(0,0,0,0.01)] ${
                        isUser 
                          ? "bg-[#6366f1] text-white rounded-br-none" 
                          : "bg-white border border-slate-200 text-slate-800 rounded-bl-none"
                      }`}>
                        <div className="font-bold text-[9px] uppercase tracking-wider mb-1 opacity-70">
                          {isUser ? "Outgoing Sales Agent" : `${lead.first_name} ${lead.last_name}`}
                        </div>
                        <p className="font-sans whitespace-pre-line">{msg.content}</p>
                        <span className="text-[8px] mt-1.5 block text-right opacity-60">
                          {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                      </div>
                    </div>
                  );
                })
              )}
            </div>

            {/* Custom Response Ingestion form */}
            <form onSubmit={handleSendMessage} className="flex gap-2">
              <input
                type="text"
                placeholder="Type reply message to prospect..."
                value={messageInput}
                onChange={(e) => setMessageInput(e.target.value)}
                className="flex-1 px-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 focus:outline-none focus:border-[#6366f1] transition-all font-sans"
              />
              <button
                type="submit"
                className="px-3.5 py-2 bg-[#6366f1] text-white hover:bg-indigo-600 rounded-lg transition-colors shadow-sm shrink-0"
              >
                <Send className="w-3.5 h-3.5" />
              </button>
            </form>

            {/* Suggested Reply Box */}
            {suggestedReply && (
              <div className="bg-indigo-50/50 border border-indigo-200 p-4 rounded-xl space-y-3 mt-4">
                <div className="flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4 text-indigo-500 fill-current animate-pulse" />
                  <span className="text-xs font-bold text-indigo-800 font-display">AI Suggested Outbound Reply</span>
                </div>
                <p className="text-xs text-slate-700 bg-white border border-indigo-100 p-3 rounded-lg font-sans leading-relaxed">
                  {suggestedReply}
                </p>
                <div className="flex justify-end gap-2">
                  <button
                    onClick={() => sendSuggestedReply(lead.id)}
                    className="px-4 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold shadow-sm font-display flex items-center gap-1"
                  >
                    <Check className="w-3.5 h-3.5" /> Approved: Send Reply
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Journey Timeline */}
          <div className="bg-white border border-slate-200/80 p-6 rounded-2xl shadow-sm space-y-4">
            <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider font-display border-b border-slate-100 pb-3 flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-blue-500" /> Journey Timeline &amp; Events
            </h3>
            
            <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-100 font-sans">
              {timeline.length === 0 ? (
                <div className="text-xs text-slate-400 py-2 pl-2">No timeline activities registered.</div>
              ) : (
                timeline.map((act) => {
                  return (
                    <div key={act.id} className="relative">
                      {/* Timeline dot */}
                      <span className="absolute -left-[20.5px] top-1 w-2.5 h-2.5 rounded-full border bg-white border-blue-500 ring-4 ring-blue-50"></span>
                      <div className="flex flex-col sm:flex-row justify-between items-start gap-1">
                        <div>
                          <span className="text-xs font-semibold text-slate-800 leading-normal">{act.note}</span>
                          <span className="text-[10px] text-slate-400 font-medium ml-2 uppercase font-display bg-slate-50 border px-1.5 py-0.2 rounded">
                            {act.channel || "system"}
                          </span>
                        </div>
                        <span className="text-[9px] text-slate-400 shrink-0 mt-1 sm:mt-0">
                          {act.created_at ? new Date(act.created_at).toLocaleDateString([], { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }) : "Just now"}
                        </span>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>

        {/* Right Column (AI Predictions, Followups, Deal Coach) */}
        <div className="space-y-6">
          {/* AI Deal Coach Widget */}
          <div className="bg-gradient-to-br from-indigo-950 to-slate-900 text-white p-6 rounded-3xl border border-indigo-500/20 shadow-lg relative overflow-hidden">
            {/* Sparkles backdrop */}
            <div className="absolute right-0 top-0 opacity-10 pointer-events-none translate-x-1/3 -translate-y-1/3">
              <Sparkles className="w-40 h-40" />
            </div>

            <div className="flex items-center gap-2 mb-4">
              <div className="p-2 bg-indigo-500/10 rounded-full text-indigo-400 border border-indigo-500/20">
                <Sparkles className="w-4.5 h-4.5 fill-current animate-pulse" />
              </div>
              <h3 className="text-xs font-bold font-display uppercase tracking-wider text-indigo-300">AI Deal Coach</h3>
            </div>

            <div className="space-y-3">
              <p className="text-xs text-slate-300 leading-normal">
                &quot;What should I do next with this lead?&quot;
              </p>
              
              {!showCoachRecommendation ? (
                <button
                  onClick={handleAskDealCoach}
                  disabled={coachLoading}
                  className="w-full flex items-center justify-center gap-1.5 px-3 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-800 text-white rounded-xl text-xs font-semibold transition-all shadow-[0_2px_8px_rgba(99,102,241,0.3)] font-display"
                >
                  <Play className="w-3.5 h-3.5 fill-current" />
                  <span>{coachLoading ? "Consulting Engine..." : "Ask Deal Coach"}</span>
                </button>
              ) : (
                <div className="space-y-3 animate-fade-in pt-1">
                  <div className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Coach Recommendations:</div>
                  <div className="space-y-2.5">
                    {coachRecommendations.map((rec, i) => (
                      <div key={i} className="flex gap-2 items-start text-xs bg-white/5 border border-white/5 p-2.5 rounded-xl">
                        <span className="text-emerald-400 mt-0.5 font-bold shrink-0">✓</span>
                        <span className="text-slate-200 font-sans leading-relaxed">{rec}</span>
                      </div>
                    ))}
                  </div>
                  <button
                    onClick={() => setShowCoachRecommendation(false)}
                    className="text-[10px] text-indigo-300 hover:text-indigo-200 mt-1 block font-semibold"
                  >
                    Clear recommendations
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* AI Insights & Predictions */}
          <div className="bg-white border border-slate-200/80 p-6 rounded-2xl shadow-sm space-y-4">
            <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider font-display border-b border-slate-100 pb-3 flex items-center gap-1.5">
              <TrendingUp className="w-4 h-4 text-[#10b981]" /> AI Diagnostics &amp; Conversion Probability
            </h3>

            {/* Probability Score */}
            <div className="flex items-center gap-4 py-2 border-b border-slate-100">
              <div className="relative w-16 h-16 shrink-0 flex items-center justify-center rounded-full bg-slate-50 border border-slate-200/50">
                <span className="text-base font-extrabold text-slate-800 font-display">{conversionProb}%</span>
              </div>
              <div>
                <span className="text-xs text-slate-400 block">Conversion Odds</span>
                <span className="text-sm font-bold text-slate-700">
                  {conversionProb >= 85 ? "High Probability" : conversionProb >= 50 ? "Medium Intent" : "Low Probability"}
                </span>
                <span className="text-[10px] text-slate-400 block mt-0.5">AI Confidence: {aiConfidence}%</span>
              </div>
            </div>

            {/* Diagnosed Pain Point */}
            <div className="space-y-1.5 pt-1">
              <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider font-display">Diagnosed Pain Point</span>
              <div className="p-3 bg-rose-50/50 border border-rose-100 text-rose-700 rounded-xl text-xs leading-relaxed font-semibold">
                {lead.stage === "new" ? "Diagnostics pending score." : "Website speed checkout API latency (>4s) detected via telemetry scan."}
              </div>
            </div>

            {/* AI Reasons */}
            <div className="space-y-2 pt-2 border-t border-slate-100">
              <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider font-display block">Primary Drivers</span>
              <div className="space-y-2 font-sans text-xs">
                {getAIReasons().map((r, i) => (
                  <div key={i} className="flex gap-2 items-start text-slate-600">
                    <span className="text-indigo-500 font-bold mt-0.5">•</span>
                    <span>{r}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* AI Risks */}
            {getAIRisks().length > 0 && (
              <div className="space-y-2 pt-2 border-t border-slate-100">
                <span className="text-[10px] text-rose-600 uppercase font-bold tracking-wider font-display block flex items-center gap-1">
                  <AlertTriangle className="w-3.5 h-3.5 text-rose-500" /> Risk Factors
                </span>
                <div className="space-y-2 font-sans text-xs">
                  {getAIRisks().map((r, i) => (
                    <div key={i} className="flex gap-2 items-start text-rose-600">
                      <span className="text-rose-500 font-bold mt-0.5">•</span>
                      <span>{r}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Follow-up Tasks */}
          <div className="bg-white border border-slate-200/80 p-6 rounded-2xl shadow-sm space-y-4">
            <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider font-display border-b border-slate-100 pb-3 flex items-center gap-1.5">
              <Calendar className="w-4 h-4 text-amber-500" /> Follow-up Action Items
            </h3>

            {/* Checklist */}
            <div className="space-y-3">
              {followups.length === 0 ? (
                <div className="text-xs text-slate-400 py-3 text-center">No scheduled follow-up actions.</div>
              ) : (
                followups.map((task) => (
                  <div 
                    key={task.id} 
                    className={`flex items-start gap-3 p-3 rounded-xl border transition-all ${
                      task.status === "completed" 
                        ? "bg-slate-50 border-slate-200 opacity-60" 
                        : "bg-amber-50/20 border-amber-200/50"
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={task.status === "completed"}
                      onChange={() => completeFollowupTask(task.id)}
                      className="mt-0.5 w-4 h-4 rounded text-amber-500 focus:ring-amber-500 cursor-pointer"
                    />
                    <div className="min-w-0 flex-1 text-xs">
                      <p className={`font-semibold leading-normal ${task.status === "completed" ? "line-through text-slate-500" : "text-slate-800"}`}>
                        {task.reason}
                      </p>
                      <div className="flex items-center gap-2 mt-1.5 text-[9px] text-slate-400 font-medium">
                        <span className="uppercase font-display border px-1 py-0.2 rounded">{task.channel}</span>
                        <span>Due: {new Date(task.due_at).toLocaleDateString([], { month: "short", day: "numeric" })}</span>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Add Followup Form */}
            <form onSubmit={handleAddFollowup} className="pt-3 border-t border-slate-100 space-y-3">
              <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider font-display block">Schedule New Task</span>
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="Task reason/details..."
                  value={followupReason}
                  onChange={(e) => setFollowupReason(e.target.value)}
                  className="flex-1 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 focus:outline-none focus:border-amber-500 transition-all font-sans"
                />
                <select
                  value={followupChannel}
                  onChange={(e) => setFollowupChannel(e.target.value as any)}
                  className="px-2 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-[10px] font-semibold text-slate-700 cursor-pointer"
                >
                  <option value="email">Email</option>
                  <option value="phone">Call</option>
                  <option value="linkedin">LinkedIn</option>
                </select>
              </div>
              <div className="flex justify-between items-center gap-2">
                <div className="flex items-center gap-1.5 text-[10px] text-slate-500">
                  <span>Due in:</span>
                  <input
                    type="number"
                    min={1}
                    max={30}
                    value={followupDays}
                    onChange={(e) => setFollowupDays(parseInt(e.target.value) || 1)}
                    className="w-10 px-1 py-0.5 border border-slate-200 bg-slate-50 rounded text-center text-xs font-semibold focus:outline-none"
                  />
                  <span>days</span>
                </div>
                <button
                  type="submit"
                  className="flex items-center gap-1 px-3 py-1.5 bg-amber-500 hover:bg-amber-600 text-white rounded-lg text-xs font-bold transition-all shadow-sm font-display"
                >
                  <Plus className="w-3.5 h-3.5" /> Schedule
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
