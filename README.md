# श्री गणेश आयुधे — कुटुंबासाठी मार्गदर्शक (Nilesh)

Repo: **Ganpati_ai_museum**  
कुटुंब: **Nilesh**  
Live: **https://smartconnect2020-hash.github.io/Ganpati_ai_museum/**

ही वेबसाइट QR किंवा NFC स्कॅन केल्यावर गणपतीच्या **२३ आयुधांपैकी** एकाची ऑडिओ कहाणी, दार्शनिक अर्थ, मूळ ग्रंथसंदर्भ + चित्र दाखवते. मजकूर मूळ गाईड-ग्रंथातून जसाच्या तसा घेतलेला आहे.

> **सद्यस्थिती (थोडक्यात):** कोड + मजकूर + चित्रं + QR कार्ड्स तयार, साइट live.  
> बाकी — २३ पैकी **२२ आयुधांचा खरा आवाज** (स्क्रिप्ट्स `audio-scripts/` मध्ये तयार, फक्त वाचून रेकॉर्ड करायचे) आणि **भौतिक पायरी** (QR प्रिंट + NFC टॅग + फोनवर स्कॅन-टेस्ट). पूर्ण तपशील: `PROJECT-STATUS.md`.

---

## पाहुण्यांसाठी कसे चालते?

1. आयुधाजवळचा **QR स्कॅन** करा किंवा **NFC** टॅगला फोन लावा  
2. वेबपेज उघडेल → मोठे सोनेरी **ऐका** (मुद्रा) बटण दाबा  
3. मराठी हीच डीफॉल्ट भाषा. *(English टॉगल सध्या लपवलेला — इंग्रजी मजकूर/आवाज अजून तयार नाही.)*

URL उदाहरणे (live):
- सर्व २३ ची यादी: https://smartconnect2020-hash.github.io/Ganpati_ai_museum/
- एक आयुध (एकदंत): https://smartconnect2020-hash.github.io/Ganpati_ai_museum/?id=001
- GitHub repo: https://github.com/smartconnect2020-hash/Ganpati_ai_museum

---

## संगणकावर लोकल पहाणे

PowerShell मध्ये प्रोजेक्ट फोल्डर उघडा:

```powershell
cd e:\Ganpati_audio_qr_project
python -m http.server 8080
```

ब्राउझर: http://localhost:8080/

> `index.html` डबल्-क्लिकने उघडू नका — `data.json` लोड होणार नाही. वरचा लोकल सर्व्हर वापरा.

---

## खरा आवाज रेकॉर्ड करणे (मुख्य उरलेलं काम)

२३ आयुधांचा मजकूर, चित्रं व `data.json` तयार आहे. फक्त आवाज बाकी — २३ पैकी **१ (एकदंत) झाला, २२ शांत placeholder** आहेत.

1. `audio-scripts/` मधली त्या आयुधाची फाइल उघडा (उदा. `item-005-सुदर्शन-mr.md`)  
   - 🎙 खालचा मजकूर **तोच वाचायचा**, शब्दशः · 🔊 / `[SFX]` ओळी **वाचायच्या नाहीत** (त्या ध्वनी-संयोजकासाठी)  
2. फोन Voice Recorder / WhatsApp voice note — स्पष्ट मराठी  
3. फाइल इथे ठेवा (जुनी शांत फाइल बदला): `media/item-XXX/audio-mr.mp3`  
   *(पाथ `data.json` मध्ये आधीच बरोबर आहे — फक्त overwrite करा)*  
4. लोकल टेस्ट: `python -m http.server 8080` → `http://127.0.0.1:8080/?id=005`  
5. `git add media data.json && git commit -m "Add real audio for item XXX" && git push` → १–२ मिनिटांत live  

> फक्त `media/` किंवा `data.json` बदललं तर एवढंच पुरेसं. पण `styles.css` / `app.js` बदललं तर `index.html` व `sw.js` मधला `?v=N` वाढवा (नाहीतर जुनी आवृत्ती cache होते).

