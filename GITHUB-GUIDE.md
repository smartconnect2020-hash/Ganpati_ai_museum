# GitHub — सोप्या भाषेत पूर्ण माहिती

## १) “Login न करता कसे झाले?”

Login **झालेलाच होता** — तुम्हाला फक्त नवीन पासवर्ड विचारला गेला नाही.

या PC वर आधीच GitHub CLI (`gh`) **login** होते:

- अकाउंट: **`smartconnect2020-hash`**
- Token Windows **keyring** मध्ये सेव्ह आहे
- म्हणून Cursor/agent ने `gh repo create` + `git push` करू शकले

तुम्ही स्वतः तपासू शकता (PowerShell):

```powershell
gh auth status
```

जर कधी logout झाले तर:

```powershell
gh auth login
```

> `smartconnect2020-lab` नावाचा युजर GitHub वर **नव्हता** (404), म्हणून सर्व काही **`smartconnect2020-hash`** वर झाले.

---

## २) Public आहे की Private?

**PUBLIC** ✅ — कोणीही लिंकने साइट आणि कोड पाहू शकतो.

| गोष्ट | मूल्य |
|---|---|
| Visibility | **Public** |
| Repo | https://github.com/smartconnect2020-hash/Ganpati_ai_museum |
| Live site | https://smartconnect2020-hash.github.io/Ganpati_ai_museum/ |
| Branch | `main` |
| Pages | `main` branch, folder `/ (root)` |

Private करायचे असल्यास GitHub → Repo → **Settings → General → Danger Zone → Change repository visibility**.  
(Private repo वर Pages साठी GitHub Pro/Org प्लॅन लागू शकते — आता Public ठेवणे घर संग्रहालयासाठी ठीक आहे.)

---

## ३) GitHub कसे अपडेट करायचे?

फाइल्स लोकल फोल्डरत बदला → GitHub ला **push** करा → १–२ मिनिटांत live साइट अपडेट होते.

लोकल फोल्डर: `e:\Ganpati_audio_qr_project`

### पद्धत A — GitHub Desktop (सोपी, कुटुंबासाठी)

1. [GitHub Desktop](https://desktop.github.com) इंस्टॉल + `smartconnect2020-hash` ने login  
2. **File → Add local repository** → हा फोल्डर निवडा  
3. ऑडिओ/फोटो/`data.json` बदला  
4. खाली Summary लिहा → **Commit to main**  
5. **Push origin**  
6. १–२ मिनिट थांबा → live URL रिफ्रेश करा  

### पद्धत B — PowerShell (git)

```powershell
cd e:\Ganpati_audio_qr_project

# काय बदलले ते पाहा
git status

# फाइल्स add करा
git add media data.json

# commit
git commit -m "Update audio and photos"

# GitHub वर पाठवा
git push
```

### पद्धत C — GitHub वेबसाइटवरून (छोटे मजकूर बदल)

1. https://github.com/smartconnect2020-hash/Ganpati_ai_museum उघडा  
2. `data.json` क्लिक → पेन्सिल (Edit)  
3. कहाणी/नाव बदला → **Commit changes**  
4. मोठे ऑडिओ/फोटो वेब Edit ने कठीण — Desktop/git वापरा  

---

## ४) काय बदलायचे = कुठे?

| तुम्ही काय करता | कुठे |
|---|---|
| आवाज | `media/item-00X/audio-mr.mp3` (जुनी फाइल overwrite) |
| इंग्रजी आवाज | `media/item-00X/audio-en.mp3` |
| फोटो | `media/item-00X/01.png` … `03.png` (किंवा webp + `data.json` पाथ) |
| कहाणी / वर्ष / स्थळ | `data.json` |
| नवीन वस्तू | नवीन `media/item-011/` + `data.json` एंट्री |

मग: **Commit + Push** → live अपडेट.

---

## ५) Live URL चेक्कलिस्ट

होम:  
https://smartconnect2020-hash.github.io/Ganpati_ai_museum/

वस्तू उदाहरणे:  
- https://smartconnect2020-hash.github.io/Ganpati_ai_museum/?id=001  
- https://smartconnect2020-hash.github.io/Ganpati_ai_museum/?id=002  
- https://smartconnect2020-hash.github.io/Ganpati_ai_museum/?id=003  

पूर्ण यादी: `qr-urls.txt` फाइलमध्ये आहे (QR/NFC साठी copy-paste).

---

## ६) पुश नंतरही जुने दिसत असेल तर

1. २ मिनिट थांबा (Pages बिल्ड)  
2. फोनवर hard refresh / Incognito  
3. Service Worker कॅश: साइट Settings → Clear data, किंवा एकदा airplane mode ऑफ करून पुन्हा उघडा  
4. GitHub → repo → **Actions / Pages** मध्ये Deployments पाहा  

---

## ७) सुरक्षा / कोण पाहू शकतो?

- Public = लिंक असलेला कोणीही मजकूर + ऑडिओ ऐकू शकतो  
- Password/login साइटवर **नाही** (स्पेकनुसार guest-friendly)  
- खाजगी कहाणी नको असल्यास Private विचारा किंवा फक्त घरच्या WiFi QR वापरा  

Repo मध्ये `.env` / पासवर्ड टाकू नका.
