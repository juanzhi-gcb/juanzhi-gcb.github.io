"""Build beautified index.html and extended.html"""
import markdown, re

with open('软件实践报告.md', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'^---\n.*?\n---\n', '', content, count=1, flags=re.DOTALL)
style_end = content.find('</style>') + len('</style>')
main_start = content.find('<div class="main-content">')
main_end = content.rfind('</div>    <!-- end .main-content -->') + len('</div>    <!-- end .main-content -->')

nav_html = content[style_end:main_start]
after_html = content[main_end:]
main_block = content[main_start:main_end]
inner_html = markdown.markdown(main_block[main_block.find('>')+1:main_block.rfind('</div>')],
                                extensions=['extra', 'fenced_code', 'tables'])

# ============= NEW MODERN CSS =============
new_css = '''<style>
  :root {
    --bg: #fafbfc; --surface: #ffffff; --surface2: #f0f2f5;
    --text: #1a1d23; --text2: #5a5f6b; --text3: #9095a1;
    --accent: #6366f1; --accent2: #8b5cf6; --accent-light: #eef2ff;
    --border: #e5e7eb; --shadow: 0 1px 3px rgba(0,0,0,.06);
    --shadow-lg: 0 8px 32px rgba(0,0,0,.08);
    --radius: 12px; --radius-sm: 8px;
    --sidebar-w: 270px; --transition: .25s cubic-bezier(.4,0,.2,1);
  }
  .dark {
    --bg: #0f1117; --surface: #1a1d27; --surface2: #232733;
    --text: #e8eaef; --text2: #a0a5b2; --text3: #6b7080;
    --accent-light: #1e2040; --border: #2a2d3a;
    --shadow: 0 1px 3px rgba(0,0,0,.3); --shadow-lg: 0 8px 32px rgba(0,0,0,.4);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; font-size: 15px; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", "Segoe UI", sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.75;
    transition: background var(--transition), color var(--transition);
    overflow-x: hidden;
  }
  /* Progress Bar */
  #progress-bar {
    position: fixed; top: 0; left: 0; height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    z-index: 10000; transition: width .1s linear;
  }
  /* Theme Toggle */
  #theme-toggle {
    position: fixed; top: 16px; right: 24px; z-index: 10001;
    width: 44px; height: 44px; border-radius: 50%; border: 2px solid var(--border);
    background: var(--surface); color: var(--text); cursor: pointer;
    font-size: 1.2em; display: flex; align-items: center; justify-content: center;
    box-shadow: var(--shadow-lg); transition: all var(--transition);
  }
  #theme-toggle:hover { transform: scale(1.1); border-color: var(--accent); }
  /* Sidebar */
  .sidebar {
    position: fixed; top: 0; left: 0; width: var(--sidebar-w); height: 100vh;
    background: var(--surface); border-right: 1px solid var(--border);
    overflow-y: auto; z-index: 1000; font-size: .88rem;
    box-shadow: var(--shadow-lg); transition: background var(--transition);
  }
  .sidebar-header {
    padding: 28px 20px; border-bottom: 1px solid var(--border);
    position: sticky; top: 0; background: var(--surface); z-index: 10;
    backdrop-filter: blur(12px);
  }
  .sidebar-header h2 {
    font-size: 1.05rem; font-weight: 700; color: var(--text);
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }
  .sidebar-header .subtitle { font-size: .75rem; color: var(--text3); margin-top: 2px; }
  .sidebar-nav details { border-bottom: 1px solid var(--border); }
  .sidebar-nav summary {
    padding: 10px 20px; cursor: pointer; font-weight: 600;
    color: var(--text); transition: all var(--transition); list-style: none;
    font-size: .84rem;
  }
  .sidebar-nav summary::-webkit-details-marker { display: none; }
  .sidebar-nav summary::before {
    content: '▸'; display: inline-block; width: 14px; font-size: .65rem;
    transition: transform .2s; margin-right: 4px;
  }
  .sidebar-nav details[open] summary::before { transform: rotate(90deg); }
  .sidebar-nav summary:hover { background: var(--surface2); color: var(--accent); }
  .sidebar-nav details > a {
    display: block; padding: 7px 20px 7px 38px; color: var(--text2);
    text-decoration: none; font-size: .8rem; transition: all .2s;
    border-left: 3px solid transparent;
  }
  .sidebar-nav details > a:hover, .sidebar-nav details > a.active {
    background: var(--accent-light); color: var(--accent);
    border-left-color: var(--accent);
  }
  .sidebar-nav > a {
    display: block; padding: 10px 20px; color: var(--text); text-decoration: none;
    font-weight: 600; font-size: .88rem; transition: all .2s;
  }
  .sidebar-nav > a:hover { background: var(--surface2); color: var(--accent); }
  /* Main */
  .main-content {
    margin-left: var(--sidebar-w); max-width: 920px;
    padding: 48px 60px 64px; transition: background var(--transition);
  }
  .main-content h1 {
    font-size: 2.2em; font-weight: 800; margin-bottom: 12px; color: var(--text);
    border-bottom: 4px solid transparent;
    border-image: linear-gradient(90deg, var(--accent), var(--accent2)) 1;
    padding-bottom: 16px; letter-spacing: -.01em; line-height: 1.25;
  }
  .main-content h2 {
    font-size: 1.5em; font-weight: 700; margin-top: 56px; margin-bottom: 20px;
    color: var(--text); border-left: 4px solid var(--accent);
    padding: 8px 0 8px 16px;
    background: linear-gradient(90deg, var(--accent-light) 0%, transparent 100%);
    border-radius: 0 6px 6px 0;
  }
  .main-content h3 {
    font-size: 1.15em; font-weight: 600; margin-top: 36px; margin-bottom: 14px;
    color: var(--text); padding-bottom: 8px;
    border-bottom: 2px solid var(--border);
  }
  .main-content h4 {
    font-size: 1.02em; font-weight: 600; margin-top: 24px; margin-bottom: 10px;
    color: var(--text);
  }
  .main-content p { margin-bottom: 14px; }
  .main-content strong { font-weight: 700; color: var(--accent); }
  .main-content a { color: var(--accent); text-decoration: none; font-weight: 500; }
  .main-content a:hover { text-decoration: underline; }
  .main-content blockquote {
    border-left: 4px solid var(--accent); padding: 16px 22px; margin: 20px 0;
    background: var(--surface); border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    color: var(--text2); font-size: .92em; box-shadow: var(--shadow);
  }
  /* Tables */
  .main-content table {
    width: 100%; border-collapse: collapse; margin: 20px 0; font-size: .9em;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow);
  }
  .main-content th {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    color: #fff; padding: 12px 16px; text-align: left; font-weight: 700;
    font-size: .82em; letter-spacing: .02em; text-transform: uppercase;
  }
  .main-content td { padding: 11px 16px; border-bottom: 1px solid var(--border); }
  .main-content tr:last-child td { border-bottom: none; }
  .main-content tr:nth-child(even) td { background: var(--surface2); }
  .main-content tr:hover td { background: var(--accent-light); transition: background .15s; }
  /* Images */
  .main-content img {
    max-width: 100%; border-radius: var(--radius); border: 1px solid var(--border);
    margin: 14px 0; box-shadow: var(--shadow-lg); cursor: zoom-in;
    transition: transform var(--transition), box-shadow var(--transition);
  }
  .main-content img:hover { transform: scale(1.01); box-shadow: 0 12px 40px rgba(0,0,0,.15); }
  .img-caption {
    text-align: center; font-size: .82em; color: var(--text3);
    margin-top: -8px; margin-bottom: 20px; font-style: italic;
  }
  /* Lightbox */
  .lightbox {
    display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,.92); z-index: 20000; cursor: zoom-out;
    align-items: center; justify-content: center;
  }
  .lightbox.active { display: flex; }
  .lightbox img { max-width: 92vw; max-height: 92vh; border-radius: 8px; cursor: default; }
  /* Code */
  .main-content code {
    background: var(--surface2); padding: 3px 8px; border-radius: 5px;
    font-family: "Cascadia Code", "Fira Code", "JetBrains Mono", "Consolas", monospace;
    font-size: .85em; color: #e0576d; border: 1px solid var(--border);
  }
  .main-content pre {
    background: #1a1d27; color: #e2e8f0; padding: 20px 24px;
    border-radius: var(--radius); overflow-x: auto; margin: 20px 0;
    font-size: .85em; font-family: "Cascadia Code", "Fira Code", "JetBrains Mono", "Consolas", monospace;
    line-height: 1.7; box-shadow: var(--shadow-lg); border: 1px solid var(--border);
    position: relative;
  }
  .main-content pre::before {
    content: attr(data-lang); position: absolute; top: 8px; right: 16px;
    font-size: .7em; color: #6366f1; text-transform: uppercase; font-weight: 600;
    letter-spacing: .05em;
  }
  .main-content pre code { background: none; color: inherit; padding: 0; font-size: inherit; border: none; }
  /* Back to top */
  #back-top {
    position: fixed; bottom: 32px; right: 32px; width: 48px; height: 48px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    color: #fff; border: none; border-radius: 50%; cursor: pointer;
    font-size: 1.3em; font-weight: 700; z-index: 9999;
    box-shadow: 0 4px 20px rgba(99,102,241,.45);
    transition: all var(--transition); opacity: 0; transform: translateY(20px);
    pointer-events: none;
  }
  #back-top.visible { opacity: 1; transform: translateY(0); pointer-events: auto; }
  #back-top:hover { transform: translateY(-3px) scale(1.08); box-shadow: 0 8px 28px rgba(99,102,241,.55); }
  /* Animations */
  .fade-in {
    opacity: 0; transform: translateY(20px);
    transition: opacity .6s ease-out, transform .6s ease-out;
  }
  .fade-in.visible { opacity: 1; transform: translateY(0); }
  /* Responsive */
  @media (max-width: 900px) {
    .sidebar { display: none; }
    .main-content { margin-left: 0; padding: 24px 20px; }
    #theme-toggle { top: 10px; right: 10px; }
  }
  @media print {
    .sidebar, #back-top, #theme-toggle, #progress-bar, .lightbox { display: none; }
    .main-content { margin-left: 0; padding: 0; max-width: 100%; }
    h2 { page-break-before: always; }
  }
  /* Extended Learning Page */
  .ext-page { background: var(--bg); min-height: 100vh; }
  .ext-header {
    text-align: center; padding: 80px 20px 40px;
    background: linear-gradient(135deg, var(--accent-light), var(--surface));
  }
  .ext-header h1 {
    font-size: 2.8em; font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
  }
  .ext-header p { color: var(--text2); font-size: 1.1em; }
  .ext-container { max-width: 1100px; margin: 0 auto; padding: 40px 24px 80px; }
  .ext-section { margin-bottom: 48px; }
  .ext-section h2 {
    font-size: 1.5em; font-weight: 700; color: var(--text);
    margin-bottom: 20px; padding-bottom: 8px;
    border-bottom: 3px solid transparent;
    border-image: linear-gradient(90deg, var(--accent), var(--accent2)) 1;
  }
  .ext-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }
  .ext-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 24px; box-shadow: var(--shadow);
    transition: all var(--transition); cursor: pointer; text-decoration: none;
    display: block; color: inherit;
  }
  .ext-card:hover {
    transform: translateY(-3px); box-shadow: var(--shadow-lg);
    border-color: var(--accent);
  }
  .ext-card .tag {
    display: inline-block; padding: 3px 12px; border-radius: 20px;
    font-size: .75em; font-weight: 600;
    background: var(--accent-light); color: var(--accent);
    margin-bottom: 10px;
  }
  .ext-card h3 { font-size: 1.05em; font-weight: 700; margin-bottom: 8px; color: var(--text); }
  .ext-card p { font-size: .88em; color: var(--text2); line-height: 1.6; }
  .ext-card .meta { margin-top: 12px; font-size: .78em; color: var(--text3); }
  .ext-nav {
    position: sticky; top: 0; z-index: 100; padding: 16px 0;
    background: var(--bg); border-bottom: 1px solid var(--border);
    backdrop-filter: blur(12px);
  }
  .ext-nav a {
    display: inline-block; padding: 8px 16px; margin: 0 4px;
    color: var(--text2); text-decoration: none; font-size: .88em;
    border-radius: 20px; transition: all .2s;
  }
  .ext-nav a:hover, .ext-nav a:focus { background: var(--accent-light); color: var(--accent); }
  .ext-back { margin-bottom: 20px; }
  .ext-back a { color: var(--accent); text-decoration: none; font-weight: 600; font-size: .9em; }
</style>'''

