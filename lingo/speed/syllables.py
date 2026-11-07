"""Automatic syllable-nucleus detection (after de Jong & Wempe 2009, 'Praat script to detect syllable nuclei'):
a syllable = an intensity peak that stands out from its surroundings and is voiced.
python3 speed/syllables.py file.wav  -> prints count, rate and peak times (also importable: nuclei(path))"""
import sys, numpy as np, parselmouth

def nuclei(path, silence_db=-25, min_dip=2.0, min_gap=0.08):
    snd = parselmouth.Sound(path).convert_to_mono()
    it = snd.to_intensity(minimum_pitch=50, time_step=0.01)
    t, v = it.xs(), it.values[0]
    thr = max(np.percentile(v, 99) + silence_db, np.median(v))
    pitch = snd.to_pitch_ac(time_step=0.01, pitch_floor=60, pitch_ceiling=500)
    peaks = [i for i in range(1, len(v) - 1) if v[i] > thr and v[i] >= v[i - 1] and v[i] > v[i + 1]]
    keep = []
    for i in peaks:
        if keep:  # needs a dip of min_dip dB since the previous kept peak, else keep the higher of the two
            j = keep[-1]; dip = v[j:i + 1].min()
            if min(v[j], v[i]) - dip < min_dip or t[i] - t[j] < min_gap:
                if v[i] > v[j]: keep[-1] = i
                continue
        keep.append(i)
    out = [float(t[i]) for i in keep if pitch.get_value_at_time(float(t[i])) == pitch.get_value_at_time(float(t[i]))]  # voiced only
    return out

if __name__ == "__main__":
    p = sys.argv[1]; n = nuclei(p)
    dur = parselmouth.Sound(p).duration
    print(len(n), "syllables in", round(dur, 2), "s =", round(len(n) / dur, 2), "syl/s")
