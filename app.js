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
      duration: (s) => `${s} सेकंद ऐका`,
      story: 'कहाणी',
      visited: 'पाहिले',
      revisit: 'तुम्ही ही वस्तू आताच पाहिली',
      homeLead: 'QR किंवा NFC स्कॅन करून प्रत्येक वस्तूची कहाणी ऐका.',
      location: 'स्थळ',
      year: 'वर्ष',
      footer: (name) => `${name} · घर संग्रहालय`,
      itemNo: (n) => `वस्तू क्र. ${n}`,
    },
    en: {
      loading: 'Loading…',
      errorTitle: 'Item not found',
      errorBody: 'The QR or link may be wrong. Go back to the list.',
      homeCta: 'See all items',
      play: 'Play',
      pause: 'Pause',
      replay: 'Play again',
      duration: (s) => `Listen · ${s} sec`,
      story: 'Story',
      visited: 'Visited',
      revisit: 'You just viewed this item',
      homeLead: 'Scan QR or NFC to hear each object’s story.',
      location: 'Location',
      year: 'Year',
      footer: (name) => `${name} · Home Museum`,
      itemNo: (n) => `ITEM NO. ${n}`,
    },
  };

  const DEVANAGARI_DIGITS = ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९'];

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
  };

  let data = null;
  let lang = localStorage.getItem(STORAGE_LANG) || 'mr';
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
    const family = meta ? meta.family_name : '';
    brandTitle.textContent = title;
    brandFamily.textContent = family;
    footerText.textContent = t().footer(family || 'Nil');
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
        <a class="back-home" href="./">${ICON.back}${u.homeCta}</a>
      </div>
    `;
  }

  function renderHome() {
    const u = t();
    const meta = data.meta;
    const count = data.items.length;
    const countStr = lang === 'mr' ? displayNum(String(count)) : String(count);
    const eyebrow =
      lang === 'mr' ? `${countStr} वस्तू · ${countStr} कहाण्या` : `${countStr} objects · ${countStr} stories`;
    const cards = data.items
      .map((item, i) => {
        const thumb = item.images[0] || '';
        const visited = isVisited(item.id)
          ? `<span class="visited-pill">${ICON.check}${u.visited}</span>`
          : '';
        return `
          <a class="item-card" href="?id=${item.id}" style="--i:${i}">
            <div class="item-card-media">
              <img class="item-card-img" src="${thumb}" alt="" loading="lazy" width="400" height="300" />
            </div>
            <span class="item-card-badge">${displayNum(item.id)}</span>
            <div class="item-card-body">
              <span class="item-card-title">${item.title[lang]}</span>
              <span class="item-card-meta">${item.year || '—'}</span>
              ${visited}
            </div>
          </a>
        `;
      })
      .join('');

    app.innerHTML = `
      <section class="home-hero">
        <span class="home-eyebrow">${eyebrow}</span>
        <h1>${meta.site_title[lang]}</h1>
        <p>${u.homeLead}</p>
      </section>
      <div class="scallop" aria-hidden="true"></div>
      <div class="item-grid">${cards}</div>
    `;
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
      showError(
        lang === 'mr'
          ? 'ऑडिओ फाइल लोड झाली नाही (media फोल्डर तपासा).'
          : 'Audio file failed to load (check media folder).'
      );
    });

    audioEl.addEventListener('timeupdate', () => {
      if (!audioEl.duration) return;
      const pct = (audioEl.currentTime / audioEl.duration) * 100;
      progress.value = String(pct);
      progress.style.setProperty('--pct', String(pct));
      timeCurrent.textContent = formatTime(audioEl.currentTime);
    });

    audioEl.addEventListener('loadedmetadata', () => {
      timeTotal.textContent = formatTime(audioEl.duration || item.duration_sec || 0);
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

  function renderItem(item) {
    const u = t();
    const recent = wasRecentVisit(item.id);
    markVisited(item.id);
    currentItem = item;

    const images = item.images || [];
    const galleryImgs = images
      .map(
        (src, i) =>
          `<img src="${src}" alt="${item.title[lang]}" loading="lazy" width="800" height="600" data-idx="${i}" />`
      )
      .join('');
    const dots =
      images.length > 1
        ? `<div class="gallery-dots" id="gallery-dots">${images
            .map((_, i) => `<span class="${i === 0 ? 'active' : ''}"></span>`)
            .join('')}</div>`
        : '';

    app.innerHTML = `
      ${recent ? `<div class="banner" role="status">${ICON.info}${u.revisit}</div>` : ''}
      <article>
        <span class="item-eyebrow">${u.itemNo(displayNum(item.id))}</span>
        <h1 class="item-title">${item.title[lang]}</h1>
        <div class="flourish" aria-hidden="true"><span class="ln"></span><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.5 7.5H22l-6 4.5 2.5 7.5L12 17l-6.5 4.5L8 14 2 9.5h7.5z"/></svg><span class="ln"></span></div>
        <p class="item-meta">
          <span>${ICON.calendar}${item.year || '—'}</span>
          <span>${ICON.location}${item.location[lang]}</span>
        </p>
        <span class="duration">${u.duration(item.duration_sec || 0)}</span>

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
              <span id="time-total">${formatTime(item.duration_sec || 0)}</span>
            </div>
          </div>
        </div>

        <div class="gallery-wrap">
          <div class="gallery" aria-label="Gallery" id="gallery">${galleryImgs}</div>
          ${dots}
        </div>

        <section class="story">
          <h2>${ICON.book}${u.story}</h2>
          <p>${item.story[lang]}</p>
        </section>

        <a class="back-home" href="./">${ICON.back}${u.homeCta}</a>
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

    try {
      await loadData();
      route();
    } catch (err) {
      app.innerHTML = `<div class="error-box"><h1>Error</h1><p>${String(err.message || err)}</p></div>`;
    }
  }

  init();
})();
