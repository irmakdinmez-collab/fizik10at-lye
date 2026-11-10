#!/usr/bin/env python3
# 10. Sınıf Fizik - Enerji: "GÜÇ nedir?" (10. hafta, FİZ.10.2.2)
# 9. haftanın çizim yardımcılarını (anim.py + anim_v6.py) kullanır: açık mavi tema, çubuk figür, yazılı ekran.
import sys, os, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'hafta09-animasyon'))
import anim
FONTDIR = os.path.join(HERE, '..', '..', 'assets', 'fonts') + '/'
import anim_v6 as b
# Yazı tipleri: depodaki Poppins; tarih kartları için serbest lisanslı Liberation Serif
anim.FD = ''
anim.FONTS.update({'b': FONTDIR + 'Poppins-Bold.ttf', 'm': FONTDIR + 'Poppins-Medium.ttf',
                   'r': FONTDIR + 'Poppins-Regular.ttf', 'i': FONTDIR + 'Poppins-Bold.ttf',
                   'l': FONTDIR + 'Poppins-Regular.ttf',
                   's': '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',
                   'si': '/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'})
b._SYM.update('≈')
from anim_v6 import (W, H, S, FPS, C, mix, clamp, ease, eio, ramp, pop, figure, ground, title, caption,
                     parts_line, BGC, YEL, GRY, DIM, ORN, CYN, GRN, RED, CARD, BOXC, BOXD,
                     date_card, timer, pill, bucket, pulley, hmark, engine, coal, stick_horse, rig, block,
                     SEPT, METAL, METD, WATER, STONE)
from anim import box

PX = 110  # 1 m = 110 px (sahnelerde)

# ------------------------------------------------------------------ yardımcılar
def stopwatch(c, cx, cy, frac, label, col=GRY, r=34, a=1.0):
    if a <= 0.01: return
    c.circle((cx, cy), r, fill=mix(BGC, CARD, a), outline=mix(BGC, col, a), w=4)
    c.rect(cx - 7, cy - r - 12, cx + 7, cy - r - 2, fill=mix(BGC, col, a), r=3)
    ang = 2 * math.pi * frac
    c.line([(cx, cy), (cx + (r - 9) * math.sin(ang), cy - (r - 9) * math.cos(ang))], mix(BGC, YEL, a), 4)
    c.circle((cx, cy), 4, fill=mix(BGC, col, a))
    c.text(cx, cy + r + 24, label, 26, col, a=a)

def tank(c, x0, y0, wd, ht, level, legs_to=None):
    """Su deposu. level: 0..1 dolu."""
    if legs_to:
        for lx in (x0 + 14, x0 + wd - 14):
            c.line([(lx, y0 + ht), (lx, legs_to)], METD, 6)
        c.line([(x0 + 14, y0 + ht + (legs_to - y0 - ht) / 2), (x0 + wd - 14, y0 + ht + (legs_to - y0 - ht) / 2)], METD, 4)
    c.rect(x0, y0, x0 + wd, y0 + ht, fill=CARD, outline=METD, w=4, r=6)
    if level > 0.01:
        c.rect(x0 + 4, y0 + ht - 4 - (ht - 8) * level, x0 + wd - 4, y0 + ht - 4, fill=WATER, r=4)

def wheel(c, cx, cy, r, ang):
    c.circle((cx, cy), r, outline=(130, 90, 55), w=7)
    for k in range(8):
        a = ang + k * math.pi / 4
        c.line([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))], (150, 110, 70), 4)
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        c.line([(px, py), (px + 22 * math.cos(a), py + 22 * math.sin(a))], (130, 90, 55), 9)
    c.circle((cx, cy), 18, fill=(110, 80, 50))
    c.circle((cx, cy), 6, fill=GRY)

def stairs(c, x0, yb, n, sw, sh, col=DIM):
    pts = [(x0, yb)]
    for k in range(n):
        pts += [(x0 + k * sw, yb - (k + 1) * sh), (x0 + (k + 1) * sw, yb - (k + 1) * sh)]
    c.line(pts, col, 4)
    c.line([(x0 + n * sw, yb - n * sh), (x0 + n * sw + 90, yb - n * sh)], col, 4)

def walker(c, x, yfoot, t, speed, h=0.9, col=GRY, up=0.0):
    ph = t * speed
    hip = (x, yfoot - 66 * h)
    sw = 16 * h * math.sin(ph)
    feet = [(x + sw, yfoot - up * max(0, math.sin(ph))), (x - sw, yfoot - up * max(0, -math.sin(ph)))]
    hands = [(x + 24 * h - sw * 0.6, hip[1] - 18 * h), (x - 18 * h + sw * 0.6, hip[1] - 14 * h)]
    figure(c, hip, col, hands, feet, lean=0.12, h=h)

