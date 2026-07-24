# Crystal Dark 视觉升级 — 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use `agentic-engineering` or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 对阿昕个人网站进行全面视觉升级 — 玻璃质感、3D 深度、微交互、动态光效

**Architecture:** 所有样式/脚本内联在 HTML 中（无构建步骤）。每项改动在一个文件中完成，所有页面共享同一套 CSS 变量设计系统。

**Tech Stack:** 原生 HTML5 + CSS3 + Vanilla JS (Canvas API, IntersectionObserver, CSS animations)

---

## 文件改动总览

| 文件 | 改动量 | 核心变更 |
|------|--------|---------|
| `index.html` | 大 | 全部 CSS 变量 + Hero 3D晶体 + 鼠标光照 + 磁性按钮 + 3D tilt + 进度条 + 技能数字动画 + 表单升级 |
| `project-ai.html` | 中 | CSS 设计系统对齐 + 进度条 + shimmer + 返回动画 |
| `project-dashboard.html` | 中 | 同上 |
| `project-ecommerce.html` | 中 | 同上 |
| `project-weekly-os.html` | 中 | CSS 设计系统对齐 + 价格动效 + CTA 光晕动画 + 弹窗 spring 动画 |

---

### Task 1: CSS 设计系统 & 玻璃质感基础

**文件:** `index.html`, `project-ai.html`, `project-dashboard.html`, `project-ecommerce.html`, `project-weekly-os.html`

**说明:** 更新所有页面的 `:root` CSS 变量，统一设计系统。新增玻璃卡片系统。这是所有后续任务的基础。

**Interfaces:**
- Produces: `--crystal-glow`, `--gold-accent`, `.glass-card` 等全局 CSS 类，供所有页面使用

---

- [ ] **Step 1: 更新 index.html 的 CSS 变量和玻璃系统**

在 `index.html` 的 `:root` 中更新：

```css
:root {
  /* 保留现有 */
  --primary: #a855f7;
  --primary-light: #c084fc;
  --primary-dark: #7c3aed;
  --secondary: #ec4899;
  --accent-gradient: linear-gradient(135deg, #a855f7, #ec4899);

  /* 新增: 结晶色系 */
  --crystal: #8a6bff;
  --crystal-light: #4fc3ff;
  --crystal-gradient: linear-gradient(135deg, #8a6bff, #4fc3ff);
  --gold: #fbbf24;
  --gold-gradient: linear-gradient(135deg, #fbbf24, #f59e0b);

  /* 调整: 更柔和的黑色基底 */
  --bg: #05060a;

  /* 保留以下不变 */
  --bg-surface: rgba(255, 255, 255, 0.04);
  --bg-surface-hover: rgba(255, 255, 255, 0.08);
  --bg-glass: rgba(255, 255, 255, 0.03);
  --text: #ffffff;
  --text-secondary: rgba(255, 255, 255, 0.7);
  --text-muted: rgba(255, 255, 255, 0.45);
  --text-dim: rgba(255, 255, 255, 0.25);
  --border: rgba(255, 255, 255, 0.06);
  --border-hover: rgba(255, 255, 255, 0.12);
  --radius-sm: 8px;
  --radius: 16px;
  --radius-lg: 24px;
  --radius-xl: 32px;
  --shadow-glow: 0 0 60px rgba(168, 85, 247, 0.15);
  --transition: 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}

/* 新增: 玻璃卡片复用类 */
.glass-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%);
  backdrop-filter: blur(20px) saturate(1.4);
  -webkit-backdrop-filter: blur(20px) saturate(1.4);
  border: 1px solid var(--border);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.1), 0 0 40px rgba(168,85,247,0.06);
}

/* 新增: 金色强调类 */
.gold-text {
  background: var(--gold-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

- [ ] **Step 2: 更新所有 project-*.html 的 CSS 变量**

在每个 project-*.html 的 `:root` 中添加相同的变量集（特别注意 `--bg: #05060a` 和新增的 `--crystal`/`--gold` 系列）。

