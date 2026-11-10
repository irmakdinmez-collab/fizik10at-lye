#!/usr/bin/env python3
# 10. Sınıf Fizik - Enerji: "İŞ nedir?"  — keşfettiren sürüm (v2)
import sys, os, math, subprocess
import anim
from anim import (W, H, S, FPS, C, mix, clamp, ease, eio, ramp, pop, figure, ground, title, caption,
                  parts_line, wall_scene, BGC, YEL, GRY, DIM, ORN, CYN, GRN, RED, CARD, BOXC, BOXD)

anim.FONTS.update({'s': 'Lora-Variable.ttf', 'si': 'Lora-Italic-Variable.ttf'})
from PIL import ImageFont as _IF
_SYM = set('→∝✓✗')
_dj = {}
def _djf(size):
    k = max(4, int(size * S))
    if k not in _dj: _dj[k] = _IF.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', k)
    return _dj[k]
def _runs(txt):
    out = []
    for ch in txt:
        sym = ch in _SYM
        if out and out[-1][1] == sym: out[-1][0] += ch
        else: out.append([ch, sym])
    return out
_orig_text, _orig_tw = C.text, C.tw
def _tw(self, txt, size, w='b'):
    if not (set(txt) & _SYM): return _orig_tw(self, txt, size, w)
    return sum((_djf(size).getlength(r) / S) if sy else _orig_tw(self, r, size, w) for r, sy in _runs(txt))
def _text(self, x, y, txt, size, col, w='b', anchor='mm', a=1.0, sc=1.0):
    if not (set(txt) & _SYM): return _orig_text(self, x, y, txt, size, col, w, anchor, a, sc)
    if a <= 0.01 or sc <= 0.02: return
    sz = size * sc; tot = _tw(self, txt, sz, w)
    x0 = x - tot / 2 if anchor[0] == 'm' else (x - tot if anchor[0] == 'r' else x)
    for r, sy in _runs(txt):
        wd = _tw(self, r, sz, w)
        if sy: self.d.text((x0 * S, y * S), r, font=_djf(sz * 0.85), fill=mix(BGC, col, a), anchor='lm')
        else: _orig_text(self, x0, y, r, size, col, w, 'lm', a, sc)
        x0 += wd
C.text, C.tw = _text, _tw
SEP = (236, 206, 150); SEPD = (200, 176, 140)
EARTH = (52, 40, 36); SHAFT = (16, 18, 28); WATER = (52, 120, 190); STONE = (92, 82, 78)
METAL = (150, 162, 180); METD = (105, 115, 135); HORSE = (176, 124, 84)

def date_card(c, t, a0, date, sub=None, y=92):
    a = ramp(t, a0, 0.45)
    if a <= 0.01: return
    wd = max(c.tw(date, 34, 's'), c.tw(sub or '', 22, 's')) + 60
    hh = 86 if sub else 60
    c.rect(640 - wd / 2, y - 30, 640 + wd / 2, y - 30 + hh, fill=mix(BGC, (58, 44, 30), a),
           outline=mix(BGC, SEP, a), w=2, r=6)
    c.text(640, y - 2, date, 34, SEP, w='s', a=a)
    if sub: c.text(640, y + 34, sub, 22, SEPD, w='s', a=a)

def timer(c, t, a0, dur, y=625):
    a = ramp(t, a0)
    if a <= 0: return
    g = clamp((t - a0) / dur)
    c.rect(340, y, 940, y + 16, fill=CARD, r=8)
    c.rect(340, y, 340 + max(16, 600 * (1 - g)), y + 16, fill=YEL, r=8)

def pill(c, t, txt, col, y=110, a0=0.05):
    sc = pop(t, a0)
    if sc <= 0: return
    wd = c.tw(txt, 32) / 2 + 34
    c.rect(640 - wd * sc, y - 30 * sc, 640 + wd * sc, y + 30 * sc, fill=col, r=30)
    c.text(640, y + 2, txt, 32, BGC, sc=sc)

def bucket(c, cx, by, s=1.0):
    tw, bw, h = 52 * s, 40 * s, 48 * s
    c.poly([(cx - tw / 2, by - h), (cx + tw / 2, by - h), (cx + bw / 2, by), (cx - bw / 2, by)], METAL)
    c.rect(cx - tw / 2 + 4 * s, by - h + 3 * s, cx + tw / 2 - 4 * s, by - h + 11 * s, fill=CYN, r=3)
    c.line([(cx - tw / 2, by - h), (cx + tw / 2, by - h)], METD, 4 * s)
    pts = [(cx + tw / 2 * math.cos(a), by - h - 22 * s * math.sin(a)) for a in [i * math.pi / 12 for i in range(13)]]
    c.line(pts, METD, 3 * s)
    return (cx, by - h - 22 * s)

def pulley(c, cx, cy):
    c.line([(cx - 70, cy - 42), (cx + 70, cy - 42)], DIM, 6)
    c.line([(cx, cy - 42), (cx, cy)], DIM, 4)
    c.circle((cx, cy), 17, fill=CARD, outline=GRY, w=4)
    c.circle((cx, cy), 4, fill=GRY)