def bulb(c, cx, cy, a=1.0):
    c.circle((cx, cy - 18), 34, fill=mix(BGC, (255, 226, 120), a), outline=mix(BGC, (205, 150, 0), a), w=3)
    c.rect(cx - 16, cy + 14, cx + 16, cy + 38, fill=mix(BGC, METAL, a), r=4)
    for k in range(3): c.line([(cx - 15, cy + 20 + k * 7), (cx + 15, cy + 20 + k * 7)], mix(BGC, METD, a), 2)

def kettle(c, cx, cy, a=1.0):
    c.poly([(cx - 40, cy + 38), (cx + 40, cy + 38), (cx + 30, cy - 34), (cx - 30, cy - 34)], mix(BGC, (120, 170, 220), a))
    c.rect(cx - 46, cy + 34, cx + 46, cy + 46, fill=mix(BGC, (60, 70, 90), a), r=4)
    c.line([(cx + 32, cy - 24), (cx + 58, cy - 14), (cx + 54, cy + 24), (cx + 36, cy + 28)], mix(BGC, (60, 70, 90), a), 7)
    c.line([(cx - 30, cy - 20), (cx - 52, cy - 36)], mix(BGC, (60, 70, 90), a), 7)
    c.rect(cx - 16, cy - 44, cx + 16, cy - 34, fill=mix(BGC, (60, 70, 90), a), r=3)

def car(c, cx, cy, a=1.0):
    col = mix(BGC, (204, 32, 72), a)
    c.rect(cx - 80, cy - 10, cx + 80, cy + 24, fill=col, r=12)
    c.poly([(cx - 48, cy - 10), (cx - 26, cy - 42), (cx + 30, cy - 42), (cx + 54, cy - 10)], col)
    c.poly([(cx - 38, cy - 12), (cx - 22, cy - 34), (cx - 2, cy - 34), (cx - 2, cy - 12)], mix(BGC, (220, 238, 252), a))
    c.poly([(cx + 6, cy - 12), (cx + 6, cy - 34), (cx + 26, cy - 34), (cx + 42, cy - 12)], mix(BGC, (220, 238, 252), a))
    for wx in (cx - 46, cx + 46):
        c.circle((wx, cy + 24), 18, fill=mix(BGC, GRY, a)); c.circle((wx, cy + 24), 7, fill=mix(BGC, METAL, a))

def card(c, x0, y0, x1, y1, a, col=None, w=2):
    c.rect(x0, y0, x1, y1, fill=mix(BGC, CARD, a), outline=mix(BGC, col or DIM, a), w=w, r=16)

# ------------------------------------------------------------------ sahneler
def s_title(c, t):
    c.text(520, 290, 'GÜÇ', 160, YEL, sc=pop(t, 0.1))
    c.text(850, 316, 'nedir?', 70, GRY, w='m', a=ramp(t, 0.45))
    c.text(640, 445, 'İş, enerji ve güç arasındaki bağ', 34, GRY, w='m', a=ramp(t, 0.9))
    c.text(640, 500, '10. Sınıf Fizik  ·  Enerji Ünitesi', 26, DIM, w='m', a=ramp(t, 1.2))

def s_recap(c, t):
    title(c, t, 'Geçen hafta öğrendik:', y=110, col=DIM, size=32)
    parts_line(c, t, 250, [('W', YEL, 'i', 0.3), (' = ', GRY, 'b', 0.45), ('F', ORN, 'i', 0.6),
                           (' · ', GRY, 'b', 0.7), ('x', CYN, 'i', 0.8)], 110)
    c.text(640, 360, 'İş  =  kuvvet  ×  kuvvet yönünde alınan yol', 32, GRY, w='m', a=ramp(t, 1.3))
    c.text(640, 480, 'Peki iş yaparken bir şey HARCANIYOR mu?', 36, YEL, a=ramp(t, 2.6))
    c.text(640, 540, 'Makine kömür yakıyor, insan yoruluyor...', 28, DIM, w='m', a=ramp(t, 3.4))