# ============= BUILD index.html =============
index_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《软件开发工具实践》实验报告</title>
{new_css}
</head>
<body>
<div id="progress-bar"></div>
<button id="theme-toggle" title="切换主题" onclick="toggleTheme()">🌓</button>
<div class="lightbox" id="lightbox" onclick="closeLightbox()"><img id="lightbox-img" src="" alt=""></div>

{nav_html}

<div class="main-content">
<h1>《软件开发工具实践》实验报告</h1>
{inner_html}
</div>

<button id="back-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" title="返回顶部">↑</button>

<script>
// Theme toggle
function toggleTheme() {{
  document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
}}
if (localStorage.getItem('theme') === 'dark') document.documentElement.classList.add('dark');

// Progress bar
window.addEventListener('scroll', () => {{
  const h = document.documentElement;
  document.getElementById('progress-bar').style.width = (h.scrollTop / (h.scrollHeight - h.clientHeight) * 100) + '%';
}});

// Back to top
window.addEventListener('scroll', () => {{
  document.getElementById('back-top').classList.toggle('visible', window.scrollY > 400);
}});

// Image lightbox
document.querySelectorAll('.main-content img').forEach(img => {{
  img.addEventListener('click', () => {{
    document.getElementById('lightbox-img').src = img.src;
    document.getElementById('lightbox').classList.add('active');
  }});
}});
function closeLightbox() {{ document.getElementById('lightbox').classList.remove('active'); }}