def hmark(c, x, y0, y1, label, col=CYN, ticks=()):
    if y0 - y1 < 6: return
    c.line([(x, y0), (x, y1)], col, 4)
    for yy in (y0, y1) + tuple(ticks): c.line([(x - 9, yy), (x + 9, yy)], col, 4)
    if label: c.text(x + 16, (y0 + y1) / 2, label, 24, col, anchor='lm')

def engine(c, x, ys, t, s=1.0, depth=None):
    """Kiriş kollu buhar makinesi. x: evin sol kenarı, ys: zemin. Pompa çubuğunun ucunu döndürür."""
    c.rect(x, ys - 150 * s, x + 120 * s, ys, fill=STONE, r=4)
    c.rect(x + 18 * s, ys - 110 * s, x + 44 * s, ys - 70 * s, fill=(255, 190, 90), r=3)
    c.rect(x + 88 * s, ys - 235 * s, x + 110 * s, ys - 150 * s, fill=(72, 64, 62), r=2)
    for k in range(3):
        u = (t * 0.55 + k / 3) % 1
        c.circle((x + 99 * s + 18 * s * u, ys - 245 * s - 75 * s * u), (8 + 14 * u) * s,
                 fill=mix(BGC, (150, 152, 162), (1 - u) * 0.7))
    pv = (x + 22 * s, ys - 172 * s)
    c.poly([(pv[0] - 14 * s, ys - 150 * s), (pv[0] + 14 * s, ys - 150 * s), pv], (120, 100, 80))
    ang = 0.16 * math.sin(t * 3)
    L = 112 * s
    le = (pv[0] - L * math.cos(ang), pv[1] + L * math.sin(ang))
    re = (pv[0] + 0.75 * L * math.cos(ang), pv[1] - 0.75 * L * math.sin(ang))
    c.line([le, re], (150, 110, 70), 9 * s)
    c.circle(pv, 5 * s, fill=GRY)
    c.line([re, (re[0], ys - 150 * s)], (130, 130, 140), 4 * s)
    bottom = depth if depth is not None else ys
    c.line([le, (le[0], bottom)], (175, 175, 185), 4 * s)
    return le

def coal(c, cx, yg, s=1.0):
    c.poly([(cx - 50 * s, yg), (cx - 30 * s, yg - 28 * s), (cx - 5 * s, yg - 40 * s), (cx + 25 * s, yg - 30 * s),
            (cx + 50 * s, yg)], (34, 34, 40))
    for dx, dy in [(-25, -12), (0, -24), (20, -10), (-8, -8), (32, -6)]:
        c.circle((cx + dx * s, yg + dy * s), 4 * s, fill=(70, 70, 80))

def horse(c, x, yg, t, moving=True):
    ph = t * 9 if moving else 0
    by = yg - 95
    for k, (dx, p) in enumerate([(-44, 0), (-30, math.pi), (30, math.pi), (44, 0)]):
        sw = 14 * math.sin(ph + p) if moving else 0
        c.line([(x + dx, by + 10), (x + dx + sw * 0.4, by + 50), (x + dx + sw, yg)], mix(HORSE, BGC, 0.25 if k % 2 else 0), 8)
    c.d.ellipse([(x - 62) * S, (by - 26) * S, (x + 62) * S, (by + 26) * S], fill=HORSE)
    c.poly([(x + 36, by - 18), (x + 58, by + 4), (x + 92, by - 46), (x + 74, by - 62)], HORSE)
    c.poly([(x + 70, by - 70), (x + 112, by - 50), (x + 108, by - 36), (x + 72, by - 46)], HORSE)
    c.poly([(x + 74, by - 68), (x + 80, by - 86), (x + 86, by - 66)], HORSE)
    c.line([(x + 40, by - 22), (x + 76, by - 66)], (110, 70, 45), 6)
    c.circle((x + 90, by - 58), 3, fill=BGC)
    c.line([(x - 60, by - 10), (x - 74, by + 20), (x - 70, by + 44)], (110, 70, 45), 6)
    c.line([(x + 30, by - 20), (x + 30, by + 18)], (90, 60, 40), 5)
    return (x + 30, by + 2)

# ------------------------------------------------------------------ sahneler
def s_title(c, t):
    c.text(560, 290, 'İŞ', 160, YEL, sc=pop(t, 0.1))
    c.text(800, 316, 'nedir?', 70, GRY, w='m', a=ramp(t, 0.45))
    c.text(640, 445, 'Fizikte bir kavram nasıl doğar?', 34, GRY, w='m', a=ramp(t, 0.9))
    c.text(640, 500, '10. Sınıf Fizik  ·  Enerji Ünitesi', 26, DIM, w='m', a=ramp(t, 1.2))

