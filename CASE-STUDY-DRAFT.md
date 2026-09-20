# श्री गणेश आयुधे — UX केस स्टडी (पहिला मसुदा)

> **स्थिती:** सतत बदलणारा draft — हा प्रोजेक्ट एकाच वेळी अनेक सेशन्समधून सक्रियपणे विकसित होतोय, त्यामुळे हा मसुदा नेहमी थोडा मागे असतो. **२० Sep 2026 पर्यंत पडताळलेली आवृत्ती.** Section 2 (खरी आठवण) अजून तुमच्याकडून बाकी; नाव **ठरलं** (Section 0 Hook + नाव-निवड यादीत ⭐); Section 4/7 (guest testing) अजून घडायचंय.
> Section 4 (research) आणि Section 7 (user metrics) **मुद्दाम मोकळे** — खरं guest testing झाल्यावरच भरायचे, इथे काहीही fabricate केलेलं नाही.
> **खुणा:** `【युजरने भरायचं】` = वैयक्तिक/खरी आठवण · `❗` = testing नंतरचा भाग · `【पडताळा】` = तपासून खात्री करायची गोष्ट.
> **Source of truth:** git log (पूर्ण इतिहास, २० Aug – २० Sep 2026), `data.json`/`styles.css`/`app.js` प्रत्यक्ष वाचून, live site.
>
> ### 🆕 २० Sep 2026 पर्यंतचे नवीन बदल (१६ Sep नंतरचे)
> - **Decision 14 जोडली (Section 5) — भौतिक आयुध-निर्मिती:** हे फक्त सॉफ्टवेअर नाही — प्रत्यक्ष घरातली मूर्तीही AI-संदर्भ-प्रतिमेवरून 3D-प्रिंट/चिकणमातीने घडवून acrylic रंगवलेली आहे. **⚠️ आकडे (८"/१०") अजून फोटोने पडताळलेले नाहीत** — Decision 14 मध्येच तसं नोंदवलंय.
> - **YouTube Shorts प्रमोशन सुरू** — "AI Tech Safar" चॅनलवर पहिला Short (87 से, गणेशोत्सव 2026 च्या मध्यात प्रकाशित) — साइटच्या सजावट-व्हिडिओ स्लॉटमध्ये **live embed म्हणून fallback** ठेवलाय (खरी `aaras.mp4` फाइल येईपर्यंत).
> - **खरा मंडप-फोटो आला** — `media/decoration/aaras-poster.jpg` — फोटो-प्लेसहोल्डर यादीतला #7 आता अंशतः भरला (व्हिडिओ अजून नाही, पण poster/social-share फोटो आहे).
> - ब्रँड-मार्क आणखी सुधारला (पूर्ण hook+play+thumb आकार, sitewide सुसंगत)
> ### 🆕 १६ Sep 2026 पर्यंतचे मोठे बदल (कालानुक्रमे, कोड वाचून पडताळलं)
> - **वस्तू २३ → २०**, id मध्ये अंतर (००१-०१४, ०१६-०१८, ०२०, ०२१, ०२३) — **कायमचं लॉक,** कारण ६ आयटम्सचे QR/NFC आधीच त्याच id वर छापलेले/एन्कोड होते (`a8fd56f` — एक sequential-renumbering प्रयत्न यामुळेच मागे घ्यावा लागला होता). डिस्प्ले-लेयरला मात्र आता स्वच्छ १-२० क्रमांक दिसतात (`0f87da4`), underlying id ला हात न लावता.
> - **आवाज आता २०/२० AI-TTS** — Sarvam Bulbul v3 ("ritu" आवाज, STT cross-check सह). **✅ ठरलं (होतं ❓):** एकदंत (००१) चं मूळ मानवी रेकॉर्डिंग होतं, पण `8918751` ने तेही **जाणीवपूर्वक बदलून TTS केलं** — "सर्व २० आयटम्सचा आवाज/पाईपलाईन सुसंगत रहावा" म्हणून, युजरने मंजूर करून. मूळ मानवी .wav फाइल डिस्कवर आहे (`media/item-001/audio-mr.wav`), पण `data.json` आता तिकडे पॉइंट करत नाही.
> - **🆕 होमपेज पूर्ण बदललं — "आयुध-चक्र" (फिरतं मंडल)** (`876e846` पासून पुढे): जुनी यादी/कार्ड-list जाऊन आता एक **फिरणारं दोन-रिंग मंडल** (desktop) — auto-rotate (१५० से/फेरी, hover/drag/hidden-tab वर थांबतं, `prefers-reduced-motion` आदर करतं), drag-to-rotate, मध्यभागी "यादृच्छिक आयुध सुचव" बटण, खरा visited-progress localStorage मधून. मोबाईलवर (<600px) रिंग लपते, त्याऐवजी swipeable circle-row (Spotify/Instagram Stories स्टाईल) — **मोजून सापडलेल्या भूमिती-समस्येमुळे** (२० नोड्स ३७५px वर एकमेकांत घुसत होते, CSS ने सुटणारं नव्हतं).
> - **नवीन ब्रँड-मार्क:** अंकुशाच्या हुकाचं टोक Play-त्रिकोण बनवणारा लोगो (गणेश-प्रतीक + "ऑडिओ गाईड" एकत्र) — जुना कलश-आयकॉन बदलला. Favicon साठी वेगळी सोपी आवृत्ती लागली (मूळ डिझाइन १६×१६ ला अस्पष्ट होता — शिप करण्याआधी झूम करून तपासलं).
> - GA4 analytics, SEO (og/twitter tags, robots.txt, sitemap.xml, JSON-LD), नवीन homepage tagline — सर्व झालं
> - सजावट-आरास व्हिडिओ — कोड तयार, फाइल **अजून नाही**
> - Ownership scaffolding — "Nilesh" (प्रथम नाव) भरलं, पूर्ण आडनाव बाकी
>
> **जुनी पडताळणी (१-२ Sep, अजूनही खरी असण्याची शक्यता — पुन्हा तपासलेली नाही):** रंग-टोकन, Wake Lock/Media Session API, QR चौरस modules + EC-Q (५ परिस्थितींत २४/२४), प्रिंट DPI. ⚠️ **या सर्वांना वरच्या आयुध-चक्र redesign चा किती परिणाम झाला ते तपासलेलं नाही** — विशेषतः रंग-टोकन/फाँट अजून तेच आहेत का, ते नक्की करा.

