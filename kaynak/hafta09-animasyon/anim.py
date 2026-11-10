#!/usr/bin/env python3
# 10. Sınıf Fizik - Enerji: İŞ ve GÜÇ (ekran yazılı kısa ders animasyonu)
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, S, FPS = 1280, 720, 2, 30
FD = '/usr/share/fonts/truetype/google-fonts/'
FONTS = {'b': 'Poppins-Bold.ttf', 'm': 'Poppins-Medium.ttf', 'r': 'Poppins-Regular.ttf',
         'i': 'Poppins-BoldItalic.ttf', 'l': 'Poppins-Light.ttf'}
_fc = {}
def font(w, size):
    k = (w, max(4, int(size * S)))
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FD + FONTS[w], k[1])
    return _fc[k]

BGC = (17, 26, 51)
YEL = (255, 201, 60); GRY = (232, 234, 238); DIM = (125, 137, 168)
ORN = (255, 120, 70); CYN = (80, 200, 240); GRN = (110, 215, 140)
RED = (239, 71, 111); BOXC = (196, 140, 90); BOXD = (140, 95, 60)
CARD = (30, 43, 80); STAIR = (42, 58, 100)

def mix(a, b, t):
    t = max(0.0, min(1.0, t)); return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def back(x):
    x = clamp(x); c = 1.7; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def ramp(t, a, d=0.35): return ease((t - a) / d)
def pop(t, a, d=0.4): return back((t - a) / d) if t > a else 0.0

def make_bg():
    y = np.linspace(0, 1, H * S)[:, None, None]
    top = np.array([24, 36, 70], np.float32); bot = np.array([11, 17, 36], np.float32)
    arr = np.broadcast_to(top * (1 - y) + bot * y, (H * S, W * S, 3)).copy()
    im = Image.fromarray(arr.astype(np.uint8)); d = ImageDraw.Draw(im)
    for gx in range(20, W, 40):
        for gy in range(20, H, 40):
            d.ellipse([gx * S - 2, gy * S - 2, gx * S + 2, gy * S + 2], fill=(34, 48, 86))
    return im
BG = make_bg()

class C:
    def __init__(s):
        s.im = BG.copy(); s.d = ImageDraw.Draw(s.im)
    def line(s, pts, col, w=4):
        P = [(x * S, y * S) for x, y in pts]
        s.d.line(P, fill=col, width=int(w * S), joint='curve')
        r = w * S / 2
        for x, y in (P[0], P[-1]):
            s.d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    def circle(s, c, r, fill=None, outline=None, w=3):
        x, y = c
        s.d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=fill,
                    outline=outline, width=int(w * S))
    def rect(s, x0, y0, x1, y1, fill=None, outline=None, w=3, r=10):
        s.d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, fill=fill,
                              outline=outline, width=int(w * S) if outline else 0)
    def poly(s, pts, fill, outline=None):
        s.d.polygon([(x * S, y * S) for x, y in pts], fill=fill, outline=outline)
    def text(s, x, y, txt, size, col, w='b', anchor='mm', a=1.0, sc=1.0):
        if a <= 0.01 or sc <= 0.02: return
        s.d.text((x * S, y * S), txt, font=font(w, size * sc), fill=mix(BGC, col, a), anchor=anchor)
    def tw(s, txt, size, w='b'): return font(w, size).getlength(txt) / S
    def arrow(s, p0, p1, col, w=6, head=18):
        x0, y0 = p0; x1, y1 = p1; L = math.hypot(x1 - x0, y1 - y0)
        if L < 3: return
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        h = min(head, L * 0.6); bx, by = x1 - ux * h, y1 - uy * h
        s.line([(x0, y0), (bx, by)], col, w)
        px, py = -uy, ux
        s.poly([(x1 + ux * 2, y1 + uy * 2), (bx + px * h * 0.6, by + py * h * 0.6),
                (bx - px * h * 0.6, by - py * h * 0.6)], col)
    def dashed(s, p0, p1, col, w=3, dash=10):
        x0, y0 = p0; x1, y1 = p1; L = math.hypot(x1 - x0, y1 - y0)
        n = int(L // (dash * 2)) + 1
        for i in range(n):
            a = i * 2 * dash / L; b = min(1, (i * 2 + 1) * dash / L)
            if a >= 1: break
            s.d.line([((x0 + (x1 - x0) * a) * S, (y0 + (y1 - y0) * a) * S),
                      ((x0 + (x1 - x0) * b) * S, (y0 + (y1 - y0) * b) * S)], fill=col, width=int(w * S))
    def frame(s, z=1.0):
        cw, ch = W * S / z, H * S / z; x0 = (W * S - cw) / 2; y0 = (H * S - ch) / 2
        return s.im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))

