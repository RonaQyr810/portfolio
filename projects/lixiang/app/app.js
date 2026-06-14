(function () {
  const isPlayMode = document.body.classList.contains('play-mode');
  const app = document.getElementById(isPlayMode ? 'app' : 'html-layer');
  const pickerBtns = document.querySelectorAll('.picker-btn');
  const toast = document.getElementById('toast');

  const TIPS_KEY = 'lixiang-scan-tips-dismissed';
  const PROFILE_KEY = 'lixiang-profile';
  const ASTRO_VIEWS = ['astro', 'astro-ai', 'astro-detail'];

  const DEFAULT_PROFILE = {
    phone: '18926957198',
    phone2: '18926987546',
    avatar: '🌿',
    nickname: '18926957198',
    gender: '女',
    zodiac: '狮子座',
    mbti: '',
    birthDate: '2004-07-25',
    birthTime: '14:30',
    birthplace: '广西',
    residence: '',
  };

  const PROFILE_FIELDS = {
    nickname: { label: '昵称', type: 'text', placeholder: '请输入昵称' },
    gender: { label: '性别', type: 'select', options: ['女', '男', '不公开'] },
    zodiac: {
      label: '星座', type: 'select',
      options: ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座'],
    },
    mbti: {
      label: 'MBTI', type: 'select', allowEmpty: true,
      options: ['INTJ', 'INTP', 'ENTJ', 'ENTP', 'INFJ', 'INFP', 'ENFJ', 'ENFP', 'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ', 'ISTP', 'ISFP', 'ESTP', 'ESFP'],
    },
    birthDate: { label: '出生日期', type: 'date' },
    birthTime: { label: '出生时间', type: 'time' },
    birthplace: { label: '出生地', type: 'text', placeholder: '省 / 市 / 区' },
    residence: { label: '现居地', type: 'text', placeholder: '选填' },
  };

  const ZODIAC_SIGNS = ['摩羯座', '水瓶座', '双鱼座', '白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座'];
  const ZODIAC_EDGES = [20, 19, 21, 21, 21, 22, 23, 23, 23, 24, 23, 22];

  function loadProfile() {
    try {
      const saved = sessionStorage.getItem(PROFILE_KEY);
      if (saved) return { ...DEFAULT_PROFILE, ...JSON.parse(saved) };
    } catch { /* ignore */ }
    return { ...DEFAULT_PROFILE };
  }

  let profile = loadProfile();
  let editingField = null;

  function saveProfile() {
    try { sessionStorage.setItem(PROFILE_KEY, JSON.stringify(profile)); } catch { /* ignore */ }
  }

  function zodiacFromDate(dateStr) {
    if (!dateStr) return profile.zodiac;
    const [, m, d] = dateStr.split('-').map(Number);
    const i = d < ZODIAC_EDGES[m - 1] ? m - 1 : m;
    return ZODIAC_SIGNS[i] || profile.zodiac;
  }

  function profileDisplay(field) {
    const val = profile[field];
    if (field === 'mbti') return val || '未填写';
    if (field === 'residence') return val || '—';
    return val || '—';
  }

  function isProfileEmpty(field) {
    return !profile[field];
  }

  const screens = {
    splash: { builder: buildSplashHTML },
    login: { builder: buildLoginHTML },
    home: { builder: buildHomeHTML },
    scan: { builder: buildScanHTML },
    match: { builder: buildMatchHTML },
    astro: { builder: buildAstroFullHTML },
    'astro-ai': { builder: buildAstroFullHTML },
    'astro-detail': { builder: buildAstroFullHTML },
    profile: { builder: buildProfileHTML },
  };

  let current = isPlayMode ? 'splash' : 'home';
  let lastAstroView = 'astro';
  let splashTimer = null;
  let codeTimer = null;

  function showToast(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(showToast._t);
    showToast._t = setTimeout(() => toast.classList.remove('show'), 2200);
  }

  function syncPicker(id) {
    pickerBtns.forEach(btn => btn.classList.toggle('active', btn.dataset.goto === id));
  }

  function navigate(id, { skipPicker = false, autoSplash = false } = {}) {
    const cfg = screens[id];
    if (!cfg) return;

    current = id;
    clearTimeout(splashTimer);
    clearInterval(codeTimer);

    if (ASTRO_VIEWS.includes(id)) lastAstroView = id;

    if (app) {
      app.hidden = false;
      app.innerHTML = cfg.builder();
      bindScreen(id);
    }

    if (!skipPicker && pickerBtns.length) syncPicker(id);
    if (id === 'splash' && autoSplash) startSplash();
  }

  function startSplash() {
    requestAnimationFrame(() => {
      app?.querySelector('.progress-fill')?.classList.add('run');
    });
    splashTimer = setTimeout(() => navigate('login'), 2600);
  }

  function statusBar(time, light) {
    const cls = light ? 'status-bar light' : 'status-bar';
    return `<div class="${cls}"><span>${time}</span><div class="island"></div><div class="status-icons">●●● ▮▮▮</div></div>`;
  }

  function tabBar(active) {
    const tabs = [
      { id: 'home', icon: '☺', label: '面相' },
      { id: 'match', icon: '♡', label: '匹配' },
      { id: 'astro', icon: '✦', label: '星宿' },
      { id: 'profile', icon: '👤', label: '我的' },
    ];
    return `<nav class="tab-bar" aria-label="底部导航"><div class="tab-bar-inner">${tabs.map(t => {
      const isActive = t.id === 'astro' ? ASTRO_VIEWS.includes(active) : t.id === active;
      return `<button type="button" class="tab-btn${isActive ? ' active' : ''}" data-tab="${t.id}"><span class="ico">${t.icon}</span>${t.label}</button>`;
    }).join('')}</div></nav>`;
  }

  function stars(n, total = 5) {
    return Array.from({ length: total }, (_, i) =>
      `<span class="star${i < n ? ' on' : ''}">★</span>`
    ).join('');
  }

  function buildSplashHTML() {
    return `
      <div class="splash-page">
        <img class="splash-logo" src="logo.png" alt="立相">
        <h1 class="splash-title">立相</h1>
        <p class="splash-sub">探索面相之美</p>
        <div class="splash-progress">
          <p>Loading…</p>
          <div class="progress-track"><div class="progress-fill"></div></div>
        </div>
        <p class="splash-skip">点击任意处跳过</p>
      </div>`;
  }

  function buildLoginHTML() {
    return `
      <div class="page-bg"></div>
      ${statusBar('16:15')}
      <div class="login-page">
        <img class="login-logo" src="logo.png" alt="立相">
        <form class="login-card" data-form="login">
          <h2>登录</h2>
          <p class="login-welcome">欢迎回来</p>
          <label class="field">
            <span class="field-ico">📞</span>
            <input type="tel" placeholder="请输入手机号" maxlength="11" data-field="phone" inputmode="numeric" autocomplete="tel">
          </label>
          <div class="code-row">
            <label class="field flex">
              <span class="field-ico">🔒</span>
              <input type="text" placeholder="6 位验证码" maxlength="6" data-field="code" inputmode="numeric">
            </label>
            <button type="button" class="code-btn" data-action="send-code">获取验证码</button>
          </div>
          <button type="submit" class="btn-primary" data-action="login">立即登录</button>
          <label class="agree-row">
            <span>我已阅读并同意用户协议与隐私政策</span>
            <input type="checkbox" data-field="agree" checked>
          </label>
          <p class="register-hint">没有账户？<button type="button" class="link-btn" data-action="register">立即注册</button></p>
        </form>
      </div>`;
  }

  function buildHomeHTML() {
    return `
      <div class="page-bg"></div>
      ${statusBar('17:15')}
      <div class="scroll-page home-page">
        <div class="home-brand">MagicFace</div>
        <div class="fortune-card">
          <div class="fortune-head">
            <span class="fortune-title">☀ 每日运势</span>
            <span class="fortune-date">2026年6月12日 · 星期五</span>
          </div>
          <h3 class="fortune-motto">静心蓄力，厚积薄发</h3>
          <p class="fortune-tags">综合 生肖 · 星座 · 血型 · 八字 · 五行</p>
          <div class="fortune-overall"><span>综合</span><span class="star-row">${stars(2)}</span></div>
          <p class="fortune-text">今日整体运势平稳，宜静不宜动。人际交往中保持耐心，避免因小事起争执。丙午年火旺，属猴者宜低调行事，多倾听少表态。</p>
          <div class="fortune-grid">
            <div><span>爱情</span><span class="star-row">${stars(5)}</span></div>
            <div><span>事业</span><span class="star-row">${stars(5)}</span></div>
            <div><span>财运</span><span class="star-row">${stars(5)}</span></div>
            <div><span>健康</span><span class="star-row">${stars(2)}</span></div>
          </div>
          <div class="fortune-lucky">
            <span>🐾 幸运色 晨曦金</span>
            <span># 幸运数 6</span>
          </div>
        </div>
        <div class="menu-list">
          <button type="button" class="menu-item" data-action="scan"><span class="menu-ico">📷</span><span><strong>3D 面相扫描</strong><small>推荐 · 精度更高</small></span><span class="chev">›</span></button>
          <button type="button" class="menu-item" data-action="album"><span class="menu-ico">🖼</span><span><strong>从相册选择</strong><small>正脸清晰、光线均匀</small></span><span class="chev">›</span></button>
          <button type="button" class="menu-item" data-action="history"><span class="menu-ico">🕐</span><span><strong>历史报告</strong><small>查看过往分析记录</small></span><span class="chev">›</span></button>
          <button type="button" class="menu-item" data-action="match-history"><span class="menu-ico">💑</span><span><strong>匹配历史</strong><small>查看双人匹配记录</small></span><span class="chev">›</span></button>
        </div>
      </div>
      ${tabBar('home')}`;
  }

  function buildMatchHTML() {
    return `
      <div class="page-bg"></div>
      ${statusBar('17:18', true)}
      <div class="match-page">
        <div class="match-intro">
          <div class="match-icon">📱</div>
          <h2>双人面相匹配</h2>
          <p>你现场拍摄，对方照片从相册上传即可匹配。</p>
        </div>
        <div class="match-actions">
          <button type="button" class="btn-primary" data-match="shoot">本人拍摄 · 对方上传照片</button>
          <button type="button" class="btn-secondary" data-match="same">对方在场 · 同一手机连拍</button>
          <button type="button" class="btn-secondary" data-match="remote">远程邀请 · 对方自行上传</button>
        </div>
      </div>
      ${tabBar('match')}`;
  }

  function buildScanHTML() {
    return `
      <div class="scan-page">
        <div class="scan-camera">
          <div class="scan-preview"></div>
          <div class="scan-oval"></div>
          <p class="scan-hint">请正对镜头，拍摄正脸</p>
        </div>
        <div class="scan-top">
          <button type="button" class="scan-back" data-action="back">取消</button>
          <span>3D 面相扫描</span>
          <button type="button" class="scan-help" data-action="tips">?</button>
        </div>
        <div class="scan-bottom">
          <button type="button" class="scan-side" data-action="album">相册</button>
          <button type="button" class="scan-shutter" data-action="shoot">拍摄</button>
          <button type="button" class="scan-side" data-action="flip">翻转</button>
        </div>
        <div class="scan-tips-sheet hidden" id="scan-tips-sheet">
          <div class="scan-tips-mask" data-action="close-tips"></div>
          <div class="scan-tips-card">
            <div class="scan-tips-header">扫描小贴士</div>
            <div class="scan-tips-body">
              <div class="tips-illus">
                <div class="tips-face"></div>
                <div class="tips-grid"></div>
              </div>
              <ul>
                <li>💡 光线均匀，无阴影遮挡</li>
                <li>👓 身体端正，双肩放平</li>
                <li>🔄 露出额头、眉毛、双耳，头发用发箍固定</li>
              </ul>
              <p class="scan-tips-warn">请按照要求操作，避免影响扫描效果！</p>
            </div>
            <label class="scan-tips-check"><input type="checkbox" data-field="dismiss-tips"> 不再自动弹出</label>
            <button type="button" class="btn-primary" data-action="close-tips">开始扫描</button>
          </div>
        </div>
      </div>`;
  }

  function accordionItem(id, color, title, summary, body, open) {
    return `
      <div class="acc-item${open ? ' open' : ''}" data-acc="${id}">
        <button type="button" class="acc-head" data-toggle-acc="${id}">
          <span class="acc-bar" style="background:${color}"></span>
          <span class="acc-meta"><strong>${title}</strong><small>${summary}</small></span>
          <span class="acc-chev">⌄</span>
        </button>
        <div class="acc-body">${body}</div>
      </div>`;
  }

  const ASTRO_FOCUS = {
    astro: { chip: 'astro', open: ['mbti'], section: 'section-archive' },
    'astro-ai': { chip: 'astro-ai', open: ['ai'], section: 'section-ai' },
    'astro-detail': { chip: 'astro-detail', open: [], section: 'section-detail' },
  };

  function astroChips(activeId) {
    const chips = [
      { id: 'astro', label: '命理档案' },
      { id: 'astro-ai', label: 'AI 总结' },
      { id: 'astro-detail', label: '十神详情' },
    ];
    return `<div class="astro-chips">${chips.map(c =>
      `<button type="button" class="astro-chip${c.id === activeId ? ' active' : ''}" data-astro="${c.id}">${c.label}</button>`
    ).join('')}</div>`;
  }

  function buildAstroFullHTML() {
    const zodiacBody = `
      <p>甲申年属猴，天干甲木坐申金，木金相战而申为禄地，主聪慧机敏、善于应变。申金为食神，思维活跃，创意与表达力俱佳。</p>
      <p>流年丙午火旺，火克金而炼金成器，今年宜在压力中磨砺专业技能，忌与人争口舌。生肖猴逢太岁无冲，整体平稳，农历七月（申月）为本命旺月，可集中推进重要事项。</p>`;

    const signBody = `
      <p>${profile.zodiac}，太阳主宰星座特质。外显热情自信、慷慨大方，有天然领导力与表现欲，在社交场合往往是焦点。</p>
      <p>与八字金日主对照：外放热情与内敛裁断交织，形成「外热内刚」格局。优势是感染力强、决策果断；需注意倾听他人、避免因面子固执己见。与属猴叠加，更添灵动与幽默感。</p>`;

    const mbtiBody = profile.mbti
      ? `<p><strong>你的类型：${profile.mbti}</strong></p>
         <p>结合${profile.zodiac}、属猴与八字金日主，${profile.mbti} 类型让你在直觉与逻辑之间保持独特平衡。可在 AI 整体总结中查看与星座、生肖、八字的交叉解读。</p>
         <div class="acc-callout">在「我的」页面可随时修改 MBTI，命理档案将同步更新。</div>`
      : `<p class="acc-hint">未填写 MBTI。可选择人格类型以获得与星座、生肖、八字交叉的解读。</p>
         <div class="acc-callout">MBTI 描述认知与决策偏好，可与星座外显气质、八字五行格局对照理解。前往「我的」页面即可填写。</div>`;

    const bloodBody = `
      <p>O 型血人群普遍被认为务实果敢、执行力强，目标导向明确，在团队中常扮演推进者角色。</p>
      <p>与金日主辛酉对照：金主决断、O 型主行动，形成「想到就做」的风格。优势是效率高、值得信赖；需注意过于直接可能伤及他人感受，亲密关系里宜多些柔软表达。</p>`;

    const baziBody = `
      <p><strong>四柱：</strong>甲申年 · 壬申月 · 辛酉日 · 甲午时</p>
      <p>辛金日主，生于申月得令而旺。申酉金气汇聚，日主身强。年干甲木为偏财，月干壬水伤官，时干甲木再透偏财，财星有源。</p>
      <p>格局要点：金旺需火炼（事业动力）、需木疏（财星流通）、需水泄（才华输出）。申酉戌金局意向，适合精密、金融、法律、科技等金气行业。</p>`;

    const wuxingBody = `
      <p><strong>命局分布：</strong>木 2 · 火 1 · 土 0 · 金 4 · 水 1</p>
      <p>金旺为病，火为用神（炼金、暖局），木为喜神（疏土、生财），水为闲神（泄秀），土为忌神（生金助旺）。</p>
      <p>调候建议：多接触绿色、东方；佩戴红玛瑙、紫水晶等火性饰品；居家西南方位（土位）不宜堆放金属杂物；宜温和有氧运动，忌过劳耗金。</p>`;

    const aiBody = `
      <div class="ai-block" id="ai-personal"><span class="ai-tag">个人</span>
        <p>作为属猴的灵动、狮子座的热情、O 型血型的果敢务实与八字金日主的果决交织的你，内在驱动力来自对变化与智慧的兴奋、被看见与被认可的渴望，以及裁断与精炼的清醒。外在呈现则带有直率爽朗、自信明快、反应快的色彩。当直觉、理性与情感同频时，你的亲和力与执行力会同步放大，周围人也更容易感受到你的可靠与温度。</p>
        <p>金旺身强，自我意识鲜明，不喜被束缚；劫财多处，独立性强但也需警惕过于自我。建议培养倾听习惯，在团队中既做引领者，也做倾听者。</p>
      </div>
      <div class="ai-block" id="ai-fortune"><span class="ai-tag">运势</span>
        <p>丙午年火旺，与你命局金旺形成火金交锋之势。上半年宜守、不宜冒进；下半年随着水木之气渐生，综合运势回暖。流年劫财透出，有破财之象，大额投资、民间借贷应慎之又慎。</p>
        <p>狮子座的你社交运活跃，属猴者逢申月为本命禄地，适合联络旧友、拓展人脉。本月综合运势 2 星，宜静心蓄力；农历七月后运势上扬，可择机推进搁置计划。</p>
      </div>
      <div class="ai-block" id="ai-career"><span class="ai-tag">事业</span>
        <p>偏印坐月、正印藏支，学习能力与领悟力俱佳，适合深耕专业或考取资质。劫财多处，职场竞争压力不小，合作中须把权责利事先约定清楚。</p>
        <p>金日主格局，适合金融、法律、珠宝、精密技术、医疗器械等金气相关行业；五行缺土，地产、陶艺、后勤管理等土性行业可补缺。领导面前既要有狮子座的担当，也要学会申猴的灵活变通。</p>
      </div>
      <div class="ai-block" id="ai-marriage"><span class="ai-tag">婚姻</span>
        <p>桃花星入命局，人缘与异性缘不差，狮子座在感情中主动而热烈。时柱劫财叠见，晚婚或经历波折后再遇良缘的概率较高，不宜仓促定论终身大事。</p>
        <p>O 型血的你在亲密关系中讲原则、重承诺，宜找能欣赏你决断力且包容你强势的伴侣。八字官杀混杂，择偶时既看重对方能力，也渴望精神共鸣——木气偏旺之人（仁慈、包容）更利调和金旺之刚。</p>
      </div>
      <div class="ai-block" id="ai-family"><span class="ai-tag">家庭</span>
        <p>年柱正官、时柱正官，与长辈缘分不薄，家庭观念强，重视名誉与规矩。劫财旺，兄弟姐妹或同辈之间偶有利益摩擦，宜以和为贵、明算账。</p>
        <p>申金为根，祖上或原生家庭或与金属、交通、机械相关行业有缘。狮子座顾家时慷慨，但也需避免因面子过度承担家族开支。西南方位适当布置黄色、陶瓷元素，有助调和五行。</p>
      </div>`;

    const relationBody = `
      <p><strong>相生：</strong>木生火 · 火生土 · 土生金 · 金生水 · 水生木</p>
      <p><strong>相克：</strong>木克土 · 土克水 · 水克火 · 火克金 · 金克木</p>
      <p>金旺而火弱，五行偏枯；日主金得势偏旺；缺土调和。局内相生：金生水（壬水伤官）、水生木（甲木偏财）；局内相克：火克金（流年丙午）、金克木（财星受日主克制）。</p>
      <p>整体格局金气主导，宜以火木调候。人际关系中，正官星现，贵人运在规矩与制度之中；劫财旺，同辈竞争激烈，合作宜明协议、忌口头承诺。</p>`;

    const shenRows = [
      ['lucky', '天乙贵人', '时支未', '贵人扶持，逢难有助', '吉'],
      ['unlucky', '羊刃', '日支酉', '性情刚烈，宜修身养性', '凶'],
      ['lucky', '金舆', '时支未', '出行有禄，利远方发展', '吉'],
      ['neutral', '桃花', '年支申', '人缘佳、异性缘旺，亦主情感波动', '中性'],
      ['neutral', '华盖', '时支未', '清高孤傲，利艺术、玄学、宗教', '中性'],
      ['lucky', '将星', '月支申', '有领导才能，宜承担管理职责', '吉'],
      ['neutral', '红鸾', '年支申', '主婚恋喜庆，利感情进展', '中性'],
      ['lucky', '天德', '月支申', '逢凶化吉，灾厄减轻', '吉'],
    ].map(([type, name, pos, desc, badge]) =>
      `<div class="shen-row ${type}"><span>${name}</span><span>${pos}</span><span>${desc}</span><span class="badge">${badge}</span></div>`
    ).join('');

    return `
      <div class="astro-shell">
        <div class="page-bg"></div>
        ${statusBar('17:16')}
        ${astroChips('astro')}
        <div class="scroll-page astro-page" id="astro-scroll">
          <h2 class="page-title">星宿关系</h2>

          <section id="section-archive" class="astro-section">
            <div class="astro-card">
              <div class="astro-card-head">
                <span><strong>你的命理档案</strong><small>生肖 · 星座 · MBTI · 血型 · 八字 · 五行</small></span>
              </div>
              <div class="acc-list">
                ${accordionItem('zodiac', '#e8b84a', '生肖', '属猴 · 甲申年', zodiacBody, false)}
                ${accordionItem('sign', '#9c70d4', '星座', profile.zodiac, signBody, false)}
                ${accordionItem('mbti', '#5b8def', 'MBTI', profile.mbti || '未填写', mbtiBody, !profile.mbti)}
                ${accordionItem('blood', '#e878a8', '血型', 'O 型', bloodBody, false)}
                ${accordionItem('bazi', '#8c61b8', '八字', '甲申年 壬申月 辛酉日 甲午时', baziBody, false)}
                ${accordionItem('wuxing', '#e8a04a', '五行', '金命 · 木2 · 火1 · 土0 · 金4 · 水1', wuxingBody, false)}
              </div>
            </div>
          </section>

          <section id="section-ai" class="astro-section">
            <div class="astro-card">
              <div class="astro-card-head">
                <span><strong>AI 整体总结</strong><small>个人 · 运势 · 事业 · 婚姻 · 家庭</small></span>
              </div>
              <div class="acc-list">
                ${accordionItem('ai', '#e878a8', 'AI 综合解读', '五维交叉分析', aiBody, true)}
              </div>
            </div>
          </section>

          <section id="section-detail" class="astro-section">
            <div class="detail-section">
              <h4>星宿关系</h4>
              <div class="detail-card">${relationBody}</div>
            </div>
            <div class="detail-section">
              <h4>十神</h4>
              <div class="pillar-list">
                <div class="pillar-row"><span>年柱</span><span><em>干</em> 劫财 <em>支</em> 正官</span></div>
                <div class="pillar-row"><span>月柱</span><span><em>干</em> 偏印 <em>支</em> 正财</span></div>
                <div class="pillar-row"><span>日柱</span><span><em>干</em> 日主 <em>支</em> 正印 · 劫财</span></div>
                <div class="pillar-row"><span>时柱</span><span><em>干</em> 劫财 <em>支</em> 劫财 · 正印 · 正官</span></div>
              </div>
              <p class="detail-sub"><strong>统计：</strong>劫财 ×4 · 正印 ×2 · 正官 ×2 · 偏印 ×1 · 正财 ×1</p>
              <p class="detail-sub muted"><strong>未显：</strong>比肩 · 食神 · 伤官 · 偏财 · 七杀</p>
              <p class="detail-text">年柱劫财配正官，早年环境竞争与规矩并存；月柱偏印坐正财，灵性与务实并重；日柱辛酉金旺，自我意志坚定；时柱劫财叠见，晚年仍拼搏，宜尽早规划被动收入。整体劫财过旺，宜培养分享与包容，以正官制化劫财。</p>
            </div>
            <div class="detail-section">
              <h4>神煞</h4>
              <div class="shen-list">${shenRows}</div>
            </div>
          </section>
        </div>
        ${tabBar('astro')}
      </div>`;
  }

  function buildProfileHTML() {
    const rows = [
      ['nickname', '昵称'],
      ['gender', '性别'],
      ['zodiac', '星座'],
      ['mbti', 'MBTI'],
    ].map(([field, label]) => {
      const empty = isProfileEmpty(field);
      return `<button type="button" class="info-row" data-edit-field="${field}"><span>${label}</span><span class="info-val${empty ? ' muted' : ''}">${profileDisplay(field)}<span class="info-chev">›</span></span></button>`;
    }).join('');

    const birthRows = [
      ['birthDate', '日期'],
      ['birthTime', '时间'],
      ['birthplace', '出生地'],
      ['residence', '现居地'],
    ].map(([field, label]) => {
      const empty = isProfileEmpty(field);
      return `<button type="button" class="info-row" data-edit-field="${field}"><span>${label}</span><span class="info-val${empty ? ' muted' : ''}">${profileDisplay(field)}<span class="info-chev">›</span></span></button>`;
    }).join('');

    return `
      <div class="page-bg"></div>
      ${statusBar('13:29')}
      <div class="scroll-page profile-page">
        <button type="button" class="profile-header" data-action="edit-avatar">
          <div class="avatar">${profile.avatar}</div>
          <div>
            <div class="profile-phone">${profile.phone}</div>
            <div class="profile-sub">${profile.phone2}</div>
          </div>
          <span class="info-chev profile-chev">›</span>
        </button>
        <p class="section-label">资料</p>
        <div class="info-card">${rows}</div>
        <p class="section-label">出生信息</p>
        <div class="info-card">${birthRows}</div>
        <button type="button" class="btn-logout" data-action="logout">退出登录</button>
      </div>
      <div class="edit-sheet hidden" id="edit-sheet">
        <div class="edit-sheet-mask" data-action="close-edit"></div>
        <div class="edit-sheet-card">
          <div class="edit-sheet-header">
            <button type="button" class="edit-sheet-cancel" data-action="close-edit">取消</button>
            <span class="edit-sheet-title" id="edit-sheet-title">编辑</span>
            <button type="button" class="edit-sheet-save" data-action="save-edit">保存</button>
          </div>
          <div class="edit-sheet-body" id="edit-sheet-body"></div>
        </div>
      </div>
      ${tabBar('profile')}`;
  }

  function buildEditFieldHTML(field) {
    const cfg = PROFILE_FIELDS[field];
    if (!cfg) return '';
    const val = profile[field] || '';

    if (cfg.type === 'select') {
      const opts = cfg.options.map(opt => {
        const selected = val === opt ? ' selected' : '';
        return `<option value="${opt}"${selected}>${opt}</option>`;
      }).join('');
      const emptyOpt = cfg.allowEmpty ? `<option value=""${!val ? ' selected' : ''}>未填写</option>` : '';
      return `<label class="edit-field"><span>${cfg.label}</span><select data-edit-input="${field}">${emptyOpt}${opts}</select></label>`;
    }

    if (cfg.type === 'date') {
      return `<label class="edit-field"><span>${cfg.label}</span><input type="date" data-edit-input="${field}" value="${val}"></label>`;
    }

    if (cfg.type === 'time') {
      return `<label class="edit-field"><span>${cfg.label}</span><input type="time" data-edit-input="${field}" value="${val}"></label>`;
    }

    return `<label class="edit-field"><span>${cfg.label}</span><input type="text" data-edit-input="${field}" value="${val}" placeholder="${cfg.placeholder || ''}"></label>`;
  }

  function openEditSheet(field) {
    const cfg = PROFILE_FIELDS[field];
    if (!cfg) return;
    editingField = field;
    const sheet = app?.querySelector('#edit-sheet');
    const title = app?.querySelector('#edit-sheet-title');
    const body = app?.querySelector('#edit-sheet-body');
    if (!sheet || !title || !body) return;
    title.textContent = `编辑${cfg.label}`;
    body.innerHTML = buildEditFieldHTML(field);
    sheet.classList.remove('hidden');
    body.querySelector('input, select')?.focus();
  }

  function closeEditSheet() {
    editingField = null;
    app?.querySelector('#edit-sheet')?.classList.add('hidden');
  }

  function saveEditField() {
    if (!editingField || editingField === '__avatar__') return;
    const input = app?.querySelector(`[data-edit-input="${editingField}"]`);
    if (!input) return;

    const value = input.value.trim();
    const cfg = PROFILE_FIELDS[editingField];
    if (!cfg) return;

    if (cfg.type === 'text' && editingField === 'nickname' && !value) {
      showToast('昵称不能为空');
      return;
    }

    profile[editingField] = value;

    if (editingField === 'birthDate') {
      profile.zodiac = zodiacFromDate(value);
    }

    saveProfile();
    closeEditSheet();
    refreshProfileRows();
    if (editingField === 'birthDate') {
      showToast(`已保存 · 星座同步为 ${profile.zodiac}`);
    } else {
      showToast('已保存');
    }
  }

  function refreshProfileRows() {
    app?.querySelectorAll('[data-edit-field]').forEach(btn => {
      const field = btn.dataset.editField;
      const valEl = btn.querySelector('.info-val');
      if (!valEl) return;
      const empty = isProfileEmpty(field);
      valEl.className = `info-val${empty ? ' muted' : ''}`;
      valEl.innerHTML = `${profileDisplay(field)}<span class="info-chev">›</span>`;
    });
    const avatar = app?.querySelector('.avatar');
    if (avatar) avatar.textContent = profile.avatar;
  }

  function openAvatarPicker() {
    const avatars = ['🌿', '🌸', '😊', '🦊', '🐱', '🌙'];
    editingField = '__avatar__';
    const sheet = app?.querySelector('#edit-sheet');
    const title = app?.querySelector('#edit-sheet-title');
    const body = app?.querySelector('#edit-sheet-body');
    if (!sheet || !title || !body) return;
    title.textContent = '更换头像';
    body.innerHTML = `<div class="avatar-picker">${avatars.map(a =>
      `<button type="button" class="avatar-opt${profile.avatar === a ? ' active' : ''}" data-avatar="${a}">${a}</button>`
    ).join('')}</div>`;
    sheet.classList.remove('hidden');
    body.querySelectorAll('[data-avatar]').forEach(btn => {
      btn.addEventListener('click', () => {
        profile.avatar = btn.dataset.avatar;
        saveProfile();
        refreshProfileRows();
        closeEditSheet();
        showToast('头像已更新');
      });
    });
  }

  function bindTabButtons() {
    app?.querySelectorAll('[data-tab]').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        const tab = btn.dataset.tab;
        navigate(tab === 'astro' ? lastAstroView : tab);
      });
    });
  }

  function bindAstroChips() {
    app?.querySelectorAll('[data-astro]').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        const viewId = btn.dataset.astro;
        lastAstroView = viewId;
        current = viewId;
        syncPicker(viewId);
        updateAstroChipActive(viewId);
        applyAstroFocus(viewId);
      });
    });
  }

  function updateAstroChipActive(viewId) {
    const chipId = ASTRO_FOCUS[viewId]?.chip || viewId;
    app?.querySelectorAll('[data-astro]').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.astro === chipId);
    });
  }

  function bindAstroAccordions() {
    app?.querySelectorAll('[data-toggle-acc]').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        btn.closest('[data-acc]')?.classList.toggle('open');
      });
    });
  }

  function applyAstroFocus(viewId) {
    const focus = ASTRO_FOCUS[viewId] || ASTRO_FOCUS.astro;
    updateAstroChipActive(viewId);

    app?.querySelectorAll('[data-acc]').forEach(item => {
      if (!focus.open.includes(item.dataset.acc)) item.classList.remove('open');
    });
    focus.open.forEach(accId => {
      app?.querySelector(`[data-acc="${accId}"]`)?.classList.add('open');
    });

    const scrollEl = app?.querySelector('#astro-scroll');
    const section = app?.querySelector(`#${focus.section}`);
    if (!scrollEl || !section) return;

    requestAnimationFrame(() => {
      const top = section.getBoundingClientRect().top - scrollEl.getBoundingClientRect().top + scrollEl.scrollTop;
      scrollEl.scrollTo({ top: Math.max(0, top - 52), behavior: 'smooth' });
    });
  }

  function tipsDismissed() {
    try { return sessionStorage.getItem(TIPS_KEY) === '1'; } catch { return false; }
  }

  function setTipsDismissed(value) {
    try { sessionStorage.setItem(TIPS_KEY, value ? '1' : '0'); } catch { /* ignore */ }
  }

  function openTips() {
    app?.querySelector('#scan-tips-sheet')?.classList.remove('hidden');
  }

  function closeTips() {
    const sheet = app?.querySelector('#scan-tips-sheet');
    const dismiss = app?.querySelector('[data-field="dismiss-tips"]');
    if (dismiss?.checked) setTipsDismissed(true);
    sheet?.classList.add('hidden');
  }

  function startCodeCountdown(btn) {
    let sec = 60;
    btn.disabled = true;
    btn.textContent = `${sec}s`;
    clearInterval(codeTimer);
    codeTimer = setInterval(() => {
      sec -= 1;
      if (sec <= 0) {
        clearInterval(codeTimer);
        btn.disabled = false;
        btn.textContent = '获取验证码';
        return;
      }
      btn.textContent = `${sec}s`;
    }, 1000);
  }

  function submitLogin(e) {
    e?.preventDefault();
    const phone = app.querySelector('[data-field="phone"]');
    const agree = app.querySelector('[data-field="agree"]');
    if (phone && !phone.value.trim()) {
      showToast('请输入手机号');
      phone.focus();
      return;
    }
    if (agree && !agree.checked) {
      showToast('请先同意用户协议');
      return;
    }
    showToast('登录成功');
    const phoneInput = app.querySelector('[data-field="phone"]');
    if (phoneInput?.value.trim()) {
      profile.phone = phoneInput.value.trim();
      if (!profile.nickname || profile.nickname === DEFAULT_PROFILE.nickname) {
        profile.nickname = phoneInput.value.trim();
      }
      saveProfile();
    }
    setTimeout(() => navigate('home'), 400);
  }

  function runScanAnalysis(btn) {
    if (btn) {
      btn.disabled = true;
      btn.textContent = '分析中…';
    }
    showToast('正在分析面相…');
    setTimeout(() => navigate('astro'), 1600);
  }

  function bindScreen(id) {
    bindTabButtons();

    if (id === 'splash') {
      app?.addEventListener('click', () => navigate('login'), { once: true });
      return;
    }

    if (id === 'login') {
      app.querySelector('[data-form="login"]')?.addEventListener('submit', submitLogin);
      app.querySelector('[data-action="send-code"]')?.addEventListener('click', e => {
        const phone = app.querySelector('[data-field="phone"]');
        if (!phone?.value.trim()) {
          showToast('请先输入手机号');
          phone?.focus();
          return;
        }
        startCodeCountdown(e.currentTarget);
        showToast('验证码已发送');
      });
      app.querySelector('[data-action="register"]')?.addEventListener('click', () => showToast('注册功能演示'));
      return;
    }

    if (id === 'home') {
      app.querySelector('[data-action="scan"]')?.addEventListener('click', () => navigate('scan'));
      app.querySelector('[data-action="album"]')?.addEventListener('click', () => {
        showToast('从相册选取正脸照片');
        setTimeout(() => navigate('scan'), 500);
      });
      app.querySelector('[data-action="history"]')?.addEventListener('click', () => {
        showToast('跳转到历史报告');
        setTimeout(() => navigate('astro-detail'), 400);
      });
      app.querySelector('[data-action="match-history"]')?.addEventListener('click', () => {
        showToast('跳转到匹配历史');
        setTimeout(() => navigate('match'), 400);
      });
      return;
    }

    if (id === 'match') {
      app.querySelectorAll('[data-match]').forEach(btn => {
        btn.addEventListener('click', () => {
          const mode = btn.dataset.match;
          if (mode === 'remote') {
            showToast('已生成邀请链接（演示）');
            return;
          }
          showToast('进入拍摄流程…');
          setTimeout(() => navigate('scan'), 500);
        });
      });
      return;
    }

    if (id === 'scan') {
      app.querySelector('[data-action="back"]')?.addEventListener('click', () => navigate('home'));
      app.querySelector('[data-action="tips"]')?.addEventListener('click', openTips);
      app.querySelector('[data-action="close-tips"]')?.addEventListener('click', closeTips);
      app.querySelector('.scan-tips-mask')?.addEventListener('click', closeTips);
      app.querySelector('[data-action="shoot"]')?.addEventListener('click', e => runScanAnalysis(e.currentTarget));
      app.querySelector('[data-action="album"]')?.addEventListener('click', () => {
        showToast('从相册选取');
        setTimeout(() => runScanAnalysis(null), 800);
      });
      app.querySelector('[data-action="flip"]')?.addEventListener('click', () => showToast('切换前置摄像头'));
      if (!tipsDismissed()) setTimeout(openTips, 500);
      return;
    }

    if (id === 'profile') {
      app.querySelectorAll('[data-edit-field]').forEach(btn => {
        btn.addEventListener('click', () => openEditSheet(btn.dataset.editField));
      });
      app.querySelector('[data-action="edit-avatar"]')?.addEventListener('click', openAvatarPicker);
      app.querySelector('[data-action="close-edit"]')?.addEventListener('click', closeEditSheet);
      app.querySelector('.edit-sheet-mask')?.addEventListener('click', closeEditSheet);
      app.querySelector('[data-action="save-edit"]')?.addEventListener('click', saveEditField);
      app.querySelector('[data-action="logout"]')?.addEventListener('click', () => {
        showToast('已退出登录');
        setTimeout(() => navigate('login'), 500);
      });
      return;
    }

    if (ASTRO_VIEWS.includes(id)) {
      bindAstroAccordions();
      bindAstroChips();
      applyAstroFocus(id);
    }
  }

  pickerBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const goto = btn.dataset.goto;
      navigate(goto, { autoSplash: goto === 'splash' });
    });
  });

  if (isPlayMode) {
    navigate('splash', { autoSplash: true });
  } else {
    navigate('home');
  }
})();
