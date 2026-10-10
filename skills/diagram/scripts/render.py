#!/usr/bin/env python3
"""把 diagram skill 的 JSON 数据渲染成飞书画板风格的自包含 HTML（零依赖，Python 3.8+）。

用法:
  python3 render.py diagram.json -o diagram.html   # 渲染 HTML
  python3 render.py diagram.json --mermaid         # 输出 Mermaid 代码
  python3 render.py diagram.json --check           # 只做结构校验
"""
import argparse, html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
THEME = json.load(open(os.path.join(HERE, "..", "theme.json"), encoding="utf-8"))
T = THEME
esc = lambda s: html.escape(str(s if s is not None else ""))
MAX_NODES, HARD_MAX = 12, 15

MERMAID_INIT = ('%%{init: {"theme":"base","themeVariables":{"primaryColor":"#EEF3FF",'
                '"primaryBorderColor":"#7A9CF5","primaryTextColor":"#1F2329","lineColor":"#646A73",'
                '"secondaryColor":"#FFF5C2","tertiaryColor":"#F8F9FA",'
                '"fontFamily":"PingFang SC, Noto Sans CJK SC, sans-serif","fontSize":"13px"}}}%%')


class Invalid(Exception):
    pass


# ---------------------------------------------------------------- 校验
def check(d):
    errs, warns = [], []
    t = d.get("type")
    if t not in RENDERERS:
        raise Invalid(f"未知的 type: {t!r}，可选: {', '.join(RENDERERS)}")
    if not d.get("title"):
        warns.append("缺少 title（这张图回答什么问题）")
    if not d.get("summary"):
        warns.append("缺少 summary（一句话结论）")

    def count(n, what):
        if n > HARD_MAX:
            errs.append(f"{what}共 {n} 个，超过硬上限 {HARD_MAX}，请拆图")
        elif n > MAX_NODES:
            warns.append(f"{what}共 {n} 个，超过建议值 {MAX_NODES}，考虑拆图")

    if t == "layered-architecture":
        layers = d.get("layers") or []
        if not layers:
            errs.append("layers 为空")
        count(sum(len(l.get("modules", [])) for l in layers), "模块")
        for l in layers:
            for m in l.get("modules", []):
                if m.get("status") not in (None, "new", "changed", "risk"):
                    errs.append(f"模块 {m.get('name')} 的 status 只能是 new/changed/risk")
    elif t == "flowchart":
        nodes, edges = d.get("nodes") or [], d.get("edges") or []
        ids = {n.get("id") for n in nodes}
        count(len(nodes), "节点")
        starts = [n for n in nodes if n.get("kind") == "start"]
        if len(starts) != 1:
            errs.append(f"需要恰好一个 start 节点，当前 {len(starts)} 个")
        if not any(n.get("kind") == "end" for n in nodes):
            errs.append("缺少 end 节点")
        for n in nodes:
            if n.get("kind") not in ("start", "end", "step", "decision", "error"):
                errs.append(f"节点 {n.get('id')} 的 kind 无效")
            if n.get("kind") == "decision":
                outs = [e for e in edges if e.get("from") == n.get("id")]
                if len(outs) != 2:
                    warns.append(f"判断节点 {n.get('id')} 应该恰好两个出口，当前 {len(outs)} 个")
                if any(not e.get("label") for e in outs):
                    warns.append(f"判断节点 {n.get('id')} 的出口缺少 label")
        for e in edges:
            if e.get("from") not in ids or e.get("to") not in ids:
                errs.append(f"连线 {e.get('from')} -> {e.get('to')} 指向不存在的节点")
    elif t == "sequence":
        ps = d.get("participants") or []
        if len(ps) > 6:
            warns.append(f"参与方 {len(ps)} 个，建议 ≤ 6")
        for m in d.get("messages") or []:
            for k in ("from", "to"):
                if m.get(k) not in ps:
                    errs.append(f"消息里的 {m.get(k)!r} 不在 participants 中")
        if len(d.get("messages") or []) > 15:
            warns.append("消息超过 15 条，考虑拆图")
    elif t == "comparison-matrix":
        crit, opts = d.get("criteria") or [], d.get("options") or []
        if not 2 <= len(opts) <= 4:
            warns.append(f"方案数 {len(opts)}，建议 2～4 个")
        for o in opts:
            if len(o.get("scores", [])) != len(crit):
                errs.append(f"方案 {o.get('name')} 的 scores 数量和 criteria 不一致")
            for s in o.get("scores", []):
                if s not in ("good", "mid", "bad"):
                    errs.append(f"方案 {o.get('name')} 的分数 {s!r} 无效")
        if sum(1 for o in opts if o.get("recommended")) > 1:
            errs.append("recommended 最多一个")
    elif t == "timeline":
        ms = d.get("milestones") or []
        if len(ms) > 6:
            warns.append(f"里程碑 {len(ms)} 个，建议 ≤ 6")
    elif t == "general":
        if not d.get("mermaid"):
            errs.append("general 类型需要 mermaid 字段")
    return errs, warns