def figure(c, hip, col, hands, feet, lean=0.0, h=1.0, face=1):
    hx, hy = hip; torso = 62 * h; w = 7 * h
    neck = (hx + math.sin(lean) * torso, hy - math.cos(lean) * torso)
    head = (hx + math.sin(lean) * (torso + 24 * h), hy - math.cos(lean) * (torso + 24 * h))
    sh = (hx + math.sin(lean) * torso * 0.85, hy - math.cos(lean) * torso * 0.85)
    for f in feet:
        k = ((hx + f[0]) / 2 + face * 7 * h, (hy + f[1]) / 2)
        c.line([hip, k, f], col, w)
    c.line([hip, neck], col, w)
    for hd in hands:
        e = ((sh[0] + hd[0]) / 2, (sh[1] + hd[1]) / 2 + 9 * h)
        c.line([sh, e, hd], col, w)
    c.circle(head, 19 * h, fill=col)
    c.circle((head[0] + face * 8 * h, head[1] - 3 * h), 3 * h, fill=BGC)
    return head

def ground(c, y, x0=60, x1=1220): c.line([(x0, y), (x1, y)], DIM, 3)

def box(c, x0, y0, sz, label=None):
    c.rect(x0, y0, x0 + sz, y0 + sz, fill=BOXC, outline=BOXD, w=3, r=6)
    c.line([(x0 + sz * 0.5, y0 + 4), (x0 + sz * 0.5, y0 + sz * 0.35)], BOXD, 4)
    if label: c.text(x0 + sz / 2, y0 + sz * 0.62, label, 22, (60, 38, 20))

def caption(c, t, a0, txt, y=645, col=GRY, size=30):
    c.text(640, y, txt, size, col, a=ramp(t, a0))

def title(c, t, txt, y=92, col=GRY, size=38, a0=0.05):
    c.text(640, y, txt, size, col, a=ramp(t, a0))

def parts_line(c, t, y, parts, size, anchor_x=640):
    """parts: (text, color, weight, appear) — ortalanmış tek satır."""
    widths = [c.tw(p[0], size, p[2]) for p in parts]
    x = anchor_x - sum(widths) / 2
    for (txt, col, wgt, a0), wd in zip(parts, widths):
        sc = pop(t, a0) if a0 is not None else 1.0
        c.text(x + wd / 2, y, txt, size, col, w=wgt, sc=max(sc, 0) if sc else 0, a=ramp(t, a0 or 0, 0.15))
        x += wd

# ---------------------------------------------------------------- sahneler
def s_title(c, t):
    c.text(470, 300, 'İŞ', 150, YEL, sc=pop(t, 0.1))
    c.text(600, 318, 've', 60, GRY, w='m', a=ramp(t, 0.3))
    c.text(830, 300, 'GÜÇ', 150, YEL, sc=pop(t, 0.5))
    c.text(640, 445, '10. Sınıf Fizik  ·  Enerji Ünitesi', 32, GRY, w='m', a=ramp(t, 0.9))
    g = ramp(t, 1.1, 0.6)
    if g > 0:
        c.line([(300, 540), (300 + 680 * g, 540)], DIM, 3)
    p = eio((t - 1.5) / 1.8)
    if t > 1.5:
        bx = 310 + 560 * p
        box(c, bx, 488, 52)
        c.arrow((bx + 60, 514), (bx + 120, 514), ORN, 5, 14)