def s_coal(c, t):
    yg = 560; ground(c, yg, 40, 1240)
    p = eio((t - 0.4) / 4.6)
    ex = 170
    engine(c, ex, yg, t, 0.9, depth=yg)
    coal(c, 405, yg, 1.5 - 1.0 * p)
    # boru ve depo
    pipe = [(ex + 108, yg - 30), (820, yg - 30), (820, 205), (880, 205)]
    c.line(pipe, METD, 10)
    if 0.4 < t < 5.2:
        L = [(pipe[i], pipe[i + 1]) for i in range(3)]
        tot = sum(math.dist(a_, b_) for a_, b_ in L)
        for k in range(10):
            u = ((t * 0.5 + k / 10) % 1) * tot
            for a_, b_ in L:
                d = math.dist(a_, b_)
                if u <= d:
                    c.circle((a_[0] + (b_[0] - a_[0]) * u / d, a_[1] + (b_[1] - a_[1]) * u / d), 4, fill=(150, 200, 240)); break
                u -= d
    tank(c, 860, 200, 220, 130, 0.1 + 0.8 * p, legs_to=yg)
    hmark(c, 1120, yg, 330, 'yüksekte' if p > 0.2 else None)
    title(c, t, 'Makine suyu yukarıdaki depoya pompalıyor.', y=88, size=32)
    caption(c, t, 2.6, 'Su yükseldikçe kömür azalıyor...', y=640, col=YEL, size=32)

def s_wheel(c, t):
    yg = 580; ground(c, yg, 40, 1240)
    p = eio((t - 0.8) / 4.2)
    tank(c, 140, 150, 220, 120, 0.9 - 0.75 * p, legs_to=yg)
    # musluk ve akan su
    c.rect(360, 236, 410, 256, fill=METD, r=4)
    flow = 0.8 < t < 5.2
    if flow:
        for k in range(14):
            u = (t * 1.3 + k / 14) % 1
            x = 410 + 70 * u; y = 246 + 120 * u * u
            c.circle((x, y), 6, fill=(110, 170, 230))
    wcx, wcy = 560, 450
    wheel(c, wcx, wcy, 88, -t * 1.6 if flow else -0.8 * 1.6)
    # ip: çark milinden makaraya, makaradan kovaya
    pcx, pcy = 960, 200
    pulley(c, pcx, pcy)
    c.line([(wcx, wcy - 18), (pcx - 17, pcy)], GRY, 3)
    by = yg - 230 * p
    hd = bucket(c, pcx + 17, by, 0.9)
    c.line([(pcx + 17, pcy), hd], GRY, 3)
    title(c, t, 'Şimdi depodaki suyu bırakalım:', y=88, size=32)
    caption(c, t, 3.4, 'Yüksekteki su çarkı döndürüyor, kovayı kaldırıyor.', y=640, size=30)
    parts_line(c, t, 690, [('Yüksekteki su da ', GRY, 'm', 4.6), ('İŞ YAPABİLİYOR!', YEL, 'b', 4.6)], 32)

def s_pause1(c, t):
    pill(c, t, 'SIRA SENDE!', YEL)
    c.text(640, 220, 'Yanan kömür de, yüksekteki su da', 38, GRY, w='m', a=ramp(t, 0.3))
    c.text(640, 280, 'iş yapabiliyor.', 38, GRY, w='m', a=ramp(t, 0.5))
    c.text(640, 380, 'İş yapabilme yeteneğine ne ad verirsin?', 36, YEL, a=ramp(t, 1.2))
    c.text(640, 520, 'Videoyu durdur ve düşün!', 34, mix(GRY, YEL, 0.5 + 0.5 * math.sin(t * 6)), a=ramp(t, 1.8))
    timer(c, t, 1.8, 5.0, y=585)

def s_energy(c, t):
    title(c, t, 'İş yapabilme yeteneğinin adı:', y=95, col=DIM, size=32)
    c.text(640, 210, 'ENERJİ', 110, YEL, sc=pop(t, 0.4))
    boxes = [('Kömür', 'enerji', 1.2), ('Yüksekteki su', 'enerji', 2.0), ('Yükselen kova', 'enerji', 2.8)]
    for k, (a_, b_, a0) in enumerate(boxes):
        x0 = 120 + k * 390; a = ramp(t, a0)
        if a <= 0: continue
        card(c, x0, 330, x0 + 260, 450, a, YEL if k == 2 else DIM)
        c.text(x0 + 130, 375, a_, 30, GRY, a=a)
        c.text(x0 + 130, 415, b_, 24, YEL, w='m', a=a)
        if k:
            g = ramp(t, a0 - 0.3)
            c.arrow((x0 - 120, 390), (x0 - 120 + 105 * g, 390), mix(BGC, ORN, g), 6, 18)
            c.text(x0 - 65, 360, 'iş', 28, ORN, w='i', a=g)
    caption(c, t, 3.8, 'İş yapıldığında enerji bir yerden başka yere AKTARILIR.', y=560, size=32)