def mine(c, t, sx, ys, level):
    c.poly([(0, ys), (W, ys), (W, H), (0, H)], EARTH)
    c.line([(0, ys), (W, ys)], (90, 140, 80), 5)
    c.rect(sx - 40, ys, sx + 40, 700, fill=SHAFT, r=0)
    c.rect(sx + 40, 550, 1080, 620, fill=SHAFT, r=0)
    for xx in range(sx + 120, 1080, 160):
        c.line([(xx, 550), (xx, 620)], (110, 85, 60), 6)
    if level < 700:
        c.rect(sx - 40, level, sx + 40, 700, fill=WATER, r=0)
        if level < 620:
            c.rect(sx + 40, max(level, 550), 1080, 620, fill=WATER, r=0)
        wy = max(level, 550) if level < 620 else level
        for i in range(8):
            xx = sx - 40 + i * 20
            c.line([(xx, wy + 2 * math.sin(t * 5 + i)), (xx + 20, wy + 2 * math.sin(t * 5 + i + 1))], (120, 180, 230), 3)

def s_mine(c, t):
    sx, ys = 420, 330
    level = 690 - 115 * eio((t - 0.5) / 3.5)
    mine(c, t, sx, ys, level)
    mx = 900 - 60 * eio((t - 1.5) / 2.5)
    figure(c, (mx, 620 - 44), GRY, [(mx - 30, 540), (mx + 26, 560)], [(mx - 10, 620), (mx + 12, 620)], h=0.62, face=-1)
    if t > 2.2: c.text(mx + 4, 500, '!', 44, RED, sc=pop(t, 2.2))
    date_card(c, t, 0.05, '1700\'ler · İngiltere')
    caption(c, t, 0.7, 'Kömür madenlerini sürekli su basıyordu.', y=200, size=32)

def s_engine(c, t):
    sx, ys = 420, 380
    level = 600 + 85 * eio((t - 0.3) / 4.0)
    mine(c, t, sx, ys, level)
    engine(c, sx + 100, ys, t, 0.8, depth=level + 6)
    c.line([(sx, ys - 18), (sx - 95, ys - 18)], METD, 10)
    for k in range(6):
        u = (t * 1.6 + k / 6) % 1
        c.circle((sx - 98 - 6 * u, ys - 14 + 14 * u * u * 1.0), 5, fill=mix(EARTH, (120, 180, 230), 1 - u * 0.5))
    title(c, t, 'Çözüm: buhar makineleri suyu yukarı pompaladı.', y=95, size=32)
    caption(c, t, 1.4, 'Ama her makine kömür yakıyordu...', y=465, col=YEL, size=30)

def s_owner(c, t):
    yg = 540
    ground(c, yg)
    for x0, lab, col in [(150, 'A', ORN), (900, 'B', CYN)]:
        engine(c, x0 + 90, yg, t + (0 if lab == 'A' else 1.1), 0.85)
        coal(c, x0 + 270, yg, 1.0)
        c.circle((x0 + 140, yg + 50), 24, fill=col)
        c.text(x0 + 140, yg + 52, lab, 28, BGC)
    hip = (640, yg - 72)
    figure(c, hip, GRY, [(612, yg - 120), (668, yg - 104)], [(626, yg), (654, yg)], h=1.05)
    sc = pop(t, 0.5)
    if sc > 0:
        c.circle((700, yg - 225), 38 * sc, fill=CARD, outline=YEL, w=3)
        c.text(700, yg - 222, '?', 48, YEL, sc=sc)
    title(c, t, 'Maden sahibinin sorusu:', y=88, col=DIM, size=30)
    caption(c, t, 0.9, 'Hangi makine daha çok iş görüyor?', y=150, col=GRY, size=36)
    caption(c, t, 2.4, 'Parayı neye göre ödemeliyim?', y=210, col=YEL, size=32)

def s_measure(c, t):
    c.text(640, 210, 'Önce şunu sormalıyız:', 34, DIM, w='m', a=ramp(t, 0.05))
    parts_line(c, t, 300, [('Makine ne ', GRY, 'b', 0.4), ('YAPTI', YEL, 'b', 0.7), ('?', GRY, 'b', 0.4)], 64)
    c.text(640, 400, 'Suyu yukarı kaldırdı.', 36, GRY, w='m', a=ramp(t, 1.4))
    parts_line(c, t, 480, [('Ne kadar ', GRY, 'm', 2.0), ('AĞIR', ORN, 'b', 2.0), ('?   Ne kadar ', GRY, 'm', 2.3),
                           ('YUKARI', CYN, 'b', 2.3), ('?', GRY, 'm', 2.3)], 36)
    by = 640 - 40 * eio((t - 0.5) / 2.5)
    bucket(c, 640, by, 0.8)

PX = 125  # 1 m

def rig(c, cx, ytop, by, n=1):
    pulley(c, cx, ytop)
    if n == 1:
        hd = bucket(c, cx, by)
        c.line([(cx, ytop + 17), hd], GRY, 3)
    else:
        h1 = bucket(c, cx - 34, by); h2 = bucket(c, cx + 34, by)
        bar_y = h1[1] - 14
        c.line([(cx - 34, bar_y), (cx + 34, bar_y)], DIM, 5)
        c.line([h1, (cx - 34, bar_y)], DIM, 3); c.line([h2, (cx + 34, bar_y)], DIM, 3)
        c.line([(cx, ytop + 17), (cx, bar_y)], GRY, 3)

