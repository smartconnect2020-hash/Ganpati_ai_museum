/**
 * Home Museum — app.js
 * URL routing, data load, audio, gallery, language, PWA helpers.
 * No external dependencies.
 */

(function () {
  'use strict';

  const STORAGE_LANG = 'lang';
  const REVISIT_MS = 30000;

  const UI = {
    mr: {
      loading: 'लोड होत आहे…',
      errorTitle: 'ही वस्तू सापडली नाही',
      errorBody: 'QR किंवा लिंक चुकीची असू शकते. मुख्य यादीकडे परत जा.',
      homeCta: 'सर्व वस्तू पहा',
      play: 'ऐका',
      pause: 'थांबवा',
      replay: 'पुन्हा ऐका',
      story: 'कहाणी',
      visited: 'पाहिले',
      revisit: 'तुम्ही ही वस्तू आताच पाहिली',
      eyebrow: 'श्री गणेशाच्या प्रत्येक आयुधामागील रंजक कथा',
      homeLead: 'QR किंवा NFC स्कॅन करून प्रत्येक वस्तूची कहाणी ऐका.',
      location: 'स्थळ',
      year: 'वर्ष',
      footer: (name) => `${name} · श्री गणेश आयुधे`,
      itemNo: (n) => `वस्तू क्र. ${n}`,
      wheelVisited: (n, total) => `${displayNum(n)} / ${displayNum(total)} पाहिले`,
      wheelNote: 'टीप: आतली व बाहेरची रिंग फक्त जागेसाठी आहे — क्रमांकच खरा क्रम दाखवतो, कुठलंही महत्त्व नाही.',
      wheelStop: '⏸ परिक्रमा थांबवा',
      wheelResume: '▶ परिक्रमा सुरू करा',
      wheelCenterLabel: 'यादृच्छिक आयुध सुचवा',
      wheelToday: 'आजचं आयुध —',
      wheelListen: 'ऐका →',
      galleryRefNote: 'टीप: ही चित्रे कल्पनाचित्रण/संदर्भासाठी आहेत — तंतोतंत प्रतिकृती नाहीत.',
    },
    en: {
      loading: 'Loading…',
      errorTitle: 'Item not found',
      errorBody: 'The QR or link may be wrong. Go back to the list.',
      homeCta: 'See all items',
      play: 'Play',
      pause: 'Pause',
      replay: 'Play again',
      story: 'Story',
      visited: 'Visited',
      revisit: 'You just viewed this item',
      eyebrow: 'The fascinating story behind each of Shri Ganesh’s weapons',
      homeLead: 'Scan QR or NFC to hear each object’s story.',
      location: 'Location',
      year: 'Year',
      footer: (name) => `${name} · Shri Ganesh's Weapons`,
      itemNo: (n) => `ITEM NO. ${n}`,
      wheelVisited: (n, total) => `${displayNum(n)} / ${displayNum(total)} visited`,
      wheelNote: 'Note: the inner and outer rings are only for spacing — the number is the real order, not importance.',
      wheelStop: '⏸ Pause the parikrama',
      wheelResume: '▶ Begin the parikrama',
      wheelCenterLabel: 'Suggest a random item',
      wheelToday: "Today's item —",
      wheelListen: 'Listen →',
      galleryRefNote: 'Note: these images are illustrative/reference — not an exact replica.',
    },
  };

  const DEVANAGARI_DIGITS = ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९'];

  /* design-ref*.jpg/jpeg files are AI-generated multi-view spec sheets
     (front/side/detail panels + printed English labels/rulers baked into
     the pixels) — not plain photos. Cropping them with object-fit:cover
     would randomly cut into that text, so they get a dedicated "show the
     whole sheet" treatment (see .is-ref in styles.css) instead of the
     normal cover-crop.
     Deliberately name-based, not content-inspected: two newer images this
     session (a labelled multi-panel shield-turnaround vs. a clean single
     shield render) both had "turnaround" in their original filenames but
     needed OPPOSITE treatment — so matching on "turnaro" caught the wrong
     one too. Fixed by renaming only the genuinely multi-panel file to
     start with "design-ref" (see media/item-011/) instead of guessing from
     an arbitrary substring; a plain single-subject photo just keeps its
     own descriptive filename and gets normal cover-crop. */
  function isDesignRef(src) {
    return typeof src === 'string' && src.includes('design-ref');
  }

  function displayNum(idStr) {
    const n = String(Number(idStr));
    if (lang !== 'mr') return n;
    return n.replace(/[0-9]/g, (d) => DEVANAGARI_DIGITS[Number(d)]);
  }

  const ICON = {
    play: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>',
    pause: '<svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>',
    replay: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/></svg>',
    skip: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M11 17V7l-7 5z"/><path d="M20 17V7l-7 5z"/></svg>',
    location: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-6.1 7-11a7 7 0 1 0-14 0c0 4.9 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    calendar: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
    book: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
    info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v5h1"/></svg>',
    back: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>',
    error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/></svg>',
    scroll: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h11a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6"/><path d="M6 3a2 2 0 0 0-2 2v1h2M6 21a2 2 0 0 1-2-2v-1h2"/><path d="M9 8h7M9 12h7M9 16h4"/></svg>',
  };

  let data = null;
  // Language toggle is hidden until English guide text exists (see styles.css
  // .lang-toggle) — forcing 'mr' here means a stale "en" in localStorage from
  // before this change can never strand a visitor on the toggle-less English view.
  let lang = 'mr';
  let audioEl = null;
  let wakeLock = null;
  let currentItem = null;

  const app = document.getElementById('app');
  const brandTitle = document.getElementById('brand-title');
  const brandFamily = document.getElementById('brand-family');
  const footerText = document.getElementById('footer-text');
  const langToggle = document.getElementById('lang-toggle');
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const lightboxClose = document.getElementById('lightbox-close');
  const lightboxPrev = document.getElementById('lightbox-prev');
  const lightboxNext = document.getElementById('lightbox-next');
  const lightboxCounter = document.getElementById('lightbox-counter');
  let lightboxImages = [];
  let lightboxIndex = 0;
  let lightboxAlt = '';

  function t() {
    return UI[lang] || UI.mr;
  }

  function getQueryId() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');
    return id ? String(id).padStart(3, '0') : null;
  }

  function findItem(id) {
    if (!data || !data.items) return null;
    return data.items.find((item) => item.id === id) || null;
  }

  function updateLangToggle() {
    langToggle.querySelectorAll('[data-lang-label]').forEach((el) => {
      el.classList.toggle('active', el.getAttribute('data-lang-label') === lang);
    });
  }

  function applyChrome() {
    const meta = data && data.meta;
    const title = meta ? meta.site_title[lang] : t().loading;
    const family = (meta && meta.family_name) || 'Nilesh';
    const developedBy = `Developed by ${family}`;
    brandTitle.textContent = title;
    brandFamily.textContent = developedBy;
    footerText.textContent = t().footer(developedBy);
    document.title = title;
    document.documentElement.lang = lang === 'mr' ? 'mr' : 'en';
    updateLangToggle();
  }

  async function loadData() {
    const res = await fetch('data.json', { cache: 'no-cache' });
    if (!res.ok) throw new Error('Failed to load data.json');
    data = await res.json();
  }

  function formatTime(sec) {
    if (!Number.isFinite(sec) || sec < 0) return '0:00';
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${String(s).padStart(2, '0')}`;
  }

  async function requestWakeLock() {
    try {
      if ('wakeLock' in navigator) {
        wakeLock = await navigator.wakeLock.request('screen');
      }
    } catch (_) {
      /* unsupported or denied — silent */
    }
  }

  async function releaseWakeLock() {
    try {
      await wakeLock?.release();
    } catch (_) {
      /* ignore */
    }
    wakeLock = null;
  }

  function setupMediaSession(item) {
    if (!('mediaSession' in navigator)) return;
    const art = item.images && item.images[0]
      ? [{ src: item.images[0], sizes: '512x512', type: 'image/png' }]
      : [];
    navigator.mediaSession.metadata = new MediaMetadata({
      title: item.title[lang],
      artist: data.meta.family_name,
      artwork: art,
    });
    navigator.mediaSession.setActionHandler('play', () => audioEl?.play());
    navigator.mediaSession.setActionHandler('pause', () => audioEl?.pause());
  }

  function markVisited(id) {
    localStorage.setItem(`visited_${id}`, '1');
    localStorage.setItem(`last_visit_${id}`, String(Date.now()));
  }

  function wasRecentVisit(id) {
    const last = Number(localStorage.getItem(`last_visit_${id}`) || 0);
    return last && Date.now() - last < REVISIT_MS;
  }

  function isVisited(id) {
    return localStorage.getItem(`visited_${id}`) === '1';
  }

  function showLightboxImage() {
    lightboxImg.src = lightboxImages[lightboxIndex];
    lightboxImg.alt = lightboxAlt;
    const multi = lightboxImages.length > 1;
    lightboxPrev.hidden = !multi;
    lightboxNext.hidden = !multi;
    lightboxCounter.hidden = !multi;
    if (multi) lightboxCounter.textContent = `${lightboxIndex + 1} / ${lightboxImages.length}`;
  }

  function openLightbox(images, index, alt) {
    lightboxImages = images;
    lightboxIndex = index || 0;
    lightboxAlt = alt || '';
    showLightboxImage();
    lightbox.hidden = false;
  }

  function lightboxStep(delta) {
    if (!lightboxImages.length) return;
    lightboxIndex = (lightboxIndex + delta + lightboxImages.length) % lightboxImages.length;
    showLightboxImage();
  }

  function closeLightbox() {
    lightbox.hidden = true;
    lightboxImg.removeAttribute('src');
  }

  function renderError() {
    const u = t();
    app.innerHTML = `
      <div class="error-box">
        ${ICON.error.replace('<svg ', '<svg class="state-icon" style="color:var(--color-error)" ')}
        <h1>${u.errorTitle}</h1>
        <p>${u.errorBody}</p>
        <a class="back-home" href="?">${ICON.back}${u.homeCta}</a>
      </div>
    `;
  }

  /* Whole-shrine decoration video: one clip for the entire "आरास" (all 23
     weapons arranged together), shown only on the home/list page — this is
     not per-item media, so it lives in data.meta, not on any single item.

     Delivery note: GitHub Pages is static file hosting — there is no server
     to pick a rendition, so "adaptive" here means picking one of two
     pre-encoded files (HD/SD) with JS before the browser ever requests
     bytes, based on viewport width + connection info. Real ABR (HLS/DASH)
     needs segmented streams a static host can't produce; this is the
     practical equivalent for a two-rendition personal site. */
  function renderDecorationVideo() {
    const dv = data.meta.decoration_video;
    if (!dv) return '';
    const title = dv.title ? dv.title[lang] || dv.title.mr : '';
    const caption = dv.caption ? dv.caption[lang] || dv.caption.mr : '';
    const copyright =
      dv.copyright && dv.copyright[lang]
        ? dv.copyright[lang]
        : lang === 'mr'
        ? `Developed by ${data.meta.family_name || ''} — केवळ वैयक्तिक अवलोकनासाठी. डाउनलोड/पुनर्प्रकाशन करू नये.`
        : `Developed by ${data.meta.family_name || ''} — for personal viewing only. Do not download or republish.`;
    const srcHd = (dv.sources && dv.sources.hd) || dv.src || '';
    const srcSd = (dv.sources && dv.sources.sd) || '';
    const yt = dv.youtube_teaser;
    const ytUrl = yt && yt.url ? yt.url : '';
    const ytLabel = yt && yt.label ? yt.label[lang] || yt.label.mr : '';
    return `
      <section class="decoration-section" aria-label="${escapeHtml(title)}">
        <h2 class="decoration-title">${escapeHtml(title)}</h2>
        <video
          class="decoration-video"
          id="decoration-video"
          controls
          controlsList="nodownload noremoteplayback"
          disablePictureInPicture
          preload="metadata"
          playsinline
          data-src-hd="${srcHd}"
          data-src-sd="${srcSd}"
          data-yt-url="${escapeHtml(ytUrl)}"
          data-yt-label="${escapeHtml(ytLabel)}"
          ${dv.poster ? `poster="${dv.poster}"` : ''}
        ></video>
        ${caption ? `<p class="decoration-caption">${escapeHtml(caption)}</p>` : ''}
        <p class="decoration-copyright">${escapeHtml(copyright)}</p>
      </section>
    `;
  }

  function bindDecorationVideo() {
    const video = document.getElementById('decoration-video');
    if (!video) return;

    /* Pick HD vs SD once at load: small/slow connections and small screens
       get the lighter file. Not live-updated on resize/connection change —
       not worth the complexity for a one-clip personal page. */
    const conn = navigator.connection || navigator.webkitConnection;
    const wantsLight =
      window.innerWidth < 480 ||
      (conn && (conn.saveData || /^(slow-2g|2g|3g)$/.test(conn.effectiveType || '')));
    const sd = video.dataset.srcSd;
    const hd = video.dataset.srcHd;
    video.src = wantsLight && sd ? sd : hd || sd;

    video.addEventListener('error', () => {
      const section = video.closest('.decoration-section');
      if (!section || section.querySelector('.decoration-error, .decoration-youtube-embed')) return;

      /* No local file yet (aaras.mp4 missing) — if a YouTube teaser is
         configured, embed it inline instead of the old bare "coming soon"
         text, so visitors get something actually playable. Once the real
         local file is added, this whole branch stops firing (the <video>
         loads fine) and the plain text fallback below is what's left for
         the case where neither a local file nor a teaser exists. */
      const ytUrl = video.dataset.ytUrl;
      const ytLabel = video.dataset.ytLabel;
      if (ytUrl) {
        const videoId = (
          ytUrl.match(/shorts\/([\w-]+)/) ||
          ytUrl.match(/embed\/([\w-]+)/) ||
          ytUrl.match(/[?&]v=([\w-]+)/) ||
          []
        )[1];
        const wrap = document.createElement('div');
        wrap.className = 'decoration-youtube-embed';
        if (videoId) {
          const iframe = document.createElement('iframe');
          iframe.src = `https://www.youtube.com/embed/${videoId}`;
          iframe.title = section.getAttribute('aria-label') || 'YouTube video';
          iframe.loading = 'lazy';
          iframe.allow =
            'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
          iframe.allowFullscreen = true;
          wrap.appendChild(iframe);
        }
        video.replaceWith(wrap);
        if (ytLabel) {
          const link = document.createElement('a');
          link.className = 'decoration-youtube-link';
          link.href = ytUrl;
          link.target = '_blank';
          link.rel = 'noopener';
          link.innerHTML = `${ICON.play}<span>${escapeHtml(ytLabel)}</span>`;
          wrap.insertAdjacentElement('afterend', link);
        }
        return;
      }

      const note = document.createElement('p');
      note.className = 'decoration-error';
      note.textContent =
        lang === 'mr'
          ? 'सजावटीचा व्हिडिओ लवकरच जोडला जाईल.'
          : 'Decoration video coming soon.';
      video.replaceWith(note);
    });

    /* Casual download deterrents only — NOT real protection. The browser
       must still fetch the raw file to play it, so anyone checking dev
       tools / view-source can find the direct URL. controlsList="nodownload"
       is Chromium-only and only hides the button; it does not block the
       request. True DRM would need EME + a license server, which a static
       GitHub Pages site cannot host. This just stops the one-click "Save
       video as" from the right-click menu for casual visitors. */
    video.addEventListener('contextmenu', (e) => e.preventDefault());
    video.setAttribute('draggable', 'false');
  }

  /* आयुध-चक्र — दोन एककेंद्री रिंगमध्ये (बाहेरची अर्धी + आतली अर्धी आयुधे)
     विभागलेलं, दोन्ही रिंग एकाच --wheel-rotation वर एकत्र फिरतात (bindWheel
     मधला एकच ड्रॅग-इंजिन). दोन रिंगमुळे प्रत्येक आयुधाभोवती आधीच्या एका-रिंग
     आवृत्तीपेक्षा (20 नोड्स) जास्त जागा मिळते — म्हणून नाव आता hover शिवायही
     कायम दिसू शकतं. Positions इथेच काढल्या (bind-time DOM पासऐवजी) कारण त्या
     फक्त इंडेक्स/एकूण संख्येवर अवलंबून असतात — प्रत्यक्ष आकार/breakpoints
     styles.css मध्ये आहेत. */
  function renderHome() {
    const u = t();
    const meta = data.meta;
    const eyebrow = u.eyebrow;
    const total = data.items.length;
    const splitAt = Math.ceil(total / 2);
    const outerItems = data.items.slice(0, splitAt);
    const innerItems = data.items.slice(splitAt);
    const cx = 50;
    const cy = 50;

    function nodePos(i, ringTotal, R) {
      const angle = (i / ringTotal) * 2 * Math.PI - Math.PI / 2;
      return { x: cx + R * Math.cos(angle), y: cy + R * Math.sin(angle) };
    }

    function buildRing(list, R, startIndex, isInner) {
      let spokes = '';
      let nodes = '';
      list.forEach((item, i) => {
        const { x, y } = nodePos(i, list.length, R);
        spokes += `<line x1="${cx}%" y1="${cy}%" x2="${x}%" y2="${y}%" />`;
        const globalIndex = startIndex + i;
        const thumb = item.images[0] || '';
        const visited = isVisited(item.id)
          ? `<span class="wheel-node-visited" role="img" aria-label="${escapeHtml(u.visited)}">${ICON.check}</span>`
          : '';
        nodes += `
          <a class="wheel-node${isInner ? ' is-inner' : ''}" href="?id=${item.id}" style="left:${x}%; top:${y}%; --i:${globalIndex}">
            <span class="wheel-node-inner">
              <span class="wheel-node-media">
                <img class="wheel-node-img${isDesignRef(thumb) ? ' is-ref' : ''}" src="${thumb}" alt="" loading="lazy" width="120" height="120" />
                <span class="wheel-node-badge">${displayNum(globalIndex + 1)}</span>
                ${visited}
              </span>
              <span class="wheel-node-label">${item.title[lang]}</span>
            </span>
          </a>
        `;
      });
      return { spokes, nodes };
    }

    const outerRing = buildRing(outerItems, 42, 0, false);
    const innerRing = buildRing(innerItems, 23, splitAt, true);
    const visitedCount = data.items.filter((item) => isVisited(item.id)).length;

    /* The wheel above is a visual index (numbered + now-labelled) — this
       legend is still the guaranteed-untruncated, always-readable list, and
       the only way keyboard/screen-reader users reach every item in a
       normal, linear order (the wheel's DOM order matches this list's
       order, so tab order is identical either way). */
    const legend = data.items
      .map((item, i) => {
        const thumb = item.images[0] || '';
        const visited = isVisited(item.id)
          ? `<span class="wheel-legend-visited" role="img" aria-label="${escapeHtml(u.visited)}">${ICON.check}</span>`
          : '';
        return `
          <li>
            <a href="?id=${item.id}">
              <span class="wheel-legend-thumb">
                <img class="wheel-legend-img${isDesignRef(thumb) ? ' is-ref' : ''}" src="${thumb}" alt="" loading="lazy" width="72" height="72" />
                <span class="wheel-legend-num">${displayNum(i + 1)}</span>
              </span>
              <span class="wheel-legend-title">${item.title[lang]}</span>
              ${visited}
            </a>
          </li>
        `;
      })
      .join('');

    /* Hero order: the wheel is this page's signature, most-characteristic
       visual — it used to render BELOW the decoration video, so a visitor's
       first impression was a secondary overview clip, not the interactive
       चक्र itself (flagged in an earlier design audit, never acted on until
       now). Decoration video moves to the very end instead — a nice-to-have
       "see the whole shrine" bonus after the primary hero + full item list,
       not competing with them for first-scroll attention. */
    app.innerHTML = `
      <section class="home-hero">
        <span class="home-eyebrow">${eyebrow}</span>
        <h1>${meta.site_title[lang]}</h1>
        <p>${u.homeLead}</p>
      </section>
      <p class="wheel-status" id="wheel-status">${u.wheelVisited(visitedCount, total)}</p>
      <div class="wheel-wrap">
        <div class="wheel-ring">
          <svg class="wheel-spokes" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">${outerRing.spokes}</svg>
          ${outerRing.nodes}
        </div>
        <div class="wheel-ring">
          <svg class="wheel-spokes" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">${innerRing.spokes}</svg>
          ${innerRing.nodes}
        </div>
        <span class="wheel-center-ring">
          <button type="button" class="wheel-center" id="wheel-center-btn" aria-label="${escapeHtml(u.wheelCenterLabel)}">
            <img class="wheel-center-img" src="icons/logo-mark-simple-light.png?v=3" alt="" />
          </button>
        </span>
      </div>
      <div class="wheel-reveal" id="wheel-reveal"></div>
      <p class="wheel-note">${u.wheelNote}</p>
      <div class="wheel-toggle-row">
        <button type="button" class="wheel-toggle" id="wheel-toggle-btn"></button>
      </div>
      <ul class="wheel-legend">${legend}</ul>
      ${renderDecorationVideo()}
    `;
    bindDecorationVideo();
    bindWheel();
  }

  /* चक्र rotation — a slow ambient auto-spin, ON by default (paused only
     under prefers-reduced-motion, on hover/drag, or an explicit stop) plus
     manual drag-to-turn. One --wheel-rotation custom property on .wheel-wrap
     drives BOTH .wheel-ring layers' rotation and every node's equal-and-
     opposite counter-rotation (see .wheel-ring / .wheel-node-inner in
     styles.css) — a single shared value means one consistent drag anywhere
     on the wheel, not two rings behaving differently depending on where you
     grab (that was tried and confirmed confusing in testing, see
     design-demos/concept-h-mandala.html). No JS/no motion still renders
     correctly: the CSS rule falls back to 0deg via var(--wheel-rotation,0deg).
     Also binds the active center button and the explicit stop/resume toggle
     — grouped here since all three act on the same .wheel-wrap instance. */
  function bindWheel() {
    const wrap = document.querySelector('.wheel-wrap');
    if (!wrap) return;
    // Hidden below phone width (see the .wheel-wrap { display:none } media
    // query in styles.css) — nothing to animate or drag there, so skip the
    // rAF loop and pointer listeners entirely rather than spend battery on
    // an invisible element.
    if (getComputedStyle(wrap).display === 'none') return;

    const u = t();
    const AUTO_PERIOD_MS = 150000; // one full turn every 150s — ambient, not distracting
    const RESUME_DELAY_MS = 2500;
    // A real mouse click almost always carries a few px of natural jitter
    // between press and release — 6px was tight enough that ordinary clicks
    // on a node were getting misread as a drag and swallowed, silently
    // breaking navigation. 12px gives clicks realistic headroom while still
    // being far below the movement a deliberate wheel-spin drag produces.
    const DRAG_THRESHOLD_PX = 12;
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    let rotation = 0;
    let autoBase = 0;
    let autoStart = null;
    // Rotation is ON by default for everyone except a reduced-motion OS
    // setting (never auto-started there) — but the toggle button below stays
    // available either way, so a reduced-motion visitor can still choose to
    // turn it on rather than the site deciding for them.
    let paused = reduceMotion;
    let stoppedByUser = false;
    let resumeTimer = null;
    let dragging = false;
    let dragMoved = false;
    let startX = 0, startY = 0, startAngle = 0, rotationAtStart = 0;

    function setRotation(deg) {
      rotation = deg;
      wrap.style.setProperty('--wheel-rotation', deg + 'deg');
    }

    const toggleBtn = document.getElementById('wheel-toggle-btn');
    function renderToggle() {
      if (!toggleBtn) return;
      const isRunning = !paused || dragging;
      toggleBtn.textContent = isRunning ? u.wheelStop : u.wheelResume;
      toggleBtn.setAttribute('aria-pressed', String(!isRunning));
    }

    function tick(ts) {
      if (!wrap.isConnected) return; // home re-rendered (e.g. language toggle) — stop this loop
      if (!paused && !dragging) {
        if (autoStart === null) autoStart = ts;
        setRotation(autoBase + ((ts - autoStart) / AUTO_PERIOD_MS) * 360);
      }
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);

    function pause() {
      paused = true;
      if (resumeTimer) { clearTimeout(resumeTimer); resumeTimer = null; }
      renderToggle();
    }
    function scheduleResume() {
      // An explicit stop from the toggle button must stick — hovering away
      // or ending a drag should never silently override what the user asked
      // for. Only the toggle button itself clears stoppedByUser.
      if (reduceMotion || dragging || stoppedByUser) return;
      if (resumeTimer) clearTimeout(resumeTimer);
      resumeTimer = setTimeout(() => {
        autoBase = rotation;
        autoStart = null;
        paused = false;
        renderToggle();
      }, RESUME_DELAY_MS);
    }

    wrap.addEventListener('pointerenter', pause);
    wrap.addEventListener('pointerleave', () => { if (!dragging) scheduleResume(); });
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) pause(); else scheduleResume();
    });

    function angleAt(x, y) {
      const r = wrap.getBoundingClientRect();
      return Math.atan2(y - (r.top + r.height / 2), x - (r.left + r.width / 2)) * (180 / Math.PI);
    }

    let activePointerId = null;

    wrap.addEventListener('pointerdown', (e) => {
      if (e.target.closest('.wheel-center')) return; // center tap, not a drag
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      dragging = true;
      dragMoved = false;
      activePointerId = e.pointerId;
      pause();
      startX = e.clientX;
      startY = e.clientY;
      startAngle = angleAt(e.clientX, e.clientY);
      rotationAtStart = rotation;
      // No setPointerCapture here on purpose: capturing on every press (even
      // a plain click that never moves) makes the browser retarget the
      // resulting click event's target to .wheel-wrap instead of the <a>
      // that was actually pressed — so the link's own navigation silently
      // never fires. Capture is taken lazily below, only once real drag
      // movement is confirmed, so an ordinary click is never touched by it.
    });

    wrap.addEventListener('pointermove', (e) => {
      if (!dragging) return;
      if (!dragMoved && Math.hypot(e.clientX - startX, e.clientY - startY) > DRAG_THRESHOLD_PX) {
        dragMoved = true;
        wrap.setPointerCapture(activePointerId);
      }
      if (dragMoved) {
        setRotation(rotationAtStart + (angleAt(e.clientX, e.clientY) - startAngle));
      }
    });

    function endDrag(e) {
      if (!dragging) return;
      dragging = false;
      try { wrap.releasePointerCapture(e.pointerId); } catch (err) { /* already released */ }
      scheduleResume();
    }
    wrap.addEventListener('pointerup', endDrag);
    wrap.addEventListener('pointercancel', endDrag);

    // A real drag ending over a .wheel-node would otherwise fire a click and
    // navigate to that item by accident — swallow just that one click.
    wrap.addEventListener('click', (e) => {
      if (dragMoved) { e.preventDefault(); e.stopPropagation(); dragMoved = false; }
    }, true);

    /* ---- explicit stop/resume toggle ---- */
    renderToggle();
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        const isRunning = !paused || dragging;
        if (isRunning) {
          stoppedByUser = true;
          pause();
        } else {
          stoppedByUser = false;
          autoBase = rotation;
          autoStart = null;
          paused = false;
          renderToggle();
        }
      });
    }
    // endDrag() already calls scheduleResume(), which re-renders the toggle
    // on its own timer/no-op paths above — this covers the one remaining
    // gap, a drag that ends WITHOUT triggering a resume (reduced-motion or
    // an explicit stop already in effect).
    wrap.addEventListener('pointerup', renderToggle);

    /* ---- active center: यादृच्छिक आयुध सुचव ---- */
    const centerBtn = document.getElementById('wheel-center-btn');
    const revealEl = document.getElementById('wheel-reveal');
    if (centerBtn && revealEl) {
      centerBtn.addEventListener('click', () => {
        const pick = data.items[Math.floor(Math.random() * data.items.length)];
        revealEl.innerHTML = `${u.wheelToday} <b>${escapeHtml(pick.title[lang])}</b> <a href="?id=${pick.id}">${u.wheelListen}</a>`;
        revealEl.classList.add('show');
      });
    }
  }

  function bindPlayer(item) {
    const u = t();
    const playBtn = document.getElementById('play-btn');
    const playLabel = document.getElementById('play-label');
    const skipBack = document.getElementById('skip-back');
    const skipFwd = document.getElementById('skip-fwd');
    const progress = document.getElementById('progress');
    const timeCurrent = document.getElementById('time-current');
    const timeTotal = document.getElementById('time-total');

    audioEl = document.getElementById('item-audio');
    if (!audioEl || !playBtn) return;

    audioEl.src = item.audio[lang];
    setupMediaSession(item);

    const showError = (msg) => {
      let note = document.getElementById('audio-error');
      if (!note) {
        note = document.createElement('p');
        note.id = 'audio-error';
        note.className = 'audio-error';
        document.querySelector('.player').appendChild(note);
      }
      note.textContent = msg;
    };

    const setPlayingUi = (playing) => {
      const label = playing ? u.pause : playBtn.dataset.ended === '1' ? u.replay : u.play;
      playBtn.classList.toggle('is-playing', playing);
      playBtn.innerHTML = playing ? ICON.pause : playBtn.dataset.ended === '1' ? ICON.replay : ICON.play;
      playBtn.setAttribute('aria-pressed', playing ? 'true' : 'false');
      playBtn.setAttribute('aria-label', label);
      playLabel.textContent = label;
    };
    setPlayingUi(false);

    playBtn.addEventListener('click', async () => {
      try {
        if (audioEl.paused) {
          if (!audioEl.src) {
            throw new Error('missing audio');
          }
          await audioEl.play();
          await requestWakeLock();
          setPlayingUi(true);
          playBtn.dataset.ended = '0';
        } else {
          audioEl.pause();
          await releaseWakeLock();
          setPlayingUi(false);
        }
      } catch (err) {
        setPlayingUi(false);
        showError(
          lang === 'mr'
            ? 'ऑडिओ चालू झाला नाही. फाइल तपासा किंवा खरा MP3 ठेवा.'
            : 'Audio could not play. Check the file or add a real MP3.'
        );
      }
    });

    skipBack.addEventListener('click', () => {
      if (!audioEl.duration) return;
      audioEl.currentTime = Math.max(0, audioEl.currentTime - 10);
    });

    skipFwd.addEventListener('click', () => {
      if (!audioEl.duration) return;
      audioEl.currentTime = Math.min(audioEl.duration, audioEl.currentTime + 10);
    });

    audioEl.addEventListener('error', () => {
      /* Most items still carry a silent placeholder MP3 (real recording
         pending) rather than a genuinely missing file — a raw "failed to
         load, check the media folder" message is a developer-debug string,
         not something a family member scanning a QR code should see. Show
         a "not recorded yet" note instead, and disable the controls so a
         second tap doesn't also hit the play() rejection error below. */
      showError(
        lang === 'mr'
          ? 'हा आवाज अजून रेकॉर्ड झालेला नाही — लवकरच येईल.'
          : 'This audio has not been recorded yet — coming soon.'
      );
      playBtn.disabled = true;
      skipBack.disabled = true;
      skipFwd.disabled = true;
    });

    audioEl.addEventListener('timeupdate', () => {
      if (!audioEl.duration) return;
      const pct = (audioEl.currentTime / audioEl.duration) * 100;
      progress.value = String(pct);
      progress.style.setProperty('--pct', String(pct));
      timeCurrent.textContent = formatTime(audioEl.currentTime);
    });

    audioEl.addEventListener('loadedmetadata', () => {
      /* Only trust the real, loaded audio file's own duration here — never
         the pre-recording duration_sec estimate in data.json. That field is
         a script-writing estimate ("how long we expect the reading to
         take"), not a measurement, and showing it as if it were the actual
         clip length is misleading, especially once real audio is recorded
         and its true length differs from the estimate. */
      if (!Number.isFinite(audioEl.duration)) return;
      timeTotal.textContent = formatTime(audioEl.duration);
    });

    audioEl.addEventListener('ended', async () => {
      playBtn.dataset.ended = '1';
      setPlayingUi(false);
      await releaseWakeLock();
    });

    progress.addEventListener('input', () => {
      if (!audioEl.duration) return;
      progress.style.setProperty('--pct', progress.value);
      audioEl.currentTime = (Number(progress.value) / 100) * audioEl.duration;
    });
  }

  function bindGallery(item) {
    const images = item.images || [];
    const gallery = document.getElementById('gallery');
    const dotsWrap = document.getElementById('gallery-dots');
    if (!gallery) return;

    const imgs = Array.from(gallery.querySelectorAll('img'));
    imgs.forEach((img, i) => {
      img.addEventListener('click', () => openLightbox(images, i, item.title[lang]));
    });

    if (dotsWrap) {
      const dots = Array.from(dotsWrap.children);
      let ticking = false;
      gallery.addEventListener('scroll', () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
          const idx = Math.round(gallery.scrollLeft / (gallery.scrollWidth / imgs.length));
          dots.forEach((d, i) => d.classList.toggle('active', i === idx));
          ticking = false;
        });
      });
    }
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  }

  /* g.sections[].sfx and g.outro are audio-production cues from the source
     guide ("(ध्वनी प्रभाव [SFX]: ...)") — meant for whoever records the
     narration, not for visitors reading the page, so they stay in data.json
     (and the generated audio-scripts/*.md files) but are never rendered here. */
  function renderGuide(g, symbol) {
    const sections = g.sections
      .map(
        (s, i) => `
        <section class="movement" style="--i:${i}">
          <h2 class="movement-label"><span class="ln"></span>${escapeHtml(s.heading)}<span class="ln"></span></h2>
          ${s.paras.map((p) => `<p>${escapeHtml(p)}</p>`).join('')}
          ${s.sources ? `<p class="granth-line">${ICON.scroll}<span>${escapeHtml(s.sources)}</span></p>` : ''}
        </section>
      `
      )
      .join('');

    return `
      ${symbol ? `<img class="symbol-medallion" src="${symbol}" alt="" width="100" height="100" />` : ''}
      <p class="guide-intro">${escapeHtml(g.intro)}</p>
      ${sections}
      <aside class="guide-outro">
        <p class="next-guide">${escapeHtml(g.nextGuide)}</p>
      </aside>
    `;
  }

  function renderItem(item) {
    const u = t();
    const recent = wasRecentVisit(item.id);
    markVisited(item.id);
    currentItem = item;

    const images = item.images || [];
    const galleryImgs = images
      .map(
        // No loading="lazy" here: a gallery only ever has 1-3 images and they
        // sit right at the top of the page the visitor navigated to, so lazy
        // loading buys nothing and has been the suspect in reports of a
        // gallery photo never appearing.
        (src, i) =>
          `<img class="${isDesignRef(src) ? 'is-ref' : ''}" src="${src}" alt="${item.title[lang]}" width="800" height="600" data-idx="${i}" />`
      )
      .join('');
    const dots =
      images.length > 1
        ? `<div class="gallery-dots" id="gallery-dots">${images
            .map((_, i) => `<span class="${i === 0 ? 'active' : ''}"></span>`)
            .join('')}</div>`
        : '';
    // At least one image in this item's gallery is an AI-generated reference
    // sheet, not a photo of the actual physical piece — say so once, under
    // the gallery, rather than leaving a visitor to assume it's a real photo.
    const hasRefImage = images.some(isDesignRef);
    const galleryNote = hasRefImage ? `<p class="gallery-note">${u.galleryRefNote}</p>` : '';

    const guide = item.guide && item.guide[lang];

    const subhead = guide
      ? `<p class="item-subtitle">${escapeHtml(guide.docTitle)}</p>`
      : `<p class="item-meta">
          <span>${ICON.calendar}${item.year || '—'}</span>
          <span>${ICON.location}${item.location[lang]}</span>
        </p>`;

    app.innerHTML = `
      ${recent ? `<div class="banner" role="status">${ICON.info}${u.revisit}</div>` : ''}
      <article>
        <span class="item-eyebrow">${u.itemNo(displayNum(data.items.findIndex((it) => it.id === item.id) + 1))}</span>
        <h1 class="item-title">${item.title[lang]}</h1>
        <div class="flourish" aria-hidden="true"><span class="ln"></span><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.5 7.5H22l-6 4.5 2.5 7.5L12 17l-6.5 4.5L8 14 2 9.5h7.5z"/></svg><span class="ln"></span></div>
        ${subhead}

        <div class="player">
          <audio id="item-audio" preload="metadata" playsinline></audio>
          <div class="player-controls">
            <button type="button" class="skip-btn" id="skip-back" aria-label="-10s">${ICON.skip}</button>
            <button type="button" class="play-btn" id="play-btn" aria-pressed="false">${ICON.play}</button>
            <button type="button" class="skip-btn skip-fwd" id="skip-fwd" aria-label="+10s">${ICON.skip}</button>
          </div>
          <p class="player-label" id="play-label">${u.play}</p>
          <div class="progress-wrap">
            <input type="range" class="progress-bar" id="progress" min="0" max="100" value="0" aria-label="Progress" style="--pct:0" />
            <div class="time-row">
              <span id="time-current">0:00</span>
              <span id="time-total">--:--</span>
            </div>
          </div>
        </div>

        <div class="gallery-wrap">
          <div class="gallery" aria-label="Gallery" id="gallery">${galleryImgs}</div>
          ${dots}
          ${galleryNote}
        </div>

        ${
          guide
            ? `<div class="narrative">${renderGuide(guide, item.symbol)}</div>`
            : `<section class="story">
                 <h2>${ICON.book}${u.story}</h2>
                 <p>${escapeHtml(item.story[lang])}</p>
               </section>`
        }

        ${(() => {
          const idx = data.items.findIndex((it) => it.id === item.id);
          const prevItem = idx > 0 ? data.items[idx - 1] : null;
          const nextItem = idx >= 0 && idx < data.items.length - 1 ? data.items[idx + 1] : null;
          if (!prevItem && !nextItem) return '';
          return `
            <nav class="item-pager" aria-label="इतर आयुधे">
              ${prevItem ? `<a class="back-home" href="?id=${prevItem.id}">← ${escapeHtml(prevItem.title[lang])}</a>` : ''}
              ${nextItem ? `<a class="back-home" href="?id=${nextItem.id}">${escapeHtml(nextItem.title[lang])} →</a>` : ''}
            </nav>
          `;
        })()}

        <a class="back-home" href="?">${ICON.back}${u.homeCta}</a>
      </article>
    `;

    bindPlayer(item);
    bindGallery(item);
  }

  async function switchLanguage(next) {
    if (next === lang) return;
    const wasPlaying = audioEl && !audioEl.paused;
    if (audioEl) {
      audioEl.pause();
      await releaseWakeLock();
    }
    lang = next;
    localStorage.setItem(STORAGE_LANG, lang);
    applyChrome();
    route();
    // Mid-switch: new audio starts paused at 0 (per spec)
    if (wasPlaying && currentItem) {
      /* UI rebuilt; user taps play again intentionally */
    }
  }

  function route() {
    applyChrome();
    const id = getQueryId();
    if (!id) {
      currentItem = null;
      renderHome();
      return;
    }
    const item = findItem(id);
    if (!item) {
      currentItem = null;
      renderError();
      return;
    }
    renderItem(item);
  }

  async function init() {
    updateLangToggle();
    langToggle.addEventListener('click', () => {
      switchLanguage(lang === 'mr' ? 'en' : 'mr');
    });
    lightboxClose.addEventListener('click', closeLightbox);
    lightboxPrev.addEventListener('click', () => lightboxStep(-1));
    lightboxNext.addEventListener('click', () => lightboxStep(1));
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });
    document.addEventListener('keydown', (e) => {
      if (lightbox.hidden) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') lightboxStep(-1);
      if (e.key === 'ArrowRight') lightboxStep(1);
    });
    document.addEventListener('visibilitychange', async () => {
      if (document.visibilityState === 'visible' && audioEl && !audioEl.paused) {
        await requestWakeLock();
      }
    });

    /* Every internal link here is a real <a href> (full navigation), not
       client-side routing, so a fresh visit always re-runs route() via
       init() below. The one gap: the browser's bfcache can restore an
       earlier page entirely from memory on back/forward, skipping JS
       execution and showing whatever was on screen at the moment the user
       left - stale if that page was mid-edit/mid-cache-bug at the time.
       Re-running route() on a persisted pageshow closes that regardless of
       what caused the staleness. */
    window.addEventListener('pageshow', (e) => {
      if (e.persisted) route();
    });

    try {
      await loadData();
      route();
    } catch (err) {
      /* Most common real-world cause: a flaky/offline connection on first
         load, before the service worker has cached the shell — the network
         fetch and the cache fallback can both miss, surfacing as a raw
         "Failed to fetch". A retry button covers that case without a
         confusing dead-end error screen. */
      app.innerHTML = `
        <div class="error-box">
          <h1>${lang === 'mr' ? 'लोड होऊ शकलं नाही' : 'Could not load'}</h1>
          <p>${lang === 'mr' ? 'इंटरनेट कनेक्शन तपासा आणि पुन्हा प्रयत्न करा.' : 'Check your internet connection and try again.'}</p>
          <p class="error-detail">${escapeHtml(String(err.message || err))}</p>
          <button type="button" class="retry-btn" onclick="location.reload()">${lang === 'mr' ? 'पुन्हा प्रयत्न करा' : 'Retry'}</button>
        </div>
      `;
    }
  }

  init();
})();
