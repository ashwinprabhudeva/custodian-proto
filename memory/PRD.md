# Custodian Prototype PRD

## Original problem statement
Build “Custodian,” a cultural-tourism platform for Manipal and Udupi where local custodians control how their experiences are shown, priced, and accessed. Tourists browse and request direct-access cultural experiences; the prototype includes discovery, experience details, custodian profiles, mock booking, tourist passport, time capsule, skill swap, legacy questions, mystery local, seasonal availability, and a custodian consent dashboard.

## Architecture decisions
- React frontend with React Router for the discovery, detail, custodian, passport, and dashboard routes.
- FastAPI backend with in-memory illustrative experience data and API endpoints for experiences, bookings, and legacy questions.
- Existing MongoDB configuration remains untouched; no login or persistent user accounts are required for this prototype.
- Frontend calls only `REACT_APP_BACKEND_URL`; booking/payment and legacy persistence are intentionally **MOCKED**.

## User personas
- Curious tourist seeking intimate, respectful cultural experiences around Manipal and Udupi.
- Local custodian wanting visible control over framing, access, pricing, participation, and revocability.
- Returning visitor collecting personal field notes, learned skills, badges, and delayed messages.

## Core requirements
- Six seeded custodian experiences across Food, Craft, Ritual / Religious, Performance, and Nature / Fishing.
- Custodian-authored first-person descriptions and visible consent settings.
- Mystery Local selection, review-based Boosted visibility, trusted local partner badges, and testimonial reviews.
- Request → pending confirmation → mock payment-ready booking flow.
- Tourist badge scrapbook, Skill Swap Passport, Time Capsule inbox, and legacy questions.
- Custodian dashboard with six consent toggles and seasonal availability calendar.

## Implemented

### 2026-09-12
- Replaced starter screen with full editorial Custodian experience and seeded Manipal/Udupi content.
- Added responsive discovery feed, category filters, Mystery Local modal, experience detail routes, custodian profiles, tourist passport, and consent dashboard.
- Added FastAPI endpoints for experiences, mock booking requests, and legacy reflections.
- Added visual system using Playfair Display, Plus Jakarta Sans, earthy editorial palette, responsive layouts, motion, and stable image assets.
- Added descriptive `data-testid` attributes to interactive and critical experience elements.
- Added functional responsive mobile navigation and verified it at phone width.
- Verified API regression, frontend journeys, responsive overflow, build, and no-console-error regression tests.

## Prioritized backlog
- P0: Keep the prototype flows stable and continue validating the seeded content with local cultural partners.
- P1: Add persistent profiles and booking history when the prototype moves beyond seeded demo data.
- P1: Add real custodian availability editing and visitor-specific Time Capsule delivery dates.
- P2: Add shareable passport story-card export and richer badge artwork.

## P0 / P1 / P2 remaining
- P0: None for the requested prototype scope.
- P1: Persistence, real calendar editing, and visitor session state.
- P2: Share/export, richer content moderation, and optional real payments.

## Next tasks
1. Connect custodians to persistent profiles and editable experience settings.
2. Store booking requests and show a visitor’s request history.
3. Let custodians record and schedule Time Capsule messages.
4. Generate a shareable passport story card from collected badges and skills.