- [ ] **Step 3: 将现有卡片类改为 glass-card**

在 `index.html` 中，找到 `.about-info .item`、`.skill-card`、`.project-card`，添加 `box-shadow: inset 0 1px 0 rgba(255,255,255,0.1), 0 0 40px rgba(168,85,247,0.06);`

在 project-*.html 中，在 `.project-content ul li` 和 `.feature-card` 等处同样添加。

---

### Task 2: 导航栏 + 滚动进度条

**文件:** `index.html`

**说明:** 导航栏增加顶部滚动进度条、当前 section 高亮

---

- [ ] **Step 1: 添加进度条 HTML**

在 `<nav class="navbar">` 内部末尾添加：

```html
<div class="progress-bar" id="progressBar"></div>
```

- [ ] **Step 2: 添加进度条 CSS**

在导航栏相关 CSS 中追加：

```css
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  padding: 20px 0 0; /* 底部留空间给进度条 */
}

.progress-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 1.5px;
  background: var(--accent-gradient);
  width: 0%;
  transition: width 0.1s linear;
  border-radius: 0 1px 1px 0;
}
```

- [ ] **Step 3: 添加进度条 JS**

在 `index.html` 的 `<script>` 中加入：

```js
// ===== 滚动进度条 =====
const progressBar = document.getElementById('progressBar');
window.addEventListener('scroll', () => {
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const scrollPercent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
  progressBar.style.width = scrollPercent + '%';
});
```

- [ ] **Step 4: 添加当前 section 高亮 JS**

```js
// ===== 当前 Section 导航高亮 =====
const sections = document.querySelectorAll('section[id]');
const navAnchors = document.querySelectorAll('.nav-links a');
const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navAnchors.forEach(a => {
        a.style.color = a.getAttribute('href') === '#' + entry.target.id ? 'var(--text)' : '';
      });
    }
  });
}, { threshold: 0.3, rootMargin: '-80px 0px 0px 0px' });
sections.forEach(s => sectionObserver.observe(s));
```

---

### Task 3: Hero 区升级 — 3D 晶体粒子

**文件:** `index.html`

**说明:** 在 Hero Canvas 中绘制旋转 3D 多面体（八面体），半透明紫/青色，鼠标跟随视差

---

- [ ] **Step 1: 在 Canvas 中添加 3D 晶体类**

在现有的粒子 Canvas 代码中，在 `class Particle` 之后追加 `class Crystal`：

```js
// ===== 3D 浮动晶体 =====
class Crystal {
  constructor(w, h) {
    this.w = w;
    this.h = h;
    this.reset();
  }
  reset() {
    this.x = Math.random() * this.w;
    this.y = Math.random() * this.h;
    this.z = Math.random() * 200 - 100; // 深度
    this.size = Math.random() * 30 + 15;
    this.rotation = Math.random() * Math.PI * 2;
    this.rotSpeed = (Math.random() - 0.5) * 0.02;
    this.opacity = Math.random() * 0.3 + 0.1;
    this.color = Math.random() > 0.5 ? '#8a6bff' : '#4fc3ff';
    this.floatAmp = Math.random() * 20 + 10;
    this.floatSpeed = Math.random() * 0.005 + 0.003;
    this.floatOffset = Math.random() * Math.PI * 2;
  }
  update(time, mouseX, mouseY) {
    this.rotation += this.rotSpeed;
    // 浮动
    this.y += Math.sin(time * this.floatSpeed + this.floatOffset) * 0.3;
    this.x += Math.cos(time * this.floatSpeed * 0.7 + this.floatOffset) * 0.2;
    // 鼠标视差
    if (mouseX) {
      const dx = (mouseX / this.w - 0.5) * this.z * 0.05;
      this.x += dx;
    }
    if (mouseY) {
      const dy = (mouseY / this.h - 0.5) * this.z * 0.05;
      this.y += dy;
    }
    // 边界循环
    if (this.x < -50) this.x = this.w + 50;
    if (this.x > this.w + 50) this.x = -50;
    if (this.y < -50) this.y = this.h + 50;
    if (this.y > this.h + 50) this.y = -50;
  }
  draw(ctx) {
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.rotate(this.rotation);
    ctx.globalAlpha = this.opacity;
    ctx.strokeStyle = this.color;
    ctx.lineWidth = 1.2;
    ctx.shadowColor = this.color;
    ctx.shadowBlur = 10;

    const s = this.size;
    // 绘制八面体 (两个菱形)
    ctx.beginPath();
    ctx.moveTo(0, -s);
    ctx.lineTo(s * 0.6, -s * 0.3);
    ctx.lineTo(0, s * 0.4);
    ctx.lineTo(-s * 0.6, -s * 0.3);
    ctx.closePath();
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(0, s);
    ctx.lineTo(s * 0.6, s * 0.3);
    ctx.lineTo(0, -s * 0.4);
    ctx.lineTo(-s * 0.6, s * 0.3);
    ctx.closePath();
    ctx.stroke();

    ctx.restore();
  }
}
```