// Sidebar active tracking
const sections = document.querySelectorAll('h2[id], h3[id]');
const links = document.querySelectorAll('.sidebar-nav a[href^=\"#\"]');
window.addEventListener('scroll', () => {{
  let current = '';
  sections.forEach(s => {{ if (window.scrollY >= s.offsetTop - 100) current = s.id; }});
  links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + current));
}});

// Fade-in animations
const observer = new IntersectionObserver(entries => {{
  entries.forEach(e => {{ if (e.isIntersecting) e.target.classList.add('visible'); }});
}}, {{ threshold: 0.1 }});
document.querySelectorAll('h2, h3, img, pre, table, blockquote').forEach(el => {{
  el.classList.add('fade-in'); observer.observe(el);
}});

// Add data-lang to code blocks
document.querySelectorAll('pre code[class*=\"language-\"]').forEach(code => {{
  const lang = code.className.match(/language-(\\w+)/);
  if (lang) code.parentElement.setAttribute('data-lang', lang[1]);
}});
</script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print(f'index.html written ({len(index_html)} chars)')

# ============= BUILD extended.html =============
extended_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>扩展学习 - 软件开发工具实践</title>
{new_css}
</head>
<body class="ext-page">
<div id="progress-bar"></div>
<button id="theme-toggle" title="切换主题" onclick="toggleTheme()">🌓</button>