**नवीन आयुध जोडायचं असल्यास:** `data.json` च्या `items` मध्ये शेवटी नवीन entry (नेस्टेड `guide` ऑब्जेक्टसह — आधीची एखादी entry कॉपी करून बदला), https://jsonlint.com वर तपासा, `media/item-XXX/` फोल्डर, मग `python _generate_qr.py`.

---

## २३ आयुधे

| id | मराठी | English | id | मराठी | English |
|---|---|---|---|---|---|
| 001 | एकदंत | Ekadanta | 013 | बाण | Bana |
| 002 | पाश | Pasha | 014 | इक्षुकार्मुक | Ikshukarmuka |
| 003 | अंकुश | Ankusha | 015 | पुष्पबाण | Kusumashara |
| 004 | परशू | Parashu | 016 | वज्रशूळ | Vajra Shool |
| 005 | सुदर्शन चक्र | Chakra | 017 | वेताळ अस्त्र | Vetala |
| 006 | गदा | Gada | 018 | खेटक | Khetaka |
| 007 | खड्ग | Khadga | 019 | खंजीर | Churi |
| 008 | त्रिशूळ | Shula | 020 | पाषाणधारण | Pasanadharana |
| 009 | खट्वांग | Khatvanga | 021 | नांगर | Hala |
| 010 | मुद्गर | Mudgara | 022 | कवच | Kavacha |
| 011 | कुंत | Kunta | 023 | अग्नी | Agni |
| 012 | धनुष्य | Karmuka | | | |

सर्व URL: `qr-urls.txt`. कहाणी / अर्थ / चित्रं `data.json` व `media/item-XXX/` मध्ये.

---

## GitHub Pages वर अपलोड (हे एकदाच — आधीच झालेलं, फक्त संदर्भासाठी)

1. GitHub वर public repo तयार करा: `Ganpati_ai_museum`  
2. PowerShell:

```powershell
cd e:\Ganpati_audio_qr_project
git init
git add .
git commit -m "Initial Ganpati home museum site"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Ganpati_ai_museum.git
git push -u origin main
```

3. Repo → **Settings → Pages** → Branch: `main`, folder: `/ (root)` → Save  
4. URL: `https://YOUR_USERNAME.github.io/Ganpati_ai_museum/`

---

## QR + NFC

- प्रत्येक वस्तूसाठी QR आणि NFC वर **एकच URL**  
- NFC **धातू** फ्रेम/शेल्फ मागे काम करत नाही — लाकूड/कार्डबोर्ड/पेपर वापरा  
- जुने iPhone: NFC कठीण → QR बॅकअप आवश्यक  

QR कोड्स `python _generate_qr.py` ने स्थानिक तयार होतात (`qr-codes/` मध्ये, फक्त प्रिंटसाठी — `.gitignore` मध्ये). रंग `#7a1e2b` (मरून), **square modules + error correction Q (~२५%)**, मध्यभागी logo **नाही** (आयकॉन कार्डवर वेगळा सील). सर्व २४ कोड rotation/blur/JPEG/लांबून सर्व परिस्थितींत scan होतात हे verified. बदल हवा असल्यास `_generate_qr.py`.

**३ प्रिंट फॉरमॅट:** `_print_sheet.py` → 6 पानं, पूर्ण सजावटी कार्ड (QR ~५.८ सेमी) · `_print_sheet_compact.py` → 2 पानं, साधा B/W (५.४ सेमी) · `_print_sheet_patrika_compact.py` → 2 पानं, पत्रिका कार्ड (~३.८ सेमी). सर्व PDF `qr-codes/` मध्ये. **१००% scale वर प्रिंट करा.**

---

## तांत्रिक टिपा (डेव्हलपर)

- फ्रेमवर्क नाही — फक्त `index.html`, `styles.css`, `app.js`, `data.json`  
- ऑफलाइन: Service Worker (`sw.js`) + `manifest.json`  
- भाषा निवड `localStorage` मध्ये जतन (English टॉगल सध्या UI मधून लपवलेला)  
- ३० सेकंदात पुन्हा स्कॅन → ऑडिओ आपोआप रीस्टार्ट होत नाही  

स्पेक: `home-audio-guide-build-spec.md`