- [ ] **Step 2: 初始化晶体并添加到动画循环**

将粒子初始化后的代码改为同时管理晶体：

```js
// 在粒子初始化之后
const crystals = [];
for (let i = 0; i < 8; i++) crystals.push(new Crystal(w, h));

// 鼠标位置跟踪
let mouseX = null, mouseY = null;
canvas.addEventListener('mousemove', (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
});
canvas.addEventListener('mouseleave', () => { mouseX = null; mouseY = null; });

// 在 animate 函数中，在粒子绘制之后加入:
let time = 0;
// 修改 animate:
function animate() {
  ctx.clearRect(0, 0, w, h);
  time++;
  particles.forEach(p => { p.update(); p.draw(); });
  connect();
  crystals.forEach(c => {
    c.update(time, mouseX, mouseY);
    c.draw(ctx);
  });
  requestAnimationFrame(animate);
}
```

- [ ] **Step 3: 添加 Hero 鼠标光照效果**

在 Hero CSS 中添加光晕跟随变量，JS 中更新：

```js
// Hero 鼠标追光
const heroSection = document.querySelector('.hero');
heroSection.addEventListener('mousemove', (e) => {
  const rect = heroSection.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * 100;
  const y = ((e.clientY - rect.top) / rect.height) * 100;
  heroSection.style.setProperty('--mouse-x', x + '%');
  heroSection.style.setProperty('--mouse-y', y + '%');
});
```

在 hero CSS 中，修改 `.hero::before`：

```css
.hero::before {
  content: '';
  position: absolute;
  top: var(--mouse-y, 50%);
  left: var(--mouse-x, 50%);
  transform: translate(-50%, -50%);
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(168, 85, 247, 0.12) 0%, transparent 60%);
  pointer-events: none;
  transition: top 0.3s ease-out, left 0.3s ease-out;
}
```

---

### Task 4: 磁性按钮 + Hero 滚动视差

**文件:** `index.html`

---

- [ ] **Step 1: 磁性按钮 JS**

在 Hero actions 的按钮上添加磁性跟随：

```js
// ===== 磁性按钮 =====
document.querySelectorAll('.hero-actions .btn').forEach(btn => {
  btn.addEventListener('mousemove', (e) => {
    const rect = btn.getBoundingClientRect();
    const dx = e.clientX - rect.left - rect.width / 2;
    const dy = e.clientY - rect.top - rect.height / 2;
    const dist = Math.sqrt(dx * dx + dy * dy);
    const maxDist = 100;
    if (dist < maxDist) {
      const strength = (1 - dist / maxDist) * 8;
      const angle = Math.atan2(dy, dx);
      const moveX = Math.cos(angle) * strength;
      const moveY = Math.sin(angle) * strength;
      btn.style.transform = `translate(${moveX}px, ${moveY}px) scale(1.03)`;
      btn.style.boxShadow = `0 0 30px rgba(168, 85, 247, ${0.1 + strength * 0.02})`;
    }
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transform = '';
    btn.style.boxShadow = '';
  });
});
```

