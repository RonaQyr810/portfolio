document.addEventListener('DOMContentLoaded', () => {
  const expTabs = document.getElementById('expTabs');

  const galleries = {
    looptrace: [
      { src: 'assets/portfolio/looptrace-poster.jpg', caption: '环溯 LoopTrace · 惜食小站作品海报' },
      { src: 'assets/portfolio/looptrace-home.png', caption: '环溯 LoopTrace · 首页（责任消费仪表盘）' },
      { src: 'assets/portfolio/looptrace-list.png', caption: '环溯 LoopTrace · 智能购物清单' },
      { src: 'assets/portfolio/looptrace-mall.png', caption: '环溯 LoopTrace · 碳积分商城' },
      { src: 'assets/portfolio/looptrace-rank.png', caption: '环溯 LoopTrace · 企业红黑榜' },
      { src: 'assets/portfolio/looptrace-recycle.png', caption: '环溯 LoopTrace · 智能回收' },
      { src: 'assets/portfolio/looptrace-product.png', caption: '环溯 LoopTrace · 商品详情（供应链护照）' },
      { src: 'assets/portfolio/looptrace-order.png', caption: '环溯 LoopTrace · 订单管理' },
      { src: 'assets/portfolio/looptrace-trace.png', caption: '环溯 LoopTrace · 整改追溯系统' },
      { src: 'assets/portfolio/looptrace-challenge.png', caption: '环溯 LoopTrace · 环保挑战中心' },
      { src: 'assets/portfolio/looptrace-bill.png', caption: '环溯 LoopTrace · 环境账单详情' },
    ],
    'health-food': [
      { src: 'assets/portfolio/health-food-logo.png', caption: '健康食途 · APP 图标' },
      { src: 'assets/portfolio/health-food-login.png', caption: '健康食途 · 登录页' },
      { src: 'assets/portfolio/health-food-home-general.png', caption: '健康食途 · 首页 · 大众会员（每日套餐）' },
      { src: 'assets/portfolio/health-food-home-ai.png', caption: '健康食途 · 首页 · AI 定制会员' },
      { src: 'assets/portfolio/health-food-home-nutritionist.png', caption: '健康食途 · 首页 · 专属营养师定制' },
      { src: 'assets/portfolio/health-food-profile.png', caption: '健康食途 · 个人中心（会员开通 / 目标设置）' },
      { src: 'assets/portfolio/health-food-bubble.png', caption: '健康食途 · 社区冒泡' },
      { src: 'assets/portfolio/health-food-rank.png', caption: '健康食途 · 身体素质排行榜' },
    ],
    medical: [
      { src: 'assets/portfolio/medical-home.jpg', caption: '健康医疗网站 · 首页（DocWala）' },
      { src: 'assets/portfolio/medical-guide.jpg', caption: '健康医疗网站 · 牙痛就医指南页' },
      { src: 'assets/portfolio/medical-hospital.jpg', caption: '健康医疗网站 · 医院列表' },
      { src: 'assets/portfolio/medical-about.png', caption: '健康医疗网站 · 关于我们' },
      { src: 'assets/portfolio/medical-help.png', caption: '健康医疗网站 · 帮助中心' },
      { src: 'assets/portfolio/medical-donation.png', caption: '健康医疗网站 · 捐赠页面' },
      { src: 'assets/portfolio/medical-contact.png', caption: '健康医疗网站 · 联系我们' },
      { src: 'assets/portfolio/medical-register.jpg', caption: '健康医疗网站 · 注册页' },
      { src: 'assets/portfolio/medical-login-web.jpg', caption: '健康医疗网站 · 登录页' },
      { src: 'assets/portfolio/medical-sitemap.png', caption: '健康医疗网站 · 网站结构规划（思维导图）' },
    ],
    'health-pathway': [
      { src: 'assets/portfolio/health-pathway.jpg', caption: '健康之路 · 项目展板（团队项目）' },
    ],
    'web-house': [
      { src: 'assets/portfolio/web-house-sample.jpg', caption: '房屋租赁可视化 Web · 系统界面素材' },
    ],
    brand: [
      { src: 'assets/portfolio/brand-logo-cover.svg', caption: '品牌视觉设计 · 主 LOGO 方案' },
      { src: 'assets/portfolio/brand-logo-alt.png', caption: '品牌视觉设计 · LOGO 变体' },
      { src: 'assets/portfolio/brand-logo-restored.svg', caption: '品牌视觉设计 · LOGO 精修版' },
    ],
    'peking-opera': [
      { src: 'assets/portfolio/peking-opera-cover.png', caption: '梨园之韵 · 京剧文化可视化（封面）' },
    ],
    lixiang: [
      { src: 'assets/portfolio/lixiang/splash.png', caption: '立相 MagicFace · 品牌开屏' },
      { src: 'assets/portfolio/lixiang/login.png', caption: '立相 MagicFace · 登录注册' },
      { src: 'assets/portfolio/lixiang/home.png', caption: '立相 MagicFace · 首页 · 每日运势' },
      { src: 'assets/portfolio/lixiang/scan.png', caption: '立相 MagicFace · 3D 拍摄入口' },
      { src: 'assets/portfolio/lixiang/astro.png', caption: '立相 MagicFace · 关系分析 · 手风琴展开' },
      { src: 'assets/portfolio/lixiang/astro-detail.png', caption: '立相 MagicFace · 十神 / 神煞详情' },
      { src: 'assets/portfolio/lixiang/profile.png', caption: '立相 MagicFace · 我的' },
    ],
  };

  let currentGallery = [];
  let currentIndex = 0;

  if (expTabs) {
    const tabs = expTabs.querySelectorAll('.exp-tab');
    const panels = document.querySelectorAll('.exp-panel');

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const target = tab.dataset.tab;
        tabs.forEach(t => t.classList.remove('active'));
        panels.forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(`panel-${target}`).classList.add('active');
      });
    });
  }

  const portfolioFilters = document.getElementById('portfolioFilters');
  const portfolioItems = document.querySelectorAll('.portfolio-item');

  if (portfolioFilters) {
    portfolioFilters.querySelectorAll('.portfolio-filter').forEach(btn => {
      btn.addEventListener('click', () => {
        const filter = btn.dataset.filter;
        portfolioFilters.querySelectorAll('.portfolio-filter').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        portfolioItems.forEach(item => {
          const categories = item.dataset.category.split(' ');
          const show = filter === 'all' || categories.includes(filter);
          item.classList.toggle('hidden', !show);
        });
      });
    });
  }

  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxCaption = document.getElementById('lightboxCaption');
  const lightboxClose = document.getElementById('lightboxClose');
  const lightboxPrev = document.getElementById('lightboxPrev');
  const lightboxNext = document.getElementById('lightboxNext');

  function openLightbox(galleryKey, index = 0) {
    currentGallery = galleries[galleryKey] || [];
    currentIndex = index;
    if (!currentGallery.length) return;
    updateLightboxImage();
    lightbox.classList.add('open');
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lightbox.classList.remove('open');
    lightbox.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  function updateLightboxImage() {
    const item = currentGallery[currentIndex];
    lightboxImg.src = item.src;
    lightboxImg.alt = item.caption;
    lightboxCaption.textContent = `${item.caption} (${currentIndex + 1}/${currentGallery.length})`;
    const multi = currentGallery.length > 1;
    lightboxPrev.style.display = multi ? 'flex' : 'none';
    lightboxNext.style.display = multi ? 'flex' : 'none';
  }

  function openUrl(url) {
    // noopener 时 window.open 恒为 null，不能用返回值判断弹窗是否成功
    window.open(url, '_blank', 'noopener,noreferrer');
  }

  const RIKXINIAO_PLAY_URL = new URL('projects/rikxiniao/app/play.html', document.baseURI).href;
  const LIXIANG_PLAY_URL = new URL('projects/lixiang/app/play.html', document.baseURI).href;

  function openRikxiniaoDemo() {
    openUrl(RIKXINIAO_PLAY_URL);
  }

  function openLixiangDemo() {
    openUrl(LIXIANG_PLAY_URL);
  }

  document.querySelectorAll('.portfolio-item').forEach(item => {
    const galleryKey = item.dataset.gallery;
    const demoUrl = item.dataset.demo;
    const cover = item.querySelector('.portfolio-cover');
    const coverImg = item.querySelector('.portfolio-cover img');
    const gallery = galleries[galleryKey];

    if (gallery && gallery.length && coverImg && item.dataset.coverSync !== 'false') {
      const coverIndex = Number.parseInt(item.dataset.coverIndex || '0', 10);
      const idx = Number.isFinite(coverIndex) ? Math.min(Math.max(coverIndex, 0), gallery.length - 1) : 0;
      coverImg.src = gallery[idx].src;
      coverImg.alt = gallery[idx].caption;
    }

    if (cover) {
      cover.addEventListener('click', () => {
        if (item.dataset.autoStart) {
          openRikxiniaoDemo();
          return;
        }
        if (demoUrl) {
          if (demoUrl.includes('lixiang')) {
            openLixiangDemo();
            return;
          }
          openUrl(new URL(demoUrl, location.href).href);
        } else if (galleryKey) {
          openLightbox(galleryKey);
        }
      });
    }
  });

  lightboxClose.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', e => {
    if (e.target === lightbox) closeLightbox();
  });

  lightboxPrev.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + currentGallery.length) % currentGallery.length;
    updateLightboxImage();
  });

  lightboxNext.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % currentGallery.length;
    updateLightboxImage();
  });

  document.addEventListener('keydown', e => {
    if (!lightbox.classList.contains('open')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') lightboxPrev.click();
    if (e.key === 'ArrowRight') lightboxNext.click();
  });

  document.querySelectorAll('[data-rikxiniao-demo]').forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      openRikxiniaoDemo();
    });
  });

  document.querySelectorAll('[data-lixiang-demo]').forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      openLixiangDemo();
    });
  });

  document.querySelectorAll('[data-open-gallery]').forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      openLightbox(link.dataset.openGallery);
    });
  });

  const revealElements = document.querySelectorAll(
    '.section-header, .about-card, .about-subsection, .practice-subsection, .school-main, .school-major, .highlight-card, .skill-card, .exp-item, .portfolio-item, .portfolio-video-cta, .project-card, .metric-item, .contact-item, .contact-quote, .exp-highlight'
  );

  revealElements.forEach(el => el.classList.add('reveal'));

  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  revealElements.forEach(el => observer.observe(el));

  document.querySelectorAll('.skill-card').forEach((card, i) => {
    card.style.transitionDelay = `${i * 0.08}s`;
  });

  document.querySelectorAll('.exp-item').forEach((item, i) => {
    item.style.transitionDelay = `${i * 0.1}s`;
  });

  document.querySelectorAll('.highlight-card').forEach((card, i) => {
    card.style.transitionDelay = `${i * 0.06}s`;
  });

  document.querySelectorAll('.portfolio-item').forEach((item, i) => {
    item.style.transitionDelay = `${i * 0.08}s`;
  });
});
