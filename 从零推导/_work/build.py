#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 src/<doc>/*.html 章节片段拼成单文件交互式 HTML，KaTeX（含字体）全部内联。

用法：python3 _work/build.py
"""
import base64, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
SRC = os.path.join(HERE, "src")

DOCS = [
    {
        "key": "dg",
        "file": "网格上的微分几何.html",
        "title": "网格上的微分几何",
        "subtitle": "从一条边的长度，推到余切权重、角度亏欠和 Gauss-Bonnet",
        "parts": [
            ("根", ["dg0", "dg1"]),
            ("工具", ["dg2", "dg3"]),
            ("主干", ["dg4", "dg5", "dg6"]),
            ("应用", ["dg7"]),
        ],
        "chapters": [
            ("dg0", "第 0 章 开场：三个要推的公式", "从一条边的长度推到余切权重、曲率与 Gauss-Bonnet"),
            ("dg1", "第 1 章 预备：向量、点积、叉积与余切", "只用坐标和乘加，就能算出夹角与面积"),
            ("dg2", "第 2 章 一个三角形里能算出什么", "边长、夹角、面积，以及绕一圈的角度和"),
            ("dg3", "第 3 章 分片线性函数的梯度", "在一个三角形上，函数的斜度是一个常向量"),
            ("dg4", "第 4 章 从能量到余切权重", "为什么权重是 (cot α + cot β)/2，而不是随便什么数"),
            ("dg5", "第 5 章 余切权重的三个后果", "钝角为什么给出负权重，混合面积在修什么"),
            ("dg6", "第 6 章 曲率与角度亏欠", "绕一个顶点一圈，角度少了多少就是曲率"),
            ("dg7", "第 7 章 用起来：光顺、参数化与校验", "同一个算子三种用法，以及写完怎么自查"),
        ],
    },
    {
        "key": "grad",
        "file": "梯度域形变.html",
        "title": "梯度域形变",
        "subtitle": "从“保住局部形状”推到 Poisson 方程、Helmholtz 分解和 ARAP",
        "parts": [
            ("根", ["g0"]),
            ("工具", ["g1", "g2"]),
            ("主干", ["g3", "g4", "g5", "g6"]),
            ("收尾", ["g7"]),
        ],
        "chapters": [
            ("g0", "第 0 章 预备：位移、最小二乘、矩阵", "只用到加减乘除和一个“让平方和最小”的想法"),
            ("g1", "第 1 章 什么是“局部形状”", "拉普拉斯坐标：一个顶点比邻居平均高多少"),
            ("g2", "第 2 章 把目标写成方程", "保局部 + 满足约束 = 一个最小二乘问题"),
            ("g3", "第 3 章 为什么不能直接积分", "向量场不一定可积，路径不同结果就不同"),
            ("g4", "第 4 章 Helmholtz 分解与 Poisson", "把不可积的部分切掉，剩下的才解得出"),
            ("g5", "第 5 章 解出来：稀疏系统与数值例", "Cholesky、共轭梯度，以及手算一个 4 顶点例子"),
            ("g6", "第 6 章 ARAP：让局部只旋转不拉伸", "Procrustes 与局部-全局交替，以及它的失败案例"),
            ("g7", "第 7 章 收尾：它和全书其他方法的关系", "与 Poisson 重建、投影动力学共享同一个骨架"),
        ],
    },
]


def font_css():
    css = open(os.path.join(ASSETS, "katex.min.css"), encoding="utf-8").read()

    def fix_block(m):
        block = m.group(0)
        names = sorted(set(re.findall(r"fonts/([A-Za-z0-9_\-]+)\.woff2", block)))
        parts = []
        for n in names:
            fp = os.path.join(ASSETS, "fonts", n + ".woff2")
            if not os.path.exists(fp):
                continue
            b64 = base64.b64encode(open(fp, "rb").read()).decode()
            parts.append('url(data:font/woff2;base64,%s) format("woff2")' % b64)
        if not parts:
            return block
        i = block.find("src:")
        j = block.rfind("}")
        return block[:i] + "src:" + ",".join(parts) + block[j:]

    css = re.sub(r"@font-face\{[^}]*\}", fix_block, css)
    return css


CSS = r"""
:root{--bg:#fbfbf8;--fg:#1f2328;--muted:#6b7280;--line:#e3e3dd;--card:#fff;--accent:#2f6b4f;--accent2:#8a5a2b;--warn:#f2f7ee;--tip:#fff8e8;--blue:#eef4fb}
[data-theme=dark]{--bg:#15171a;--fg:#e8e8e4;--muted:#9aa0a6;--line:#2c3035;--card:#1b1e22;--accent:#7cc4a3;--accent2:#d7a86e;--warn:#1d2620;--tip:#2a2416;--blue:#18222e}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--fg);font-family:-apple-system,"PingFang SC","Microsoft YaHei",system-ui,sans-serif;line-height:1.85;font-size:16px;overflow-wrap:break-word}
a{color:var(--accent);text-decoration:none}
.topbar{position:fixed;top:0;left:0;right:0;height:56px;display:flex;align-items:center;gap:8px;padding:0 10px;background:var(--card);border-bottom:1px solid var(--line);z-index:30}
.topbar button{min-width:44px;min-height:44px;border:1px solid var(--line);background:var(--bg);color:var(--fg);border-radius:10px;font-size:15px;cursor:pointer}
#cur-title{flex:1;font-size:14px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-align:center}
main{max-width:860px;margin:0 auto;padding:70px 16px 80px}
.sidebar{position:fixed;top:0;bottom:0;left:0;width:280px;background:var(--card);border-right:1px solid var(--line);padding:16px;overflow:auto;transform:translateX(-100%);transition:transform .2s;z-index:40}
.sidebar.open{transform:none}
.sidebar h3{margin:6px 0 14px;font-size:14px;color:var(--muted);font-weight:600}
.tree-part{margin:14px 0 6px;font-size:12px;letter-spacing:1px;color:var(--accent2);font-weight:700}
.tree-item{display:block;padding:8px 6px;font-size:14px;color:var(--fg);border-radius:8px}
.tree-item.on{background:var(--warn);font-weight:600}
.chapter{display:none}
.chapter.on{display:block}
.ch-title{font-size:22px;line-height:1.4;margin:6px 0 4px}
.ch-desc{color:var(--muted);font-size:14px;margin:0 0 18px}
.breadcrumb{font-size:12px;color:var(--muted);margin-bottom:6px}
h2{font-size:18px;margin:28px 0 10px;padding-left:10px;border-left:3px solid var(--accent)}
h3{font-size:16px;margin:20px 0 8px}
p{margin:10px 0}
.intuition{background:var(--warn);border-left:4px solid var(--accent);padding:10px 12px;border-radius:0 8px 8px 0;margin:14px 0;font-size:15px}
.tip{background:var(--tip);border-left:4px solid var(--accent2);padding:10px 12px;margin:14px 0;font-size:15px}
.keybox{background:var(--blue);border:1px dashed var(--line);padding:12px;border-radius:8px;margin:16px 0}
.pre{font-size:13px;background:var(--blue);border-left:3px solid var(--accent);padding:8px 10px;margin:10px 0}
.formula{overflow-x:auto;max-width:100%}
details{border:1px solid var(--line);border-radius:10px;padding:8px 12px;margin:12px 0;background:var(--card)}
details>summary{cursor:pointer;font-weight:600;font-size:15px;list-style:none;min-height:32px}
details>summary::-webkit-details-marker{display:none}
details>summary:before{content:"▸ ";color:var(--accent)}
details[open]>summary:before{content:"▾ "}
details .body{padding-top:6px}
.kv{width:100%;border-collapse:collapse;margin:12px 0;font-size:14px}
.kv th,.kv td{border:1px solid var(--line);padding:6px 8px;text-align:left}
.kv th{background:var(--blue)}
code{background:var(--blue);padding:1px 5px;border-radius:4px;font-size:14px}
ol,ul{padding-left:22px}
.chapter-nav{display:flex;gap:10px;justify-content:space-between;margin:34px 0 10px;border-top:1px solid var(--line);padding-top:14px}
.chapter-nav a{padding:10px 12px;border:1px solid var(--line);border-radius:10px;font-size:14px;min-height:44px;display:inline-block}
.chapter-nav .ph{visibility:hidden;border:none}
#totop{position:fixed;right:14px;bottom:18px;width:44px;height:44px;border-radius:50%;border:1px solid var(--line);background:var(--card);color:var(--fg);cursor:pointer;z-index:20}
#theme-btn{position:fixed;right:14px;bottom:70px;width:44px;height:44px;border-radius:50%;border:1px solid var(--line);background:var(--card);color:var(--fg);cursor:pointer;z-index:20}
.mask{display:none;position:fixed;inset:0;background:rgba(0,0,0,.3);z-index:35}
.mask.on{display:block}
.demo{border:1px solid var(--line);border-radius:10px;padding:10px;margin:14px auto;max-width:520px;text-align:center;background:var(--card)}
.demo canvas{width:100%;max-width:480px;height:230px;display:block;margin:0 auto;touch-action:none}
.demo input[type=range]{width:90%;margin:8px 0}
.demo .v{font-size:13px;color:var(--muted)}
@media (min-width:768px){
  .topbar{display:none}
  .sidebar{transform:none;width:300px}
  main{margin-left:300px;padding:30px 24px 100px;max-width:900px}
  .ch-title{font-size:26px}
}
"""

JS = r"""
var ORDER = __ORDER__;
var TITLES = __TITLES__;
var PARTS = __PARTS__;
var cur = ORDER[0];

function renderMath(el){
  if(!window.renderMathInElement){ return false; }
  try{
    renderMathInElement(el,{
      delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false},
                  {left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false}],
      throwOnError:false, ignoredTags:['script','noscript','style','textarea','pre','code']
    });
    return true;
  }catch(e){ return false; }
}

