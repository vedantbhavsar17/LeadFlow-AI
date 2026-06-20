"use client";

import { useState } from "react";
import { useLeads, Conversation, Message } from "@/lib/lead-context";
import { Lead } from "@/services/api-client";
import { 
  MessageSquare, 
  Send, 
  Sparkles, 
  Check, 
  Clock, 
  User, 
  Bot, 
  ChevronRight,
  Inbox
} from "lucide-react";

export default function ConversationsPage() {
  const { 
    leads, 
    conversations, 
    addMessage, 
    sendSuggestedReply 
  } = useLeads();

  // Find all leads that have conversation threads
  const activeThreads = conversations.map((c: Conversation) => {
    const lead = leads.find((l: Lead) => l.id === c.leadId);
    const lastMessage = c.messages.length > 0 ? c.messages[c.messages.length - 1] : null;
    return {
      conversation: c,
      lead,
      lastMessage
    };
  }).filter((t) => t.lead !== undefined) as { conversation: Conversation; lead: Lead; lastMessage: Message | null }[];

  const [selectedLeadId, setSelectedLeadId] = useState<number | null>(
    activeThreads.length > 0 ? activeThreads[0].lead?.id || null : null
  );

  const [replyText, setReplyText] = useState("");

  const currentThread = activeThreads.find(t => t.lead?.id === selectedLeadId);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!replyText.trim() || !selectedLeadId) return;
    addMessage(selectedLeadId, "user", replyText);
    setReplyText("");
  };

  const handleSendSuggested = () => {
    if (!selectedLeadId) return;
    sendSuggestedReply(selectedLeadId);
  };

  return (
    <div className="h-[calc(100vh-10rem)] max-w-7xl mx-auto bg-white border border-slate-200/80 rounded-2xl shadow-sm overflow-hidden flex font-sans">
      {/* Sidebar: Threads List */}
      <div className="w-80 border-r border-slate-200 flex flex-col shrink-0 bg-slate-50/30">
        <div className="p-4 border-b border-slate-200 bg-white">
          <div className="flex items-center gap-2">
            <Inbox className="w-4 h-4 text-indigo-500" />
            <h3 className="text-xs font-bold font-display uppercase tracking-wider text-slate-800">Conversations Inbox</h3>
          </div>
          <p className="text-[10px] text-slate-400 mt-1">Manage outbound sales emails and incoming feedback.</p>
        </div>

        <div className="flex-1 overflow-y-auto divide-y divide-slate-100">
          {activeThreads.length === 0 ? (
            <div className="p-6 text-center text-slate-400 text-xs flex flex-col items-center justify-center h-40">
              <MessageSquare className="w-6 h-6 text-slate-300 mb-2" />
              <span>No active conversations</span>
              <span className="text-[9px] text-slate-400 mt-1">Run steps in the Demo Hub to simulate discussions.</span>
            </div>
          ) : (
            activeThreads.map((thread) => {
              const isSelected = thread.lead?.id === selectedLeadId;
              const lastMsgContent = thread.lastMessage?.content || "No messages";
              const lastMsgTime = thread.lastMessage 
                ? new Date(thread.lastMessage.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
                : "";

              return (
                <div
                  key={thread.lead?.id}
                  onClick={() => setSelectedLeadId(thread.lead?.id || null)}
                  className={`p-4 cursor-pointer transition-all flex flex-col gap-1.5 border-l-2 select-none hover:bg-slate-50 ${
                    isSelected 
                      ? "bg-indigo-50/30 border-[#6366f1] shadow-[inset_4px_0_12px_rgba(99,102,241,0.02)]" 
                      : "border-transparent"
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-xs text-slate-800 truncate max-w-[140px] font-display">
                      {thread.lead?.company}
                    </span>
                    <span className="text-[8px] text-slate-400 font-medium shrink-0 flex items-center gap-1">
                      <Clock className="w-2.5 h-2.5" /> {lastMsgTime}
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-[10px] text-slate-400 truncate max-w-[140px]">
                      {thread.lead?.first_name} {thread.lead?.last_name}
                    </span>
                    <span className={`text-[8px] font-extrabold px-1.5 py-0.2 rounded border leading-none uppercase ${
                      thread.lead?.status === "HOT"
                        ? "bg-[#10b981]/10 text-[#10b981] border-[#10b981]/20"
                        : "bg-blue-500/10 text-blue-500 border-blue-500/20"
                    }`}>
                      {thread.lead?.status}
                    </span>
                  </div>

                  <p className="text-[10px] text-slate-500 truncate leading-relaxed">
                    {lastMsgContent}
                  </p>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Main Chat Pane */}
      <div className="flex-1 flex flex-col bg-slate-50/10">
        {currentThread ? (
          <>
            {/* Header */}
            <div className="p-4 border-b border-slate-200 bg-white flex justify-between items-center">
              <div>
                <h4 className="text-xs font-bold font-display text-slate-800">
                  {currentThread.lead?.company}
                </h4>
                <p className="text-[10px] text-slate-400 mt-0.5">
                  Contact: {currentThread.lead?.first_name} {currentThread.lead?.last_name} | {currentThread.lead?.email}
                </p>
              </div>
              <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full border leading-none uppercase ${
                currentThread.lead?.stage === "converted"
                  ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                  : "bg-indigo-50 text-indigo-700 border-indigo-200"
              }`}>
                Stage: {currentThread.lead?.stage.replace("_", " ")}
              </span>
            </div>

            {/* Messages Stream */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {currentThread.conversation.messages.map((msg) => {
                const isUser = msg.sender === "user";
                return (
                  <div key={msg.id} className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
                    <div className="flex gap-2 items-end max-w-[70%]">
                      {!isUser && (
                        <div className="w-6 h-6 rounded-full bg-slate-200 flex items-center justify-center text-[10px] font-bold text-slate-500 shrink-0">
                          <User className="w-3.5 h-3.5" />
                        </div>
                      )}
                      <div className={`p-3.5 rounded-2xl text-xs leading-normal shadow-[0_1px_4px_rgba(0,0,0,0.01)] ${
                        isUser 
                          ? "bg-[#6366f1] text-white rounded-br-none" 
                          : "bg-white border border-slate-200 text-slate-800 rounded-bl-none"
                      }`}>
                        <p className="font-sans whitespace-pre-line">{msg.content}</p>
                        <span className="text-[8px] mt-1.5 block text-right opacity-60">
                          {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Suggested Reply Box (Drawer) */}
            {currentThread.conversation.suggestedReply && (
              <div className="px-4 py-3 bg-indigo-50/50 border-t border-indigo-100 flex flex-col gap-2">
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-indigo-500 fill-current animate-pulse" />
                    <span className="text-[10px] font-bold text-indigo-800 font-display">AI Suggested Reply</span>
                  </div>
                  <button
                    onClick={handleSendSuggested}
                    className="flex items-center gap-1 px-3 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-[10px] font-bold transition-all shadow-sm font-display"
                  >
                    <Check className="w-3 h-3" /> Approve &amp; Send
                  </button>
                </div>
                <p className="text-[10px] text-slate-600 bg-white border border-indigo-100 p-2.5 rounded-lg font-sans leading-relaxed">
                  {currentThread.conversation.suggestedReply}
                </p>
              </div>
            )}

            {/* Input Form */}
            <form onSubmit={handleSend} className="p-4 border-t border-slate-200 bg-white flex gap-2">
              <input
                type="text"
                placeholder="Type your response email..."
                value={replyText}
                onChange={(e) => setReplyText(e.target.value)}
                className="flex-1 px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:border-[#6366f1] transition-all font-sans"
              />
              <button
                type="submit"
                className="px-4 py-2 bg-[#6366f1] text-white hover:bg-indigo-600 rounded-xl text-xs font-semibold shadow-sm font-display flex items-center gap-1.5 shrink-0"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Send</span>
              </button>
            </form>
          </>
        ) : (
          <div className="flex-1 flex flex-col justify-center items-center text-slate-400 text-center p-6 h-full">
            <MessageSquare className="w-10 h-10 text-slate-300 mb-2 animate-pulse" />
            <h4 className="font-bold text-slate-700">No conversation selected</h4>
            <p className="text-xs text-slate-400 mt-1 max-w-xs leading-normal">
              Select a thread from the inbox sidebar to view history, review AI suggested responses, and reply.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