def wall_scene(c, t):
    ground(c, 560)
    c.rect(760, 250, 870, 560, fill=(150, 72, 62), r=4)
    for i, yy in enumerate(range(250, 560, 34)):
        c.line([(760, yy), (870, yy)], (110, 50, 45), 2)
        off = 0 if i % 2 == 0 else 27
        for xx in range(760 + off + 27, 870, 55):
            c.line([(xx, yy), (xx, min(yy + 34, 560))], (110, 50, 45), 2)
    sh = math.sin(t * 38) * 1.5
    hip = (650 + sh, 488)
    head = figure(c, hip, GRY, [(758, 392), (758, 420)], [(598 + sh, 560), (566 + sh, 560)], lean=0.5)
    for k, a0 in enumerate([1.0, 1.6, 2.2]):
        if t > a0:
            u = (t - a0) % 1.4
            dx = head[0] - 30 - k * 8; dy = head[1] - 18 + u * 60
            col = mix(BGC, CYN, 1 - u / 1.4)
            c.poly([(dx, dy - 10), (dx - 6, dy + 2), (dx + 6, dy + 2)], col)
            c.circle((dx, dy + 3), 6, fill=col)

def s_wall1(c, t):
    wall_scene(c, t)
    title(c, t, 'Bütün gün bir duvarı ittiğini düşün...')
    caption(c, t, 1.4, 'Çok yorulursun, değil mi?')

def s_wall2(c, t):
    wall_scene(c, t + 3)
    title(c, t, 'Ama duvar yerinden hiç kıpırdamadı!')
    sc = pop(t, 0.7, 0.35)
    if sc > 0:
        wdt, hgt = 470 * sc, 100 * sc
        c.rect(640 - wdt / 2, 250 - hgt / 2, 640 + wdt / 2, 250 + hgt / 2, fill=(40, 20, 38), outline=RED, w=6, r=14)
        c.text(640, 252, 'FİZİKTE İŞ = 0', 62, RED, sc=sc)
    caption(c, t, 1.7, 'Yer değiştirme yoksa, iş de yoktur.', col=YEL)

def s_push(c, t):
    ground(c, 560)
    p = eio((t - 0.4) / 2.8); bx = 330 + 490 * p
    if t > 0.4:
        c.rect(330, 450, 440, 560, outline=DIM, w=2, r=6)
    box(c, bx, 450, 110)
    hip = (bx - 82, 488); ph = bx * 0.07
    figure(c, hip, GRY, [(bx - 2, 494), (bx - 2, 516)],
           [(hip[0] - 18 + 24 * math.sin(ph), 560), (hip[0] - 18 - 24 * math.sin(ph), 560)], lean=0.35)
    c.arrow((bx + 20, 425), (bx + 100, 425), ORN, 7, 20)
    c.text(bx + 60, 398, 'F', 32, ORN, w='i')
    L = bx - 330
    if L > 6:
        c.arrow((385, 600), (385 + L, 600), CYN, 6, 18)
    if L > 60:
        c.text(385 + L / 2, 628, 'x', 30, CYN, w='i')
    title(c, t, 'Kuvvet uygulandı VE cisim yer değiştirdi.')
    caption(c, t, 2.7, 'İşte bu, fizikte İŞ\'tir!', y=680, col=YEL, size=34)

def s_formula_w(c, t):
    title(c, t, 'İşin formülü', col=DIM, size=32)
    parts_line(c, t, 270, [('W', YEL, 'i', 0.1), (' = ', GRY, 'b', 0.3), ('F', ORN, 'i', 0.45),
                           (' · ', GRY, 'b', 0.6), ('x', CYN, 'i', 0.7)], 120)
    a = ramp(t, 1.2)
    parts_line(c, t, 385, [('W: iş', YEL, 'm', 1.2), ('     F: kuvvet (N)', ORN, 'm', 1.2),
                           ('     x: yer değiştirme (m)', CYN, 'm', 1.2)], 28)
    c.text(640, 495, 'Birimi: joule (J)', 40, YEL, sc=pop(t, 2.0))
    c.text(640, 555, '1 J = 1 N · 1 m', 30, GRY, w='m', a=ramp(t, 2.5))