function fillNav(sec, idx){
  var bc = sec.querySelector('.breadcrumb');
  if(bc){ bc.textContent = '从零推导 / ' + (sec.dataset.part||'') + ' / ' + (sec.dataset.title||''); }
  var nav = sec.querySelector('.chapter-nav');
  if(!nav){ return; }
  var prev = idx>0 ? '<a href="#/'+ORDER[idx-1]+'" data-go="'+ORDER[idx-1]+'">‹ '+(TITLES[ORDER[idx-1]]||'')+'</a>' : '<span class="ph">占位</span>';
  var next = idx<ORDER.length-1 ? '<a href="#/'+ORDER[idx+1]+'" data-go="'+ORDER[idx+1]+'">'+(TITLES[ORDER[idx+1]]||'')+' ›</a>' : '<span class="ph">占位</span>';
  nav.innerHTML = prev + next;
}

function show(id, push){
  if(ORDER.indexOf(id) < 0){ id = ORDER[0]; }
  cur = id;
  document.querySelectorAll('.chapter').forEach(function(s){ s.classList.remove('on'); });
  var sec = document.getElementById('sec-'+id);
  if(!sec){ return; }
  sec.classList.add('on');
  fillNav(sec, ORDER.indexOf(id));
  document.getElementById('cur-title').textContent = TITLES[id] || '';
  document.querySelectorAll('.tree-item').forEach(function(a){
    a.classList.toggle('on', a.dataset.target === id);
  });
  renderMath(sec);
  window.scrollTo(0,0);
  if(push !== false){ history.replaceState(null,'','#/'+id); }
  closeDrawer();
}