def s_exp1(c, t):
    title(c, t, 'Düşün 1:  Kova sayısı iki katına çıkarsa?', y=80, size=34)
    yg = 520; ground(c, yg, 80, 1200)
    p = eio((t - 0.4) / 1.6)
    for cx, n, lab in [(360, 1, '1 kova  ·  1 m'), (920, 2, '2 kova  ·  1 m')]:
        by = yg - PX * p
        rig(c, cx, 190, by, n)
        hmark(c, cx + (100 if n == 2 else 75), yg, by, '1 m' if p > 0.5 else None)
        c.text(cx, yg + 34, lab, 26, GRY, w='m', a=ramp(t, 0.2))
    caption(c, t, 2.3, '2 kovayı kaldırmak  =  1 kovayı İKİ KEZ kaldırmak', y=615, size=30)
    parts_line(c, t, 670, [('Ağırlık ×2  →  iş ', GRY, 'b', 3.3), ('×2', YEL, 'b', 3.6)], 36)

def s_exp2(c, t):
    title(c, t, 'Düşün 2:  Yükseklik iki katına çıkarsa?', y=80, size=34)
    yg = 520; ground(c, yg, 80, 1200)
    p = eio((t - 0.4) / 1.8)
    by1 = yg - PX * p
    rig(c, 360, 175, by1, 1); hmark(c, 435, yg, by1, '1 m' if p > 0.5 else None)
    c.text(360, yg + 34, '1 kova  ·  1 m', 26, GRY, w='m', a=ramp(t, 0.2))
    by2 = yg - 2 * PX * p
    rig(c, 920, 175, by2, 1)
    hmark(c, 995, yg, by2, None, ticks=(yg - PX,) if p > 0.55 else ())
    if p > 0.5: c.text(1011, yg - PX / 2, '1 m', 24, CYN, anchor='lm')
    if p > 0.98: c.text(1011, yg - PX * 1.5, '1 m', 24, CYN, anchor='lm')
    c.text(920, yg + 34, '1 kova  ·  2 m', 26, GRY, w='m', a=ramp(t, 0.2))
    caption(c, t, 2.4, '2 m kaldırmak  =  1 m\'yi İKİ KEZ kaldırmak', y=615, size=30)
    parts_line(c, t, 670, [('Yükseklik ×2  →  iş ', GRY, 'b', 3.4), ('×2', YEL, 'b', 3.7)], 36)

def s_table(c, t):
    title(c, t, 'Şimdiye kadar bulduklarımız', y=110, col=DIM, size=32)
    rows = [('Ağırlık', ORN, 0.3), ('Yükseklik', CYN, 0.9)]
    for k, (nm, col, a0) in enumerate(rows):
        y = 240 + k * 100; a = ramp(t, a0)
        if a <= 0: continue
        c.rect(260, y - 40, 1020, y + 40, fill=mix(BGC, CARD, a), r=14)
        c.text(420, y, f'{nm} ×2', 36, col, a=a)
        c.text(640, y, '→', 40, GRY, a=a)
        parts_line(c, t, y, [('İş ', GRY, 'b', a0 + 0.2), ('×2', YEL, 'b', a0 + 0.3)], 36, anchor_x=840)
    c.text(640, 480, 'İş, ağırlıkla da yükseklikle de doğru orantılı.', 32, YEL, a=ramp(t, 1.8))
    c.text(640, 545, 'Peki ikisini tek bir sayıda nasıl birleştireceğiz?', 28, GRY, w='m', a=ramp(t, 2.8))

def block(c, x0, yb, wd, ht, label):
    c.rect(x0, yb - ht, x0 + wd, yb, fill=(120, 124, 140), outline=(80, 84, 100), w=3, r=6)
    c.text(x0 + wd / 2, yb - ht / 2, label, 19, (20, 24, 40))

def s_descartes(c, t):
    date_card(c, t, 0.05, '1637 · René Descartes', 'Basit makineler üzerine bir mektup')
    yg = 520; ground(c, yg, 120, 1160)
    p = eio((t - 0.9) / 1.8); U = 90
    by = yg - 2 * U * p
    block(c, 290, by, 100, U, '100 libre'); hmark(c, 420, yg, by, '2 ayak' if p > 0.5 else None)
    by2 = yg - U * p
    block(c, 760, by2, 200, U, '200 libre'); hmark(c, 990, yg, by2, '1 ayak' if p > 0.5 else None)
    c.text(640, 420, '=', 80, YEL, sc=pop(t, 2.8))
    caption(c, t, 3.0, 'Descartes: “İkisi için de aynı çaba gerekir.”', y=600, size=32)
    c.text(640, 650, '(libre ≈ 0,45 kg ağırlık · ayak ≈ 30 cm)', 22, DIM, w='m', a=ramp(t, 3.5))