- [ ] **Step 2: Hero 按钮涟漪效果**

在每个按钮上添加点击涟漪：

```js
// ===== 按钮涟漪 =====
document.querySelectorAll('.hero-actions .btn').forEach(btn => {
  btn.addEventListener('click', function(e) {
    const ripple = document.createElement('span');
    ripple.className = 'ripple';
    const rect = this.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
    ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
    this.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });
});
```

CSS 波纹：

```css
.ripple {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: scale(0);
  animation: ripple-effect 0.6s ease-out;
  pointer-events: none;
}
.btn { position: relative; overflow: hidden; }
@keyframes ripple-effect {
  to { transform: scale(4); opacity: 0; }
}
```

- [ ] **Step 3: Hero 滚动视差**

```js
// ===== Hero 滚动视差 =====
window.addEventListener('scroll', () => {
  const heroContent = document.querySelector('.hero-content');
  const scrollY = window.scrollY;
  if (scrollY < window.innerHeight) {
    heroContent.style.transform = `translateY(${scrollY * 0.15}px)`;
    heroContent.style.opacity = 1 - scrollY / (window.innerHeight * 0.8);
  }
});
```

---

### Task 5: 3D Card Tilt + 微交互系统

**文件:** `index.html`

---

- [ ] **Step 1: 3D 卡片倾斜**

给 `.project-card` 添加 3D tilt 效果：

```js
// ===== 3D Card Tilt =====
document.querySelectorAll('.project-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;
    const y = (e.clientY - rect.top) / rect.height;
    const tiltX = (y - 0.5) * -12;
    const tiltY = (x - 0.5) * 12;
    card.style.transform =
      `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) translateY(-6px)`;
    // 光晕跟随
    const glareX = x * 100 + '%';
    const glareY = y * 100 + '%';
    card.style.setProperty('--glare-x', glareX);
    card.style.setProperty('--glare-y', glareY);
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
  });
});
```

添加 CSS：
```css
.project-card {
  transition: transform 0.2s ease-out, border-color 0.4s, box-shadow 0.4s;
  position: relative;
  overflow: hidden;
}
.project-card::after {
  content: '';
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: radial-gradient(circle at var(--glare-x, 50%) var(--glare-y, 50%),
    rgba(168,85,247,0.08) 0%, transparent 60%);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s;
}
.project-card:hover::after {
  opacity: 1;
}
```

- [ ] **Step 2: 技能数字跳动**

替换现有的技能条动画为数字跳动：

```js
// ===== 技能数字跳动 =====
const skillObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const card = entry.target;
      const bar = card.querySelector('.skill-bar');
      const label = card.querySelector('.skill-bar-label span:last-child');
      if (bar && !bar.dataset.animated) {
        const level = parseInt(bar.dataset.level);
        bar.dataset.animated = 'true';
        // 延迟 0.3s 后开始动画（制造节奏感）
        setTimeout(() => {
          bar.style.width = level + '%';
          // 数字跳动
          let current = 0;
          const step = Math.ceil(level / 30);
          const interval = setInterval(() => {
            current += step;
            if (current >= level) {
              current = level;
              clearInterval(interval);
            }
            label.textContent = current + '%';
          }, 30);
        }, 300);
      }
    }
  });
}, { threshold: 0.3 });
document.querySelectorAll('.skill-card').forEach(card => skillObserver.observe(card));
```

- [ ] **Step 3: 时间线节点脉冲 + 流动光点**