# ---------------------------------------------------------------- 外壳
def page(d, body, extra_head=""):
    return f"""<!doctype html><html lang="zh"><head><meta charset="utf-8">
<title>{esc(d.get('title'))}</title>{extra_head}
<style>
*{{box-sizing:border-box}}
body{{margin:0;font-family:{T['font']};color:{T['text']};background:{T['canvas']};
background-image:radial-gradient({T['dot']} 1px,transparent 1px);background-size:18px 18px;padding:32px}}
.card{{background:{T['card']};border:1px solid {T['border']};border-radius:12px;padding:20px 24px 24px;
box-shadow:0 2px 8px rgba(31,35,41,.06);display:inline-block;min-width:520px;max-width:100%}}
.hd{{display:flex;align-items:center;gap:8px;margin-bottom:4px}}
.tag{{font-size:12px;color:{T['primary']};background:#EEF3FF;border-radius:4px;padding:2px 6px}}
h1{{font-size:16px;margin:0;font-weight:600}}
.sum{{font-size:13px;color:{T['textSecondary']};margin:2px 0 16px}}
.legend{{display:flex;gap:14px;font-size:12px;color:{T['textSecondary']};margin-top:14px}}
.legend i{{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:4px;vertical-align:-2px;border:1.5px solid}}
</style></head><body><div class="card">
<div class="hd"><span class="tag">{esc(TYPE_NAMES[d['type']])}</span><h1>{esc(d.get('title'))}</h1></div>
<div class="sum">{esc(d.get('summary'))}</div>
{body}</div></body></html>"""


def legend(used):
    items = [k for k in ("new", "changed", "risk") if k in used]
    if not items:
        return ""
    s = T["status"]
    return '<div class="legend">' + "".join(
        f'<span><i style="background:{s[k]["fill"]};border-color:{s[k]["stroke"]}"></i>{s[k]["label"]}</span>'
        for k in items) + "</div>"


