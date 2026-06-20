"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { ApiClient, Lead, LeadActivity, BusinessContext, DashboardMetrics } from "../services/api-client";

export function normalizeLeadStatus(status: string | undefined | null): string {
  if (!status) return "WARM";
  const s = status.toUpperCase();
  if (["HOT", "INTERESTED", "QUALIFIED", "MEETING_BOOKED"].includes(s)) {
    return "HOT";
  }
  if (["WARM", "NEW", "CONTACTED"].includes(s)) {
    return "WARM";
  }
  if (["COLD", "NO_RESPONSE", "NOT_INTERESTED", "UNQUALIFIED", "LOST", "CONVERTED"].includes(s)) {
    return "COLD";
  }
  return "WARM";
}

export function normalizeLeadStage(stage: string | undefined | null): string {
  if (!stage) return "new";
  const s = stage.toLowerCase().trim();
  if (s === "qualification") return "qualified";
  if (s === "negotiation") return "proposal_sent";
  return s;
}


export interface Message {
  id: string;
  sender: "customer" | "user" | "ai";
  content: string;
  created_at: string;
}

export interface Conversation {
  leadId: number;
  threadId: string;
  messages: Message[];
  suggestedReply: string | null;
}

export interface Followup {
  id: string;
  leadId: number;
  channel: "email" | "phone" | "linkedin";
  reason: string;
  due_at: string;
  status: "pending" | "completed";
}

interface LeadContextType {
  leads: Lead[];
  activities: LeadActivity[];
  businessContext: BusinessContext | null;
  conversations: Conversation[];
  followups: Followup[];
  selectedLeadId: number | null;
  setSelectedLeadId: (id: number | null) => void;
  loading: boolean;
  isBackendOnline: boolean;
  demoScriptStep: number;
  setDemoScriptStep: (step: number) => void;
  
  // Actions
  refreshData: () => Promise<void>;
  generate50DemoLeads: () => void;
  resetDatabase: () => void;
  addLead: (lead: Partial<Lead>) => Promise<Lead>;
  updateLeadStage: (id: number, stage: string) => Promise<void>;
  updateLeadStatus: (id: number, status: string) => Promise<void>;
  saveBusinessContext: (context: BusinessContext) => Promise<void>;
  addMessage: (leadId: number, sender: "customer" | "user" | "ai", content: string) => Promise<void>;
  sendSuggestedReply: (leadId: number) => Promise<void>;
  addFollowupTask: (leadId: number, channel: "email" | "phone" | "linkedin", reason: string, dueInDays: number) => Promise<void>;
  completeFollowupTask: (id: string) => Promise<void>;
  triggerDemoStep: (step: number) => void;
  
  // Helpers
  getLeadMessages: (leadId: number) => Message[];
  getLeadFollowups: (leadId: number) => Followup[];
  getLeadTimeline: (leadId: number) => LeadActivity[];
  getLeadSuggestedReply: (leadId: number) => string | null;
  getDealCoachRecommendations: (leadId: number) => string[];
}

const LeadContext = createContext<LeadContextType | undefined>(undefined);

