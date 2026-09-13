#!/usr/bin/env python3
"""Generate the first half (through the algorithms) of the FMCAD 2026 talk
"Parallelizing Congruence Closure".  Run:  python3 make_slides.py
Output: parallelcc-part1.pptx next to this script."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE
from pptx.oxml.ns import qn
import os

# ---------------------------------------------------------------- palette
NAVY   = RGBColor(0x1F, 0x2A, 0x44)
INK    = RGBColor(0x2B, 0x2F, 0x36)
GRAY   = RGBColor(0x6B, 0x71, 0x7A)
LIGHT  = RGBColor(0xC9, 0xCD, 0xD3)
ORANGE = RGBColor(0xC8, 0x50, 0x1E)
AMBER  = RGBColor(0xE0, 0xA3, 0x00)
AMBER_FILL = RGBColor(0xFF, 0xF3, 0xCC)
PURPLE = RGBColor(0x7B, 0x4F, 0xB5)
RED    = RGBColor(0xC0, 0x39, 0x2B)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
EDGE   = RGBColor(0x8A, 0x8F, 0x98)

CLASS_STYLE = {   # fill, outline
    'leaf': (RGBColor(0xEE, 0xF0, 0xF3), RGBColor(0x9A, 0xA0, 0xA8)),
    'a':    (RGBColor(0xDC, 0xEA, 0xF8), RGBColor(0x2E, 0x6F, 0xB0)),
    'x':    (RGBColor(0xDD, 0xF1, 0xE2), RGBColor(0x3A, 0x9A, 0x5B)),
    'm':    (RGBColor(0xFB, 0xE4, 0xD3), ORANGE),
}

FONT = 'Calibri'
MONO = 'Consolas'

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SLIDE_NO = [0]

# ---------------------------------------------------------------- helpers
def no_shadow(shape):
    shape.shadow.inherit = False
    st = shape._element.find(qn('p:style'))
    if st is not None:
        shape._element.remove(st)

def set_arrow(conn, head=True):
    ln = conn.line._get_or_add_ln()
    tag = 'a:tailEnd' if head else 'a:headEnd'
    for el in ln.findall(qn(tag)):
        ln.remove(el)
    ln.append(ln.makeelement(qn(tag), {'type': 'triangle', 'w': 'med', 'len': 'med'}))

def style_run(run, size, bold=False, color=INK, font=FONT, italic=False):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = font
    run.font.color.rgb = color

def add_runs(p, text, size, color=INK, font=FONT, bold=False):
    """'**' toggles bold inside text."""
    parts = text.split('**')
    for i, part in enumerate(parts):
        if not part:
            continue
        r = p.add_run()
        r.text = part
        style_run(r, size, bold=(bold or i % 2 == 1), color=color, font=font)

def add_text(slide, text, x, y, w, h, size=20, bold=False, color=INK,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font=FONT, italic=False,
             line_spacing=None):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.03)
    lines = text.split('\n')
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if line_spacing:
            p.line_spacing = line_spacing
        add_runs(p, line, size, color=color, font=font, bold=bold)
        if italic:
            for r in p.runs:
                r.font.italic = True
    return tb

def set_bullet(p, level, char='•', color=None):
    pPr = p._p.get_or_add_pPr()
    pPr.set('marL', str(int(Inches(0.30 + 0.34 * level))))
    pPr.set('indent', str(-int(Inches(0.26))))
    for tag in ('a:buNone', 'a:buChar', 'a:buAutoNum', 'a:buClr'):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    if color is not None:
        buClr = pPr.makeelement(qn('a:buClr'), {})
        srgb = buClr.makeelement(qn('a:srgbClr'), {'val': '%02X%02X%02X' % (color[0], color[1], color[2])})
        buClr.append(srgb)
        pPr.append(buClr)
    pPr.append(pPr.makeelement(qn('a:buChar'), {'char': char}))

def add_bullets(slide, items, x, y, w, h, size=20, color=INK, gap=6, font=FONT):
    """items: list of str or (level, str).  '**' toggles bold.  A leading
    '#' marks a heading line (bold, no bullet)."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05)
    first = True
    for it in items:
        level, text = (it if isinstance(it, tuple) else (0, it))
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        if text.startswith('#'):
            p.space_before = Pt(gap + 6)
            p.space_after = Pt(2)
            add_runs(p, text[1:].strip(), size, color=NAVY, font=font, bold=True)
            continue
        p.space_before = Pt(gap if level == 0 else 2)
        lvl_size = size if level == 0 else size - 3
        set_bullet(p, level, char='•' if level == 0 else '–', color=GRAY)
        add_runs(p, text, lvl_size, color=color, font=font)
    return tb

def add_rect(slide, x, y, w, h, fill=None, line=None, width=1.0, dash=None,
             rounded=True, radius=0.15, text=None, size=14, bold=False,
             color=INK, align=PP_ALIGN.CENTER, font=FONT):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    no_shadow(s)
    if rounded:
        s.adjustments[0] = radius
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(width)
        if dash:
            s.line.dash_style = dash
    tf = s.text_frame
    tf.margin_left = tf.margin_right = Inches(0.06)
    tf.margin_top = tf.margin_bottom = Inches(0.03)
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    if text is not None:
        lines = text.split('\n')
        for i, line in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            add_runs(p, line, size, color=color, font=font, bold=bold)
    return s

def add_line(slide, x1, y1, x2, y2, color=EDGE, width=1.25, arrow=False, dash=None):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1),
                                   Inches(x2), Inches(y2))
    no_shadow(c)
    c.line.color.rgb = color
    c.line.width = Pt(width)
    if dash:
        c.line.dash_style = dash
    if arrow:
        set_arrow(c)
    return c

def new_slide(title=None, notes=None, number=True):
    s = prs.slides.add_slide(BLANK)
    SLIDE_NO[0] += 1
    if title:
        add_text(s, title, 0.55, 0.32, 12.2, 0.8, size=30, bold=True, color=NAVY,
                 anchor=MSO_ANCHOR.MIDDLE)
        add_line(s, 0.62, 1.12, 3.0, 1.12, color=ORANGE, width=2.5)
    if number:
        add_text(s, str(SLIDE_NO[0]), 12.3, 7.0, 0.8, 0.35, size=11, color=GRAY,
                 align=PP_ALIGN.RIGHT)
        add_text(s, 'Parallelizing Congruence Closure  ·  FMCAD 2026', 0.55, 7.0,
                 6, 0.35, size=11, color=GRAY)
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s

