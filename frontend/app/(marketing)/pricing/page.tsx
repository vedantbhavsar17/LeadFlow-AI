"use client";

import { useState } from "react";
import Link from "next/link";
import { Check, X, ChevronDown } from "lucide-react";

export default function PricingPage() {
  const [isAnnual, setIsAnnual] = useState(false);
  const [activeFaq, setActiveFaq] = useState<number | null>(null);

  const toggleFaq = (index: number) => {
    setActiveFaq(activeFaq === index ? null : index);
  };

  return (
    <div>
      {/* Premium Navigation */}
      <header className="navbar">
        <div className="nav-container">
          <Link href="/" className="logo">
            <img src="/logo.jpg" alt="LeadFlow Logo" className="logo-icon" />
            <span className="logo-text">
              LeadFlow <span className="ai-badge">AI</span>
            </span>
          </Link>
          <nav className="nav-links">
            <Link href="/#features">Features</Link>
            <Link href="/#showcase">Dashboard</Link>
            <Link href="/#roadmap">Roadmap</Link>
            <Link href="/pricing" className="active">
              Pricing
            </Link>
          </nav>
          <div className="nav-actions">
            <Link href="/#demo" className="btn btn-secondary btn-sm" id="nav-demo-btn">
              Watch Demo
            </Link>
            <Link href="/dashboard" className="btn btn-primary btn-sm" id="nav-cta-btn">
              Get Started
            </Link>
          </div>
        </div>
      </header>

      {/* Pricing Hero & Billing Toggle */}
      <section className="pricing-hero">
        <div className="pricing-bg-glow"></div>
        <div className="container text-center">
          <span className="section-tag">Flexible Plans</span>
          <h1 className="pricing-title">Simple, transparent pricing.</h1>
          <p className="pricing-sub">
            Choose the perfect autonomous pipeline configuration to supercharge your outbound sales
            operations.
          </p>

          {/* Toggle Control */}
          <div className="toggle-container">
            <span className={`toggle-label ${!isAnnual ? "active" : ""}`} id="billing-monthly">
              Monthly
            </span>
            <button
              className={`billing-toggle ${isAnnual ? "active" : ""}`}
              id="billing-toggle-btn"
              onClick={() => setIsAnnual(!isAnnual)}
            >
              <span className="toggle-circle"></span>
            </button>
            <span className={`toggle-label ${isAnnual ? "active" : ""}`} id="billing-annual">
              Annual <span className="discount-tag">Save 20%</span>
            </span>
          </div>
        </div>
      </section>

      {/* Pricing Cards Grid */}
      <section className="pricing-cards-section">
        <div className="container">
          <div className="pricing-grid">
            {/* Starter Plan */}
            <div className="pricing-card card-glass">
              <div className="plan-header">
                <h3>Starter</h3>
                <p className="plan-desc">For freelancers and solo agencies beginning outbound automation.</p>
                <div className="plan-price">
                  <span className="currency">$</span>
                  <span className="price-val">{isAnnual ? "39" : "49"}</span>
                  <span className="period">/mo</span>
                </div>
                <div className="annual-note">{isAnnual ? "Billed annually" : "Billed monthly"}</div>
              </div>
              <div className="plan-divider"></div>
              <ul className="plan-features">
                <li>
                  <Check className="col-green" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>1 Active AI Agent representative</span>
                </li>
                <li>
                  <Check className="col-green" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>1,000 qualified leads/mo</span>
                </li>
                <li>
                  <Check className="col-green" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>Standard website tech diagnostics</span>
                </li>
                <li>
                  <Check className="col-green" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>Core email copy generation</span>
                </li>
                <li>
                  <X className="col-red" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span className="disabled">AI Reply Intelligence parsing</span>
                </li>
                <li>
                  <X className="col-red" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span className="disabled">Lead Memory network graph</span>
                </li>
                <li>
                  <X className="col-red" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span className="disabled">CRM API synchronizations</span>
                </li>
              </ul>
              <div className="plan-cta">
                <Link href="/dashboard" className="btn btn-secondary">
                  Get Started
                </Link>
              </div>
            </div>

            {/* Growth Plan (Recommended) */}
            <div className="pricing-card card-glass recommended">
              <div className="recommended-badge">MOST POPULAR</div>
              <div className="plan-header">
                <h3>Growth</h3>
                <p className="plan-desc">For scaling agencies looking for deep lead intelligence.</p>
                <div className="plan-price">
                  <span className="currency">$</span>
                  <span className="price-val">{isAnnual ? "99" : "129"}</span>
                  <span className="period">/mo</span>
                </div>
                <div className="annual-note">{isAnnual ? "Billed annually" : "Billed monthly"}</div>
              </div>
              <div className="plan-divider"></div>
              <ul className="plan-features">
                <li>
                  <Check className="col-cyan" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>
                    <strong>3 Active AI Agent</strong> representatives
                  </span>
                </li>
                <li>
                  <Check className="col-cyan" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>
                    <strong>5,000 qualified leads/mo</strong>
                  </span>
                </li>
                <li>
                  <Check className="col-cyan" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>Deep footprint diagnostics scanning</span>
                </li>
                <li>
                  <Check className="col-cyan" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>Personalized outreach generation</span>
                </li>
                <li>
                  <Check className="col-cyan" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>AI Reply Intelligence parsing</span>
                </li>
                <li>
                  <Check className="col-cyan" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>Lead Memory database mapping</span>
                </li>
                <li>
                  <Check className="col-cyan" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>Native CRM &amp; Zapier sync</span>
                </li>
              </ul>
              <div className="plan-cta">
                <Link href="/dashboard" className="btn btn-primary">
                  Start Free Trial
                </Link>
              </div>
            </div>

            {/* Enterprise Plan */}
            <div className="pricing-card card-glass">
              <div className="plan-header">
                <h3>Enterprise</h3>
                <p className="plan-desc">For large companies demanding infinite volume and voice agents.</p>
                <div className="plan-price">
                  <span className="price-val custom-text">Custom</span>
                </div>
                <div className="annual-note">Contact for volume quotes</div>
              </div>
              <div className="plan-divider"></div>
              <ul className="plan-features">
                <li>
                  <Check className="col-green" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>
                    <strong>Unlimited AI Agent</strong> representatives
                  </span>
                </li>
                <li>
                  <Check className="col-green" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>
                    <strong>Unlimited lead processing</strong>
                  </span>
                </li>
                <li>
                  <Check className="col-green" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>Voice calling agents (ultra low latency)</span>
                </li>
                <li>
                  <Check className="col-green" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>Dedicated execution database</span>
                </li>
                <li>
                  <Check className="col-green" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>Custom LLM fine-tuning options</span>
                </li>
                <li>
                  <Check className="col-green" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>Dedicated Account Engineer</span>
                </li>
                <li>
                  <Check className="col-green" style={{ width: "16px", height: "16px", flexShrink: 0 }} />{" "}
                  <span>99.9% processing uptime SLA</span>
                </li>
              </ul>
              <div className="plan-cta">
                <Link href="/dashboard" className="btn btn-secondary">
                  Contact Sales
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Detailed Feature Comparison Table */}
      <section className="comparison-section">
        <div className="container">
          <div className="section-header text-center">
            <h2 className="section-title">Compare plan capabilities.</h2>
            <p className="section-sub">Every detail analyzed to help you find the right fit.</p>
          </div>

          <div className="comparison-table-wrapper card-glass">
            <table className="comparison-table">
              <thead>
                <tr>
                  <th>Outbound Capabilities</th>
                  <th>Starter</th>
                  <th>Growth</th>
                  <th>Enterprise</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="feature-name">Active Representatives</td>
                  <td>1 Agent</td>
                  <td>3 Agents</td>
                  <td>Unlimited Swarm</td>
                </tr>
                <tr>
                  <td className="feature-name">Monthly Processing Capacity</td>
                  <td>1,000 leads</td>
                  <td>5,000 leads</td>
                  <td>Unlimited</td>
                </tr>
                <tr>
                  <td className="feature-name">Website Bug Diagnostics</td>
                  <td>Standard</td>
                  <td>Deep Scan</td>
                  <td>Custom Scanning Script</td>
                </tr>
                <tr>
                  <td className="feature-name">Personalized Writing Models</td>
                  <td>
                    <Check className="col-green" style={{ width: "16px", height: "16px", margin: "auto" }} />
                  </td>
                  <td>
                    <Check className="col-green" style={{ width: "16px", height: "16px", margin: "auto" }} />
                  </td>
                  <td>Custom Fine-Tuning</td>
                </tr>
                <tr>
                  <td className="feature-name">Reply Classification</td>
                  <td>
                    <span className="col-muted">-</span>
                  </td>
                  <td>
                    <Check className="col-green" style={{ width: "16px", height: "16px", margin: "auto" }} />
                  </td>
                  <td>
                    <Check className="col-green" style={{ width: "16px", height: "16px", margin: "auto" }} />
                  </td>
                </tr>
                <tr>
                  <td className="feature-name">Memory Graph nodes</td>
                  <td>
                    <span className="col-muted">-</span>
                  </td>
                  <td>
                    <Check className="col-green" style={{ width: "16px", height: "16px", margin: "auto" }} />
                  </td>
                  <td>Dedicated cluster</td>
                </tr>
                <tr>
                  <td className="feature-name">Outbound Voice Calls</td>
                  <td>
                    <span className="col-muted">-</span>
                  </td>
                  <td>
                    <span className="col-muted">-</span>
                  </td>
                  <td>Add-on supported</td>
                </tr>
                <tr>
                  <td className="feature-name">API Integrations</td>
                  <td>
                    <span className="col-muted">-</span>
                  </td>
                  <td>Zapier &amp; Webhooks</td>
                  <td>Direct CRM Sync</td>
                </tr>
                <tr>
                  <td className="feature-name">Security Controls</td>
                  <td>Standard SSL</td>
                  <td>SOC2 compliance</td>
                  <td>Custom VPC isolation</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* Pricing FAQs Section */}
      <section className="pricing-faq-section">
        <div className="container">
          <div className="section-header text-center">
            <span className="section-tag">Common Inquiries</span>
            <h2 className="section-title">Frequently Asked Questions</h2>
            <p className="section-sub">Answers to help you guide your choice.</p>
          </div>

          <div className="faq-list">
            {/* FAQ Item 1 */}
            <div className={`faq-item card-glass ${activeFaq === 0 ? "active" : ""}`}>
              <button className="faq-question" onClick={() => toggleFaq(0)}>
                <span>How does the AI lead qualification engine score leads?</span>
                <ChevronDown className="faq-arrow" />
              </button>
              <div
                className="faq-answer"
                style={{
                  maxHeight: activeFaq === 0 ? "200px" : "0px",
                  transition: "max-height 0.4s ease",
                  overflow: "hidden",
                }}
              >
                <p>
                  LeadFlow AI reads the context parameters you input (such as CSV fields) and initiates
                  diagnostic web spiders to check public registers, domain metadata, speed logs, and mobile
                  alignment. It cross-references this with client criteria to calculate a qualification
                  confidence rating (HOT, WARM, COLD).
                </p>
              </div>
            </div>

            {/* FAQ Item 2 */}
            <div className={`faq-item card-glass ${activeFaq === 1 ? "active" : ""}`}>
              <button className="faq-question" onClick={() => toggleFaq(1)}>
                <span>Is there a setup fee or long-term contract?</span>
                <ChevronDown className="faq-arrow" />
              </button>
              <div
                className="faq-answer"
                style={{
                  maxHeight: activeFaq === 1 ? "200px" : "0px",
                  transition: "max-height 0.4s ease",
                  overflow: "hidden",
                }}
              >
                <p>
                  No. LeadFlow AI operates on a month-to-month subscription model. You can modify tiers,
                  upgrade representatives, or cancel billing anytime from your admin panel without fees. Annual
                  contracts are available with a 20% discount.
                </p>
              </div>
            </div>

            {/* FAQ Item 3 */}
            <div className={`faq-item card-glass ${activeFaq === 2 ? "active" : ""}`}>
              <button className="faq-question" onClick={() => toggleFaq(2)}>
                <span>Can I synchronize LeadFlow AI with my existing HubSpot or Salesforce CRM?</span>
                <ChevronDown className="faq-arrow" />
              </button>
              <div
                className="faq-answer"
                style={{
                  maxHeight: activeFaq === 2 ? "200px" : "0px",
                  transition: "max-height 0.4s ease",
                  overflow: "hidden",
                }}
              >
                <p>
                  Yes! Our Growth tier supports Zapier, Make, and webhook connections. The Enterprise tier
                  includes dedicated integration engineer assistance to set up direct pipeline synchronization,
                  mapping qualified conversations instantly.
                </p>
              </div>
            </div>

            {/* FAQ Item 4 */}
            <div className={`faq-item card-glass ${activeFaq === 3 ? "active" : ""}`}>
              <button className="faq-question" onClick={() => toggleFaq(3)}>
                <span>What happens if I exceed my monthly lead processing limits?</span>
                <ChevronDown className="faq-arrow" />
              </button>
              <div
                className="faq-answer"
                style={{
                  maxHeight: activeFaq === 3 ? "200px" : "0px",
                  transition: "max-height 0.4s ease",
                  overflow: "hidden",
                }}
              >
                <p>
                  If your outbound pipeline exceeds the active limit, your agents will hold further
                  qualifications. You can select single-month extra blocks ($15 per 500 leads) or upgrade to
                  higher capacity limits smoothly without losing existing memory logs.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="final-cta" id="get-started">
        <div className="cta-glow-bg"></div>
        <div className="container text-center">
          <div className="cta-box card-glass">
            <h2 className="cta-headline">Unlock Autonomous Outbound Growth.</h2>
            <p className="cta-sub">
              Set up your lead diagnostics, launch representatives, and book meetings in less than 10 minutes.
            </p>
            <div className="cta-actions">
              <Link href="/dashboard" className="btn btn-primary btn-lg">
                Start Free Trial
              </Link>
              <Link href="/dashboard" className="btn btn-secondary btn-lg" id="final-demo-btn">
                Contact Sales
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-grid">
            <div className="footer-info">
              <div className="logo">
                <img src="/logo.jpg" alt="LeadFlow Logo" className="logo-icon-small" />
                <span className="logo-text">LeadFlow AI</span>
              </div>
              <p className="footer-desc">
                Premium AI-native outbound qualification, diagnostic detection, and outreach systems.
              </p>
            </div>
            <div className="footer-nav">
              <div className="footer-col">
                <h4>Product</h4>
                <Link href="/#features">Features</Link>
                <Link href="/#showcase">Dashboard</Link>
                <Link href="/#roadmap">Labs Roadmap</Link>
              </div>
              <div className="footer-col">
                <h4>Technology</h4>
                <span className="nav-item-mock">AI Qualification</span>
                <span className="nav-item-mock">Reply Core</span>
                <span className="nav-item-mock">Data Privacy</span>
              </div>
              <div className="footer-col">
                <h4>Pricing</h4>
                <Link href="/pricing">Starter Agency</Link>
                <Link href="/pricing">Enterprise Custom</Link>
              </div>
              <div className="footer-col">
                <h4>Contact</h4>
                <span className="nav-item-mock">support@leadflow.ai</span>
                <span className="nav-item-mock">sales@leadflow.ai</span>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>© 2026 LeadFlow AI. All Rights Reserved.</p>
            <p>Built for elite sales agencies.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
