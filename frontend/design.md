---
name: LeadFlow AI Design System
colors:
surface: '#faf8ff'
surface-dim: '#d2d9f4'
surface-bright: '#faf8ff'
surface-container-lowest: '#ffffff'
surface-container-low: '#f2f3ff'
surface-container: '#eaedff'
surface-container-high: '#e2e7ff'
surface-container-highest: '#dae2fd'
on-surface: '#131b2e'
on-surface-variant: '#464554'
inverse-surface: '#283044'
inverse-on-surface: '#eef0ff'
outline: '#767586'
outline-variant: '#c7c4d7'
surface-tint: '#494bd6'
primary: '#4648d4'
on-primary: '#ffffff'
primary-container: '#6063ee'
on-primary-container: '#fffbff'
inverse-primary: '#c0c1ff'
secondary: '#006c49'
on-secondary: '#ffffff'
secondary-container: '#6cf8bb'
on-secondary-container: '#00714d'
tertiary: '#6b38d4'
on-tertiary: '#ffffff'
tertiary-container: '#8455ef'
on-tertiary-container: '#fffbff'
error: '#ba1a1a'
on-error: '#ffffff'
error-container: '#ffdad6'
on-error-container: '#93000a'
primary-fixed: '#e1e0ff'
primary-fixed-dim: '#c0c1ff'
on-primary-fixed: '#07006c'
on-primary-fixed-variant: '#2f2ebe'
secondary-fixed: '#6ffbbe'
secondary-fixed-dim: '#4edea3'
on-secondary-fixed: '#002113'
on-secondary-fixed-variant: '#005236'
tertiary-fixed: '#e9ddff'
tertiary-fixed-dim: '#d0bcff'
on-tertiary-fixed: '#23005c'
on-tertiary-fixed-variant: '#5516be'
background: '#faf8ff'
on-background: '#131b2e'
surface-variant: '#dae2fd'
typography:
headline-xl:
fontFamily: Geist
fontSize: 48px
fontWeight: '700'
lineHeight: '1.1'
letterSpacing: -0.03em
headline-lg:
fontFamily: Geist
fontSize: 32px
fontWeight: '600'
lineHeight: '1.2'
letterSpacing: -0.02em
headline-md:
fontFamily: Geist
fontSize: 24px
fontWeight: '600'
lineHeight: '1.3'
body-lg:
fontFamily: Inter
fontSize: 18px
fontWeight: '400'
lineHeight: '1.6'
body-md:
fontFamily: Inter
fontSize: 16px
fontWeight: '400'
lineHeight: '1.5'
body-sm:
fontFamily: Inter
fontSize: 14px
fontWeight: '400'
lineHeight: '1.5'
label-md:
fontFamily: Geist
fontSize: 14px
fontWeight: '600'
lineHeight: '1.2'
label-sm:
fontFamily: Geist
fontSize: 12px
fontWeight: '500'
lineHeight: '1.2'
letterSpacing: 0.02em
headline-lg-mobile:
fontFamily: Geist
fontSize: 28px
fontWeight: '700'
lineHeight: '1.2'
rounded:
sm: 0.25rem
DEFAULT: 0.5rem
md: 0.75rem
lg: 1rem
xl: 1.5rem
full: 9999px
spacing:
container-max: 1440px
gutter: 1.5rem
margin-mobile: 1rem
sidebar-width: 240px
card-padding: 1.5rem
stack-gap: 1rem
Brand & Style
This design system is engineered for an AI-centric sales automation environment. It prioritizes a sense of "intelligent clarity"—balancing high-density data visualization with sophisticated, breathable aesthetics.
The style is Modern Corporate with Glassmorphic accents, characterized by:
Intelligent Flow: Use of soft gradients and "flow" lines to represent the movement of data and leads.
Precision Glassmorphism: Subtle background blurs and translucent surface treatments to imply depth without sacrificing legibility.
High-Performance Tone: A professional, tech-forward aesthetic that feels reliable enough for enterprise finance yet agile enough for a startup.
State-Driven Visuals: Heavy reliance on color-coded "states" (e.g., Qualified, Engaged) to provide instant cognitive feedback.
Colors
The palette is anchored in deep indigos and violets to represent intelligence and technology, contrasted against a functional "Success Green" for lead qualification.
Primary (Indigo): #6366f1. Used for primary actions, active navigation states, and brand-defining accents.
Secondary (Qualified Green): #10b981. Specifically reserved for "Qualified" lead states, growth metrics, and positive success indicators.
Tertiary (Violet): #8b5cf6. Used for secondary metrics, "Conversations" data, and AI-powered feature highlights.
Neutral (Slate/Navy): #0f172a. Used for deep-background sidebars, primary text in light mode, and structural elements.
Functional Backgrounds: Light mode uses #F8FAFC (Slate 50) for canvas backgrounds, while dark mode utilizes #020617 (Slate 950).
Typography
The system utilizes a dual-font strategy. Geist provides a technical, geometric edge for headlines and labels, reinforcing the AI/developer-centric nature of the product. Inter is used for body copy to ensure maximum legibility at high densities.
Weight Hierarchy: Bold weights (700) are reserved for primary marketing headlines. Semi-bold (600) is the workhorse for dashboard headers and metric labels.
Tight Kerning: Headlines use slightly negative letter-spacing to feel more "locked-in" and professional.
Metric Emphasis: Numbers in dashboards should use Geist Medium/Semi-bold for a crisp, tabular feel even without monospacing.
Layout & Spacing
This design system uses a Flexible Fluid Grid with specific sidebar and main-content constraints.
The Dashboard Shell: A fixed-width left sidebar (72px collapsed, 240px expanded) paired with a fluid main content area.
Rhythm: An 8px base unit drives all spacing. Dashboard cards typically use 24px (1.5rem) internal padding.
Stacking: Vertically stacked components in lead lists use a 12px or 16px gap to maintain high information density without clutter.
Breakpoints:
Desktop: 12-column grid.
Tablet: 6-column grid, sidebar collapses to icon-only.
Mobile: 1-column grid, sidebar moves to a bottom nav or hamburger menu.
Elevation & Depth
Visual hierarchy is established through Tonal Layering and Glassmorphism rather than traditional heavy shadows.
Surface Levels:
Level 0 (Base): The canvas color (#F8FAFC).
Level 1 (Cards): White or #FFFFFF with a 1px border (#E2E8F0).
Level 2 (Modals/Popovers): White with a subtle backdrop blur (12px) and a soft, diffused shadow (0 10px 15px -3px rgba(0,0,0,0.05)).
Glassmorphic Accents: Secondary navigation elements or information tooltips use 20% opacity white with a 16px blur effect.
Borders: Instead of drop shadows, use 1px solid borders in a slightly darker shade of the background to define container boundaries.
Shapes
The shape language is "Sophisticated Softness."
Primary Containers: Dashboard cards and main UI blocks use a 16px (rounded-xl) radius.
Interactive Elements: Buttons and input fields use a 12px (rounded-lg) radius.
Small Components: Chips and tags use an 8px (rounded-md) radius or a full pill shape for status indicators.
Consistency: Never use sharp 0px corners; every element must have a degree of curvature to maintain the approachable, modern brand personality.
Components
Buttons
Primary: Solid indigo (#6366f1) with white text. High-contrast, 12px corner radius.
Secondary: Ghost style with indigo border or light indigo tint background.
AI Action: Gradient background (Indigo to Violet) with a "sparkle" icon.
Cards (The "Flow" Card)
Dashboard Metrics: White background, 1px grey border, 16px radius. Feature a mini-sparkline graph at the bottom using the primary or secondary color.
Pipeline Cards: Use subtle pastel backgrounds (e.g., 5% opacity of the state color) to denote status.
Input Fields
Default: Light grey stroke (#CBD5E1), 12px radius, Inter 14px text.
Focus: 2px indigo border with a soft glow (3px spread).
Chips & Tags
Status Tags: Pill-shaped, using 10% opacity of the status color for the background and 100% opacity for the text and icon.
Navigation
Sidebar: Dark navy (#0f172a). Icons should be thin-stroke (2px) and monochromatic, turning primary indigo when active. Use a subtle vertical glow line on the left of the active item.