def s_example(c, t):
    title(c, t, 'Örnek', col=DIM, size=32)
    ground(c, 470)
    p = eio((t - 0.3) / 1.8); bx = 240 + 400 * p
    if t > 0.3: c.rect(240, 370, 340, 470, outline=DIM, w=2, r=6)
    box(c, bx, 370, 100)
    c.arrow((bx + 108, 420), (bx + 200, 420), ORN, 7, 20)
    c.text(bx + 160, 390, 'F = 20 N', 26, ORN)
    L = bx - 240
    if L > 6: c.arrow((290, 510), (290 + L, 510), CYN, 6, 18)
    if p > 0.95: c.text(290 + L / 2, 540, 'x = 5 m', 26, CYN, a=ramp(t, 2.1))
    a = ramp(t, 0.9)
    c.text(800, 625, 'W = 20 N × 5 m =', 40, GRY, anchor='rm', a=a)
    v = 100 * eio((t - 1.0) / 1.6) if t > 1.0 else 0
    if a > 0:
        fin = t > 2.6
        c.text(820, 625, f'{int(round(v))} J', 52 if fin else 44, YEL, anchor='lm',
               sc=pop(t, 2.6, 0.3) if fin else 1.0)

def s_angle(c, t):
    title(c, t, 'Kuvvet eğik uygulanırsa?')
    ground(c, 540)
    bx = 400 + 70 * eio((t - 0.4) / 3.2)
    box(c, bx, 420, 120)
    o = (bx + 122, 450)
    g = ramp(t, 0.2, 0.5)
    tip = (o[0] + 160 * g, o[1] - 120 * g)
    c.arrow(o, tip, ORN, 7, 22)
    if g > 0.9: c.text(tip[0] + 22, tip[1] - 12, 'F', 32, ORN, w='i')
    k = ramp(t, 1.0, 0.5)
    if k > 0:
        c.dashed((o[0] + 160, o[1] - 120), (o[0] + 160, o[1]), DIM, 3)
        c.dashed((o[0] + 160, o[1] - 120), (o[0], o[1] - 120), DIM, 3)
        c.arrow(o, (o[0], o[1] - 120 * k), DIM, 6, 18)
        c.arrow(o, (o[0] + 160 * k, o[1]), YEL, 7, 20)
        c.text(o[0] - 14, o[1] - 120, 'Fy  (iş yapmaz)', 24, DIM, anchor='rm', a=k)
        c.text(o[0] + 175, o[1] + 34, 'Fx  (iş yapar)', 26, YEL, anchor='mm', a=k)
    caption(c, t, 1.9, 'Yalnızca hareket yönündeki bileşen iş yapar:', y=615, size=28)
    c.text(640, 665, 'W = Fx · x', 36, YEL, w='i', a=ramp(t, 2.3))

def s_bag(c, t):
    title(c, t, 'Çantanı tutarak düz yolda yürüyorsun...')
    ground(c, 560)
    hx = 280 + 430 * (t / 4.0); hip = (hx, 488); ph = hx * 0.07
    figure(c, hip, GRY, [(hx + 56, 478), (hx - 18, 540)],
           [(hx + 22 * math.sin(ph), 560), (hx - 22 * math.sin(ph), 560)], lean=0.06)
    c.line([(hx + 46, 494), (hx + 56, 478), (hx + 66, 494)], (90, 60, 120), 4)
    c.rect(hx + 32, 492, hx + 82, 535, fill=(120, 80, 160), outline=(80, 55, 110), w=2, r=6)
    o = (hx + 57, 513)
    k = ramp(t, 0.6, 0.4)
    c.arrow(o, (o[0], o[1] - 115 * k), ORN, 6, 18)
    c.arrow(o, (o[0] + 120 * k, o[1]), CYN, 6, 18)
    if k > 0.5:
        c.line([(o[0], o[1] - 16), (o[0] + 16, o[1] - 16), (o[0] + 16, o[1])], GRY, 2)
        c.text(o[0] + 14, o[1] - 105, 'F', 30, ORN, w='i', anchor='lm', a=k)
        c.text(o[0] + 128, o[1], 'hareket', 22, CYN, anchor='lm', a=k)
    caption(c, t, 1.6, 'Kuvvet yukarı, hareket yana (90°)', y=630, size=30)
    c.text(640, 678, 'İş = 0', 40, RED, sc=pop(t, 2.2))