# ---------------------------------------------------------------- 分层架构图
def render_layered(d):
    used, rows = set(), []
    for i, l in enumerate(d["layers"]):
        c = T["layers"][i % len(T["layers"])]
        mods = []
        for m in l.get("modules", []):
            st = m.get("status") or "none"
            used.add(st)
            s = T["status"][st]
            code = f'<div class="code">{esc(m["code"])}</div>' if m.get("code") else ""
            note = f'<div class="note">{esc(m["note"])}</div>' if m.get("note") else ""
            badge = f'<span class="badge" style="color:{s["text"]};background:{s["fill"]}">{s["label"]}</span>' if st != "none" else ""
            mods.append(f'<div class="mod" style="background:{"#FFFFFF" if st=="none" else s["fill"]};'
                        f'border-color:{s["stroke"]};border-width:{1 if st=="none" else 1.5}px">'
                        f'<div class="mn">{esc(m["name"])}{badge}</div>{code}{note}</div>')
        rows.append(f'<div class="layer" style="background:{c["fill"]};border-color:{c["stroke"]}">'
                    f'<div class="ln">{esc(l["name"])}</div><div class="mods">{"".join(mods)}</div></div>')
    css = f"""<style>
.layers{{display:flex;flex-direction:column;gap:8px}}
.layer{{display:flex;align-items:stretch;border:1px solid;border-radius:8px;padding:10px 12px;gap:12px}}
.ln{{width:64px;flex:none;font-size:13px;font-weight:600;color:{T['textSecondary']};display:flex;align-items:center}}
.mods{{display:flex;gap:10px;flex-wrap:wrap;flex:1}}
.mod{{border:1px solid;border-radius:6px;padding:8px 12px;min-width:120px;flex:1;max-width:220px}}
.mn{{font-size:13px;font-weight:500;display:flex;align-items:center;gap:6px;white-space:nowrap}}
.badge{{font-size:11px;border-radius:3px;padding:0 4px;font-weight:400}}
.code{{font-size:11px;color:{T['textMuted']};font-family:Menlo,monospace;margin-top:2px}}
.note{{font-size:11px;color:{T['textSecondary']};margin-top:2px}}
</style>"""
    return page(d, f'<div class="layers">{"".join(rows)}</div>{legend(used)}', css)


# ---------------------------------------------------------------- 流程图
FW = {"start": 150, "end": 150, "step": 160, "decision": 136, "error": 150}
FH = {"start": 38, "end": 38, "step": 42, "decision": 70, "error": 42}
GAP = 38


def layout_flow(d):
    nodes = {n["id"]: n for n in d["nodes"]}
    edges = d["edges"]
    outs = lambda nid: [e for e in edges if e["from"] == nid]
    start = next(n["id"] for n in d["nodes"] if n["kind"] == "start")
    main, cur, seen = [], start, set()
    while cur and cur not in seen:
        seen.add(cur)
        main.append(cur)
        nxt = [e for e in outs(cur) if not e.get("branch") and not e.get("back") and e["to"] not in seen]
        cur = nxt[0]["to"] if nxt else None
    pos, y, cx = {}, 10, 120
    for nid in main:
        k = nodes[nid]["kind"]
        pos[nid] = (cx, y + FH[k] / 2)
        y += FH[k] + GAP
    bx = cx + 110 + 140
    side = []
    for nid in main:  # 侧向分支放在源节点右侧，分支后续节点往下排
        for e in outs(nid):
            if e.get("branch") and e["to"] not in pos:
                t, yy = e["to"], pos[nid][1]
                while t and t not in pos:
                    pos[t] = (bx, yy)
                    side.append(t)
                    yy += FH[nodes[t]["kind"]] + GAP
                    fw = [x for x in outs(t) if not x.get("back") and x["to"] not in pos]
                    t = fw[0]["to"] if fw else None
    for nid in nodes:  # 兜底：没被放置的节点放在最下面
        if nid not in pos:
            pos[nid] = (cx, y + 20)
            y += 60
    return nodes, edges, pos, main, bx


def shape(n, x, y):
    k, c = n["kind"], T["flow"][n["kind"]]
    w, h = FW[k], FH[k]
    txt = f'<text x="{x}" y="{y+4.5}" text-anchor="middle" font-size="13" fill="{T["text"]}">{esc(n["text"])}</text>'
    if k == "decision":
        pts = f"{x},{y-h/2} {x+w/2},{y} {x},{y+h/2} {x-w/2},{y}"
        return f'<polygon points="{pts}" fill="{c["fill"]}" stroke="{c["stroke"]}" stroke-width="1.5"/>' + txt
    r = h / 2 if k in ("start", "end") else 6
    return (f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="{r}" '
            f'fill="{c["fill"]}" stroke="{c["stroke"]}" stroke-width="1.5"/>' + txt)


