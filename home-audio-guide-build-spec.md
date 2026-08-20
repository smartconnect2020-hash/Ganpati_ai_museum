# घर संग्रहालय — Audio Guide Web App (Build Spec v1)

> **Audience:** Claude Code / Cursor / Antigravity / any AI coding agent
> **Language:** Instructions in Marathi + English (tech terms preserved). Code comments in English. UI strings bilingual (Marathi default).
> **Goal:** एका webpage वर QR/NFC scan केल्यावर specific वस्तूची audio + photos + text story दिसते. 10 वस्तूंसाठी scalable, ₹0 hosting.

---

## 1. Core architecture decision (must-follow)

**One HTML page + URL parameter routing + JSON data source.** No frameworks. No build tools. No npm.

```
https://username.github.io/ghar-museum/?id=001   → Item 1
https://username.github.io/ghar-museum/?id=002   → Item 2
...
https://username.github.io/ghar-museum/          → Home / list of all items
```

**का हा approach:**
- 10 वस्तूंसाठी 10 HTML files नकोत — एकच `index.html`
- नवीन वस्तू add करायला फक्त JSON मध्ये entry — no code change
- QR आणि NFC same URL point करतात → **no double-play conflict** (browser same URL open करतो, दुसरा tab नाही)
- Content management non-technical person पण करू शकतो (JSON = text file)

---

## 2. Success criteria (definition of done)

- [ ] Guest QR किंवा NFC scan करतो → 3 seconds मध्ये page load होते
- [ ] Play button दिसतो (audio autoplay blocked in mobile browsers — verified)
- [ ] Tap केल्यावर audio सुरू होतो, photo gallery swipeable
- [ ] Marathi/English toggle (Marathi default, choice localStorage मध्ये save)
- [ ] सर्व 10 items same page structure वापरतात
- [ ] नवीन वस्तू add करण्यासाठी: `data.json` edit + `media/item-011/` folder add + git push (3 minutes)
- [ ] Offline-capable (PWA — first visit नंतर internet नसताना पण चालतो)
- [ ] Lock-screen वर audio controls (Media Session API)
- [ ] Audio सुरू असताना screen बंद होत नाही (Wake Lock API)

---

## 3. Tech stack (strictly locked)

| Layer | Choice | का |
|---|---|---|
| Frontend | Vanilla HTML + CSS + JavaScript | Framework overkill for 10 items. Loads instantly. |
| Data | Single `data.json` file | Text-editable, git-diffable, no database needed |
| Hosting | GitHub Pages | Free forever, HTTPS auto, custom domain optional |
| Audio format | MP3 (128kbps mono) | Universal support, small file size |
| Image format | WebP with JPG fallback | 30-50% smaller than JPG |
| Offline | Service Worker + Cache API (native) | PWA standards, no library |
| QR generation | qrcode-monkey.com (free) | Logo + color customization |
| NFC tags | NTAG213 stickers | Cheapest, universally compatible |
| NFC encoding | "NFC Tools" app (free, Android + iOS) | GUI, no dev knowledge needed |

**DO NOT install:** React, Vue, Svelte, Vite, webpack, npm packages, any bundler. **या project ला त्याची गरज नाही.**

---

## 4. File structure

```
ghar-museum/
├── index.html              # Single page — reads ?id= param, renders item
├── styles.css              # Mobile-first responsive CSS
├── app.js                  # URL routing, data loading, audio control, gallery
├── data.json               # All 10 items metadata (source of truth)
├── manifest.json           # PWA manifest (installable to home screen)
├── sw.js                   # Service worker for offline caching
├── icons/
│   ├── icon-192.png
│   └── icon-512.png
├── media/
│   ├── item-001/
│   │   ├── audio-mr.mp3
│   │   ├── audio-en.mp3
│   │   ├── 01.webp
│   │   ├── 02.webp
│   │   └── 03.webp
│   ├── item-002/
│   │   └── ... (same structure)
│   └── ... (up to item-010)
└── README.md               # Update workflow for non-technical family members
```

---

## 5. `data.json` schema (contract)

```json
{
  "meta": {
    "site_title": {
      "mr": "आमचं घर संग्रहालय",
      "en": "Our Home Museum"
    },
    "family_name": "Deshmukh",
    "version": "1.0"
  },
  "items": [
    {
      "id": "001",
      "title": {
        "mr": "आजोबांचं जुनं घड्याळ",
        "en": "Grandfather's Vintage Watch"
      },
      "year": "1952",
      "location": {
        "mr": "मुख्य hall showcase",
        "en": "Main hall showcase"
      },
      "audio": {
        "mr": "media/item-001/audio-mr.mp3",
        "en": "media/item-001/audio-en.mp3"
      },
      "images": [
        "media/item-001/01.webp",
        "media/item-001/02.webp",
        "media/item-001/03.webp"
      ],
      "story": {
        "mr": "हे घड्याळ 1952 साली आजोबांनी मुंबईहून विकत घेतलं...",
        "en": "This watch was bought by Grandfather from Bombay in 1952..."
      },
      "related_ids": ["003", "007"],
      "duration_sec": 45
    }
  ]
}
```