def s_lift(c, t):
    title(c, t, 'Cismi sabit hızla yukarı kaldırmak')
    ground(c, 590, 140, 700)
    p = eio((t - 0.4) / 1.8); by = 490 - 240 * p
    if t > 0.4: c.rect(300, 490, 400, 590, outline=DIM, w=2, r=6)
    box(c, 300, by, 100, '2 kg')
    c.arrow((350, by - 6), (350, by - 80), ORN, 7, 20)
    c.text(372, by - 60, 'F', 30, ORN, w='i', anchor='lm')
    hb = 590 - (by + 100)
    if hb > 8:
        c.line([(450, 590), (450, by + 100)], CYN, 4)
        c.line([(440, 590), (460, 590)], CYN, 4); c.line([(440, by + 100), (460, by + 100)], CYN, 4)
        c.text(470, 590 - hb / 2, 'h = 3 m' if p > 0.9 else 'h', 28, CYN, anchor='lm')
    c.text(900, 250, 'W = m · g · h', 44, GRY, w='i', a=ramp(t, 0.3))
    c.text(900, 320, '= 2 · 10 · 3', 40, GRY, a=ramp(t, 1.2))
    if t > 1.6:
        v = 60 * eio((t - 1.6) / 1.0)
        c.text(900, 400, f'= {int(round(v))} J', 52, YEL, sc=pop(t, 2.6, 0.3) if t > 2.6 else 1.0)
    c.text(900, 470, '(g = 10 N/kg)', 24, DIM, w='m', a=ramp(t, 1.2))

def s_question(c, t):
    c.text(640, 270, 'Aynı işi...', 70, GRY, a=ramp(t, 0.05))
    parts_line(c, t, 365, [('kim daha ', GRY, 'b', 0.6), ('HIZLI', YEL, 'b', 0.9), (' yapar?', GRY, 'b', 0.6)], 70)
    a = ramp(t, 0.4)
    if a > 0:
        cc = (640, 520)
        c.circle(cc, 48, outline=mix(BGC, GRY, a), w=5)
        ang = t * 9
        c.line([cc, (cc[0] + 34 * math.sin(ang), cc[1] - 34 * math.cos(ang))], mix(BGC, YEL, a), 5)
        c.line([cc, (cc[0] + 22 * math.sin(ang / 12), cc[1] - 22 * math.cos(ang / 12))], mix(BGC, GRY, a), 5)

def stairs(c, x0, col):
    pts = [(x0, 600)]
    for i in range(8):
        y = 600 - 30 * (i + 1); pts += [(x0 + i * 50, y), (x0 + (i + 1) * 50, y)]
    pts += [(x0 + 440, 360), (x0 + 440, 600)]
    c.poly(pts, STAIR, outline=None)

def climber(c, x0, p, col):
    s = p * 8
    if s <= 0: fx, fy = x0 - 30, 600
    else:
        fx = x0 - 15 + s * 50 + (20 if s >= 8 else 0)
        fy = 600 - 30 * min(8, math.ceil(s - 1e-6))
    b = s % 1 if 0 < s < 8 else 0
    h = 0.8; hip = (fx, fy - 60 - 6 * math.sin(b * math.pi))
    figure(c, hip, col, [(fx + 22, fy - 70), (fx - 20, fy - 48)],
           [(fx - 12, fy), (fx + 14, fy - 30 * (1 - b) if b else fy)], lean=0.12, h=h)

