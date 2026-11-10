# v8: v7 ritmi (%20 yavaş) + yazılı sahnelerin sonunda okuma süresi
import sys, os
import anim_v6 as b
F = 1.2
HOLD = {'01_baslik': 1.0, '02_maden': 1.5, '03_makine': 2.0, '04_soru': 2.5, '05_olcum': 2.5,
        '06_deney1': 3.0, '07_deney2': 3.0, '08_tablo': 3.0, '09_descartes': 3.0, '10_sira_sende': 2.0,
        '11_dene': 3.5, '12_duty': 3.5, '13_coriolis': 2.5, '14_genelle': 3.0, '15_formul_sen': 1.5,
        '16_formul': 3.0, '17_duvar': 2.0, '18_tasima': 2.0, '19_kanal': 3.0, '20_test': 2.0,
        '21_cozum': 2.5, '22_zincir': 3.0, '23_guc': 2.5, '24_son': 1.0}
def _wrap(fn): return lambda c, t: fn(c, t / F)
SCENES = [(n, d * F + HOLD[n], _wrap(fn), [(te * F, k) for te, k in ev]) for n, d, fn, ev in b.SCENES]
b.SCENES = SCENES
if __name__ == '__main__':
    outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
    for i in map(int, sys.argv[3:]): b.render_scene(i, outdir)