def s_pause1(c, t):
    pill(c, t, 'SIRA SENDE!', YEL)
    c.text(640, 230, 'Ağırlık ile yüksekliği tek bir sayıda', 40, GRY, w='m', a=ramp(t, 0.3))
    c.text(640, 290, 'nasıl birleştirirsin?', 40, GRY, w='m', a=ramp(t, 0.5))
    c.text(640, 380, 'İpucu: Descartes\'ın iki durumu aynı sayıyı vermeli.', 28, YEL, w='m', a=ramp(t, 1.2))
    c.text(640, 430, '100 libre & 2 ayak    ve    200 libre & 1 ayak', 26, DIM, w='m', a=ramp(t, 1.5))
    c.text(640, 560, 'Videoyu durdur ve düşün!', 34, mix(GRY, YEL, 0.5 + 0.5 * math.sin(t * 6)), a=ramp(t, 1.8))
    timer(c, t, 1.8, 5.0)

def s_test(c, t):
    title(c, t, 'İki yolu deneyelim', y=88, col=DIM, size=32)
    for x0, nm, op, r1, r2, ok, a0 in [(110, 'Toplarsak', '+', '102', '201', False, 0.3),
                                         (680, 'Çarparsak', '×', '200', '200', True, 2.0)]:
        a = ramp(t, a0)
        if a <= 0: continue
        res = t > a0 + 1.1
        col = (GRN if ok else RED) if res else DIM
        c.rect(x0, 150, x0 + 490, 470, fill=mix(BGC, CARD, a), outline=mix(BGC, col, a), w=4 if res else 2, r=18)
        c.text(x0 + 245, 200, nm, 36, GRY, a=a)
        c.text(x0 + 245, 280, f'100 {op} 2 = {r1}', 40, GRY, w='m', a=ramp(t, a0 + 0.4))
        c.text(x0 + 245, 345, f'200 {op} 1 = {r2}', 40, GRY, w='m', a=ramp(t, a0 + 0.7))
        c.text(x0 + 245, 420, 'aynı! ✓' if ok else 'farklı ✗', 38, GRN if ok else RED, sc=pop(t, a0 + 1.1))
    sc = pop(t, 4.0)
    if sc > 0:
        c.text(640, 560, 'İş  ∝  ağırlık × yükseklik', 50, YEL, sc=sc)
    c.text(640, 625, 'Çarpım, ×2 → ×2 orantılarına da uyuyor.', 26, GRY, w='m', a=ramp(t, 4.6))

def s_duty(c, t):
    title(c, t, 'Mühendisler de makineleri tam böyle ölçtü', y=88, size=32)
    c.text(640, 175, 'Bir makinenin “görev” (duty) değeri:', 30, DIM, w='m', a=ramp(t, 0.4))
    c.text(640, 240, '1 kile kömürle kaç libre suyu kaç ayak yükselttiği', 30, GRY, w='m', a=ramp(t, 0.9))
    sc = pop(t, 1.8)
    if sc > 0:
        c.rect(640 - 330 * sc, 360 - 55 * sc, 640 + 330 * sc, 360 + 55 * sc, fill=CARD, outline=YEL, w=3, r=16)
        parts_line(c, t, 362, [('libre', ORN, 'b', 1.8), ('  ×  ', GRY, 'b', 1.8), ('ayak', CYN, 'b', 1.8)], 50)
    parts_line(c, t, 470, [('Birimleri: ', GRY, 'm', 2.8), ('ayak-libre', YEL, 'b', 2.8), ('  (foot-pound)', DIM, 'm', 2.8)], 32)
    c.text(640, 545, 'Birimin kendisi bile bir çarpım!', 34, YEL, a=ramp(t, 3.6))

def s_coriolis(c, t):
    date_card(c, t, 0.05, '1829 · Gaspard-Gustave Coriolis', 'Fransız mühendis ve matematikçi')
    c.text(640, 230, 'Bu niceliğe bilimsel bir ad verdi:', 32, GRY, w='m', a=ramp(t, 0.7))
    c.text(430, 360, 'travail', 84, SEP, w='si', sc=pop(t, 1.3))
    g = ramp(t, 2.0, 0.4)
    if g > 0: c.arrow((600, 362), (600 + 90 * g, 362), GRY, 6, 18)
    c.text(850, 352, 'İŞ', 110, YEL, sc=pop(t, 2.3))
    c.text(640, 500, 'İngilizcesi “work”  →  bu yüzden simgesi W', 28, DIM, w='m', a=ramp(t, 3.0))

def s_general(c, t):
    title(c, t, 'Ya yük yukarı değil de yatay çekilirse?', y=80, size=32)
    yg = 470; ground(c, yg, 60, 1220)
    hx = 640 + 180 * eio((t - 0.5) / 3.6)
    hp = horse(c, hx, yg, t, moving=0.5 < t < 4.1)
    bx = hx - 330
    if t > 0.5: c.rect(310, yg - 70, 420, yg, outline=DIM, w=2, r=6)
    c.rect(bx, yg - 70, bx + 110, yg, fill=BOXC, outline=BOXD, w=3, r=6)
    c.line([(bx - 6, yg - 2), (bx + 118, yg - 2)], (110, 80, 50), 6)
    c.line([(bx + 110, yg - 40), (hp[0] - 2, hp[1])], GRY, 3)
    c.arrow((bx + 130, yg - 100), (bx + 220, yg - 100), ORN, 7, 20)
    c.text(bx + 175, yg - 128, 'F', 30, ORN, w='i')
    L = bx - 310
    if L > 6: c.arrow((365, yg + 30), (365 + L, yg + 30), CYN, 6, 18)
    if L > 60: c.text(365 + L / 2, yg + 58, 'x', 28, CYN, w='i')
    parts_line(c, t, 590, [('ağırlık  →  ', GRY, 'm', 2.0), ('KUVVET', ORN, 'b', 2.0)], 32)
    parts_line(c, t, 640, [('yükseklik  →  ', GRY, 'm', 2.8), ('kuvvet yönünde alınan YOL', CYN, 'b', 2.8)], 32)