def render_flow(d):
    nodes, edges, pos, main, bx = layout_flow(d)
    hw = lambda nid: FW[nodes[nid]["kind"]] / 2
    hh = lambda nid: FH[nodes[nid]["kind"]] / 2
    paths, labels, lane = [], [], 0
    right = bx + 75
    for e in edges:
        a, b = e["from"], e["to"]
        (x1, y1), (x2, y2) = pos[a], pos[b]
        lab = e.get("label")
        if e.get("back") or y2 < y1 - 1:  # 回路：从右侧绕上去，进入目标右侧
            lane += 1
            lx = max(x1 + hw(a), x2 + hw(b), right if x1 >= bx else x1 + hw(a)) + 18 * lane
            sx, tx = x1 + hw(a), x2 + hw(b)
            if x1 < bx and x2 < bx and right > lx:  # 主列内部回路：走主列和分支列之间
                lx = x1 + hw(a) + 18 * lane
            p = f"M{sx},{y1} H{lx} V{y2} H{tx}"
            if lab:
                labels.append((lx + 4, (y1 + y2) / 2, lab, "start"))
        elif abs(y1 - y2) < 1:  # 同一行：向右
            p = f"M{x1+hw(a)},{y1} H{x2-hw(b)}"
            if lab:
                labels.append(((x1 + hw(a) + x2 - hw(b)) / 2, y1 - 6, lab, "middle"))
        elif abs(x1 - x2) < 1:  # 同一列：向下
            p = f"M{x1},{y1+hh(a)} V{y2-hh(b)}"
            if lab:
                labels.append((x1 + 8, y1 + hh(a) + 16, lab, "start"))
        else:  # 跨列向下
            p = f"M{x1},{y1+hh(a)} V{y2} H{x2 + (hw(b) if x2 < x1 else -hw(b))}"
            if lab:
                labels.append((x1 + 8, y1 + hh(a) + 16, lab, "start"))
        paths.append(f'<path d="{p}" fill="none" stroke="{T["line"]}" stroke-width="1.3" marker-end="url(#ar)"/>')
    shapes = "".join(shape(nodes[n], *pos[n]) for n in nodes)
    labs = "".join(f'<text x="{x}" y="{y}" font-size="12" fill="{T["textSecondary"]}" text-anchor="{a}">{esc(t)}</text>'
                   for x, y, t, a in labels)
    W = int(max([x + FW[nodes[n]["kind"]] / 2 + 30 + 18 * lane for n, (x, _) in pos.items()] +
                [x + 13 * len(str(t)) + 10 for x, _, t, a in labels if a == "start"]))
    H = int(max(y + FH[nodes[n]["kind"]] / 2 for n, (_, y) in pos.items()) + 14)
    svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
           f'font-family=\'{T["font"]}\'><defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" '
           f'markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
           f'fill="{T["line"]}"/></marker></defs>{"".join(paths)}{shapes}{labs}</svg>')
    return page(d, svg)


# ---------------------------------------------------------------- 对比矩阵
def render_matrix(d):
    sc = T["score"]
    head = "<th></th>" + "".join(
        f'<th class="{"rec" if o.get("recommended") else ""}">{esc(o["name"])}'
        f'{"<span class=r>推荐</span>" if o.get("recommended") else ""}</th>' for o in d["options"])
    rows = []
    for i, c in enumerate(d["criteria"]):
        cells = []
        for o in d["options"]:
            s = sc[o["scores"][i]]
            note = (o.get("notes") or [""] * len(d["criteria"]))[i] if i < len(o.get("notes") or []) else ""
            cells.append(f'<td style="background:{s["fill"]};color:{s["text"]}"><b>{s["mark"]}</b>'
                         f'{" " + esc(note) if note else ""}</td>')
        rows.append(f'<tr><th class="c">{esc(c)}</th>{"".join(cells)}</tr>')
    css = f"""<style>table{{border-collapse:separate;border-spacing:4px;font-size:13px}}
th{{font-weight:600;padding:8px 12px;text-align:left;white-space:nowrap}} th.c{{color:{T['textSecondary']};font-weight:500}}
th.rec{{color:{T['primary']}}} .r{{font-size:11px;font-weight:400;background:#EEF3FF;color:{T['primary']};border-radius:3px;padding:1px 5px;margin-left:6px}}
td{{padding:8px 12px;border-radius:6px;min-width:140px}} td b{{margin-right:2px}}</style>"""
    return page(d, f"<table><tr>{head}</tr>{''.join(rows)}</table>", css)


