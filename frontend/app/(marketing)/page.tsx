"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import {
  Play,
  FileUp,
  CheckCircle2,
  ScanFace,
  Mail,
  MessageSquareCode,
  Calendar,
  Trophy,
  FileSpreadsheet,
  TableProperties,
  FormInput,
  MailWarning,
  FileText,
  Database,
  Cpu,
  ScanSearch,
  XCircle,
  ArrowDown,
  Sparkles,
  UserCheck,
  AlertTriangle,
  DollarSign,
  Clock,
  Network,
  BellRing,
  CheckSquare,
  Search,
  Edit3,
  BrainCircuit,
  AlarmClock,
  LayoutDashboard,
  LayoutGrid,
  Users,
  MessageSquare,
  Send,
  BarChart3,
  Settings,
  ChevronDown,
  ArrowUpRight,
  MessageCircle,
  Star,
  Target,
  Check,
  X,
  PlayCircle,
  PauseCircle,
  PhoneCall,
  TrendingUp,
  UsersRound,
  Landmark,
} from "lucide-react";

const STAGES = ["csv", "qualify", "pain-points", "outreach", "reply", "follow-up", "meeting"] as const;
type Stage = typeof STAGES[number];

export default function LandingPage() {
  // Showcase chart interaction state
  const [hoveredPoint, setHoveredPoint] = useState<{ x: number; y: number; week: string; value: string } | null>(null);

  // Demo Modal State
  const [isDemoModalOpen, setIsDemoModalOpen] = useState(false);
  const [demoPlaying, setDemoPlaying] = useState(false);
  const [demoSubtitleIdx, setDemoSubtitleIdx] = useState(0);

  // Pipeline Animation State
  const [activeStage, setActiveStage] = useState<Stage>("csv");
  const [stageStatus, setStageStatus] = useState<"processing" | "success">("processing");
  const [qualifyScore, setQualifyScore] = useState<number>(10);
  const [replyText, setReplyText] = useState<string>("Budget ✓");
  const [connectorActive, setConnectorActive] = useState<boolean[]>(new Array(6).fill(false));

  // Refs for Scrolltelling
  const scrollTrackRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // Statistics Counter Animation State
  const statsSectionRef = useRef<HTMLDivElement>(null);
  const [statsAnimated, setStatsAnimated] = useState(false);
  const [statLessWork, setStatLessWork] = useState(0);
  const [statFasterQual, setStatFasterQual] = useState(0);
  const [statFasterFollow, setStatFasterFollow] = useState(0);

  // 1. Pipeline Animation Loop
  useEffect(() => {
    let active = true;
    let currentIdx = 0;
    let timerId: NodeJS.Timeout;
    let animationInterval: NodeJS.Timeout;

    const durations: Record<Stage, number> = {
      csv: 1500,
      qualify: 1500,
      "pain-points": 1500,
      outreach: 1500,
      reply: 1500,
      "follow-up": 1500,
      meeting: 2500,
    };

    const runStep = () => {
      if (!active) return;

      const stage = STAGES[currentIdx];
      setActiveStage(stage);
      setStageStatus("processing");

      const duration = durations[stage];

      if (stage === "qualify") {
        let val = 10;
        animationInterval = setInterval(() => {
          val += 7;
          if (val > 91) val = 91;
          setQualifyScore(val);
        }, 100);
      } else if (stage === "reply") {
        const replies = ["Objection ✓", "Budget ✓", "Timeline ✓", "Meeting ✓"];
        let idx = 0;
        animationInterval = setInterval(() => {
          setReplyText(replies[idx % replies.length]);
          idx++;
        }, 300);
      }

      timerId = setTimeout(() => {
        if (animationInterval) clearInterval(animationInterval);
        setStageStatus("success");

        if (currentIdx < STAGES.length - 1) {
          setConnectorActive((prev) => {
            const next = [...prev];
            next[currentIdx] = true;
            return next;
          });

          timerId = setTimeout(() => {
            currentIdx++;
            runStep();
          }, 800);
        } else {
          timerId = setTimeout(() => {
            setConnectorActive(new Array(6).fill(false));
            setQualifyScore(10);
            setReplyText("Budget ✓");
            currentIdx = 0;
            runStep();
          }, duration);
        }
      }, duration);
    };

    runStep();

    return () => {
      active = false;
      clearTimeout(timerId);
      clearInterval(animationInterval);
    };
  }, []);

  // 2. Scrolltelling Scroll Logic
  useEffect(() => {
    const handleScroll = () => {
      const scrollTrack = scrollTrackRef.current;
      const scrollContainer = scrollContainerRef.current;
      if (!scrollTrack || !scrollContainer) return;

      const trackRect = scrollTrack.getBoundingClientRect();
      const trackTop = trackRect.top;
      const trackHeight = trackRect.height;

      const totalScrollable = trackHeight - window.innerHeight;
      let progress = -trackTop / totalScrollable;
      progress = Math.min(Math.max(progress, 0), 1);

      const totalScenes = 6;
      const sceneIndex = Math.min(Math.floor(progress * totalScenes), totalScenes - 1);
      const sceneProgress = progress * totalScenes - sceneIndex;

      // Update text scenes
      const textScenes = scrollContainer.querySelectorAll(".scene-text");
      textScenes.forEach((sceneText, idx) => {
        sceneText.classList.remove("active", "exit");
        if (idx === sceneIndex) {
          sceneText.classList.add("active");
        } else if (idx < sceneIndex) {
          sceneText.classList.add("exit");
        }
      });

      // Update visual scenes
      const visualScenes = scrollContainer.querySelectorAll(".scene-visual");
      visualScenes.forEach((sceneVis, idx) => {
        sceneVis.classList.remove("active");
        if (idx === sceneIndex) {
          sceneVis.classList.add("active");
        }
      });

      // Scene 1: Chaos Leads
      const chaosLeads = scrollContainer.querySelectorAll(".chaos-lead") as NodeListOf<HTMLElement>;
      const chaosCenterGlow = scrollContainer.querySelector(".chaos-center-glow") as HTMLElement;
      if (sceneIndex === 0) {
        if (chaosCenterGlow) {
          chaosCenterGlow.style.opacity = `${sceneProgress * 0.8}`;
          chaosCenterGlow.style.transform = `scale(${0.5 + sceneProgress * 1.5})`;
        }
        chaosLeads.forEach((lead, i) => {
          const initialX = parseFloat(lead.getAttribute("data-x") || "0");
          const initialY = parseFloat(lead.getAttribute("data-y") || "0");
          const initialR = parseFloat(lead.getAttribute("data-r") || "0");

          const currentX = initialX * (1 - sceneProgress);
          const currentY = initialY * (1 - sceneProgress);
          const currentR = initialR * (1 - sceneProgress);
          const scale = 1 - sceneProgress * 0.3;

          lead.style.transform = `translate(${currentX}px, ${currentY}px) rotate(${currentR}deg) scale(${scale})`;
          lead.style.opacity = `${1 - sceneProgress * 0.8}`;
        });
      } else {
        chaosLeads.forEach((lead) => {
          const initialX = lead.getAttribute("data-x") || "0";
          const initialY = lead.getAttribute("data-y") || "0";
          const initialR = lead.getAttribute("data-r") || "0";
          lead.style.transform = `translate(${initialX}px, ${initialY}px) rotate(${initialR}deg)`;
          lead.style.opacity = "1";
        });
        if (chaosCenterGlow) chaosCenterGlow.style.opacity = "0";
      }

      // Scene 2: AI Core Qualification
      const hotCard = scrollContainer.querySelector(".hot-card") as HTMLElement;
      const warmCard = scrollContainer.querySelector(".warm-card") as HTMLElement;
      const coldCard = scrollContainer.querySelector(".cold-card") as HTMLElement;

      if (sceneIndex === 1) {
        if (sceneProgress > 0.1) {
          const hotProgress = Math.min((sceneProgress - 0.1) / 0.4, 1);
          if (hotCard) {
            hotCard.style.transform = `translate(${hotProgress * 130}px, -${hotProgress * 110}px) scale(${0.6 + hotProgress * 0.4})`;
            hotCard.style.opacity = `${hotProgress}`;
          }
        } else if (hotCard) {
          hotCard.style.transform = "translate(0px, 0px) scale(0.6)";
          hotCard.style.opacity = "0";
        }

        if (sceneProgress > 0.3) {
          const warmProgress = Math.min((sceneProgress - 0.3) / 0.4, 1);
          if (warmCard) {
            warmCard.style.transform = `translate(${warmProgress * 160}px, 0px) scale(${0.6 + warmProgress * 0.4})`;
            warmCard.style.opacity = `${warmProgress}`;
          }
        } else if (warmCard) {
          warmCard.style.transform = "translate(0px, 0px) scale(0.6)";
          warmCard.style.opacity = "0";
        }

        if (sceneProgress > 0.5) {
          const coldProgress = Math.min((sceneProgress - 0.5) / 0.4, 1);
          if (coldCard) {
            coldCard.style.transform = `translate(${coldProgress * 130}px, ${coldProgress * 110}px) scale(${0.6 + coldProgress * 0.4})`;
            coldCard.style.opacity = `${coldProgress}`;
          }
        } else if (coldCard) {
          coldCard.style.transform = "translate(0px, 0px) scale(0.6)";
          coldCard.style.opacity = "0";
        }
      }

      // Scene 3: Diagnostics
      const laserLine = scrollContainer.querySelector(".scan-laser-line") as HTMLElement;
      const diagnosticItems = scrollContainer.querySelectorAll(".diagnostic-item");
      const diagnosticFooter = scrollContainer.querySelector(".diagnostic-footer") as HTMLElement;

      if (sceneIndex === 2) {
        if (laserLine) laserLine.classList.add("animating");

        if (sceneProgress > 0.1) diagnosticItems[0].classList.add("revealed");
        else diagnosticItems[0].classList.remove("revealed");

        if (sceneProgress > 0.3) diagnosticItems[1].classList.add("revealed");
        else diagnosticItems[1].classList.remove("revealed");

        if (sceneProgress > 0.5) diagnosticItems[2].classList.add("revealed");
        else diagnosticItems[2].classList.remove("revealed");

        if (sceneProgress > 0.7) {
          diagnosticItems[3].classList.add("revealed");
          if (diagnosticFooter) diagnosticFooter.classList.add("revealed");
        } else {
          diagnosticItems[3].classList.remove("revealed");
          if (diagnosticFooter) diagnosticFooter.classList.remove("revealed");
        }
      } else {
        if (laserLine) laserLine.classList.remove("animating");
        diagnosticItems.forEach((item) => item.classList.remove("revealed"));
        if (diagnosticFooter) diagnosticFooter.classList.remove("revealed");
      }

      // Scene 4: Typewriter Email
      const typedEmailSpan = scrollContainer.querySelector("#typed-email") as HTMLElement;
      const emailText = `Hi John,

I noticed Acme Corp's website speed is 6.4s, and you are missing active intake mechanisms. Let's fix this for Q3. We can build a bespoke high-performance funnel that converts.

Best,
LeadFlow AI`;
      if (sceneIndex === 3 && typedEmailSpan) {
        const charCount = Math.floor(sceneProgress * emailText.length);
        const visibleText = emailText.substring(0, charCount);
        typedEmailSpan.innerHTML = visibleText.replace(/\n/g, "<br>");
      }

      // Scene 5: Reply Intelligence
      const extractedProfile = scrollContainer.querySelector(".extracted-profile-card") as HTMLElement;
      if (sceneIndex === 4 && extractedProfile) {
        if (sceneProgress > 0.4) {
          extractedProfile.classList.add("active");
        } else {
          extractedProfile.classList.remove("active");
        }
      } else if (extractedProfile) {
        extractedProfile.classList.remove("active");
      }

      // Scene 6: Persistant Memory
      const followUpToast = scrollContainer.querySelector(".follow-up-toast") as HTMLElement;
      if (sceneIndex === 5 && followUpToast) {
        if (sceneProgress > 0.5) {
          followUpToast.classList.add("active");
        } else {
          followUpToast.classList.remove("active");
        }
      } else if (followUpToast) {
        followUpToast.classList.remove("active");
      }
    };

    window.addEventListener("scroll", handleScroll);
    handleScroll();

    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // 3. Feature Cards Glow Tracker
  const handleFeatureCardMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const card = e.currentTarget;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    card.style.setProperty("--mouse-x", `${x}px`);
    card.style.setProperty("--mouse-y", `${y}px`);
  };

  // 4. Statistics Counters Observer
  useEffect(() => {
    const section = statsSectionRef.current;
    if (!section) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !statsAnimated) {
            setStatsAnimated(true);
            animateStats();
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.3 }
    );

    observer.observe(section);

    const animateStats = () => {
      const duration = 1500;
      const startTime = performance.now();

      const run = (currentTime: number) => {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const ease = progress * (2 - progress); // easeOutQuad

        setStatLessWork(Math.floor(ease * 80));
        setStatFasterQual(Math.floor(ease * 3));
        setStatFasterFollow(Math.floor(ease * 50));

        if (progress < 1) {
          requestAnimationFrame(run);
        } else {
          setStatLessWork(80);
          setStatFasterQual(3);
          setStatFasterFollow(50);
        }
      };

      requestAnimationFrame(run);
    };

    return () => observer.disconnect();
  }, [statsAnimated]);

  // 5. Watch Demo Modal Subtitle loop
  useEffect(() => {
    if (!isDemoModalOpen) return;

    const subtitles = [
      "LeadFlow AI loads leads from lists, registers, or inbound forms...",
      "The Diagnostic Engine instantly profiles technical errors & SEO bugs...",
      "Our generative models build dynamic outreach for their specific defects...",
      "Reply Intelligence parses incoming queries to pull budget, dates, and actions...",
      "Lead Memory links records securely and triggers automated pipeline sequences...",
    ];

    const timer = setInterval(() => {
      setDemoSubtitleIdx((prev) => (prev + 1) % subtitles.length);
    }, 3500);

    return () => clearInterval(timer);
  }, [isDemoModalOpen]);

  const demoSubtitles = [
    "LeadFlow AI loads leads from lists, registers, or inbound forms...",
    "The Diagnostic Engine instantly profiles technical errors & SEO bugs...",
    "Our generative models build dynamic outreach for their specific defects...",
    "Reply Intelligence parses incoming queries to pull budget, dates, and actions...",
    "Lead Memory links records securely and triggers automated pipeline sequences...",
  ];

  const handleChartInteraction = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const percentX = clickX / rect.width;
    const svgX = percentX * 300; // viewBox width is 300

    const points = [
      { x: 80, y: 50, week: "Week 1", value: "18.2%" },
      { x: 150, y: 40, week: "Week 2", value: "20.1%" },
      { x: 220, y: 20, week: "Week 3", value: "22.8%" },
      { x: 300, y: 10, week: "Week 4", value: "24.6%" }
    ];

    let closest = points[0];
    let minDiff = Math.abs(svgX - points[0].x);

    for (let i = 1; i < points.length; i++) {
      const diff = Math.abs(svgX - points[i].x);
      if (diff < minDiff) {
        minDiff = diff;
        closest = points[i];
      }
    }

    setHoveredPoint(closest);
  };

  return (
    <div ref={scrollContainerRef}>
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
            <a href="#features">Features</a>
            <a href="#showcase">Dashboard</a>
            <a href="#roadmap">Roadmap</a>
            <Link href="/pricing">Pricing</Link>
          </nav>
          <div className="nav-actions">
            <button
              onClick={() => setIsDemoModalOpen(true)}
              className="btn btn-secondary btn-sm"
              id="nav-demo-btn"
            >
              Watch Demo
            </button>
            <Link href="/dashboard" className="btn btn-primary btn-sm" id="nav-cta-btn">
              Get Started
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-bg-glow"></div>
        <div className="hero-container">
          <h1 className="hero-headline">
            Transform Raw Leads Into <br />
            <span className="gradient-text">Qualified Sales Conversations</span>
          </h1>
          <p className="hero-subheadline">
            LeadFlow AI automatically qualifies leads, generates personalized outreach, analyzes replies,
            and manages follow-ups so your team can focus on closing deals.
          </p>

          <div className="hero-ctas">
            <Link href="/dashboard" className="btn btn-primary btn-lg">
              Get Started
            </Link>
            <button
              onClick={() => setIsDemoModalOpen(true)}
              className="btn btn-secondary btn-lg"
              id="hero-demo-btn"
            >
              <Play className="icon-play" style={{ width: "16px", height: "16px" }} /> Watch Demo
            </button>
          </div>

          {/* Hero Visual: Animated AI Pipeline */}
          <div className="hero-pipeline-wrapper">
            <div className="pipeline-title">Continuous AI Sales Operations Pipeline</div>
            <div className="pipeline-container">
              {/* Node 1: CSV Upload */}
              <div
                className={`pipeline-node ${activeStage === "csv" ? "active" : ""} ${
                  activeStage === "csv" && stageStatus === "processing" ? "processing" : ""
                } ${
                  STAGES.indexOf(activeStage) > 0 || (activeStage === "csv" && stageStatus === "success")
                    ? "success"
                    : ""
                }`}
                data-stage="csv"
              >
                <div className="node-icon-wrapper">
                  <FileUp />
                </div>
                <span className="node-label">CSV Upload</span>
                <div className="node-status"></div>
                <div className="node-mini-progress">
                  <div
                    className="progress-fill"
                    style={{
                      width:
                        activeStage === "csv" && stageStatus === "processing"
                          ? "100%"
                          : STAGES.indexOf(activeStage) > 0
                          ? "100%"
                          : "0%",
                      transition: activeStage === "csv" && stageStatus === "processing" ? "width 1.5s linear" : "none",
                    }}
                  ></div>
                </div>
              </div>

              <div className={`pipeline-connector ${connectorActive[0] ? "active" : ""}`}>
                <div className="connector-pulse"></div>
              </div>

              {/* Node 2: AI Qualification */}
              <div
                className={`pipeline-node ${activeStage === "qualify" ? "active" : ""} ${
                  activeStage === "qualify" && stageStatus === "processing" ? "processing" : ""
                } ${
                  STAGES.indexOf(activeStage) > 1 || (activeStage === "qualify" && stageStatus === "success")
                    ? "success"
                    : ""
                }`}
                data-stage="qualify"
              >
                <div className="node-icon-wrapper">
                  <CheckCircle2 />
                </div>
                <span className="node-label">AI Qualification</span>
                <div className="node-status"></div>
                <div className="node-readout" id="pipe-score-readout">
                  {activeStage === "qualify" ? `${qualifyScore} HOT` : STAGES.indexOf(activeStage) > 1 ? "91 HOT" : "-- WARM"}
                </div>
              </div>

              <div className={`pipeline-connector ${connectorActive[1] ? "active" : ""}`}>
                <div className="connector-pulse"></div>
              </div>

              {/* Node 3: Pain Detection */}
              <div
                className={`pipeline-node ${activeStage === "pain-points" ? "active" : ""} ${
                  activeStage === "pain-points" && stageStatus === "processing" ? "processing" : ""
                } ${
                  STAGES.indexOf(activeStage) > 2 || (activeStage === "pain-points" && stageStatus === "success")
                    ? "success"
                    : ""
                }`}
                data-stage="pain-points"
              >
                <div className="node-icon-wrapper">
                  <ScanFace />
                </div>
                <span className="node-label">Pain Detection</span>
                <div className="node-status"></div>
                <div className={`node-scanner-beam ${activeStage === "pain-points" && stageStatus === "processing" ? "animating" : ""}`}></div>
              </div>

              <div className={`pipeline-connector ${connectorActive[2] ? "active" : ""}`}>
                <div className="connector-pulse"></div>
              </div>

              {/* Node 4: Personalized Outreach */}
              <div
                className={`pipeline-node ${activeStage === "outreach" ? "active" : ""} ${
                  activeStage === "outreach" && stageStatus === "processing" ? "processing" : ""
                } ${
                  STAGES.indexOf(activeStage) > 3 || (activeStage === "outreach" && stageStatus === "success")
                    ? "success"
                    : ""
                }`}
                data-stage="outreach"
              >
                <div className="node-icon-wrapper">
                  <Mail />
                </div>
                <span className="node-label">Personalized Outreach</span>
                <div className="node-status"></div>
                <div className="node-typing-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>

              <div className={`pipeline-connector ${connectorActive[3] ? "active" : ""}`}>
                <div className="connector-pulse"></div>
              </div>

              {/* Node 5: Reply Intelligence */}
              <div
                className={`pipeline-node ${activeStage === "reply" ? "active" : ""} ${
                  activeStage === "reply" && stageStatus === "processing" ? "processing" : ""
                } ${
                  STAGES.indexOf(activeStage) > 4 || (activeStage === "reply" && stageStatus === "success")
                    ? "success"
                    : ""
                }`}
                data-stage="reply"
              >
                <div className="node-icon-wrapper">
                  <MessageSquareCode />
                </div>
                <span className="node-label">Reply Intelligence</span>
                <div className="node-status"></div>
                <div className="node-readout" id="pipe-reply-readout">
                  {replyText}
                </div>
              </div>

              <div className={`pipeline-connector ${connectorActive[4] ? "active" : ""}`}>
                <div className="connector-pulse"></div>
              </div>

              {/* Node 6: Follow-Up Automation */}
              <div
                className={`pipeline-node ${activeStage === "follow-up" ? "active" : ""} ${
                  activeStage === "follow-up" && stageStatus === "processing" ? "processing" : ""
                } ${
                  STAGES.indexOf(activeStage) > 5 || (activeStage === "follow-up" && stageStatus === "success")
                    ? "success"
                    : ""
                }`}
                data-stage="follow-up"
              >
                <div className="node-icon-wrapper">
                  <Calendar />
                </div>
                <span className="node-label">Follow-Up Automation</span>
                <div className="node-status"></div>
                <div className={`node-clock-hand ${activeStage === "follow-up" && stageStatus === "processing" ? "spinning" : ""}`}></div>
              </div>

              <div className={`pipeline-connector ${connectorActive[5] ? "active" : ""}`}>
                <div className="connector-pulse"></div>
              </div>

              {/* Node 7: Meeting Scheduled */}
              <div
                className={`pipeline-node highlight ${activeStage === "meeting" ? "active" : ""} ${
                  activeStage === "meeting" && stageStatus === "processing" ? "processing" : ""
                } ${
                  activeStage === "meeting" && stageStatus === "success" ? "success" : ""
                }`}
                data-stage="meeting"
              >
                <div className="node-icon-wrapper">
                  <Trophy />
                </div>
                <span className="node-label">Meeting Scheduled</span>
                <div className="node-status bg-accent-glow"></div>
                <div className="node-glow-burst"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Scrolltelling Track */}
      <div className="scrolltelling-track" id="scroll-track" ref={scrollTrackRef}>
        <div className="scrolltelling-sticky">
          {/* Left side: Text descriptions */}
          <div className="scenes-text-container">
            <div className="scene-text active" id="scene-text-1" data-scene="1">
              <span className="scene-badge">Scene 1 / 6: The Problem</span>
              <h2 className="scene-title">Leads are everywhere.</h2>
              <p className="scene-desc">
                Most agencies lose opportunities because their sales process is fragmented. Raw leads sit
                scattered across unsorted CSV files, spreadsheets, WebForms, and legacy emails.
              </p>
            </div>

            <div className="scene-text" id="scene-text-2" data-scene="2">
              <span className="scene-badge">Scene 2 / 6: Qualification</span>
              <h2 className="scene-title">AI identifies your best opportunities.</h2>
              <p className="scene-desc">
                Raw files compile into our central AI Core. LeadFlow automatically processes company data,
                industry parameters, and business size, qualifying leads and scoring them instantly.
              </p>
            </div>

            <div className="scene-text" id="scene-text-3" data-scene="3">
              <span className="scene-badge">Scene 3 / 6: Diagnostics</span>
              <h2 className="scene-title">Find opportunities before your competitors.</h2>
              <p className="scene-desc">
                The engine diagnostics scan each prospect's public digital footprint. LeadFlow AI surfaces
                active website issues, SEO gaps, missing lead forms, and brand presence shortcomings.
              </p>
            </div>

            <div className="scene-text" id="scene-text-4" data-scene="4">
              <span className="scene-badge">Scene 4 / 6: Outreach</span>
              <h2 className="scene-title">Every message feels personal.</h2>
              <p className="scene-desc">
                No templates. Our AI dynamically generates outreach copy addressing the specific diagnosed
                pain point. Instantly produce bespoke context-rich emails tailored to the recipient's role.
              </p>
            </div>

            <div className="scene-text" id="scene-text-5" data-scene="5">
              <span className="scene-badge">Scene 5 / 6: Analysis</span>
              <h2 className="scene-title">AI understands every conversation.</h2>
              <p className="scene-desc">
                When prospects reply, our Reply Intelligence extracts crucial attributes: budget limits,
                timelines, underlying requirements, and objections, organizing them in real-time.
              </p>
            </div>

            <div className="scene-text" id="scene-text-6" data-scene="6">
              <span className="scene-badge">Scene 6 / 6: Persistent Memory</span>
              <h2 className="scene-title">Your AI never forgets a lead.</h2>
              <p className="scene-desc">
                All details populate a persistent Semantic Memory Graph. Relational nodes connect budgets,
                objections, and next actions to trigger automated follow-ups, keeping the sales loop running
                24/7.
              </p>
            </div>
          </div>

          {/* Right side: Visual canvas */}
          <div className="scenes-visual-container">
            {/* Scene 1 Visual */}
            <div className="scene-visual active" id="scene-vis-1" data-scene="1">
              <div className="chaos-lead card-glass" data-x="-120" data-y="-80" data-r="-12" style={{ left: "50%", top: "50%" }}>
                <FileSpreadsheet className="col-green" /> <span>leads_export_q2.csv</span>
              </div>
              <div className="chaos-lead card-glass" data-x="130" data-y="-110" data-r="8" style={{ left: "50%", top: "50%" }}>
                <TableProperties className="col-blue" /> <span>Google Sheet (Shared)</span>
              </div>
              <div className="chaos-lead card-glass" data-x="-150" data-y="100" data-r="-8" style={{ left: "50%", top: "50%" }}>
                <FormInput className="col-cyan" /> <span>Contact Form #4</span>
              </div>
              <div className="chaos-lead card-glass" data-x="120" data-y="90" data-r="15" style={{ left: "50%", top: "50%" }}>
                <MailWarning className="col-purple" /> <span>Inbound Request</span>
              </div>
              <div className="chaos-lead card-glass" data-x="0" data-y="-160" data-r="-3" style={{ left: "50%", top: "50%" }}>
                <FileText className="col-red" /> <span>outbox_leads_list</span>
              </div>
              <div className="chaos-lead card-glass" data-x="-20" data-y="150" data-r="5" style={{ left: "50%", top: "50%" }}>
                <Database className="col-orange" /> <span>Backup_CRM_final</span>
              </div>
              <div className="chaos-center-glow"></div>
            </div>

            {/* Scene 2 Visual */}
            <div className="scene-visual" id="scene-vis-2" data-scene="2">
              <div className="ai-core-hub">
                <div className="ai-core-ring ring-1"></div>
                <div className="ai-core-ring ring-2"></div>
                <div className="ai-core-ring ring-3"></div>
                <div className="ai-core-center">
                  <Cpu className="ai-core-icon" />
                </div>
              </div>

              <div className="qualify-lead-card card-glass hot-card" style={{ left: "50%", top: "50%", marginLeft: "-110px", marginTop: "-35px" }}>
                <div className="qualify-header">
                  <span className="q-name">Acme Corp</span>
                  <span className="q-badge hot">91 HOT</span>
                </div>
                <div className="q-details">SaaS Agency • $10M Revenue</div>
              </div>

              <div className="qualify-lead-card card-glass warm-card" style={{ left: "50%", top: "50%", marginLeft: "-110px", marginTop: "-35px" }}>
                <div className="qualify-header">
                  <span className="q-name">Apex Global</span>
                  <span className="q-badge warm">74 WARM</span>
                </div>
                <div className="q-details">E-commerce • $2.5M Revenue</div>
              </div>

              <div className="qualify-lead-card card-glass cold-card" style={{ left: "50%", top: "50%", marginLeft: "-110px", marginTop: "-35px" }}>
                <div className="qualify-header">
                  <span className="q-name">Local Bistro</span>
                  <span className="q-badge cold">35 COLD</span>
                </div>
                <div className="q-details">Restaurant • $200k Revenue</div>
              </div>
            </div>

            {/* Scene 3 Visual */}
            <div className="scene-visual" id="scene-vis-3" data-scene="3">
              <div className="diagnostic-card card-glass">
                <div className="diagnostic-header">
                  <ScanSearch className="col-cyan" />
                  <span>AI Diagnostic Engine</span>
                  <span className="status-scanning">SCANNING ACTIVE</span>
                </div>
                <div className="diagnostic-lead-name">Acme Corp Digital Assets</div>

                <div className="diagnostic-scan-container">
                  <div className="diagnostic-item error">
                    <XCircle />
                    <div className="diag-detail">
                      <strong>Website Load Speed</strong>
                      <span>6.4s response time (Failed)</span>
                    </div>
                  </div>
                  <div className="diagnostic-item error">
                    <XCircle />
                    <div className="diag-detail">
                      <strong>SEO Configuration</strong>
                      <span>Missing canonical references, metadata sparse</span>
                    </div>
                  </div>
                  <div className="diagnostic-item success">
                    <CheckCircle2 />
                    <div className="diag-detail">
                      <strong>SSL Certificate</strong>
                      <span>Valid secure HTTPS (Passed)</span>
                    </div>
                  </div>
                  <div className="diagnostic-item error">
                    <XCircle />
                    <div className="diag-detail">
                      <strong>Lead Capture Mechanics</strong>
                      <span>No visible CTAs or active intake structures</span>
                    </div>
                  </div>

                  <div className="scan-laser-line"></div>
                </div>

                <div className="diagnostic-footer">
                  <span className="footer-label">SUGGESTED ANGLE:</span>
                  <span className="angle-text">
                    &quot;Website performance optimization &amp; High-conversion landing funnel bundle&quot;
                  </span>
                </div>
              </div>
            </div>

            {/* Scene 4 Visual */}
            <div className="scene-visual" id="scene-vis-4" data-scene="4">
              <div className="email-terminal card-glass" style={{ width: "420px" }}>
                <div className="terminal-bar">
                  <div className="dot red"></div>
                  <div className="dot yellow"></div>
                  <div className="dot green"></div>
                  <div className="terminal-title">outreach_generator.sh</div>
                </div>
                <div className="terminal-meta">
                  <div>
                    <strong>To:</strong> john@acmecorp.com
                  </div>
                  <div>
                    <strong>Subject:</strong> AI analysis of Acme Corp&apos;s conversion pipeline
                  </div>
                </div>
                <div className="terminal-body" style={{ minHeight: "150px" }}>
                  <span id="typed-email"></span>
                  <span className="terminal-cursor">|</span>
                </div>
              </div>
            </div>

            {/* Scene 5 Visual */}
            <div className="scene-visual" id="scene-vis-5" data-scene="5">
              {/* Inbound Reply */}
              <div className="reply-bubble card-glass" style={{ width: "360px", transform: "translateY(-80px)" }}>
                <div className="reply-header">
                  <div className="avatar">J</div>
                  <div className="reply-meta">
                    <strong>John Doe (Acme Corp)</strong>
                    <span>Received: 2 minutes ago</span>
                  </div>
                </div>
                <div className="reply-content">
                  &quot;Hi, saw your analysis on our checkout flow. That speed diagnostic is spot on. We
                  want to fix this by Q3. Budget is around $8k. Do you have slots next Tuesday at 3 PM EST for
                  a call?&quot;
                </div>
              </div>

              <ArrowDown className="extractor-arrow" style={{ position: "absolute", zIndex: 10, width: "24px", height: "24px" }} />

              {/* Extracted Profile */}
              <div className="extracted-profile-card card-glass" style={{ width: "380px", transform: "translateY(80px)" }}>
                <div className="profile-title">
                  <Sparkles /> Reply Analysis Insights
                </div>
                <div className="profile-grid">
                  <div className="profile-field">
                    <span className="field-label">Budget Range</span>
                    <span className="field-value badge-glow col-cyan">$8,000</span>
                  </div>
                  <div className="profile-field">
                    <span className="field-label">Target Timeline</span>
                    <span className="field-value badge-glow col-green">Q3 Implementation</span>
                  </div>
                  <div className="profile-field">
                    <span className="field-label">Sentiment</span>
                    <span className="field-value badge-glow col-purple">Highly Interested</span>
                  </div>
                  <div className="profile-field">
                    <span className="field-label">Objection</span>
                    <span className="field-value badge-glow col-red">None Detected</span>
                  </div>
                </div>
                <div className="profile-action">
                  <span className="action-label">Next Best Action:</span>
                  <span className="action-value">Auto-book Calendar: Tuesday 3:00 PM EST</span>
                </div>
              </div>
            </div>

            {/* Scene 6 Visual */}
            <div className="scene-visual" id="scene-vis-6" data-scene="6">
              <div className="memory-graph-canvas" style={{ position: "relative", width: "380px", height: "280px" }}>
                <svg className="graph-svg" width="380" height="280">
                  <line x1="190" y1="140" x2="60" y2="70" className="graph-line"></line>
                  <line x1="190" y1="140" x2="320" y2="70" className="graph-line"></line>
                  <line x1="190" y1="140" x2="70" y2="210" className="graph-line"></line>
                  <line x1="190" y1="140" x2="310" y2="210" className="graph-line"></line>
                </svg>

                <div className="graph-node node-center" style={{ left: "190px", top: "140px" }}>
                  <UserCheck />
                  <span className="node-tooltip">John Doe</span>
                </div>
                <div className="graph-node node-sub" style={{ left: "60px", top: "70px" }}>
                  <AlertTriangle className="col-red" />
                  <span className="node-tooltip">Site Speed</span>
                </div>
                <div className="graph-node node-sub" style={{ left: "320px", top: "70px" }}>
                  <DollarSign className="col-cyan" />
                  <span className="node-tooltip">$8,000</span>
                </div>
                <div className="graph-node node-sub" style={{ left: "70px", top: "210px" }}>
                  <Clock className="col-purple" />
                  <span className="node-tooltip">Tuesday Call</span>
                </div>
                <div className="graph-node node-sub" style={{ left: "310px", top: "210px" }}>
                  <Network className="col-blue" />
                  <span className="node-tooltip">Acme Corp</span>
                </div>

                <div className="follow-up-toast card-glass">
                  <BellRing className="pulse-icon col-cyan" />
                  <div>
                    <strong>Automated Follow-Up Sent</strong>
                    <span>Confirming Tuesday invite in John&apos;s calendar.</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Final Hero Transformation Section */}
      <section className="transformation-section">
        <div className="container text-center">
          <span className="section-tag">Unified Operations</span>
          <h2 className="transformation-headline">The future of sales operations.</h2>
          <p className="transformation-sub">
            Every lead, analysis, outbound communication, and schedule structured within a single command
            center. Stop jumping between fragmented apps.
          </p>

          <div className="dashboard-pipeline-preview card-glass">
            <div className="dashboard-inner-header">
              <div className="db-title-group">
                <span className="db-dot"></span>
                <span className="db-dot"></span>
                <span className="db-dot"></span>
                <span className="db-window-title">LeadFlow Dashboard — Unified View</span>
              </div>
              <div className="db-header-actions">
                <span className="db-pill">
                  <Calendar style={{ width: "14px", height: "14px", marginRight: "4px" }} /> Tuesday Call Scheduled
                </span>
              </div>
            </div>

            {/* Live widgets */}
            <div className="db-widgets">
              <div className="db-widget">
                <span className="w-lbl">Total Leads</span>
                <span className="w-val">2,482</span>
                <span className="w-change plus">+12.4%</span>
              </div>
              <div className="db-widget">
                <span className="w-lbl">Hot Leads</span>
                <span className="w-val">312</span>
                <span className="w-change plus">+28.1%</span>
              </div>
              <div className="db-widget">
                <span className="w-lbl">Emails Sent</span>
                <span className="w-val">1,829</span>
                <span className="w-change plus">+5.3%</span>
              </div>
              <div className="db-widget">
                <span className="w-lbl">Replies</span>
                <span className="w-val">492</span>
                <span className="w-change plus">+14.2%</span>
              </div>
              <div className="db-widget">
                <span className="w-lbl">Meetings</span>
                <span className="w-val">87</span>
                <span className="w-change plus">+32.0%</span>
              </div>
              <div className="db-widget">
                <span className="w-lbl">Conversions</span>
                <span className="w-val">12.8%</span>
                <span className="w-change plus">+2.4%</span>
              </div>
            </div>

            {/* Kanban board pipeline */}
            <div className="kanban-pipeline-wrapper">
              <div className="kanban-col">
                <div className="col-head">
                  New <span className="badge">12</span>
                </div>
                <div className="kanban-card">
                  <span className="card-name">TechCorp</span>
                  <span className="card-desc">Inbound Form</span>
                  <span className="card-score cold">32</span>
                </div>
                <div className="kanban-card">
                  <span className="card-name">Delta Inc</span>
                  <span className="card-desc">CSV Import</span>
                  <span className="card-score warm">58</span>
                </div>
              </div>
              <div className="kanban-col">
                <div className="col-head">
                  Qualified <span className="badge">8</span>
                </div>
                <div className="kanban-card">
                  <span className="card-name">Alpha Media</span>
                  <span className="card-desc">SaaS Dev Agency</span>
                  <span className="card-score hot">88</span>
                </div>
              </div>
              <div className="kanban-col">
                <div className="col-head">
                  Pitched <span className="badge">14</span>
                </div>
                <div className="kanban-card">
                  <span className="card-name">Nova Studio</span>
                  <span className="card-desc">Outbound Sent</span>
                  <span className="card-score hot">90</span>
                </div>
                <div className="kanban-card">
                  <span className="card-name">Scale Digital</span>
                  <span className="card-desc">Pain Pitch</span>
                  <span className="card-score warm">76</span>
                </div>
              </div>
              <div className="kanban-col">
                <div className="col-head">
                  Replied <span className="badge">6</span>
                </div>
                <div className="kanban-card highlight-glow">
                  <span className="card-name">Acme Corp</span>
                  <span className="card-desc">Interested (Reply Q3)</span>
                  <span className="card-score hot">91</span>
                </div>
              </div>
              <div className="kanban-col">
                <div className="col-head">
                  Meeting Needed <span className="badge">2</span>
                </div>
                <div className="kanban-card">
                  <span className="card-name">Zeta Logistics</span>
                  <span className="card-desc">Invite Sent</span>
                  <span className="card-score hot">94</span>
                </div>
              </div>
              <div className="kanban-col">
                <div className="col-head">
                  Won <span className="badge">48</span>
                </div>
                <div className="kanban-card won">
                  <span className="card-name">Vortex Co</span>
                  <span className="card-desc">Contract Signed</span>
                  <span className="card-badge-won">WON</span>
                </div>
              </div>
            </div>
          </div>

          <div className="trans-cta">
            <Link href="/dashboard" className="btn btn-primary btn-lg">
              Start Using LeadFlow AI
            </Link>
          </div>
        </div>
      </section>

      {/* Feature Grid Section */}
      <section className="features-section" id="features">
        <div className="container">
          <div className="section-header text-center">
            <span className="section-tag">System Capabilities</span>
            <h2 className="section-title">Designed for enterprise sales teams.</h2>
            <p className="section-sub">
              A full-cycle outbound operations framework inside one clean system.
            </p>
          </div>

          <div className="features-grid">
            <div className="feature-card" onMouseMove={handleFeatureCardMouseMove}>
              <div className="feature-card-glow"></div>
              <div className="feature-icon">
                <CheckSquare />
              </div>
              <h3 className="feature-title">AI Lead Qualification</h3>
              <p className="feature-desc">
                Classify and enrich thousands of leads in minutes. Evaluate relevance, revenue capacity, and
                buying intent accurately.
              </p>
            </div>

            <div className="feature-card" onMouseMove={handleFeatureCardMouseMove}>
              <div className="feature-card-glow"></div>
              <div className="feature-icon">
                <Search style={{ width: "20px", height: "20px" }} />
              </div>
              <h3 className="feature-title">Pain Point Detection</h3>
              <p className="feature-desc">
                Scan corporate websites, domains, and SEO metadata to uncover technological weaknesses and
                direct pitch angles.
              </p>
            </div>

            <div className="feature-card" onMouseMove={handleFeatureCardMouseMove}>
              <div className="feature-card-glow"></div>
              <div className="feature-icon">
                <Edit3 />
              </div>
              <h3 className="feature-title">Personalized Outreach</h3>
              <p className="feature-desc">
                Instantly create highly custom copy detailing how you can solve their exact pain points. No
                templates used.
              </p>
            </div>

            <div className="feature-card" onMouseMove={handleFeatureCardMouseMove}>
              <div className="feature-card-glow"></div>
              <div className="feature-icon">
                <BrainCircuit />
              </div>
              <h3 className="feature-title">Reply Intelligence</h3>
              <p className="feature-desc">
                Categorize incoming emails by purchase timeline, budget availability, specific demands, and
                potential objections.
              </p>
            </div>

            <div className="feature-card" onMouseMove={handleFeatureCardMouseMove}>
              <div className="feature-card-glow"></div>
              <div className="feature-icon">
                <Network />
              </div>
              <h3 className="feature-title">Lead Memory</h3>
              <p className="feature-desc">
                Retain structured histories of prior dialogues, target budgets, obstacles, and next steps
                in a secure semantic graph.
              </p>
            </div>

            <div className="feature-card" onMouseMove={handleFeatureCardMouseMove}>
              <div className="feature-card-glow"></div>
              <div className="feature-icon">
                <AlarmClock />
              </div>
              <h3 className="feature-title">Follow-Up Automation</h3>
              <p className="feature-desc">
                Trigger custom messages based on the exact elapsed time and previous interactions without
                human intervention.
              </p>
            </div>

            <div className="feature-card full-width-card" onMouseMove={handleFeatureCardMouseMove}>
              <div className="feature-card-glow"></div>
              <div className="feature-icon">
                <LayoutDashboard />
              </div>
              <div className="full-card-content">
                <h3 className="feature-title">Pipeline Dashboard</h3>
                <p className="feature-desc">
                  Track conversion KPIs, lead counts, and appointment status live on a clean dashboard
                  tailored for sales leadership.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof Section */}
      <section className="social-proof-section" ref={statsSectionRef}>
        <div className="container">
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-value">{statLessWork}%</div>
              <div className="stat-label">Less Manual Work</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{statFasterQual}x</div>
              <div className="stat-label">Faster Qualification</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{statFasterFollow}%</div>
              <div className="stat-label">Faster Follow-Ups</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">24/7</div>
              <div className="stat-label">AI Sales Assistant</div>
            </div>
          </div>
        </div>
      </section>

      {/* Dashboard Showcase Section */}
      <section className="showcase-section" id="showcase">
        <div className="container">
          <div className="section-header text-center">
            <span className="section-tag">Interactive Interface</span>
            <h2 className="section-title">The LeadFlow AI Platform Showcase</h2>
            <p className="section-sub">
              Take control of your entire sales pipeline. Explore dynamic dashboard analytics, real-time
              insights, and automated activity tracking.
            </p>
          </div>

          {/* High fidelity mockup showcase */}
          <div className="showcase-mockup-wrapper card-glass">
            {/* Left Sidebar */}
            <div className="showcase-sidebar">
              <div className="sidebar-logo">
                <img src="/logo.jpg" alt="LeadFlow Logo" className="logo-icon-small" />
                <span>LeadFlow</span>
              </div>
              <div className="sidebar-menu">
                <div className="menu-item active">
                  <LayoutGrid /> <span>Dashboard</span>
                </div>
                <div className="menu-item">
                  <Users /> <span>Leads</span>
                </div>
                <div className="menu-item">
                  <MessageSquare /> <span>Conversations</span>
                </div>
                <div className="menu-item">
                  <Send /> <span>Campaigns</span>
                </div>
                <div className="menu-item">
                  <BarChart3 /> <span>Analytics</span>
                </div>
                <div className="menu-item">
                  <Settings /> <span>Settings</span>
                </div>
              </div>
            </div>

            {/* Main Content Showcase */}
            <div className="showcase-main">
              {/* Inner Navigation */}
              <div className="showcase-inner-nav">
                <h3 className="inner-nav-title">Dashboard Overview</h3>
                <div className="inner-nav-actions">
                  <span className="date-picker-mock">
                    <Calendar style={{ width: "14px", height: "14px", marginRight: "4px" }} /> This Month{" "}
                    <ChevronDown style={{ width: "14px", height: "14px", marginLeft: "4px" }} />
                  </span>
                </div>
              </div>

              {/* Key Metrics Grid */}
              <div className="showcase-metrics">
                <div className="metric-card">
                  <div className="m-card-header">
                    <span className="m-lbl">Total Leads</span>
                    <Users className="col-blue" />
                  </div>
                  <span className="m-val">1,248</span>
                  <span className="m-sub plus">
                    <ArrowUpRight style={{ width: "14px", height: "14px", marginRight: "2px" }} /> 18.6% vs
                    last month
                  </span>
                </div>

                <div className="metric-card">
                  <div className="m-card-header">
                    <span className="m-lbl">Qualified Leads</span>
                    <CheckCircle2 className="col-green" />
                  </div>
                  <span className="m-val">312</span>
                  <span className="m-sub plus">
                    <ArrowUpRight style={{ width: "14px", height: "14px", marginRight: "2px" }} /> 21.3% vs
                    last month
                  </span>
                </div>

                <div className="metric-card">
                  <div className="m-card-header">
                    <span className="m-lbl">Conversations</span>
                    <MessageCircle className="col-purple" />
                  </div>
                  <span className="m-val">128</span>
                  <span className="m-sub plus">
                    <ArrowUpRight style={{ width: "14px", height: "14px", marginRight: "2px" }} /> 15.7% vs
                    last month
                  </span>
                </div>

                <div className="metric-card">
                  <div className="m-card-header">
                    <span className="m-lbl">Conversion Rate</span>
                    <Target className="col-orange" />
                  </div>
                  <span className="m-val">24.6%</span>
                  <span className="m-sub plus">
                    <ArrowUpRight style={{ width: "14px", height: "14px", marginRight: "2px" }} /> 6.4% vs last
                    month
                  </span>
                </div>
              </div>

              {/* Mid Section Content */}
              <div className="showcase-split-grid">
                {/* Recent activity & channels */}
                <div className="split-column left-split card-glass-dark">
                  <h4 className="column-title">Recent Pipeline Activity</h4>
                  <div className="activity-timeline">
                    <div className="activity-item">
                      <div className="act-icon bg-blue">
                        <Send style={{ width: "14px", height: "14px" }} />
                      </div>
                      <div className="act-details">
                        <p>AI outreach email delivered to 45 hot SaaS prospects</p>
                        <span>2 mins ago</span>
                      </div>
                    </div>
                    <div className="activity-item">
                      <div className="act-icon bg-green">
                        <Check style={{ width: "14px", height: "14px" }} />
                      </div>
                      <div className="act-details">
                        <p>12 leads qualified automatically by Diagnostic Engine</p>
                        <span>15 mins ago</span>
                      </div>
                    </div>
                    <div className="activity-item">
                      <div className="act-icon bg-purple">
                        <MessageCircle style={{ width: "14px", height: "14px" }} />
                      </div>
                      <div className="act-details">
                        <p>3 new conversations analyzed with positive interest</p>
                        <span>1 hour ago</span>
                      </div>
                    </div>
                    <div className="activity-item">
                      <div className="act-icon bg-orange">
                        <Star style={{ width: "14px", height: "14px" }} />
                      </div>
                      <div className="act-details">
                        <p>
                          Meeting scheduled: <strong>BrightFuture Inc</strong>
                        </p>
                        <span>2 hours ago</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* AI Insights Widget */}
                <div className="split-column right-split card-glass-dark">
                  <div className="insights-header">
                    <h4 className="column-title">
                      <Sparkles className="col-cyan" /> LeadFlow AI Insight
                    </h4>
                    <span className="badge-growth">+18%</span>
                  </div>
                  <p className="insight-text">
                    Your outreach conversion rate is up <strong>18%</strong> this month. Diagnostics show that
                    leading with <em>Website Load Speed</em> and <em>SEO Gaps</em> drives a{" "}
                    <strong>2.8x higher response rate</strong> compared to general agency marketing.
                  </p>

                  {/* Mock Line Chart */}
                  <div 
                    className="mock-chart-container" 
                    style={{ position: "relative" }}
                    onMouseMove={handleChartInteraction}
                    onClick={handleChartInteraction}
                    onMouseLeave={() => setHoveredPoint(null)}
                  >
                    <div className="chart-label">Conversion Performance Trajectory</div>
                    <div className="chart-canvas-mock">
                      <svg 
                        className="chart-svg" 
                        viewBox="0 0 300 100" 
                        style={{ cursor: "pointer" }}
                      >
                        <line x1="0" y1="20" x2="300" y2="20" stroke="rgba(255,255,255,0.05)" strokeDasharray="3"></line>
                        <line x1="0" y1="50" x2="300" y2="50" stroke="rgba(255,255,255,0.05)" strokeDasharray="3"></line>
                        <line x1="0" y1="80" x2="300" y2="80" stroke="rgba(255,255,255,0.05)" strokeDasharray="3"></line>

                        <path d="M 0 90 Q 50 80 80 50 T 150 40 T 220 20 T 300 10 L 300 100 L 0 100 Z" fill="url(#chart-grad)" opacity="0.15"></path>

                        <path d="M 0 90 Q 50 80 80 50 T 150 40 T 220 20 T 300 10" fill="none" stroke="url(#stroke-grad)" strokeWidth="3"></path>

                        <circle
                          cx="80"
                          cy="50"
                          r="3"
                          fill="#4F46E5"
                          stroke="#00D4FF"
                          strokeWidth="1"
                          style={{ pointerEvents: "none" }}
                        />

                        <circle
                          cx="150"
                          cy="40"
                          r="3"
                          fill="#4F46E5"
                          stroke="#00D4FF"
                          strokeWidth="1"
                          style={{ pointerEvents: "none" }}
                        />

                        <circle
                          cx="220"
                          cy="20"
                          r="3"
                          fill="#4F46E5"
                          stroke="#00D4FF"
                          strokeWidth="1"
                          style={{ pointerEvents: "none" }}
                        />

                        <circle cx="300" cy="10" r="5" fill="#00D4FF" className="chart-pulse-dot" style={{ pointerEvents: "none" }}></circle>

                        <defs>
                          <linearGradient id="chart-grad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stopColor="#4F46E5"></stop>
                            <stop offset="100%" stopColor="#4F46E5" stopOpacity="0"></stop>
                          </linearGradient>
                          <linearGradient id="stroke-grad" x1="0" y1="0" x2="1" y2="0">
                            <stop offset="0%" stopColor="#4F46E5"></stop>
                            <stop offset="100%" stopColor="#00D4FF"></stop>
                          </linearGradient>
                        </defs>
                      </svg>
                    </div>

                    {hoveredPoint && (
                      <div 
                        className="absolute bg-slate-950/90 border border-indigo-500/40 text-white rounded-lg px-2 py-1 text-[9px] shadow-[0_0_15px_rgba(79,70,229,0.3)] pointer-events-none transition-all duration-150 z-20 backdrop-blur-sm"
                        style={{
                          left: `${(hoveredPoint.x / 300) * 100}%`,
                          top: `${(hoveredPoint.y / 100) * 100 - 35}%`,
                          transform: 'translateX(-50%)',
                        }}
                      >
                        <div className="font-bold text-indigo-300">{hoveredPoint.week}</div>
                        <div>Conv. Rate: <span className="font-semibold text-[#00D4FF]">{hoveredPoint.value}</span></div>
                      </div>
                    )}
                    <div className="chart-xaxis">
                      <span>Week 1</span>
                      <span>Week 2</span>
                      <span>Week 3</span>
                      <span>Week 4</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Future Vision Section */}
      <section className="roadmap-section" id="roadmap">
        <div className="container">
          <div className="section-header text-center">
            <span className="section-tag">Next-Gen Roadmap</span>
            <h2 className="section-title">The future of autonomous sales operations.</h2>
            <p className="section-sub">
              We are building the intelligence layers for multi-channel sales representation. Here is what is
              coming next to LeadFlow Labs.
            </p>
          </div>

          <div className="roadmap-grid">
            <div className="roadmap-card">
              <div className="rm-badge">LABS</div>
              <h3 className="rm-title">
                <PhoneCall className="col-cyan" /> AI Voice Agent
              </h3>
              <p className="rm-desc">
                Ultra-low latency conversational voice interfaces to handle cold calling qualification calls and
                outbound follow-up queries with natural human intonation.
              </p>
            </div>

            <div className="roadmap-card">
              <div className="rm-badge">PLANNED</div>
              <h3 className="rm-title">
                <MessageSquare className="col-blue" /> WhatsApp Automation
              </h3>
              <p className="rm-desc">
                Interact natively with prospects on mobile. Automatically construct chat pipelines, handle
                responses, and drop booking calendar invitations inside WhatsApp.
              </p>
            </div>

            <div className="roadmap-card">
              <div className="rm-badge">PLANNED</div>
              <h3 className="rm-title">
                <Network className="col-purple" /> LinkedIn Outreach
              </h3>
              <p className="rm-desc">
                Sync LinkedIn networks to run multi-agent social outreach. Build lists, visit key targets, and
                coordinate messages with standard inbox systems.
              </p>
            </div>

            <div className="roadmap-card">
              <div className="rm-badge">LABS</div>
              <h3 className="rm-title">
                <TrendingUp className="col-green" /> Predictive Conversion Analytics
              </h3>
              <p className="rm-desc">
                Machine learning forecast models that predict deal closure probabilities based on response
                sentiment dynamics, client profiles, and historical cycles.
              </p>
            </div>

            <div className="roadmap-card">
              <div className="rm-badge">IN DEV</div>
              <h3 className="rm-title">
                <UsersRound className="col-orange" /> Multi-Agent Sales Teams
              </h3>
              <p className="rm-desc">
                Deploy coordinate swarms of AI agents acting in specialist roles (e.g., Prospector Agent,
                Quality Evaluator Agent, Outbox Writer Agent) for complete vertical operations.
              </p>
            </div>

            <div className="roadmap-card">
              <div className="rm-badge">IN DEV</div>
              <h3 className="rm-title">
                <Landmark className="col-red" /> Revenue Forecasting
              </h3>
              <p className="rm-desc">
                Link outbound campaign intensity directly with revenue forecasting charts, visualizing expected
                contract yields and future sales pipelines.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="final-cta" id="get-started">
        <div className="cta-glow-bg"></div>
        <div className="container text-center">
          <div className="cta-box card-glass">
            <h2 className="cta-headline">
              Stop Managing Leads. <br />
              <span className="gradient-text">Start Closing Deals.</span>
            </h2>
            <p className="cta-sub">
              LeadFlow AI handles qualification, outreach, follow-ups, and lead intelligence while your team
              focuses on growth. Join the future of autonomous sales operations.
            </p>
            <div className="cta-actions">
              <Link href="/dashboard" className="btn btn-primary btn-lg">
                Get Started
              </Link>
              <button
                onClick={() => setIsDemoModalOpen(true)}
                className="btn btn-secondary btn-lg"
                id="final-demo-btn"
              >
                Book Demo
              </button>
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
                <a href="#features">Features</a>
                <a href="#showcase">Dashboard</a>
                <a href="#roadmap">Labs Roadmap</a>
              </div>
              <div className="footer-col">
                <h4>Technology</h4>
                <span className="nav-item-mock">AI Qualification</span>
                <span className="nav-item-mock">Reply Core</span>
                <span className="nav-item-mock">Data Privacy</span>
              </div>
              <div className="footer-col">
                <h4>Pricing</h4>
                <span className="nav-item-mock">Standard Agency</span>
                <span className="nav-item-mock">Enterprise Custom</span>
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

      {/* Watch Demo Modal Overlay */}
      {isDemoModalOpen && (
        <div className="demo-modal-overlay active" id="demo-modal" onClick={() => setIsDemoModalOpen(false)}>
          <div className="demo-modal card-glass" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>LeadFlow AI Walkthrough Demonstration</h3>
              <button
                className="modal-close"
                id="modal-close-btn"
                onClick={() => setIsDemoModalOpen(false)}
              >
                &times;
              </button>
            </div>
            <div className="modal-body">
              <div className="mock-player" onClick={() => setDemoPlaying(!demoPlaying)}>
                <div className="player-overlay">
                  {demoPlaying ? (
                    <PauseCircle className="player-play-icon" />
                  ) : (
                    <PlayCircle className="player-play-icon" />
                  )}
                  <span>{demoPlaying ? "Click to pause video player" : "Click to play interactive sales workflow demo"}</span>
                </div>
                <div className="player-subtitles" style={{ background: demoPlaying ? "rgba(79, 70, 229, 0.4)" : "rgba(0, 0, 0, 0.6)" }}>
                  &quot;{demoSubtitles[demoSubtitleIdx]}&quot;
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
