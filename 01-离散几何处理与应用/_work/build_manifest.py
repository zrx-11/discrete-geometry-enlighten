#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 quiz.md / flashcards.md / glossary.md 生成 manifest.json（book-enlighten §10 schema）。"""
import json, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CH = [
    ("ch01", "第 1 章：几何处理的数学基础", "chapters/ch01-数学基础.md", 1),
    ("ch02", "第 2 章：点云曲面重建和光顺", "chapters/ch02-重建与光顺.md", 2),
    ("ch03", "第 3 章：网格曲面的参数化和多分辨率表示", "chapters/ch03-参数化与多分辨率.md", 2),
    ("ch04", "第 4 章：网格模型的重网格化", "chapters/ch04-重网格化.md", 3),
    ("ch05", "第 5 章：三维形状分析", "chapters/ch05-形状分析.md", 2),
    ("ch06", "第 6 章：网格曲面的形变", "chapters/ch06-曲面形变.md", 2),
    ("ch07", "第 7 章：弹性运动模拟", "chapters/ch07-弹性模拟.md", 3),
    ("ch08", "第 8 章：基于机器学习的几何处理", "chapters/ch08-机器学习几何.md", 3),
    ("ch09", "第 9 章：新型几何处理应用", "chapters/ch09-新型应用.md", 1),
    ("mix", "综合测验与最终检验", "quiz.md", 2),
]

CONCEPTS = [
    ("c01", "离散 Laplace 算子与余切权重", "concepts/discrete-laplace.md", ["ch01", "ch02", "ch03", "ch05", "ch06", "ch07"]),
    ("c02", "离散高斯曲率与角度亏欠", "concepts/gauss-curvature.md", ["ch01", "ch04", "ch05"]),
    ("c03", "样条家族：从三次样条到 NURBS", "concepts/splines.md", ["ch01", "ch03"]),
    ("c04", "点云配准与 ICP", "concepts/icp-registration.md", ["ch02", "ch09"]),
    ("c05", "Voronoi / Delaunay 与 Crust 系列重建", "concepts/voronoi-crust.md", ["ch01", "ch02"]),
    ("c06", "Poisson 曲面重建", "concepts/poisson-reconstruction.md", ["ch02", "ch06", "ch07"]),
    ("c07", "参数化：调和、共形与防翻转", "concepts/parameterization.md", ["ch03", "ch04"]),
    ("c08", "QEM 简化与渐进网格", "concepts/qem-progressive-mesh.md", ["ch03"]),
    ("c09", "方向场、周期跳跃与奇异点", "concepts/cross-field.md", ["ch04"]),
    ("c10", "标架场与六面体重网格化", "concepts/frame-field-hex.md", ["ch04"]),
    ("c11", "形状描述子与谱签名（HKS / WKS）", "concepts/shape-descriptor.md", ["ch05", "ch08"]),
    ("c12", "网格分割与归一化割", "concepts/mesh-segmentation.md", ["ch05", "ch09"]),
    ("c13", "蒙皮：LBS、DQS 与骨骼学习", "concepts/skinning-lbs.md", ["ch06"]),
    ("c14", "梯度域形变与 ARAP", "concepts/gradient-domain-arap.md", ["ch06", "ch07"]),
    ("c15", "弹性模拟：隐式积分、PBD 与子空间", "concepts/elastic-simulation.md", ["ch07"]),
    ("c16", "稀疏、低秩与深度几何学习", "concepts/sparse-and-deep.md", ["ch08"]),
]

PATH = [
    ("01", "几何处理的数学基础", ["ch01"], "ch01 自测 ≥ 3/4，能写出余切权重表达式"),
    ("02", "点云曲面重建与光顺", ["ch02"], "能讲清 ICP 两步交替为什么单调下降"),
    ("03", "参数化与多分辨率表示", ["ch03"], "能解释参数化为什么翻转、QEM 误差怎么累加"),
    ("04", "网格模型的重网格化", ["ch04"], "能画出方向场奇异点与 3/5 价顶点的对应"),
    ("05", "三维形状分析", ["ch05"], "能说出 HKS 为什么等距不变"),
    ("06", "网格曲面的形变", ["ch06"], "能写出梯度域形变的最小二乘形式"),
    ("07", "弹性运动模拟", ["ch07"], "能解释 PBD 与隐式积分的关系"),
    ("08", "基于机器学习的几何处理", ["ch08"], "能说出 PointNet 为什么能容忍点序"),
    ("09", "新型几何处理应用", ["ch09"], "能列出 3D 打印的三类几何约束"),
    ("10", "综合检验", ["mix"], "完成最终检验项目并给出技术报告"),
]