def s_transfer(c, t):
    title(c, t, 'Yapılan iş  =  aktarılan enerji', y=88, size=36)
    yg = 560; ground(c, yg, 80, 820)
    # raf
    c.rect(540, yg - 2 * PX - 10, 760, yg - 2 * PX + 4, fill=(150, 110, 70), r=3)
    c.line([(750, yg - 2 * PX + 4), (750, yg)], (150, 110, 70), 6)
    p = eio((t - 0.6) / 2.4)
    bx = 350 + 230 * p; byy = yg - 80 - 2 * PX * p
    if p >= 1: byy = yg - 2 * PX - 10 - 80
    box(c, bx, byy, 80, '100 N')
    hip = (290 + 170 * p, yg - 66)
    hy = byy + 40
    figure(c, hip, GRY, [(bx + 2, hy), (bx + 4, hy + 18)], [(hip[0] - 14, yg), (hip[0] + 14, yg)], lean=0.1)
    hmark(c, 800, yg, yg - 2 * PX, '2 m', ticks=())
    # enerji çubuğu
    a = ramp(t, 0.3)
    c.text(1040, 190, 'Kutunun enerjisi', 26, GRY, a=a)
    c.rect(990, 220, 1090, 520, fill=mix(BGC, CARD, a), outline=mix(BGC, DIM, a), w=3, r=10)
    base = 0.25
    lvl = base + 0.55 * p
    c.rect(996, 514 - 288 * lvl, 1084, 514, fill=mix(BGC, YEL, a), r=8)
    if p > 0.05:
        c.dashed((990, 514 - 288 * base), (1090, 514 - 288 * base), GRY, 2, 6)
        c.text(1110, 514 - 288 * (base + 0.55 * p / 2), '+ ' + str(int(round(200 * p / 10) * 10)) + ' J', 30, YEL, anchor='lm')
    c.text(640, 620, 'Kutuya yapılan iş:  W = 100 N · 2 m = 200 J', 30, GRY, w='m', a=ramp(t, 3.2))
    parts_line(c, t, 672, [('Kutunun enerjisi ', GRY, 'm', 4.0), ('200 J', YEL, 'b', 4.0),
                           (' arttı.  Enerjinin birimi de joule.', GRY, 'm', 4.0)], 30)

def s_watt(c, t):
    date_card(c, t, 0.05, '1776 · James Watt', 'Yeni buhar makinesini satmak istiyordu')
    yg = 430
    c.poly([(0, yg), (W, yg), (W, H), (0, H)], (52, 40, 36))
    c.line([(0, yg), (W, yg)], (90, 140, 80), 5)
    sx = 330
    c.rect(sx - 40, yg, sx + 40, 720, fill=(16, 18, 28), r=0)
    c.rect(sx - 40, 660, sx + 40, 720, fill=WATER, r=0)
    pcx, pcy = sx, 300
    c.line([(sx - 40, yg), (pcx, pcy), (sx + 40, yg)], (120, 100, 80), 6)
    pulley(c, pcx, pcy + 42)
    pcy += 42
    p = eio((t - 0.6) / 4.0)
    by = 680 - 180 * p
    hd = bucket(c, pcx - 17, by, 0.8)
    c.line([(pcx - 17, pcy), hd], GRY, 3)
    hx = 640 + 260 * p
    hp = stick_horse(c, hx, yg, t, moving=0.6 < t < 4.6, k=1.4)
    c.line([(pcx + 17, pcy), hp], GRY, 3)
    caption(c, t, 1.2, 'Madenciler suyu atlarla çıkarıyordu.', y=210, size=30)
    c.text(640, 270, 'Müşteriler sordu:  “Bu makine kaç ata bedel?”', 32, YEL, a=ramp(t, 2.6))

def two_rigs(c, t, specs, yg=520, ytop=175):
    """specs: (cx, n, yükseklik m, başlama, süre(anim sn), etiket, saat yazısı, renk)"""
    ground(c, yg, 80, 1200)
    for cx, n, hm, t0, d, lab, sure, col in specs:
        p = eio((t - t0) / d)
        by = yg - PX * hm * p
        rig(c, cx, ytop, by, n)
        hmark(c, cx + (100 if n == 2 else 72), yg, by, (f'{hm} m' if p > 0.5 else None))
        c.text(cx, yg + 34, lab, 26, col, a=ramp(t, 0.2))
        fr = clamp((t - t0) / d)
        stopwatch(c, cx - 150, 300, fr, sure if fr >= 1 else '...', col=col, a=ramp(t, 0.2))

def s_same(c, t):
    title(c, t, 'İki makine aynı yükü aynı yüksekliğe kaldırıyor', y=70, size=32)
    two_rigs(c, t, [(400, 1, 2, 0.5, 1.6, 'Makine A', '10 s', ORN), (960, 1, 2, 0.5, 3.2, 'Makine B', '20 s', CYN)])
    caption(c, t, 4.0, 'İkisi de AYNI işi yaptı.', y=610, size=32)
    parts_line(c, t, 665, [('Ama A, bu işi ', GRY, 'm', 4.8), ('yarı sürede', YEL, 'b', 4.8), (' yaptı. Hangisi daha değerli?', GRY, 'm', 4.8)], 30)