# ---------------------------------------------------------------- 时间线
def render_timeline(d):
    used, items = set(), []
    for m in d["milestones"]:
        st = m.get("status") or "none"
        used.add(st)
        s = T["status"][st]
        dl = "".join(f"<li>{esc(x)}</li>" for x in m.get("deliverables", []))
        items.append(f'<div class="ms"><div class="dot" style="background:{s["stroke"] if st!="none" else T["primary"]}"></div>'
                     f'<div class="when">{esc(m.get("when"))}</div>'
                     f'<div class="box" style="background:{s["fill"]};border-color:{s["stroke"]}">'
                     f'<div class="nm">{esc(m["name"])}</div><ul>{dl}</ul></div></div>')
    css = f"""<style>.tl{{display:flex;gap:12px;position:relative;padding-top:8px}}
.tl:before{{content:"";position:absolute;left:0;right:0;top:14px;border-top:2px solid {T['border']}}}
.ms{{flex:1;min-width:150px;position:relative}} .dot{{width:12px;height:12px;border-radius:50%;margin:0 0 8px 0;position:relative;border:2px solid #fff}}
.when{{font-size:12px;color:{T['textSecondary']};margin-bottom:6px}}
.box{{border:1px solid;border-radius:8px;padding:10px 12px}} .nm{{font-size:13px;font-weight:600}}
ul{{margin:6px 0 0;padding-left:16px;font-size:12px;color:{T['textSecondary']}}}</style>"""
    return page(d, f'<div class="tl">{"".join(items)}</div>{legend(used)}', css)


