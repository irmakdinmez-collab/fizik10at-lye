// Ortak yardımcılar — Fizik Dijital Atölyesi
var UNITE_RENK = {
  'Kuvvet ve Hareket': 'var(--u-hareket)', 'Enerji': 'var(--u-enerji)',
  'Elektrik': 'var(--u-elektrik)', 'Dalgalar': 'var(--u-dalgalar)', 'Yıl Sonu': 'var(--u-yilsonu)'
};
var BOLUMLER = [
  { anahtar: 'lab', ad: 'Dijital Laboratuvar', aciklama: 'Tahmin et, dene, ölç, sonuca ulaş', renk: 'var(--u-dalgalar)' },
  { anahtar: 'animasyon', ad: 'Animasyon', aciklama: 'Kavramı keşfettiren kısa film', renk: 'var(--mavi)' },
  { anahtar: 'oyun', ad: 'Oyun', aciklama: '3 can, bölüm bölüm ilerleyen sorular', renk: 'var(--vurgu)' },
  { anahtar: 'test', ad: 'Kazanım Testi', aciklama: 'Kazanımı ne kadar kavradık?', renk: 'var(--yesil)' }
];
var IKON = {
  animasyon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="5" width="19" height="14" rx="3"/><path d="M10 9.5v5l4.5-2.5z" fill="currentColor"/></svg>',
  lab: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6M10 3v6L4.5 18.5A1.7 1.7 0 0 0 6 21h12a1.7 1.7 0 0 0 1.5-2.5L14 9V3"/><path d="M7.5 15h9"/></svg>',
  oyun: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="7" width="19" height="11" rx="5"/><path d="M7.5 11v3M6 12.5h3"/><circle cx="15.5" cy="11.5" r=".6" fill="currentColor"/><circle cx="17.5" cy="13.5" r=".6" fill="currentColor"/></svg>',
  test: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="18" rx="3"/><path d="M8 8.5l1.5 1.5L12 7.5M8 14.5l1.5 1.5 2.5-2.5M14 9h2.5M14 15h2.5"/></svg>'
};
function bugunISO() {
  var d = new Date();
  return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}
// Bugünü içeren hafta; tatildeyse bir sonraki hafta
function buHafta() {
  var b = bugunISO(), H = window.HAFTALAR;
  for (var i = 0; i < H.length; i++) if (b <= H[i].bit) return H[i];
  return H[H.length - 1];
}
function haftaAdi(h) { return h.ay + ' · ' + h.ayHafta + '. Hafta'; }
function kac(h) { var n = 0; BOLUMLER.forEach(function (b) { if (h.icerik[b.anahtar]) n++; }); return n; }
function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