---

## 🏷️ नाव-निवड — २० पर्याय (निर्णय बाकी)

> आधी फक्त चॅटमध्ये दिले होते, फाइलमध्ये नव्हते — इथे कायमचे. `[ ]` वर `[x]` करून निवडा.

**प्रोजेक्ट/ब्रँड-नाव (poetic — कुटुंब + पोर्टफोलिओ दोन्हीसाठी):**

- [ ] परंपरा ते प्रज्ञा — Tradition → Wisdom (प्रज्ञा = शहाणपण **आणि** intelligence, AI शी double-meaning)
- [ ] **मूर्ती बोलते** — The Idol Speaks — सर्वात साधं, भावनिक, लक्षात राहणारं ⭐ *(माझी टॉप शिफारस)*
- [ ] श्रद्धा × संहिता — Faith × Code (संहिता = धर्मग्रंथ **आणि** codified system)
- [ ] मूक शस्त्रांची वाणी — Voice of the Silent Weapons — जास्त काव्यात्मक
- [ ] आयुध.AI — modern/techy, domain-नाव म्हणूनही वापरता येईल
- [ ] बाप्पाच्या हातातलं रहस्य — curiosity-hook, शेअर होण्याजोगं
- [ ] कर-कथा — हात-कथा (कर=हात) — छोटं, अनोखं संस्कृत-मराठी जोड
- [ ] **बाप्पा बोलतो** — बोलीभाषेतलं, उबदार, reel/meme-friendly ⭐ *(दुसरी टॉप शिफारस)*
- [ ] आयुधवाणी — एक-शब्दी ब्रँड-नाव (Koo/ShareChat स्टाईल)
- [ ] मूर्तीशास्त्र.ऐका — domain-सारखं वाटणारं
- [ ] घरचा गणपती, डिजिटल गाईड — साधं, शोधता येण्याजोगं (productize केलं तर उपयोगी)
- [ ] आयुध आर्काइव्ह — clean इंग्रजी-मराठी संकर, GitHub-repo स्टाईल professional
- [ ] स्कॅन आणि श्रद्धा — कार्यात्मक+भावनिक जोडी
- [ ] घंटा ते गीगाबाईट — Temple-bell to Gigabyte — तीव्र परंपरा↔तंत्रज्ञान विरोधाभास, tagline-style
- [ ] **एक स्कॅन, एक अवतार** — One Scan, One Form — "अवतार" चा दुहेरी अर्थ (देवाचं रूप + digital avatar), स्मार्ट wordplay ⭐ *(तिसरी टॉप शिफारस — portfolio ला उठून दिसेल)*

**टॅगलाइन/कॅप्शन-स्टाईल (नाव नाही, पण वापरता येण्याजोगं):**

- [ ] २० आयुधे, २० कथा — आकडा-हुक, listicle-format सोशलवर सर्वात जास्त शेअर होतो
- [ ] NFC नमस्कार — तंत्रज्ञान+विधी यांचा खेळकर पन — Instagram कॅप्शनसाठी
- [ ] QR ने कथा, कानाने संस्कार — "क" अनुप्रासामुळे लक्षात राहणारं
- [ ] शब्द ते ध्वनी: आयुधांची गोष्ट — TTS pipeline चं process-वर्णन, तांत्रिक खोली दाखवतं
- [ ] शस्त्र संहिता AI — तांत्रिक+शास्त्रीय जोड, LinkedIn headline साठी keyword-rich

**केस-स्टडी headline (portfolio scan-title — नाव वेगळं, हे वेगळं; recruiter साठी outcome-descriptive हवं, संशोधनाने सिद्ध — वर बघा):**

- [x] ⭐ **अंतिम निवड — Title + Subtitle:**
  > ## No One Could Explain the Idol's Symbolism Anymore
  > *How I Gave Our Family's Real Ganpati Decoration an AI-Narrated Voice and a Modern Digital Layer — Solo, Offline-First*
- [ ] *(पहिला मसुदा, आता superseded):* "Giving Voice to 20 Sacred Symbols — a solo AI + UX case study" (offline PWA · QR/NFC · AI-narrated Marathi audio guide)

---

## 📷 फोटो / व्हिज्युअल्स — प्लेसहोल्डर यादी

