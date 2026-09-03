# श्री गणेश आयुधे — UX केस स्टडी (पहिला मसुदा)

> **स्थिती:** पहिला draft. Sections 5 व 6 मध्ये `DESIGN-DECISIONS.md` मधला खरा मजकूर विलीन केला आहे.
> Section 4 (research) आणि Section 7 (user metrics) **मुद्दाम मोकळे** — खरं guest testing झाल्यावरच भरायचे, इथे काहीही fabricate केलेलं नाही.
> **खुणा:** `【युजरने भरायचं】` = वैयक्तिक/खरी आठवण · `❗` = testing नंतरचा भाग · `【पडताळा】` = तपासून खात्री करायची गोष्ट.
> **Source of truth:** `PROJECT-STATUS.md` (25 Aug 2026), `DESIGN-DECISIONS.md` (21 Aug 2026), git log (20–31 Aug 2026), `styles.css` / `app.js` (verified), live site.
>
> **पडताळणीची स्थिती (प्रामाणिकपणे, १ Sep 2026 ला स्वतंत्र तपासणी):**
> - ✅ *कोड/फाइल पाहून खात्री:* रंग-टोकन (styles.css), Wake Lock + Media Session API (app.js), build-spec = १८ विभाग, git-तारखा, आयटम-संख्या = २३ (data.json), फाँट/dark-mode काढल्याच्या नोंदी (styles.css कमेंट्स), कंटेंट पूर्ण + placeholder-मुक्त (data.json), आवाज १ खरा/२२ placeholder, QR DPI 300 + चौरस ~५.८ सेमी + रुंदी ७.६ सेमी + EC-Q + square modules (`_generate_qr.py`), center-logo-काढल्याचं कारण.
> - ⚠️ *बाकी छोटं:* home QR कार्डवर अजून जुनं नाव "आमचं घर संग्रहालय"; कार्ड-उंची आयकॉन-बॅजनुसार बदलते (~१०.५ सेमी आयटम, ~८.५ home).
> - ✅ *re-run केला (१–२ Sep):* सुरुवातीला QR stress-test JPEG q45 वर १७/२४ होतं (rounded modules + EC-M). कार्ड्स **square modules + EC-Q** वर बदलले → आता **सर्व ५ परिस्थितींत २४/२४**, तिन्ही प्रिंट-फॉरमॅटमध्ये (~३.८ सेमी scale वरही). तपशील Section 7 + 8.
> - ✅ *अंशतः:* live साइट प्रतिसाद देते, हेडिंग "श्री गणेश आयुधे", live `data.json` = वैध JSON २३ आयटम्स (local शी जुळतं). आयटम-यादीचं render + 375px खऱ्या ब्राउझरमध्ये तपासा.
> - ❌ *reproduce अशक्य:* "२९९/२९९ fields" — स्रोत docx repo मध्ये नाही, checker script नाही.
> - ❓ *अज्ञात — केस स्टडीत लिहिण्याआधी नक्की करा:* एकदंत (००१) ऑडिओचा स्रोत (खरा रेकॉर्ड की AI); QR pipeline scripts कुणी लिहिले; काम part-time की full-time.

---

## Section 0 — Hook

# मी घरातल्या गणपतीच्या मूर्तीला ऑडिओ गाईड दिला. प्रत्येक आयुधाची स्वतःची कथा आहे.

*QR / NFC स्कॅन करा — बाप्पाच्या हातातल्या २३ आयुधांची (एकदंत, परशू, अंकुश, सुदर्शन चक्र, खट्वांग…) मराठी ऑडिओ कहाणी, मूळ ग्रंथसंदर्भासह. ₹० होस्टिंगवर, framework शिवाय, ऑफलाइनही चालतं.*

