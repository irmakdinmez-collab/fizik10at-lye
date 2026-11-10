# 9. hafta animasyonu — "İŞ nedir?" kaynak kodu

Python + Pillow + ffmpeg ile kareler çizilir. Ses (müzik + efekt) kodla üretilir; dış ses/görsel yok.

- `anim.py` — ortak çizim yardımcıları (C sınıfı, figure, yazı, renkler) + ilk sürüm "İş ve Güç" (73 sn).
- `anim_v2.py` — keşfettiren senaryo (24 sahne). v3: kg/metre, v4–v5: çubuk at, v6: açık mavi tema.
- `anim_v8.py` — YAYINDAKİ SÜRÜM: v6 + %20 yavaş ritim + yazılı sahnelerde okuma süresi (3:33).
- `audio.py` — müzik ve efekt sesi: `python3 audio.py anim_v8 ses.wav`

Üretim:
```
python3 anim_v8.py scenes sahneler 0 1 2 ... 23      # her sahne ayrı mp4
# sahneleri concat ile birleştir, sesi ekle (alimiter + loudnorm I=-16, TP=-2)
python3 anim_v6.py sheet onizleme                    # her sahneden bir kare
```
