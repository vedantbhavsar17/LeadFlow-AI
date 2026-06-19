document.addEventListener('DOMContentLoaded', () => {
  
  /* ==========================================================================
     1. HERO PIPELINE ANIMATION (REFINED SEQUENTIAL PACKET FLOW)
     ========================================================================== */
  const pipelineNodes = document.querySelectorAll('.pipeline-node');
  const pipelineConnectors = document.querySelectorAll('.pipeline-connector');
  let currentStageIndex = 0;
  let pipelineActive = true;
  
  const stageDurations = {
    'csv': 1500,        // progress bar fills
    'qualify': 1500,    // scores count up
    'pain-points': 1500, // laser beam flashes
    'outreach': 1500,   // typing dots animate
    'reply': 1500,      // category chips display
    'follow-up': 1500,  // clocks spin
    'meeting': 2500     // bursts confetti
  };

  const pipeScoreReadout = document.getElementById('pipe-score-readout');
  const pipeReplyReadout = document.getElementById('pipe-reply-readout');

  function resetPipeline() {
    pipelineNodes.forEach(node => {
      node.classList.remove('active', 'processing', 'success');
    });
    pipelineConnectors.forEach(conn => {
      conn.classList.remove('active');
    });
    if (pipeScoreReadout) pipeScoreReadout.textContent = '-- WARM';
    if (pipeReplyReadout) pipeReplyReadout.textContent = 'Budget ✓';
  }

  function runPipelineStep() {
    if (!pipelineActive) return;
    
    // Reset all nodes if we are starting over
    if (currentStageIndex === 0) {
      resetPipeline();
    }
    
    const currentNode = pipelineNodes[currentStageIndex];
    if (!currentNode) return;
    
    const stage = currentNode.getAttribute('data-stage');
    const duration = stageDurations[stage] || 1500;
    
    // Set active and processing
    currentNode.classList.add('active', 'processing');
    
    // Custom JS animations during processing
    if (stage === 'qualify' && pipeScoreReadout) {
      let val = 10;
      const interval = setInterval(() => {
        val += 7;
        if (val > 91) val = 91;
        pipeScoreReadout.textContent = `${val} HOT`;
      }, 100);
      setTimeout(() => clearInterval(interval), duration);
    }
    
    if (stage === 'reply' && pipeReplyReadout) {
      const replies = ['Objection ✓', 'Budget ✓', 'Timeline ✓', 'Meeting ✓'];
      let idx = 0;
      const interval = setInterval(() => {
        pipeReplyReadout.textContent = replies[idx % replies.length];
        idx++;
      }, 300);
      setTimeout(() => clearInterval(interval), duration);
    }

    // After processing finishes, transition to success and trigger connector flow
    setTimeout(() => {
      currentNode.classList.remove('processing');
      currentNode.classList.add('success');
      
      // If there is a next connector, run its flow pulse
      if (currentStageIndex < pipelineNodes.length - 1) {
        const currentConnector = pipelineConnectors[currentStageIndex];
        if (currentConnector) currentConnector.classList.add('active');
        
        // Wait for connector pulse (800ms) to travel before launching next node
        setTimeout(() => {
          currentStageIndex++;
          runPipelineStep();
        }, 800);
      } else {
        // Last node (Meeting Scheduled) stays success for its duration, then starts over
        setTimeout(() => {
          currentStageIndex = 0;
          runPipelineStep();
        }, duration);
      }
    }, duration);
  }

  // Start the pipeline loop
  if (pipelineNodes.length > 0) {
    runPipelineStep();
  }

  
  /* ==========================================================================
     2. SCROLLTELLING ENGINE
     ========================================================================== */
  const scrollTrack = document.getElementById('scroll-track');
  const textScenes = document.querySelectorAll('.scene-text');
  const visualScenes = document.querySelectorAll('.scene-visual');
  
  // Scroll variables for Scene 1 (Chaos leads)
  const chaosLeads = document.querySelectorAll('.chaos-lead');
  const chaosCenterGlow = document.querySelector('.chaos-center-glow');
  
  // Scroll variables for Scene 2 (Qualification)
  const hotCard = document.querySelector('.hot-card');
  const warmCard = document.querySelector('.warm-card');
  const coldCard = document.querySelector('.cold-card');
  
  // Scroll variables for Scene 3 (Diagnostics)
  const diagnosticItems = document.querySelectorAll('.diagnostic-item');
  const laserLine = document.querySelector('.scan-laser-line');
  const diagnosticFooter = document.querySelector('.diagnostic-footer');
  
  // Scroll variables for Scene 4 (Outreach typing)
  const typedEmailSpan = document.getElementById('typed-email');
  const emailText = `Hi John,

I noticed Acme Corp's website speed is 6.4s, and you are missing active intake mechanisms. Let's fix this for Q3. We can build a bespoke high-performance funnel that converts.

Best,
LeadFlow AI`;

  // Scroll variables for Scene 5 (Reply extraction)
  const extractedProfile = document.querySelector('.extracted-profile-card');
  
  // Scroll variables for Scene 6 (Memory toast)
  const followUpToast = document.querySelector('.follow-up-toast');

  function updateScrolltelling() {
    if (!scrollTrack) return;
    
    const trackRect = scrollTrack.getBoundingClientRect();
    const trackTop = trackRect.top;
    const trackHeight = trackRect.height;
    
    // Calculate global scroll progress of the track (0.0 to 1.0)
    const totalScrollable = trackHeight - window.innerHeight;
    let progress = -trackTop / totalScrollable;
    progress = Math.min(Math.max(progress, 0), 1);
    
    // Determine which scene is currently active (6 scenes total)
    const totalScenes = 6;
    const sceneIndex = Math.min(Math.floor(progress * totalScenes), totalScenes - 1);
    
    // Update active classes for texts and visuals
    textScenes.forEach((sceneText, idx) => {
      sceneText.classList.remove('active', 'exit');
      if (idx === sceneIndex) {
        sceneText.classList.add('active');
      } else if (idx < sceneIndex) {
        sceneText.classList.add('exit');
      }
    });
    
    visualScenes.forEach((sceneVis, idx) => {
      sceneVis.classList.remove('active');
      if (idx === sceneIndex) {
        sceneVis.classList.add('active');
      }
    });
    
    // Calculate local progress within the active scene range (0.0 to 1.0)
    const sceneProgress = (progress * totalScenes) - sceneIndex;
    
    /* ----------------------------------------------------
       SCENE 1: Chaos Leads
       As we scroll from 0% -> 100% of Scene 1, they fly inwards
       ---------------------------------------------------- */
    if (sceneIndex === 0) {
      // Scale glow in center based on scroll
      chaosCenterGlow.style.opacity = sceneProgress * 0.8;
      chaosCenterGlow.style.transform = `scale(${0.5 + (sceneProgress * 1.5)})`;
      
      chaosLeads.forEach((lead, i) => {
        // Retrieve initial positions from HTML inline styles or custom factors
        const factor = (i + 1) * 0.2;
        // Interpolate translations towards (0, 0)
        const initialX = parseFloat(lead.style.getPropertyValue('--x'));
        const initialY = parseFloat(lead.style.getPropertyValue('--y'));
        const initialR = parseFloat(lead.style.getPropertyValue('--r'));
        
        const currentX = initialX * (1 - sceneProgress);
        const currentY = initialY * (1 - sceneProgress);
        const currentR = initialR * (1 - sceneProgress);
        const scale = 1 - (sceneProgress * 0.3);
        
        lead.style.transform = `translate(${currentX}px, ${currentY}px) rotate(${currentR}deg) scale(${scale})`;
        lead.style.opacity = 1 - (sceneProgress * 0.8);
      });
    } else {
      // Reset Scene 1 if we scroll past
      chaosLeads.forEach(lead => {
        const initialX = lead.style.getPropertyValue('--x');
        const initialY = lead.style.getPropertyValue('--y');
        const initialR = lead.style.getPropertyValue('--r');
        lead.style.transform = `translate(${initialX}, ${initialY}) rotate(${initialR})`;
        lead.style.opacity = 1;
      });
      chaosCenterGlow.style.opacity = 0;
    }
    
    /* ----------------------------------------------------
       SCENE 2: AI Core Qualification
       Leads exit from the AI core into scored cards
       ---------------------------------------------------- */
    if (sceneIndex === 1) {
      // Hot card exits to top-right
      if (sceneProgress > 0.1) {
        const hotProgress = Math.min((sceneProgress - 0.1) / 0.4, 1);
        hotCard.style.transform = `translate(${hotProgress * 130}px, -${hotProgress * 110}px) scale(${0.6 + (hotProgress * 0.4)})`;
        hotCard.style.opacity = hotProgress;
      } else {
        hotCard.style.transform = 'translate(0, 0) scale(0.6)';
        hotCard.style.opacity = 0;
      }
      
      // Warm card exits to middle-right
      if (sceneProgress > 0.3) {
        const warmProgress = Math.min((sceneProgress - 0.3) / 0.4, 1);
        warmCard.style.transform = `translate(${warmProgress * 160}px, 0px) scale(${0.6 + (warmProgress * 0.4)})`;
        warmCard.style.opacity = warmProgress;
      } else {
        warmCard.style.transform = 'translate(0, 0) scale(0.6)';
        warmCard.style.opacity = 0;
      }
      
      // Cold card exits to bottom-right
      if (sceneProgress > 0.5) {
        const coldProgress = Math.min((sceneProgress - 0.5) / 0.4, 1);
        coldCard.style.transform = `translate(${coldProgress * 130}px, ${coldProgress * 110}px) scale(${0.6 + (coldProgress * 0.4)})`;
        coldCard.style.opacity = coldProgress;
      } else {
        coldCard.style.transform = 'translate(0, 0) scale(0.6)';
        coldCard.style.opacity = 0;
      }
    }
    
    /* ----------------------------------------------------
       SCENE 3: Pain Diagnostics Scan
       Diagnostic checklist items checked off sequentially
       ---------------------------------------------------- */
    if (sceneIndex === 2) {
      laserLine.classList.add('animating');
      
      // Reveal items sequentially
      if (sceneProgress > 0.1) diagnosticItems[0].classList.add('revealed');
      else diagnosticItems[0].classList.remove('revealed');
      
      if (sceneProgress > 0.3) diagnosticItems[1].classList.add('revealed');
      else diagnosticItems[1].classList.remove('revealed');
      
      if (sceneProgress > 0.5) diagnosticItems[2].classList.add('revealed');
      else diagnosticItems[2].classList.remove('revealed');
      
      if (sceneProgress > 0.7) {
        diagnosticItems[3].classList.add('revealed');
        diagnosticFooter.classList.add('revealed');
      } else {
        diagnosticItems[3].classList.remove('revealed');
        diagnosticFooter.classList.remove('revealed');
      }
    } else {
      laserLine.classList.remove('animating');
      diagnosticItems.forEach(item => item.classList.remove('revealed'));
      diagnosticFooter.classList.remove('revealed');
    }
    
    /* ----------------------------------------------------
       SCENE 4: Personalized Outreach Copy Writing
       Typewriter effect synchronized to scroll position
       ---------------------------------------------------- */
    if (sceneIndex === 3) {
      const charCount = Math.floor(sceneProgress * emailText.length);
      const visibleText = emailText.substring(0, charCount);
      // Format line breaks
      typedEmailSpan.innerHTML = visibleText.replace(/\n/g, '<br>');
    }
    
    /* ----------------------------------------------------
       SCENE 5: Reply Analysis extraction
       Transition the extraction cards based on scroll
       ---------------------------------------------------- */
    if (sceneIndex === 4) {
      if (sceneProgress > 0.4) {
        extractedProfile.classList.add('active');
      } else {
        extractedProfile.classList.remove('active');
      }
    } else {
      extractedProfile.classList.remove('active');
    }
    
    /* ----------------------------------------------------
       SCENE 6: Lead Memory & Follow-Up
       Node networks draw and follow up notification displays
       ---------------------------------------------------- */
    if (sceneIndex === 5) {
      if (sceneProgress > 0.5) {
        followUpToast.classList.add('active');
      } else {
        followUpToast.classList.remove('active');
      }
    } else {
      followUpToast.classList.remove('active');
    }
  }

  // Register Scroll Listener
  window.addEventListener('scroll', updateScrolltelling);
  updateScrolltelling(); // Run initially

  
  /* ==========================================================================
     3. FEATURE CARDS CURSOR TRACKING GLOW
     ========================================================================== */
  const featureCards = document.querySelectorAll('.feature-card');
  
  featureCards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);
    });
  });

  
  /* ==========================================================================
     4. STATISTICS COUNTER ANIMATION
     ========================================================================== */
  const statsSection = document.querySelector('.social-proof-section');
  const statValues = document.querySelectorAll('.stat-value');
  let animatedStats = false;
  
  function animateCounters() {
    statValues.forEach(val => {
      const targetStr = val.getAttribute('data-target');
      if (!targetStr) return; // Skip 24/7 static value
      
      const target = parseInt(targetStr);
      let count = 0;
      const duration = 1500; // ms
      const startTime = performance.now();
      
      function updateCount(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing out quad
        const easeProgress = progress * (2 - progress);
        const currentVal = Math.floor(easeProgress * target);
        
        // Format check: handles multipliers (3x) vs percentages (80%)
        if (targetStr === '3') {
          val.textContent = `${currentVal}x`;
        } else {
          val.textContent = `${currentVal}%`;
        }
        
        if (progress < 1) {
          requestAnimationFrame(updateCount);
        } else {
          if (targetStr === '3') val.textContent = '3x';
          else val.textContent = `${target}%`;
        }
      }
      
      requestAnimationFrame(updateCount);
    });
  }
  
  // Set up intersection observer to trigger counters once
  if (statsSection) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !animatedStats) {
          animatedStats = true;
          animateCounters();
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });
    
    observer.observe(statsSection);
  }

  
  /* ==========================================================================
     5. WATCH DEMO MODAL TRIGGER SYSTEM
     ========================================================================== */
  const demoModal = document.getElementById('demo-modal');
  const demoButtons = [
    document.getElementById('nav-demo-btn'),
    document.getElementById('hero-demo-btn'),
    document.getElementById('final-demo-btn')
  ];
  const modalCloseBtn = document.getElementById('modal-close-btn');
  const mockPlayer = document.querySelector('.mock-player');
  const subtitleOverlay = document.querySelector('.player-subtitles');
  let currentDemoSubtitleInterval = null;
  
  // Subtitle script
  const demoSubtitles = [
    "LeadFlow AI loads leads from lists, registers, or inbound forms...",
    "The Diagnostic Engine instantly profiles technical errors & SEO bugs...",
    "Our generative models build dynamic outreach for their specific defects...",
    "Reply Intelligence parses incoming queries to pull budget, dates, and actions...",
    "Lead Memory links records securely and triggers automated pipeline sequences..."
  ];

  function startDemoSubtitles() {
    let index = 0;
    subtitleOverlay.textContent = `"${demoSubtitles[index]}"`;
    
    currentDemoSubtitleInterval = setInterval(() => {
      index = (index + 1) % demoSubtitles.length;
      subtitleOverlay.textContent = `"${demoSubtitles[index]}"`;
    }, 3500);
  }

  function stopDemoSubtitles() {
    if (currentDemoSubtitleInterval) {
      clearInterval(currentDemoSubtitleInterval);
      currentDemoSubtitleInterval = null;
    }
  }

  demoButtons.forEach(btn => {
    if (!btn) return;
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      demoModal.classList.add('active');
      startDemoSubtitles();
    });
  });

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', () => {
      demoModal.classList.remove('active');
      stopDemoSubtitles();
    });
  }

  // Close modal when clicking outside contents
  if (demoModal) {
    demoModal.addEventListener('click', (e) => {
      if (e.target === demoModal) {
        demoModal.classList.remove('active');
        stopDemoSubtitles();
      }
    });
  }
  
  // Click on mock player simulates close or interaction
  if (mockPlayer) {
    mockPlayer.addEventListener('click', () => {
      // Simulate play pause toggles
      const playIcon = mockPlayer.querySelector('.player-play-icon');
      if (playIcon.getAttribute('data-lucide') === 'play-circle') {
        playIcon.setAttribute('data-lucide', 'pause-circle');
        lucide.createIcons();
        subtitleOverlay.style.background = "rgba(79, 70, 229, 0.4)";
      } else {
        playIcon.setAttribute('data-lucide', 'play-circle');
        lucide.createIcons();
        subtitleOverlay.style.background = "rgba(0, 0, 0, 0.6)";
      }
    });
  }

  /* ==========================================================================
     6. PRICING PAGE TOGGLE & FAQ ACCORDION LOGIC
     ========================================================================== */
  const billingToggleBtn = document.getElementById('billing-toggle-btn');
  const billingMonthlyLabel = document.getElementById('billing-monthly');
  const billingAnnualLabel = document.getElementById('billing-annual');
  const priceValues = document.querySelectorAll('.price-val');
  const annualNotes = document.querySelectorAll('.annual-note');
  
  if (billingToggleBtn) {
    billingToggleBtn.addEventListener('click', () => {
      billingToggleBtn.classList.toggle('active');
      const isAnnual = billingToggleBtn.classList.contains('active');
      
      if (isAnnual) {
        if (billingMonthlyLabel) billingMonthlyLabel.classList.remove('active');
        if (billingAnnualLabel) billingAnnualLabel.classList.add('active');
      } else {
        if (billingMonthlyLabel) billingMonthlyLabel.classList.add('active');
        if (billingAnnualLabel) billingAnnualLabel.classList.remove('active');
      }
      
      priceValues.forEach(price => {
        const monthlyPrice = price.getAttribute('data-monthly');
        const annualPrice = price.getAttribute('data-annual');
        
        if (monthlyPrice && annualPrice) {
          price.textContent = isAnnual ? annualPrice : monthlyPrice;
        }
      });
      
      annualNotes.forEach(note => {
        if (note.textContent.trim() !== "Contact for volume quotes") {
          note.textContent = isAnnual ? "Billed annually" : "Billed monthly";
        }
      });
    });
  }
  
  // FAQ Accordion
  const faqQuestions = document.querySelectorAll('.faq-question');
  
  faqQuestions.forEach(question => {
    question.addEventListener('click', () => {
      const faqItem = question.parentElement;
      const faqAnswer = faqItem.querySelector('.faq-answer');
      const isActive = faqItem.classList.contains('active');
      
      // Close all other FAQs
      document.querySelectorAll('.faq-item').forEach(item => {
        item.classList.remove('active');
        const answer = item.querySelector('.faq-answer');
        if (answer) answer.style.maxHeight = '0px';
      });
      
      // Toggle current FAQ
      if (!isActive) {
        faqItem.classList.add('active');
        faqAnswer.style.maxHeight = faqAnswer.scrollHeight + 'px';
      } else {
        faqItem.classList.remove('active');
        faqAnswer.style.maxHeight = '0px';
      }
    });
  });
});
