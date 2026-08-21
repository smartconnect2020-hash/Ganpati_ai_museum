# UI Redesign — निर्णय नोंदी (21 Aug 2026)

> ही फाइल `case-study-template.md` च्या **Section 5 (Design decisions)** आणि **Section 6 (AI-assisted workflow)** साठी कच्चा मसुदा आहे — खरे, या सेशनमध्ये घडलेले निर्णय. युजर संशोधन/मुलाखती/मेट्रिक्स (Section 4, 7) इथे नाहीत — ते खरे guest testing झाल्यावर वेगळे भरायचे, इथे fabricate केलेले नाहीत.

## संदर्भ

`ui-ux-pro-max` skill (design-system + domain search: color/typography/style/google-fonts) आणि `design:design-critique` दृष्टिकोन वापरून सध्याच्या साइटचा (index.html/app.js/styles.css) रिव्ह्यू केला, नंतर redesign लागू केला. बदल फक्त `styles.css`, `app.js`, `index.html`, `manifest.json` मध्ये — build tooling किंवा नवीन dependency नाही.

## निर्णय १ — रंगसंगती: cream+brown ऐवजी "देवघर पॅलेट" (सिंदूर-मरून + पितळी सोनं + हस्तिदंती)

**आधीचं:** `#8B4513` (साधा brown) + `#F7F1E8` (cream) — पण हे नेमके AI-generated डिझाइनमध्ये सर्वात जास्त दिसणारे combo आहे (warm cream + terracotta accent), वेगळेपण नव्हतं.

**नवीन:** Primary `#8A2E1F` (सिंदूर/कुंकवाचा गडद मरून), Gold `#8F6224` (जुनं पितळ), Background `#F8F1E4` (हस्तिदंती).

**कारण:** घरगुती देवघर/पूजा वस्तूंच्या (सिंदूर, पितळी दिवा, कुंकू) रंगांशी थेट नातं — "generic warm palette" नाही, या विशिष्ट प्रोजेक्टचं. Dark mode स्वतंत्रपणे टेस्ट केलं (हलका coral-red + हलकं सोनं, near-black bg).

**पडताळणी (WCAG contrast, या सेशनमध्ये गणित करून तपासलं):**
| जोडी | Ratio | निकाल |
|---|---|---|
| Primary #8A2E1F on cream | 7.5:1 | ✅ AAA |
| Muted text on cream | 5.8:1 | ✅ AA |
| Gold — पहिला प्रयत्न #B8863B on cream | 2.87:1 | ❌ FAIL |
| Gold — दुरुस्त #8F6224 on cream | 4.74:1 | ✅ AA |
| Dark-mode gold/primary/muted on near-black | 6.5–9:1 | ✅ AAA |