<div class="ext-header">
  <h1>📚 扩展学习资源</h1>
  <p>Bilibili 精选教程 · 持续更新</p>
</div>

<div class="ext-nav" style="text-align:center">
  <a href="#nodejs">Node.js</a>
  <a href="#vscode">VS Code</a>
  <a href="#hexo">Hexo & GitHub Pages</a>
  <a href="#git">Git 版本控制</a>
  <a href="#linux">Linux 命令行</a>
  <a href="#ssh">SSH 远程管理</a>
  <a href="#nginx">Nginx</a>
  <a href="#cicd">CI/CD</a>
</div>

<div class="ext-container">

<div class="ext-back"><a href="index.html">← 返回实验报告</a></div>

<div class="ext-section" id="nodejs">
<h2>🟢 Node.js & npm</h2>
<div class="ext-grid">
  <a class="ext-card" href="https://www.bilibili.com/video/BV1GCoBY7ES3/" target="_blank">
    <span class="tag">入门首选</span>
    <h3>NodeJS简明教程 (2025新版)</h3>
    <p>65集完整课程，从安装到Express+数据库+JWT+实战项目</p>
    <span class="meta">▶ 10.1万播放 · BV1GCoBY7ES3</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1QT421Y7PK/" target="_blank">
    <span class="tag">快速入门</span>
    <h3>1小时学会Node.js (ESM规范)</h3>
    <p>短小精悍，核心模块fs/path/http/crypto一网打尽</p>
    <span class="meta">▶ BV1QT421Y7PK</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1VktQz9EY7/" target="_blank">
    <span class="tag">体系课程</span>
    <h3>Node.js全套入门教程</h3>
    <p>含ES6模块化+npm+Express+Webpack+Promise实战</p>
    <span class="meta">▶ BV1VktQz9EY7</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1W9mTBjELb/" target="_blank">
    <span class="tag">进阶提升</span>
    <h3>Node.js从基础到实战</h3>
    <p>Express+Koa双框架，JWT/Session认证，MySQL操作</p>
    <span class="meta">▶ BV1W9mTBjELb</span>
  </a>
