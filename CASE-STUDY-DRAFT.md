# श्री गणेश आयुधे — UX केस स्टडी (मसुदा)

> **स्थिती:** हा एक वाचनीय, वाचकासाठी स्वच्छ ठेवलेला मसुदा आहे. Section 2 (खरी वैयक्तिक आठवण) आणि Section 4/7 (guest-testing निकाल) अजून प्रामाणिकपणे रिकामे/draft आहेत — जोवर खरं घडत नाही तोवर काहीही fabricate केलेलं नाही. कामाच्या नोंदी, बदल-इतिहास, आणि तपशीलवार पडताळणी-लॉगसाठी [CASE-STUDY-NOTES.md](CASE-STUDY-NOTES.md) बघा.
>
> **खुणा:** `【युजरने भरायचं】` = वैयक्तिक/खरी आठवण · `❗` = testing नंतरचा भाग.

---

## नाव-निवड (अंतिम)

**Title + Subtitle:**
> ## No One Could Explain the Idol's Symbolism Anymore
> *How I Gave Our Family's Real Ganpati Decoration an AI-Narrated Voice and a Modern Digital Layer — Solo, Offline-First*

*(इतर १९ पर्याय आणि निवड-प्रक्रिया [CASE-STUDY-NOTES.md](CASE-STUDY-NOTES.md) मध्ये.)*

---

## फोटो / व्हिज्युअल्स — काय हवं

तयारीचे rough फोटो अजून जोडायचे आहेत — प्रकाशित करण्याआधी प्रत्येक `[PHOTO: ...]` जागी खरा फोटो टाका, रिकामी जागा किंवा stock फोटो नको (Section 8 च्या प्रामाणिकपणाच्या भावनेशी विसंगत होईल).

- **Hook कव्हर** — पूर्ण सजलेला मखर + मूर्ती ✅ मिळालं
- **सुरुवात (Section 2)** — घरचा देव्हारा वाइड शॉट + `ankush.jpg` चा खरा कुटुंब-फोटो ✅ मिळालं
- **Design decisions** — redesign च्या ३ संकल्पनांची तुलना, जुनं vs नवं QR, आयुध-चक्र GIF, जुना-नवा लोगो 🔲
- **AI workflow** — Claude Code टर्मिनल स्क्रीनशॉट (ऐच्छिक) 🔲
- **सजावट आरास** — मखर-उभारणीचे फोटो ✅ मिळालं, curate केलं
- **Testing (Section 7)** — पाहुणे स्कॅन करतानाचा फोटो 🔲 guest testing नंतर
- **प्रिंट** — छापलेली QR कार्ड्स + NFC क्लोज-अप 🟡 अंशतः
- **भौतिक निर्मिती** — raw 3D-प्रिंट, रंगवलेली तयार वस्तू, product shots ✅ मिळालं
- **Cover/hero** — 1200×630 social-share इमेज 🔲

फोटो-tracking चा तपशीलवार टेबल (कुठला फोटो कुठल्या फाइलमध्ये, काय पडताळलं) [CASE-STUDY-NOTES.md](CASE-STUDY-NOTES.md) मध्ये.

---

## Section 0 — Hook

# घरातल्या मूर्तीचा अर्थ आता कुणालाच सांगता येत नव्हता

### मी आमच्या खऱ्या गणपती सजावटीला AI-कथन आणि आधुनिक डिजिटल थर कसा दिला — एकट्याने, पूर्णपणे ऑफलाइन

*QR / NFC स्कॅन करा — बाप्पाच्या हातातल्या २० आयुधांची (एकदंत, परशू, अंकुश, सुदर्शन चक्र, खट्वांग…) मराठी ऑडिओ कहाणी, मूळ ग्रंथसंदर्भासह. ₹० होस्टिंगवर, framework शिवाय, ऑफलाइनही चालतं.*

