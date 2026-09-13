# 🛡️ [PROJECT_NAME] — मालकी संरक्षण चेकलिस्ट

(सविस्तर मार्गदर्शन: `docs/IP_PROTECTION_MARATHI.md`)

> ही फाईल `git ownership-init` (किंवा equivalent bootstrap) द्वारे
> आपोआप या प्रोजेक्टमध्ये आली आहे. `[PROJECT_NAME]`, `[OWNER_EMAIL]`
> वगैरे placeholders भरा आणि खालील पायऱ्या पूर्ण करा.

## 🔴 सर्वप्रथम — नाव भरा

- [ ] **मालकाचे पूर्ण कायदेशीर नाव ठरवा** (Aadhaar/PAN वरील, किंवा कंपनीचे)
- [ ] LICENSE, NOTICE, OWNERSHIP.md मधील placeholders भरा
- [ ] `git config user.name "खरे नाव"` (या प्रोजेक्टपुरतं, गरज असल्यास)

## 📅 पहिल्या आठवड्यात (मोफत)

- [ ] Repository **PRIVATE** असल्याची खात्री करा (गृहीत धरू नका — प्रत्यक्ष
      तपासा: `gh repo view <owner>/<repo> --json isPrivate`)
- [ ] Global commit signing आधीच सेट आहे का तपासा:
      `git config --global --get commit.gpgsign`
      (जर आधीच्या प्रोजेक्टमध्ये सेट केलं असेल तर हा प्रोजेक्ट आपोआप
      त्याचा फायदा घेतो — पुन्हा करायची गरज नाही)
- [ ] Public signing key GitHub वर upload झाली आहे का तपासा (नसेल तर
      Settings → SSH and GPG keys → New SSH key → "Signing Key")
- [ ] Git bundle backup घ्या आणि दुसऱ्या ठिकाणी ठेवा:
  ```bash
  git bundle create ../backup-$(date +%Y%m%d).bundle --all
  ```
- [ ] मोठ्या milestone ला OpenTimestamps stamp करा — https://opentimestamps.org
      (फक्त bundle चा SHA-256 hash असलेली छोटी टेक्स्ट फाईल अपलोड करा,
      संपूर्ण bundle नाही — जास्त सुरक्षित)

## 🏛️ पहिल्या महिन्यात (सशुल्क, गरजेनुसार)

- [ ] IP वकिलाचा सल्ला (Copyright/Trademark साठी)
- [ ] Copyright नोंदणी — copyright.gov.in, Form XIV
- [ ] Trademark search + अर्ज (नाव/ब्रँड ठरलं असल्यास) — ipindia.gov.in

## ⚠️ कधीही करू नका

- ❌ नाव/आकडे अंदाजाने भरू नका — रिकामी जागा ठेवा, विचारा, मगच भरा
- ❌ जुना git इतिहास rewrite करू नका — `.mailmap` वापरा
- ❌ कायदेशीर आकडे (दंड, फी) न तपासता लिहू नका

---
*Template आवृत्ती — `~/.project-templates/ownership/` मधून कॉपी. मूळ स्रोत:
CareerBrain AI प्रोजेक्टमधील अनुभव. कायदेशीर सल्ला नाही.*