**[▶ लाइव्ह डेमो](https://smartconnect2020-hash.github.io/Ganpati_ai_museum/)** &nbsp;&nbsp; **[GitHub](https://github.com/smartconnect2020-hash/Ganpati_ai_museum)** &nbsp;&nbsp; **[केस स्टडी वाचा ↓]**

---

## Section 1 — TL;DR box (recruiter चा १५-सेकंद scan)

```
Problem      →  गणपतीच्या मूर्तीतल्या प्रत्येक आयुधाला शास्त्रीय अर्थ आहे —
                पण उत्सवात पाहुण्यांना/मुलांना तो सांगणारं कुणी नसतं;
                गाईड-ग्रंथ कपाटात बंद राहतो
Solution     →  QR + NFC ऑडिओ गाईड, २३ आयुधे, मराठी-first, offline PWA,
                मजकूर मूळ ग्रंथातून verbatim
My role      →  एकटा — संशोधन + UX + व्हिज्युअल डिझाइन + no-framework build
                + QR/NFC pipeline + AI-workflow orchestration
Timeline     →  २० Aug 2026 पहिला commit (साइट लगेच live) → ३१ Aug शेवटचा
                code commit (~१२ दिवसांचा commit-पट्टा; रोजचे तास 【पडताळा】)
Stack        →  Vanilla HTML/CSS/JS · PWA + Service Worker · single data.json
                · Python (qrcode / Pillow / pyzbar) · Claude Code · AI image tools
Results      →  ❗ Guest testing बाकी — तांत्रिक पडताळणी पूर्ण (QR 24/24 decode,
                299/299 content fields, live 200 OK, 375px mobile layout)
Impact       →  Maharashtra मधल्या घरांसाठी / गणेशोत्सव मंडळांसाठी productizable template
```

---

## Section 2 — सुरुवात कशी झाली

*First person. Jargon नाही. २ छोटे परिच्छेद.*

> **【युजरने भरायचं — खरी आठवण】** खालचा मजकूर मसुदा आहे, repo मधल्या तथ्यांवर आधारित. तुमची खरी आठवण टाकून हा अंतिम करा.
>
> गणेशोत्सवात घरी येणारे पाहुणे बाप्पाच्या मूर्तीसमोर उभे राहतात, हात जोडतात — आणि पुढे सरकतात. मूर्तीच्या प्रत्येक हातात एक आयुध असतं: कुठे परशू, कुठे अंकुश, कुठे खट्वांग. प्रत्येकामागे मुद्गल पुराण / शिव पुराणातली एक कथा आणि एक दार्शनिक अर्थ आहे. आमच्याकडे तो सगळा मजकूर एका गाईड-ग्रंथात होता — पण ग्रंथ कपाटात, आणि उत्सवाच्या गडबडीत कुणी उघडून वाचत नाही.
>
> UX designer म्हणून मला प्रश्न पडला: ही माहिती **वस्तूच्या जागीच, ऐकता येईल अशी** का नाही? Album किंवा लेक्चर फार formal. मुलाला किंवा ७० वर्षांच्या काकांना सारखीच सोपी वाटेल अशी गोष्ट हवी होती — फोन काढा, स्कॅन करा, ऐका.
>
> *(पडताळण्याजोगं तथ्य, वापरता येईल: `००३ अंकुश` ला `ankush.jpg` हा घरातला खरा कुटुंब-फोटो गॅलरीत पहिला आहे — बाकी २२ आयुधांचे फोटो AI-जनरेटेड turnaround शीट्स आहेत. या एका खऱ्या फोट्याभोवती वैयक्तिक आठवण गुंफता येईल.)*

---

## Section 3 — हा solved problem का नाही (constraints ने डिझाइन ठरवलं)

> **Recruiter signal:** Constraints स्पष्ट दाखवल्या की systems-thinking दिसतं.

| Constraint | का महत्त्वाचं | Design implication |
|---|---|---|
| **बजेट: ₹० होस्टिंग** | कुठल्याही घराला परवडलं पाहिजे | GitHub Pages (free, auto-HTTPS); QR स्वतः Python ने generate (बाह्य paid साइट नाही); NFC ~₹१५/टॅग |
| **कंटेंट-संपादक: non-technical कुटुंबीय** | माझ्याशिवाय मजकूर बदलता आला पाहिजे | एकच `data.json` (text file) + Notepad + jsonlint.com तपासणी + README मध्ये ३-मिनिटांचा flow. *(स्पेकमध्ये Google Sheets + n8n होतं; प्रत्यक्षात pipeline अजून जोडलं नाही — म्हणून सध्या सरळ JSON)* |
| **पाहुणे वयोगट ८ ते ८०** | UI सर्व पिढ्यांना चालला पाहिजे | Marathi default, system-ui फाँट, मोठे tap-targets (मुद्रा Play ८०px, ±१०s skip ४८px, lightbox nav ४८px — सर्व ≥४४px) |
| **डिव्हाइस: iPhone 6 ते 15, स्वस्त Android** | आधुनिक NFC गृहीत धरता येत नाही | QR नेहमी primary, NFC secondary; जुन्या iPhone साठी placard सूचना |
| **घरात patchy WiFi** | इंटरनेटशिवाय चाललं पाहिजे | PWA + Service Worker, cache-first; पहिल्या भेटीनंतर फोटो/ऑडिओ/फाँट offline |
| **धार्मिक + शास्त्रीय मजकूर — अचूकता संवेदनशील** | एक शब्द बदलला तरी अर्थ बदलतो | मजकूर मूळ गाईड-ग्रंथातून **verbatim**, प्रोग्रामने पडताळून (२९९/२९९ फील्ड जुळल्या); प्रत्येक आयुधाचा मूळ ग्रंथ-संदर्भ (मुद्गल पुराण इ.) पानावर दाखवला |
| **एक स्कॅन = एक वस्तू** | पाहुण्याचा गोंधळ नको | "इतर वस्तू पहा" काढलं; QR व NFC एकाच URL वर (double-play conflict संपला) |

---

## Section 4 — Research

> ❗ **हा विभाग खऱ्या guest testing नंतर भरायचा. इथे एकही quote किंवा आकडा fabricate केलेला नाही.**

### नियोजित पद्धत (अजून झालेली नाही)

- **User interviews:** ३ कुटुंबीय (संभाव्य संपादक) + ५–८ पाहुणे, वयोगट ८–८०
- **Contextual observation:** गणेशोत्सवात पाहुणे प्रत्यक्ष QR स्कॅन करताना बघणे — friction points नोंदवणे
- **Comparative analysis:** izi.TRAVEL, museum audio guides, मंदिर-दर्शन अ‍ॅप्स — काय जमतं, काय नाही

### भरायचे प्रश्न

- "संग्रहालय" vs "आयुधे" — कुठली framing कमी intimidating वाटते?
- QR स्कॅन करण्याआधी लोक कचरतात का? (virus भीती?)
- तरुण पाहुणे ऑडिओ किती सेकंदांनी skip करतात?
- जुन्या iPhone वर NFC किती steps लागतात?
- non-technical संपादकाला नवीन आयुध जोडता येतं का — मदतीशिवाय?

*(खरी observation + थेट quotes इथे. Synthesized personas नकोत.)*

---

## Section 5 — Design decisions with rationale

> `DESIGN-DECISIONS.md` (21 Aug) + नंतरचे खरे निर्णय (git log, PROJECT-STATUS §7) इथे विलीन केले.
> **Recruiter signal:** "मी screens बनवले" नाही — **"मी X केलं कारण Y, आणि Z trade-off स्वीकारला."**

### 🎯 Decision 1 — QR व NFC साठी एकच URL (वेगळे flows नाहीत)

**पर्याय:** (A) प्रत्येक method ला वेगळी URL (QR → mobile-web, NFC → app deep-link) · (B) दोन्हीला एकच URL.

**B निवडलं कारण:**
- संपूर्ण double-play conflict class नाहीशी होते — browser तीच URL पुन्हा उघडतो, नवीन tab नाही
- Content-management surface कमी — प्रति-आयुध एकच source of truth
- पाहुण्याला कुठलं trigger वापरलं याची पर्वा नाही — अनुभव सारखाच

**Trade-off स्वीकारला:** QR vs NFC engagement वेगळं track करता येत नाही (नंतर URL param ने सोडवता येईल).

### 🎯 Decision 2 — रंगसंगती: generic warm palette ऐवजी "पूजा पत्रिका" पॅलेट

**आधीचं:** `#8B4513` साधा brown + `#F7F1E8` cream — नेमकं AI-generated डिझाइनमध्ये सर्वात जास्त दिसणारं combo, वेगळेपण शून्य.

**प्रवास:** प्रथम "देवघर पॅलेट" (सिंदूर-मरून + पितळी सोनं + हस्तिदंती) redesign केला. युजरला "अजून impressive नाही" वाटला → नुसते रंग न बदलता **३ पूर्ण वेगळ्या संकल्पना** (structure + motif + interaction) बनवून interactive comparison पानावर दाखवल्या: **संग्रहालय फलक**, **पूजा पत्रिका**, **दिवा प्रकाश**. युजरने **पूजा पत्रिका** निवडली — सोनेरी दुहेरी-गोल चौकट, "मुद्रा" (सील) Play बटण, दोरी-style progress bar.

**अंतिम टोकन** (हेक्स `styles.css` शी जुळले — तपासलं; ratio आकडे `DESIGN-DECISIONS.md` मधल्या गणनेतले, bg `#fbf1de` वर किरकोळ फरक शक्य):

| टोकन | मूल्य (styles.css) | Contrast (~cream bg वर) | निकाल |
|---|---|---|---|
| `--color-text` (मुख्य मजकूर) | `#3a0f16` | ~14.9:1 | ✅ AAA |
| `--color-primary` (मरून) | `#7a1e2b` | ~9.2:1 | ✅ AAA |
| `--color-muted` | `#7a5c46` | ~5.4:1 | ✅ AA |
| `--color-gold` | `#8f6224` | ~4.8:1 | ✅ AA |

**प्रामाणिक टीप:** gold accent **दोनदा** contrast-fail झाला — `#B8863B` (2.87:1) आणि नंतर पत्रिका-mockup मधला `#B3872F` (2.92:1) — दोन्ही लहान eyebrow-label मजकुरासाठी. Production ला जाण्याआधी manual WCAG गणिताने पकडून `#8F6224` वर आणलं. **धडा:** palette-tool मधून रंग उचलण्याआधी contrast गणित करा.

### 🎯 Decision 3 — Web font: नाही → Yatra One → परत नाही (system-ui)

तीन टप्पे, तिन्ही जाणीवपूर्वक:
1. **सुरुवात — "no web fonts":** साइट offline PWA, service worker फक्त local assets cache करतो.
2. **पत्रिका दिशेत Yatra One जोडला** — फक्त शीर्षकांसाठी (site title, item title); body मजकूर system-ui वरच (वयोगट ८–८० साठी लांब परिच्छेदाला स्वच्छ sans जास्त वाचनीय). Offline साठी `sw.js` मध्ये `fonts.googleapis.com` + `fonts.gstatic.com` ला cache-first fetch जोडला.
3. **फाँट-तक्रारींनंतर पूर्ण काढला** — परत system-ui स्टॅक (देवनागरीही व्यवस्थित दाखवतो). Visual identity टायपोग्राफी scale/weight/spacing ने, external dependency शिवाय.

**धडा:** offline-विश्वासार्हता vs सजावटी टायपोग्राफी — या प्रोजेक्टसाठी offline जिंकलं.

### 🎯 Decision 4 — Icon-only बटणं, पण accessibility बग टाळून

Play/pause बटण आधी `ऐका`/`थांबवा` मजकूर दाखवत होतं. नवीन डिझाइनमध्ये SVG आयकॉन — पण त्यामुळे screen-reader साठी बटणाचं नाव हरवलं. Browser testing मध्ये (accessibility tree वाचून) पकडलं, `aria-label` + खालचा दृश्य label दोन्ही जोडून लगेच फिक्स.

### 🎯 Decision 5 — JSON-as-CMS + jsonlint guard

**पर्याय:** (A) थेट JSON edit · (B) Airtable + n8n · (C) Google Sheets + n8n · (D) custom admin panel.

**सध्या A (सोप्या सुरक्षिततेसह):** एकच `data.json`, Notepad मध्ये edit, चूक टाळायला jsonlint.com तपासणी, README मध्ये copy-paste flow. C (Sheets + n8n) हे स्पेकमधलं ध्येय — pipeline नंतर जोडता येईल, पण त्यासाठी नवीन tool + hosting; सध्या घराला एकाच text file ने भागतं. **Trade-off:** JSON चुकला तर साइट बंद पडते — म्हणून lint-तपासणी बंधनकारक केली.

### 🎯 Decision 6 — मोठं "मुद्रा" Play बटण, autoplay नाही

**Constraint:** सर्व mobile browsers autoplay universally block करतात (verified).

**लढण्याऐवजी स्वीकारलं:** Play बटण design opportunity बनलं — सोनेरी सील, दुहेरी रिंग, visual anchor. Expectation सेट करतं: हा निवडलेला अनुभव आहे, passive नाही.

### 🎯 Decision 7 — Dark mode: बनवलं → टेस्ट केलं → पूर्ण काढलं

सुरुवातीला dark mode (हलका coral-red + हलकं सोनं, near-black bg) बनवून WCAG-पडताळला (6.5–15.6:1, AAA). पण non-technical कुटुंबाला अनपेक्षित तपकिरी थीम गोंधळात टाकत होती. **पूर्ण काढला** — कायम एकाच थीममध्ये. धडा: theoretically-correct feature सुद्धा target user गोंधळवत असेल तर तो bug आहे.

### 🎯 Decision 8 — १० placeholder आयटम्स → २३ खरी आयुधे

मध्येच सविस्तर docx गाईड-ग्रंथ मिळाला (२३ आयुधे: नाव + कथा + दार्शनिक अर्थ + मूळ ग्रंथसंदर्भ). Scope १० → २३ केला. **सुरक्षित का:** QR/NFC टॅग अजून छापलेले नव्हते, त्यामुळे URL scheme बदलण्याचा धोका नव्हता. मजकूर verbatim घेतला, प्रोग्रामने २९९/२९९ फील्ड पडताळल्या.

### 🎯 Decision 9 — QR मध्ये आयकॉन मध्यभागी नाही, वर स्वतंत्र सील

आयकॉन QR च्या मध्यभागी टाकल्यावर stress-test मध्ये **१४/२४ कोड scan-fail** झाले (error-correction capacity ओलांडली). आयकॉन कोडच्या वर स्वतंत्र सील म्हणून हलवला → २४/२४ पास. चाचणीने सापडलेला निर्णय.

### 🎯 Decision 10 — आयटम-क्रमांक बॅज (#001) — सजावट नाही, माहिती

यादीत `#001`, `#002`… दिसतात. हे decorative नाही: भौतिक QR/NFC टॅग्सवर **हेच क्रमांक** असतात (`qr-urls.txt`), त्यामुळे यादीतला क्रमांक थेट "हा टॅग कुठला" सांगतो.

### 🎯 Decision 11 — मोठ्या ऑडिओसाठी नवीन नियंत्रणं (सर्व reduced-motion-safe)

±१० सेकंद skip; gallery dots + counter; lightbox मध्ये prev/next + keyboard arrows (आधी फक्त एक फोटो + बंद बटण). Play करताना pulse-ring, cards चं staggered entrance — दोन्ही `prefers-reduced-motion` respect करतात.

---

## Section 6 — AI-assisted design workflow

> `DESIGN-DECISIONS.md` §6 + PROJECT-STATUS मधून — या प्रोजेक्टचा खरा workflow.

| Tool | भूमिका | माणसाने काय, AI ने काय |
|---|---|---|
| **Claude Sonnet 5 (Claude Code)** | Spec architect + implementation | मी constraints दिल्या; Claude ने १८-विभागी build-spec रचला, redesign (CSS/JS/HTML) implement केला. QR pipeline (Python scripts) — 【पडताळा: Claude ने की तुम्ही】 |
| **`ui-ux-pro-max` skill** | Color/typography/style domain search | पॅलेट व फाँट-जोड्या सुचवल्या; **अंतिम निवड माझी** + manual WCAG गणित |
| **`design:design-critique` दृष्टिकोन** | Review lens | सध्याच्या साइटचा designer's-eye रिव्ह्यू, मग redesign |
| **Claude Browser (in-app)** | Live testing | DOM / console / accessibility-tree + click-tests. **Pixel screenshot उपलब्ध नव्हता** — पडताळणी computed-style वर आधारित |
| **AI image tools (OpenArt / Seedream 4.5)** | आयकॉन-निर्मिती | App icon (कलश) + ९ आयुध-बॅज AI-चित्रित; credits संपल्यावर उरलेले १३ बॅज Claude ने vector आर्ट म्हणून काढले (cubic-bezier, दुरंगी gold gradient) |
| **Python (qrcode / Pillow / pyzbar)** | QR pipeline | २४ सानुकूल QR कार्ड्स local generate + pyzbar ने २४/२४ decode-पडताळणी + stress-test (तिरकं/अंधुक/लांबून) |
| **आवाज (एकदंत ००१)** — 【पडताळा】 | ऑडिओ स्रोत अनिश्चित | `media/item-001/audio-mr.wav` (६.२ MB, ~६५ से) फक्त एकदंतसाठी आहे; बाकी २२ शांत placeholder. जुनं फाइलनाव `multi-speaker_एकदंत.wav` होतं → AI-निर्मित असू शकतं, पण repo मध्ये पुष्टी नाही. **खरा रेकॉर्ड की ElevenLabs/AI — केस स्टडीत लिहिण्याआधी नक्की करा.** (टेम्प्लेटमधली "grandma voice → uncanny → real recording" कथा या प्रोजेक्टला लागू आहे की नाही तेही तपासा) |

**प्रामाणिक self-assessment:**
- **AI ने चांगलं केलं:** repetitive scaffolding, syntax, edge-case enumeration, contrast गणित, QR stress-simulation
- **मी override केलं:** धार्मिक/शास्त्रीय मजकुराची verbatim अचूकता, emotional design, dark-mode काढण्याचा निर्णय, फाँट काढण्याचा निर्णय, prioritization
- **धडा:** AI execution-वेळ compress करतो. Design judgment माणसाकडेच.
- **मर्यादा:** या सेशनमध्ये pixel-screenshot QA शक्य नव्हतं; खरी device-चाचणी बाकी.

---

## Section 7 — Testing & metrics

> तांत्रिक पडताळणी आणि user-metrics वेगळे ठेवले आहेत — गोंधळ नको.

### तांत्रिक पडताळणी

> **स्तंभ २ = मी या मसुद्यासाठी स्वतंत्रपणे तपासलं (१ Sep 2026).** ✅ = कोड/फाइल पाहून खात्री · ⚠️ = अंशतः / सुधारणा · ❌ = या सेशनमध्ये re-run जमलं नाही (मशीन load; pyzbar >३० से/इमेज).

| तपासणी | स्वतंत्र निकाल |
|---|---|
| **कंटेंट (data.json)** | ✅ २३ पूर्ण आयटम्स; प्रत्येकात title/story/guide/audio/images/duration भरलेलं. `guide.mr` = संपूर्ण रचित मजकूर (पौराणिक कथा verbatim, SFX cues, प्रतीकार्थ, ग्रंथसंदर्भ). ५७५ string fields, **० placeholder** |
| **आवाज** | ✅ नक्की **१ खरा / २२ placeholder** — ००१ `audio-mr.wav` (६.२७ MB); ००२–०२३ `audio-mr.mp3` ६४३ B / ६४ B (शांत) |
| **QR assets** | ✅ २४ branded PNG (०००-home + ००१–०२३) + contact-sheet + A4 print-PDF, सर्व २९ Aug. `qr-urls.txt` प्रत्येक id → बरोबर `?id=NNN` |
| **QR प्रिंट DPI / आकार** | ✅ `_generate_qr.py`: 300 DPI embed; QR चौरस ~६८६px/300 = **~५.८ सेमी** (module ~१.१९ मिमी); कार्ड रुंदी **७.६ सेमी**, उंची आयकॉन-बॅजनुसार (~१०.५ सेमी आयटम, ~८.५ home) |
| **QR error-correction** | ✅ **`ERROR_CORRECT_Q`** (~२५%) + square modules + exact-integer render — stress-verified (आधी M + rounded होतं) |
| **QR मध्यभागी logo नाही** | ✅ `_generate_qr.py` कमेंट पुष्टी करते: embedded icon "roughly half" कोड scan-fail करत होतं → आयकॉन कार्डवर सील म्हणून (Decision 9 खरा) |
| **QR decode (pyzbar)** | ✅ **re-run केला — baseline २४/२४ decode pass.** (per-file verifier `_verify_qr.py` repo मध्ये नाही, पण `_stress_test_qr.py` तेच काम करतो) |
| **QR stress-test** | ✅ **square modules + EC-Q नंतर: सर्व २४/२४**, ५ परिस्थितींत (सरळ · rotation ४° · blur · print+photo JPEG q45 · arm's-length distance), पूर्ण कार्ड आणि patrika ~३.८ सेमी scale — दोन्हीवर. तिन्ही PDF मधून whole-page decode २४/२४. *(आधी rounded + EC-M होतं → JPEG q45 वर १७/२४; ते बदललं.)* |
| **"२९९/२९९ fields (docx→json)"** | ❌ reproduce अशक्य — स्रोत `.docx` repo मध्ये नाही, checker script नाही. जेवढं सांगता येतं: २३ पूर्ण, placeholder-मुक्त आयटम्स |
| **Live site** | ✅ अंशतः — homepage हेडिंग "श्री गणेश आयुधे" ठीक; live `data.json` = वैध JSON, २३ आयटम्स, local शी जुळतं. ⚠️ आयटम-यादी JS ने render होते → WebFetch ने "लोड होत आहे…" दिसलं (fetch-tool ची मर्यादा, बग नाही); ३७५px + प्रत्यक्ष render खऱ्या ब्राउझरमध्ये तपासा |
| **किरकोळ** | ⚠️ home QR कार्ड अजून जुनं नाव "आमचं घर संग्रहालय" छापतं (साइट = "श्री गणेश आयुधे") |

### ❗ User metrics (बाकी — guest testing नंतर)

| Metric | Result | Target |
|---|---|---|
| QR स्कॅन → पहिला audio play वेळ | ❗ | < १० सेकंद |
| Full-tour completion rate | ❗ | — (baseline स्थापन करायचा) |
| पुन्हा ऐकलेले आयटम्स (delight signal) | ❗ | — |
| non-technical संपादकाने नवीन आयुध जोडलं | ❗ | ३/३ |
| पहिल्या महिन्याचा bandwidth | ❗ | GitHub 100GB limit च्या खूप आत |

### ❗ पाहुण्यांचे थेट quotes

> *(खऱ्या testing नंतर. आत्ता एकही नाही.)*

---

## Section 8 — काय चाललं नाही

> हा विभाग बहुतेक portfolios टाळतात — म्हणून ठेवला.

1. **Gold accent contrast दोनदा fail** — `#B8863B` (2.87:1), मग `#B3872F` (2.92:1). Manual WCAG गणिताने पकडून `#8F6224` वर आणलं. धडा: palette-tool वर आंधळा विश्वास नको, आधी गणित.
2. **Yatra One web font** — जोडला, फाँट-तक्रारी आल्या, पूर्ण काढला. Offline-safety vs टायपोग्राफी लढाईत offline जिंकलं.
3. **Dark mode** — पूर्ण बनवून WCAG-पडताळला, पण कुटुंबाला अनपेक्षित तपकिरी थीम गोंधळवत होती. काढून टाकला.
4. **QR मध्यभागी आयकॉन** — १४/२४ कोड scan-fail. आयकॉन बाहेर काढला.
5. **पहिले hand-drawn आयकॉन flat-polyline होते** — नंतर cubic-bezier + gradient ने अधिक पॉलिश आवृत्तीने replace केले (`_draw_remaining_icons_v2.py`).
6. **Autoplay** — स्पेकमध्येच "verified blocked" होतं; लढलो नाही, Play बटण design opportunity बनवली.
7. **पहिला "देवघर पॅलेट" redesign** — युजरला "अजून impressive नाही". धडा: फक्त रंग ट्यून करणं ≠ redesign; structure/motif/interaction बदलावं लागतं. ३ पूर्ण संकल्पना बनवल्यावर निवड झाली.
8. **QR "सर्व पास" चा दावा घाईचा होता, आणि पहिली रचना नाजूक होती** — status doc मध्ये "२४/२४ पास" होतं; बारकाईने re-run केल्यावर JPEG q45 recompression वर ७/२४ fail. मूळ कारण: rounded modules (सजावटी) + EC-M (१५% recovery). rounded → **square modules**, EC-M → **EC-Q (२५%)**, आणि QR resize न करता exact integer module-size ने रेंडर — तिन्ही बदलल्यावर सर्व २४ कोड सर्व परिस्थितींत पास. धडा: (अ) "पास" लिहिण्याआधी condition-wise आकडे नोंदवा; (ब) QR वर सजावट (rounded corners, कमी EC, resize) scannability विरुद्ध जाते — साधा square QR च सर्वात विश्वासार्ह.

---

## Section 9 — पुढे काय

- **खरा आवाज** — उरलेल्या २२ आयुधांचा मराठी आवाज (स्क्रिप्ट्स `audio-scripts/` मध्ये तयार, फक्त वाचून रेकॉर्ड करायचं)
- **English** — इंग्रजी ऑडिओ + English toggle पुन्हा चालू (आत्ता तात्पुरता लपवलेला)
- **भौतिक पायरी** — २४ QR कार्ड्स रंगीत प्रिंट · खरा फोन-कॅमेरा scan-टेस्ट · NFC टॅग्स (NTAG213, `qr-urls.txt` मधले URL) · लाकूड/कार्डबोर्ड मागे लावणे (धातू नाही)
- **CMS upgrade** (ऐच्छिक) — Google Sheets → n8n → JSON → GitHub push pipeline (स्पेकमधलं मूळ ध्येय)
- **आयकॉन** — credits आल्यावर १३ vector बॅज AI-चित्रणाने बदलणे
- **v2** — multi-family / गणेशोत्सव-मंडळ template म्हणून productized service; प्रति-आयुध WhatsApp bot conversational deep-dive
- **Custom domain**

---

## Section 10 — Toolkit (recruiter keyword scan)

> 【पडताळा】 खालची यादी repo मध्ये प्रत्यक्ष दिसलेल्या गोष्टींपुरती ठेवली आहे. Figma / Maze / Web NFC API इथे **मुद्दाम नाहीत** — त्यांचा वापर repo मध्ये दिसला नाही (टेम्प्लेटमधली उदाहरणं होती). वापरला असेल तर जोडा.

**Design:** `ui-ux-pro-max` / `design:design-critique` skills, WCAG manual audit
**Frontend:** HTML5, CSS3 (custom properties / tokens), Vanilla JS, PWA, Service Worker (offline + cache-versioning), Media Session API, Wake Lock API, `prefers-reduced-motion`
**NFC/QR:** NTAG213 tags + "NFC Tools" app (physical), Python (qrcode, Pillow, pyzbar) QR generation + decode-verification pipeline
**Hosting:** GitHub Pages (free, auto-HTTPS)
**AI:** Claude Sonnet 5 / Claude Code (spec + implementation + review), Claude Browser (live DOM/a11y QA), OpenArt / Seedream 4.5 (iconography)
**Accessibility:** WCAG 2.1 AA (manual contrast math), aria-label, keyboard nav, ≥44px targets, reduced-motion

---

## Section 11 — Contact / CTA

**तुमच्या घरासाठी किंवा मंडळासाठी असं काही हवं आहे?**
- LinkedIn: 【भरायचं】
- WhatsApp: 【भरायचं】
- Email: 【भरायचं】
- GitHub template: https://github.com/smartconnect2020-hash/Ganpati_ai_museum

---

# Publishing checklist

## Notion (primary)
- [ ] सर्व sections खऱ्या मजकुराने भरले (Section 2 खरी आठवण, Section 4 + 7 testing data)
- [ ] लाइव्ह डेमो < ३ सेकंदात लोड
- [ ] सर्व images WebP, प्रत्येक < 200KB
- [ ] Cover image (1200×630, social sharing)
- [ ] Notion page → Public

## Medium (secondary)
- [ ] 800–1200 शब्दांची condensed आवृत्ती, Notion ला cross-link
- [ ] Tags: `UX Design`, `Case Study`, `AI Tools`, `PWA`, `Cultural Preservation`, `Indian Design`

## LinkedIn (traffic driver)
- [ ] ५-slide carousel: problem → solution → key decision → metric → CTA
- [ ] ६० सेकंद phone-recorded walkthrough
- [ ] Hashtags: `#UXDesign` `#ProductDesign` `#AITools` `#IndianDesign`

## Behance
- [ ] Strong hero image + process artifacts (decision matrix, ३-संकल्पना comparison board)

## GitHub (proof of build)
- [ ] README मध्ये interaction GIFs
- [ ] Setup सूचना अनोळखी माणसालाही कळतील इतक्या स्पष्ट
- [ ] License: MIT

---

## Anti-cookie-cutter reminders (2026)

- [x] "The Problem / My Role / User Research / Solution" verbatim headers **नाहीत**
- [x] Story-first, structure नंतर
- [ ] खऱ्या users चे खरे quotes (testing नंतर)
- [ ] Metrics खरे आकडे (testing नंतर) — "improved satisfaction" छाप वाक्यं नकोत
- [x] "काय चाललं नाही" विभाग आहे
- [x] AI workflow documented
- [x] लाइव्ह डेमो चालतो
- [ ] Mobile-optimized केस स्टडी पान (recruiters फोनवर scan करतात)

---

*पहिला मसुदा समाप्त. पुढचं पाऊल: Section 2 खरी आठवण, मग guest testing → Section 4 + 7. `【पडताळा】` एकदंत-ऑडिओ स्रोत नक्की करा.*
