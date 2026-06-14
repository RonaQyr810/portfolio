const GITHUB_MEDIA_BASE =
  'https://media.githubusercontent.com/media/RonaQyr810/portfolio/main/assets/videos/';
const ONLINE_ASSETS_BASE = '../assets/videos/';
const LOCAL_PORTFOLIO_BASE = '../../作品集/';

function isLocalPreview() {
  const host = location.hostname;
  return host === 'localhost' || host === '127.0.0.1' || host === '';
}

function toVideoAssetBase(assetBase) {
  if (isLocalPreview()) {
    return assetBase || ONLINE_ASSETS_BASE;
  }
  if (assetBase) {
    const match = assetBase.match(/assets\/videos\/(.+)?/);
    if (match) return GITHUB_MEDIA_BASE + (match[1] || '');
  }
  return GITHUB_MEDIA_BASE;
}

function resolveLocalPath(relativePath) {
  return encodeURI(LOCAL_PORTFOLIO_BASE + relativePath).replace(/#/g, '%23');
}

function getVideoHint() {
  const params = new URLSearchParams(location.search);
  const query = params.get('v');
  if (query) return query;
  const hash = location.hash.replace(/^#/, '');
  return hash || null;
}

function resolveVideoIndex(videos, hint, fallback = 0) {
  if (!hint) return fallback;
  const decoded = decodeURIComponent(hint);
  if (/^\d+$/.test(decoded)) {
    const n = parseInt(decoded, 10);
    return Number.isFinite(n) ? Math.min(Math.max(n, 0), videos.length - 1) : fallback;
  }
  const byId = videos.findIndex(item => item.id === decoded);
  if (byId >= 0) return byId;
  return fallback;
}

function updateUrlForVideo(item, index) {
  const id = item.id || String(index);
  const url = new URL(location.href);
  url.searchParams.set('v', id);
  url.hash = '';
  history.replaceState({ videoId: id }, '', url);
}

function showVideoLoadError(mainVideo, playerDesc) {
  if (playerDesc) {
    playerDesc.textContent =
      '视频加载失败，请检查网络或稍后重试。部分大文件首次加载可能较慢。';
  }
  if (mainVideo) mainVideo.removeAttribute('src');
}

function initVideoPage(videos, options = {}) {
  const opts = typeof options === 'number' ? { defaultIndex: options } : options;
  const { defaultIndex = 0, assetBase = null } = opts;

  const mainVideo = document.getElementById('mainVideo');
  const playerTitle = document.getElementById('playerTitle');
  const playerDesc = document.getElementById('playerDesc');
  const grid = document.getElementById('videoGrid');
  const mainPlayer = document.querySelector('.main-player');

  if (!mainVideo || !videos.length) return;

  videos.forEach((item, index) => {
    if (!item.id) item.id = `video-${index}`;
  });

  const initialHint = getVideoHint();
  let currentIndex = resolveVideoIndex(videos, initialHint, defaultIndex);

  mainVideo.addEventListener('error', () => showVideoLoadError(mainVideo, playerDesc));

  function resolveSrc(item) {
    if (item.file) {
      const base = toVideoAssetBase(assetBase || (ONLINE_ASSETS_BASE + (item.category || '') + '/'));
      return base + item.file;
    }
    if (item.path) return resolveLocalPath(item.path);
    return '';
  }

  function playVideo(index, { scrollCard = false, updateUrl = true } = {}) {
    currentIndex = index;
    const item = videos[index];
    mainVideo.src = resolveSrc(item);
    mainVideo.load();
    if (playerTitle) playerTitle.textContent = item.title;
    if (playerDesc) {
      playerDesc.textContent = item.desc + (item.size ? ` · ${item.size}` : '');
    }
    document.querySelectorAll('.video-card').forEach((card, i) => {
      const active = i === index;
      card.classList.toggle('active', active);
      if (active && scrollCard) {
        requestAnimationFrame(() => {
          card.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' });
        });
      }
    });
    if (updateUrl) updateUrlForVideo(item, index);
  }

  if (grid) {
    videos.forEach((item, index) => {
      const card = document.createElement('article');
      card.className = 'video-card' + (index === currentIndex ? ' active' : '');
      card.dataset.videoId = item.id;
      card.innerHTML = `
        <div class="video-thumb">▶</div>
        <div class="video-card-body">
          <h3>${item.title}</h3>
          <p>${item.desc}</p>
          ${item.size ? `<span class="size">${item.size}</span>` : ''}
        </div>`;
      card.addEventListener('click', () => playVideo(index, { scrollCard: true }));
      grid.appendChild(card);
    });
  }

  window.addEventListener('popstate', () => {
    const idx = resolveVideoIndex(videos, getVideoHint(), currentIndex);
    playVideo(idx, { scrollCard: true, updateUrl: false });
    if (mainPlayer) {
      mainPlayer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });

  playVideo(currentIndex, { scrollCard: false, updateUrl: !!initialHint });

  if (initialHint && mainPlayer) {
    requestAnimationFrame(() => {
      mainPlayer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }
}
