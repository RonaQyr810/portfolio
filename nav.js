(function initSiteNav() {
  const nav = document.getElementById('nav');
  if (!nav) return;

  const root = document.documentElement.dataset.navRoot || '';

  const pageLink = (id) => (root ? `${root}index.html#${id}` : `#${id}`);
  const logoHref = root ? `${root}index.html#hero` : '#hero';
  const designHref = root ? `${root}index.html#portfolio` : '#portfolio';
  const videoIndexHref = document.documentElement.dataset.videoIndex || `${root}videos/index.html`;

  const chevron = '<svg viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2.5 4.5L6 8l3.5-3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function buildDropdown(id, label, items) {
    const itemsHtml = items.map(({ href, title, desc }) => `
      <a href="${href}" class="nav-dropdown-item" role="menuitem">
        <span class="nav-dropdown-title">${title}</span>
        <span class="nav-dropdown-desc">${desc}</span>
      </a>`).join('');

    return `
      <li class="nav-dropdown" id="${id}">
        <button type="button" class="nav-dropdown-trigger" aria-expanded="false" aria-haspopup="true">
          ${label} ${chevron}
        </button>
        <div class="nav-dropdown-menu" role="menu">${itemsHtml}</div>
      </li>`;
  }

  const aboutDropdown = buildDropdown('navAbout', '关于我', [
    { href: pageLink('about'), title: '个人简介', desc: '背景、教育与实践概况' },
    { href: pageLink('school'), title: '就读院校', desc: '上海建桥学院与数媒专业' },
    { href: pageLink('highlights'), title: '核心亮点', desc: '用数据说话的能力证明' },
    { href: pageLink('skills'), title: '专业技能', desc: '产品管理、AI 验证、原型与技术协作' },
  ]);

  const portfolioDropdown = buildDropdown('navPortfolio', '产品案例', [
    { href: designHref, title: '核心产品案例', desc: '0→1 交付、AI 应用与原型方案，共 6 个核心项目' },
    { href: `${designHref}`, title: '更多作品', desc: '开发验证、课程作业与影像创作补充' },
    { href: videoIndexHref, title: '视频库', desc: '演示录屏、动画与课程影像，共 31 部' },
  ]);

  const practiceDropdown = buildDropdown('navPractice', '实践', [
    { href: pageLink('experience'), title: '实习经历', desc: '和光同坤三线并行实习' },
    { href: pageLink('projects'), title: '实践项目', desc: '京东美妆活动与传媒运营' },
  ]);

  const topLinks = [
    [pageLink('contact'), '联系'],
  ].map(([href, label]) => `<li><a href="${href}">${label}</a></li>`).join('');

  nav.innerHTML = `
    <div class="nav-inner">
      <a href="${logoHref}" class="nav-logo">秦艺榕</a>
      <button class="nav-toggle" id="navToggle" aria-label="打开菜单">
        <span></span><span></span><span></span>
      </button>
      <ul class="nav-links" id="navLinks">${aboutDropdown}${portfolioDropdown}${practiceDropdown}${topLinks}</ul>
    </div>
  `;

  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  const dropdowns = navLinks.querySelectorAll('.nav-dropdown');
  const pageSections = document.querySelectorAll('section[id], header[id], .about-subsection[id], .practice-subsection[id]');

  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 40);
    if (pageSections.length) updateActiveNavLink();
  });

  navToggle.addEventListener('click', () => {
    navToggle.classList.toggle('open');
    navLinks.classList.toggle('open');
  });

  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navToggle.classList.remove('open');
      navLinks.classList.remove('open');
      closeAllDropdowns();
    });
  });

  dropdowns.forEach(dropdown => initDropdown(dropdown));

  document.addEventListener('click', () => closeAllDropdowns());

  function closeAllDropdowns() {
    dropdowns.forEach(dropdown => {
      dropdown.classList.remove('open');
      dropdown.querySelector('.nav-dropdown-trigger')?.setAttribute('aria-expanded', 'false');
    });
  }

  function initDropdown(dropdown) {
    const trigger = dropdown.querySelector('.nav-dropdown-trigger');

    trigger?.addEventListener('click', (e) => {
      if (window.matchMedia('(min-width: 769px)').matches) return;
      e.stopPropagation();
      const isOpen = dropdown.classList.toggle('open');
      trigger.setAttribute('aria-expanded', String(isOpen));
    });

    dropdown.addEventListener('click', (e) => e.stopPropagation());

    dropdown.addEventListener('mouseenter', () => {
      if (!window.matchMedia('(hover: hover) and (min-width: 769px)').matches) return;
      dropdown.classList.add('open');
      trigger?.setAttribute('aria-expanded', 'true');
    });

    dropdown.addEventListener('mouseleave', () => {
      if (!window.matchMedia('(hover: hover) and (min-width: 769px)').matches) return;
      dropdown.classList.remove('open');
      trigger?.setAttribute('aria-expanded', 'false');
    });
  }

  function hrefMatchesSection(href, sectionId) {
    if (!href) return false;
    return href === `#${sectionId}` || href.endsWith(`#${sectionId}`);
  }

  function updateActiveNavLink() {
    const scrollPos = window.scrollY + 120;
    let current = '';

    pageSections.forEach(section => {
      if (section.offsetTop <= scrollPos) {
        current = section.getAttribute('id');
      }
    });

    navLinks.querySelectorAll(':scope > li > a').forEach(link => {
      link.classList.toggle('active', hrefMatchesSection(link.getAttribute('href'), current));
    });
  }

  if (pageSections.length) updateActiveNavLink();
})();