</div>
</div>

<div class="ext-section" id="vscode">
<h2>🔵 VS Code 高效使用</h2>
<div class="ext-grid">
  <a class="ext-card" href="https://www.bilibili.com/video/BV1jW42197jN/" target="_blank">
    <span class="tag">效率神器</span>
    <h3>VSCode 你真的会用么？</h3>
    <p>15分钟干货，覆盖大量效率技巧，32.5万播放</p>
    <span class="meta">▶ 32.5万播放 · BV1jW42197jN</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1ka4y1j7ZS/" target="_blank">
    <span class="tag">极速入门</span>
    <h3>VSCode 五分钟上手教程</h3>
    <p>无一句废话，适合零基础快速上手</p>
    <span class="meta">▶ 49.2万播放 · BV1ka4y1j7ZS</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1jY4y1U7Yv/" target="_blank">
    <span class="tag">配置优化</span>
    <h3>VSCode 优化体验篇</h3>
    <p>推荐设置+插件推荐，打造舒适开发环境</p>
    <span class="meta">▶ 28.7万播放 · BV1jY4y1U7Yv</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1hV411A7xv/" target="_blank">
    <span class="tag">Git整合</span>
    <h3>VSCode+Git 最佳代码管理</h3>
    <p>39分钟系统讲解VSCode中的Git集成工作流</p>
    <span class="meta">▶ 14万播放 · BV1hV411A7xv</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1tv411r7ID/" target="_blank">
    <span class="tag">完整系列</span>
    <h3>VS Code 零基础教程</h3>
    <p>2小时40分，持续更新，43万播放量</p>
    <span class="meta">▶ 43万播放 · BV1tv411r7ID</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1Xq4y1Z7aq/" target="_blank">
    <span class="tag">插件推荐</span>
    <h3>VSCode 真香插件</h3>
    <p>前端效率神器推荐，3分钟快速了解</p>
    <span class="meta">▶ 28.1万播放 · BV1Xq4y1Z7aq</span>
  </a>
</div>
</div>