```css
.timeline-item::before {
  /* 增强光晕 */
  box-shadow: 0 0 0 2px var(--primary), 0 0 20px rgba(168, 85, 247, 0.3);
  animation: timeline-pulse 3s ease-in-out infinite;
}
@keyframes timeline-pulse {
  0%, 100% { box-shadow: 0 0 0 2px var(--primary), 0 0 20px rgba(168, 85, 247, 0.3); }
  50% { box-shadow: 0 0 0 4px var(--primary), 0 0 30px rgba(168, 85, 247, 0.5); }
}

/* 连线上流动光点 */
.timeline::before {
  background: linear-gradient(to bottom, var(--primary), var(--secondary), transparent);
  /* 新增光点流动动画 */
}
.timeline::after {
  content: '';
  position: absolute;
  left: 15px;
  top: 0;
  width: 3px;
  height: 20px;
  background: var(--crystal-gradient);
  border-radius: 2px;
  filter: blur(3px);
  animation: timeline-flow 3s ease-in-out infinite;
}
@keyframes timeline-flow {
  0% { top: 0; opacity: 1; }
  100% { top: 100%; opacity: 0; }
}
```

- [ ] **Step 4: Stagger 滚动动画增强**

```js
// ===== Stagger 滚动动画 =====
const staggerObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const parent = entry.target;
      const children = parent.querySelectorAll('.fade-in');
      children.forEach((child, i) => {
        child.style.transitionDelay = (i * 0.08) + 's';
        child.classList.add('visible');
      });
    }
  });
}, { threshold: 0.1 });
// 对 grid/列表容器使用 stagger
document.querySelectorAll('.skills-grid, .projects-grid, .timeline').forEach(el => {
  staggerObserver.observe(el);
});
```

---

### Task 6: Contact 表单升级

**文件:** `index.html`

---

- [ ] **Step 1: 输入框聚焦光晕动画**

```css
.contact-form input,
.contact-form textarea {
  position: relative;
  transition: border-color 0.4s, box-shadow 0.4s, background 0.4s;
}

.contact-form input:focus,
.contact-form textarea:focus {
  border-color: var(--primary);
  box-shadow:
    0 0 0 3px rgba(168, 85, 247, 0.12),
    0 0 20px rgba(168, 85, 247, 0.08);
  background: var(--bg-surface-hover);
}

/* 聚焦时底部渐变线 */
.contact-form .input-wrap {
  position: relative;
}
.contact-form .input-wrap::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0;
  width: 0; height: 2px;
  background: var(--crystal-gradient);
  border-radius: 1px;
  transition: width 0.4s ease;
}
.contact-form .input-wrap:focus-within::after {
  width: 100%;
}
```

然后在表单中给每个 input/textarea 包一层 `<div class="input-wrap">`。

- [ ] **Step 2: 提交按钮加载 + 成功反馈**

修改表单提交处理：

```js
// ===== 联系表单提交 =====
form.addEventListener('submit', (e) => {
  e.preventDefault();
  const btn = form.querySelector('button[type="submit"]');
  const originalText = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = '⏳ 发送中...';

  setTimeout(() => {
    // 成功反馈
    btn.innerHTML = '✅ 已发送！';
    showToast('🎉 感谢你的留言！我会尽快回复。');
    form.reset();

    // 可选: 添加 confetti 效果
    createConfetti();

    setTimeout(() => {
      btn.disabled = false;
      btn.innerHTML = originalText;
    }, 2000);
  }, 1200); // 模拟发送延迟
});
```

- [ ] **Step 3: Confetti 庆祝效果**