तुम्ही rough तयारीचे फोटो देणार आहात — इथे प्रत्येक स्लॉट कुठे लागेल आणि काय हवं ते. प्रकाशित करण्याआधी प्रत्येक `[PHOTO: ...]` जागी खरा फोटो टाका.

| # | कुठे लागेल | काय फोटो हवा | स्थिती |
|---|---|---|---|
| 1 | Section 0 Hook (cover) | मोबाईलमध्ये live साइट उघडलेली, हातात धरलेली — किंवा गणपती मूर्ती + फोन scan करतानाचा शॉट | 🔲 |
| 2 | Section 2 (सुरुवात) | घरचा देव्हारा / गणपती मूर्ती — आयुधं दिसतील असा वाइड शॉट | 🔲 |
| 3 | Section 2 (सुरुवात) | `००३ अंकुश` चा खरा कुटुंब-फोटो (`ankush.jpg`) — **हा आधीच आहे**, वापरता येईल | ✅ existing |
| 4 | Section 5 (Design decisions) | Redesign च्या ३ संकल्पनांचा तुलना-स्क्रीनशॉट (संग्रहालय फलक / पूजा पत्रिका / दिवा प्रकाश) — जर screenshot घेतला असेल | 🔲 |
| 5 | Section 5 / QR निर्णय | जुनं (गोल modules) vs नवं (चौरस modules) QR कार्ड side-by-side | 🔲 |
| 6 | Section 6 (AI workflow) | Claude Code / टर्मिनल स्क्रीनशॉट — काम करतानाचा (ऐच्छिक, पण "process दाखवणं" recruiter ला आवडतं — संशोधनात सापडलं) | 🔲 |
| 7 | सजावट आरास | तयारी/मखर सजावटीचे rough फोटो — QR/NFC कसे लावले, भौतिक आयुध-निर्मिती (3D print/clay) चे फोटो | 🟡 **अंशतः** — `aaras-poster.jpg` आहे; तयारीचे rough फोटो + निर्मिती-प्रक्रियेचे फोटो अजून हवेत |
| 8 | Section 7 (Testing) | पाहुणे प्रत्यक्ष QR स्कॅन करतानाचा फोटो/व्हिडिओ (guest testing झाल्यावर) | 🔲 testing नंतर |
| 9 | Section 9 / प्रिंट | छापलेली QR कार्ड्स + NFC टॅग लावलेला फोटो | 🔲 |
| 10 | Cover / hero (केस स्टडी प्लॅटफॉर्मसाठी) | 1200×630 social-share कव्हर इमेज (Canva) | 🔲 |
| 11 | **🆕** Section 5 Decision 12 | `design-demos/` मधल्या ९ पर्यायी होमपेज-संकल्पनांचे स्क्रीनशॉट (wheel/mala/bento/coverflow इ.) — "मी screens बनवले नाही, निर्णय घेतला" हे दाखवायला सर्वोत्तम पुरावा | 🔲 **screenshot घेणं सोपं, फोटोची गरज नाही — मीच काढून देऊ शकतो, सांगा** |
| 12 | **🆕** Section 5 Decision 12/13 | आयुध-चक्र (फिरतं मंडल) चालू असतानाचा स्क्रीन-रेकॉर्डिंग/GIF + जुना-नवा लोगो side-by-side | 🔲 **मीच काढून देऊ शकतो** |

**नियम:** खरा फोटो येईपर्यंत `[PHOTO: विवरण]` असं मार्कर ठेवा — रिकामी जागा किंवा stock फोटो वापरू नका (Section 8 "काय चाललं नाही" च्या प्रामाणिकपणाच्या भावनेशी विसंगत होईल).

---

## Section 0 — Hook

# मी घरातल्या गणपतीच्या मूर्तीला ऑडिओ गाईड दिला. प्रत्येक आयुधाची स्वतःची कथा आहे.

*QR / NFC स्कॅन करा — बाप्पाच्या हातातल्या २० आयुधांची (एकदंत, परशू, अंकुश, सुदर्शन चक्र, खट्वांग…) मराठी ऑडिओ कहाणी, मूळ ग्रंथसंदर्भासह. ₹० होस्टिंगवर, framework शिवाय, ऑफलाइनही चालतं. 【पडताळा: संख्या २३→२० झाली, हुक-वाक्य अपडेट केलं पण पूर्ण मसुदा अजून जुना आहे】

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
Timeline     →  २० Aug 2026 पहिला commit → १४ Sep 2026 पर्यंत सक्रिय
                (~३.५ आठवडे, टप्प्याटप्प्याने; रोजचे तास 【पडताळा】)
Stack        →  Vanilla HTML/CSS/JS · PWA + Service Worker · single data.json
                · Python (qrcode / Pillow / pyzbar / uharfbuzz) · Claude Code
                · Sarvam Bulbul v3 TTS · AI image tools
Results      →  ✅ २०/२० आयटम्सचा खरा आवाज (सर्व AI-TTS, पडताळलं — Section 8 #१२ मध्ये
                मानवी-आवाज→TTS trade-off प्रामाणिकपणे मांडलं आहे)
                ❗ Guest testing अजून बाकी — तांत्रिक पडताळणी पूर्ण (QR 21/21
                decode सर्व ५ stress-परिस्थितींत 【३dc3ae7 नुसार — 24 नव्हे,
                item-count 23→20 झाल्यावर आकडा बदलला】, live 200 OK)