<div class="ext-section" id="hexo">
<h2>🟣 Hexo + GitHub Pages 博客搭建</h2>
<div class="ext-grid">
  <a class="ext-card" href="https://www.bilibili.com/video/BV1fW4y1t7WJ/" target="_blank">
    <span class="tag">进阶优化</span>
    <h3>Hexo博客从入门到入土完全优化</h3>
    <p>23集涵盖Butterfly主题、SEO、PWA、评论系统、看板娘</p>
    <span class="meta">▶ 15万播放 · BV1fW4y1t7WJ</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1Yb411a7ty/" target="_blank">
    <span class="tag">经典入门</span>
    <h3>CodeSheep Hexo搭建教程</h3>
    <p>经典教程，零基础友好，手把手教你搭建个人博客</p>
    <span class="meta">▶ BV1Yb411a7ty</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1Ko4y1S7mv/" target="_blank">
    <span class="tag">主题美化</span>
    <h3>Butterfly主题配置教程</h3>
    <p>专门的Butterfly主题美化教学，打造高颜值博客</p>
    <span class="meta">▶ BV1Ko4y1S7mv</span>
  </a>
</div>
</div>

<div class="ext-section" id="git">
<h2>🟠 Git 版本控制</h2>
<div class="ext-grid">
  <a class="ext-card" href="https://www.bilibili.com/video/BV1HM4y1G7Yj/" target="_blank">
    <span class="tag">首推</span>
    <h3>GeekHour 一小时Git教程</h3>
    <p>动画生动、概念清晰、节奏紧凑，79.5万播放</p>
    <span class="meta">▶ 79.5万播放 · BV1HM4y1G7Yj</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV17eewzqEPv/" target="_blank">
    <span class="tag">入门到精通</span>
    <h3>Git入门到精通</h3>
    <p>从零掌握版本控制，系统全面</p>
    <span class="meta">▶ BV17eewzqEPv</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1x7411H7wa/" target="_blank">
    <span class="tag">名校课程</span>
    <h3>MIT《消失的学期》Git部分</h3>
    <p>世界顶尖名校公开课，深入理解Git设计哲学</p>
    <span class="meta">▶ BV1x7411H7wa</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1ym9hBFEUf/" target="_blank">
    <span class="tag">2026最新</span>
    <h3>零基础小白自学Git</h3>
    <p>全功能精讲，让你少走90%弯路</p>
    <span class="meta">▶ BV1ym9hBFEUf</span>
  </a>
</div>
</div>

<div class="ext-section" id="linux">
<h2>🐧 Linux 命令行</h2>
<div class="ext-grid">
  <a class="ext-card" href="https://www.bilibili.com/video/BV1ES1nBzEfp/" target="_blank">
    <span class="tag">2025最新</span>
    <h3>Linux操作系统教程(完整版)</h3>
    <p>19章覆盖安装、目录、用户、权限、vim、环境变量等</p>
    <span class="meta">▶ 2025新版 · BV1ES1nBzEfp</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1fe28BeEY2/" target="_blank">
    <span class="tag">就业导向</span>
    <h3>Linux从入门到精通必学</h3>
    <p>通俗易懂，2025最新版，学完即可就业</p>
    <span class="meta">▶ BV1fe28BeEY2</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1FuvpBJEcv/" target="_blank">
    <span class="tag">快速入门</span>
    <h3>全31集 一口气学完Linux</h3>
    <p>全程高能无废话，Ubuntu系统+文件操作+权限+远程登录</p>
    <span class="meta">▶ BV1FuvpBJEcv</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1S89uYQEoc/" target="_blank">
    <span class="tag">全面精通</span>
    <h3>Linux从入门到精通(72集)</h3>
    <p>含环境部署、Shell脚本、云平台实践、大数据集群</p>
    <span class="meta">▶ BV1S89uYQEoc</span>
  </a>
</div>
</div>

<div class="ext-section" id="ssh">
<h2>🔐 SSH 远程管理 & 文件传输</h2>
<div class="ext-grid">
  <a class="ext-card" href="https://www.bilibili.com/video/BV1ES1nBzEfp/" target="_blank">
    <span class="tag">Linux综合</span>
    <h3>Linux教程含SSH章节</h3>
    <p>上述Linux教程中均包含SSH远程登录和SCP传输内容</p>
    <span class="meta">▶ 参见Linux分类</span>
  </a>