def s_exp1(c, t):
    title(c, t, 'Düşün 1:  Aynı sürede iki kat iş yapılırsa?', y=70, size=32)
    two_rigs(c, t, [(400, 1, 2, 0.5, 2.0, '1 kova', '10 s', ORN), (960, 2, 2, 0.5, 2.0, '2 kova', '10 s', CYN)])
    caption(c, t, 3.0, '2 kovayı 10 s\'de kaldırmak = 1 kovayı 10 s\'de İKİ KEZ kaldırmak', y=610, size=28)
    parts_line(c, t, 665, [('İş ×2  (süre aynı)  →  iş yapma hızı ', GRY, 'b', 3.9), ('×2', YEL, 'b', 4.2)], 34)

def s_exp2(c, t):
    title(c, t, 'Düşün 2:  Aynı iş yarı sürede yapılırsa?', y=70, size=32)
    two_rigs(c, t, [(400, 1, 2, 0.5, 1.4, '1 kova', '5 s', ORN), (960, 1, 2, 0.5, 2.8, '1 kova', '10 s', CYN)])
    caption(c, t, 3.6, 'A, her saniyede B\'nin iki katı iş yapıyor.', y=610, size=30)
    parts_line(c, t, 665, [('Süre ½  (iş aynı)  →  iş yapma hızı ', GRY, 'b', 4.4), ('×2', YEL, 'b', 4.7)], 34)

def s_table(c, t):
    title(c, t, 'Şimdiye kadar bulduklarımız', y=110, col=DIM, size=32)
    rows = [('İş ×2', ORN, '×2', 0.3), ('Süre ×2', CYN, '½', 0.9)]
    for k, (nm, col, r_, a0) in enumerate(rows):
        y = 240 + k * 100; a = ramp(t, a0)
        if a <= 0: continue
        c.rect(220, y - 40, 1060, y + 40, fill=mix(BGC, CARD, a), r=14)
        c.text(380, y, nm, 36, col, a=a)
        c.text(560, y, '→', 40, GRY, a=a)
        parts_line(c, t, y, [('iş yapma hızı ', GRY, 'b', a0 + 0.2), (r_, YEL, 'b', a0 + 0.3)], 36, anchor_x=800)
    c.text(640, 480, 'İş yapma hızı, işle doğru, süreyle ters orantılı.', 32, YEL, a=ramp(t, 1.8))
    c.text(640, 545, 'Bunu tek bir sayıyla nasıl yazarız?', 28, GRY, w='m', a=ramp(t, 2.8))

def s_pause2(c, t):
    pill(c, t, 'ŞİMDİ FORMÜLÜ SEN KUR!', YEL)
    parts_line(c, t, 250, [('İş: ', GRY, 'm', 0.4), ('W', YEL, 'i', 0.4), ('        Süre: ', GRY, 'm', 0.7), ('t', CYN, 'i', 0.7)], 44)
    parts_line(c, t, 370, [('İş yapma hızı', GRN, 'b', 1.2), ('  =  ', GRY, 'b', 1.2), ('?', YEL, 'b', 1.5)], 70)
    c.text(640, 520, 'Videoyu durdur ve defterine yaz!', 34, mix(GRY, YEL, 0.5 + 0.5 * math.sin(t * 6)), a=ramp(t, 1.8))
    timer(c, t, 1.8, 4.5, y=585)

def s_reveal(c, t):
    title(c, t, 'Senin bulduğun büyüklüğün adı:', col=DIM, size=32)
    c.text(640, 175, 'GÜÇ', 72, GRN, sc=pop(t, 0.2))
    parts_line(c, t, 300, [('P', GRN, 'i', 0.7), (' = ', GRY, 'b', 0.85), ('W', YEL, 'i', 1.0), (' / ', GRY, 'b', 1.1), ('t', CYN, 'i', 1.2)], 110)
    parts_line(c, t, 410, [('P: güç', GRN, 'm', 1.7), ('     W: iş (J)', YEL, 'm', 1.7), ('     t: süre (s)', CYN, 'm', 1.7)], 28)
    c.text(640, 490, 'Güç: birim zamanda yapılan iş (aktarılan enerji)', 32, GRY, a=ramp(t, 2.5))
    c.text(640, 560, 'Birimi:  J / s  =  watt (W)', 40, YEL, sc=pop(t, 3.3))