export function LeadProvider({ children }: { children: React.ReactNode }) {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [activities, setActivities] = useState<LeadActivity[]>([]);
  const [businessContext, setBusinessContext] = useState<BusinessContext | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [followups, setFollowups] = useState<Followup[]>([]);
  const [selectedLeadId, setSelectedLeadId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [isBackendOnline, setIsBackendOnline] = useState(false);
  const [demoScriptStep, setDemoScriptStep] = useState(0);

  // Initialize data on mount
  useEffect(() => {
    refreshData();
  }, []);

  const checkBackendHealth = async (): Promise<boolean> => {
    try {
      const res = await fetch("/api/health");
      if (res.ok) {
        const data = await res.json();
        return data.status === "healthy" || data.status === "OK" || true;
      }
      return false;
    } catch {
      return false;
    }
  };

  const refreshData = async () => {
    setLoading(true);
    const online = await checkBackendHealth();
    setIsBackendOnline(online);

    if (online) {
      try {
        const leadsRes = await ApiClient.getLeads();
        const normalizedLeads = leadsRes.leads.map((l: Lead) => ({
          ...l,
          status: normalizeLeadStatus(l.status),
          stage: normalizeLeadStage(l.stage)
        }));
        setLeads(normalizedLeads);

        // Fetch context
        try {
          const ctxRes = await ApiClient.getBusinessContext();
          setBusinessContext(ctxRes.business_context);
        } catch {
          // If no context exists yet, it's fine
        }
        
        // Sync activities
        const allActs: LeadActivity[] = [];
        for (const l of leadsRes.leads) {
          try {
            const actRes = await ApiClient.getLeadTimeline(l.id);
            allActs.push(...actRes.activities);
          } catch {}
        }
        setActivities(allActs);

        // Sync followups from backend
        const allFollows: Followup[] = [];
        for (const l of leadsRes.leads) {
          try {
            const followRes = await ApiClient.getFollowups(l.id);
            allFollows.push(...followRes.followups.map((f: any) => ({
              id: String(f.id),
              leadId: f.lead_id,
              channel: f.channel,
              reason: f.reason,
              due_at: f.due_at,
              status: f.status
            })));
          } catch {}
        }
        setFollowups(allFollows);

        // Sync conversations from backend
        const allConvs: Conversation[] = [];
        for (const l of leadsRes.leads) {
          try {
            const convRes = await ApiClient.getMessages(l.id);
            if (convRes.messages && convRes.messages.length > 0) {
              allConvs.push({
                leadId: l.id,
                threadId: `thread_${l.id}`,
                messages: convRes.messages.map((m: any) => ({
                  id: String(m.id),
                  sender: m.sender as any,
                  content: m.content,
                  created_at: m.created_at
                })),
                suggestedReply: convRes.suggested_reply
              });
            }
          } catch {}
        }
        setConversations(allConvs);

      } catch (err) {
        console.error("Backend fetch failed, using fallback mock data:", err);
        loadMockData();
      }
    } else {
      loadMockData();
    }
    setLoading(false);
  };

  const loadMockData = () => {
    // Standard starting leads
    const mockLeads: Lead[] = [
      {
        id: 1,
        first_name: "John",
        last_name: "Doe",
        email: "john@acme.com",
        phone: "+1-555-0101",
        company: "Acme Corp",
        industry: "SaaS Agency",
        source: "Web Form",
        stage: "qualified",
        status: "HOT",
        priority: "high",
        notes: "Highly interested in automating their sales outbound.",
        assigned_to: "Representative Alpha",
        external_source_id: null,
        campaign_name: "Outbound Alpha",
        last_contacted_at: new Date(Date.now() - 3600000 * 2).toISOString(),
        last_followup_at: null,
        converted_at: null,
        lost_at: null,
        created_at: new Date(Date.now() - 3600000 * 24).toISOString(),
        updated_at: new Date(Date.now() - 3600000 * 2).toISOString(),
      },
      {
        id: 2,
        first_name: "Jane",
        last_name: "Smith",
        email: "jane@apex.com",
        phone: "+1-555-0102",
        company: "Apex Global",
        industry: "E-Commerce",
        source: "Ads",
        stage: "outreach_sent",
        status: "WARM",
        priority: "normal",
        notes: "Failed core web vitals and mobile indexing gaps identified.",
        assigned_to: "Representative Alpha",
        external_source_id: null,
        campaign_name: "Ad campaign Q2",
        last_contacted_at: new Date(Date.now() - 3600000 * 5).toISOString(),
        last_followup_at: null,
        converted_at: null,
        lost_at: null,
        created_at: new Date(Date.now() - 3600000 * 48).toISOString(),
        updated_at: new Date(Date.now() - 3600000 * 5).toISOString(),
      },
      {
        id: 3,
        first_name: "Robert",
        last_name: "Johnson",
        email: "robert@localbistro.com",
        phone: "+1-555-0103",
        company: "Local Bistro Group",
        industry: "Restaurant",
        source: "Referrals",
        stage: "new",
        status: "COLD",
        priority: "low",
        notes: "Missing responsive mobile design elements.",
        assigned_to: null,
        external_source_id: null,
        campaign_name: null,
        last_contacted_at: null,
        last_followup_at: null,
        converted_at: null,
        lost_at: null,
        created_at: new Date(Date.now() - 3600000 * 72).toISOString(),
        updated_at: new Date(Date.now() - 3600000 * 72).toISOString(),
      }
    ];

    setLeads(mockLeads);

    const mockActivities: LeadActivity[] = [
      { id: 1, lead_id: 1, activity_type: "lead_created", channel: "system", note: "Lead created via Web Form.", created_at: new Date(Date.now() - 3600000 * 24).toISOString(), updated_at: "" },
      { id: 2, lead_id: 1, activity_type: "status_changed", channel: "system", note: "Stage updated to qualified. AI Score computed: 91.", created_at: new Date(Date.now() - 3600000 * 23).toISOString(), updated_at: "" },
      { id: 3, lead_id: 2, activity_type: "lead_created", channel: "system", note: "Lead imported from Ad campaign.", created_at: new Date(Date.now() - 3600000 * 48).toISOString(), updated_at: "" },
      { id: 4, lead_id: 2, activity_type: "outreach_sent", channel: "email", note: "AI outreach email sent highlighting SEO pain points.", created_at: new Date(Date.now() - 3600000 * 5).toISOString(), updated_at: "" }
    ];
    setActivities(mockActivities);

    setBusinessContext({
      company_name: "LeadFlow AI",
      industry: "B2B SaaS",
      services: "Automated Lead Qualification & Engagement",
      ideal_customer_profile: "B2B service providers, SaaS companies, and digital agencies.",
      target_market: "Growth-stage companies receiving 100+ inbound leads monthly.",
      common_pain_points: "Slow follow-up times, unqualified sales calls, lack of CRM discipline.",
      competitors: "Manual outreach platforms, legacy HubSpot flows.",
      brand_tone: "Professional, analytical, yet highly engaging and responsive.",
      sales_goals: "Book 20 qualified demos per rep monthly."
    });

    const mockConvs: Conversation[] = [
      {
        leadId: 1,
        threadId: "t1",
        messages: [
          { id: "m1", sender: "user", content: "Hi John, noticed Acme Corp's website speed latency is currently 6.4s. Do you have 5 mins to chat about how this impacts your conversion?", created_at: new Date(Date.now() - 3600000 * 2).toISOString() }
        ],
        suggestedReply: "Hey John, thanks for responding. Since checkout latency is your main dropoff point, here is our demo scheduling link: leadflow.ai/demo"
      },
      {
        leadId: 2,
        threadId: "t2",
        messages: [
          { id: "m2", sender: "user", content: "Hi Jane, I ran a diagnostic on Apex Global and noticed multiple indexing gaps. Are you looking to scale e-commerce search rankings this quarter?", created_at: new Date(Date.now() - 3600000 * 5).toISOString() }
        ],
        suggestedReply: null
      }
    ];
    setConversations(mockConvs);

    const mockFollowups: Followup[] = [
      { id: "f1", leadId: 1, channel: "email", reason: "Follow up on diagnostic audit presentation", due_at: new Date(Date.now() + 86400000).toISOString(), status: "pending" }
    ];
    setFollowups(mockFollowups);
  };

  const generate50DemoLeads = () => {
    const firstNames = ["Sarah", "Avery", "Liam", "Sophia", "Noah", "Emma", "Oliver", "Ava", "Elijah", "Isabella", "James", "Mia", "Benjamin", "Charlotte", "Lucas", "Amelia", "Mason", "Harper", "Logan", "Evelyn"];
    const lastNames = ["Jenkins", "Shah", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White", "Lopez", "Lee", "Gonzalez"];
    const companies = ["CloudScale Solutions", "Apex Retail", "TechFlow Inc", "Optima Growth", "Vortex Digital", "Northstar FinTech", "Quantify Media", "Integra Lab", "Quantum Analytics", "BlueSky Capital", "Zeta Health", "Prism Consulting", "Alpha Legal", "LaunchPad Software", "Beacon Logistics", "Matrix E-Commerce", "Nexus Security", "Elevate HR", "Nova Learning", "Aero Manufacturing"];
    const industries = ["B2B SaaS", "E-Commerce", "Healthcare Tech", "Logistics", "Digital Agency", "Consulting", "Finance", "Legal Tech", "Education", "Manufacturing"];
    const sources = ["Web Form", "Ads", "LinkedIn Outreach", "Cold Email", "Referrals"];
    const stages = ["new", "qualified", "outreach_sent", "customer_replied", "followup_scheduled", "converted"];
    const priorities = ["low", "normal", "high", "urgent"];
    const statusChoices = ["HOT", "WARM", "COLD"];
    const painPoints = [
      "Website landing page loading speed is 5.8s, leading to high bounce rate",
      "No contact collection form on service pages",
      "Form submission API takes 3.4s to respond, causing transaction dropoffs",
      "Outdated SSL certificates and security protocol warning on checkout",
      "Broken SEO redirects causing 404 indexing errors on main blog",
      "Missing OpenGraph tags and metadata for social link sharing previews",
      "Cart checkout mobile layout is non-responsive",
      "Search widget yields zero-results queries frequently",
      "DNS resolution lags in APAC region by up to 2.1 seconds",
      "API request timeouts on mobile billing options"
    ];

    const generatedLeads: Lead[] = [];
    const generatedActivities: LeadActivity[] = [];
    const generatedConversations: Conversation[] = [];
    const generatedFollowups: Followup[] = [];

    // Reset settings
    setSelectedLeadId(null);
    setDemoScriptStep(0);

    for (let i = 4; i <= 53; i++) {
      const first = firstNames[i % firstNames.length];
      const last = lastNames[i % lastNames.length];
      const name = `${first} ${last}`;
      const company = `${companies[i % companies.length]} ${Math.random() > 0.6 ? "Group" : "Ltd"}`;
      const industry = industries[i % industries.length];
      const source = sources[i % sources.length];
      const stage = stages[i % stages.length];
      const priority = priorities[i % priorities.length];
      const score = Math.floor(Math.random() * 60) + 40; // 40-99
      const status = score >= 85 ? "HOT" : score >= 60 ? "WARM" : "COLD";
      const revenue = `$${(Math.random() * 20 + 1).toFixed(1)}M`;
      const pain = painPoints[i % painPoints.length];
      const daysAgo = Math.floor(Math.random() * 10) + 1;
      const createdDate = new Date(Date.now() - 86400000 * daysAgo).toISOString();

      const lead: Lead = {
        id: i,
        first_name: first,
        last_name: last,
        email: `${first.toLowerCase()}.${last.toLowerCase()}@${companies[i % companies.length].toLowerCase().replace(/\s+/g, "")}.com`,
        phone: `+1-555-01${i.toString().padStart(2, "0")}`,
        company,
        industry,
        source,
        stage,
        status,
        priority,
        notes: `Automatically identified pain point: ${pain}. Est. Rev: ${revenue}.`,
        assigned_to: "Representative Alpha",
        external_source_id: null,
        campaign_name: source === "Ads" ? "Ad campaign Q2" : "Organic Inbound",
        last_contacted_at: stage !== "new" ? new Date(Date.now() - 3600000 * (daysAgo * 12)).toISOString() : null,
        last_followup_at: stage === "followup_scheduled" ? new Date(Date.now() - 3600000 * 2).toISOString() : null,
        converted_at: stage === "converted" ? new Date().toISOString() : null,
        lost_at: null,
        created_at: createdDate,
        updated_at: new Date().toISOString(),
      };

      generatedLeads.push(lead);

      // Activities
      let actId = activities.length + generatedActivities.length + 1;
      generatedActivities.push({
        id: actId++,
        lead_id: i,
        activity_type: "lead_created",
        channel: "system",
        note: `Lead created via ${source}.`,
        created_at: createdDate,
        updated_at: ""
      });

      if (stage !== "new") {
        generatedActivities.push({
          id: actId++,
          lead_id: i,
          activity_type: "status_changed",
          channel: "system",
          note: `Lead qualified. Diagnostic score: ${score} (${status}). Identified pain: ${pain}.`,
          created_at: new Date(new Date(createdDate).getTime() + 1800000).toISOString(),
          updated_at: ""
        });
      }

      if (stage === "outreach_sent" || stage === "customer_replied" || stage === "followup_scheduled" || stage === "converted") {
        generatedActivities.push({
          id: actId++,
          lead_id: i,
          activity_type: "outreach_sent",
          channel: "email",
          note: `Personalized outbound email sent concerning website latency.`,
          created_at: new Date(new Date(createdDate).getTime() + 7200000).toISOString(),
          updated_at: ""
        });
      }

      // Conversations
      if (stage === "customer_replied" || stage === "followup_scheduled" || stage === "converted") {
        const emailSentDate = new Date(new Date(createdDate).getTime() + 7200000).toISOString();
        const replyDate = new Date(new Date(emailSentDate).getTime() + 14400000).toISOString();
        
        const messages: Message[] = [
          {
            id: `m_${i}_1`,
            sender: "user",
            content: `Hi ${first}, I noticed ${company}'s system is facing: ${pain}. Our LeadFlow optimizer handles this in real-time. Do you have a few minutes for a brief call?`,
            created_at: emailSentDate
          },
          {
            id: `m_${i}_2`,
            sender: "customer",
            content: `Thanks for the heads-up, ${first}. Yes, checkout lags are definitely hurting our conversion rates this month. Can you send pricing information and a link to schedule a demo?`,
            created_at: replyDate
          }
        ];

        if (stage === "converted") {
          messages.push({
            id: `m_${i}_3`,
            sender: "user",
            content: `Absolutely! Here is our scheduler: leadflow.ai/demo. I've also attached the pricing deck. Looking forward to our call.`,
            created_at: new Date(new Date(replyDate).getTime() + 3600000).toISOString()
          });
          messages.push({
            id: `m_${i}_4`,
            sender: "customer",
            content: `Perfect, booked for Thursday at 2 PM. Excited to see the demo!`,
            created_at: new Date(new Date(replyDate).getTime() + 7200000).toISOString()
          });
        }

        generatedConversations.push({
          leadId: i,
          threadId: `thread_${i}`,
          messages,
          suggestedReply: stage === "customer_replied" 
            ? `Hi ${first}, absolutely! You can schedule a convenient time here: leadflow.ai/demo. I am also attaching our pricing sheet outlining our packages.` 
            : null
        });
      }

      // Follow-ups
      if (stage === "followup_scheduled") {
        generatedFollowups.push({
          id: `f_${i}`,
          leadId: i,
          channel: "email",
          reason: "Send checkout optimizer demo link and confirm pricing options",
          due_at: new Date(Date.now() + 86400000 * 2).toISOString(),
          status: "pending"
        });
      }
    }

    setLeads((prev) => [...prev.filter(l => l.id <= 3), ...generatedLeads]);
    setActivities((prev) => [...prev.filter(a => a.lead_id <= 3), ...generatedActivities]);
    setConversations((prev) => [...prev.filter(c => c.leadId <= 3), ...generatedConversations]);
    setFollowups((prev) => [...prev.filter(f => f.leadId <= 3), ...generatedFollowups]);
  };

  const resetDatabase = () => {
    setSelectedLeadId(null);
    setDemoScriptStep(0);
    loadMockData();
  };

  const addLead = async (leadData: Partial<Lead>): Promise<Lead> => {
    if (isBackendOnline) {
      try {
        const res = await ApiClient.createLead(leadData);
        const mappedLead = { 
          ...res.lead, 
          status: normalizeLeadStatus(res.lead.status),
          stage: normalizeLeadStage(res.lead.stage)
        };
        setLeads(prev => [mappedLead, ...prev]);
        return mappedLead;
      } catch (err) {
        console.error("Backend create lead failed, using fallback:", err);
      }
    }

    const nextId = leads.length > 0 ? Math.max(...leads.map(l => l.id)) + 1 : 1;
    const newLead: Lead = {
      id: nextId,
      first_name: leadData.first_name || "New",
      last_name: leadData.last_name || "Lead",
      email: leadData.email || "new@lead.com",
      phone: leadData.phone || "+1-555-0000",
      company: leadData.company || "New Company",
      industry: leadData.industry || "Technology",
      source: leadData.source || "Manual Ingestion",
      stage: leadData.stage || "new",
      status: leadData.status || "WARM",
      priority: leadData.priority || "normal",
      notes: leadData.notes || "",
      assigned_to: "Representative Alpha",
      external_source_id: null,
      campaign_name: null,
      last_contacted_at: null,
      last_followup_at: null,
      converted_at: null,
      lost_at: null,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    setLeads(prev => [newLead, ...prev]);

    // Add activity
    const newAct: LeadActivity = {
      id: activities.length + 1,
      lead_id: nextId,
      activity_type: "lead_created",
      channel: "system",
      note: "Lead ingested.",
      created_at: new Date().toISOString(),
      updated_at: ""
    };
    setActivities(prev => [newAct, ...prev]);

    return newLead;
  };

  const updateLeadStage = async (id: number, stage: string) => {
    if (isBackendOnline) {
      try {
        await ApiClient.changeLeadStage(id, stage);
      } catch (err) {
        console.error("Backend stage update failed:", err);
      }
    }

    setLeads(prev => prev.map(l => {
      if (l.id === id) {
        const converted_at = stage === "converted" ? new Date().toISOString() : l.converted_at;
        return { ...l, stage, converted_at, updated_at: new Date().toISOString() };
      }
      return l;
    }));

    // Add activity
    const newAct: LeadActivity = {
      id: activities.length + 1,
      lead_id: id,
      activity_type: "status_changed",
      channel: "system",
      note: `Stage updated to: ${stage.replace("_", " ")}.`,
      created_at: new Date().toISOString(),
      updated_at: ""
    };
    setActivities(prev => [newAct, ...prev]);
  };

  const updateLeadStatus = async (id: number, status: string) => {
    if (isBackendOnline) {
      try {
        await ApiClient.changeLeadStatus(id, status);
      } catch (err) {
        console.error("Backend status update failed:", err);
      }
    }
    const normalizedStatus = normalizeLeadStatus(status);
    setLeads(prev => prev.map(l => l.id === id ? { ...l, status: normalizedStatus, updated_at: new Date().toISOString() } : l));
  };

  const saveBusinessContext = async (context: BusinessContext) => {
    if (isBackendOnline) {
      try {
        const res = await ApiClient.createBusinessContext(context);
        setBusinessContext(res.business_context);
        return;
      } catch (err) {
        console.error("Backend context save failed:", err);
      }
    }

    setBusinessContext(context);
  };

  const addMessage = async (leadId: number, sender: "customer" | "user" | "ai", content: string) => {
    if (isBackendOnline && leadId !== 999) {
      try {
        await ApiClient.createMessage(leadId, { sender, content });
        await refreshData();
        return;
      } catch (err) {
        console.error("Backend add message failed:", err);
      }
    }

    setConversations(prev => {
      const idx = prev.findIndex(c => c.leadId === leadId);
      const newMsg: Message = {
        id: `m_${leadId}_${Date.now()}`,
        sender,
        content,
        created_at: new Date().toISOString()
      };

      if (idx === -1) {
        return [...prev, {
          leadId,
          threadId: `thread_${leadId}`,
          messages: [newMsg],
          suggestedReply: null
        }];
      } else {
        return prev.map((c, i) => i === idx ? { ...c, messages: [...c.messages, newMsg] } : c);
      }
    });

    // Add activity for outbound messages
    if (sender === "user") {
      setActivities(prev => [{
        id: prev.length + 1,
        lead_id: leadId,
        activity_type: "outreach_sent",
        channel: "email",
        note: `Sent response message to prospect.`,
        created_at: new Date().toISOString(),
        updated_at: ""
      }, ...prev]);
    } else if (sender === "customer") {
      setActivities(prev => [{
        id: prev.length + 1,
        lead_id: leadId,
        activity_type: "reply_received",
        channel: "email",
        note: `Inbound customer reply received.`,
        created_at: new Date().toISOString(),
        updated_at: ""
      }, ...prev]);
    }
  };

  const sendSuggestedReply = async (leadId: number) => {
    const thread = conversations.find(c => c.leadId === leadId);
    if (!thread || !thread.suggestedReply) return;

    const replyText = thread.suggestedReply;
    
    if (isBackendOnline && leadId !== 999) {
      try {
        await ApiClient.createMessage(leadId, { sender: "user", content: replyText });
        await ApiClient.changeLeadStage(leadId, "followup_scheduled");
        await refreshData();
        return;
      } catch (err) {
        console.error("Backend send suggested reply failed:", err);
      }
    }

    // Add outreach sent activity
    addMessage(leadId, "user", replyText);

    // Clear suggested reply and update stage to followup_scheduled or outreach_sent
    setConversations(prev => prev.map(c => c.leadId === leadId ? { ...c, suggestedReply: null } : c));
    updateLeadStage(leadId, "followup_scheduled");
  };

  const addFollowupTask = async (leadId: number, channel: "email" | "phone" | "linkedin", reason: string, dueInDays: number) => {
    if (isBackendOnline && leadId !== 999) {
      try {
        const due_at = new Date(Date.now() + 86400000 * dueInDays).toISOString();
        await ApiClient.createFollowup(leadId, { channel, reason, due_at });
        await refreshData();
        return;
      } catch (err) {
        console.error("Backend create followup task failed:", err);
      }
    }

    const newFollow: Followup = {
      id: `f_${leadId}_${Date.now()}`,
      leadId,
      channel,
      reason,
      due_at: new Date(Date.now() + 86400000 * dueInDays).toISOString(),
      status: "pending"
    };

    setFollowups(prev => [newFollow, ...prev]);

    setActivities(prev => [{
      id: prev.length + 1,
      lead_id: leadId,
      activity_type: "followup_created",
      channel: "system",
      note: `Followup task scheduled via ${channel}: ${reason}`,
      created_at: new Date().toISOString(),
      updated_at: ""
    }, ...prev]);
  };

  const completeFollowupTask = async (id: string) => {
    if (isBackendOnline && !id.startsWith("demo_") && !isNaN(Number(id))) {
      try {
        await ApiClient.completeFollowup(Number(id));
        await refreshData();
        return;
      } catch (err) {
        console.error("Backend complete followup task failed:", err);
      }
    }

    const task = followups.find(f => f.id === id);
    setFollowups(prev => prev.map(f => f.id === id ? { ...f, status: "completed" as const } : f));
    
    if (task) {
      setActivities(prev => [{
        id: prev.length + 1,
        lead_id: task.leadId,
        activity_type: "followup_completed",
        channel: "system",
        note: `Followup completed: ${task.reason}`,
        created_at: new Date().toISOString(),
        updated_at: ""
      }, ...prev]);
    }
  };

  // Demo script state machine
  const triggerDemoStep = async (step: number) => {
    setDemoScriptStep(step);
    
    const DEMO_LEAD_ID = 999;

    if (step === 1) {
      // Step 1: New Lead enters
      const newLead: Lead = {
        id: DEMO_LEAD_ID,
        first_name: "Sarah",
        last_name: "Jenkins",
        email: "sarah.j@cloudscale.com",
        phone: "+1-555-0899",
        company: "CloudScale Solutions",
        industry: "B2B SaaS",
        source: "Web Form",
        stage: "new",
        status: "WARM",
        priority: "normal",
        notes: "CTO submitted form looking for latency optimization audits.",
        assigned_to: "Representative Alpha",
        external_source_id: null,
        campaign_name: "Web Inbound",
        last_contacted_at: null,
        last_followup_at: null,
        converted_at: null,
        lost_at: null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };

      setLeads(prev => [newLead, ...prev.filter(l => l.id !== DEMO_LEAD_ID)]);
      setSelectedLeadId(DEMO_LEAD_ID);

      const act: LeadActivity = {
        id: activities.length + 101,
        lead_id: DEMO_LEAD_ID,
        activity_type: "lead_created",
        channel: "system",
        note: "Lead created from Web Form submission (sarah.j@cloudscale.com).",
        created_at: new Date().toISOString(),
        updated_at: ""
      };
      setActivities(prev => [act, ...prev.filter(a => a.lead_id !== DEMO_LEAD_ID)]);

      // Clear conversation & follow-up for this demo ID
      setConversations(prev => prev.filter(c => c.leadId !== DEMO_LEAD_ID));
      setFollowups(prev => prev.filter(f => f.leadId !== DEMO_LEAD_ID));

    } else if (step === 2) {
      // Step 2: AI qualifies lead
      setLeads(prev => prev.map(l => l.id === DEMO_LEAD_ID ? {
        ...l,
        stage: "qualified",
        status: "HOT",
        priority: "high",
        notes: "AI Diagnostics completed. High intent signal. Core pain: Checkout API latency (4.8s), leading to 18% cart dropoff.",
        updated_at: new Date().toISOString()
      } : l));

      setActivities(prev => [
        {
          id: activities.length + 102,
          lead_id: DEMO_LEAD_ID,
          activity_type: "status_changed",
          channel: "system",
          note: "Lead qualified as HOT. AI score calculated: 94. Pain identified: Checkout latencies.",
          created_at: new Date().toISOString(),
          updated_at: ""
        },
        ...prev
      ]);

    } else if (step === 3) {
      // Step 3: AI generates outreach
      setLeads(prev => prev.map(l => l.id === DEMO_LEAD_ID ? {
        ...l,
        stage: "outreach_sent",
        last_contacted_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      } : l));

      setActivities(prev => [
        {
          id: activities.length + 103,
          lead_id: DEMO_LEAD_ID,
          activity_type: "outreach_sent",
          channel: "email",
          note: "AI outreach sent to sarah.j@cloudscale.com. Pitch topic: latency-based dropoff reduction.",
          created_at: new Date().toISOString(),
          updated_at: ""
        },
        ...prev
      ]);

      const threadMsg: Message = {
        id: `demo_m1`,
        sender: "user",
        content: "Hi Sarah, I noticed CloudScale Solutions has a checkout loading speed of 4.8s. Our optimizer fixes checkout latency instantly and recaptures lost revenue. Do you have 10 minutes for a quick demo this Thursday?",
        created_at: new Date(Date.now() - 5000).toISOString()
      };

      setConversations(prev => [
        {
          leadId: DEMO_LEAD_ID,
          threadId: `thread_${DEMO_LEAD_ID}`,
          messages: [threadMsg],
          suggestedReply: null
        },
        ...prev.filter(c => c.leadId !== DEMO_LEAD_ID)
      ]);

    } else if (step === 4) {
      // Step 4: Customer replies
      setLeads(prev => prev.map(l => l.id === DEMO_LEAD_ID ? {
        ...l,
        stage: "customer_replied",
        updated_at: new Date().toISOString()
      } : l));

      setActivities(prev => [
        {
          id: activities.length + 104,
          lead_id: DEMO_LEAD_ID,
          activity_type: "reply_received",
          channel: "email",
          note: "Customer reply received: Interested in checkout speed demonstration and pricing details.",
          created_at: new Date().toISOString(),
          updated_at: ""
        },
        ...prev
      ]);

      const customerMsg: Message = {
        id: `demo_m2`,
        sender: "customer",
        content: "Thanks for reaching out! Yes, checkout latency is a major focus for us right now, we are losing sales. Can you send pricing information and a link to schedule a demo?",
        created_at: new Date().toISOString()
      };

      setConversations(prev => prev.map(c => c.leadId === DEMO_LEAD_ID ? {
        ...c,
        messages: [...c.messages, customerMsg],
        suggestedReply: "Hi Sarah, absolutely! Here is our demo calendar link: leadflow.ai/demo. I've also attached our standard pricing grid for SaaS packages."
      } : c));

    } else if (step === 5) {
      // Step 5: AI analyzes reply (updates conversion probability)
      // Done inside context states - the detailed prediction will now reflect 95% conversion score
      setActivities(prev => [
        {
          id: activities.length + 105,
          lead_id: DEMO_LEAD_ID,
          activity_type: "status_changed",
          channel: "system",
          note: "AI Analyzed sentiment: positive. Conversion probability updated to 95%. Suggested response generated.",
          created_at: new Date().toISOString(),
          updated_at: ""
        },
        ...prev
      ]);

    } else if (step === 6) {
      // Step 6: Followup generated
      setLeads(prev => prev.map(l => l.id === DEMO_LEAD_ID ? {
        ...l,
        stage: "followup_scheduled",
        last_followup_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      } : l));

      const replyMsg: Message = {
        id: `demo_m3`,
        sender: "user",
        content: "Hi Sarah, absolutely! Here is our demo calendar link: leadflow.ai/demo. I've also attached our standard pricing grid for SaaS packages.",
        created_at: new Date().toISOString()
      };

      setConversations(prev => prev.map(c => c.leadId === DEMO_LEAD_ID ? {
        ...c,
        messages: [...c.messages, replyMsg],
        suggestedReply: null
      } : c));

      const follow: Followup = {
        id: `demo_f1`,
        leadId: DEMO_LEAD_ID,
        channel: "email",
        reason: "Confirm demo booking details and follow up on pricing approval",
        due_at: new Date(Date.now() + 86400000 * 2).toISOString(),
        status: "pending"
      };

      setFollowups(prev => [follow, ...prev.filter(f => f.id !== `demo_f1`)]);

      setActivities(prev => [
        {
          id: activities.length + 106,
          lead_id: DEMO_LEAD_ID,
          activity_type: "followup_created",
          channel: "system",
          note: "Followup task generated: Confirm demo booking details and follow up on pricing approval.",
          created_at: new Date().toISOString(),
          updated_at: ""
        },
        ...prev
      ]);

    } else if (step === 7) {
      // Step 7: Conversion concluded
      setLeads(prev => prev.map(l => l.id === DEMO_LEAD_ID ? {
        ...l,
        stage: "converted",
        status: "HOT",
        converted_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      } : l));

      // Mark the followup as completed
      setFollowups(prev => prev.map(f => f.leadId === DEMO_LEAD_ID ? { ...f, status: "completed" as const } : f));

      setActivities(prev => [
        {
          id: activities.length + 107,
          lead_id: DEMO_LEAD_ID,
          activity_type: "followup_completed",
          channel: "system",
          note: "Followup completed: Booking confirmed.",
          created_at: new Date().toISOString(),
          updated_at: ""
        },
        {
          id: activities.length + 108,
          lead_id: DEMO_LEAD_ID,
          activity_type: "status_changed",
          channel: "system",
          note: "Lead converted successfully! Deal won.",
          created_at: new Date().toISOString(),
          updated_at: ""
        },
        ...prev
      ]);
    }
  };

  // Helper selectors
  const getLeadMessages = (leadId: number) => {
    return conversations.find(c => c.leadId === leadId)?.messages || [];
  };

  const getLeadFollowups = (leadId: number) => {
    return followups.filter(f => f.leadId === leadId);
  };

  const getLeadTimeline = (leadId: number) => {
    return activities.filter(a => a.lead_id === leadId);
  };

  const getLeadSuggestedReply = (leadId: number) => {
    return conversations.find(c => c.leadId === leadId)?.suggestedReply || null;
  };

  const getDealCoachRecommendations = (leadId: number) => {
    const lead = leads.find(l => l.id === leadId);
    if (!lead) return ["Ingest a prospect to see Deal Coach tips."];

    const currentStage = lead.stage;

    switch (currentStage) {
      case "new":
        return [
          "Ask Deal Coach to analyze initial tech profile.",
          "Generate and send AI outreach email highlighting core latency problems.",
          "Identify and assign to a sales administrator."
        ];
      case "qualified":
        return [
          "Initiate outbound copy campaign (analytical gaps style).",
          "Offer a direct diagnostic audit of checkout page latency.",
          "Send personalized diagnostic checklist."
        ];
      case "outreach_sent":
        return [
          "Wait for email IMAP inbound listener response (approx. 24 hours).",
          "If no response, prepare a secondary soft follow-up in 2 days.",
          "Connect on LinkedIn to warm up the channel."
        ];
      case "customer_replied":
        return [
          "Highly Positive Intent detected! AI recommends sending the demo calendar scheduling link.",
          "Send pricing details requested in the customer's email.",
          "Prepare 10-minute speed-optimization demo assets."
        ];
      case "followup_scheduled":
        return [
          "Ensure calendar appointment is set up in CRM.",
          "Follow up 2 hours before the meeting with calendar invite.",
          "Confirm pricing sheets and SLA parameters are shared."
        ];
      case "converted":
        return [
          "Deal successfully closed! 🎉",
          "Initiate customer onboarding workflow.",
          "Sync lead status to external HubSpot CRM integration."
        ];
      default:
        return [
          "Analyze previous activities in the journey timeline.",
          "Identify secondary stake-holders within the company.",
          "Conduct outbound call to target phone number."
        ];
    }
  };

  return (
    <LeadContext.Provider
      value={{
        leads,
        activities,
        businessContext,
        conversations,
        followups,
        selectedLeadId,
        setSelectedLeadId,
        loading,
        isBackendOnline,
        demoScriptStep,
        setDemoScriptStep,
        refreshData,
        generate50DemoLeads,
        resetDatabase,
        addLead,
        updateLeadStage,
        updateLeadStatus,
        saveBusinessContext,
        addMessage,
        sendSuggestedReply,
        addFollowupTask,
        completeFollowupTask,
        triggerDemoStep,
        getLeadMessages,
        getLeadFollowups,
        getLeadTimeline,
        getLeadSuggestedReply,
        getDealCoachRecommendations
      }}
    >
      {children}
    </LeadContext.Provider>
  );
}

export function useLeads() {
  const context = useContext(LeadContext);
  if (!context) {
    throw new Error("useLeads must be used within a LeadProvider");
  }
  return context;
}