def s_stairs(c, t):
    title(c, t, 'İkisi de 50 kg, ikisi de 4 m çıkıyor:  W = 2000 J', size=30)
    stairs(c, 120, YEL); stairs(c, 680, CYN)
    pE = clamp((t - 0.4) / 2.0); pC = clamp((t - 0.4) / 4.0)
    climber(c, 120, pE, YEL); climber(c, 680, pC, CYN)
    c.text(340, 190, 'Ece', 34, YEL); c.text(900, 190, 'Can', 34, CYN)
    c.text(340, 655, f't = {int(round(pE * 10))} s', 34, YEL if pE < 1 else GRN, sc=pop(t, 2.4, 0.3) if pE >= 1 else 1)
    c.text(900, 655, f't = {int(round(pC * 20))} s', 34, CYN if pC < 1 else GRN, sc=pop(t, 4.4, 0.3) if pC >= 1 else 1)

def s_formula_p(c, t):
    title(c, t, 'GÜÇ: birim zamanda yapılan iş', col=DIM, size=32)
    parts_line(c, t, 270, [('P', GRN, 'i', 0.1), (' = ', GRY, 'b', 0.3), ('W', YEL, 'i', 0.45),
                           (' / ', GRY, 'b', 0.6), ('t', CYN, 'i', 0.7)], 120)
    a = ramp(t, 1.2)
    parts_line(c, t, 385, [('P: güç', GRN, 'm', 1.2), ('     W: iş (J)', YEL, 'm', 1.2),
                           ('     t: süre (s)', CYN, 'm', 1.2)], 28)
    c.text(640, 495, 'Birimi: watt (W)', 40, GRN, sc=pop(t, 2.0))
    c.text(640, 555, '1 W = 1 J / 1 s', 30, GRY, w='m', a=ramp(t, 2.5))

def s_compare(c, t):
    title(c, t, 'Kim daha güçlü?', col=DIM, size=32)
    for x0, nm, col, tt, val, a0 in [(150, 'Ece', YEL, '10', '200', 0.1), (690, 'Can', CYN, '20', '100', 0.4)]:
        a = ramp(t, a0)
        if a <= 0: continue
        hl = x0 == 150 and t > 2.0
        c.rect(x0, 180, x0 + 440, 450, fill=mix(BGC, CARD, a),
               outline=mix(BGC, GRN if hl else col, a * (0.6 + 0.4 * abs(math.sin(t * 5))) if hl else a), w=5 if hl else 3, r=18)
        c.text(x0 + 220, 230, nm, 38, col, a=a)
        c.text(x0 + 220, 310, f'P = 2000 J / {tt} s', 32, GRY, w='m', a=ramp(t, a0 + 0.5))
        c.text(x0 + 220, 390, f'= {val} W', 56, GRN if hl else col, sc=pop(t, a0 + 0.9))
    caption(c, t, 2.0, 'Aynı işi daha kısa sürede yapanın gücü daha büyüktür.', y=560, col=YEL, size=30)

def s_daily(c, t):
    title(c, t, 'Günlük hayatta güç')
    items = [('LED ampul', 10, 0.3), ('Dizüstü bilgisayar', 60, 0.6), ('Saç kurutma makinesi', 2000, 0.9)]
    for k, (nm, val, a0) in enumerate(items):
        y = 230 + k * 120
        a = ramp(t, a0 - 0.1)
        c.text(400, y, nm, 26, GRY, w='m', anchor='rm', a=a)
        g = eio((t - a0) / 1.0)
        if g > 0:
            wd = max(8, 720 * val / 2000) * g
            c.rect(420, y - 24, 420 + wd, y + 24, fill=[CYN, YEL, ORN][k], r=8)
            c.text(420 + wd + 14, y, f'{int(round(val * g))} W', 28, GRY, anchor='lm')
    c.text(640, 600, '(yaklaşık değerler)', 22, DIM, w='m', a=ramp(t, 1.8))

