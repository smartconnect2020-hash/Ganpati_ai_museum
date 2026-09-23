# Shri Ganesh Aayudhe — UX Case Study (English)

> **Status:** Full English translation of [CASE-STUDY-DRAFT.md](CASE-STUDY-DRAFT.md) (Marathi is the source of truth — if the two ever diverge, trust the Marathi). Section 2 (real personal memory) and Section 4/7 (guest-testing results) are still honestly empty/draft — nothing has been fabricated while waiting for the real thing. Working notes, change history, and detailed verification logs live in [CASE-STUDY-NOTES.md](CASE-STUDY-NOTES.md) (Marathi only).
>
> **Markers:** `【TO FILL】` = real personal memory · `❗` = pending real testing.

---

## Name (final)

**Title + Subtitle:**
> ## No One Could Explain the Idol's Symbolism Anymore
> *How I Gave Our Family's Real Ganpati Decoration an AI-Narrated Voice and a Modern Digital Layer — Solo, Offline-First*

*(19 other name options and the selection process are in CASE-STUDY-NOTES.md, Marathi only.)*

---

## Photos / Visuals — what's needed and what to name it

> Research principle: *"Visuals aren't decoration, they're evidence — incomplete without a caption."* ([IxDF — Picture Perfect](https://www.interaction-design.org/literature/article/how-to-create-visuals-for-your-ux-case-study)) Each slot below has a **fixed filename + caption** — drop the real photo under that exact name in `case-study-assets/final/` and it slots in directly. No empty placeholders or stock photos (would contradict Section 8's honesty).

| Slot | Filename to use | Caption (draft) | Status |
|---|---|---|---|
| Hook cover | `hero-cover.jpg` | "Our home's mandap — Bappa enthroned, all 20 aayudhe with QR labels" | ✅ have it (copy from `10-HERO-mandap-complete-ganpati.jpg`) |
| Section 2 — altar | `section2-devhara-wide.jpg` | "The home altar — a wide shot where every aayudh is visible" | ✅ have it |
| Section 2 — real photo | `section2-ankush-family.jpg` | "Ankush — our real family photo (the other 19 are AI reference art)" | ✅ existing (`ankush.jpg`) |
| Decision 2 — palette | `decision-palette-3concepts.jpg` | "3 concepts — museum placard, puja invitation (chosen), diya light" | 🔲 you provide |
| Decision 9 — QR | `decision-qr-before-after.jpg` | "Old (round modules, center icon) vs new (square, seal moved out)" | 🔲 you provide |
| Decision 12 — aayudh-chakra | `decision-ayudh-chakra.gif` or `.jpg` | "The rotating wheel — live on desktop" | 🔲 I can screen-record this, just ask |
| Decision 13 — logo | `decision-logo-before-after.jpg` | "Old kalash icon vs new ankush-play mark" | 🔲 I can produce this |
| Section 6 — workflow | `workflow-terminal.jpg` | "Claude Code terminal — a moment of actual work (optional)" | 🔲 optional |
| Decision 14 — raw 3D print | `fabrication-01-raw-print.jpg` | "3D print, still unpainted" | ✅ have it (from `01`/`02`) |
| Decision 14 — painted | `fabrication-02-painted.jpg` | "Finished piece, acrylic-painted" | ✅ have it (from `04`) |
| Decision 14 — product shots | `fabrication-03-product-*.jpg` | "Each aayudh, with its own QR label" | ✅ have it (from `11`, `12`) |
| Decoration/mandap journey | `decoration-mandap-0N.jpg` (N=1…5) | "Building the mandap — raw structure to complete, over 3 days" | ✅ have it, curated |
| Section 7 — testing | `testing-guest-scan.jpg` | "A guest actually scanning a QR code" | 🔲 after guest testing |
| Print close-up | `print-qr-cards-closeup.jpg` | "Printed QR cards + NFC tag" | 🟡 partial |
| Cover/hero (social) | `cover-social-1200x630.jpg` | — (no text, just a share preview) | 🔲 you provide |
| Section 7 — SEO proof | `seo-rich-results-proof.jpg` | "Google's Rich Results Test result — independent verification" | 🟡 **result verified (text proof below), but the screenshot file itself isn't saved yet** — I can re-capture it if asked |
| Section 7 — Analytics proof | `analytics-dashboard.jpg` | "GA4 dashboard — real users/traffic" | 🔲 **only you can get this** (it's behind your Google login, I have no access) |

The older, more detailed photo-tracking table (with verification history) stays in CASE-STUDY-NOTES.md.

---

## Section 0 — Hook

# No One Could Explain the Idol's Symbolism Anymore

### How I gave our family's real Ganpati decoration an AI-narrated voice and a modern digital layer — solo, offline-first

*Scan a QR code or tap NFC — Marathi audio stories for the 20 ritual weapons/attributes (Ekadanta, Parashu, Ankusha, Sudarshan Chakra, Khatvanga…) in Ganpati's hands, sourced verbatim from the original scripture guide. ₹0 hosting, no framework, works offline too.*

**[▶ Live demo](https://smartconnect2020-hash.github.io/Ganpati_ai_museum/)** &nbsp;&nbsp; **[GitHub](https://github.com/smartconnect2020-hash/Ganpati_ai_museum)** &nbsp;&nbsp; **[Read the case study ↓]**

---

## Section 1 — TL;DR box (the recruiter's 15-second scan)

```
Problem      →  Every weapon/attribute in Ganpati's idol carries real scriptural
                meaning — but during the festival no one explains it to guests
                or kids; the reference text stays shut in a cupboard
Solution     →  QR + NFC audio guide, 20 items, Marathi-first, offline PWA,
                text verbatim from the source guide + AI-TTS narration
My role      →  Solo — research + UX + visual design + no-framework build
                + QR/NFC pipeline + TTS pipeline + AI-workflow orchestration
Timeline     →  First commit 20 Aug 2026 → active through September 2026
Stack        →  Vanilla HTML/CSS/JS · PWA + Service Worker · single data.json
                · Python (qrcode / Pillow / pyzbar / uharfbuzz) · Claude Code
                · Sarvam Bulbul v3 TTS · AI image tools
Results      →  ✅ Real audio for 20/20 items (all AI-TTS — Section 8 #12
                is an honest account of the human-voice-to-TTS trade-off)
                ❗ Guest testing still pending — technical verification
                (QR decode, stress-test, live site) is done
Impact       →  A productizable template for Maharashtra households /
                Ganeshotsav community mandals
```

### 🧭 Problem frame — 5W1H (only what TL;DR doesn't already cover)

> *(Research: [Orbix — 5 W's in UX Design](https://www.orbix.studio/blogs/5-ws-in-ux-design))*

| | |
|---|---|
| **When** | Ganeshotsav 2026 — from deciding on the decoration (August) to going live before the festival |
| **Where** | The home mandap (physical) + an offline-first PWA (digital) — has to work even on patchy home WiFi |
| **Why** | The guide-text stays shut in a cupboard; it never reaches relatives who live elsewhere; some guests find reading it hard |

**Problem Statement (NN/g pattern — user + need + insight):**
> Guests visiting for Ganeshotsav, and relatives who live too far away to visit, want to understand the meaning behind Ganpati's ritual weapons/attributes, **because** the current guide-text takes time and inclination to read that people don't have, and it simply never reaches the ones who can't be there in person.

---

## Section 2 — How it started

*First person. No jargon.*

This year, while planning a new kind of home decoration, we settled on Ganpati's ritual weapons/attributes as the theme — and immediately realized: most people don't actually know what these aayudhe are or what they're called (beyond 2-3 of them). So I started gathering that information — from the puranas, from a history book.

Then the real question hit me: **how do I show this to relatives who live too far away to visit?** The answer: a QR code for every aayudh — since everyone has a phone and a scanner in their pocket these days. So I built a free website (from a GitHub repo, with Claude's help), and mapped all the information onto it.

But reading plain text turned out to be hard for some people — especially older relatives and young kids. So I decided to add audio, with AI's help. And to make sure this information reached as many people as possible, I added SEO and Analytics to the site.

*(Based on two real handwritten notes — the first paragraph is from the "physical decoration" note, the rest from the "QR/website" note; the connecting thread between the two notes ["decided on the aayudhe" → "the question of showing relatives"] is my own inference, not written verbatim in that sequence in the notes. Full original text — HANDWRITTEN-NOTES-DIGITIZED.md, Marathi only.)*

---

## Section 3 — Why this isn't a solved problem (constraints shaped the design)

| Constraint | Why it matters | Design implication |
|---|---|---|
| **Budget: ₹0 hosting** | Has to be affordable for any household | GitHub Pages (free, auto-HTTPS); QR codes generated in-house with Python; NFC ~₹15/tag |
| **Content editor: a non-technical family member** | Text has to be editable without me | A single `data.json` (plain text file) + Notepad + a jsonlint.com check + a 3-minute flow documented in the README |
| **Guest ages 8 to 80** | The UI has to work for every generation | Marathi by default, system-ui font, large tap targets (the "mudra" Play button is 80px, ±10s skip is 48px — everything ≥44px) |
| **Devices: iPhone 6 through 15, budget Android** | Can't assume modern NFC | QR is always primary, NFC secondary; a placard note for older iPhones |
| **Patchy home WiFi** | Has to work without the internet | PWA + Service Worker, cache-first; photos/audio/fonts go offline after the first visit |
| **Religious + scriptural text — accuracy is sensitive** | One changed word changes the meaning | Text is **verbatim** from the original guide-text; each aayudh's original scriptural reference (Mudgala Purana, etc.) is shown on its page |
| **One scan = one object** | No confusing the guest | Removed "see other items"; QR and NFC both resolve to the same URL (ends the double-play conflict) |

---

## Section 4 — Research

> ❗ **This section gets filled in after real guest testing. Nothing here — no quote, no number — is fabricated.**

### Planned method

- **User interviews:** 3 family members (potential editors) + 5–8 guests, ages 8–80
- **Contextual observation:** watching guests actually scan a QR during the festival — noting friction points
- **Comparative analysis:** izi.TRAVEL, museum audio guides, temple-visit apps — what works, what doesn't

### Questions to answer

- "Museum" vs "aayudhe" (ritual weapons) — which framing feels less intimidating?
- Do people hesitate before scanning a QR code (virus fears)?
- How many seconds in do younger guests skip the audio?
- How many steps does NFC take on an older iPhone?
- Can a non-technical editor add a new aayudh — without help?

*(Real observations + direct quotes go here. No synthesized personas.)*

The full observation log, consent script, and interview-question kit are ready and waiting in CASE-STUDY-NOTES.md — usable the moment guests show up during the festival.

---

## Section 5 — Design decisions with rationale

> **Recruiter signal:** not "I built screens" but **"I did X because Y, and accepted trade-off Z."**

### 🎯 Decision 1 — One URL for both QR and NFC (no separate flows)

**Options:** (A) a different URL per method (QR → mobile web, NFC → app deep-link) · (B) one URL for both.

**Chose B because:**
- It eliminates the entire class of double-play conflicts — the browser reopens the same URL, not a new tab
- Less content-management surface — one source of truth per aayudh
- The guest doesn't need to care which trigger they used — the experience is identical

**Trade-off accepted:** can't track QR vs. NFC engagement separately (solvable later with a URL param).

### 🎯 Decision 2 — Color palette: a "puja invitation" palette instead of generic warm tones

**Before:** plain brown + cream — the single most common combo in AI-generated designs, zero distinctiveness.

**The journey:** First redesigned toward a "devghar palette" (vermillion-maroon + brass-gold + ivory). It still felt "not impressive enough" → instead of just retuning colors, built **3 fully distinct concepts** (structure + motif + interaction) and put them on a comparison page: **museum placard**, **puja invitation**, **diya light**. Chose **puja invitation** — a gold double-ring border, a "mudra" (seal) Play button, a cord-style progress bar.

**Final tokens:**

| Token | Value | Contrast (on cream bg) | Result |
|---|---|---|---|
| Body text | `#3a0f16` | ~14.9:1 | ✅ AAA |
| Maroon (primary) | `#7a1e2b` | ~9.2:1 | ✅ AAA |
| Muted | `#7a5c46` | ~5.4:1 | ✅ AA |
| Gold | `#8f6224` | ~4.8:1 | ✅ AA |

**Honest note:** the gold accent failed contrast **twice** at first (on small eyebrow-label text). Caught it with manual WCAG math and landed on the value above. **Lesson:** run the contrast math before trusting a color a palette tool hands you.

### 🎯 Decision 3 — Web font: none → Yatra One → back to none (system-ui)

Three deliberate phases:
1. **Start — "no web fonts":** the site is an offline PWA; the service worker only caches local assets.
2. **Added Yatra One** in the invitation-styled redesign — headings only; body text stayed on system-ui (a clean sans reads better for long paragraphs across an 8–80 age range).
3. **Removed it entirely** after font complaints — back to the system-ui stack (renders Devanagari cleanly too). Visual identity now comes from type scale/weight/spacing, with no external dependency.

**Lesson:** offline reliability vs. decorative typography — for this project, offline won.

### 🎯 Decision 4 — Icon-only buttons, without the accessibility bug

The play/pause button used to show text. The new design switched to an SVG icon — which quietly dropped the button's accessible name for screen readers. Caught during browser testing; fixed immediately by adding both `aria-label` and a visible label.

### 🎯 Decision 5 — JSON-as-CMS + a jsonlint guard

**Options:** (A) edit the JSON directly · (B) Airtable + n8n · (C) Google Sheets + n8n · (D) a custom admin panel.

**Currently A, with a cheap safety net:** a single `data.json`, edited in Notepad, a jsonlint.com check to catch mistakes, a copy-paste flow documented in the README. (C) — Sheets + n8n — is the longer-term goal; for now, one text file is enough for a household. **Trade-off:** a broken JSON takes the whole site down — hence the mandatory lint check.

### 🎯 Decision 6 — A big "mudra" Play button, no autoplay

**Constraint:** every mobile browser blocks autoplay, universally.

**Embraced it instead of fighting it:** the Play button became a design opportunity — a gold seal, double ring, a visual anchor. It sets an expectation: this is a chosen experience, not a passive one.

### 🎯 Decision 7 — Dark mode: built → tested → removed entirely

Built a full dark mode first and verified it against WCAG (AAA). But the unexpected brown theme confused the non-technical family. **Removed it entirely** — one theme, always. Lesson: even a theoretically-correct feature is a bug if it confuses the target user.

### 🎯 Decision 8 — Placeholder items → real aayudhe

Midway through, a detailed docx guide-text turned up (name + story + philosophical meaning + original scriptural reference for each item). Expanded scope. **Why it was safe:** the QR/NFC tags weren't printed yet, so there was no risk to the URL scheme. Text was taken verbatim.

### 🎯 Decision 9 — No icon in the QR code's center, a separate seal above it instead

Putting an icon in the QR's center caused a large share of codes to fail scanning under stress-testing (it ate into error-correction capacity). Moved the icon to a separate seal above the code → full pass. A decision the testing itself surfaced.

### 🎯 Decision 10 — Item-number badges (#001) — information, not decoration

The list shows `#001`, `#002`… This isn't decorative: the **same numbers** are on the physical QR/NFC tags, so the number in the list directly tells you which tag is which.

### 🎯 Decision 11 — New controls for longer audio (all reduced-motion-safe)

±10-second skip; gallery dots + counter; prev/next plus keyboard arrows in the lightbox. A pulse-ring while playing, staggered card entrances — both respect `prefers-reduced-motion`.

### 🎯 Decision 12 — "Aayudh-Chakra," a rotating wheel, instead of a list/card grid

**Before:** a simple scrollable list/card grid — functional, but it showed nothing of "how these 20 different objects relate to each other."

**New:** an Om at the center, 20 aayudhe on two concentric rotating rings around it — evoking a temple mandala/chakra. Auto-rotate (slow, pausable), drag-to-rotate, a center "suggest a random aayudh" button.

**Exploration:** didn't jump straight to this design — `design-demos/` holds **9 fully-built alternative concepts** (wheel, mala, featured, scroll, deck, bento, playlist, mandala, coverflow), preserved with code.

**Problem found and solved:** on mobile (measured at 375px), fitting all 20 nodes on one ring left the gap between neighbors below the minimum tap target — **the overlap was mathematically unavoidable, not something CSS could fix.** Solution: hide the ring entirely below 600px, replace it with a swipeable circle-row (Spotify/Instagram-Stories style).

**Lesson:** the assumption "one ring will fit every screen size" was wrong — only real measurement (node spacing at a 375px viewport) revealed it, not a guess.

### 🎯 Decision 13 — A new brand mark, and a separate simplified version for the favicon

Replaced the old inline kalash SVG icon with a new mark — the tip of the ankusha's hook forms a play-button triangle (Ganesh symbolism and "this is an audio guide" in one line). But the same detailed mark looked blurry at 16×16/32×32 favicon size — caught by zooming in before shipping, and built a separate simplified crop. One icon doesn't fit every size — true here too, same as Decision 12.

### 🎯 Decision 14 — Making the physical aayudhe: AI reference art → 3D print/clay → acrylic finishing

This part is different from the site's *software* half — it's the process of how the actual idol figures sitting in the mandap were made. Proof that "AI wasn't just for code — it went into physical craft too" — a rare digital + physical maker workflow combination.

**Pipeline (digital → physical, full tool chain):**
1. **Research** — gathered information from the puranas and a history book; used research tools and NotebookLM to pull all sources together into reference files (ties to Decision 8)
2. **AI reference art** — turned that research into prompts for each aayudh, generated reference images with **Google Flow**. Research initially covered 20+ aayudhe; due to space constraints, only **18-19 of them got a physical figure** actually placed in the mandap — the **20 aayudhe** on the digital site is a separate (fully-covering) count; the two numbers describe different things, they aren't inconsistent
3. **Physical fabrication — two methods, in parallel:**
   - **3D printing:** with time short, some aayudhe went from Google Flow images through **meshy.ai** to 3D models → prep and `.stl` editing in **Ultimaker** (software I didn't know beforehand, picked up as I went) → printed by a **local vendor** (didn't print it myself)
   - **Hand-sculpting:** some aayudhe were shaped in parallel from **Fevicryl clay**
4. **Finishing** — a black matte spray primer coat on pieces from both methods, then acrylic detail painting (golden, copper, metallic, brown for anything meant to read as wood)
5. **Sizing — a deliberate decision, not an aesthetic one:** each idol figure is roughly 8" tall; the stand is taller, roughly 10" — made of cardboard, finished in black spray paint. **Why 10":** (a) space was needed above the aayudh for a QR code + name label, (b) so the aayudhe wouldn't **overlap** each other when arranged together
6. **Backdrop** — black paper matching the theme, so each aayudh stands out visually
7. **QR layer** — a separate QR code per aayudh, plus one master QR for the main landing page

*(Full original note — HANDWRITTEN-NOTES-DIGITIZED.md, Marathi only.)*

**Intent:** puranic material tends to be dense, formal language, and some guests — especially older ones, or those who simply can't read it — can't access it that way, so an audio layer was added so the full text could be **heard**. That's the real accessibility reason, not technology added for its own sake.

**Framing:** modern technology (AI image generation, 3D printing, TTS, QR) doesn't **replace** a traditional Ganeshotsav decoration — it **carries its meaning to more people.** Not a parody, not a gimmick.

---

## Section 6 — AI-assisted design workflow

| Tool | Role | What the human did, what AI did |
|---|---|---|
| **Claude Sonnet 5 (Claude Code)** | Spec architect + implementation | I supplied the constraints; Claude drafted the build-spec and implemented the redesign (CSS/JS/HTML) |
| **`ui-ux-pro-max` skill** | Color/typography/style domain search | Suggested palette and font pairings; **final choice was mine** + manual WCAG math |
| **`design:design-critique` lens** | Review lens | A designer's-eye review of the existing site, then the redesign |
| **Claude Browser (in-app)** | Live testing | DOM / console / accessibility-tree + click-tests |
| **AI image tools (OpenArt / Seedream 4.5)** | Icon creation | App icon + aayudh badges AI-illustrated; remaining badges Claude drew as vector art |
| **Python (qrcode / Pillow / pyzbar)** | QR pipeline | Custom QR cards generated locally + pyzbar decode-verification + stress-testing (tilted/blurred/at a distance) |
| **Sarvam Bulbul v3 (TTS)** | **Voice for all 20/20 aayudhe** | Voice "ritu". **Speech-to-text run back over the audio to cross-check against the approved script** — an automated pronunciation-accuracy check, not just "sounded fine on listen." Ekadanta's (001) human recording was kept separate at first, but **later deliberately replaced with TTS too** — for consistency, with the original .wav kept safe on disk |

**Honest self-assessment:**
- **What AI did well:** repetitive scaffolding, syntax, edge-case enumeration, contrast math, QR stress-simulation
- **What I overrode:** the verbatim accuracy of religious/scriptural text, emotional design, the call to remove dark mode, the call to remove the font, prioritization
- **Lesson:** AI compresses execution time. Design judgment stays with the human.
- **Limitation:** pixel-level screenshot QA wasn't possible in this session; real device testing is still pending

### 🧾 Evidence Sheet

> No need to state this for every AI-assisted step — only where the decision genuinely affects how the work gets evaluated. Three places: brief → constraint → what AI gave → where the human overrode it → what shipped.

**1. Voice — the TTS decision**

| | |
|---|---|
| Brief | Consistent-quality voice needed for 20 aayudhe |
| Constraint | Recording 20 items solo, in time, wasn't feasible |
| AI gave | Generating the full text through TTS (Sarvam Bulbul v3) |
| Human override | Kept the text 100% verbatim from the original scripture; added an STT cross-check gate myself (not automatic in the tool) |
| Shipped | 20/20 voices, pronunciation-verified — even Ekadanta's original human recording was later swapped for consistency (Section 8 #12) |

**2. Color — the palette decision**

| | |
|---|---|
| Brief | Wanted distinctiveness instead of a generic warm-brown palette |
| Constraint | Just retuning colors turned out to be "not impressive enough" |
| AI gave | Color/font pairing options (via the `ui-ux-pro-max` skill) |
| Human override | Built 3 full structural concepts and chose between them; caught the gold accent failing contrast twice and fixed it with manual WCAG math |
| Shipped | The "puja invitation" palette, every token at AA/AAA contrast |

**3. Navigation — the aayudh-chakra layout**

| | |
|---|---|
| Brief | A list/card grid showed nothing of "how these 20 objects relate" |
| Constraint | Didn't want to jump blindly into a single ring design |
| AI gave | 9 alternative concepts (Claude Code, in `design-demos/`), with code |
| Human override | Chose, and measured directly on mobile (375px) — found the single-ring layout mathematically breaking, called for a different pattern |
| Shipped | A rotating wheel (desktop) + a swipeable row (mobile), verified by measurement |

### AI × UX, tied together — questions this comes up in interviews

> Recruiters/interviewers often ask, "You used AI, but where's the UX work?"

1. **"What was the real problem, and why did AI even come into it?"**
   The problem was a UX one (people don't know what the aayudhe mean, and don't have the time or inclination to read) — not a technology problem. AI wasn't part of deciding the solution (audio guide, QR/NFC, Marathi-first) — that decision came from research and constraints. AI came in during **implementation**: compressing the time from spec to build, and making it possible to produce 20 voices when recording them solo simply wasn't.

2. **"Where does your UX judgment show up in the AI's output?"**
   AI suggested design colors/fonts, but the final choice plus the WCAG math was mine. Choosing the TTS voice wasn't just "generate and use it" — the **STT re-verification** is a quality-gate step I added myself. That's exactly where UX/product thinking lives: deciding whether the AI's output can actually be trusted.

3. **"Isn't using an AI voice instead of a human one contradictory — in a project meant to preserve tradition?"**
   The original plan was a human voice. But recording 20 aayudhe at a consistent quality, solo, wasn't practical. **The choice:** kept the text 100% verbatim from the original scripture (authenticity of the content), used AI for the voice but added an accuracy check — STT cross-check — for the voice's reliability. *"Tradition was preserved in the text; technology was used to deliver it."*

### 🎙️ Voice selection — how much was actually tried (verified from the `audio-drafts/` folder in the repo)

"Just generated one voice and used it" doesn't cover it — 3 voices (priya/ritu/shreya) were compared, 3 tonal variants of ritu (intimate/lively/warm) were tested. One entirely different direction was also tried and dropped: a first-person, child-addressed script where "Bappa himself speaks to the kids" (3 drafts) — and for that, a child's voice was engineered through **two distinct technical methods** (a simple pitch-shift, and a WORLD-vocoder approach that separates pitch from formants) across 6+ iterations. Both were ultimately dropped in favor of a simple, trustworthy adult voice + verbatim text (confirmed: no reference to a baby/kid voice anywhere in `app.js`/`data.json`).

*(Full technical detail — pitch/formant parameters, every version's filename — lives in CASE-STUDY-NOTES.md, Marathi only.)*

---

## Section 7 — Testing & metrics

### Technical verification

The site's technical core has been independently checked: content (every item, no placeholders left), audio (20/20 real TTS), QR assets (branded, correct DPI/size, EC-Q error correction), QR decode and stress-testing (tilted/blurred/printed-and-photographed/at a distance — passes under every condition), and the live site (valid JSON, loads correctly). The detailed results table lives in CASE-STUDY-NOTES.md.

### ✅ SEO + Analytics — independently verified (22 Sep 2026)

> These are proofs of **technical implementation** (code + an external verification tool) — **not traffic/user numbers** (those live under "User metrics" below, marked ❗, and only arrive after real testing; vague phrases like "improved reach" are deliberately avoided here).

| Check | Result |
|---|---|
| Google Analytics 4 | ✅ found live in the site's code — Measurement ID `G-E3SHSB62WD`, `gtag.js` loads |
| Meta description / Open Graph / Twitter Card | ✅ all three found in `index.html` (og:title, og:description, twitter:card) |
| Structured data (JSON-LD) | ✅ **independently verified by Google's own [Rich Results Test](https://search.google.com/test/rich-results)** — "Crawled successfully on Sep 22, 2026" + "Carousels — 1 valid item detected" — meaning the structured data isn't just present in the code, Google considers it valid too |
| robots.txt / sitemap.xml | ✅ both present in the repo |

**Screenshot placeholder (also noted in the photo table above):** `seo-rich-results-proof.jpg` — I verified the result above by viewing it in the browser (the text proof in the table is real), **but the actual screenshot hasn't been saved as a file** — I can re-capture it if asked. And `analytics-dashboard.jpg` (GA4's actual dashboard — **only you can get this one**, it's behind your Google login, I have no access there).

### ❗ User metrics (pending — after guest testing)

| Metric | Result | Target |
|---|---|---|
| QR scan → first audio play, time | ❗ | < 10 seconds |
| Full-tour completion rate | ❗ | — (baseline to be established) |
| Items re-listened to (a delight signal) | ❗ | — |
| Non-technical editor added a new aayudh | ❗ | 3/3 |
| First month's bandwidth | ❗ | well within GitHub's 100GB limit |

### ❗ Direct guest quotes

> *(After real testing. None yet.)*

---

## Section 8 — What didn't work

> Most portfolios skip this section — that's exactly why it's here.

1. **Gold accent failed contrast twice** — caught with manual WCAG math and fixed. Lesson: don't trust a palette tool blindly, do the math first.
2. **The Yatra One web font** — added, drew font complaints, removed entirely. In the fight between offline safety and decorative typography, offline won.
3. **Dark mode** — built fully, WCAG-verified, but the unexpected brown theme confused the family. Removed.
4. **A center icon in the QR code** — a large share of codes failed to scan. Moved the icon out.
5. **The first hand-drawn icons were flat polylines** — later replaced with a more polished cubic-bezier + gradient version.
6. **Autoplay** — verified as blocked; didn't fight it, turned the Play button into a design opportunity instead.
7. **The first "devghar palette" redesign** — felt "not impressive enough." Lesson: tuning colors alone isn't a redesign; structure/motif/interaction have to change. The choice only became clear after building 3 full concepts.
8. **The "all pass" QR claim was premature, and the first design was fragile** — a careful re-run showed a significant failure rate under JPEG recompression. Root cause: rounded modules (decorative) + weaker error correction. rounded → **square modules**, EC-M → **EC-Q**, and rendering at an exact integer module size instead of resizing the QR — after all three changes, everything passed under every condition. Lesson: (a) record condition-by-condition numbers before writing "pass"; (b) decoration on a QR code (rounded corners, lower error correction, resizing) works against scannability — a plain square QR is the most reliable.
9. **A sequential-id cleanup had to be reverted** — tried making item ids gap-free (looked "cleaner"), but some items' QR/NFC tags were already printed/encoded against the old ids — scans started landing on the wrong item. Reverted, kept the original ids permanently. Lesson: any identifier tied to a printed, physical object should **never** be changed for the sake of tidiness — once it's "out," once, it stays fixed.
10. **The first attempt to fit all 20 aayudhe on one ring on mobile failed** — the nodes were mathematically overlapping (found by measurement, not guesswork). The fix wasn't CSS tuning — it needed an entirely different mobile pattern (a swipeable row).
11. **The new brand mark was illegible at favicon size** — caught by zooming in before shipping; had to build a separate simplified version. Lesson: one icon doesn't work at every size.
12. **The original "a human voice is the only authentic choice" decision was itself reversed** — Ekadanta's (001) recording was a real human voice, but it was later replaced with AI-TTS too, for consistency. There was a **genuine trade-off** between the original value (a human voice) and practicality (a consistent pipeline, scale) — and consistency won. Being upfront about that is the right call; hiding it would only raise more suspicion.
13. **"Bappa himself speaks to the kids" — neither the narrative direction nor the child-voice engineered for it shipped** — wrote a separate first-person, child-addressed script (3 drafts), and engineered a child's voice for it through two distinct technical methods (a simple pitch-shift, and a WORLD-vocoder approach separating pitch from formants) across 6+ tuning passes (details in Section 6). Ultimately chose the simple, trustworthy adult voice + verbatim-scripture direction instead. Lesson: trying a creative experiment and not shipping it isn't a failure — if anything, the confidence in the path that *was* chosen came directly from that experiment.

---

## Section 9 — What's next

- [x] Real audio — done (20/20, all AI-TTS — even Ekadanta's human recording was later replaced with TTS)
- [x] Homepage redesign — done (the "aayudh-chakra" rotating wheel + mobile swipe-row)
- [x] Brand mark/logo — done
- [x] SEO + analytics — done
- [~] Decoration video — a poster photo + a YouTube Shorts teaser are up; the real video file is still pending
- [ ] Physical steps — printing QR cards in color · a real phone-camera scan test · attaching NFC tags
- [ ] English — English audio + turning the English toggle back on
- [ ] Guest testing — invite guests, observe + interview → fill in Section 4 + 7
- [ ] CMS upgrade (optional) — a Google Sheets → n8n → JSON → GitHub push pipeline
- [ ] Icons — replace the remaining vector badges with AI-illustrated ones
- [ ] v2 — a productized service for multiple families / Ganeshotsav community mandals; a per-aayudh WhatsApp bot
- [ ] Custom domain
- [ ] Filling in the legal-name placeholder in `OWNERSHIP.md` (only you can do this)

---

## Section 10 — Toolkit

**Design:** `ui-ux-pro-max` / `design:design-critique` skills, manual WCAG audit
**Frontend:** HTML5, CSS3 (custom properties / tokens), Vanilla JS, PWA, Service Worker (offline + cache-versioning), Media Session API, Wake Lock API, `prefers-reduced-motion`
**NFC/QR:** NTAG213 tags + the "NFC Tools" app (physical), Python (qrcode, Pillow, pyzbar) QR generation + decode-verification pipeline
**Hosting:** GitHub Pages (free, auto-HTTPS)
**AI:** Claude Sonnet 5 / Claude Code (spec + implementation + review), Claude Browser (live DOM/a11y QA), OpenArt / Seedream 4.5 (iconography), Google Flow (reference art), meshy.ai (2D → 3D models), NotebookLM (research-source collation)
**Physical fabrication:** Ultimaker (print prep, `.stl` editing), a local 3D-print vendor, Fevicryl clay, acrylic + spray-paint finishing
**Accessibility:** WCAG 2.1 AA (manual contrast math), aria-label, keyboard nav, ≥44px targets, reduced-motion

---

## Section 11 — Contact / CTA

**Want something like this for your own home or community mandal?**
- LinkedIn: 【to fill】
- WhatsApp: 【to fill】
- Email: 【to fill】
- GitHub template: https://github.com/smartconnect2020-hash/Ganpati_ai_museum

---

# Publishing checklist

## Notion (primary)
- [ ] Every section filled with real content (Section 2's real memory, Section 4 + 7's testing data)
- [ ] Live demo loads in < 3 seconds
- [ ] All images as WebP, each < 200KB
- [ ] Cover image (1200×630, social sharing)
- [ ] Notion page → Public

## Medium (secondary)
- [ ] An 800–1200 word condensed version, cross-linked to Notion
- [ ] Tags: `UX Design`, `Case Study`, `AI Tools`, `PWA`, `Cultural Preservation`, `Indian Design`

## LinkedIn (traffic driver)
- [ ] A 5-slide carousel: problem → solution → key decision → metric → CTA
- [ ] A 60-second phone-recorded walkthrough
- [ ] Hashtags: `#UXDesign` `#ProductDesign` `#AITools` `#IndianDesign`

## Behance
- [ ] A strong hero image + process artifacts (the decision matrix, the 3-concept comparison board)

## GitHub (proof of build)
- [ ] Interaction GIFs in the README
- [ ] Setup instructions clear enough for a total stranger
- [ ] License: MIT

---

## Anti-cookie-cutter reminders

- [x] Verbatim "The Problem / My Role / User Research / Solution" headers **are not used**
- [x] Story-first, structure second
- [ ] Real quotes from real users (after testing)
- [ ] Real metric numbers (after testing) — no "improved satisfaction"-flavored sentences
- [x] A "what didn't work" section exists
- [x] AI workflow documented
- [x] Live demo works
- [x] A mobile-optimized case-study page — accordion decisions + a sticky thumb-zone CTA, using the site's own color tokens: [mobile artifact](https://claude.ai/artifact/F7wfyHKYJ52AFanUCaPaAj) (use the same pattern on whatever platform it's finally published to — Notion/webpage)