def s_unit(c, t):
    sc = pop(t, 0.2)
    if sc > 0:
        c.rect(640 - 300 * sc, 230 - 70 * sc, 640 + 300 * sc, 230 + 70 * sc, fill=CARD, outline=YEL, w=4, r=20)
        c.text(640, 232, '1 W  =  1 J / s', 72, YEL, sc=sc)
    c.text(640, 370, 'Her saniye 1 joule iş yapmak (enerji aktarmak)', 32, GRY, w='m', a=ramp(t, 1.0))
    c.text(640, 430, 'Birimin adı, James Watt\'ın onuruna verildi.', 28, DIM, w='m', a=ramp(t, 1.8))
    a = ramp(t, 2.8)
    if a > 0:
        c.rect(250, 500, 1030, 600, fill=mix(BGC, (255, 244, 220), a), outline=mix(BGC, ORN, a), w=3, r=14)
        c.text(640, 532, 'Dikkat: aynı harf, iki anlam!', 26, ORN, a=a)
        parts_line(c, t, 572, [('W', YEL, 'i', 2.8), (' = 500 J  (iş)', GRY, 'm', 2.8), ('        P = 500 ', GRY, 'm', 2.8), ('W', GRN, 'b', 2.8), ('  (watt)', GRY, 'm', 2.8)], 26)

def s_horse(c, t):
    title(c, t, 'Watt\'ın ölçüsü: beygir gücü', y=70, size=34)
    yg = 470; ground(c, yg, 60, 1220)
    pcx, pcy = 330, 170
    pulley(c, pcx, pcy)
    p = eio((t - 0.5) / 2.0)
    by = yg - PX * p
    block(c, pcx - 17 - 55, by, 110, 70, '75 kg')
    c.line([(pcx - 17, pcy), (pcx - 17, by - 70)], GRY, 3)
    hmark(c, pcx - 110, yg, by, '1 m' if p > 0.5 else None)
    hx = 640 + PX * p
    hp = stick_horse(c, hx, yg, t, moving=0.5 < t < 2.5, k=1.5)
    c.line([(pcx + 17, pcy), (pcx + 17, hp[1]), hp], GRY, 3)
    stopwatch(c, 1080, 260, clamp((t - 0.5) / 2.0), '1 s' if t > 2.5 else '...', col=GRN, a=ramp(t, 0.2))
    caption(c, t, 2.6, 'Bir at, 75 kg\'lık yükü (yaklaşık 750 N) her saniye 1 m kaldırabilir.', y=545, size=28)
    c.text(640, 600, 'P = 750 J / 1 s  ≈  750 W', 36, GRY, w='m', a=ramp(t, 3.6))
    parts_line(c, t, 655, [('1 beygir gücü (bg)  ≈  ', GRY, 'm', 4.4), ('750 W', YEL, 'b', 4.4)], 34)
    c.text(640, 700, '(Bugünkü tanımlarda 1 bg, 735–746 W arasındadır.)', 20, DIM, w='m', a=ramp(t, 4.8))

def s_devices(c, t):
    title(c, t, 'Günlük hayatta güç', y=80, size=36)
    items = [(250, bulb, 'LED lamba', '10 W', 0.4), (640, kettle, 'Su ısıtıcısı', '2000 W', 1.0), (1030, car, 'Otomobil motoru', '70 000 W', 1.6)]
    for cx, fn, nm, pw, a0 in items:
        a = ramp(t, a0)
        if a <= 0: continue
        card(c, cx - 170, 150, cx + 170, 470, a)
        fn(c, cx, 270, a)
        c.text(cx, 370, nm, 28, GRY, a=a)
        c.text(cx, 425, pw, 40, YEL, a=a)
    caption(c, t, 2.6, 'Su ısıtıcısı her saniye 2000 J enerji aktarır.', y=550, size=32)
    c.text(640, 610, 'LED lamba aynı enerjiyi 200 saniyede aktarır.', 28, DIM, w='m', a=ramp(t, 3.6))

def s_stairs(c, t):
    title(c, t, 'Ali ile Bora aynı merdiveni çıkıyor (ağırlıkları eşit)', y=70, size=30)
    for x0, nm, d, sure, col, spd in [(120, 'Ali koşuyor', 1.6, '4 s', ORN, 22), (700, 'Bora yürüyor', 4.4, '12 s', CYN, 9)]:
        yb = 520; n = 6; sw = 60; sh = 40
        stairs(c, x0, yb, n, sw, sh)
        p = clamp((t - 0.5) / d)
        x = x0 - 30 + (n * sw + 70) * p
        k = clamp((x - x0) / (n * sw))
        yf = yb - n * sh * k if x > x0 else yb
        walker(c, x, yf, t, spd if 0 < p < 1 else 0, h=0.8, col=col)
        c.text(x0 + 200, yb + 40, nm, 26, col, a=ramp(t, 0.2))
        stopwatch(c, x0 + 40, 220, p, sure if p >= 1 else '...', col=col, r=30, a=ramp(t, 0.2))
    parts_line(c, t, 618, [('Aynı ağırlık, aynı yükseklik  →  ', GRY, 'm', 5.0), ('AYNI İŞ', YEL, 'b', 5.0)], 30)
    parts_line(c, t, 668, [('Ali daha kısa sürede  →  ', GRY, 'm', 5.8), ('DAHA BÜYÜK GÜÇ', GRN, 'b', 5.8)], 30)