Impact       →  Maharashtra मधल्या घरांसाठी / गणेशोत्सव मंडळांसाठी productizable template
```

---

## 🌐 English toggle — योजना (साइटच्याच पॅटर्नने)

> साइटवर आधीच language-toggle mechanism आहे (सध्या लपवलेला, कारण इंग्रजी मजकूर नाही). केस स्टडीतही तोच MR/EN जोडी-पॅटर्न वापरणार — जेव्हा हे प्रकाशित करू (Notion/Artifact/webpage), तेव्हा प्रत्येक विभागाखाली EN block, वर टॉगल बटण.

**आत्ता भाषांतर केलं** (स्थिर विभाग — बदलण्याची शक्यता कमी):
- ✅ Section 0 Hook
- ✅ Section 1 TL;DR

**मुद्दाम भाषांतर केलेलं नाही अजून** (अस्थिर — Section 2 खरी आठवण अजून लिहायचीय, Section 4/7 guest-testing नंतर भरायचेत, Section 5/8 पूर्ण refresh बाकी) — **आधी मराठी मजकूर अंतिम करा, मग भाषांतर करा** — नाहीतर दोनदा काम होईल. मराठी अंतिम झाल्यावर सांगा, उरलेलं भाषांतर करतो.

### Section 0 — Hook (EN)

# No One Could Explain the Idol's Symbolism Anymore

### How I Gave Our Family's Real Ganpati Decoration an AI-Narrated Voice and a Modern Digital Layer — Solo, Offline-First

*Scan a QR or tap NFC — Marathi audio stories for the 20 ritual weapons/attributes (आयुधे) in Ganpati's hands (Ekadanta, Parashu, Ankusha, Sudarshan Chakra, Khatvanga…), sourced verbatim from the original scripture guide. ₹0 hosting, no framework, works offline.

**[▶ Live demo](https://smartconnect2020-hash.github.io/Ganpati_ai_museum/)** &nbsp;&nbsp; **[GitHub](https://github.com/smartconnect2020-hash/Ganpati_ai_museum)**

### Section 1 — TL;DR (EN)

```
Problem      →  Every weapon in Ganpati's idol carries real scriptural meaning —
                but during the festival no one explains it to guests/kids;
                the reference text stays shut in a cupboard
Solution     →  QR + NFC audio guide, 20 items, Marathi-first, offline PWA,
                text verbatim from the source guide + AI-TTS narration
My role      →  Solo — research + UX + visual design + no-framework build
                + QR/NFC pipeline + TTS pipeline + AI-workflow orchestration
Timeline     →  First commit 20 Aug 2026 → active through 14 Sep 2026
                (~3.5 weeks, in phases)
Stack        →  Vanilla HTML/CSS/JS · PWA + Service Worker · single data.json
                · Python (qrcode / Pillow / pyzbar / uharfbuzz) · Claude Code
                · Sarvam Bulbul v3 TTS · AI image tools
Results      →  ✅ Real audio for 20/20 items (all AI-TTS, verified — see Section 8 #12
                for the honest human-voice-to-TTS trade-off)
                ❗ Guest testing still pending — technical verification done
                (QR 21/21 decode across 5 stress conditions, live 200 OK)
Impact       →  Productizable template for Maharashtra households / Ganeshotsav mandals
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

### 🧰 Guest-testing किट (आता प्रत्यक्ष वापरण्यासाठी तयार — १४ Sep 2026)

> मी (Claude) प्रत्यक्ष पाहुण्यांना भेटू शकत नाही किंवा मुलाखत घेऊ शकत नाही — फक्त **साधनं तयार करू शकतो.** खाली दिलेलं सर्व रिकामं/टेम्प्लेट आहे — एकही सेल आधीच भरलेला नाही. गणेशोत्सव/पाहुणे आल्यावर हेच वापरून थेट Section 4 व 7 भरता येतील.

**पाहुण्याला सांगायचं (संमती + framing):**
> *"आमच्याकडे गणपतीच्या आयुधांची QR-ऑडिओ गाईड आहे — स्कॅन करून बघता का? नंतर २ मिनिटं feedback विचारेन, चालेल का?"*

**Live observation log** (प्रत्येक पाहुण्यासाठी एक ओळ — स्कॅन करतानाच भरा):

| पाहुणा (वय/नातं) | QR की NFC वापरलं | scan → audio सुरू (सेकंद) | पूर्ण ऐकलं / मध्येच थांबवलं (कुठे) | पुन्हा दुसरं आयुध बघितलं का | अडचण आली का (काय) |
|---|---|---|---|---|---|
| *(रिकामं)* | | | | | |
| *(रिकामं)* | | | | | |

**अनुभवानंतरचे ३ प्रश्न** (३० सेकंदांत उत्तर द्यायला हवेत — जास्त लांबलं तर पाहुणा कंटाळतो):
1. "आयुधाची गोष्ट आधी माहीत होती का? आत्ता नवीन काय कळलं?"
2. "स्कॅन करणं सोपं वाटलं की किचकट?" (मोकळेपणाने बोलू द्या, हो/नाही मध्ये अडकवू नका)
3. "अजून काय हवं वाटलं — इंग्रजी, अधिक फोटो, अजून काही?"