def s_twow(c, t):
    title(c, t, 'Dikkat: iki farklı "W" var!', col=YEL, size=40)
    for x0, wgt, col, txt, a0 in [(190, 'i', YEL, 'iş (fiziksel nicelik)', 0.2), (690, 'b', GRN, 'watt (güç birimi)', 0.6)]:
        a = ramp(t, a0)
        if a <= 0: continue
        c.rect(x0, 180, x0 + 400, 470, fill=mix(BGC, CARD, a), outline=mix(BGC, col, a), w=3, r=18)
        c.text(x0 + 200, 300, 'W', 150, col, w=wgt, sc=pop(t, a0))
        c.text(x0 + 200, 420, txt, 26, GRY, w='m', a=ramp(t, a0 + 0.3))
    caption(c, t, 1.8, 'Formülde eğik W = iş     ·     Sayının yanında W = watt', y=570, size=26)

def s_summary(c, t):
    title(c, t, 'Özet', col=DIM, size=32)
    for x0, nm, col, f, u, a0 in [(150, 'İŞ', YEL, 'W = F · x', 'birimi: joule (J)', 0.1),
                                   (690, 'GÜÇ', GRN, 'P = W / t', 'birimi: watt (W)', 0.5)]:
        a = ramp(t, a0)
        if a <= 0: continue
        c.rect(x0, 160, x0 + 440, 470, fill=mix(BGC, CARD, a), outline=mix(BGC, col, a), w=3, r=18)
        c.text(x0 + 220, 225, nm, 46, col, sc=pop(t, a0))
        c.text(x0 + 220, 325, f, 58, GRY, w='i', a=ramp(t, a0 + 0.3))
        c.text(x0 + 220, 415, u, 28, col, w='m', a=ramp(t, a0 + 0.5))
    caption(c, t, 2.0, 'İş: aktarılan enerji     ·     Güç: aktarımın hızı', y=565, col=GRY, size=30)

def s_quiz(c, t):
    sc = pop(t, 0.05)
    if sc > 0:
        c.rect(640 - 80 * sc, 110 - 30 * sc, 640 + 80 * sc, 110 + 30 * sc, fill=YEL, r=30)
        c.text(640, 112, 'SORU', 34, BGC, sc=sc)
    c.text(640, 235, '60 kg kütleli Ali, 3 m yüksekliğe', 38, GRY, w='m', a=ramp(t, 0.3))
    c.text(640, 295, '6 saniyede çıkıyor.', 38, GRY, w='m', a=ramp(t, 0.6))
    c.text(640, 365, 'Ali\'nin gücü kaç watt\'tır?', 42, YEL, a=ramp(t, 0.9))
    c.text(640, 425, '(g = 10 N/kg)', 26, DIM, w='m', a=ramp(t, 1.1))
    a = ramp(t, 1.4)
    c.text(640, 545, 'Videoyu durdur ve çöz!', 34, mix(GRY, YEL, 0.5 + 0.5 * math.sin(t * 6)), a=a)
    g = clamp((t - 1.4) / 3.0)
    if a > 0:
        c.rect(340, 605, 940, 621, fill=CARD, r=8)
        c.rect(340, 605, 340 + max(16, 600 * (1 - g)), 621, fill=YEL, r=8)

def s_answer(c, t):
    sc = pop(t, 0.05)
    if sc > 0:
        c.rect(640 - 100 * sc, 110 - 30 * sc, 640 + 100 * sc, 110 + 30 * sc, fill=GRN, r=30)
        c.text(640, 112, 'ÇÖZÜM', 34, BGC, sc=sc)
    c.text(640, 250, 'W = m · g · h = 60 · 10 · 3 = 1800 J', 38, GRY, w='m', a=ramp(t, 0.3))
    c.text(640, 335, 'P = W / t = 1800 J / 6 s', 38, GRY, w='m', a=ramp(t, 1.0))
    sc2 = pop(t, 1.8, 0.4)
    if sc2 > 0:
        c.rect(640 - 230 * sc2, 455 - 60 * sc2, 640 + 230 * sc2, 455 + 60 * sc2, fill=(26, 60, 52), outline=GRN, w=4, r=20)
        c.text(640, 458, 'P = 300 W', 76, GRN, sc=sc2)