def s_quiz(c, t):
    pill(c, t, 'SORU', YEL)
    c.text(640, 210, 'Ağırlığı 500 N olan Ece, 3 m yükseklikteki', 36, GRY, w='m', a=ramp(t, 0.3))
    c.text(640, 265, 'üst kata merdivenle 6 saniyede çıkıyor.', 36, GRY, w='m', a=ramp(t, 0.6))
    c.text(640, 345, 'a) Ece\'nin yaptığı iş kaç joule?', 36, YEL, a=ramp(t, 0.9))
    c.text(640, 400, 'b) Ece\'nin gücü kaç watt?', 36, GRN, a=ramp(t, 1.1))
    c.text(640, 520, 'Videoyu durdur ve çöz!', 34, mix(GRY, YEL, 0.5 + 0.5 * math.sin(t * 6)), a=ramp(t, 1.4))
    timer(c, t, 1.4, 4.3, y=585)

def s_answer(c, t):
    pill(c, t, 'ÇÖZÜM', GRN)
    c.text(640, 230, 'a)  W = F · x = 500 N · 3 m = 1500 J', 36, GRY, w='m', a=ramp(t, 0.3))
    c.text(640, 300, 'b)  P = W / t = 1500 J / 6 s', 36, GRY, w='m', a=ramp(t, 1.1))
    sc = pop(t, 1.8, 0.4)
    if sc > 0:
        c.rect(640 - 220 * sc, 420 - 60 * sc, 640 + 220 * sc, 420 + 60 * sc, fill=(222, 246, 230), outline=GRN, w=4, r=20)
        c.text(640, 423, 'P = 250 W', 72, GRN, sc=sc)
    c.text(640, 545, 'Koşarak 3 saniyede çıksaydı: iş yine 1500 J, güç 500 W.', 26, DIM, w='m', a=ramp(t, 2.8))

def s_chain(c, t):
    title(c, t, 'Üç kavram, tek bağ', y=100, col=DIM, size=32)
    cards = [('ENERJİ', 'iş yapabilme yeteneği', 'birimi: joule (J)', YEL, 0.3),
             ('İŞ', 'aktarılan enerji', 'W = F · x   (J)', ORN, 1.1),
             ('GÜÇ', 'iş yapma hızı', 'P = W / t   (W)', GRN, 1.9)]
    for k, (a_, b_, c_, col, a0) in enumerate(cards):
        x0 = 90 + k * 380; a = ramp(t, a0)
        if a <= 0: continue
        card(c, x0, 190, x0 + 340, 400, a, col, 3)
        c.text(x0 + 170, 245, a_, 44, col, a=a)
        c.text(x0 + 170, 310, b_, 26, GRY, w='m', a=a)
        c.text(x0 + 170, 360, c_, 26, DIM, w='m', a=a)
        if k: c.arrow((x0 - 34, 295), (x0 - 6, 295), mix(BGC, GRY, a), 5, 12)
    c.text(640, 500, 'Güç büyükse aynı enerji daha kısa sürede aktarılır.', 30, YEL, a=ramp(t, 3.0))

def s_teaser(c, t):
    c.text(640, 210, 'Enerji başka nerelerde saklanır?', 40, GRY, a=ramp(t, 0.1))
    c.text(640, 300, 'Yuvarlanan bir top, gerilmiş bir yay, sıcak bir çay...', 30, SEPT, w='s', a=ramp(t, 1.0))
    parts_line(c, t, 420, [('Sıradaki konu:  ', GRY, 'm', 2.0), ('ENERJİ BİÇİMLERİ', YEL, 'b', 2.3)], 50)
    a = ramp(t, 0.4)
    if a > 0:
        bx = 520 + 60 * math.sin(t * 2)
        c.circle((bx, 560), 26, fill=mix(BGC, ORN, a))
        c.line([(700, 560), (760, 540), (780, 580), (800, 540), (820, 580), (840, 560)], mix(BGC, CYN, a), 5)

def s_end(c, t):
    parts_line(c, t, 300, [('GÜÇ', YEL, 'b', 0.05), (' nedir?', GRY, 'm', 0.25)], 80)
    c.text(640, 385, '10. Sınıf Fizik  ·  Enerji Ünitesi', 28, GRY, w='m', a=ramp(t, 0.5))
    c.text(640, 520, 'Hazırlayan: Irmak Dinmez', 30, YEL, w='m', a=ramp(t, 0.9))