**संपादक-चाचणी** (कुटुंबातल्या एका बिगर-तांत्रिक व्यक्तीला मदतीशिवाय):
- कार्य: `data.json` मध्ये एक (काल्पनिक) नवीन आयुध entry जोडून बघा — किती वेळ लागला, कुठे अडखळले, मदत लागली का
- हे Decision "JSON-as-CMS" च्या दाव्याची खरी पडताळणी आहे (Section 5)

**Section 7 च्या मेट्रिक्स टेबलमध्ये भरायला — याच किट मधून थेट मिळेल:**
वरच्या log मधून "scan → audio सुरू" सरासरी काढा, "पूर्ण ऐकलं" चं प्रमाण काढा, संपादक-चाचणीचा वेळ नोंदवा — कुठलाही आकडा अंदाजाने टाकू नका.

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

### 🎯 Decision 12 — यादी/कार्ड-list ऐवजी "आयुध-चक्र" फिरतं मंडल (१६ Sep पर्यंतचा सर्वात मोठा redesign)

**आधीचं:** साधी स्क्रोल-करण्याजोगी यादी/कार्ड-ग्रिड — कार्यक्षम, पण "२० वेगवेगळ्या वस्तूंमधलं नातं" काहीच दाखवत नव्हती.

**नवीन:** मध्यभागी ॐ, त्याभोवती दोन एकसमान फिरणाऱ्या रिंगमध्ये २० आयुधं — मंदिरातल्या मंडल/चक्राची भावना. Auto-rotate (धीमं, थांबवता येणारं), drag-to-rotate, मध्यभागी "यादृच्छिक आयुध सुचव" बटण.

**Exploration:** एकदम या डिझाइनवर उडी मारली नाही — `design-demos/` मध्ये **९ पूर्ण पर्यायी संकल्पना** (wheel, mala, featured, scroll, deck, bento, playlist, mandala चे ३ refinement टप्पे, coverflow) कोडसह जतन आहेत — निर्णय-प्रक्रिया दाखवण्यासाठी उत्तम पुरावा.

**Trade-off/समस्या सापडली आणि सोडवली:** मोबाईलवर (375px मोजून) २० नोड्स एका रिंगवर ठेवल्यास शेजारी-शेजारी अंतर फक्त ~44px उरत होतं, पण किमान tap-target (44px) नोड स्वतःच ~60px भरत होता — **overlap गणिती अपरिहार्य होता, CSS ने सुटणारा नव्हता.** उपाय: 600px खाली रिंग पूर्ण लपवली, त्याजागी Spotify/Instagram-Stories स्टाईल swipeable circle-row (existing accessible legend-list चाच पुनर्वापर — screen-reader साठी वेगळं काही सांभाळायला लागत नाही).

**धडा:** "एकच रिंग सर्व स्क्रीन आकारांना पुरेल" हे गृहीतक चुकलं — प्रत्यक्ष मोजमापानेच (375px viewport वर नोड-अंतर) कळलं, अंदाजाने नाही.

### 🎯 Decision 13 — नवीन ब्रँड-मार्क, आणि favicon साठी वेगळी सोपी आवृत्ती

जुना इनलाइन कलश-SVG आयकॉन बदलून नवीन मार्क — अंकुशाच्या हुकाचं टोक Play-बटणाचा त्रिकोण बनतं (गणेश-प्रतीकवाद + "हे ऑडिओ गाईड आहे" एकाच रेषेत). हेडर/192px/512px/apple-touch साठी तपशीलवार आवृत्ती वापरली, पण **16×16/32×32 favicon ला तीच आवृत्ती अस्पष्ट दिसली** (शिप करण्याआधी zoom करून प्रत्यक्ष तपासलं) — म्हणून favicon साठी फक्त हुक+त्रिकोणाचा वेगळा सोपा crop बनवला. एकच आयकॉन सर्व आकारांना चालत नाही हे इथेही खरं ठरलं (Decision 12 सारखंच).

### 🎯 Decision 14 — भौतिक आयुध-निर्मिती: AI संदर्भ-प्रतिमा → 3D प्रिंट/चिकणमाती → acrylic फिनिशिंग (🆕 १९ Sep — 【युजरने पडताळायचं — नवीन माहिती, screenshot/फोटोने अजून verify केलेली नाही】)

> हा भाग साइटच्या *सॉफ्टवेअर* भागापेक्षा वेगळा आहे — प्रत्यक्ष मखरातल्या आयुधांच्या मूर्ती **कशा बनवल्या** याची प्रक्रिया. केस स्टडीत हे "AI फक्त कोडपुरतं नाही, भौतिक क्राफ्टलाही लागलं" हे दाखवणारा सर्वात मजबूत पुरावा ठरेल — recruiter साठी दुर्मिळ combo (digital + physical maker workflow).

