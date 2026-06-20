"use client";

import { useState, useEffect } from "react";
import { Cpu, Key, Save, Check, Briefcase } from "lucide-react";
import { useLeads } from "@/lib/lead-context";

export default function SettingsPage() {
  const { businessContext, saveBusinessContext } = useLeads();

  // Agent config state
  const [agentName, setAgentName] = useState("Representative Alpha");
  const [pitchStyle, setPitchStyle] = useState("Analytical Gaps focus (Recommended)");
  const [scanFrequency, setScanFrequency] = useState("Continuous (Real-time checks)");
  
  // API Keys state
  const [hubspotKey, setHubspotKey] = useState("••••••••••••••••••••••••");
  const [salesforceKey, setSalesforceKey] = useState("");
  const [openaiKey, setOpenaiKey] = useState("••••••••••••••••••••••••••••••••");
  const [showKeys, setShowKeys] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Business Context state
  const [companyName, setCompanyName] = useState("");
  const [industry, setIndustry] = useState("");
  const [services, setServices] = useState("");
  const [icp, setIcp] = useState("");
  const [targetMarket, setTargetMarket] = useState("");
  const [brandTone, setBrandTone] = useState("");
  const [painPoints, setPainPoints] = useState("");
  const [competitors, setCompetitors] = useState("");
  const [salesGoals, setSalesGoals] = useState("");

  // Load from context on mount/update
  useEffect(() => {
    if (businessContext) {
      setCompanyName(businessContext.company_name || "");
      setIndustry(businessContext.industry || "");
      setServices(businessContext.services || "");
      setIcp(businessContext.ideal_customer_profile || "");
      setTargetMarket(businessContext.target_market || "");
      setBrandTone(businessContext.brand_tone || "");
      setPainPoints(businessContext.common_pain_points || "");
      setCompetitors(businessContext.competitors || "");
      setSalesGoals(businessContext.sales_goals || "");
    }
  }, [businessContext]);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Save to context
    await saveBusinessContext({
      company_name: companyName,
      industry: industry,
      services: services,
      ideal_customer_profile: icp,
      target_market: targetMarket,
      brand_tone: brandTone,
      common_pain_points: painPoints,
      competitors: competitors,
      sales_goals: salesGoals
    });

    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 2000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold font-display text-slate-800 tracking-tight">System Operations &amp; Keys</h1>
        <p className="text-sm text-slate-500 mt-1">Configure active AI models, business context parameters, and third-party CRM API integrations.</p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* Card 1: Business Context Setup */}
        <div className="bg-white border border-slate-200 p-6 rounded-2xl shadow-sm space-y-6">
          <h3 className="text-sm font-semibold text-slate-800 flex items-center gap-2 border-b border-slate-100 pb-3 font-display uppercase tracking-wider">
            <Briefcase className="w-4 h-4 text-[#6366f1]" /> Business Context &amp; ICP Setup
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex flex-col gap-2">
              <label className="text-xs font-semibold text-slate-500 font-display">Company Name</label>
              <input
                type="text"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                className="px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-sans"
                placeholder="e.g. LeadFlow AI"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-xs font-semibold text-slate-500 font-display">Company Industry</label>
              <input
                type="text"
                value={industry}
                onChange={(e) => setIndustry(e.target.value)}
                className="px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-sans"
                placeholder="e.g. B2B SaaS"
              />
            </div>

            <div className="flex flex-col gap-2 md:col-span-2">
              <label className="text-xs font-semibold text-slate-500 font-display">Services Offered</label>
              <input
                type="text"
                value={services}
                onChange={(e) => setServices(e.target.value)}
                className="px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-sans"
                placeholder="e.g. Outbound marketing automation, speed diagnostics"
              />
            </div>

            <div className="flex flex-col gap-2 md:col-span-2">
              <label className="text-xs font-semibold text-slate-500 font-display">Ideal Customer Profile (ICP) Description</label>
              <textarea
                value={icp}
                onChange={(e) => setIcp(e.target.value)}
                rows={2}
                className="px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-sans"
                placeholder="e.g. Technology leaders at growth-stage SaaS firms struggling with site speeds"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-xs font-semibold text-slate-500 font-display">Target Market &amp; Segments</label>
              <input
                type="text"
                value={targetMarket}
                onChange={(e) => setTargetMarket(e.target.value)}
                className="px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-sans"
                placeholder="e.g. US/Europe SaaS companies"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-xs font-semibold text-slate-500 font-display">Brand Tone</label>
              <input
                type="text"
                value={brandTone}
                onChange={(e) => setBrandTone(e.target.value)}
                className="px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-sans"
                placeholder="e.g. Professional, analytical, helpful"
              />
            </div>

            <div className="flex flex-col gap-2 md:col-span-2">
              <label className="text-xs font-semibold text-slate-500 font-display">Common Prospect Pain Points</label>
              <textarea
                value={painPoints}
                onChange={(e) => setPainPoints(e.target.value)}
                rows={2}
                className="px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-sans"
                placeholder="e.g. High bounce rates, dropoffs in checkout flows, slow page loads"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-xs font-semibold text-slate-500 font-display">Key Competitors</label>
              <input
                type="text"
                value={competitors}
                onChange={(e) => setCompetitors(e.target.value)}
                className="px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-sans"
                placeholder="e.g. Traditional CRMs, manual outreach tools"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-xs font-semibold text-slate-500 font-display">Sales Objectives / Goals</label>
              <input
                type="text"
                value={salesGoals}
                onChange={(e) => setSalesGoals(e.target.value)}
                className="px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-sans"
                placeholder="e.g. Schedule 10 quality checkout audit demos monthly"
              />
            </div>
          </div>
        </div>

        {/* Card 2: AI Agent Configuration */}
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
                className="px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-sans cursor-pointer"
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
                className="px-4 py-2 bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#6366f1] focus:ring-2 focus:ring-[#6366f1]/15 transition-all font-sans cursor-pointer"
              >
                <option>Continuous (Real-time checks)</option>
                <option>Daily Batch Processing</option>
                <option>Weekly Outbox Cycle</option>
              </select>
            </div>
          </div>
        </div>

        {/* Card 3: API Keys & Credentials */}
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
