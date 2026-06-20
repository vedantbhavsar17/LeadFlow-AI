// LeadFlow API Client for Backend Integration

export interface Lead {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  company: string;
  source: string;
  stage: string;
  status: string;
  priority: string;
  notes: string | null;
  assigned_to: string | null;
  external_source_id: string | null;
  campaign_name: string | null;
  last_contacted_at: string | null;
  last_followup_at: string | null;
  converted_at: string | null;
  lost_at: string | null;
  created_at: string;
  updated_at: string;
  industry?: string;
  revenue?: string;
}

export interface LeadActivity {
  id: number;
  lead_id: number;
  activity_type: string;
  channel: string;
  note: string;
  created_at: string;
  updated_at: string;
}

export interface BusinessContext {
  id?: number;
  company_name: string;
  industry: string;
  services: string;
  ideal_customer_profile: string;
  target_market: string;
  common_pain_points: string;
  competitors: string;
  brand_tone: string;
  sales_goals: string;
  created_at?: string;
  updated_at?: string;
}

export interface DashboardMetrics {
  total_leads: number;
  qualified_leads: number;
  engaged_leads: number;
  converted_leads: number;
  conversion_rate: number;
  hot_leads_count: number;
  followups_due_count: number;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const url = path.startsWith("/") ? path : `/${path}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || `HTTP Error ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export const ApiClient = {
  // Leads API
  async getLeads(params?: {
    limit?: number;
    offset?: number;
    source?: string;
    stage?: string;
    status?: string;
    assigned_to?: string;
  }): Promise<{ leads: Lead[] }> {
    const query = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, val]) => {
        if (val !== undefined && val !== null) {
          query.append(key, String(val));
        }
      });
    }
    const queryString = query.toString();
    return request<{ leads: Lead[] }>(`/api/leads${queryString ? `?${queryString}` : ""}`);
  },

  async getLead(id: number): Promise<{ lead: Lead }> {
    return request<{ lead: Lead }>(`/api/leads/${id}`);
  },

  async createLead(lead: Partial<Lead>): Promise<{ lead: Lead }> {
    return request<{ lead: Lead }>("/api/leads", {
      method: "POST",
      body: JSON.stringify(lead),
    });
  },

  async updateLead(id: number, lead: Partial<Lead>): Promise<{ lead: Lead }> {
    return request<{ lead: Lead }>(`/api/leads/${id}`, {
      method: "PUT",
      body: JSON.stringify(lead),
    });
  },

  async changeLeadStatus(id: number, status: string): Promise<{ lead: Lead }> {
    return request<{ lead: Lead }>(`/api/leads/${id}/status`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    });
  },

  async changeLeadStage(id: number, stage: string): Promise<{ lead: Lead }> {
    return request<{ lead: Lead }>(`/api/leads/${id}/stage`, {
      method: "PATCH",
      body: JSON.stringify({ stage }),
    });
  },

  async getLeadTimeline(id: number): Promise<{ activities: LeadActivity[] }> {
    return request<{ activities: LeadActivity[] }>(`/api/leads/${id}/timeline`);
  },

  async getLeadJourney(id: number): Promise<{ journey: any }> {
    return request<{ journey: any }>(`/api/leads/${id}/journey`);
  },

  async getLeadStageProgress(id: number): Promise<{ stage_progress: any }> {
    return request<{ stage_progress: any }>(`/api/leads/${id}/stage-progress`);
  },

  // Business Context API
  async getBusinessContext(): Promise<{ business_context: BusinessContext }> {
    return request<{ business_context: BusinessContext }>("/api/business-context");
  },

  async createBusinessContext(context: BusinessContext): Promise<{ business_context: BusinessContext }> {
    return request<{ business_context: BusinessContext }>("/api/business-context", {
      method: "POST",
      body: JSON.stringify(context),
    });
  },

  async updateBusinessContext(context: BusinessContext): Promise<{ business_context: BusinessContext }> {
    return request<{ business_context: BusinessContext }>("/api/business-context", {
      method: "PUT",
      body: JSON.stringify(context),
    });
  },

  // Analytics API
  async getDashboardMetrics(): Promise<{ dashboard: DashboardMetrics }> {
    return request<{ dashboard: DashboardMetrics }>("/api/analytics/dashboard");
  },

  // Ingestion API
  async importManualLead(payload: {
    name: string;
    email: string;
    phone?: string;
    company?: string;
    notes?: string;
  }): Promise<{ lead: Lead; raw_event: any }> {
    return request<{ lead: Lead; raw_event: any }>("/api/import/manual", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  async importCsvLeads(csvContent: string): Promise<{
    success_count: number;
    failed_count: number;
    duplicate_count: number;
    raw_event_count: number;
    errors: string[];
  }> {
    return request<{
      success_count: number;
      failed_count: number;
      duplicate_count: number;
      raw_event_count: number;
      errors: string[];
    }>("/api/import/csv", {
      method: "POST",
      body: JSON.stringify({ csv: csvContent }),
    });
  },

  // Followups API
  async getFollowups(leadId: number): Promise<{ followups: any[] }> {
    return request<{ followups: any[] }>(`/api/leads/${leadId}/followups`);
  },

  async createFollowup(leadId: number, followup: { channel: string; reason: string; due_at: string }): Promise<{ followup: any }> {
    return request<{ followup: any }>(`/api/leads/${leadId}/followups`, {
      method: "POST",
      body: JSON.stringify(followup),
    });
  },

  async completeFollowup(followupId: number): Promise<{ followup: any }> {
    return request<{ followup: any }>(`/api/leads/followups/${followupId}/complete`, {
      method: "PATCH",
    });
  },

  // Messages & Conversations API
  async getMessages(leadId: number): Promise<{ messages: any[]; suggested_reply: string | null }> {
    return request<{ messages: any[]; suggested_reply: string | null }>(`/api/leads/${leadId}/messages`);
  },

  async createMessage(leadId: number, message: { sender: string; content: string; channel?: string }): Promise<{ message: any }> {
    return request<{ message: any }>(`/api/leads/${leadId}/messages`, {
      method: "POST",
      body: JSON.stringify(message),
    });
  },

  async getConversations(): Promise<{ conversations: any[] }> {
    return request<{ conversations: any[] }>("/api/leads/conversations");
  },
};