def s_pause2(c, t):
    pill(c, t, 'ŞİMDİ FORMÜLÜ SEN KUR!', YEL)
    parts_line(c, t, 250, [('Kuvvet: ', GRY, 'm', 0.4), ('F', ORN, 'i', 0.4), ('        Yol: ', GRY, 'm', 0.7), ('x', CYN, 'i', 0.7)], 44)
    parts_line(c, t, 370, [('İş', YEL, 'b', 1.2), ('  =  ', GRY, 'b', 1.2), ('?', YEL, 'b', 1.5)], 90)
    c.text(640, 520, 'Videoyu durdur ve defterine yaz!', 34, mix(GRY, YEL, 0.5 + 0.5 * math.sin(t * 6)), a=ramp(t, 1.8))
    timer(c, t, 1.8, 4.5, y=585)

def s_reveal(c, t):
    title(c, t, 'Senin bulduğun tanım:', col=DIM, size=32)
    parts_line(c, t, 260, [('W', YEL, 'i', 0.1), (' = ', GRY, 'b', 0.3), ('F', ORN, 'i', 0.45),
                           (' · ', GRY, 'b', 0.6), ('x', CYN, 'i', 0.7)], 120)
    parts_line(c, t, 375, [('W: iş', YEL, 'm', 1.2), ('     F: kuvvet (N)', ORN, 'm', 1.2),
                           ('     x: kuvvet yönünde yol (m)', CYN, 'm', 1.2)], 28)
    c.text(640, 480, 'Birimi:  N · m  =  joule (J)', 40, YEL, sc=pop(t, 2.2))
    c.text(640, 545, 'İngiliz bilim insanı James Prescott Joule\'ün onuruna', 24, DIM, w='m', a=ramp(t, 2.8))

def s_wall(c, t):
    wall_scene(c, t)
    title(c, t, 'Tanımı sınayalım  1)  Duvarı itmek', y=88, size=32)
    parts_line(c, t, 640, [('Kuvvet var, yol yok:  ', GRY, 'm', 1.2), ('x = 0  →  W = 0', RED, 'b', 1.8)], 32)

def s_carry(c, t):
    title(c, t, '2)  Kovayı düz yolda taşımak', y=88, size=32)
    yg = 540; ground(c, yg)
    hx = 280 + 430 * (t / 5.0); hip = (hx, yg - 72); ph = hx * 0.07
    figure(c, hip, GRY, [(hx + 50, yg - 70), (hx - 18, yg - 20)],
           [(hx + 22 * math.sin(ph), yg), (hx - 22 * math.sin(ph), yg)], lean=0.06)
    hd = bucket(c, hx + 50, yg - 6 + 0, 0.8)
    o = (hx + 50, yg - 30)
    k = ramp(t, 0.6, 0.4)
    c.arrow((o[0], o[1] - 70), (o[0], o[1] - 70 - 100 * k), ORN, 6, 18)
    c.arrow((o[0] + 40, o[1]), (o[0] + 40 + 120 * k, o[1]), CYN, 6, 18)
    if k > 0.5:
        c.text(o[0] + 16, o[1] - 160, 'F', 30, ORN, w='i', anchor='lm', a=k)
        c.text(o[0] + 172, o[1], 'yol', 24, CYN, anchor='lm', a=k)
    caption(c, t, 1.6, 'Kuvvet yukarı, yol yatay: kuvvet yönünde yol yok.', y=615, size=30)
    parts_line(c, t, 668, [('Su hiç yükselmedi  →  ', GRY, 'm', 2.6), ('W = 0', RED, 'b', 2.6)], 34)