**पाइपलाइन (डिजिटल → भौतिक):**
1. **AI संदर्भ-प्रतिमा** — प्रत्येक आयुधाचं AI-generated टर्नअराउंड/रेफरन्स शीट आधी तयार केलं (हेच `media/item-XXX/design-ref*.jpg` — गॅलरीतही वापरलेलं संदर्भचित्र, Decision बद्दल वर नोंद आहे).
2. **भौतिक निर्मिती — दोन पद्धती एकत्र:** काही आयुधे **3D प्रिंट** केली, काही **चिकणमातीने (clay) हाताने घडवली** — AI संदर्भ-प्रतिमेनुसार आकार ठरवून.
3. **फिनिशिंग:** आधी **काळा स्प्रे पेंट** प्राइमर कोट (base), मग त्यावर **acrylic रंगांनी** डिटेल पेंटिंग/फिनिशिंग — दगड/धातू/लाकडाचा वास्तव भास यावा म्हणून.
4. **आकारमान-मानकीकरण (उभं राहण्यासाठी/मांडणीसाठी):** मूर्तीची उंची सुमारे **८ इंच**, स्टँडची उंची सुमारे **१० इंच** — जेणेकरून सर्व २० आयुधे मखरात एकसमान दिसतील. **【स्पष्टीकरण हवं】** हे दोन आकडे नक्की कसे जोडतात हे अजून स्पष्ट नाही — (अ) मूर्ती + स्टँड मिळून एकूण उंची १०" (स्टँड फक्त २" उंच), की (ब) स्टँड स्वतःच १०" उंच (मूर्तीपेक्षा उंच पेडेस्टल, मूर्ती अधिक ठळक दिसण्यासाठी) — दोन्ही शक्य आहेत, इथे कुठलाही अंदाज बांधलेला नाही, फोटो आल्यावर नक्की करा.
5. **जागा वाचवण्यासाठी डिझाइन-निर्णय:** खालच्या रांगेत/कमी उंचीवर मांडायच्या आयुधांसाठी **लहान (उरलेल्या उंचीचे) स्टँड** वापरले — जेणेकरून एकंदर मखर कमी जागेत बसेल, तरी प्रत्येक मूर्ती नीट दिसेल.
6. **बॅकड्रॉप:** स्टँड्सच्या मागे/खाली **काळ्या थीमशी जुळणारा पेपर** वापरला — जेणेकरून प्रत्येक आयुध दृश्यदृष्ट्या उठून दिसेल (उच्च कॉन्ट्रास्ट, फोटो/व्हिडिओतही स्वच्छ दिसतं).
7. **संशोधन/मजकूर (कंटेंट लेयर):** प्रत्येक आयुधामागची कथा/दार्शनिक अर्थ **मूळ पुराणग्रंथांतून (पुराणे) आणि मूळ स्रोतांतून संदर्भ गोळा करून** संकलित — हाच मजकूर वेबसाईटवर टाकला (Decision 8 "verbatim" तत्त्वाशी सुसंगत) आणि त्यावरून प्रत्येक आयुधाचं मराठी ऑडिओ तयार केलं (TTS पाइपलाइन — Section 6).
8. **QR थर:** प्रत्येक आयुधासाठी **स्वतंत्र QR कोड** (त्या एका आयुधाच्या माहितीकडे नेणारा) + **मुख्य लँडिंग-पेजसाठी एक वेगळा मास्टर QR** (संपूर्ण साइट/यादीकडे नेणारा) — दोन्ही वेगळ्या स्तरांवर (per-item deep-link vs. home).

**हेतू (design rationale, दोन ओळीत):** पुराणातली माहिती दाट/जड भाषेत असते, आणि जुन्या पिढीला वाचवत नाही किंवा वाचता येत नाही अशा पाहुण्यांसाठी संपूर्ण मजकूर **ऐकता यावा** म्हणून ऑडिओ थर जोडला — म्हणजे "वाचता न येणाऱ्यांसाठी" हे प्रवेशयोग्यतेचं (accessibility) मूळ कारण आहे, केवळ नावीन्यासाठी टेक जोडलेली नाही.

**थीम-फ्रेमिंग (केस स्टडीच्या headline साठी वापरण्याजोगी):** *"AI + परंपरागत उत्सव"* आणि *"विज्ञान + सण-उत्सव"* — म्हणजे आधुनिक तंत्रज्ञान (AI इमेज जनरेशन, 3D प्रिंटिंग, TTS, QR) पारंपरिक गणेशोत्सव सजावटीला **बदलत नाही, तर तिचा अर्थ अधिक लोकांपर्यंत पोहोचवतं** — parody किंवा gimmick म्हणून नाही.

**पुढचं पाऊल (पडताळणी बाकी):** वरची सर्व माहिती युजरने चॅटमध्ये सांगितलेली आहे, कुठल्याही फोटो/मापाने अजून पडताळलेली नाही — **वास्तविक फोटो/व्हिडिओ आल्यावर** (`media/decoration/` — Section 9 मध्ये नोंद आहे) इथले आकडे (८"/१०") आणि पद्धत (कुठले आयुध 3D-print, कुठले clay) प्रत्यक्षाशी जुळवून घ्या.

---

## Section 6 — AI-assisted design workflow

> `DESIGN-DECISIONS.md` §6 + PROJECT-STATUS मधून — या प्रोजेक्टचा खरा workflow.