</div>
</div>

<div class="ext-section" id="nginx">
<h2>🌐 Nginx Web服务器</h2>
<div class="ext-grid">
  <a class="ext-card" href="https://www.bilibili.com/video/BV1zJ411w7SV/" target="_blank">
    <span class="tag">经典推荐</span>
    <h3>尚硅谷Nginx教程由浅入深</h3>
    <p>100万+播放，涵盖基本概念、安装、配置、原理四大模块</p>
    <span class="meta">▶ 100万+ · BV1zJ411w7SV</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV18fAAznEnz/" target="_blank">
    <span class="tag">小白友好</span>
    <h3>Nginx零基础到精通(80集)</h3>
    <p>静态资源、Gzip、缓存、防盗链、Rewrite、反向代理、SSL</p>
    <span class="meta">▶ 80集 · BV18fAAznEnz</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1eo4y1B75E/" target="_blank">
    <span class="tag">快速上手</span>
    <h3>3天从小白变高手</h3>
    <p>从TCP/HTTP协议基础讲起，循序渐进</p>
    <span class="meta">▶ BV1eo4y1B75E</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1ptDZYqEiB/" target="_blank">
    <span class="tag">实战导向</span>
    <h3>Linux云计算之Nginx(51集)</h3>
    <p>含购买域名/VPS/SSL证书/Discuz安装等线上实战</p>
    <span class="meta">▶ 51集 · BV1ptDZYqEiB</span>
  </a>
</div>
</div>

<div class="ext-section" id="cicd">
<h2>⚡ GitHub Actions CI/CD</h2>
<div class="ext-grid">
  <a class="ext-card" href="https://www.bilibili.com/video/BV1jNSEBiE6D/" target="_blank">
    <span class="tag">必看</span>
    <h3>为什么大佬都在用GitHub Actions？</h3>
    <p>深入理解CI/CD自动化部署的核心价值</p>
    <span class="meta">▶ BV1jNSEBiE6D</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1j2HazoEZv/" target="_blank">
    <span class="tag">实用技巧</span>
    <h3>一行命令触发GitHub Actions</h3>
    <p>自动化工作流程，提升效率</p>
    <span class="meta">▶ BV1j2HazoEZv</span>
  </a>
  <a class="ext-card" href="https://www.bilibili.com/video/BV1FxpEzZEHU/" target="_blank">
    <span class="tag">企业实践</span>
    <h3>Gitlab CI/CD开源安全流水线</h3>
    <p>企业级CI/CD实践方案对比</p>
    <span class="meta">▶ BV1FxpEzZEHU</span>
  </a>
  <a class="ext-card" href="https://opencamp.cn/Git/camp/2025/stage/2" target="_blank">
    <span class="tag">系统课程</span>
    <h3>Learning Git Camp 2025</h3>
    <p>专业阶段：GitHub Actions CI/CD系统教学</p>
    <span class="meta">▶ opencamp.cn</span>
  </a>
</div>
</div>

</div>

<button id="back-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" title="返回顶部">↑</button>

<script>
function toggleTheme() {{
  document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
}}
if (localStorage.getItem('theme') === 'dark') document.documentElement.classList.add('dark');

window.addEventListener('scroll', () => {{
  const h = document.documentElement;
  document.getElementById('progress-bar').style.width = (h.scrollTop / (h.scrollHeight - h.clientHeight) * 100) + '%';
  document.getElementById('back-top').classList.toggle('visible', window.scrollY > 400);
}});

const observer = new IntersectionObserver(entries => {{
  entries.forEach(e => {{ if (e.isIntersecting) e.target.classList.add('visible'); }});
}}, {{ threshold: 0.1 }});
document.querySelectorAll('.ext-card').forEach(el => {{ el.classList.add('fade-in'); observer.observe(el); }});
</script>
</body>
</html>'''

with open('extended.html', 'w', encoding='utf-8') as f:
    f.write(extended_html)
print(f'extended.html written ({len(extended_html)} chars)')
print('DONE')