CN_NUM = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def parse_quiz(path):
    text = open(path, encoding="utf-8").read()
    quizzes = []
    cur_ch, cur_mix, stop = None, False, False
    blocks = text.split("\n### ")
    # 先按 ## 切大节
    sections = re.split(r"\n## ", text)
    n = 0
    for sec in sections:
        head = sec.split("\n", 1)[0]
        m = re.match(r"第\s*(\d+)\s*章", head)
        if m:
            cur_ch = "ch%02d" % int(m.group(1))
        elif head.startswith("综合测验"):
            cur_ch = "mix"
        elif head.startswith("最终检验"):
            stop = True
        else:
            continue
        stop = head.startswith("最终检验")
        if stop:
            continue
        # 该节内的题目
        for b in re.split(r"\n### ", sec)[1:]:
            lines = b.split("\n")
            qhead = lines[0]
            mm = re.match(r"Q(\d+)\.（(单选|多选|填空|简答)）(.*)", qhead)
            if not mm:
                continue
            n += 1
            qtype = mm.group(2)
            stem = mm.group(3).strip()
            opts, ans, expl = [], None, []
            for ln in lines[1:]:
                s = ln.strip()
                om = re.match(r"- [A-D]\. (.*)", s)
                if om:
                    opts.append(om.group(1))
                    continue
                am = re.match(r"\*\*答案\*\*：(.*)", s)
                if am:
                    ans = am.group(1).strip()
                    continue
                em = re.match(r"\*\*解析\*\*：(.*)", s)
                if em:
                    expl.append(em.group(1).strip())
                    continue
                if expl and s:
                    expl.append(s)
            if ans is None:
                continue
            qid = "q%02d" % n
            if qtype == "单选":
                idx = "ABCD".index(ans[0])
                quizzes.append(dict(id=qid, chapterId=cur_ch, type="single", question=stem,
                                    options=opts, answer=idx, explain=" ".join(expl)))
            elif qtype == "多选":
                letters = [c for c in ans if c in "ABCD"]
                quizzes.append(dict(id=qid, chapterId=cur_ch, type="multi", question=stem,
                                    options=opts, answer=["ABCD".index(c) for c in letters],
                                    explain=" ".join(expl)))
            else:
                quizzes.append(dict(id=qid, chapterId=cur_ch, type="blank", question=stem,
                                    options=[], answer=ans, explain=" ".join(expl)))
    return quizzes


def parse_cards(path):
    text = open(path, encoding="utf-8").read()
    cards, cur = [], None
    n = 0
    for line in text.split("\n"):
        m = re.match(r"## 第\s*(\d+)\s*章", line)
        if m:
            cur = "ch%02d" % int(m.group(1))
            continue
        if line.startswith("### 卡片："):
            n += 1
            cards.append(dict(id="f%02d" % n, chapterId=cur, front=line[len("### 卡片："):].strip(),
                              back="", tags=[]))
            continue
        if cards:
            bm = re.match(r"- \*\*背面\*\*：(.*)", line.strip())
            if bm:
                cards[-1]["back"] = bm.group(1).strip()
                continue
            tm = re.match(r"- \*\*标签\*\*：(.*)", line.strip())
            if tm:
                cards[-1]["tags"] = [t.strip() for t in re.split(r"[,，]", tm.group(1)) if t.strip()]
    return cards


def parse_glossary(path):
    rows = []
    for line in open(path, encoding="utf-8"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or cells[0] in ("术语",) or set(cells[0]) <= set("-: "):
            continue
        ch = cells[3]
        m = re.match(r"第\s*(\d+)\s*章", ch)
        cid = "ch%02d" % int(m.group(1)) if m else "ch01"
        rows.append({"term": cells[0], "def": cells[1], "chapterId": cid})
    return rows


manifest = {
    "slug": "discrete-geometry-processing",
    "title": "《离散几何处理与应用》点化学习",
    "subtitle": "从数学基础到 3D 打印与机器人：九章逐层拆到零基础能读",
    "book": {
        "title": "离散几何处理与应用",
        "author": "鲍虎军、黄劲、刘利刚",
        "source": ["离散几何处理与应用 (鲍虎军, 黄劲, 刘利刚) (扫描版, 351 页, 2020-11)"],
    },
    "audience": "零基础（需高中向量与导数；前置缺口已补讲）",
    "goal": "系统掌握三角网格上的离散微分几何、重建、参数化、重网格化、形变与模拟，并能判断真实任务该选哪条技术路线",
    "learningPath": [dict(step=s, title=t, chapterIds=c, checkpoint=k) for s, t, c, k in PATH],
    "chapters": [dict(id=i, title=t, file=f, difficulty=d) for i, t, f, d in CH],
    "concepts": [dict(id=i, title=t, file=f, chapterIds=c) for i, t, f, c in CONCEPTS],
    "glossary": parse_glossary(os.path.join(BASE, "glossary.md")),
    "patterns": {"file": "patterns.md"},
    "cheatsheet": {"file": "cheatsheet.md"},
    "quizzes": parse_quiz(os.path.join(BASE, "quiz.md")),
    "flashcards": parse_cards(os.path.join(BASE, "flashcards.md")),
    "companion": "discrete-geometry-processing学习伴侣.html",
}

out = os.path.join(BASE, "manifest.json")
json.dump(manifest, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("chapters", len(manifest["chapters"]), "concepts", len(manifest["concepts"]),
      "glossary", len(manifest["glossary"]), "quizzes", len(manifest["quizzes"]),
      "cards", len(manifest["flashcards"]))
# 校验
ids = {c["id"] for c in manifest["chapters"]}
bad = [q["id"] for q in manifest["quizzes"] if q["chapterId"] not in ids]
bad += [c["id"] for c in manifest["flashcards"] if c["chapterId"] not in ids]
print("bad chapter refs:", bad)
missing = [q["id"] for q in manifest["quizzes"] if not q["explain"]]
print("missing explain:", missing)
for c in manifest["concepts"]:
    for cid in c["chapterIds"]:
        assert cid in ids, (c["id"], cid)
print("ok")