# ---------------------------------------------------------------- e-graph diagram
LEAF, GATE, ITE = 4.05, 2.3, 0.55
LW, LH = 0.60, 0.46      # leaf node: name only
GW, GH = 0.88, 0.62      # gate node: operator (large) + label
NODES = {  # id: (label, operator, cx, cy) in diagram-local inches
    'r':  ('r',  None, 0.66, LEAF), 'rp': ('r\u2032', None, 1.34, LEAF),
    's':  ('s',  None, 2.30, LEAF), 'sp': ('s\u2032', None, 2.98, LEAF),
    'c':  ('c',  None, 3.94, LEAF), 'cp': ('c\u2032', None, 4.62, LEAF),
    'u':  ('u',  None, 5.58, LEAF), 'up': ('u\u2032', None, 6.26, LEAF),
    'v':  ('v',  None, 7.22, LEAF), 'vp': ('v\u2032', None, 7.90, LEAF),
    'a1': ('a\u2081', 'AND', 1.25, GATE), 'a2': ('a\u2082', 'AND', 2.45, GATE),
    'x1': ('x\u2081', 'XOR', 6.10, GATE), 'x2': ('x\u2082', 'XOR', 7.30, GATE),
    'm1': ('m\u2081', 'ITE', 3.70, ITE),  'm2': ('m\u2082', 'ITE', 5.15, ITE),
}
EDGES = {'a1': ['r', 's'], 'a2': ['rp', 'sp'], 'x1': ['u', 'v'], 'x2': ['up', 'vp'],
         'm1': ['c', 'a1', 'x1'], 'm2': ['cp', 'a2', 'x2']}
DIAG_CX = 4.28           # horizontal centre of the diagram in local inches

def ox_for(left=0.5, right=8.95):
    """Origin that centres the diagram in the strip between left and right."""
    return (left + right) / 2.0 - DIAG_CX

OX_FULL = ox_for(0.5, 12.83)   # whole slide, no side text
OX, OY = OX_FULL, 1.55         # every diagram is centred on the slide

def nsize(nid):
    return (GW, GH) if NODES[nid][1] else (LW, LH)

LAB_UP, LAB_RT = 0.30, 0.37   # room the outside label needs

LPOS = {'m1': 'left'}         # per-node overrides; keeps the m1/m2 gap clear

def lpos(nid):
    """Where the term name sits relative to its node."""
    if nid in LPOS:
        return LPOS[nid]
    sym = NODES[nid][1]
    if sym is None:
        return None            # leaves carry their name inside
    return 'right' if sym == 'ITE' else 'above'

LEAF_CLASSES = [(['r', 'rp'], 'leaf'), (['s', 'sp'], 'leaf'), (['c', 'cp'], 'leaf'),
                (['u', 'up'], 'leaf'), (['v', 'vp'], 'leaf')]
A_CLASS = (['a1', 'a2'], 'a')
X_CLASS = (['x1', 'x2'], 'x')
M_CLASS = (['m1', 'm2'], 'm')

def _bbox(ids, pad):
    x0 = min(NODES[i][2] - nsize(i)[0] / 2 - (LAB_RT if lpos(i) == 'left' else 0)
             for i in ids)
    x1 = max(NODES[i][2] + nsize(i)[0] / 2 + (LAB_RT if lpos(i) == 'right' else 0)
             for i in ids)
    y0 = min(NODES[i][3] - nsize(i)[1] / 2 - (LAB_UP if lpos(i) == 'above' else 0)
             for i in ids)
    y1 = max(NODES[i][3] + nsize(i)[1] / 2 for i in ids)
    return (x0 - pad, y0 - pad, x1 - x0 + 2 * pad, y1 - y0 + 2 * pad)

def draw_egraph(slide, ox=OX, oy=OY, classes=(), highlight=(), groups=(),
                dirty=(), labels=None, dim=(), edge_hl=()):
    """classes: list of (member ids, style key); highlight: node ids with amber
    outline; groups: list of id-lists drawn as dotted purple outlines; dirty:
    indices into classes that get a 'dirty' tag; labels: {class index: text};
    edge_hl: (parent, child) pairs drawn as orange arrows."""
    labels = labels or {}
    edge_hl = set(edge_hl)
    # class boxes
    for ci, (members, key) in enumerate(classes):
        fill, line = CLASS_STYLE[key]
        bx, by, bw, bh = _bbox(members, 0.13)
        add_rect(slide, ox + bx, oy + by, bw, bh, fill=fill, line=line, width=1.5,
                 dash=MSO_LINE.DASH, radius=0.25)
        if ci in labels:
            add_text(slide, labels[ci], ox + bx - 0.05, oy + by - 0.36, bw + 0.4, 0.32,
                     size=12, bold=True, color=line)
        if ci in dirty:
            ty = oy + by + bh - 0.12 if key == 'leaf' else oy + by - 0.14
            add_rect(slide, ox + bx + bw - 0.52, ty, 0.56, 0.26, fill=WHITE,
                     line=RED, width=1.25, radius=0.5, text='dirty', size=9.5, bold=True,
                     color=RED)
    # candidate groups
    for members in groups:
        bx, by, bw, bh = _bbox(members, 0.06)
        add_rect(slide, ox + bx, oy + by, bw, bh, fill=None, line=PURPLE, width=1.75,
                 dash=MSO_LINE.ROUND_DOT, radius=0.3)
    # edges: plain first, highlighted on top
    for wanted in (False, True):
        for parent, kids in EDGES.items():
            px, py = NODES[parent][2], NODES[parent][3]
            ph = nsize(parent)[1]
            for k in kids:
                if ((parent, k) in edge_hl) != wanted:
                    continue
                kx, ky = NODES[k][2], NODES[k][3]
                kh = nsize(k)[1]
                # stop above an outside label so the line never crosses the name
                ktop = ky - kh / 2 - (LAB_UP + 0.01 if lpos(k) == 'above' else 0)
                col = ORANGE if wanted else (LIGHT if (parent in dim or k in dim) else EDGE)
                add_line(slide, ox + px, oy + py + ph / 2, ox + kx, oy + ktop,
                         color=col, width=2.5 if wanted else 1.25, arrow=wanted)
    # nodes
    for nid, (lab, sym, cx, cy) in NODES.items():
        w, h = nsize(nid)
        hl = nid in highlight
        shp = add_rect(slide, ox + cx - w / 2, oy + cy - h / 2, w, h,
                       fill=(AMBER_FILL if hl else WHITE),
                       line=(AMBER if hl else RGBColor(0x4A, 0x4F, 0x57)),
                       width=(2.75 if hl else 1.0), radius=0.2)
        tf = shp.text_frame
        tf.margin_top = tf.margin_bottom = Inches(0.0)
        txtcol = LIGHT if nid in dim else INK
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        add_runs(p, sym if sym else lab, 16 if sym else 14, color=txtcol, bold=True)
        where = lpos(nid)
        if where == 'above':
            add_text(slide, lab, ox + cx - 0.45, oy + cy - h / 2 - LAB_UP + 0.01, 0.9, 0.28,
                     size=13, bold=True, color=txtcol, align=PP_ALIGN.CENTER,
                     anchor=MSO_ANCHOR.MIDDLE)
        elif where == 'right':
            add_text(slide, lab, ox + cx + w / 2 + 0.02, oy + cy - 0.15, 0.35, 0.3,
                     size=13, bold=True, color=txtcol, anchor=MSO_ANCHOR.MIDDLE)
        elif where == 'left':
            add_text(slide, lab, ox + cx - w / 2 - LAB_RT + 0.01, oy + cy - 0.15, 0.35, 0.3,
                     size=13, bold=True, color=txtcol, align=PP_ALIGN.RIGHT,
                     anchor=MSO_ANCHOR.MIDDLE)