def s_canal(c, t):
    title(c, t, '3)  At, kanaldaki mavnayı kıyıdan çekiyor', y=80, size=32)
    c.rect(0, 250, W, 330, fill=(40, 70, 50), r=0)
    c.rect(0, 330, W, 410, fill=(96, 82, 60), r=0)
    c.rect(0, 410, W, 560, fill=(36, 82, 132), r=0)
    for i in range(10):
        xx = (i * 140 + t * 20) % W
        c.line([(xx, 470 + 30 * (i % 3)), (xx + 40, 470 + 30 * (i % 3))], (70, 120, 170), 3)
    off = 160 * eio((t - 0.3) / 4.5)
    b = 230 + off; hx = 760 + off
    c.rect(b, 450, b + 230, 520, fill=(130, 90, 60), outline=(90, 60, 40), w=3, r=26)
    c.rect(b + 40, 462, b + 160, 508, fill=(160, 120, 80), r=8)
    c.d.ellipse([(hx - 38) * S, (370 - 15) * S, (hx + 38) * S, (370 + 15) * S], fill=HORSE)
    c.d.ellipse([(hx + 34) * S, (370 - 9) * S, (hx + 62) * S, (370 + 9) * S], fill=HORSE)
    att = (b + 220, 470)
    c.line([att, (hx - 36, 370)], GRY, 3)
    ux, uy = (hx - 36 - att[0]), (370 - att[1]); L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
    k = ramp(t, 1.0, 0.5)
    tip = (att[0] + 200 * ux * k, att[1] + 200 * uy * k)
    if k > 0:
        c.arrow(att, tip, ORN, 7, 20)
    k2 = ramp(t, 1.8, 0.5)
    if k2 > 0:
        fx, fy = 200 * ux, 200 * uy
        c.arrow(att, (att[0] + fx * k2, att[1]), YEL, 7, 20)
        c.arrow(att, (att[0], att[1] + fy * k2), (180, 190, 215), 6, 18)
        c.text(att[0] + fx * 0.5, att[1] + 34, 'Fx  (iş yapar)', 24, YEL, a=k2)
        c.text(att[0] - 14, att[1] + fy - 6, 'Fy  (iş yapmaz)', 22, (210, 216, 232), anchor='rm', a=k2)
        c.text(tip[0] + 10, tip[1] - 14, 'F', 28, ORN, w='i', anchor='lm', a=k2)
    caption(c, t, 2.8, 'Yalnızca yol yönündeki kuvvet bileşeni iş yapar:', y=615, size=28)
    c.text(640, 665, 'W = Fx · x', 38, YEL, w='i', a=ramp(t, 3.4))

def s_quiz(c, t):
    pill(c, t, 'SORU', YEL)
    c.text(640, 230, 'Bir vinç, 500 N ağırlığındaki yükü', 38, GRY, w='m', a=ramp(t, 0.3))
    c.text(640, 290, 'sabit hızla 4 m yukarı kaldırıyor.', 38, GRY, w='m', a=ramp(t, 0.6))
    c.text(640, 370, 'Vincin yaptığı iş kaç joule?', 42, YEL, a=ramp(t, 0.9))
    c.text(640, 520, 'Videoyu durdur ve çöz!', 34, mix(GRY, YEL, 0.5 + 0.5 * math.sin(t * 6)), a=ramp(t, 1.4))
    timer(c, t, 1.4, 4.3, y=585)

def s_answer(c, t):
    pill(c, t, 'ÇÖZÜM', GRN)
    c.text(640, 260, 'Kuvvet = 500 N   ·   kuvvet yönünde yol = 4 m', 32, GRY, w='m', a=ramp(t, 0.3))
    c.text(640, 335, 'W = F · x = 500 N · 4 m', 40, GRY, w='m', a=ramp(t, 0.9))
    sc = pop(t, 1.6, 0.4)
    if sc > 0:
        c.rect(640 - 230 * sc, 455 - 60 * sc, 640 + 230 * sc, 455 + 60 * sc, fill=(26, 60, 52), outline=GRN, w=4, r=20)
        c.text(640, 458, 'W = 2000 J', 72, GRN, sc=sc)

def s_chain(c, t):
    title(c, t, 'Bir kavram böyle doğdu', y=110, col=DIM, size=32)
    steps = [('Problem', 'su basan madenler'), ('Düşünce', 'deneyleri'), ('Orantılar', '×2 → ×2'),
             ('Çarpım', 'ağırlık × yükseklik'), ('Bir ad', 'İŞ (1829)'), ('Tanım', 'W = F · x')]
    for k, (a_, b_) in enumerate(steps):
        x0 = 55 + k * 200; a0 = 0.3 + k * 0.45; a = ramp(t, a0)
        if a <= 0: continue
        last = k == len(steps) - 1
        c.rect(x0, 260, x0 + 180, 400, fill=mix(BGC, CARD, a), outline=mix(BGC, YEL if last else DIM, a), w=3 if last else 2, r=14)
        c.text(x0 + 90, 310, a_, 26, YEL if last else GRY, a=a)
        c.text(x0 + 90, 355, b_, 16, GRY if last else (170, 180, 205), w='m', a=a)
        if k:
            c.arrow((x0 - 18, 330), (x0 - 3, 330), mix(BGC, GRY, a), 4, 10)
    c.text(640, 520, 'Fizikteki tanımlar, gerçek sorulara verilen cevaplardır.', 30, YEL, a=ramp(t, 3.4))

def s_teaser(c, t):
    c.text(640, 230, 'Peki aynı işi daha HIZLI yapan makine?', 40, GRY, a=ramp(t, 0.1))
    c.text(640, 320, 'James Watt, makinelerini atlarla kıyaslayarak sattı...', 30, SEP, w='s', a=ramp(t, 1.0))
    parts_line(c, t, 440, [('Sıradaki kavram:  ', GRY, 'm', 2.0), ('GÜÇ', GRN, 'b', 2.3)], 56)
    a = ramp(t, 0.4)
    if a > 0:
        cc = (640, 570)
        c.circle(cc, 44, outline=mix(BGC, GRY, a), w=5)
        ang = t * 9
        c.line([cc, (cc[0] + 32 * math.sin(ang), cc[1] - 32 * math.cos(ang))], mix(BGC, YEL, a), 5)

