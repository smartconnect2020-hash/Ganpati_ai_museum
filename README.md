# घर संग्रहालय — कुटुंबासाठी मार्गदर्शक (Nil)

Repo: **Ganpati_ai_museum**  
कुटुंब: **Nil**

ही वेबसाइट QR किंवा NFC स्कॅन केल्यावर घरातल्या वस्तूची ऑडिओ कहाणी + फोटो दाखवते.

---

## पाहुण्यांसाठी कसे चालते?

1. वस्तूजवळचा **QR स्कॅन** करा किंवा **NFC** टॅगला फोन लावा  
2. वेबपेज उघडेल → मोठे **ऐका / Play** बटण दाबा  
3. वर उजवीकडे **मराठी | English** बदलता येते  

URL उदाहरणे:
- यादी: `https://YOUR_USERNAME.github.io/Ganpati_ai_museum/`
- वस्तू: `https://YOUR_USERNAME.github.io/Ganpati_ai_museum/?id=001`

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

## नवीन वस्तू जोडणे (३ मिनिटांचा फ्लो)

1. फोनवर **३०–६० सेकंद** ऑडिओ रेकॉर्ड करा (मराठी + इंग्रजी वेगळे)  
2. वस्तूचे **३ फोटो** घ्या  
3. संगणकावर `media/` मध्ये नवीन फोल्डर: `item-011/`  
4. फाइल्स या नावांनी ठेवा:
   - `audio-mr.mp3`
   - `audio-en.mp3`
   - `01.webp` (किंवा आताच्या प्लेसहोल्डरसाठी `01.png`), `02`, `03` — नंतर खरे WebP फोटो ठेवा  
5. `data.json` Notepad मध्ये उघडा → शेवटच्या item नंतर copy-paste करून नवीन entry भरा (`id`: `"011"`)  
6. JSON चुकीचा तर साइट बंद पडते — तपासा: https://jsonlint.com  
7. GitHub Desktop → **Commit** + **Push**  
8. २ मिनिटांनी live  
9. [qrcode-monkey.com](https://www.qrcode-monkey.com) वर QR: `...?id=011`  
10. NFC Tools अॅपमध्ये **तोच URL** टॅगवर लिहा  

---

## सध्याच्या १० वस्तू

| id | मराठी | English |
|---|---|---|
| 001 | गणपतीची आयुधे | Ganpati Aayudha |
| 002 | परशु | Parshu |
| 003 | अंकुश | Ankush |
| 004–010 | प्लेसहोल्डर | Placeholder — नंतर भरा |

खरी कहाणी / ऑडिओ / फोटो `data.json` आणि `media/item-XXX/` मध्ये बदला.

---

## GitHub Pages वर अपलोड

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

QR रंग सुचवणी: dark brown `#3E2723`, error correction **High (H)**

---

## तांत्रिक टिपा (डेव्हलपर)

- फ्रेमवर्क नाही — फक्त `index.html`, `styles.css`, `app.js`, `data.json`  
- ऑफलाइन: Service Worker (`sw.js`) + `manifest.json`  
- भाषा निवड `localStorage` मध्ये जतन  
- ३० सेकंदात पुन्हा स्कॅन → ऑडिओ आपोआप रीस्टार्ट होत नाही  

स्पेक: `home-audio-guide-build-spec.md`