**Notes for the coding agent:**
- All 10 items start with placeholder content — user fills in real audio/photos later
- `related_ids` drives "similar वस्तू पहा" links at end of each item
- `duration_sec` shown in UI ("45 सेकंद ऐका")
- Add validation in `app.js` — if `id` doesn't exist, show friendly error page

---

## 6. Behavior spec (implement in `app.js`)

### 6.1 Page load flow
1. Parse `?id=` from `window.location.search`
2. `fetch('data.json')` → find matching item by id
3. If `?id=` missing → show home/list view with all items
4. If id not found → show error: "ही वस्तू सापडली नाही"
5. Render: title, year, location, big Play button, image gallery, story text
6. Load selected language from `localStorage.getItem('lang')` (default: 'mr')

### 6.2 Audio control (critical — mobile autoplay is blocked)
- **Do NOT attempt autoplay.** Show large centered Play button.
- On tap: `audio.play()` — wrap in try/catch (some browsers still throw)
- Show pause/play toggle, progress bar, current time / total time
- On audio end: show "पुन्हा ऐका" button + "इतर वस्तू पहा" links to related items
- Use `MediaSession API` to show controls on phone lock screen:
```js
navigator.mediaSession.metadata = new MediaMetadata({
  title: item.title[lang],
  artist: siteMeta.family_name,
  artwork: [{ src: item.images[0], sizes: '512x512', type: 'image/webp' }]
});
```

### 6.3 Wake Lock (screen stays on during audio)
```js
let wakeLock = null;
async function requestWakeLock() {
  try { wakeLock = await navigator.wakeLock.request('screen'); }
  catch (e) { /* not supported — silent fail */ }
}
// Call requestWakeLock() when audio play starts
// Release: wakeLock?.release() on pause/end
```

### 6.4 Language toggle
- Button top-right: "मराठी | English"
- On toggle: update all UI strings, swap audio source, save to localStorage
- Handle mid-audio switch: pause current, load new lang audio at 0

### 6.5 Image gallery
- Horizontal swipeable (CSS scroll-snap — no library needed)
- Tap image → full-screen modal, pinch to zoom (native browser)
- Lazy load (`loading="lazy"` attribute)

### 6.6 Re-scan protection (prevents double-play if guest re-scans within 30s)
```js
const lastVisit = localStorage.getItem(`last_visit_${id}`);
const now = Date.now();
if (lastVisit && (now - lastVisit) < 30000) {
  // Show non-intrusive banner: "तुम्ही ही वस्तू आताच पाहिली"
  // Don't auto-restart audio
}
localStorage.setItem(`last_visit_${id}`, now);
```

### 6.7 Home / list view (when no `?id=`)
- Grid of 10 cards, each shows thumbnail + title + year
- Tap card → navigate to `?id=00X`
- Show "visited" indicator on cards user has seen (from localStorage)

---

## 7. QR + NFC conflict handling (user's specific concern)

**Answer:** दोघे same URL point करत असल्यास conflict नाही.

| Scenario | काय होतं |
|---|---|
| Only QR scan | Browser opens URL → page loads |
| Only NFC tap | Browser opens URL → page loads |
| QR + NFC same item (accidental double trigger) | Browser same URL open करतो, नवीन tab नाही. Page load होते once. |
| QR + NFC different items rapidly | Browser navigates to second URL, first audio stops (browser default) |
| Re-scan same item within 30s | Section 6.6 handles — no auto-restart |
| Two guests scan different items on same phone | Both work — each opens new URL, previous audio stops |

**Design rule:** प्रत्येक वस्तूसाठी QR आणि NFC **exact same URL** encode करा. मग conflict चा प्रश्नच येत नाही.

---

## 8. PWA setup (offline capability)

