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

### 🧭 When, where, and what for — really

The timing was simple — Ganeshotsav 2026 was coming up, and this had to be live sometime between deciding on the decoration (August) and the festival starting. The "where" is a little more interesting, because this was built for two places at once: the actual mandap at home, and an offline-first PWA that has to keep working even on patchy home WiFi.

And "why" doesn't fit in one line, but here's an attempt: the guide-text stays shut in a cupboard, it never reaches relatives who live elsewhere, and even for the ones who do read it, some find it hard going. Put more formally —

> Guests visiting for Ganeshotsav, and relatives who live too far away to visit, want to understand the meaning behind Ganpati's ritual weapons/attributes, **because** the current guide-text takes time and inclination to read that people don't have, and it simply never reaches the ones who can't be there in person.

*(5W1H framework — [Orbix](https://www.orbix.studio/blogs/5-ws-in-ux-design); the line above follows NN/g's "user + need + insight" pattern.)*

---

## Section 2 — How it started

*First person. No jargon.*

This year, while planning a new kind of home decoration, we settled on Ganpati's ritual weapons/attributes as the theme — and immediately realized: most people don't actually know what these aayudhe are or what they're called (beyond 2-3 of them). So I started gathering that information — from the puranas, from a history book.

Then the real question hit me: **how do I show this to relatives who live too far away to visit?** The answer: a QR code for every aayudh — since everyone has a phone and a scanner in their pocket these days. So I built a free website (from a GitHub repo, with Claude's help), and mapped all the information onto it.

But reading plain text turned out to be hard for some people — especially older relatives and young kids. So I decided to add audio, with AI's help. And to make sure this information reached as many people as possible, I added SEO and Analytics to the site.

*(Based on two real handwritten notes — the first paragraph is from the "physical decoration" note, the rest from the "QR/website" note; the connecting thread between the two notes ["decided on the aayudhe" → "the question of showing relatives"] is my own inference, not written verbatim in that sequence in the notes. Full original text — HANDWRITTEN-NOTES-DIGITIZED.md, Marathi only.)*

---

## Section 3 — Why this isn't a "solved problem"

This was never just a technical showcase — every decision below traces back to a real limit, and that limit is what pushed the design in a particular direction.

The first limit was money — spending on hosting for a home project wasn't something I could justify, and if any other household wanted to use this too, the same had to hold for them. So ₹0 hosting became a hard rule — GitHub Pages (free, auto-HTTPS), QR codes generated in-house with Python, and NFC tags costing only ~₹15 each.

Second — I won't always be the one maintaining this; someone else in the family needs to be able to edit the text tomorrow, and that person isn't technical. So no heavyweight CMS or database — a single `data.json` file, editable straight in Notepad, a jsonlint.com check to catch mistakes, and a three-minute flow written into the README.

Guests range from age 8 to 80 — meaning the UI couldn't be built for just one generation. Marathi stayed the default language, the font stayed on system-ui, and tap targets got sized up (the "mudra" Play button is 80px, the ±10s skip is 48px — everything at least 44px). And phones aren't uniform either — someone's on an iPhone 6, someone else on a budget Android — so modern NFC couldn't be assumed. QR stayed primary, NFC secondary, with a simple placard note for older iPhones.

Home WiFi is unreliable some days — so this couldn't depend on the internet. Built it as a PWA with a Service Worker, cache-first — once you've visited once, the photos, audio, and fonts are all saved offline.

The most sensitive limit was the text itself — this is religious and scriptural material, and one changed word changes the meaning. So the text stayed verbatim from the original guide-text, and each aayudh's original scriptural reference (Mudgala Purana, etc.) is shown right on its page — so if anyone ever questions it, the source is right there.

And finally, one simple rule I set for myself: one scan means one object, nothing more confusing than that. So options like "see other items" got removed, and QR and NFC both resolve to the same URL — which also quietly ended the problem of two audios playing at once.

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

## Section 5 — Design decisions — why, how, and where I got it wrong

There's a reason behind every decision below — sometimes a technical snag, sometimes someone in the family just said "I don't like this," sometimes something I only found testing at midnight. Here it is, roughly how it actually happened.

### 🎯 One URL for both QR and NFC

At first I figured QR would get one URL and NFC another — then it hit me that meant maintaining the same thing in two places, and why should it matter to a guest whether they scanned or tapped? Gave both the same URL. That also quietly killed an entire class of bugs — two tabs open, two audios playing at once — because the browser just reopens the same URL instead of a new tab. One thing I did give up: I can't separately count how many people came via QR versus NFC. That's solvable later with a URL parameter, but it wasn't the priority right now.

### 🎯 Color — changed three times before it finally felt right

The first pass was plain brown-on-cream — then I noticed that's basically the combo every AI-generated design reaches for, nothing about it felt like *us*. Tried a "devghar palette" next (vermillion-maroon + brass-gold + ivory) — still felt "not impressive enough." That's when it clicked: retuning colors wasn't going to fix it, the structure itself needed to change. So I built three completely different directions at once — one like a museum placard, one like a wedding invitation, one like diya-light — and put them side by side on a comparison page. The "puja invitation" direction won: a gold double-ring border, a Play button shaped like a temple seal, a progress bar that looks like a cord.

Even after the colors were locked in, one thing lingered — the gold accent failed the contrast test twice (on small eyebrow-label text). It looked fine to the eye, but the math doesn't lie. Caught it with manual WCAG math and fixed it: final tokens — body text `#3a0f16` (14.9:1, AAA), maroon `#7a1e2b` (9.2:1, AAA), muted `#7a5c46` (5.4:1, AA), gold `#8f6224` (4.8:1, AA). Simple lesson: whatever color a palette tool hands you, run the math before you trust it.

### 🎯 Added a font, then took it back out

I'd decided early on — no web fonts, period — because the site is a fully offline PWA and the service worker only caches local assets. Then, in the invitation direction, I gave in a little: added Yatra One, headings only, kept body text on system-ui (long paragraphs across an 8-to-80 age range just read better in a clean sans). Then font complaints started coming in, and I asked myself — why take this risk at all? Pulled it entirely, back to the system-ui stack, which renders Devanagari cleanly too. Now the identity comes purely from type scale, weight, and spacing — no outside dependency. Between offline reliability and decorative typography, offline won.

### 🎯 Went icon-only, and a bug hid inside it

The play/pause button used to have text on it. The new design switched to plain SVG icons — looked cleaner, but it quietly stripped the button's name for screen readers. I found this myself while testing in the browser. Fixed it right away with an `aria-label` plus a visible label underneath — a five-minute fix, but if I hadn't caught it, it would have stayed broken indefinitely.

### 🎯 Wanted Google Sheets, ended up with a plain JSON file

The original plan was Google Sheets + n8n, so anyone at home could edit an aayudh. In practice that much setup wasn't needed yet — a single `data.json`, opened and edited in Notepad, checked against jsonlint.com to catch mistakes, with the flow written into the README. Turned out to be enough. The one real risk: one misplaced comma in that JSON and the whole site goes down, which is why the lint check is non-negotiable. Sheets + n8n is still the longer-term goal, but for now a household gets by fine on one text file.

### 🎯 Made peace with no autoplay, made the Play button worth looking at

Every mobile browser blocks autoplay, universally — not something worth fighting. Instead I made the Play button itself the focal point — a gold seal, a double ring, a clear visual anchor. It quietly sets an expectation: you're starting this yourself, it isn't going to just happen to you.

### 🎯 Built dark mode, then removed it completely

Built a full dark mode, verified it against WCAG, got it to AAA — technically everything checked out. But someone in the family looked confused by the unexpected brown theme. I stopped and asked myself — if it's confusing the very family it's built for, what good is "technically correct"? Pulled it entirely; there's one theme now, always. A feature can be a genuine gimmick and still be the right one to cut if it becomes a bug for the actual user.

### 🎯 From placeholder items to the real aayudhe

Work started with just a handful of placeholder items. Partway through, a detailed docx guide-text landed in my lap — name, story, philosophical meaning, the original scriptural reference, all of it. Expanded scope right away. It was safe to do because the QR/NFC tags weren't printed yet, so there was no risk to the URL scheme. Took the text verbatim.

### 🎯 Moved the icon out of the QR code

The first version had an icon right in the QR's center — looked great. But under stress-testing, a large share of codes failed to scan — the icon was eating into the error-correction capacity. Found that by actually testing it, not by guessing. Moved the icon to a separate seal above the code, and every code started scanning again.

### 🎯 The #001, #002 numbers aren't decoration

Every item in the list carries a number like `#001`, `#002`… not for looks. The exact same number is printed on the physical QR/NFC tag, so the number in the list tells you directly which tag you're looking at.

### 🎯 Added new controls once the audio got longer

Play/pause alone stopped being enough once the audio got substantial — added a ±10-second skip, dots and a counter in the gallery, prev/next plus keyboard arrows in the lightbox. A soft pulse-ring when playing, cards entering in a stagger — all of it built to respect `prefers-reduced-motion`.

### 🎯 Replaced the list with "Aayudh-Chakra," a rotating wheel — the biggest redesign of the project

A simple scrollable list or card grid worked fine, but it lost something — nowhere did it show that these twenty different objects actually relate to each other. So I put an Om at the center and arranged all twenty aayudhe on two concentric rotating rings around it, aiming for the feel of a temple mandala or chakra. It auto-rotates slowly (and can be paused), you can drag it to spin it yourself, and there's a "suggest a random aayudh" button at the center.

I didn't jump straight to this design — `design-demos/` still holds nine completely different concepts I built first (wheel, mala, featured, scroll, deck, bento, playlist, mandala, coverflow), all preserved with code. Even after choosing the wheel, one problem surfaced: on mobile (measured at 375px, not guessed), fitting all twenty nodes onto a single ring left less space between neighbors than the minimum tap target allows. That overlap was mathematically unavoidable — no amount of CSS tuning was going to fix it. So the ring disappears entirely below 600px, replaced by a swipeable row of circles, Spotify or Instagram Stories style. My assumption that one ring would fit every screen size turned out to be wrong — and I only found that out by measuring, not by guessing.

### 🎯 Built a new brand mark — and it disappeared at one size

Replaced the old inline kalash icon with a new mark — the tip of the ankusha's hook curves into a play-button triangle, so Ganesh symbolism and "this is an audio guide" both land in one shape. But before shipping I zoomed in to check the favicon, and the same detailed mark turned into a blurry smudge at 16×16/32×32. Had to build a separate, simpler crop just for that size. Same lesson as the wheel — one design doesn't survive every size, you have to actually look at each one.

### 🎯 Making the physical aayudhe — where the work left the screen entirely

This part is a different animal from the software side of the site — it's the story of how the idol figures actually standing in the mandap got made. AI wasn't just for code here; it went into physical craft too, and this is the part of the project that shows that most clearly.

I started by reading through the puranas and a history book, then pulled everything into NotebookLM to collate it into reference files (this later fed into the docx guide-text from Decision 8). From that research I wrote prompts for each aayudh and generated reference images with Google Flow. Research initially covered more than twenty aayudhe, but space ran out — in the end only 18-19 of them actually got a physical figure placed in the mandap. (The digital site still has all twenty — that's a separate, fully-covering count; the two numbers are about different things, not a contradiction.)

With time short, I decided some aayudhe would be 3D printed — Google Flow's images went through meshy.ai to become 3D models, then into Ultimaker for prep and `.stl` editing (software I didn't know at all going in, picked it up as I went), and a local vendor did the actual printing — I didn't print it myself. In parallel, some aayudhe were shaped by hand from Fevicryl clay instead. Pieces from both methods got a black matte spray primer first, then acrylic detailing on top — golden, coppery, metallic-looking finishes, brown for anything meant to read as wood.

The sizing was a deliberate call, not an aesthetic one — each figure is roughly 8" tall, the stand beneath it taller still, around 10", made of cardboard and finished in black spray paint. The stand was made tall on purpose: there needed to be room above each aayudh for a QR code and a name label, and it also kept the aayudhe from overlapping each other once they were all arranged together. Black paper went behind everything so each piece would stand out. And finally, each aayudh got its own QR code, plus one master QR pointing to the main landing page.

*(Full original note — HANDWRITTEN-NOTES-DIGITIZED.md, Marathi only.)*

Why do all this — puranic language is dense and formal, and some guests, especially older family members or anyone who simply can't read it, can't get at it that way. Adding an audio layer meant the full text could be *heard* instead — that's the real accessibility reason, not technology for its own sake. And in one line: modern technology here — AI image generation, 3D printing, TTS, QR — doesn't replace a traditional Ganeshotsav decoration, it carries its meaning to more people. Not a parody, not a gimmick.

---

## Section 6 — How I actually worked with AI

I built this whole thing solo — but "solo" doesn't mean without AI. If anything, without it this wouldn't have come together in time. The line between what AI did and what I decided is a clean one though, laid out below.

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

### 🎤 Other questions this project comes up in — and answers that aren't generic

> Not every interview question is about AI — some are just an interviewer being skeptical of a solo project. Each answer below is anchored to one real moment in the project, not stock advice.

1. **"Why solo? Wouldn't a team have helped?"**
   Maybe — but a team wouldn't have caught a QR failing to scan under stress-testing and re-run the test myself within the hour, or reverted a sequential-id "cleanup" the moment it started breaking scans. Working solo means no middleman between a decision and its consequence, so mistakes surface fast and get fixed fast. The real cost is obvious too — no second pair of eyes — which is exactly why I leaned on Claude's Browser tool to check the accessibility tree itself, and on running my own honest self-review, as a deliberate substitute.

2. **"This is built for one household — how do you argue it 'scales' in front of a company?"**
   I'd flip the question: I put this much care into a single non-technical user — a 3-minute content-editing flow, a hard rule about never changing an item id, a separate icon crop for every size that needed one — precisely because that same discipline is what won't break if it's applied to 100 households, or a whole Ganeshotsav community mandal. Scale is something you add later; getting it right for one real, demanding user first is the actual foundation.

3. **"Guest testing hasn't even happened yet — so how can you claim this 'works'?"**
   I don't. Section 7 deliberately leaves the user-metrics table marked ❗ and empty — not one number in there is a guess. What I *can* claim is narrower: the technical core (QR decode, stress-testing, SEO/structured data — independently verified by Google's own Rich Results Test) is solid. Not conflating "this is technically sound" with "people find this useful" is the honest position — and, per the research I did on this, honesty is exactly what impresses a recruiter more than polish does.

4. **"What's the biggest mistake you made that you could have avoided?"**
   Trying to make the item ids sequential "for tidiness" (Section 8 #9). Changed them to close the gaps, and six items' QR/NFC tags were already printed against the old ones — scans started landing on the wrong item. It was avoidable with one rule set up front: never change a number tied to a physical object. That rule exists now — it just took a mistake to learn it.

5. **"If you started over, what would you do differently?"**
   I'd test the aayudh-chakra on mobile earlier. The overlap problem at 375px surfaced late, close to shipping — caught in time, but only by luck. Testing each of the 9 design-demos concepts on mobile as I built them would have saved a whole extra pass.

6. **"Why Marathi-first? Wouldn't starting in English reach a bigger audience?"**
   Because the real user — the guest at home, the relative living elsewhere — thinks and reads and listens in Marathi. Starting in English would have made that exact person secondary in their own project. The English toggle already exists in the site (currently hidden, waiting on the content) — but the priority never got flipped, because sidelining the real user for "wider reach" felt like the wrong trade.

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
