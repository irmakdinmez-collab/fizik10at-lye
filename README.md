# Fizik Dijital Atölyesi · 10. Sınıf

Yıllık plana göre her hafta için dört içerik: **Dijital Laboratuvar**, **Animasyon**, **Oyun**, **Kazanım Testi**.
Hazırlayan: Irmak Dinmez

## Yapı
```
index.html            Ana sayfa: aylara göre hafta kartları
hafta.html?no=9       Hafta sayfası (tek şablon, veriyi okur)
data/haftalar.js      Haftalar ve içerik bağlantıları (sitenin tek veri kaynağı)
data/haftalar.json    Aynı verinin JSON kopyası
assets/               Stil, ortak kod, yazı tipleri (Poppins, SIL OFL)
hafta/NN/             O haftanın dosyaları: animasyon.mp4, kapak.jpg, lab.html, oyun.html, test.html
```

## Yeni içerik eklemek
1. Dosyayı `hafta/NN/` klasörüne koy (ör. `hafta/09/lab.html`).
2. `data/haftalar.js` ve `data/haftalar.json` içinde o haftanın `icerik` alanına ekle:
   `"lab": {"dosya": "hafta/09/lab.html", "baslik": "Kuvvet–yol grafiği ve iş"}`
3. GitHub'a gönder; Netlify siteyi kendiliğinden günceller.

## Telif ilkeleri
- Tüm sorular, senaryolar, çizimler ve simülasyonlar özgündür; ders kitabından veya başka kaynaklardan soru/metin/görsel kopyalanmaz.
- Kazanım kodları ve başlıkları MEB Fizik Dersi Öğretim Programı'ndan alınır; ticari yıllık plan metinleri yayımlanmaz.
- Yalnızca açık lisanslı yazı tipi ve kendi üretilen müzik/efektler kullanılır; dış görseller kullanılmaz.