**टीप (प्रामाणिकपणे):** पहिला gold accent (#B8863B) लहान eyebrow-label मजकुरासाठी contrast fail होत होता — हे टेस्टिंग दरम्यान सापडलं आणि सेशनमध्येच दुरुस्त केलं. Screenshot/visual QA या सेशनमध्ये शक्य नव्हतं (browser pane compositing उपलब्ध नव्हती); पडताळणी DOM/computed-style/console द्वारे केली, पिक्सेल-स्क्रीनशॉटने नाही — त्यामुळे फोनवर एकदा प्रत्यक्ष उघडून बघण्याची शिफारस आहे.

## निर्णय २ — Web fonts जोडले नाहीत (मुद्दाम)

**पर्याय:** Google Fonts (Kadwa + Anek Devanagari — देवनागरी सपोर्ट असलेली जोडी `ui-ux-pro-max` typography search मधून सापडली).

**नाही वापरलं कारण:** `styles.css` च्या पहिल्याच ओळीत आधीचा निर्णय होता — "no web fonts", कारण साइट **offline PWA** आहे आणि service worker फक्त local assets cache करतो. External font टाकायचं झाल्यास font फाइल्स local download करून `sw.js` cache मध्ये टाकाव्या लागतील (नवीन फाइल्स डाउनलोड करायला आधी परवानगी लागते). सध्या system-ui स्टॅक (जो देवनागरीही व्यवस्थित दाखवतो) कायम ठेवला, टायपोग्राफी scale/weight/spacing ने visual identity मजबूत केली.

**पुढचं पाऊल (ऐच्छिक, युजरने ठरवायचं):** हवं असल्यास Kadwa+Anek Devanagari फाँट फाइल्स डाउनलोड करून local + SW-cached करता येतील — वेगळी विनंती लागेल.

## निर्णय ३ — Icon-only बटणांना text लपवलं नाही, अ‍ॅक्सेसिबिलिटी बग टाळला

Play/pause बटण आधी मजकूर दाखवत होतं (`ऐका`/`थांबवा`). नवीन डिझाइनमध्ये SVG आयकॉन वापरला — पण त्यामुळे स्क्रीन-रीडरसाठी बटणाचं नाव हरवलं होतं. ब्राउझर टेस्टिंगमध्ये (accessibility tree वाचून) हे लक्षात आलं आणि `aria-label` + खालचा दृश्य label (`player-label`) दोन्ही जोडून लगेच फिक्स केलं.

## निर्णय ४ — नवीन फीचर्स (सगळे वास्तविक कोड, टेस्ट केलेले)

- **±10 सेकंद skip बटणे** — मोठ्या ऑडिओ गाईडसाठी उपयोगी, आधी नव्हतं.
- **Gallery dots + counter, lightbox मध्ये prev/next + keyboard arrows** — आधी लाइटबॉक्स फक्त एक फोटो, बंद करायचं बटण एवढंच होतं.
- **वस्तू क्रमांक बॅज (`#001` इ.)** — हे सजावटीचं नाही: भौतिक QR/NFC टॅग्सवर हेच क्रमांक असतात (`qr-urls.txt`), त्यामुळे यादीत क्रमांक दिसणं प्रत्यक्ष उपयोगाची माहिती आहे.
- **Play करताना pulse-ring अ‍ॅनिमेशन**, कार्ड्सचं staggered entrance — दोन्ही `prefers-reduced-motion` respect करतात.
- सर्व नवीन इंटरॅक्टिव्ह एलिमेंट्स ≥44px टच-टारगेट (skip 48px, play 80px, lightbox nav 48px).

## Section 6 साठी — AI-workflow ओळ (खरी, या सेशनची)

| Tool | भूमिका |
|---|---|
| Claude Sonnet 5 (Claude Code) | कोड रिव्ह्यू + redesign इम्प्लीमेंटेशन (CSS/JS/HTML) |
| `ui-ux-pro-max` skill | Color/typography/style domain search — पॅलेट व फाँट पर्याय सुचवले, अंतिम निवड मानवी (माझी) निवड + मॅन्युअल WCAG गणित |
| Claude Browser (in-app) | Live DOM/console/interaction टेस्टिंग — pixel screenshot उपलब्ध नव्हता, त्यामुळे accessibility-tree आणि computed-style वर आधारित पडताळणी |

**प्रामाणिक मर्यादा:** हे केवळ visual/interaction redesign आहे — घरातल्या माणसांचं प्रत्यक्ष usability testing (case study Section 4/7 साठी लागणारं) अजून झालेलं नाही.

---

## अपडेट (21 Aug 2026, संध्याकाळ) — "अजून impressive नाही" फीडबॅक नंतर

वरचा redesign युजरला "अजून impressive नाही" वाटला. फक्त रंग/आयकॉन ट्यून करण्याऐवजी ३ पूर्णपणे वेगळ्या संकल्पना (structure + motif + interaction, नुसते रंग नाही) तयार केल्या आणि इंटरॅक्टिव्ह तुलना पानावर (Artifact) दाखवल्या — **संग्रहालय फलक** (गडद+brass, गॅलरी-शैली), **पूजा पत्रिका** (सोनेरी नक्षीची चौकट, उत्सवी), **दिवा प्रकाश** (गडद+immersive, दिवा उजळणारं Play बटण). युजरने **पूजा पत्रिका** निवडली — तीच आता खऱ्या साइटवर (`styles.css`/`app.js`/`index.html`/`sw.js`) पूर्ण उतरवली आहे.

### निर्णय ५ — Web font जोडला, पण निवडकपणे (निर्णय २ चा सुधारित अंमल)

पूर्वी ठरवलं होतं "no web fonts" (offline विश्वासार्हतेसाठी). पत्रिका दिशेत heading साठी **Yatra One** (Google Font, देवनागरी सपोर्ट) जोडला — पण:
- **फक्त शीर्षकांसाठी** (site title, item title) — मोठा, थोडक्यात मजकूर. Body मजकूर (कहाणी, meta, बटणं) **system-ui वरच ठेवला** — कारण केस-स्टडीतच नोंदलेला constraint आहे की guest वयोगट ८ ते ८० आहे; लांब परिच्छेदासाठी सजावटी फाँटपेक्षा स्वच्छ sans जास्त वाचनीय राहतो.
- **Offline सुरक्षितता जपली:** `sw.js` मध्ये आता `fonts.googleapis.com` + `fonts.gstatic.com` साठी cache-first fetch जोडला (आधी फक्त same-origin cache होत होतं). त्यामुळे फाँट एकदा ऑनलाइन लोड झाला की नंतर ऑफलाइनही दिसतो — फोटो/ऑडिओसारखाच पॅटर्न (पहिल्या भेटीनंतर cache).

### निर्णय ६ — Accessibility पुन्हा गणित करून तपासलं (नवीन पॅलेटसाठी)

पत्रिका दिशेचा प्रारंभिक gold (#B3872F, mockup मध्ये वापरलेला) cream bg वर फक्त 2.92:1 होता — पुन्हा तोच contrast bug प्रकार. उत्पादन साइटवर टाकण्याआधी दुरुस्त केला:

| टोकन | मूल्य | Contrast (cream bg वर) | निकाल |
|---|---|---|---|
| ink (मुख्य मजकूर) | #3A0F16 | 14.9:1 | ✅ AAA |
| primary (मरून) | #7A1E2B | 9.2:1 | ✅ AAA |
| muted | #7A5C46 (पहिला प्रयत्न #8A6A52 = 4.39, अपुरा होता) | 5.4:1 | ✅ AA |
| gold | #8F6224 (पहिला प्रयत्न #B3872F = 2.92, fail) | 4.8:1 | ✅ AA |
| Dark-mode सर्व टोकन | — | 6.5–15.6:1 | ✅ AAA |

### काय अजून तसंच आहे

- Skip ±10s बटणे, गॅलरी dots, lightbox prev/next/counter — आधीच्या redesign मधलेच, फक्त गोल्ड-रिंग स्टाइलमध्ये retheme केले.
- Play बटण आता "मुद्रा" (गोल सील, दुहेरी सोनेरी रिंग) दिसतं — क्लिक/keyboard/aria-label logic जसंच्या तसं (JS ला हात लावला नाही, फक्त CSS).
- पडताळणी: DOM/console/computed-style + लाइव्ह क्लिक-टेस्ट (लाइटबॉक्स prev/next/counter, play बटणाचा aria-label) — सर्व काम करतं. **पिक्सेल स्क्रीनशॉट अजूनही या सेशनमध्ये शक्य नाही** — फोनवर/लॅपटॉपवर बघून अंतिम खात्री करा.