# ---------------------------------------------------------------- Mermaid
def to_mermaid(d):
    t = d["type"]
    q = lambda s: str(s).replace('"', "'")
    if t == "general":
        return MERMAID_INIT + "\n" + d["mermaid"]
    if t == "sequence":
        L = ["sequenceDiagram"] + [f"  participant P{i} as {q(p)}" for i, p in enumerate(d["participants"])]
        idx = {p: f"P{i}" for i, p in enumerate(d["participants"])}
        notes = {}
        for n in d.get("notes") or []:
            notes.setdefault(n.get("after", 0), []).append(n)
        for i, m in enumerate(d["messages"]):
            L.append(f"  {idx[m['from']]}{'-->>' if m.get('reply') else '->>'}{idx[m['to']]}: {q(m['text'])}")
            for n in notes.get(i, []):
                L.append(f"  Note over {idx[n['over']]}: {q(n['text'])}")
        return MERMAID_INIT + "\n" + "\n".join(L)
    if t == "flowchart":
        # `end` is a Mermaid reserved word, so class names cannot reuse node kinds.
        kind_cls = {"start": "kindStart", "end": "kindEnd", "step": "kindStep",
                    "decision": "kindDecision", "error": "kindError"}
        sh = {"start": '(["{}"])', "end": '(["{}"])', "step": '["{}"]', "decision": '{{"{}"}}', "error": '["{}"]'}
        L = ["flowchart TD"] + [f"  {n['id']}{sh[n['kind']].format(q(n['text']))}" for n in d["nodes"]]
        for e in d["edges"]:
            L.append(f"  {e['from']} -->{'|' + q(e['label']) + '|' if e.get('label') else ''} {e['to']}")
        for k, c in T["flow"].items():
            L.append(f"  classDef {kind_cls[k]} fill:{c['fill']},stroke:{c['stroke']},color:{T['text']}")
        for n in d["nodes"]:
            L.append(f"  class {n['id']} {kind_cls[n['kind']]}")
        return MERMAID_INIT + "\n" + "\n".join(L)
    if t == "layered-architecture":
        L, k = ["flowchart TB"], 0
        for i, l in enumerate(d["layers"]):
            L.append(f'  subgraph L{i}["{q(l["name"])}"]')
            L.append("    direction LR")
            for m in l.get("modules", []):
                L.append(f'    M{k}["{q(m["name"])}"]')
                if m.get("status"):
                    L.append(f"    class M{k} {m['status']}")
                k += 1
            L.append("  end")
        for i in range(len(d["layers"]) - 1):
            L.append(f"  L{i} ~~~ L{i+1}")
        for st, c in T["status"].items():
            L.append(f"  classDef {st} fill:{c['fill']},stroke:{c['stroke']},color:{T['text']}")
        return MERMAID_INIT + "\n" + "\n".join(L)
    if t == "comparison-matrix":
        sc = T["score"]
        L, classes = ["flowchart LR"], []
        for oi, o in enumerate(d["options"]):
            title = q(o["name"])
            if o.get("recommended"):
                title += " · 推荐"
            L.append(f'  subgraph O{oi}["{title}"]')
            L.append("    direction TB")
            notes = o.get("notes") or []
            ids = []
            for i, crit in enumerate(d["criteria"]):
                score = o["scores"][i]
                note = notes[i] if i < len(notes) else ""
                label = q(crit) + " " + sc[score]["mark"]
                if note:
                    label += " " + q(note)
                nid = f"O{oi}C{i}"
                ids.append(nid)
                L.append(f'    {nid}["{label}"]')
                classes.append(f"  class {nid} {score}")
            for a, b in zip(ids, ids[1:]):
                L.append(f"    {a} ~~~ {b}")
            L.append("  end")
        for key, c in sc.items():
            L.append(f"  classDef {key} fill:{c['fill']},stroke:{c['text']},color:{c['text']}")
        L.extend(classes)
        return MERMAID_INIT + "\n" + "\n".join(L)
    raise Invalid(f"{t} 暂不支持输出 Mermaid，请用 HTML")


def render_mermaid_html(d):
    code = to_mermaid(d)
    head = ('<script type="module">import m from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";'
            'm.initialize({startOnLoad:true});</script>')
    return page(d, f'<pre class="mermaid">{esc(code)}</pre>', head)


RENDERERS = {
    "layered-architecture": render_layered,
    "flowchart": render_flow,
    "sequence": render_mermaid_html,
    "comparison-matrix": render_matrix,
    "timeline": render_timeline,
    "general": render_mermaid_html,
}
TYPE_NAMES = {"layered-architecture": "架构图", "flowchart": "流程图", "sequence": "时序图",
              "comparison-matrix": "方案对比", "timeline": "时间线", "general": "通用图"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("-o", "--output", help="输出 HTML 路径，默认与输入同名")
    ap.add_argument("--mermaid", action="store_true", help="输出 Mermaid 代码到标准输出")
    ap.add_argument("--check", action="store_true", help="只校验，不渲染")
    a = ap.parse_args()
    try:
        d = json.load(open(a.input, encoding="utf-8"))
        errs, warns = check(d)
    except (Invalid, json.JSONDecodeError) as ex:
        print(f"错误: {ex}", file=sys.stderr)
        sys.exit(2)
    for w in warns:
        print(f"警告: {w}", file=sys.stderr)
    if errs:
        for e in errs:
            print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    if a.check:
        print("校验通过")
        return
    if a.mermaid:
        print(to_mermaid(d))
        return
    out = a.output or os.path.splitext(a.input)[0] + ".html"
    open(out, "w", encoding="utf-8").write(RENDERERS[d["type"]](d))
    print(out)


if __name__ == "__main__":
    main()
