"use client";

import { useState } from "react";
import { Cpu, Key, Save, Check } from "lucide-react";

export default function SettingsPage() {
  const [agentName, setAgentName] = useState("Representative Alpha");
  const [pitchStyle, setPitchStyle] = useState("Analytical Gaps focus (Recommended)");
  const [scanFrequency, setScanFrequency] = useState("Continuous (Real-time checks)");
  const [hubspotKey, setHubspotKey] = useState("••••••••••••••••••••••••");
  const [salesforceKey, setSalesforceKey] = useState("");
  const [openaiKey, setOpenaiKey] = useState("••••••••••••••••••••••••••••••••");
  const [showKeys, setShowKeys] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 2000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold font-display text-slate-800 tracking-tight">System Operations &amp; Keys</h1>
        <p className="text-sm text-slate-500 mt-1">Configure active AI models and third-party CRM API integrations.</p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* Card 1: AI Agent Configuration */}
        <div className="bg-white border border-slate-200 p-6 rounded-2xl shadow-sm space-y-6">
          <h3 className="text-sm font-semibold text-slate-800 flex items-center gap-2 border-b border-slate-100 pb-3 font-display uppercase tracking-wider">
            <Cpu className="w-4 h-4 text-[#6366f1]" /> AI Agent Representative Profiles
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex flex-col gap-2">
              <label className="text-xs font-semibold text-slate-500 font-display">Agent Identity Name</label>
              <input
                type="text"
                value={agentName}
                onChange={(e) => setAgentName(e.target.value)}
                className="px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-sans"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-xs font-semibold text-slate-500 font-display">Outbound Copy Pitch Style</label>
              <select
                value={pitchStyle}
                onChange={(e) => setPitchStyle(e.target.value)}
                className="px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-sans"
              >
                <option>Analytical Gaps focus (Recommended)</option>
                <option>Aggressive ROI &amp; Revenue Pitch</option>
                <option>Soft Introduction &amp; Scheduling Request</option>
              </select>
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-xs font-semibold text-slate-500 font-display">Diagnostic Scanning Frequency</label>
              <select
                value={scanFrequency}
                onChange={(e) => setScanFrequency(e.target.value)}
                className="px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-sans"
              >
                <option>Continuous (Real-time checks)</option>
                <option>Daily Batch Processing</option>
                <option>Weekly Outbox Cycle</option>
              </select>
            </div>
          </div>
        </div>

        {/* Card 2: API Keys & Credentials */}
        <div className="bg-white border border-slate-200 p-6 rounded-2xl shadow-sm space-y-6">
          <div className="flex justify-between items-center border-b border-slate-100 pb-3">
            <h3 className="text-sm font-semibold text-slate-800 flex items-center gap-2 font-display uppercase tracking-wider">
              <Key className="w-4 h-4 text-[#6366f1]" /> Integrations &amp; API Tokens
            </h3>
            <button
              type="button"
              onClick={() => setShowKeys(!showKeys)}
              className="text-[10px] text-slate-500 hover:text-slate-800 border border-slate-200 px-2.5 py-1 rounded bg-slate-50 transition-colors font-semibold"
            >
              {showKeys ? "Hide Keys" : "Show Keys"}
            </button>
          </div>

          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
              <div className="flex flex-col">
                <span className="text-xs font-semibold text-slate-800">HubSpot Integration API</span>
                <span className="text-[10px] text-slate-400 mt-0.5 font-sans">Allows syncing qualified leads.</span>
              </div>
              <div className="md:col-span-2">
                <input
                  type={showKeys ? "text" : "password"}
                  value={hubspotKey}
                  onChange={(e) => setHubspotKey(e.target.value)}
                  className="w-full px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-mono"
                  placeholder="Insert HubSpot access token..."
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
              <div className="flex flex-col">
                <span className="text-xs font-semibold text-slate-800">Salesforce Client Secret</span>
                <span className="text-[10px] text-slate-400 mt-0.5 font-sans">Allows scheduling direct callbacks.</span>
              </div>
              <div className="md:col-span-2">
                <input
                  type={showKeys ? "text" : "password"}
                  value={salesforceKey}
                  onChange={(e) => setSalesforceKey(e.target.value)}
                  className="w-full px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-mono"
                  placeholder="Insert Salesforce secret key..."
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
              <div className="flex flex-col">
                <span className="text-xs font-semibold text-slate-800">OpenAI API Key credential</span>
                <span className="text-[10px] text-slate-400 mt-0.5 font-sans">Runs generative outreach models.</span>
              </div>
              <div className="md:col-span-2">
                <input
                  type={showKeys ? "text" : "password"}
                  value={openaiKey}
                  onChange={(e) => setOpenaiKey(e.target.value)}
                  className="w-full px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-mono"
                  placeholder="sk-..."
                />
              </div>
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="flex justify-end gap-3">
          <button
            type="submit"
            className="flex items-center gap-2 px-6 py-2.5 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] hover:brightness-105 text-white rounded-lg text-sm font-medium transition-all shadow-[0_4px_12px_rgba(99,102,241,0.25)] font-display"
          >
            {saveSuccess ? (
              <>
                <Check className="w-4 h-4" />
                <span>Configuration Saved</span>
              </>
            ) : (
              <>
                <Save className="w-4 h-4" />
                <span>Save Changes</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