```js
// ===== Confetti =====
function createConfetti() {
  const colors = ['#a855f7', '#ec4899', '#fbbf24', '#4fc3ff', '#8a6bff'];
  for (let i = 0; i < 30; i++) {
    const el = document.createElement('div');
    el.style.cssText = `
      position: fixed; z-index: 10000; pointer-events: none;
      width: ${Math.random() * 8 + 4}px; height: ${Math.random() * 8 + 4}px;
      background: ${colors[Math.floor(Math.random() * colors.length)]};
      border-radius: ${Math.random() > 0.5 ? '50%' : '2px'};
      left: ${Math.random() * 100}vw;
      top: -10px;
      opacity: 1;
      transition: all ${Math.random() * 2 + 1}s cubic-bezier(0.22, 1, 0.36, 1);
    `;
    document.body.appendChild(el);
    requestAnimationFrame(() => {
      el.style.transform = `translateY(${window.innerHeight + 50}px) rotate(${Math.random() * 720}deg)`;
      el.style.left = (parseFloat(el.style.left) + (Math.random() - 0.5) * 20) + 'vw';
      el.style.opacity = '0';
    });
    setTimeout(() => el.remove(), 4000);
  }
}
```

---

### Task 7: 项目详情页统一升级

**文件:** `project-ai.html`, `project-dashboard.html`, `project-ecommerce.html`

---

- [ ] **Step 1: 添加顶部阅读进度条**

在每个 project-*.html 的 `<body>` 开头添加：

```html
<div class="reading-progress" id="readingProgress"></div>
```

CSS:
```css
.reading-progress {
  position: fixed;
  top: 0; left: 0;
  height: 2px;
  background: linear-gradient(90deg, #a855f7, #ec4899);
  width: 0%;
  z-index: 9999;
  transition: width 0.1s linear;
}
```

JS:
```js
window.addEventListener('scroll', () => {
  const h = document.documentElement.scrollHeight - window.innerHeight;
  document.getElementById('readingProgress').style.width = (window.scrollY / h * 100) + '%';
});
```

- [ ] **Step 2: Shimmer 骨架屏动画**

将 `.screenshot` 的 CSS 替换为：

```css
.screenshot {
  /* 保留原有尺寸和边框 */
  position: relative;
  overflow: hidden;
}
.screenshot::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255,255,255,0.03) 50%,
    transparent 100%
  );
  animation: shimmer 2s ease-in-out infinite;
}
@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}
```

- [ ] **Step 3: 返回按钮悬停动画**

```css
.back-btn {
  transition: color 0.4s, gap 0.3s;
}
.back-btn:hover {
  gap: 12px;
}
```

将返回按钮的 HTML 改为：
```html
<a href="index.html" class="back-btn" style="display:inline-flex;align-items:center;gap:8px;">← 返回主页</a>
```

- [ ] **Step 4: 内容滚动渐入 + stagger**

在每个 project-*.html 中添加 IntersectionObserver：

```js
// ===== 滚动渐入 =====
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('.project-content > *').forEach((el, i) => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = `opacity 0.6s ease ${i * 0.08}s, transform 0.6s ease ${i * 0.08}s`;
  observer.observe(el);
});
```

---

### Task 8: Weekly OS 产品页专项升级

**文件:** `project-weekly-os.html`

---

- [ ] **Step 1: 价格标签闪烁发光 + hover 放大**

```css
.product-hero .price-tag {
  animation: price-glow 2.5s ease-in-out infinite;
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.4s;
}
.product-hero .price-tag:hover {
  transform: scale(1.08);
  box-shadow: 0 8px 40px rgba(168,85,247,0.5);
}
@keyframes price-glow {
  0%, 100% { box-shadow: 0 4px 24px rgba(168,85,247,0.3); }
  50% { box-shadow: 0 4px 40px rgba(168,85,247,0.5), 0 0 60px rgba(168,85,247,0.2); }
}
```

- [ ] **Step 2: CTA 区域彩虹光晕渐变动画**

```css
.cta-section {
  position: relative;
  overflow: hidden;
}
.cta-section::before {
  content: '';
  position: absolute;
  top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: conic-gradient(
    from 0deg,
    transparent 0deg,
    rgba(168,85,247,0.03) 60deg,
    rgba(79,195,255,0.03) 120deg,
    rgba(251,191,36,0.03) 180deg,
    rgba(236,73,153,0.03) 240deg,
    transparent 300deg
  );
  animation: cta-rotate 10s linear infinite;
  pointer-events: none;
}
@keyframes cta-rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
```