| Tool | भूमिका | माणसाने काय, AI ने काय |
|---|---|---|
| **Claude Sonnet 5 (Claude Code)** | Spec architect + implementation | मी constraints दिल्या; Claude ने १८-विभागी build-spec रचला, redesign (CSS/JS/HTML) implement केला. QR pipeline (Python scripts) — 【पडताळा: Claude ने की तुम्ही】 |
| **`ui-ux-pro-max` skill** | Color/typography/style domain search | पॅलेट व फाँट-जोड्या सुचवल्या; **अंतिम निवड माझी** + manual WCAG गणित |
| **`design:design-critique` दृष्टिकोन** | Review lens | सध्याच्या साइटचा designer's-eye रिव्ह्यू, मग redesign |
| **Claude Browser (in-app)** | Live testing | DOM / console / accessibility-tree + click-tests. **Pixel screenshot उपलब्ध नव्हता** — पडताळणी computed-style वर आधारित |
| **AI image tools (OpenArt / Seedream 4.5)** | आयकॉन-निर्मिती | App icon (कलश) + ९ आयुध-बॅज AI-चित्रित; credits संपल्यावर उरलेले बॅज Claude ने vector आर्ट म्हणून काढले (cubic-bezier, दुरंगी gold gradient). 【मूळ १३ होते (३० Aug नोंद) — नंतर ३ आयुधे बंद झाल्याने (कवच/खंजीर/पुष्पबाण) आता **१०** उरले आहेत — १४ Sep ला data.json शी पडताळून दुरुस्त केलं】 |
| **Python (qrcode / Pillow / pyzbar)** | QR pipeline | २४ सानुकूल QR कार्ड्स local generate + pyzbar ने २४/२४ decode-पडताळणी + stress-test (तिरकं/अंधुक/लांबून) |
| **🆕 Sarvam Bulbul v3 (TTS)** | **सर्व २०/२० आयुधांचा आवाज** | `_generate_audio_tts.py`. Voice "ritu", pace 0.98, temperature 1.0. **STT (speech-to-text) ने परत मजकूर काढून approved script शी cross-check** — उच्चार-अचूकतेची स्वयंचलित पडताळणी, फक्त "ऐकून ठीक वाटलं" नाही. सुरुवातीला एकदंत (००१) चं मानवी रेकॉर्डिंग वेगळं ठेवलं होतं, पण **नंतर तेही जाणीवपूर्वक TTS ने बदललं** — सुसंगततेसाठी, युजर-मंजुरीने (मूळ .wav डिस्कवर सुरक्षित). हे केस स्टडीसाठी **सर्वात मजबूत AI-वर्कफ्लो पुरावा** आहे — पूर्ण मजकूर उत्पादनासाठी न वापरता, अचूकता-पडताळणीसह वापरलं. |

**प्रामाणिक self-assessment:**
- **AI ने चांगलं केलं:** repetitive scaffolding, syntax, edge-case enumeration, contrast गणित, QR stress-simulation
- **मी override केलं:** धार्मिक/शास्त्रीय मजकुराची verbatim अचूकता, emotional design, dark-mode काढण्याचा निर्णय, फाँट काढण्याचा निर्णय, prioritization
- **धडा:** AI execution-वेळ compress करतो. Design judgment माणसाकडेच.
- **मर्यादा:** या सेशनमध्ये pixel-screenshot QA शक्य नव्हतं; खरी device-चाचणी बाकी.

### AI × UX ची सांगड — मुलाखतीत विचारले जाणारे प्रश्न (draft उत्तरं — पडताळून अंतिम करा)

> Recruiter/मुलाखतकार अनेकदा "AI वापरलंस, पण UX चं काम कुठे आहे?" असं विचारतात. या प्रोजेक्टमध्ये उत्तर स्पष्ट लिहायला हवं:

1. **"खरी समस्या काय होती, आणि AI का लागलं?"**
   *उत्तर-मसुदा:* समस्या UX ची होती (लोकांना आयुधांचा अर्थ माहीत नाही, वाचायला वेळ/इच्छा नाही) — तंत्रज्ञानाची नाही. उपाय ठरवताना (ऑडिओ-गाईड, QR/NFC, मराठी-first) AI आलंच नाही — तो **निर्णय संशोधन/constraints मधून आला.** AI आलं **अंमलबजावणीत**: १८-विभागी spec पासून implementation पर्यंतचा वेळ compress करायला, आणि २० आवाज एकट्याने रेकॉर्ड करणं अशक्य असताना (वेळ, आवाजाचा दर्जा सुसंगत ठेवणं) TTS ने ते शक्य केलं.

2. **"AI च्या आउटपुटवर तुझा UX निर्णय कुठे दिसतो?"**
   *उत्तर-मसुदा:* डिझाइन-रंग/फाँट AI ने सुचवले, पण अंतिम निवड + WCAG गणित माणसाने केलं (Decision 2, 3). TTS आवाज निवडताना नुसतं "generate करून वापरणं" नाही — **STT ने परत पडताळणी** ही स्वतः जोडलेली quality-gate पायरी आहे, जी कुठल्याही AI tool मध्ये आपोआप येत नाही. हीच UX/product-thinking ची जागा — "AI आउटपुट विश्वासार्ह आहे का" हे ठरवणं.