def s_end(c, t):
    parts_line(c, t, 300, [('İŞ', YEL, 'b', 0.05), (' ve ', GRY, 'm', 0.2), ('GÜÇ', YEL, 'b', 0.35)], 80)
    c.text(640, 385, '10. Sınıf Fizik  ·  Enerji Ünitesi', 28, GRY, w='m', a=ramp(t, 0.5))
    c.text(640, 520, 'Hazırlayan: Irmak Dinmez', 30, YEL, w='m', a=ramp(t, 0.9))

# isim, süre, fonksiyon, ses olayları (zaman, tür)
SCENES = [
    ('01_baslik', 3.5, s_title, [(0.1, 'pop'), (0.5, 'pop'), (1.5, 'whoosh')]),
    ('02_duvar', 3.5, s_wall1, [(0.0, 'whoosh')]),
    ('03_is_sifir', 3.5, s_wall2, [(0.7, 'stamp')]),
    ('04_kutu', 4.0, s_push, [(0.0, 'whoosh'), (2.7, 'ding')]),
    ('05_formul_is', 4.0, s_formula_w, [(0.0, 'whoosh'), (0.1, 'pop'), (0.45, 'pop'), (0.7, 'pop'), (2.0, 'pop')]),
    ('06_ornek', 4.0, s_example, [(0.0, 'whoosh')] + [(1.0 + i * 0.12, 'tick') for i in range(13)] + [(2.6, 'ding')]),
    ('07_egik', 4.0, s_angle, [(0.0, 'whoosh'), (1.0, 'pop')]),
    ('08_canta', 4.0, s_bag, [(0.0, 'whoosh'), (2.2, 'stamp')]),
    ('09_kaldir', 4.0, s_lift, [(0.0, 'whoosh')] + [(1.6 + i * 0.12, 'tick') for i in range(8)] + [(2.6, 'ding')]),
    ('10_hizli', 3.0, s_question, [(0.0, 'whoosh'), (0.9, 'pop')]),
    ('11_merdiven', 4.5, s_stairs, [(0.0, 'whoosh'), (2.4, 'ding'), (4.4, 'pop')]),
    ('12_formul_guc', 4.0, s_formula_p, [(0.0, 'whoosh'), (0.1, 'pop'), (0.45, 'pop'), (0.7, 'pop'), (2.0, 'pop')]),
    ('13_karsilastir', 4.0, s_compare, [(0.0, 'whoosh'), (1.0, 'pop'), (1.3, 'pop'), (2.0, 'ding')]),
    ('14_gunluk', 4.0, s_daily, [(0.0, 'whoosh'), (0.3, 'pop'), (0.6, 'pop'), (0.9, 'pop')]),
    ('15_iki_w', 3.5, s_twow, [(0.0, 'whoosh'), (0.2, 'pop'), (0.6, 'pop')]),
    ('16_ozet', 4.0, s_summary, [(0.0, 'whoosh'), (0.1, 'pop'), (0.5, 'pop')]),
    ('17_soru', 4.5, s_quiz, [(0.0, 'whoosh'), (0.05, 'pop')]),
    ('18_cozum', 4.0, s_answer, [(0.0, 'whoosh'), (1.8, 'ding')]),
    ('19_son', 3.0, s_end, [(0.0, 'whoosh')]),
]

def render_frame(idx, t):
    name, dur, fn, _ = SCENES[idx]
    c = C(); fn(c, t)
    u = eio(t / dur)
    z = 1.0 + 0.045 * (u if idx % 2 == 0 else 1 - u)
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
            i, tt = spec.split(':'); render_frame(int(i), float(tt)).save(os.path.join(outdir, f'p{i}_{tt}.png'))
    elif mode == 'scenes':
        outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
        for i in map(int, sys.argv[3:]): render_scene(i, outdir)