function step(d){
  var i = ORDER.indexOf(cur) + d;
  if(i>=0 && i<ORDER.length){ show(ORDER[i]); }
}

function openDrawer(){ document.getElementById('sidebar').classList.add('open'); document.getElementById('mask').classList.add('on'); }
function closeDrawer(){ document.getElementById('sidebar').classList.remove('open'); document.getElementById('mask').classList.remove('on'); }

function boot(){
  var hash = location.hash.replace(/^#\//,'');
  show(ORDER.indexOf(hash)>=0?hash:ORDER[0], false);
  document.getElementById('menu-btn').addEventListener('click', openDrawer);
  document.getElementById('mask').addEventListener('click', closeDrawer);
  document.getElementById('prev-btn').addEventListener('click', function(){ step(-1); });
  document.getElementById('next-btn').addEventListener('click', function(){ step(1); });
  document.getElementById('totop').addEventListener('click', function(){ window.scrollTo({top:0,behavior:'smooth'}); });
  document.getElementById('theme-btn').addEventListener('click', function(){
    var d = document.body.dataset.theme==='dark' ? 'light':'dark';
    document.body.dataset.theme = d;
    this.textContent = d==='dark' ? '☀' : '☾';
  });
  document.addEventListener('click', function(e){
    var a = e.target.closest('[data-go]');
    if(a){ e.preventDefault(); show(a.dataset.go); }
    var t = e.target.closest('.tree-item');
    if(t){ e.preventDefault(); show(t.dataset.target); }
  });
  window.addEventListener('hashchange', function(){
    var h = location.hash.replace(/^#\//,'');
    if(ORDER.indexOf(h)>=0 && h!==cur){ show(h, false); }
  });
  // 所有章节（含隐藏的）都渲染一次
  ORDER.forEach(function(id, i){
    var s = document.getElementById('sec-'+id);
    if(s){ fillNav(s, i); renderMath(s); }
  });
  // 兜底重试（KaTeX 可能稍晚就绪）
  var tries = 0;
  var iv = setInterval(function(){
    tries++;
    if(window.renderMathInElement || tries>40){
      clearInterval(iv);
      ORDER.forEach(function(id){
        var s = document.getElementById('sec-'+id);
        if(s){ renderMath(s); }
      });
    }
  }, 150);
}
document.addEventListener('DOMContentLoaded', boot);
"""


def build(doc):
    chapters = doc["chapters"]
    order = [c[0] for c in chapters]
    part_of = {}
    for part, ids in doc["parts"]:
        for i in ids:
            part_of[i] = part

    secs = []
    for cid, title, desc in chapters:
        p = os.path.join(SRC, doc["key"], cid + ".html")
        frag = open(p, encoding="utf-8").read()
        secs.append(
            '<section class="chapter" id="sec-%s" data-cid="%s" data-title="%s" data-part="%s">\n'
            '<div class="breadcrumb"></div>\n'
            '<h1 class="ch-title">%s</h1>\n'
            '<p class="ch-desc">%s</p>\n%s\n'
            '<div class="chapter-nav"></div>\n</section>' % (cid, cid, title, part_of[cid], title, desc, frag)
        )

    tree = []
    for part, ids in doc["parts"]:
        tree.append('<div class="tree-part">%s</div>' % part)
        for cid, title, _ in chapters:
            if cid in ids:
                tree.append('<a class="tree-item" data-target="%s" href="#/%s">%s</a>' % (cid, cid, title))
    tree_html = "\n  ".join(tree)

    demo = os.path.join(HERE, "demo_%s.js" % doc["key"])
    if os.path.exists(demo):
        JS_EXTRA = open(demo, encoding="utf-8").read()
    else:
        JS_EXTRA = ""

    js = (JS.replace("__ORDER__", repr(order).replace("'", '"'))
              .replace("__TITLES__", __import__("json").dumps({c[0]: c[1] for c in chapters}, ensure_ascii=False))
              .replace("__PARTS__", "{}")) + "\n" + JS_EXTRA

    katex_css = font_css()
    katex_js = open(os.path.join(ASSETS, "katex.min.js"), encoding="utf-8").read()
    auto_js = open(os.path.join(ASSETS, "contrib", "auto-render.min.js"), encoding="utf-8").read()

    html = """<!DOCTYPE html>
<html lang="zh-CN" data-doc="__KEY__">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ · 从零推导</title>
<style>__KATEX_CSS__</style>
<style>__CSS__</style>
</head>
<body>
<div class="topbar">
  <button id="menu-btn" aria-label="目录">☰</button>
  <div id="cur-title"></div>
  <button id="prev-btn" aria-label="上一章">‹</button>
  <button id="next-btn" aria-label="下一章">›</button>
</div>
<div class="mask" id="mask"></div>
<aside class="sidebar" id="sidebar">
  <h3>__TITLE__ · 知识树</h3>
  __TREE__
</aside>

<main>
__SECTIONS__
</main>

<button id="theme-btn" aria-label="切换主题">☾</button>
<button id="totop" aria-label="回到顶部">↑</button>

<script>__KATEX_JS__</script>
<script>__AUTO_JS__</script>
<script>__JS__</script>
</body>
</html>
"""

    html = (html.replace("__KEY__", doc["key"])
                .replace("__TITLE__", doc["title"])
                .replace("__KATEX_CSS__", katex_css)
                .replace("__CSS__", CSS)
                .replace("__TREE__", tree_html)
                .replace("__SECTIONS__", "\n".join(secs))
                .replace("__KATEX_JS__", katex_js)
                .replace("__AUTO_JS__", auto_js)
                .replace("__JS__", js))

    out = os.path.join(os.path.dirname(HERE), doc["file"])
    open(out, "w", encoding="utf-8").write(html)
    print("%s  %.1f KB  sections=%d" % (doc["file"], len(html.encode()) / 1024, len(secs)))


if __name__ == "__main__":
    for d in DOCS:
        build(d)
