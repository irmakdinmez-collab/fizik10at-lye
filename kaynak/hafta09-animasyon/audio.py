import numpy as np, wave
import sys, importlib
SCENES = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else "anim").SCENES
OUT = sys.argv[2] if len(sys.argv) > 2 else "ses.wav"
SR = 44100
total = sum(d for _, d, _, _ in SCENES)
N = int(total * SR) + SR
rng = np.random.default_rng(3)

def note(f, dur, amp, decay=3.0, harm=(1, .5, .25)):
    t = np.arange(int(dur * SR)) / SR
    y = sum(a * np.sin(2 * np.pi * f * (k + 1) * t) for k, a in enumerate(harm))
    env = np.exp(-decay * t) * np.minimum(1, t / 0.005)
    return amp * y * env

def add(buf, x, t0):
    i = int(t0 * SR); j = min(len(buf), i + len(x))
    if i < len(buf): buf[i:j] += x[:j - i]

music = np.zeros(N)
bpm = 104; beat = 60 / bpm
# C - Am - F - G, her akor 2 ölçü
chords = [[261.63, 329.63, 392.0], [220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 246.94, 293.66]]
bar = 4 * beat
k = 0; t = 0.0
while t < total:
    ch = chords[(k // 2) % 4]
    # pad
    dur = bar
    tt = np.arange(int(dur * SR)) / SR
    pad = sum(np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * f * 2.003 * tt) for f in ch)
    env = np.minimum(1, tt / 0.4) * np.minimum(1, (dur - tt) / 0.4)
    add(music, 0.035 * pad * env, t)
    # bas
    add(music, note(ch[0] / 2, beat * 1.8, 0.22, 2.0, (1, .3)), t)
    add(music, note(ch[0] / 2, beat * 1.8, 0.16, 2.0, (1, .3)), t + 2 * beat)
    # arpej (sekizlik)
    seq = [ch[0] * 2, ch[1] * 2, ch[2] * 2, ch[1] * 2]
    for e in range(8):
        add(music, note(seq[e % 4], 0.5, 0.07, 6.0, (1, .35, .1)), t + e * beat / 2)
    # hafif hi-hat
    for e in range(8):
        n = rng.standard_normal(int(0.03 * SR)) * np.exp(-np.arange(int(0.03 * SR)) / SR * 150)
        n = np.diff(n, prepend=0)
        add(music, 0.02 * n, t + e * beat / 2 + beat / 4)
    t += bar; k += 1

sfx = np.zeros(N)
def whoosh():
    d = 0.4; n = int(d * SR); x = rng.standard_normal(n)
    # basit kayan alçak geçiren
    out = np.zeros(n); y = 0
    for i in range(n):
        a = 0.02 + 0.25 * np.sin(np.pi * i / n) ** 2
        y += a * (x[i] - y); out[i] = y
    return 0.6 * out * np.sin(np.pi * np.arange(n) / n) ** 2
def popf():
    d = 0.12; t = np.arange(int(d * SR)) / SR
    f = 900 * np.exp(-t * 12)
    return 0.35 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 25)
def tick():
    t = np.arange(int(0.025 * SR)) / SR
    return 0.15 * np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 200)
def ding():
    t = np.arange(int(0.9 * SR)) / SR
    return 0.22 * (np.sin(2 * np.pi * 1318.5 * t) + 0.6 * np.sin(2 * np.pi * 1975.5 * t)) * np.exp(-t * 4.5)
def stamp():
    t = np.arange(int(0.25 * SR)) / SR
    return 0.5 * (np.sin(2 * np.pi * 110 * t) * np.exp(-t * 18) + 0.3 * rng.standard_normal(len(t)) * np.exp(-t * 40))
W_ = whoosh(); FX = {'whoosh': W_, 'pop': popf(), 'tick': tick(), 'ding': ding(), 'stamp': stamp()}
off = 0.0
for _, d, _, ev in SCENES:
    for te, kind in ev: add(sfx, FX[kind], off + te)
    off += d

# müzik efektlerin ~12 dB altında kalacak şekilde
mix_ = music / np.abs(music).max() * 0.25 + sfx / max(1e-9, np.abs(sfx).max()) * 0.9
n_end = int(total * SR)
mix_ = mix_[:n_end]
fade = int(2.0 * SR); mix_[-fade:] *= np.linspace(1, 0, fade)
mix_[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))
mix_ /= np.abs(mix_).max() * 1.05
pcm = (mix_ * 32767).astype(np.int16)
with wave.open(OUT, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('total', total)