WH = 'whoosh'
BASE = [
    ('01_baslik', 3.5, s_title, [(0.1, 'pop'), (0.45, 'pop')], 1.0),
    ('02_hatirla', 4.5, s_recap, [(0.0, WH), (0.3, 'pop'), (2.6, 'ding')], 2.5),
    ('03_komur', 5.5, s_coal, [(0.0, WH)], 2.5),
    ('04_cark', 6.0, s_wheel, [(0.0, WH), (4.6, 'ding')], 3.0),
    ('05_sira_sende', 7.0, s_pause1, [(0.0, WH), (0.05, 'pop')], 2.0),
    ('06_enerji', 5.5, s_energy, [(0.0, WH), (0.4, 'pop'), (1.2, 'pop'), (2.0, 'pop'), (2.8, 'pop')], 3.0),
    ('07_aktarim', 5.5, s_transfer, [(0.0, WH), (4.0, 'ding')], 3.5),
    ('08_watt', 5.5, s_watt, [(0.0, WH), (2.6, 'pop')], 3.0),
    ('09_ayni_is', 6.5, s_same, [(0.0, WH), (2.1, 'tick'), (3.7, 'tick'), (4.8, 'pop')], 3.5),
    ('10_dusun1', 6.0, s_exp1, [(0.0, WH), (2.5, 'tick'), (4.2, 'ding')], 3.0),
    ('11_dusun2', 6.0, s_exp2, [(0.0, WH), (1.9, 'tick'), (3.3, 'tick'), (4.7, 'ding')], 3.0),
    ('12_tablo', 5.0, s_table, [(0.0, WH), (0.5, 'pop'), (1.1, 'pop')], 3.0),
    ('13_formul_sen', 6.5, s_pause2, [(0.0, WH), (0.05, 'pop'), (1.5, 'pop')], 1.5),
    ('14_formul', 5.5, s_reveal, [(0.0, WH), (0.2, 'pop'), (0.7, 'pop'), (1.0, 'pop'), (3.3, 'ding')], 3.5),
    ('15_watt_birim', 5.0, s_unit, [(0.0, WH), (0.2, 'pop'), (2.8, 'stamp')], 3.5),
    ('16_beygir', 6.0, s_horse, [(0.0, WH), (2.5, 'tick'), (4.4, 'ding')], 3.5),
    ('17_gunluk', 5.0, s_devices, [(0.0, WH), (0.4, 'pop'), (1.0, 'pop'), (1.6, 'pop')], 3.0),
    ('18_merdiven', 7.0, s_stairs, [(0.0, WH), (2.1, 'tick'), (4.9, 'tick'), (5.8, 'ding')], 3.0),
    ('19_soru', 6.0, s_quiz, [(0.0, WH), (0.05, 'pop')], 2.0),
    ('20_cozum', 4.5, s_answer, [(0.0, WH), (1.8, 'ding')], 3.0),
    ('21_zincir', 5.5, s_chain, [(0.0, WH), (0.3, 'pop'), (1.1, 'pop'), (1.9, 'pop')], 3.5),
    ('22_sonraki', 4.5, s_teaser, [(0.0, WH), (2.3, 'ding')], 2.5),
    ('23_son', 3.5, s_end, [(0.0, WH)], 1.0),
]
# 9. haftadaki gibi: %20 yavaş ritim + yazılı sahnelerin sonunda okuma süresi
F = 1.2
def _wrap(fn): return lambda c, t: fn(c, t / F)
SCENES = [(n, d * F + hold, _wrap(fn), [(te * F, k) for te, k in ev]) for n, d, fn, ev, hold in BASE]

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
    if mode == 'sheet':
        from PIL import Image
        outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
        fr = float(sys.argv[3]) if len(sys.argv) > 3 else 0.97
        ims = [render_frame(i, d * fr).resize((640, 360)) for i, (_, d, _, _) in enumerate(SCENES)]
        rows = (len(ims) + 3) // 4
        sh = Image.new('RGB', (2560, 360 * rows))
        for k, im in enumerate(ims): sh.paste(im, ((k % 4) * 640, (k // 4) * 360))
        sh.save(os.path.join(outdir, 'sheet.png'))
    elif mode == 'preview':
        outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
        for spec in sys.argv[3:]:
            i, tt = spec.split(':'); render_frame(int(i), float(tt)).save(os.path.join(outdir, f'q{int(i):02d}_{tt}.png'))
    elif mode == 'scenes':
        outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
        for i in map(int, sys.argv[3:]): render_scene(i, outdir)
    elif mode == 'total':
        print(sum(d for _, d, _, _ in SCENES))
