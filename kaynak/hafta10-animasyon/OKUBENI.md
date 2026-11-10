# 10. hafta animasyonu — "GÜÇ nedir?" kaynak kodu

9. haftanın çizim yardımcılarını (`../hafta09-animasyon/anim.py`, `anim_v6.py`) kullanır: açık mavi tema, çubuk figür, yazılı ekran, %20 yavaş ritim ve okuma süreleri. Yazı tipi depodaki Poppins.

- `anim10.py` — 23 sahne (3:34): hatırlatma → kömür ve yüksekteki su (enerji = iş yapabilme yeteneği) → yapılan iş = aktarılan enerji → Watt ve "kaç ata bedel?" → düşünce deneyleri → P = W / t → watt → beygir gücü → günlük güçler → merdiven → soru/çözüm → özet → enerji biçimlerine köprü.

Üretim:
```
python3 anim10.py sheet onizleme                 # her sahneden bir kare
python3 anim10.py scenes sahneler 0 1 2 ... 22   # her sahne ayrı mp4
# sahneleri concat ile birleştir, sesi ekle:
PYTHONPATH=. python3 ../hafta09-animasyon/audio.py anim10 ses.wav
# ffmpeg: libx264 crf 26 + aac 128k, alimiter + loudnorm I=-16, TP=-2
```
