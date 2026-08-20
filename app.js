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
    },
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

  function openLightbox(src, alt) {
    lightboxImg.src = src;
    lightboxImg.alt = alt || '';
    lightbox.hidden = false;
  }

  function closeLightbox() {
    lightbox.hidden = true;
    lightboxImg.removeAttribute('src');
  }

  function renderError() {
    const u = t();
    app.innerHTML = `
      <div class="error-box">
        <h1>${u.errorTitle}</h1>
        <p>${u.errorBody}</p>
        <a class="back-home" href="./">${u.homeCta}</a>
      </div>
    `;
  }

  function renderHome() {
    const u = t();
    const meta = data.meta;
    const cards = data.items
      .map((item) => {
        const thumb = item.images[0] || '';
        const visited = isVisited(item.id)
          ? `<span class="visited-pill">${u.visited}</span>`
          : '';
        return `
          <a class="item-card" href="?id=${item.id}">
            <img class="item-card-img" src="${thumb}" alt="" loading="lazy" width="400" height="300" />
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
        <h1>${meta.site_title[lang]}</h1>
        <p>${u.homeLead}</p>
      </section>
      <div class="item-grid">${cards}</div>
    `;
  }

  function bindPlayer(item) {
    const u = t();
    const playBtn = document.getElementById('play-btn');
    const progress = document.getElementById('progress');
    const timeCurrent = document.getElementById('time-current');
    const timeTotal = document.getElementById('time-total');

    audioEl = document.getElementById('item-audio');
    if (!audioEl || !playBtn) return;

    audioEl.src = item.audio[lang];
    setupMediaSession(item);

    const setPlayingUi = (playing) => {
      playBtn.textContent = playing ? u.pause : playBtn.dataset.ended === '1' ? u.replay : u.play;
      playBtn.setAttribute('aria-pressed', playing ? 'true' : 'false');
    };

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
        const msg =
          lang === 'mr'
            ? 'ऑडिओ चालू झाला नाही. फाइल तपासा किंवा खरा MP3 ठेवा.'
            : 'Audio could not play. Check the file or add a real MP3.';
        let note = document.getElementById('audio-error');
        if (!note) {
          note = document.createElement('p');
          note.id = 'audio-error';
          note.className = 'audio-error';
          playBtn.insertAdjacentElement('afterend', note);
        }
        note.textContent = msg;
      }
    });

    audioEl.addEventListener('error', () => {
      const msg =
        lang === 'mr'
          ? 'ऑडिओ फाइल लोड झाली नाही (media फोल्डर तपासा).'
          : 'Audio file failed to load (check media folder).';
      let note = document.getElementById('audio-error');
      if (!note) {
        note = document.createElement('p');
        note.id = 'audio-error';
        note.className = 'audio-error';
        playBtn.insertAdjacentElement('afterend', note);
      }
      note.textContent = msg;
    });

    audioEl.addEventListener('timeupdate', () => {
      if (!audioEl.duration) return;
      progress.value = String((audioEl.currentTime / audioEl.duration) * 100);
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
      audioEl.currentTime = (Number(progress.value) / 100) * audioEl.duration;
    });

    document.querySelectorAll('.gallery img').forEach((img) => {
      img.addEventListener('click', () => openLightbox(img.src, item.title[lang]));
    });
  }

  function renderItem(item) {
    const u = t();
    const recent = wasRecentVisit(item.id);
    markVisited(item.id);
    currentItem = item;

    const images = (item.images || [])
      .map(
        (src) =>
          `<img src="${src}" alt="${item.title[lang]}" loading="lazy" width="800" height="600" />`
      )
      .join('');

    app.innerHTML = `
      ${recent ? `<div class="banner" role="status">${u.revisit}</div>` : ''}
      <article>
        <h1 class="item-title">${item.title[lang]}</h1>
        <p class="item-meta">${u.year}: ${item.year || '—'} · ${u.location}: ${item.location[lang]}</p>
        <span class="duration">${u.duration(item.duration_sec || 0)}</span>

        <div class="player">
          <audio id="item-audio" preload="metadata" playsinline></audio>
          <button type="button" class="play-btn" id="play-btn" aria-pressed="false">${u.play}</button>
          <div class="progress-wrap">
            <input type="range" class="progress-bar" id="progress" min="0" max="100" value="0" aria-label="Progress" />
            <div class="time-row">
              <span id="time-current">0:00</span>
              <span id="time-total">${formatTime(item.duration_sec || 0)}</span>
            </div>
          </div>
        </div>

        <div class="gallery" aria-label="Gallery">${images}</div>

        <section class="story">
          <h2>${u.story}</h2>
          <p>${item.story[lang]}</p>
        </section>

        <a class="back-home" href="./">${u.homeCta}</a>
      </article>
    `;

    bindPlayer(item);
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
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeLightbox();
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