**[▶ लाइव्ह डेमो](https://smartconnect2020-hash.github.io/Ganpati_ai_museum/)** &nbsp;&nbsp; **[GitHub](https://github.com/smartconnect2020-hash/Ganpati_ai_museum)** &nbsp;&nbsp; **[केस स्टडी वाचा ↓]**

---

## Section 1 — TL;DR box (recruiter चा १५-सेकंद scan)

```
Problem      →  गणपतीच्या मूर्तीतल्या प्रत्येक आयुधाला शास्त्रीय अर्थ आहे —
                पण उत्सवात पाहुण्यांना/मुलांना तो सांगणारं कुणी नसतं;
                गाईड-ग्रंथ कपाटात बंद राहतो
Solution     →  QR + NFC ऑडिओ गाईड, २० आयुधे, मराठी-first, offline PWA,
                मजकूर मूळ ग्रंथातून verbatim + AI-TTS कथन
My role      →  एकटा — संशोधन + UX + व्हिज्युअल डिझाइन + no-framework build
                + QR/NFC pipeline + TTS pipeline + AI-workflow orchestration
Timeline     →  २० Aug 2026 पहिला commit → सप्टेंबर २०२६ पर्यंत सक्रिय
Stack        →  Vanilla HTML/CSS/JS · PWA + Service Worker · single data.json
                · Python (qrcode / Pillow / pyzbar / uharfbuzz) · Claude Code
                · Sarvam Bulbul v3 TTS · AI image tools
Results      →  ✅ २०/२० आयटम्सचा खरा आवाज (सर्व AI-TTS — Section 8 #१२ मध्ये
                मानवी-आवाज→TTS trade-off प्रामाणिकपणे मांडलं आहे)
                ❗ Guest testing अजून बाकी — तांत्रिक पडताळणी (QR decode,
                stress-test, live site) पूर्ण
Impact       →  Maharashtra मधल्या घरांसाठी / गणेशोत्सव मंडळांसाठी productizable template
```

---

## Section 2 — सुरुवात कशी झाली

*First person. Jargon नाही.*

ह्या वर्षी घरी नवीन प्रकारे आरास करताना गणपतीची आयुधं ठरवली — आणि लगेच लक्षात आलं: बऱ्याच जणांना आयुधं म्हणजे नक्की काय, कोणकोणती असतात, हेच माहीत नसतं (२-३ सोडून). मग ती माहिती गोळा करायला सुरुवात केली — पुराणांमधून, History book मधून.

मग **बाहेरगावच्या नातेवाईकांना ही माहिती कशी दाखवणार?** हा प्रश्न पडला. उत्तर: प्रत्येक आयुधासाठी एक QR कोड — जसं आजकाल प्रत्येकाच्या हातात फोन आणि स्कॅनर असतोच. मग एक मोफत साइट बनवली (GitHub repo वरून, Claude च्या मदतीने), आणि सगळी माहिती त्यावर मॅप केली.

पण नुसता मजकूर वाचून काहींना — विशेषतः वयस्कर आणि लहान मुलांना — तो वाचणं अवघड वाटलं. म्हणून आवाज जोडायचं ठरलं, AI च्या मदतीने. आणि ही माहिती जास्तीत जास्त लोकांपर्यंत पोहचावी म्हणून साइटमध्ये SEO आणि Analytics जोडलं.

*(दोन खऱ्या हस्तलिखित नोंदींवर आधारित — पहिला परिच्छेद "भौतिक आरास"-नोंदीतून, उरलेले "QR/website"-नोंदीतून; दोन्ही नोंदींमधला जोडणारा दुवा ["आयुधं ठरवली" → "नातेवाईकांना दाखवायचा प्रश्न"] माझा तर्क आहे, नोंदीत शब्दशः तसा क्रम लिहिलेला नाही. पूर्ण मूळ मजकूर — [HANDWRITTEN-NOTES-DIGITIZED.md](HANDWRITTEN-NOTES-DIGITIZED.md).)*

---

## Section 3 — हा solved problem का नाही (constraints ने डिझाइन ठरवलं)

| Constraint | का महत्त्वाचं | Design implication |
|---|---|---|
| **बजेट: ₹० होस्टिंग** | कुठल्याही घराला परवडलं पाहिजे | GitHub Pages (free, auto-HTTPS); QR स्वतः Python ने generate; NFC ~₹१५/टॅग |
| **कंटेंट-संपादक: non-technical कुटुंबीय** | माझ्याशिवाय मजकूर बदलता आला पाहिजे | एकच `data.json` (text file) + Notepad + jsonlint.com तपासणी + README मध्ये ३-मिनिटांचा flow |
| **पाहुणे वयोगट ८ ते ८०** | UI सर्व पिढ्यांना चालला पाहिजे | Marathi default, system-ui फाँट, मोठे tap-targets (मुद्रा Play ८०px, ±१०s skip ४८px — सर्व ≥४४px) |
| **डिव्हाइस: iPhone 6 ते 15, स्वस्त Android** | आधुनिक NFC गृहीत धरता येत नाही | QR नेहमी primary, NFC secondary; जुन्या iPhone साठी placard सूचना |
| **घरात patchy WiFi** | इंटरनेटशिवाय चाललं पाहिजे | PWA + Service Worker, cache-first; पहिल्या भेटीनंतर फोटो/ऑडिओ/फाँट offline |
| **धार्मिक + शास्त्रीय मजकूर — अचूकता संवेदनशील** | एक शब्द बदलला तरी अर्थ बदलतो | मजकूर मूळ गाईड-ग्रंथातून **verbatim**; प्रत्येक आयुधाचा मूळ ग्रंथ-संदर्भ (मुद्गल पुराण इ.) पानावर दाखवला |
| **एक स्कॅन = एक वस्तू** | पाहुण्याचा गोंधळ नको | "इतर वस्तू पहा" काढलं; QR व NFC एकाच URL वर (double-play conflict संपला) |

---

## Section 4 — Research

> ❗ **हा विभाग खऱ्या guest testing नंतर भरायचा. इथे एकही quote किंवा आकडा fabricate केलेला नाही.**

### नियोजित पद्धत

- **User interviews:** ३ कुटुंबीय (संभाव्य संपादक) + ५–८ पाहुणे, वयोगट ८–८०
- **Contextual observation:** गणेशोत्सवात पाहुणे प्रत्यक्ष QR स्कॅन करताना बघणे — friction points नोंदवणे
- **Comparative analysis:** izi.TRAVEL, museum audio guides, मंदिर-दर्शन अ‍ॅप्स — काय जमतं, काय नाही

### भरायचे प्रश्न

- "संग्रहालय" vs "आयुधे" — कुठली framing कमी intimidating वाटते?
- QR स्कॅन करण्याआधी लोक कचरतात का?
- तरुण पाहुणे ऑडिओ किती सेकंदांनी skip करतात?
- जुन्या iPhone वर NFC किती steps लागतात?
- non-technical संपादकाला नवीन आयुध जोडता येतं का — मदतीशिवाय?

*(खरी observation + थेट quotes इथे. Synthesized personas नकोत.)*

निरीक्षण-लॉग, संमती-वाक्य आणि मुलाखत-प्रश्नांचं तयार किट [CASE-STUDY-NOTES.md](CASE-STUDY-NOTES.md) मध्ये आहे — गणेशोत्सवात पाहुणे आल्यावर लगेच वापरता येईल.

---

## Section 5 — Design decisions with rationale

> **Recruiter signal:** "मी screens बनवले" नाही — **"मी X केलं कारण Y, आणि Z trade-off स्वीकारला."**

### 🎯 Decision 1 — QR व NFC साठी एकच URL (वेगळे flows नाहीत)

**पर्याय:** (A) प्रत्येक method ला वेगळी URL (QR → mobile-web, NFC → app deep-link) · (B) दोन्हीला एकच URL.

**B निवडलं कारण:**
- संपूर्ण double-play conflict class नाहीशी होते — browser तीच URL पुन्हा उघडतो, नवीन tab नाही
- Content-management surface कमी — प्रति-आयुध एकच source of truth
- पाहुण्याला कुठलं trigger वापरलं याची पर्वा नाही — अनुभव सारखाच

**Trade-off स्वीकारला:** QR vs NFC engagement वेगळं track करता येत नाही (नंतर URL param ने सोडवता येईल).

### 🎯 Decision 2 — रंगसंगती: generic warm palette ऐवजी "पूजा पत्रिका" पॅलेट

**आधीचं:** साधा brown + cream — AI-generated डिझाइनमध्ये सर्वात जास्त दिसणारं combo, वेगळेपण शून्य.

**प्रवास:** प्रथम "देवघर पॅलेट" (सिंदूर-मरून + पितळी सोनं + हस्तिदंती) redesign केला. "अजून impressive नाही" वाटलं → नुसते रंग न बदलता **३ पूर्ण वेगळ्या संकल्पना** (structure + motif + interaction) बनवून तुलना-पानावर दाखवल्या: **संग्रहालय फलक**, **पूजा पत्रिका**, **दिवा प्रकाश**. **पूजा पत्रिका** निवडली — सोनेरी दुहेरी-गोल चौकट, "मुद्रा" (सील) Play बटण, दोरी-style progress bar.

**अंतिम टोकन:**

| टोकन | मूल्य | Contrast (cream bg वर) | निकाल |
|---|---|---|---|
| मुख्य मजकूर | `#3a0f16` | ~14.9:1 | ✅ AAA |
| मरून (primary) | `#7a1e2b` | ~9.2:1 | ✅ AAA |
| Muted | `#7a5c46` | ~5.4:1 | ✅ AA |
| Gold | `#8f6224` | ~4.8:1 | ✅ AA |

**प्रामाणिक टीप:** gold accent सुरुवातीला **दोनदा** contrast-fail झाला होता (छोट्या eyebrow-label मजकुरासाठी). Manual WCAG गणिताने पकडून वरच्या मूल्यावर आणलं. **धडा:** palette-tool मधून रंग उचलण्याआधी contrast गणित करा.

### 🎯 Decision 3 — Web font: नाही → Yatra One → परत नाही (system-ui)

तीन टप्पे, तिन्ही जाणीवपूर्वक:
1. **सुरुवात — "no web fonts":** साइट offline PWA, service worker फक्त local assets cache करतो.
2. **पत्रिका दिशेत Yatra One जोडला** — फक्त शीर्षकांसाठी; body मजकूर system-ui वरच (वयोगट ८–८० साठी लांब परिच्छेदाला स्वच्छ sans जास्त वाचनीय).
3. **फाँट-तक्रारींनंतर पूर्ण काढला** — परत system-ui स्टॅक (देवनागरीही व्यवस्थित दाखवतो). Visual identity टायपोग्राफी scale/weight/spacing ने, external dependency शिवाय.

**धडा:** offline-विश्वासार्हता vs सजावटी टायपोग्राफी — या प्रोजेक्टसाठी offline जिंकलं.

### 🎯 Decision 4 — Icon-only बटणं, पण accessibility बग टाळून

Play/pause बटण आधी मजकूर दाखवत होतं. नवीन डिझाइनमध्ये SVG आयकॉन — पण त्यामुळे screen-reader साठी बटणाचं नाव हरवलं. Browser testing मध्ये पकडलं, `aria-label` + दृश्य label दोन्ही जोडून लगेच फिक्स.

### 🎯 Decision 5 — JSON-as-CMS + jsonlint guard

**पर्याय:** (A) थेट JSON edit · (B) Airtable + n8n · (C) Google Sheets + n8n · (D) custom admin panel.

**सध्या A (सोप्या सुरक्षिततेसह):** एकच `data.json`, Notepad मध्ये edit, चूक टाळायला jsonlint.com तपासणी, README मध्ये copy-paste flow. C (Sheets + n8n) हे पुढचं ध्येय — सध्या घराला एकाच text file ने भागतं. **Trade-off:** JSON चुकला तर साइट बंद पडते — म्हणून lint-तपासणी बंधनकारक केली.

### 🎯 Decision 6 — मोठं "मुद्रा" Play बटण, autoplay नाही

**Constraint:** सर्व mobile browsers autoplay universally block करतात.

**लढण्याऐवजी स्वीकारलं:** Play बटण design opportunity बनलं — सोनेरी सील, दुहेरी रिंग, visual anchor. Expectation सेट करतं: हा निवडलेला अनुभव आहे, passive नाही.

### 🎯 Decision 7 — Dark mode: बनवलं → टेस्ट केलं → पूर्ण काढलं

सुरुवातीला dark mode बनवून WCAG-पडताळला (AAA). पण non-technical कुटुंबाला अनपेक्षित तपकिरी थीम गोंधळात टाकत होती. **पूर्ण काढला** — कायम एकाच थीममध्ये. धडा: theoretically-correct feature सुद्धा target user गोंधळवत असेल तर तो bug आहे.

### 🎯 Decision 8 — Placeholder आयटम्स → खरी आयुधे

मध्येच सविस्तर docx गाईड-ग्रंथ मिळाला (नाव + कथा + दार्शनिक अर्थ + मूळ ग्रंथसंदर्भ). Scope वाढवला. **सुरक्षित का:** QR/NFC टॅग अजून छापलेले नव्हते, त्यामुळे URL scheme बदलण्याचा धोका नव्हता. मजकूर verbatim घेतला.

### 🎯 Decision 9 — QR मध्ये आयकॉन मध्यभागी नाही, वर स्वतंत्र सील

आयकॉन QR च्या मध्यभागी टाकल्यावर stress-test मध्ये मोठा भाग कोड scan-fail झाला (error-correction capacity ओलांडली). आयकॉन कोडच्या वर स्वतंत्र सील म्हणून हलवला → पूर्ण pass. चाचणीने सापडलेला निर्णय.

### 🎯 Decision 10 — आयटम-क्रमांक बॅज (#001) — सजावट नाही, माहिती

यादीत `#001`, `#002`… दिसतात. हे decorative नाही: भौतिक QR/NFC टॅग्सवर **हेच क्रमांक** असतात, त्यामुळे यादीतला क्रमांक थेट "हा टॅग कुठला" सांगतो.

### 🎯 Decision 11 — मोठ्या ऑडिओसाठी नवीन नियंत्रणं (सर्व reduced-motion-safe)

±१० सेकंद skip; gallery dots + counter; lightbox मध्ये prev/next + keyboard arrows. Play करताना pulse-ring, cards चं staggered entrance — दोन्ही `prefers-reduced-motion` respect करतात.

### 🎯 Decision 12 — यादी/कार्ड-list ऐवजी "आयुध-चक्र" फिरतं मंडल

**आधीचं:** साधी स्क्रोल-करण्याजोगी यादी/कार्ड-ग्रिड — कार्यक्षम, पण "२० वेगवेगळ्या वस्तूंमधलं नातं" काहीच दाखवत नव्हती.

**नवीन:** मध्यभागी ॐ, त्याभोवती दोन एकसमान फिरणाऱ्या रिंगमध्ये २० आयुधं — मंदिरातल्या मंडल/चक्राची भावना. Auto-rotate (धीमं, थांबवता येणारं), drag-to-rotate, मध्यभागी "यादृच्छिक आयुध सुचव" बटण.

**Exploration:** एकदम या डिझाइनवर उडी मारली नाही — `design-demos/` मध्ये **९ पूर्ण पर्यायी संकल्पना** (wheel, mala, featured, scroll, deck, bento, playlist, mandala, coverflow) कोडसह जतन आहेत.

**समस्या सापडली आणि सोडवली:** मोबाईलवर (375px मोजून) २० नोड्स एका रिंगवर ठेवल्यास शेजारी-शेजारी अंतर किमान tap-target पेक्षा कमी उरत होतं — **overlap गणिती अपरिहार्य होता, CSS ने सुटणारा नव्हता.** उपाय: 600px खाली रिंग पूर्ण लपवली, त्याजागी swipeable circle-row (Spotify/Instagram-Stories स्टाईल).

**धडा:** "एकच रिंग सर्व स्क्रीन आकारांना पुरेल" हे गृहीतक चुकलं — प्रत्यक्ष मोजमापानेच कळलं, अंदाजाने नाही.

### 🎯 Decision 13 — नवीन ब्रँड-मार्क, आणि favicon साठी वेगळी सोपी आवृत्ती

जुना इनलाइन कलश-SVG आयकॉन बदलून नवीन मार्क — अंकुशाच्या हुकाचं टोक Play-बटणाचा त्रिकोण बनतं (गणेश-प्रतीकवाद + "हे ऑडिओ गाईड आहे" एकाच रेषेत). पण १६×१६/३२×३२ favicon ला तीच तपशीलवार आवृत्ती अस्पष्ट दिसली — शिप करण्याआधी zoom करून तपासलं, वेगळा सोपा crop बनवला. एकच आयकॉन सर्व आकारांना चालत नाही हे इथेही खरं ठरलं.

### 🎯 Decision 14 — भौतिक आयुध-निर्मिती: AI संदर्भ-प्रतिमा → 3D प्रिंट/चिकणमाती → acrylic फिनिशिंग

हा भाग साइटच्या *सॉफ्टवेअर* भागापेक्षा वेगळा आहे — प्रत्यक्ष मखरातल्या आयुधांच्या मूर्ती **कशा बनवल्या** याची प्रक्रिया. "AI फक्त कोडपुरतं नाही, भौतिक क्राफ्टलाही लागलं" हे दाखवणारा पुरावा — digital + physical maker workflow.

**पाइपलाइन (डिजिटल → भौतिक, पूर्ण tool-chain):**
1. **संशोधन** — पुराणं + History book मधून माहिती गोळा केली; Research tools + NotebookLM मध्ये सर्व sources एकत्र करून संदर्भ-फाइल्स बनवल्या (Decision 8 शी संबंधित)
2. **AI संदर्भ-प्रतिमा** — त्या माहितीवरून प्रत्येक आयुधासाठी Prompts तयार केले, **Google Flow** ने संदर्भचित्रं जनरेट केली. सुरुवातीला २०+ आयुधांची माहिती गोळा झाली, जागेअभावी **१८-१९ आयुधांच्याच भौतिक मूर्ती** मखरात प्रत्यक्ष मांडल्या — डिजिटल साइटवरचे **२० आयुधे** ही वेगळी (सर्व-कव्हर करणारी) संख्या आहे, दोन्ही आकडे वेगवेगळ्या गोष्टींचे आहेत, विसंगत नाहीत
3. **भौतिक निर्मिती — दोन पद्धती समांतर:**
   - **3D प्रिंट:** वेळ कमी असल्यामुळे काही आयुधांसाठी Google Flow च्या प्रतिमा **meshy.ai** ने 3D मॉडेलमध्ये बदलल्या → **Ultimaker** मध्ये सेटिंग + `.stl` फाइल edit (हे सॉफ्टवेअर आधी येत नव्हतं, थोडं शिकून घेतलं) → **local vendor** कडून प्रिंट करून घेतलं (स्वतः प्रिंट केलं नाही)
   - **हाताने घडवणी:** काही आयुधं **Fevicryl clay** ने समांतर (parallely) घडवली
4. **फिनिशिंग** — दोन्ही पद्धतींच्या वस्तूंवर आधी काळा matt स्प्रे प्राइमर कोट, मग acrylic रंगांनी (golden, copper, metallic, लाकडासाठी brown इ.) डिटेल पेंटिंग
5. **आकारमान — मुद्दाम ठरवलेलं, सौंदर्यासाठी नाही:** मूर्ती स्वतः सुमारे ८ इंच; स्टँड त्याहून मोठा, सुमारे १० इंच — कार्डबोर्डाचा, काळ्या स्प्रे पेंटने फिनिश केलेला. **१० इंच उंचीचं कारण:** (अ) आयुधाच्या वर QR-कोड + नाव-लेबल लावायला जागा हवी होती, (ब) मांडणीत सर्व आयुधं एकमेकांवर **overlap होऊ नयेत**
6. **बॅकड्रॉप** — काळ्या थीमशी जुळणारा पेपर, प्रत्येक आयुध उठून दिसावं म्हणून
7. **QR थर** — प्रत्येक आयुधासाठी स्वतंत्र QR + मुख्य लँडिंग-पेजसाठी एक मास्टर QR

*(पूर्ण मूळ नोंद — [HANDWRITTEN-NOTES-DIGITIZED.md](HANDWRITTEN-NOTES-DIGITIZED.md).)*

**हेतू:** पुराणातली माहिती दाट/जड भाषेत असते, आणि जुन्या पिढीला वाचवत नाही किंवा वाचता येत नाही अशा पाहुण्यांसाठी संपूर्ण मजकूर **ऐकता यावा** म्हणून ऑडिओ थर जोडला — हे प्रवेशयोग्यतेचं (accessibility) मूळ कारण आहे, केवळ नावीन्यासाठी टेक जोडलेली नाही.

**थीम-फ्रेमिंग:** आधुनिक तंत्रज्ञान (AI इमेज जनरेशन, 3D प्रिंटिंग, TTS, QR) पारंपरिक गणेशोत्सव सजावटीला **बदलत नाही, तर तिचा अर्थ अधिक लोकांपर्यंत पोहोचवतं** — parody किंवा gimmick म्हणून नाही.

---

## Section 6 — AI-assisted design workflow

| Tool | भूमिका | माणसाने काय, AI ने काय |
|---|---|---|
| **Claude Sonnet 5 (Claude Code)** | Spec architect + implementation | मी constraints दिल्या; Claude ने build-spec रचला, redesign (CSS/JS/HTML) implement केला |
| **`ui-ux-pro-max` skill** | Color/typography/style domain search | पॅलेट व फाँट-जोड्या सुचवल्या; **अंतिम निवड माझी** + manual WCAG गणित |
| **`design:design-critique` दृष्टिकोन** | Review lens | सध्याच्या साइटचा designer's-eye रिव्ह्यू, मग redesign |
| **Claude Browser (in-app)** | Live testing | DOM / console / accessibility-tree + click-tests |
| **AI image tools (OpenArt / Seedream 4.5)** | आयकॉन-निर्मिती | App icon + आयुध-बॅज AI-चित्रित; उरलेले बॅज Claude ने vector आर्ट म्हणून काढले |
| **Python (qrcode / Pillow / pyzbar)** | QR pipeline | सानुकूल QR कार्ड्स local generate + pyzbar ने decode-पडताळणी + stress-test (तिरकं/अंधुक/लांबून) |
| **Sarvam Bulbul v3 (TTS)** | **सर्व २०/२० आयुधांचा आवाज** | Voice "ritu". **STT (speech-to-text) ने परत मजकूर काढून approved script शी cross-check** — उच्चार-अचूकतेची स्वयंचलित पडताळणी, फक्त "ऐकून ठीक वाटलं" नाही. सुरुवातीला एकदंतचं (००१) मानवी रेकॉर्डिंग वेगळं ठेवलं होतं, पण **नंतर तेही जाणीवपूर्वक TTS ने बदललं** — सुसंगततेसाठी, मूळ .wav डिस्कवर सुरक्षित |

**प्रामाणिक self-assessment:**
- **AI ने चांगलं केलं:** repetitive scaffolding, syntax, edge-case enumeration, contrast गणित, QR stress-simulation
- **मी override केलं:** धार्मिक/शास्त्रीय मजकुराची verbatim अचूकता, emotional design, dark-mode काढण्याचा निर्णय, फाँट काढण्याचा निर्णय, prioritization
- **धडा:** AI execution-वेळ compress करतो. Design judgment माणसाकडेच.
- **मर्यादा:** pixel-screenshot QA या सेशनमध्ये शक्य नव्हतं; खरी device-चाचणी बाकी

### 🧾 निर्णय-पुरावा (Evidence Sheet)

> प्रत्येक AI-वापरलेल्या पायरीवर हे सांगण्याची गरज नाही — फक्त जिथे तो निर्णय मूल्यमापनावर खरा परिणाम करतो, तिथे. तीन ठिकाणी: brief → constraint → AI ने काय दिलं → माणसाने कुठे override केलं → शेवटी काय शिप झालं.

**१. आवाज — TTS निवड**

| | |
|---|---|
| Brief | २० आयुधांचा सुसंगत-दर्जाचा आवाज हवा |
| Constraint | एकट्याने २० रेकॉर्डिंग्स वेळेत करणं अशक्य |
| AI ने दिलं | पूर्ण मजकूर TTS ने generate करणं (Sarvam Bulbul v3) |
| माणसाने override केलं | मजकूर १००% मूळ ग्रंथातून verbatim ठेवला; STT cross-check गेट स्वतः जोडला (tool मध्ये automatic नाही) |
| शिप झालं | २०/२० आवाज, उच्चार-पडताळणीसह — एकदंतचं मूळ मानवी रेकॉर्डिंगही सुसंगततेसाठी नंतर बदललं (Section 8 #12) |

**२. रंगसंगती — पॅलेट निवड**

| | |
|---|---|
| Brief | Generic warm-brown पॅलेट ऐवजी वेगळेपण हवं |
| Constraint | नुसते रंग बदलणं "अजून impressive नाही" ठरलं |
| AI ने दिलं | (`ui-ux-pro-max` skill) रंग/फाँट जोड्यांचे पर्याय |
| माणसाने override केलं | ३ पूर्ण structural संकल्पना बनवून निवड केली; gold accent दोनदा contrast-fail झाला तेव्हा manual WCAG गणिताने पकडून दुरुस्त केलं |
| शिप झालं | "पूजा पत्रिका" पॅलेट, सर्व टोकन AA/AAA contrast |

**३. नेव्हिगेशन — आयुध-चक्र रचना**

| | |
|---|---|
| Brief | यादी/कार्ड-ग्रिडमध्ये "२० वस्तूंमधलं नातं" दिसत नव्हतं |
| Constraint | एकाच रिंग-डिझाइनवर आंधळेपणे उडी मारायची नव्हती |
| AI ने दिलं | (Claude Code) ९ पर्यायी संकल्पना (`design-demos/`) कोडसह |
| माणसाने override केलं | निवड + मोबाईलवर प्रत्यक्ष मोजमाप (375px) — एक-रिंग रचना गणितीयदृष्ट्या मोडत असल्याचं सापडलं, वेगळा पॅटर्न मागवला |
| शिप झालं | फिरतं मंडल (desktop) + swipeable row (mobile), मोजमापाने पडताळलेलं |

### AI × UX ची सांगड — मुलाखतीत विचारले जाणारे प्रश्न

> Recruiter/मुलाखतकार अनेकदा "AI वापरलंस, पण UX चं काम कुठे आहे?" असं विचारतात.

1. **"खरी समस्या काय होती, आणि AI का लागलं?"**
   समस्या UX ची होती (लोकांना आयुधांचा अर्थ माहीत नाही, वाचायला वेळ/इच्छा नाही) — तंत्रज्ञानाची नाही. उपाय ठरवताना (ऑडिओ-गाईड, QR/NFC, मराठी-first) AI आलंच नाही — तो निर्णय संशोधन/constraints मधून आला. AI आलं **अंमलबजावणीत**: spec पासून implementation पर्यंतचा वेळ compress करायला, आणि २० आवाज एकट्याने रेकॉर्ड करणं अशक्य असताना TTS ने ते शक्य केलं.

2. **"AI च्या आउटपुटवर तुझा UX निर्णय कुठे दिसतो?"**
   डिझाइन-रंग/फाँट AI ने सुचवले, पण अंतिम निवड + WCAG गणित माणसाने केलं. TTS आवाज निवडताना नुसतं "generate करून वापरणं" नाही — **STT ने परत पडताळणी** ही स्वतः जोडलेली quality-gate पायरी आहे. हीच UX/product-thinking ची जागा — "AI आउटपुट विश्वासार्ह आहे का" हे ठरवणं.

3. **"मानवी आवाजाऐवजी AI आवाज वापरणं — हे विरोधाभासी नाही का?"**
   मूळ योजना मानवी आवाज होती. पण २० आयुधांचं सुसंगत-दर्जाचं रेकॉर्डिंग एकट्याने करणं व्यवहार्य नव्हतं. **निवड:** मजकूर १००% मूळ ग्रंथातून verbatim ठेवला (सामग्रीची सत्यता), आवाजासाठी AI वापरला पण अचूकता-पडताळणी (STT cross-check) जोडली (आवाजाच्या विश्वासार्हतेची हमी). *"परंपरा मजकुरात जपली, तंत्रज्ञान पोहोचवण्यासाठी वापरलं."*

---

## Section 7 — Testing & metrics

### तांत्रिक पडताळणी

साइटचा तांत्रिक गाभा स्वतंत्रपणे तपासला आहे: कंटेंट (सर्व आयटम्स, कुठलाही placeholder नाही), आवाज (२०/२० खरा TTS), QR assets (branded, योग्य DPI/आकार, EC-Q error-correction), QR decode व stress-test (तिरकं/अंधुक/प्रिंट+फोटो/लांबून — सर्व परिस्थितीत pass), आणि live site (वैध JSON, योग्य लोड). तपशीलवार निकाल-टेबल [CASE-STUDY-NOTES.md](CASE-STUDY-NOTES.md) मध्ये.

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

1. **Gold accent contrast दोनदा fail** — manual WCAG गणिताने पकडून दुरुस्त केलं. धडा: palette-tool वर आंधळा विश्वास नको, आधी गणित.
2. **Yatra One web font** — जोडला, फाँट-तक्रारी आल्या, पूर्ण काढला. Offline-safety vs टायपोग्राफी लढाईत offline जिंकलं.
3. **Dark mode** — पूर्ण बनवून WCAG-पडताळला, पण कुटुंबाला अनपेक्षित तपकिरी थीम गोंधळवत होती. काढून टाकला.
4. **QR मध्यभागी आयकॉन** — मोठ्या प्रमाणात कोड scan-fail. आयकॉन बाहेर काढला.
5. **पहिले hand-drawn आयकॉन flat-polyline होते** — नंतर cubic-bezier + gradient ने अधिक पॉलिश आवृत्तीने replace केले.
6. **Autoplay** — verified blocked होतं; लढलो नाही, Play बटण design opportunity बनवली.
7. **पहिला "देवघर पॅलेट" redesign** — "अजून impressive नाही" वाटलं. धडा: फक्त रंग ट्यून करणं ≠ redesign; structure/motif/interaction बदलावं लागतं. ३ पूर्ण संकल्पना बनवल्यावर निवड झाली.
8. **QR "सर्व पास" चा दावा घाईचा होता, आणि पहिली रचना नाजूक होती** — बारकाईने re-run केल्यावर JPEG recompression वर लक्षणीय fail दिसले. मूळ कारण: rounded modules (सजावटी) + कमी error-correction. rounded → **square modules**, EC-M → **EC-Q**, आणि QR resize न करता exact integer module-size ने रेंडर — तिन्ही बदलल्यावर सर्व परिस्थितींत pass. धडा: (अ) "पास" लिहिण्याआधी condition-wise आकडे नोंदवा; (ब) QR वर सजावट (rounded corners, कमी EC, resize) scannability विरुद्ध जाते — साधा square QR च सर्वात विश्वासार्ह.
9. **Id sequential करायचा प्रयत्न मागे घ्यावा लागला** — वस्तूंचे id गॅपशिवाय "स्वच्छ" करायचा प्रयत्न केला, पण काही आयटम्सचे QR/NFC आधीच जुन्या id वर छापलेले/एन्कोड होते — स्कॅन चुकीच्या वस्तूवर जायला लागला. मागे घेतलं, मूळ id कायमचे ठेवले. धडा: छापील/भौतिक वस्तूंशी जोडलेला कुठलाही ओळख-क्रमांक एकदा "बाहेर" गेला की **कधीही सौंदर्यासाठी बदलू नये.**
10. **एका रिंगमध्ये सर्व २० आयुधं मोबाईलवर बसवण्याचा पहिला प्रयत्न फसला** — नोड्स गणितीयदृष्ट्या एकमेकांवर चढत होते (मोजून सापडलं, अंदाजाने नाही). उपाय CSS-tuning नव्हता — पूर्ण वेगळा मोबाईल-पॅटर्न (swipeable row) लागला.
11. **नवीन ब्रँड-मार्क favicon आकारात वाचता येत नव्हता** — शिप करण्याआधी zoom करून तपासलं, वेगळी सोपी आवृत्ती बनवावी लागली. धडा: एकच आयकॉन सर्व आकारांना चालत नाही.
12. **"मानवी आवाज हाच अस्सलपणा" हा मूळ निर्णय स्वतःच मागे घेतला** — एकदंतचं खरं मानवी रेकॉर्डिंग होतं, पण नंतर तेही AI-TTS ने बदललं — सुसंगततेसाठी. मूळ मूल्य (माणसाचा आवाज) आणि व्यावहारिकता (सुसंगत पाईपलाईन, स्केल) यांच्यात **खरा trade-off होता, आणि सुसंगततेची बाजू जिंकली.** प्रामाणिकपणे मांडणं हेच योग्य — लपवणं उलट संशय निर्माण करेल.

---

## Section 9 — पुढे काय

- [x] खरा आवाज — पूर्ण (२०/२०, सर्व AI-TTS — एकदंतचं मानवी रेकॉर्डिंगही नंतर TTS ने बदललं)
- [x] होमपेज redesign — पूर्ण ("आयुध-चक्र" फिरतं मंडल + मोबाईल swipe-row)
- [x] ब्रँड-मार्क/लोगो — पूर्ण
- [x] SEO + analytics — पूर्ण
- [~] सजावट आरास व्हिडिओ — poster-फोटो + YouTube Shorts teaser आलं; खरी व्हिडिओ फाइल अजून बाकी
- [ ] भौतिक पायरी — QR कार्ड्स रंगीत प्रिंट · खरा फोन-कॅमेरा scan-टेस्ट · NFC टॅग्स लावणे
- [ ] English — इंग्रजी ऑडिओ + English toggle पुन्हा चालू
- [ ] Guest testing — पाहुणे बोलावून निरीक्षण + मुलाखत → Section 4 + 7 भरणे
- [ ] CMS upgrade (ऐच्छिक) — Google Sheets → n8n → JSON → GitHub push pipeline
- [ ] आयकॉन — उरलेले vector बॅज AI-चित्रणाने बदलणे
- [ ] v2 — multi-family / गणेशोत्सव-मंडळ template म्हणून productized service
- [ ] Custom domain
- [ ] `OWNERSHIP.md` मधलं legal name placeholder भरणे (फक्त तुम्ही करू शकता)

---

## Section 10 — Toolkit

**Design:** `ui-ux-pro-max` / `design:design-critique` skills, WCAG manual audit
**Frontend:** HTML5, CSS3 (custom properties / tokens), Vanilla JS, PWA, Service Worker (offline + cache-versioning), Media Session API, Wake Lock API, `prefers-reduced-motion`
**NFC/QR:** NTAG213 tags + "NFC Tools" app (physical), Python (qrcode, Pillow, pyzbar) QR generation + decode-verification pipeline
**Hosting:** GitHub Pages (free, auto-HTTPS)
**AI:** Claude Sonnet 5 / Claude Code (spec + implementation + review), Claude Browser (live DOM/a11y QA), OpenArt / Seedream 4.5 (iconography), Google Flow (संदर्भ-प्रतिमा), meshy.ai (2D → 3D मॉडेल), NotebookLM (संशोधन-सोर्स संकलन)
**Physical fabrication:** Ultimaker (print prep, `.stl` edit), local 3D-print vendor, Fevicryl clay, acrylic + spray paint finishing
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

## Anti-cookie-cutter reminders

- [x] "The Problem / My Role / User Research / Solution" verbatim headers **नाहीत**
- [x] Story-first, structure नंतर
- [ ] खऱ्या users चे खरे quotes (testing नंतर)
- [ ] Metrics खरे आकडे (testing नंतर) — "improved satisfaction" छाप वाक्यं नकोत
- [x] "काय चाललं नाही" विभाग आहे
- [x] AI workflow documented
- [x] लाइव्ह डेमो चालतो
- [ ] Mobile-optimized केस स्टडी पान (recruiters फोनवर scan करतात)
