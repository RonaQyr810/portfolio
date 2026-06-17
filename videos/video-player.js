const GH_PAGES_VIDEO_BASE = 'https://ronaqyr810.github.io/portfolio/assets/videos/';
const GITHUB_MEDIA_BASE =
  'https://media.githubusercontent.com/media/RonaQyr810/portfolio/main/assets/videos/';
const ONLINE_ASSETS_BASE = '../assets/videos/';
const LOCAL_PORTFOLIO_BASE = '../../作品集/';

function isLocalPreview() {
  const host = location.hostname;
  return host === 'localhost' || host === '127.0.0.1' || host === '';
}

function extractVideoSubpath(assetBase) {
  const match = (assetBase || '').match(/assets\/videos\/(.*)/);
  return match ? match[1] : '';
}

function buildVideoCandidates(file, assetBase) {
  const subpath = extractVideoSubpath(assetBase);
  const relativeBase = assetBase || (ONLINE_ASSETS_BASE + subpath);
  const candidates = [relativeBase + file];

  if (!isLocalPreview()) {
    candidates.push(GH_PAGES_VIDEO_BASE + subpath + file);
    candidates.push(GITHUB_MEDIA_BASE + subpath + file);
  }

  return candidates;
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

function showVideoLoadError(mainVideo, playerDesc, item) {
  if (playerDesc) {
    const hint = item?.paths?.length
      ? '视频文件无法播放，可能已损坏或未正确导出。请用 Premiere 重新导出 MP4 后运行 sync-videos，再刷新页面。'
      : '视频加载失败，请检查网络或稍后重试。部分大文件首次加载可能较慢。';
    playerDesc.textContent = hint;
  }
  if (mainVideo) mainVideo.removeAttribute('src');
}

function markCardState(index, state) {
  const card = document.querySelectorAll('.video-card')[index];
  if (!card) return;
  card.classList.toggle('load-error', state === 'error');
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
  let activeCandidates = [];
  let candidateIndex = 0;

  function resolveCandidates(item) {
    const candidates = [];
    if (item.file) candidates.push(...buildVideoCandidates(item.file, assetBase));
    const localPaths = item.paths || (item.path ? [item.path] : []);
    if (isLocalPreview()) {
      localPaths.forEach(rel => candidates.push(resolveLocalPath(rel)));
    }
    return [...new Set(candidates)];
  }

  function onVideoError() {
    candidateIndex += 1;
    if (candidateIndex < activeCandidates.length) {
      mainVideo.src = activeCandidates[candidateIndex];
      mainVideo.load();
      return;
    }
    const item = videos[currentIndex];
    showVideoLoadError(mainVideo, playerDesc, item);
    markCardState(currentIndex, 'error');
  }

  mainVideo.addEventListener('error', onVideoError);

  function playVideo(index, { scrollCard = false, updateUrl = true } = {}) {
    currentIndex = index;
    const item = videos[index];
    activeCandidates = resolveCandidates(item);
    candidateIndex = 0;

    if (!activeCandidates.length) {
      showVideoLoadError(mainVideo, playerDesc, item);
      markCardState(index, 'error');
      return;
    }

    if (playerDesc && item.desc) {
      playerDesc.textContent = item.desc + (item.size ? ` · ${item.size}` : '');
    }

    mainVideo.src = activeCandidates[0];
    mainVideo.load();
    if (playerTitle) playerTitle.textContent = item.title;
    document.querySelectorAll('.video-card').forEach((card, i) => {
      const active = i === index;
      card.classList.toggle('active', active);
      card.classList.toggle('load-error', false);
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