3. **"मानवी आवाजाऐवजी AI आवाज वापरणं — हे विरोधाभासी नाही का (परंपरा जपण्यासाठी बनवलेल्या प्रोजेक्टमध्ये)?"**
   *उत्तर-मसुदा (प्रामाणिक, तुम्ही अंतिम करा):* मूळ योजना मानवी आवाज होती (एकदंतसाठी अजूनही आहे). पण २० आयुधांचं सुसंगत-दर्जाचं रेकॉर्डिंग एकट्याने करणं व्यवहार्य नव्हतं. **निवड:** मजकूर १००% मूळ ग्रंथातून verbatim ठेवला (सामग्रीची सत्यता), आवाजासाठी AI वापरला पण अचूकता-पडताळणी (STT cross-check) जोडली (आवाजाच्या विश्वासार्हतेची हमी). *"परंपरा मजकुरात जपली, तंत्रज्ञान पोहोचवण्यासाठी वापरलं"* — ही framing खरी आहे आणि केस स्टडीच्या नावाशीही जुळते (खाली सुचवलेली नावं बघा).

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
9. **Id sequential करायचा प्रयत्न मागे घ्यावा लागला** — एका commit ने वस्तूंचे id गॅपशिवाय (००१-०२०) केले, "स्वच्छ" दिसावं म्हणून. पण ६ आयटम्सचे QR/NFC आधीच जुन्या id वर छापलेले/एन्कोड होते — स्कॅन चुकीच्या वस्तूवर जायला लागला. मागे घेतलं, मूळ id कायमचे ठेवले. धडा: छापील/भौतिक वस्तूंशी जोडलेला कुठलाही ओळख-क्रमांक (id, URL) एकदा "बाहेर" गेला की **कधीही सौंदर्यासाठी बदलू नये** — हाच धडा custom-domain च्या निर्णयालाही लागू पडला (Section 9).
10. **एका रिंगमध्ये सर्व २० आयुधं मोबाईलवर बसवण्याचा पहिला प्रयत्न फसला** — ३७५px वर नोड्स गणितीयदृष्ट्या एकमेकांवर चढत होते (मोजून सापडलं, अंदाजाने नाही). उपाय CSS-tuning नव्हता — पूर्ण वेगळा मोबाईल-पॅटर्न (swipeable row) लागला.
11. **नवीन ब्रँड-मार्क favicon आकारात वाचता येत नव्हता** — शिप करण्याआधी zoom करून तपासलं, वेगळी सोपी आवृत्ती बनवावी लागली. धडा: एकच आयकॉन सर्व आकारांना चालत नाही — प्रत्येक वापराच्या आकारात प्रत्यक्ष बघून तपासा.
12. **"मानवी आवाज हाच अस्सलपणा" हा मूळ निर्णय स्वतःच मागे घेतला** — एकदंतचं (००१) खरं मानवी रेकॉर्डिंग होतं, पण नंतर तेही AI-TTS ने बदललं — सुसंगततेसाठी. हे केस-स्टडीत लपवण्याजोगं नाही: मूळ मूल्य (माणसाचा आवाज) आणि व्यावहारिकता (सुसंगत पाईपलाईन, स्केल) यांच्यात **खरा trade-off होता, आणि सुसंगततेची बाजू जिंकली.** प्रामाणिकपणे मांडणं हेच योग्य — लपवणं उलट संशय निर्माण करेल.

---

## Section 9 — पुढे काय

> 🆕 **१६ Sep स्थितीनुसार अपडेट:**

- [x] ~~खरा आवाज~~ — **पूर्ण** (२०/२०, सर्व Sarvam Bulbul v3 TTS — एकदंतचं मानवी रेकॉर्डिंगही नंतर TTS ने बदललं)
- [x] ~~होमपेज redesign~~ — **पूर्ण** ("आयुध-चक्र" फिरतं मंडल + मोबाईल swipe-row)
- [x] ~~ब्रँड-मार्क/लोगो~~ — **पूर्ण**
- [x] ~~SEO + analytics~~ — **पूर्ण** (GA4, og/twitter tags, sitemap, JSON-LD)
- [~] **सजावट आरास व्हिडिओ** — poster-फोटो + YouTube Shorts teaser (live fallback) आलं; **खरी `aaras.mp4`/`aaras-sd.mp4` फाइल अजून बाकी** (पायऱ्या `media/decoration/README.md` मध्ये)
- [ ] **भौतिक पायरी** — QR कार्ड्स रंगीत प्रिंट (३ फॉरमॅट तयार, verified) · खरा फोन-कॅमेरा scan-टेस्ट · NFC टॅग्स (NTAG213) · लाकूड/कार्डबोर्ड मागे लावणे
- [ ] **English** — इंग्रजी ऑडिओ + English toggle पुन्हा चालू (आत्ता तात्पुरता लपवलेला)
- [ ] **Guest testing** — पाहुणे बोलावून निरीक्षण + मुलाखत → Section 4 + 7 भरणे
- [ ] **केस स्टडी पूर्ण refresh** — हा मसुदा अजून जुन्या (२३-आयुध) आकड्यांवर आहे बऱ्याच ठिकाणी
- [ ] **CMS upgrade** (ऐच्छिक) — Google Sheets → n8n → JSON → GitHub push pipeline
- [ ] **आयकॉन** — credits आल्यावर **१०** vector बॅज AI-चित्रणाने बदलणे (आयटम: ०११,०१२,०१३,०१४,०१६,०१७,०१८,०२०,०२१,०२३ — १४ Sep ला data.json शी पडताळून मोजलं; आधी १३ म्हटलं जायचं, ३ आयुधे बंद झाल्याने कमी झाले)
- [ ] **v2** — multi-family / गणेशोत्सव-मंडळ template म्हणून productized service; प्रति-आयुध WhatsApp bot
- [ ] **Custom domain**
- [ ] `OWNERSHIP.md` मधलं legal name placeholder भरणे (AI भरू शकत नाही — फक्त तुम्ही)

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