def s_end(c, t):
    parts_line(c, t, 300, [('İŞ', YEL, 'b', 0.05), (' nedir?', GRY, 'm', 0.25)], 80)
    c.text(640, 385, '10. Sınıf Fizik  ·  Enerji Ünitesi', 28, GRY, w='m', a=ramp(t, 0.5))
    c.text(640, 520, 'Hazırlayan: Irmak Dinmez', 30, YEL, w='m', a=ramp(t, 0.9))

WH = 'whoosh'
SCENES = [
    ('01_baslik', 3.5, s_title, [(0.1, 'pop'), (0.45, 'pop')]),
    ('02_maden', 4.5, s_mine, [(0.0, WH), (2.2, 'stamp')]),
    ('03_makine', 4.5, s_engine, [(0.0, WH)]),
    ('04_soru', 5.5, s_owner, [(0.0, WH), (0.5, 'pop'), (2.4, 'pop')]),
    ('05_olcum', 3.8, s_measure, [(0.0, WH), (0.7, 'pop')]),
    ('06_deney1', 6.0, s_exp1, [(0.0, WH), (3.6, 'ding')]),
    ('07_deney2', 6.0, s_exp2, [(0.0, WH), (3.7, 'ding')]),
    ('08_tablo', 5.0, s_table, [(0.0, WH), (0.5, 'pop'), (1.1, 'pop')]),
    ('09_descartes', 6.5, s_descartes, [(0.0, WH), (2.8, 'ding')]),
    ('10_sira_sende', 7.0, s_pause1, [(0.0, WH), (0.05, 'pop')]),
    ('11_dene', 6.5, s_test, [(0.0, WH), (1.4, 'stamp'), (3.1, 'ding'), (4.0, 'pop')]),
    ('12_duty', 6.0, s_duty, [(0.0, WH), (1.8, 'pop'), (3.6, 'ding')]),
    ('13_coriolis', 5.0, s_coriolis, [(0.0, WH), (1.3, 'pop'), (2.3, 'ding')]),
    ('14_genelle', 6.5, s_general, [(0.0, WH), (2.0, 'pop'), (2.8, 'pop')]),
    ('15_formul_sen', 6.5, s_pause2, [(0.0, WH), (0.05, 'pop'), (1.5, 'pop')]),
    ('16_formul', 5.5, s_reveal, [(0.0, WH), (0.1, 'pop'), (0.45, 'pop'), (0.7, 'pop'), (2.2, 'ding')]),
    ('17_duvar', 5.0, s_wall, [(0.0, WH), (1.8, 'stamp')]),
    ('18_tasima', 5.0, s_carry, [(0.0, WH), (2.6, 'stamp')]),
    ('19_kanal', 6.0, s_canal, [(0.0, WH), (1.8, 'pop'), (3.4, 'ding')]),
    ('20_test', 6.0, s_quiz, [(0.0, WH), (0.05, 'pop')]),
    ('21_cozum', 4.0, s_answer, [(0.0, WH), (1.6, 'ding')]),
    ('22_zincir', 6.0, s_chain, [(0.0, WH)] + [(0.3 + k * 0.45, 'pop') for k in range(6)]),
    ('23_guc', 5.0, s_teaser, [(0.0, WH), (2.3, 'ding')]),
    ('24_son', 3.5, s_end, [(0.0, WH)]),
]

def render_frame(idx, t):
    name, dur, fn, _ = SCENES[idx]
    c = C(); fn(c, t)
    u = eio(t / dur)
    z = 1.0 + 0.04 * (u if idx % 2 == 0 else 1 - u)
    return c.frame(z)

def render_scene(idx, outdir):
    name, dur, fn, _ = SCENES[idx]
    n = int(round(dur * FPS)); out = os.path.join(outdir, name + '.mp4'); tmp = os.path.join(outdir, name + '.tmp.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast',
                          '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(render_frame(idx, i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, out)
    else: raise SystemExit('ffmpeg failed ' + name)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'preview':
        outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
        for spec in sys.argv[3:]:
            i, tt = spec.split(':'); render_frame(int(i), float(tt)).save(os.path.join(outdir, f'q{int(i):02d}_{tt}.png'))
    elif mode == 'sheet':
        from PIL import Image
        outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
        ims = [render_frame(i, d * 0.9).resize((640, 360)) for i, (_, d, _, _) in enumerate(SCENES)]
        rows = (len(ims) + 3) // 4
        sh = Image.new('RGB', (2560, 360 * rows))
        for k, im in enumerate(ims): sh.paste(im, ((k % 4) * 640, (k // 4) * 360))
        sh.save(os.path.join(outdir, 'sheet_v2.png'))
    elif mode == 'scenes':
        outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
        for i in map(int, sys.argv[3:]): render_scene(i, outdir)