- [ ] **Step 3: Social Proof 数字跳动**

在价格标签附近添加：

```html
<div class="social-proof">
  <span class="sp-count" id="buyerCount">128</span>
  <span class="sp-label">人已拥有 · 好评率 97%</span>
</div>
```

CSS:
```css
.social-proof {
  margin-top: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 0.9rem;
  color: var(--text-muted);
}
.social-proof .sp-count {
  font-size: 1.3rem;
  font-weight: 700;
  background: var(--crystal-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

JS 数字跳动:
```js
// ===== Social Proof 数字跳动 =====
function animateCounter(el, target) {
  let current = 0;
  const step = Math.ceil(target / 40);
  const interval = setInterval(() => {
    current += step;
    if (current >= target) {
      current = target;
      clearInterval(interval);
    }
    el.textContent = current;
  }, 30);
}
const countObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !entry.target.dataset.animated) {
      entry.target.dataset.animated = 'true';
      animateCounter(entry.target, 128);
    }
  });
}, { threshold: 0.5 });
const countEl = document.getElementById('buyerCount');
if (countEl) countObserver.observe(countEl);
```

- [ ] **Step 4: 弹窗 spring 弹出动画**

```css
.modal-overlay {
  opacity: 0;
  transition: opacity 0.3s ease;
}
.modal-overlay[style*="flex"] {
  opacity: 1;
}
.modal-box {
  transform: scale(0.85) translateY(20px);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.modal-overlay[style*="flex"] .modal-box {
  transform: scale(1) translateY(0);
}
```

同时修改 JS 中的弹窗打开函数：

```js
function openXHS() {
  const modal = document.getElementById('xhsModal');
  modal.style.display = 'flex';
  requestAnimationFrame(() => { modal.style.opacity = '1'; });
}
function closeXHSModal() {
  const modal = document.getElementById('xhsModal');
  modal.style.opacity = '0';
  setTimeout(() => { modal.style.display = 'none'; }, 300);
}
// 同理修改微信弹窗
```

---

### Task 9: 响应式收尾检查

**文件:** 全部 HTML

---

- [ ] **Step 1: 在全部页面添加响应式降级规则**

在现有 `@media` 基础上补充：

```css
/* 平板: 关闭 3D tilt，降粒子密度 */
@media (max-width: 768px) {
  .project-card { transform: none !important; }
  .project-card::after { display: none; }
}

/* 手机: 关闭 Canvas 粒子 */
@media (max-width: 480px) {
  #particles-canvas { display: none; }
  .glow-orbe { opacity: 0.15; }
  .social-proof { flex-direction: column; gap: 4px; }
}
```

---

## 执行顺序说明

| 任务 | 前置依赖 | 可独立执行 |
|------|---------|-----------|
| Task 1: 设计系统 & 玻璃基础 | 无 | ✅ |
| Task 2: 导航 + 进度条 | Task 1 | ✅ |
| Task 3: Hero 3D 晶体 | Task 1 | ✅ |
| Task 4: 磁性按钮 + 视差 | Task 1 | ✅ |
| Task 5: 3D Tilt + 微交互 | Task 1 | ✅ |
| Task 6: 表单升级 | Task 1 | ✅ |
| Task 7: 项目详情页 | Task 1 | ✅ (独立于 index) |
| Task 8: Weekly OS 页 | Task 1 | ✅ (独立于 index) |
| Task 9: 响应式收尾 | Task 1-8 完成后 | ❌ 需最后执行 |

Task 1 是唯一前置依赖。Task 2~6 在 index.html 中互不冲突。Task 7~8 在独立文件中，完全可并行。
