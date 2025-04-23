# 3_filters/code_filter_sandh.py
# part of todbot circuitpython synthio tutorial
# 14 Apr 2025 - @todbot / Tod Kurt
import time, random
import ulab.numpy as np
import synthio
from synth_setup import synth, mixer, knobA, knobB

mixer.voice[0].level = 0.5  # band pass is quieter, so raise volume
wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)  # saw osc

# and a "random" wave for sample-n-hold effect
wave_rand = np.array([random.randint(-32000, 32000) for i in range(128)], dtype=np.int16)
lfo_sh = synthio.LFO(rate=0.05, interpolate=False, waveform=wave_rand)
filt = synthio.Biquad(synthio.FilterMode.BAND_PASS, frequency=lfo_sh, Q=2.8)

midi_note = 36
note = synthio.Note(synthio.midi_to_hz(midi_note),
                    waveform=wave_saw, filter=filt)
synth.press(note)

while True:
    print("note:%d lfo_sh:%d" % (midi_note,lfo_sh.value))
    time.sleep(0.05)
    vA = knobA.value/65535  # normalize 0-1
    vB = knobB.value/65535  # normalize 0-1
    lfo_sh.offset = 100 + vA*2000  # max frequency of S&H effect
    lfo_sh.scale = lfo_sh.offset * 0.85  # 0.85 = depth of effect
    midi_note = 32 + vB * 12  # knobB controls note 32-44
    note.frequency = synthio.midi_to_hz(midi_note)