EQ_PAIRS = [('r', 'rp'), ('s', 'sp'), ('c', 'cp'), ('u', 'up'), ('v', 'vp')]

def query_mark(slide, ox, oy=OY, sym='=?', color=ORANGE):
    """The query, drawn in the gap between the two ITE nodes."""
    mid = (NODES['m1'][2] + NODES['m2'][2]) / 2.0
    add_text(slide, 'Query', ox + mid - 0.55, oy + ITE - 0.66, 1.1, 0.3, size=12,
             bold=True, color=GRAY, align=PP_ALIGN.CENTER)
    add_text(slide, sym, ox + mid - 0.55, oy + ITE - 0.26, 1.1, 0.52, size=24, bold=True,
             color=color, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

def union_mark(slide, ox, a, b, oy=OY):
    """A union symbol in the gap between two nodes on the same row."""
    mid = (NODES[a][2] + NODES[b][2]) / 2.0
    add_text(slide, '\u222a', ox + mid - 0.4, oy + NODES[a][3] - 0.3, 0.8, 0.6, size=22,
             bold=True, color=ORANGE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

ROUND_ROWS = [(['r', 'rp', 's', 'sp', 'c', 'cp', 'u', 'up', 'v', 'vp'], 'round 0'),
              (['a1', 'a2', 'x1', 'x2'], 'round 1'), (['m1', 'm2'], 'round 2')]

def round_bands(slide, ox, oy=OY):
    """A labelled ring around each round of the schedule."""
    for ids, lab in ROUND_ROWS:
        bx, by, bw, bh = _bbox(ids, 0.27)
        add_rect(slide, ox + bx, oy + by, bw, bh, fill=None, line=NAVY, width=2.25,
                 dash=MSO_LINE.LONG_DASH, radius=0.35)
        add_text(slide, lab, ox + bx + bw + 0.1, oy + by + bh / 2 - 0.2, 1.3, 0.4, size=16,
                 bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)

def eq_marks(slide, ox, oy=OY, sym='='):
    """A symbol under every pair of input wires tied by E, below the class boxes."""
    for a, b in EQ_PAIRS:
        mid = (NODES[a][2] + NODES[b][2]) / 2.0
        add_text(slide, sym, ox + mid - 0.35, oy + LEAF + LH / 2 + 0.14, 0.7, 0.5,
                 size=(32 if sym == '=' else 24), bold=True, color=ORANGE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

def banner(slide, text, size=26):
    """Full-width takeaway strip under a centred diagram."""
    add_rect(slide, 0.6, 6.12, 12.1, 0.76, fill=NAVY, line=None, text=text, size=size,
             bold=True, color=WHITE)

def par_mark(slide, ox, oy=OY):
    """The independence symbol between the AND merge and the XOR merge."""
    ax = _bbox(A_CLASS[0], 0.13)
    xx = _bbox(X_CLASS[0], 0.13)
    mid = ((ax[0] + ax[2]) + xx[0]) / 2.0
    add_text(slide, '\u2225', ox + mid - 0.45, oy + GATE - 0.42, 0.9, 0.62, size=40,
             bold=True, color=ORANGE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, 'independent', ox + mid - 0.75, oy + GATE + 0.24, 1.5, 0.3, size=13,
             bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

def side_panel(slide, heading, items, x=8.95, y=1.5, w=4.05, size=16):
    add_text(slide, heading, x, y, w, 0.45, size=18, bold=True, color=NAVY)
    add_bullets(slide, items, x, y + 0.45, w, 5.2, size=size, gap=5)

def legend(slide, entries, x=0.55, y=6.45):
    """entries: list of (kind, text) with kind in {'hl','group','class'}"""
    cx = x
    for kind, text in entries:
        if kind == 'hl':
            add_rect(slide, cx, y + 0.05, 0.36, 0.24, fill=AMBER_FILL, line=AMBER, width=2)
        elif kind == 'group':
            add_rect(slide, cx, y + 0.05, 0.36, 0.24, fill=None, line=PURPLE, width=1.75,
                     dash=MSO_LINE.ROUND_DOT)
        else:
            f, l = CLASS_STYLE['a']
            add_rect(slide, cx, y + 0.05, 0.36, 0.24, fill=f, line=l, width=1.5, dash=MSO_LINE.DASH)
        add_text(slide, text, cx + 0.42, y, 2.4, 0.35, size=12, color=GRAY)
        cx += 0.42 + 0.12 * len(text) + 0.35

# ================================================================ slides
# 1 ---- title
s = new_slide(number=False, notes=(
    'Title. Joint work with Amar Shah, equal contribution. I will cover the problem, '
    'the two algorithms, and implementation; Amar covers the evaluation.'))
add_rect(s, 0, 0, 13.333, 7.5, fill=NAVY, line=None, rounded=False)
add_line(s, 0.9, 3.55, 4.2, 3.55, color=ORANGE, width=3)
add_text(s, 'Parallelizing Congruence Closure', 0.85, 2.2, 11.5, 1.3, size=44, bold=True,
         color=WHITE, anchor=MSO_ANCHOR.BOTTOM)
add_text(s, 'Zachary Kent*   ·   Amar Shah*', 0.85, 3.75, 11, 0.6, size=24, color=WHITE)
add_text(s, 'Carnegie Mellon University', 0.85, 4.35, 11, 0.5, size=20,
         color=RGBColor(0xC9, 0xD3, 0xE6))
add_text(s, 'FMCAD 2026', 0.85, 5.0, 11, 0.5, size=20, color=RGBColor(0xC9, 0xD3, 0xE6))
add_text(s, '* equal contribution', 0.85, 6.6, 6, 0.4, size=13, color=RGBColor(0x9A, 0xA8, 0xC4))
add_text(s, 'github.com/amarshah10/ParallelEgraph', 7.3, 6.6, 5.6, 0.4, size=13,
         color=RGBColor(0x9A, 0xA8, 0xC4), align=PP_ALIGN.RIGHT)

# 2 ---- what is congruence closure
s = new_slide('Congruence closure', notes=(
    'Define the problem in words: given equalities between terms over uninterpreted functions, '
    'compute the smallest equivalence relation containing them that is closed under this one '
    'rule. Equal arguments give equal applications. The example: transitivity gives a and c '
    'equal, congruence gives f(a) and f(c) equal, which refutes the disequality. The standard '
    'engine is a union-find plus a signature table, an e-graph, and every implementation we '
    'know of is sequential.'))
add_rect(s, 0.8, 1.7, 5.6, 3.3, fill=RGBColor(0xF4, 0xF5, 0xF7), line=None)
add_text(s, 'Congruence rule', 1.0, 1.78, 3, 0.35, size=13, bold=True, color=GRAY)
add_text(s, 's₁ ≡ t₁    …    sₖ ≡ tₖ', 1.0, 2.6, 5.2, 0.6, size=28, align=PP_ALIGN.CENTER)
add_line(s, 1.5, 3.35, 5.7, 3.35, color=INK, width=1.75)
add_text(s, 'f(s₁, …, sₖ) ≡ f(t₁, …, tₖ)', 1.0, 3.5, 5.2, 0.6, size=28, align=PP_ALIGN.CENTER)
add_rect(s, 7.0, 1.7, 5.5, 3.3, fill=RGBColor(0xF4, 0xF5, 0xF7), line=None)
add_text(s, 'Example', 7.2, 1.78, 3, 0.35, size=13, bold=True, color=GRAY)
add_text(s, 'a = b      b = c      f(a) ≠ f(c)', 7.2, 2.6, 5.1, 0.6, size=26, bold=True,
         align=PP_ALIGN.CENTER)
add_text(s, 'a ≡ c   ⇒   f(a) ≡ f(c)', 7.2, 3.5, 5.1, 0.6, size=26, align=PP_ALIGN.CENTER)
banner(s, 'Smallest equivalence relation containing E, closed under congruence', size=22)
add_text(s, 'Nelson & Oppen 1980   ·   Downey, Sethi & Tarjan 1980   ·   Nieuwenhuis & Oliveras 2007',
         0.8, 5.35, 12, 0.35, size=12, color=GRAY, align=PP_ALIGN.CENTER)

# 3 ---- why it matters
s = new_slide('Where congruence closure runs', notes=(
    'It is a core, performance-critical component in many engines and hence in the '
    'applications built on them. Decades of engineering have gone into sequential '
    'implementations.'))
add_text(s, 'Engines', 0.7, 1.5, 5, 0.45, size=22, bold=True, color=NAVY)
add_bullets(s, [
    '**SMT solvers**: Z3, cvc5 (theory of uninterpreted functions)',
    '**SAT solvers**: Kissat (clausal congruence closure)',
    '**Equality saturation**: egg, egglog',
    '**Type unification**',
], 0.6, 2.0, 5.9, 4, size=19)
add_text(s, 'Applications', 6.95, 1.5, 5, 0.45, size=22, bold=True, color=NAVY)
add_bullets(s, [
    '**Circuit equivalence checking**',
    '**Software verification**: Dafny, Verus',
    '**Hardware design**',
    '**Theorem proving**: Lean grind',
], 6.85, 2.0, 5.9, 4, size=19)
add_rect(s, 0.6, 4.7, 12.1, 1.0, fill=RGBColor(0xF4, 0xF5, 0xF7), line=None,
         text='Performance critical: called millions of times inside a solver run', size=20,
         bold=True, color=NAVY)

# 4 ---- the gap
s = new_slide('Sequential in practice, hard in theory', notes=(
    'Every implementation we know of is sequential, and machines are wide: our test box has '
    '96 cores. Theory is discouraging. Congruence closure is P-complete, so a polylog-span '
    'algorithm is not expected; worst-case instances force a long chain of dependent merges. '
    'The question we ask is whether the instances people actually solve behave like the worst case.'))
add_text(s, 'every implementation: sequential', 0.8, 1.9, 12, 0.7, size=30, bold=True, color=NAVY,
         align=PP_ALIGN.CENTER)
add_text(s, 'P-complete', 0.8, 3.0, 12, 0.7, size=30, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
add_text(s, 'Kanellakis & Revesz 1989', 0.8, 3.65, 12, 0.35, size=13, color=GRAY, align=PP_ALIGN.CENTER)
add_rect(s, 0.6, 4.9, 12.1, 1.2, fill=NAVY, line=None,
         text='Do practical instances expose enough independent merges?',
         size=24, bold=True, color=WHITE)

# 5 ---- contributions
s = new_slide('Contributions', notes=(
    'Three contributions plus open-source code. Emphasize that the algorithms replace the '
    'sequential worklist with bulk-synchronous rounds.'))
rows = [
    ('1', 'Two parallel algorithms: ParentCC and FilterCC',
     'bulk-synchronous rounds of data-parallel primitives over a lock-free concurrent union-find'),
    ('2', 'Workload characterization: congruence depth and width',
     'width, the number of independent merges per round, is the dominant factor empirically'),
    ('3', 'Evaluation on random, synthetic, and circuit-equivalence benchmarks',
     'near-linear speedup up to 32 cores over a tuned sequential baseline'),
    ('4', 'Open source implementation and benchmarks',
     'github.com/amarshah10/ParallelEgraph'),
]
y = 1.55
for num, head, sub in rows:
    add_rect(s, 0.7, y + 0.05, 0.62, 0.62, fill=ORANGE, line=None, radius=0.5, text=num,
             size=20, bold=True, color=WHITE)
    add_text(s, head, 1.55, y - 0.02, 11, 0.5, size=22, bold=True, color=NAVY)
    add_text(s, sub, 1.55, y + 0.45, 11, 0.5, size=17, color=GRAY)
    y += 1.3

# 6 ---- setting: miters and the term grammar
s = new_slide('Setting: combinational equivalence checking', notes=(
    'Where the running example comes from. A miter feeds the same inputs to two circuits, '
    'XORs the corresponding outputs, and asserts the result is 1. The circuits agree on '
    'every input exactly when that assertion is unsatisfiable. Encoding a miter to CNF '
    'destroys the gate structure, so Biere et al. recover the gates and close them under '
    'congruence, which often decides the instance outright. Gates become terms under this '
    'grammar: input wires are leaves, every gate is a function symbol applied to its inputs.'))
# --- miter block diagram ---
add_rect(s, 2.05, 5.72, 3.1, 0.45, fill=RGBColor(0xEE, 0xF0, 0xF3), line=RGBColor(0x9A, 0xA0, 0xA8),
         width=1.25, text='shared inputs  r, s, u, v, c', size=13)
CB = RGBColor(0xDC, 0xEA, 0xF8)
add_rect(s, 1.55, 4.35, 1.7, 0.85, fill=CB, line=RGBColor(0x2E, 0x6F, 0xB0), width=1.5,
         text='**C\u2081**', size=19, color=NAVY)
add_rect(s, 3.95, 4.35, 1.7, 0.85, fill=CB, line=RGBColor(0x2E, 0x6F, 0xB0), width=1.5,
         text='**C\u2082**', size=19, color=NAVY)
add_line(s, 2.40, 5.72, 2.40, 5.20, arrow=True)
add_line(s, 4.80, 5.72, 4.80, 5.20, arrow=True)
add_rect(s, 2.80, 2.95, 1.6, 0.72, fill=RGBColor(0xFB, 0xE4, 0xD3), line=ORANGE, width=1.5,
         text='**XOR**', size=17, color=NAVY)
add_line(s, 2.40, 4.35, 3.20, 3.67, arrow=True)
add_line(s, 4.80, 4.35, 4.00, 3.67, arrow=True)
add_text(s, 'm\u2081', 2.38, 3.85, 0.5, 0.3, size=14, bold=True, color=GRAY)
add_text(s, 'm\u2082', 4.52, 3.85, 0.5, 0.3, size=14, bold=True, color=GRAY)
add_line(s, 3.60, 2.95, 3.60, 2.45, arrow=True)
add_text(s, 'p', 3.30, 2.08, 0.5, 0.35, size=16, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
add_rect(s, 4.00, 2.05, 1.85, 0.42, fill=NAVY, line=None, text='assert p = 1', size=14,
         bold=True, color=WHITE)
# --- right column ---
add_bullets(s, [
    '#Miter',
    'two circuits, same inputs',
    'XOR the corresponding outputs',
    'p = 1  \u27fa  the circuits disagree',
    '**equivalent  \u27fa  p = 1 unsatisfiable**',
], 6.25, 1.42, 6.5, 2.2, size=18, gap=5)
add_rect(s, 6.35, 3.45, 6.35, 1.45, fill=RGBColor(0xF4, 0xF5, 0xF7), line=None)
add_text(s, 'Terms', 6.55, 3.52, 3, 0.35, size=15, bold=True, color=NAVY)
gb = s.shapes.add_textbox(Inches(6.55), Inches(3.86), Inches(6.0), Inches(1.0))
gtf = gb.text_frame
gtf.word_wrap = False
for i, (code_, note) in enumerate([
        ('t  ::=  x', 'leaf: an input wire'),
        ('   |   f(t\u2081, \u2026, t\u2096)', 'gate: f \u2208 F,  arity k'),
        ('F = {AND, OR, XOR, ITE, \u2026}', '')]):
    par = gtf.paragraphs[0] if i == 0 else gtf.add_paragraph()
    par.space_after = Pt(2)
    add_runs(par, code_.ljust(22), 14, font=MONO)
    if note:
        add_runs(par, note, 13, color=GRAY)

# 7 ---- running example: the miter
s = new_slide('Running example: a miter', notes=(
    'Miter adapted from Biere et al., Clausal Congruence Closure, SAT 2024. Two copies of '
    'the same three-gate circuit, side by side. Each copy has its own input wires. Nodes '
    'are terms, one per gate; edges point to children. Say out loud that the left half is '
    'copy one and the right half is copy two, and that the two ITE gates at the top are the '
    'two outputs.'))
draw_egraph(s, ox=OX_FULL)

# 8 ---- the query
s = new_slide('Running example: the query', notes=(
    'Assert that the two outputs differ. If that is unsatisfiable the circuits are '
    'equivalent. The query is the only thing on the slide, sitting between the two output '
    'gates.'))
draw_egraph(s, ox=OX_FULL, highlight=['m1', 'm2'])
query_mark(s, OX_FULL)

# 9 ---- the input equalities
s = new_slide('Running example: input equalities', notes=(
    'The equalities tie the two copies together: each input wire of copy one equals the '
    'corresponding wire of copy two. These are the only given equalities, and they are what '
    'we union first.'))
draw_egraph(s, ox=OX_FULL, highlight=['r', 'rp', 's', 'sp', 'c', 'cp', 'u', 'up', 'v', 'vp'])
eq_marks(s, OX_FULL)

# 10 ---- reading the diagram: one node, one term
FOCUS = ['m2', 'cp', 'a2', 'x2']
DIMMED = [n for n in NODES if n not in FOCUS]
M2X, M2Y = OX_FULL + NODES['m2'][2], OY + ITE
s = new_slide('Reading the diagram: one node, one term', notes=(
    'Focus on a single node before the trace starts. The box carries the operator, the name '
    'sits alongside, and the three outgoing edges are its children in argument order. '
    'Everything else is greyed out so only this term and its children are in view.'))
draw_egraph(s, ox=OX_FULL, highlight=['m2'],
            edge_hl=[('m2', 'cp'), ('m2', 'a2'), ('m2', 'x2')], dim=DIMMED)
add_rect(s, M2X + 0.75, 1.22, 2.5, 0.46, fill=AMBER_FILL, line=AMBER, width=1.5,
         text='m\u2082 = ITE(c\u2032, a\u2082, x\u2082)', size=15, bold=True)
add_line(s, M2X + 0.75, 1.45, M2X + 0.22, M2Y - GH / 2 - 0.02, color=AMBER, width=2.25,
         arrow=True)

# 11 ---- parent and children
s = new_slide('Reading the diagram: parent and children', notes=(
    'Name the relationship the algorithms are built around. An edge goes from a term to the '
    'arguments it is applied to. m2 is the parent, its three arguments are the children. '
    'Every term is the parent of its arguments and a child of every term that mentions it.'))
draw_egraph(s, ox=OX_FULL, highlight=['m2'],
            edge_hl=[('m2', 'cp'), ('m2', 'a2'), ('m2', 'x2')], dim=DIMMED)
add_text(s, 'parent', M2X + 0.90, M2Y - 0.17, 0.9, 0.34, size=17, bold=True, color=ORANGE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
for kid, dx, dy in [('cp', 0.0, 0.42), ('a2', 0.88, 0.0), ('x2', 0.88, 0.0)]:
    kx, ky = OX_FULL + NODES[kid][2], OY + NODES[kid][3]
    add_text(s, 'child', kx + dx - 0.45, ky + dy - 0.16, 0.9, 0.32, size=15, bold=True,
             color=ORANGE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# 10-13 ---- sequential walkthrough
s = new_slide('Congruence closure by hand: step 0', notes=(
    'Start from the given equalities.'))
draw_egraph(s)
eq_marks(s, OX)

s = new_slide('Congruence closure by hand: step 0', notes=(
    'Union each pair. The dashed boxes are the equivalence classes.'))
draw_egraph(s, classes=LEAF_CLASSES)
eq_marks(s, OX, sym='∪')

s = new_slide('Congruence closure by hand: step 1', notes=(
    'Examine the two AND gates. Same symbol, and their children are pairwise in the same '
    'class, so the congruence rule applies. Yellow means we are looking at them.'))
draw_egraph(s, classes=LEAF_CLASSES, highlight=['a1', 'a2'])

s = new_slide('Congruence closure by hand: step 1', notes=(
    'Congruence fires, so union the two classes.'))
draw_egraph(s, classes=LEAF_CLASSES + [A_CLASS], highlight=['a1', 'a2'])
union_mark(s, OX, 'a1', 'a2')

s = new_slide('Congruence closure by hand: step 2', notes=(
    'Examine the two XOR gates: same symbol, children pairwise equivalent.'))
draw_egraph(s, classes=LEAF_CLASSES + [A_CLASS], highlight=['x1', 'x2'])

s = new_slide('Congruence closure by hand: step 2', notes=('Union them.'))
draw_egraph(s, classes=LEAF_CLASSES + [A_CLASS, X_CLASS], highlight=['x1', 'x2'])
union_mark(s, OX, 'x1', 'x2')

s = new_slide('Congruence closure by hand: step 3', notes=(
    'Examine the two ITE gates. Only now are their children pairwise equivalent, because '
    'steps 1 and 2 merged the AND and XOR classes.'))
draw_egraph(s, classes=LEAF_CLASSES + [A_CLASS, X_CLASS], highlight=['m1', 'm2'])

s = new_slide('Congruence closure by hand: step 3', notes=(
    'Union them. Note that step 3 depended on steps 1 and 2, but 1 and 2 did not depend on '
    'each other.'))
draw_egraph(s, classes=LEAF_CLASSES + [A_CLASS, X_CLASS, M_CLASS], highlight=['m1', 'm2'])
union_mark(s, OX, 'm1', 'm2')

s = new_slide('Congruence closure by hand: query answered', notes=(
    'The outputs are in one class, so the query m1 differs from m2 is unsatisfiable: the '
    'circuits are equivalent.'))
draw_egraph(s, classes=LEAF_CLASSES + [A_CLASS, X_CLASS, M_CLASS], highlight=['m1', 'm2'])
query_mark(s, OX, sym='=', color=RGBColor(0x3A, 0x9A, 0x5B))

# 15 ---- observation: depth and width
s = new_slide('Observation: what does a merge wait on?', notes=(
    'The pivot of the talk. Go back over the trace we just did and ask what forced its '
    'order. The ITE merge waited for the AND merge and the XOR merge, and for nothing else. '
    'Why: congruence tests the classes of the children, so a term can only become mergeable '
    'when one of its children changes class. That is exactly an edge of the diagram, '
    'traversed upward. Dependences in congruence closure are not hidden in a data structure, '
    'they are the term structure itself, which is what makes the problem tractable to '
    'parallelize. Say the caveat out loud rather than putting it on the slide: a child can '
    'also change class through a chain of earlier merges, so the dependence is the '
    'transitive closure of the parent-child relation.'))
draw_egraph(s, ox=OX_FULL, classes=LEAF_CLASSES + [A_CLASS, X_CLASS, M_CLASS],
            highlight=['m1', 'm2'],
            edge_hl=[('m1', 'a1'), ('m1', 'x1'), ('m2', 'a2'), ('m2', 'x2')])
banner(s, 'Data dependences are parent\u2013child edges')

s = new_slide('Observation: unrelated merges do not wait', notes=(
    'The other half. Nothing connects the AND merge to the XOR merge: neither is an '
    'ancestor of the other, so neither can change the other\u2019s signature. They can run '
    'at the same time, on different cores, in either order, with the same result. That is '
    'the parallelism we are after, and the algorithms are built to find all of it at once '
    'instead of one merge at a time.'))
draw_egraph(s, ox=OX_FULL, classes=LEAF_CLASSES + [A_CLASS, X_CLASS, M_CLASS],
            highlight=['a1', 'a2', 'x1', 'x2'])
par_mark(s, OX_FULL)
banner(s, 'Unrelated merges run in parallel')

s = new_slide('The structure induces a bulk-synchronous schedule', notes=(
    'Read the dependences as a schedule. Everything with no unmet dependence goes in the '
    'current round, all at once; a barrier; then everything the round just enabled. Round 0 '
    'is the input equalities, round 1 the two gate merges, round 2 the output merge. This is '
    'Valiant’s bulk-synchronous model, and it falls straight out of the term structure.'))
draw_egraph(s, classes=LEAF_CLASSES + [A_CLASS, X_CLASS, M_CLASS])
round_bands(s, OX)
banner(s, 'Bulk-synchronous parallel: rounds of independent merges')

s = new_slide('The structure induces a bulk-synchronous schedule', notes=(
    'Two names for the evaluation. Depth is the number of rounds, width the merges available '
    'in one round. Here both are 2. On the circuit benchmarks width reaches millions while '
    'depth stays small, and Amar will show that width is what predicts speedup.'))
draw_egraph(s, classes=LEAF_CLASSES + [A_CLASS, X_CLASS, M_CLASS])
round_bands(s, OX)
banner(s, 'depth: number of rounds        width: merges per round', size=22)

# ---- two questions per round
s = new_slide('Two questions per round, two primitives', notes=(
    'The schedule tells us when. Two questions remain about how. First, how do we find every '
    'merge a round allows, all at once, rather than one at a time? Semisort: compute each '
    'term’s signature, the symbol plus the classes of its children, and group equal '
    'signatures together; every group is a set of congruent terms. Second, how do we perform '
    'thousands of unions from many threads and still end up with the right classes? A '
    'concurrent union-find: lock-free, linearizable, so the result is the same as if the '
    'unions had happened one after another. Both come from the parallel algorithms '
    'literature and both are in ParlayLib.'))
QA = [
    ('How do we find all the merges of a round?',
     'after one Find per child, congruence is equality of a key',
     'semisort by that key',
     'Gu, Shun, Sun & Blelloch, SPAA 2015'),
    ('How do we run thousands of unions at once, correctly?',
     'the partition a set of unions produces does not depend on their order',
     'lock-free concurrent union-find, no coordination',
     'Alistarh, Fedorov & Koval, OPODIS 2019'),
]
y = 1.55
for q, insight, prim, cite in QA:
    add_text(s, q, 0.8, y, 11.8, 0.55, size=24, bold=True, color=NAVY)
    add_text(s, 'insight', 1.4, y + 0.7, 1.3, 0.4, size=13, bold=True, color=GRAY,
             anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, insight, 2.7, y + 0.66, 9.4, 0.5, size=19, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, 'so apply', 1.4, y + 1.25, 1.3, 0.55, size=13, bold=True, color=GRAY,
             anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, 2.7, y + 1.22, 9.4, 0.62, fill=RGBColor(0xFB, 0xE4, 0xD3), line=ORANGE,
             width=1.5, text=prim, size=20, bold=True)
    add_text(s, cite, 2.7, y + 1.86, 9.4, 0.3, size=11, color=GRAY, align=PP_ALIGN.RIGHT)
    y += 2.65

# ---- ParentCC, one round
s = new_slide('ParentCC: one round', notes=(
    'Now the algorithm, at the level of a round. Three phases. Who might have become '
    'congruent? Only a term whose child just changed class, so: the parents of whatever merged '
    'last round. Of those, who actually is congruent? Group them by signature. Then merge '
    'every group, in parallel. Repeat while a round merged something. The very first round '
    'has no previous merges to look at, so it considers every term; that also catches terms '
    'that were congruent before any equality was applied.'))
PH = [
    ('1', 'Who might have become congruent?', 'the parents of last round’s merges',
     RGBColor(0xDC, 0xEA, 0xF8), RGBColor(0x2E, 0x6F, 0xB0)),
    ('2', 'Who actually is?', 'group them by signature',
     RGBColor(0xEA, 0xE2, 0xF5), PURPLE),
    ('3', 'Merge', 'every group, in parallel',
     RGBColor(0xFB, 0xE4, 0xD3), ORANGE),
]
PW, PHT = 3.6, 2.7
px = [0.75, 4.87, 8.99]
py = 1.85
for (num, q, a, fill, line), x in zip(PH, px):
    add_rect(s, x, py, PW, PHT, fill=fill, line=line, width=1.5)
    add_rect(s, x + 0.2, py + 0.2, 0.5, 0.5, fill=line, line=None, radius=0.5, text=num,
             size=16, bold=True, color=WHITE)
    add_text(s, q, x + 0.2, py + 0.85, PW - 0.4, 0.85, size=17, color=GRAY, align=PP_ALIGN.CENTER)
    add_text(s, a, x + 0.2, py + 1.75, PW - 0.4, 0.8, size=19, bold=True, color=NAVY,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
for i in range(2):
    add_line(s, px[i] + PW, py + PHT / 2, px[i + 1], py + PHT / 2, color=INK, width=2.0, arrow=True)
# loop back
ly = py + PHT + 0.55
add_line(s, px[2] + PW / 2, py + PHT, px[2] + PW / 2, ly, color=INK, width=2.0)
add_line(s, px[2] + PW / 2, ly, px[0] + PW / 2, ly, color=INK, width=2.0)
add_line(s, px[0] + PW / 2, ly, px[0] + PW / 2, py + PHT, color=INK, width=2.0, arrow=True)
add_text(s, 'repeat while a round merged something', 3.6, ly + 0.05, 6.1, 0.4, size=16,
         bold=True, color=NAVY, align=PP_ALIGN.CENTER)
add_text(s, 'first round: consider every term', 0.75, ly + 0.55, 11.8, 0.4, size=15, color=GRAY,
         align=PP_ALIGN.CENTER)

# ---- ParentCC on the example
FRONT1 = ['a1', 'a2', 'x1', 'x2', 'm1', 'm2']

def sig_key(slide, ox, ids, text, dy, oy=OY):
    """The grouping key written above a signature group; [t] means the class of t."""
    bx, by, bw, bh = _bbox(ids, 0.06)
    add_text(slide, text, ox + bx + bw / 2 - 1.2, oy + by + dy, 2.4, 0.3, size=11.5, bold=True,
             color=PURPLE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

s = new_slide('ParentCC on the example: round 1', notes=(
    'After the input unions, the first round considers every gate. Each gets a key: its symbol '
    'and the class of each child, written here in brackets. Equal keys group together: the '
    'ANDs match, the XORs match, the ITEs do not yet because a1 and a2 are still in different '
    'classes. The grouping is the semisort.'))
draw_egraph(s, classes=LEAF_CLASSES, highlight=FRONT1,
            groups=[['a1', 'a2'], ['x1', 'x2'], ['m1'], ['m2']])
sig_key(s, OX, ['a1', 'a2'], 'AND([r], [s])', -0.3)
sig_key(s, OX, ['x1', 'x2'], 'XOR([u], [v])', -0.3)
sig_key(s, OX, ['m1'], 'ITE([c], [a₁], [x₁])', -0.3)
sig_key(s, OX, ['m2'], 'ITE([c], [a₂], [x₂])', -0.3)

s = new_slide('ParentCC on the example: round 1', notes=(
    'Both two-member groups merge, concurrently. This is the slide that differs from the hand '
    'trace: two unions in one round.'))
draw_egraph(s, classes=LEAF_CLASSES + [A_CLASS, X_CLASS], highlight=['a1', 'a2', 'x1', 'x2'])
union_mark(s, OX, 'a1', 'a2')
union_mark(s, OX, 'x1', 'x2')

s = new_slide('ParentCC on the example: round 2', notes=(
    'Candidates are the parents of what just merged: the two ITEs. Their keys now agree, so '
    'they merge. They have no parents, so round 3 has no candidates and the loop stops. Three '
    'rounds instead of eight sequential merges.'))
draw_egraph(s, classes=LEAF_CLASSES + [A_CLASS, X_CLASS, M_CLASS], highlight=['m1', 'm2'],
            groups=[['m1', 'm2']])
sig_key(s, OX, ['m1', 'm2'], 'ITE([c], [a₁], [x₁])', -0.5)
union_mark(s, OX, 'm1', 'm2')

# ---- pseudocode
s = new_slide('ParentCC pseudocode', notes=(
    'The same three phases, precisely. Work is the set of classes that changed last round; the '
    'frontier is their parents; groups come from a semisort on signatures; each group merges by '
    'divide and conquer. Barriers separate the phases, so signatures are always computed '
    'against a union-find no thread is modifying. This slide is for the record; do not read it.'))
code = [
    ('ParentCC(E):', 0),
    ('parfor (u = v) ∈ E:  Union(u, v)', 1),
    ('Work ← terms of E', 1),
    ('while Work ≠ ∅:', 1),
    ('parfor c ∈ Work with c ≠ Find(c):                 ▹ fold parent lists', 2),
    ('Parents[Find(c)] ← Parents[Find(c)] ∪ Parents[c]', 3),
    ('Frontier ← all compound terms          on round 0   ▹ seed round', 2),
    ('Frontier ← ⋃ Parents[Find(c)] for c ∈ Work   otherwise', 2),
    ('groups ← GroupBy(Congruent, Frontier)          ▹ semisort on sigs', 2),
    ('Work ← ∅', 2),
    ('parfor g ∈ groups spanning > 1 class:', 2),
    ('MergeCongruenceClass(g)                          ▹ parallel unions', 3),
    ('Work ← Work ∪ pre-merge roots of g', 3),
    ('', 0),
    ('MergeCongruenceClass(S):                             ▹ divide and conquer', 0),
    ('if |S| = 1: return the element', 1),
    ('l, r ← MergeCongruenceClass(S[0..n/2]) ∥ MergeCongruenceClass(S[n/2..n])', 1),
    ('return Union(l, r)', 1),
]
add_rect(s, 1.6, 1.45, 10.1, 5.35, fill=RGBColor(0xF7, 0xF7, 0xF9), line=None, radius=0.05)
tb = s.shapes.add_textbox(Inches(1.9), Inches(1.55), Inches(9.6), Inches(5.2))
tf = tb.text_frame
tf.word_wrap = False
for i, (line, ind) in enumerate(code):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.space_after = Pt(1.5)
    txt = '    ' * ind + line
    if '▹' in txt:
        a, b = txt.split('▹')
        add_runs(p, a, 14, font=MONO)
        add_runs(p, '▹' + b, 14, font=MONO, color=GRAY)
    else:
        add_runs(p, txt, 14, font=MONO, bold=(ind == 0 and line != ''))

# ---- correctness
s = new_slide('Why ParentCC is correct', notes=(
    'One line each; the paper has the proofs. Deterministic: the union-find is linearizable '
    'and a set of unions yields the same partition in any order. Terminates: a round that '
    'merges anything reduces the number of classes. Sound: every group has equal symbol and '
    'equal child classes, so each merge is an instance of the congruence rule. Complete: '
    'when the last of a pair’s children merge, both parents are candidates next round.'))
props = [
    ('Deterministic', 'same classes whatever the thread order'),
    ('Terminates', 'every productive round removes a class'),
    ('Sound', 'each merge is an instance of the congruence rule'),
    ('Complete', 'a newly congruent pair is a candidate next round'),
]
y = 1.7
for head, line in props:
    add_rect(s, 0.8, y, 3.2, 0.9, fill=NAVY, line=None, text=head, size=21, bold=True, color=WHITE)
    add_rect(s, 4.0, y, 8.5, 0.9, fill=RGBColor(0xF4, 0xF5, 0xF7), line=None, rounded=False,
             text=line, size=20)
    y += 1.15

# ---- FilterCC
s = new_slide('FilterCC: drop the parent lists', notes=(
    'Parent lists cost allocation: every round appends lists. FilterCC keeps one dirty bit '
    'per class instead and recomputes the candidates by filtering all terms for a child in a '
    'dirty class. It touches every term each round, but the filter is a cheap parallel scan '
    'with no allocation. Which wins depends on how many rounds the input needs; Amar has the numbers.'))
add_text(s, 'Same rounds, different way to find the candidates', 0.8, 1.55, 12, 0.5, size=22,
         bold=True, color=NAVY)
tx, ty = 0.8, 2.4
cols = [('', 2.6), ('ParentCC', 4.6), ('FilterCC', 4.6)]
rowsT = [
    ('remember', 'parent list per class', 'one dirty bit per class'),
    ('candidates', 'parents of last round’s merges', 'filter all terms for a dirty child'),
    ('cost per round', '∝ candidates, plus allocation', '∝ all terms, no allocation'),
    ('wins when', 'many rounds', 'few rounds'),
]
cx = tx
for name, w in cols:
    add_rect(s, cx, ty, w - 0.06, 0.6, fill=NAVY, line=None, rounded=False, text=name, size=18,
             bold=True, color=WHITE)
    cx += w
ry = ty + 0.66
for row in rowsT:
    cx = tx
    for (name, w), val in zip(cols, row):
        add_rect(s, cx, ry, w - 0.06, 0.72, fill=RGBColor(0xF4, 0xF5, 0xF7), line=None,
                 rounded=False, text=val, size=17, bold=(name == ''),
                 color=(NAVY if name == '' else INK))
        cx += w
    ry += 0.78

# ---- FilterCC on the example
s = new_slide('FilterCC on the example: round 1', notes=(
    'First round: every gate is a candidate, exactly as in ParentCC. Groups and merges are the '
    'same; afterwards the two merged classes are marked dirty.'))
draw_egraph(s, classes=LEAF_CLASSES, highlight=FRONT1, dirty=[0, 1, 2, 3, 4],
            groups=[['a1', 'a2'], ['x1', 'x2'], ['m1'], ['m2']])

s = new_slide('FilterCC on the example: round 2', notes=(
    'Only the two gate classes are dirty. Filter every term for a child in a dirty class: the '
    'two ITEs. Merge them. The next filter finds nothing, so stop.'))
draw_egraph(s, classes=LEAF_CLASSES + [A_CLASS, X_CLASS], highlight=['m1', 'm2'], dirty=[5, 6],
            groups=[['m1', 'm2']])

# ---- implementation details
s = new_slide('Implementation notes', notes=(
    'Grouping: ParlayLib integer sort on the signature hashes followed by a bucket pass per '
    'hash, which beat the library semisort on the small buckets we see. Merging a group: '
    'divide and conquer unions. The baseline is the classical worklist algorithm in the '
    'Nieuwenhuis and Oliveras variant, which is what the hand trace did: one merge at a time, '
    'each merge re-examining the parents of the losing class. We tried a topological-sort '
    'fixpoint and Downey-Sethi-Tarjan as well; the worklist was fastest. It got the same '
    'tuning care as the parallel code, so speedups are against a strong baseline.'))
add_rect(s, 0.6, 1.5, 6.0, 2.6, fill=RGBColor(0xF4, 0xF5, 0xF7), line=None)
add_text(s, 'Parallel algorithms', 0.8, 1.6, 5.6, 0.45, size=21, bold=True, color=NAVY)
add_bullets(s, [
    '**grouping**: integer sort on signature hashes',
    '**merging a group**: divide-and-conquer unions',
    '**ParlayLib** for scheduling and primitives',
], 0.7, 2.25, 5.8, 3.4, size=18, gap=10)
add_rect(s, 6.85, 1.5, 5.9, 2.6, fill=RGBColor(0xF4, 0xF5, 0xF7), line=None)
add_text(s, 'Sequential baseline, tuned', 7.05, 1.6, 5.5, 0.45, size=21, bold=True, color=NAVY)
add_bullets(s, [
    '**worklist algorithm** of Nieuwenhuis & Oliveras, fastest of three variants',
    '**signature tables specialized by arity**',
    '**bump allocator**',
], 6.95, 2.25, 5.7, 3.4, size=18, gap=10)
add_text(s, 'C++ with g++ -O3.  Code and benchmarks: github.com/amarshah10/ParallelEgraph',
         0.6, 4.5, 12.2, 0.4, size=14, color=GRAY)

# 30 ---- handoff divider
s = new_slide(number=False, notes='Hand off to Amar for the evaluation.')
add_rect(s, 0, 0, 13.333, 7.5, fill=NAVY, line=None, rounded=False)
add_line(s, 0.9, 3.55, 4.2, 3.55, color=ORANGE, width=3)
add_text(s, 'Evaluation', 0.85, 2.2, 11.5, 1.3, size=44, bold=True, color=WHITE,
         anchor=MSO_ANCHOR.BOTTOM)
add_text(s, 'random, synthetic, and circuit-equivalence benchmarks', 0.85, 3.75, 11, 0.6,
         size=22, color=RGBColor(0xC9, 0xD3, 0xE6))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parallelcc-part1.pptx')
prs.save(out)
print('wrote', out, 'slides:', SLIDE_NO[0])