### `manifest.json`
```json
{
  "name": "आमचं घर संग्रहालय",
  "short_name": "घर संग्रहालय",
  "start_url": "./",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#8B4513",
  "icons": [
    { "src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

### `sw.js` (service worker)
- Cache-first strategy for: HTML, CSS, JS, data.json, all media/
- On install: pre-cache shell (HTML/CSS/JS)
- On first item visit: cache that item's audio + images
- Result: guest ने एकदा tour केला की internet नसताना पण चालतो

Register in `index.html`:
```js
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('sw.js');
}
```

---

## 9. QR code generation (Layer 4 — aesthetic)

**Tool:** [qrcode-monkey.com](https://www.qrcode-monkey.com) (free, no login required)

**Per item:**
1. Content: full URL with `?id=001`, `?id=002`, etc.
2. Set Colors: 
   - Foreground: dark brown (#3E2723) for vintage वस्तू
   - Or family theme color
3. Add Logo (optional): family monogram / घराचं symbol (PNG upload, ~20% coverage max)
4. Frame: rounded / dotted (personal choice)
5. Error correction: **High (H)** — logo center मध्ये असल्यास important
6. Download: PNG, 1000x1000 px minimum
7. Print: minimum 3x3 cm on matte paper, laminate

**"Warli-styled QR" ला clarification:**
- QR Code Monkey मध्ये built-in Warli option **नाही**
- Custom Warli art wrap करायला Illustrator/Canva मध्ये manually design work लागतो
- Alternative: QR च्या background वर Warli border ठेव Canva मध्ये overlay करून

**Save all QRs** in `qr-codes/` folder (not committed to git — just for printing)

---

## 10. NFC tag setup (Layer 2)

**Hardware:**
- NTAG213 stickers, pack of 10-25 (Amazon India, अंदाजे ₹150-500 — **खरेदीपूर्वी listing verify**)
- No special reader needed

**Encoding:**
1. Install "NFC Tools" app (free, Android + iOS)
2. Open → Write → Add record → URL
3. Enter exact same URL as corresponding QR
4. Tap phone on tag → wait for confirmation
5. Optional: Lock tag (permanent — cannot re-write)

**Critical caveats (verified):**
- ⚠️ **NFC धातू frame मागे काम करत नाही** — फक्त लाकडी/plastic/cardboard/paper backing
- iPhone 6 आणि पूर्वीचे: NFC tag reading नाहीच → **QR fallback essential**
- iPhone 7/8/X: Control Center मधून NFC toggle करावा लागतो (guest ला माहित नसतं) → **QR backup**
- iPhone XR/XS (2018) आणि नंतरचे + आधुनिक Android: automatic background reading works

**Placement strategy:**
- वस्तूच्या base खाली (लाकडी बॉक्स/plate)
- Photo frame च्या cardboard backing च्या मागे
- Small wooden plaque वर stick करून next to वस्तू
- **कधीच** metal shelf / धातू फोटो frame ला मागे नको

---

## 11. Build order (for AI coding agent)

1. Ask user: repo name (default: `ghar-museum`), family name for greetings, first 3 वस्तू names (rest use placeholders)
2. Create `index.html` with:
   - HTML5 doctype, viewport meta (mobile-first)
   - `<link rel="manifest">`, service worker registration
   - Minimal semantic structure: `<header>`, `<main>`, `<footer>`
3. Create `styles.css`:
   - Mobile-first, max-width container 600px
   - System font stack (no web fonts — faster load)
   - CSS variables for colors (easy theme change)
   - Dark-mode support via `@media (prefers-color-scheme: dark)`
4. Create `app.js`:
   - Sections 6.1 through 6.7 above
   - Well-commented, functions <30 lines each
   - No external dependencies
5. Create `data.json` with 10 items (placeholders — user fills real content)
6. Create `sw.js` and `manifest.json` per Section 8
7. Create `icons/` — placeholder 192x192 and 512x512 (user replaces later)
8. Create `media/item-001/` through `media/item-010/` with placeholder audio + images (0.5-second silent MP3, single colored placeholder WebP)
9. Create `README.md` for family — steps 12-13 below in simple Marathi
10. Git commands ready to copy-paste (see Section 12)

**Do NOT do:**
- Don't add analytics libraries (privacy — home use)
- Don't add framework (`create-react-app`, `vite`, etc.)
- Don't add build step (`npm run build` — just static files)
- Don't add login/auth — public read-only
- Don't add comments in Marathi in code (English only for code comments)

---

## 12. Deployment steps (GitHub Pages)

```powershell
# Windows PowerShell
cd ghar-museum
git init
git add .
git commit -m "Initial home museum site"
git branch -M main

# Create repo on GitHub first (public), then:
git remote add origin https://github.com/YOUR_USERNAME/ghar-museum.git
git push -u origin main
```

**Then on GitHub:**
1. Repo → Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main`, folder: `/ (root)`
4. Save → wait 2-3 minutes
5. Live URL: `https://YOUR_USERNAME.github.io/ghar-museum/`

