# Fizik Dijital Atölyesi — proje durumu ve standartlar

**Amaç:** 10. sınıf fizik yıllık planına göre her hafta için 4 içerik: Animasyon, Dijital Laboratuvar, Oyun, Kavrama Testi. Site tüm öğretmenler için; öğretmen "Kasım · 2. Hafta"ya tıklar, dört içeriğe ulaşır.
**Hazırlayan:** Irmak Dinmez · **Depo:** github.com/irmakdinmez-collab/fizik10at-lye (main) · **Yayın:** Netlify, depoya bağlı (adres eklenecek)

## Durum (10 Kasım 2026)
- [x] Site iskeleti: `index.html` (aylara göre hafta kartları, "Bu hafta" rozeti), `hafta.html?no=N` (tek şablon), `data/haftalar.js` + `.json` (37 hafta, plandan çıkarıldı).
- [x] 9. hafta (9–13 Kasım, İş, FİZ.10.2.1): animasyon yayında (`hafta/09/animasyon.mp4`, 3:33). Kaynak: `kaynak/hafta09-animasyon/`.
- [x] 9. hafta dijital laboratuvar (`hafta/09/lab.html`): maden arabası; 3 deney (sabit kuvvet, çamurlu ray = basamaklı, yaylı araba = doğrusal artan), ölçüm kaydı, veri tablosu, grafik altını boyama, alan otomatik boyanır (dikdörtgen, basamak, üçgen).
- [x] 9. hafta oyun (`hafta/09/oyun.html`: 4 bölüm, 10+10+15+15 soru, okuma metinleri "Paslı ray" ve "Okçunun yayı") ve kavrama testi (`hafta/09/test.html`: 8 çoktan seçmeli + 1 grafik okuma + 1 açık uçlu, öz değerlendirmeli).
- [ ] Pilot bitince: üretim standardını skill olarak yaz (önce denenmiş örnek, sonra skill).
- [ ] Sonra sıradaki haftalar: 10. hafta (23–27 Kasım, FİZ.10.2.2 iş-enerji-güç), 11. hafta (enerji biçimleri)… Geçmiş haftalar (1–8) en sona.
- [ ] Netlify adresi ve alt kısma lisans kararı (CC BY-NC-SA mı, "Tüm hakları saklıdır" mı) bekleniyor.

## Yeni içerik ekleme
Dosya `hafta/NN/` içine (`lab.html`, `oyun.html`, `test.html`, `animasyon.mp4` + `kapak.jpg`); `data/haftalar.js` ve `.json` içinde o haftanın `icerik` alanına `{"dosya": "...", "baslik": "..."}` eklenir; main'e gönderilir.

## Ortak standart
- Türkçe; açık mavi tema (zemin #def0fe→#b6d8f4, metin #16264a, vurgu turuncu #cd7800, mavi #0070c4, yeşil #168c48, kırmızı #cc2048); Poppins (siteyle gelir).
- Ünite renkleri: Kuvvet ve Hareket mavi, Enerji turuncu, Elektrik mor #7b4fc9, Dalgalar camgöbeği #0e9488.
- Her içerikte "Hazırlayan: Irmak Dinmez". Tek dosya, dış bağımlılık yok, internetsiz çalışır, akıllı tahtada büyük dokunma alanları.
- Her içerik haftanın kazanımını karşılamalı (kontrol listesinde ilk madde).

## Animasyon standardı (9. haftadan öğrenilenler)
- Formül baştan verilmez: tarihsel/gerçek bir problem → düşünce deneyleri → öğrencinin kendisi formüle ulaşır ("Sıra sende!" duraklamaları, süre çubuğu) → formül → tanımı sınama → soru + çözüm → özet → sonraki konuya köprü.
- Seslendirme yok, ekran yazılı; kendi üretilen müzik/efekt. Çubuk figür çizim tarzı (insan ve hayvanlar).
- Ritim sakin: animasyonlar yavaş, yazılı sahnelerin sonunda 1–3,5 sn okuma süresi. Öğrenciler yazıyı takip edebilmeli.
- Birimler SI (kg, m); tarihsel birimler (libre, ayak) kullanılmaz.
- Teslimden önce her sahneden kare kontrolü (taşan yazı, eksik glif, okunmayan renk).

## Dijital laboratuvar standardı
Beş bölüm: 1) Amaç (kazanım + tek soru) 2) Tahmin et 3) Deney (simülasyon, ölçüm aletleri, "Ölçümü kaydet") 4) Veri tablosu ve grafik 5) Sonuca ulaş (yönlendirici sorular, en sonda "Çözümü göster"). Her lab tek bir haftanın kazanımına odaklanır.
Örnek referans: kullanıcının devre simülasyonu (seri/paralel/karışık). Düzeltilecekler: lamba direnci 0 çelişkisi (lambalar direnç sayılmalı, parlaklık P=I²R), hesap baştan açık (tahmin→ölç→genelle olmalı), ampermetre/voltmetre ve veri tablosu yok, direnç ve üreteç kazanımları ayrılmalı (21–22 / 23–24. haftalar; üreteç labında tükenme süresi göstergesi), koyu tema → açık mavi.

## Oyun standardı
Kullanıcının mevcut Duolingo formatı: her alt bölüm 4 bölüm ("1.–4. Bölüm"), 10 soru, 3 can (biterse bölüm baştan), 5 seçenek, yanlışta doğru cevap gösterilir; 3. ve 4. bölümlerde özgün okuma metninden 5 ek soru. 10. sınıf oyun renkleri sarı/açık gri idi; sitede açık mavi temaya uyum düşünülecek.

## Telif ilkeleri
Tüm soru, senaryo, çizim ve simülasyonlar özgün; ders kitabından veya başka kaynaklardan kopya yok. Kazanım kodları MEB öğretim programından; ticari yıllık plan (kimyadenizi) metni yayımlanmaz, plan dosyası depoya konmaz. Gerçek kişi fotoğrafı yok.

## Plan notları
"Kasım 1. hafta" = plan 8. hafta. Ara tatil 16–20 Kasım planda yok. Plan 33. haftanın konu adı hatalıydı; kazanıma göre "Su Dalgalarında Yansıma ve Kırılma" yapıldı.