**Custom domain (optional):**
- Buy domain (₹800-1200/year, unverified — vendor-dependent)
- Settings → Pages → Custom domain → add
- Update DNS: CNAME record to `YOUR_USERNAME.github.io`

---

## 13. Update workflow (for family — non-technical)

**नवीन वस्तू add करायला:**
1. Phone वर 30-60 seconds audio record कर (Marathi आणि English वेगळे)
2. वस्तूचे 3 photos घे
3. Computer वर `media/` folder उघड → नवीन folder `item-011/` तयार कर
4. Audio आणि photos त्यात टाक (नावं exact: `audio-mr.mp3`, `audio-en.mp3`, `01.webp`, `02.webp`, `03.webp`)
5. `data.json` उघड (Notepad मध्ये चालतो) → last item नंतर copy-paste करून नवीन entry बदल
6. GitHub Desktop app मध्ये "Commit" + "Push" click कर
7. 2 minutes नंतर live
8. QR Code Monkey वर नवीन QR generate कर URL: `https://YOUR_URL/?id=011`
9. NFC Tools app मध्ये नवीन tag ला same URL write कर
10. वस्तूजवळ लाव

---

## 14. Cost breakdown (honest estimates)

| Item | Cost | Confidence |
|---|---|---|
| GitHub Pages hosting | ₹0 forever | ✅ Verified |
| Custom domain (optional) | ₹800-1200/year | ⚠️ Vendor-dependent |
| QR Code Monkey | ₹0 | ✅ Verified free |
| NFC Tools app | ₹0 | ✅ Verified free |
| 10 NTAG213 NFC stickers | ₹150-500 approx | ⚠️ Amazon India — verify listing |
| QR printing + lamination | ₹50-200 | ⚠️ Local Xerox shop |
| **Total for 10 items** | **₹200-700 (no domain)** | |
| With domain | ₹1000-1900 first year | |

---

## 15. Testing checklist (before showing to guests)

- [ ] URL `?id=001` opens correctly on Chrome Android
- [ ] Same URL opens correctly on Safari iOS
- [ ] Play button visible immediately, audio plays on tap
- [ ] Image gallery swipes smoothly
- [ ] Language toggle works, choice persists on next visit
- [ ] QR scan opens correct item (test all 10)
- [ ] NFC tap opens correct item (test on iPhone XR+ and Android)
- [ ] Re-scan within 30s doesn't restart audio
- [ ] Lock screen shows audio controls (MediaSession)
- [ ] Screen doesn't dim during audio (Wake Lock)
- [ ] Airplane mode → site still loads (PWA offline)
- [ ] "Add to Home Screen" works from browser menu
- [ ] Related items links work at end of audio

---

## 16. Known limitations (be honest with user)

1. **Mobile audio autoplay blocked** — universal browser policy. Play button unavoidable. Design accepts this.
2. **NFC metal-blocking** — physical constraint. QR backup mandatory.
3. **iPhone 6 and earlier** — no NFC tag reading. QR only.
4. **iPhone 7/8/X** — Control Center toggle needed. Not ideal UX. Print small instruction card near vastu: "iPhone जुना असल्यास QR वापरा".
5. **First visit needs internet** — service worker installs on first load, then offline works.
6. **JSON edit errors** — one wrong comma breaks site. README should explain and provide a JSON validator link (jsonlint.com).
7. **Bandwidth** — GitHub Pages soft limit ~100GB/month. For home use, plenty.

---

## 17. Smart innovations built into this spec

1. **Single URL scheme** eliminates QR/NFC conflict entirely
2. **JSON-as-CMS** = non-technical updates
3. **PWA offline** = works without internet after first visit
4. **MediaSession** = lock-screen controls (feels native)
5. **Wake Lock** = screen doesn't dim mid-story
6. **Re-scan detection** = prevents accidental restarts
7. **Related items linking** = guest naturally flows through home tour
8. **Bilingual toggle** with persistence = works for family + English-speaking guests
9. **No framework, no build** = 15-year maintenance friendly (family members can edit HTML/JSON directly forever)
10. **Static site + git version history** = every change is tracked, can roll back mistakes

---

## 18. Handoff acceptance test (for AI coding agent)

Before declaring "done":
- Open site in phone browser without internet (after one online visit)
- Scan QR on wooden picture frame — item should load, play button visible, audio plays on tap
- Toggle language — audio switches, UI text switches
- Close browser, re-scan — should recognize recent visit
- Add a fake 11th item to data.json + placeholder folder → verify it appears on home page

**If any of the above fails, do not mark spec as complete.**

---

*End of spec. Version 1.0. Total build time estimate: 2-4 hours for coding agent, plus 4-6 hours for user to record all audio + take photos + generate QRs + encode NFCs.*
