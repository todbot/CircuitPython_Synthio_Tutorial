# 3_filters/code_filter_sandh.py
# part of todbot circuitpython synthio tutorial
# 14 Apr 2025 - @todbot / Tod Kurt
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB

# make a quicky saw wave for oscillator
wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)

# and a "random" wave for sample-n-hold effect
wave_rand = np.array([random.randint(-32000, 32000) for i in range(128)], dtype=np.int16)
lfo_sh = synthio.LFO(rate=0.05, interpolate=False, waveform=wave_rand, offset=300, scale=200)
lpf = synthio.Biquad(synthio.FilterMode.BAND_PASS, frequency=lfo_sh, Q=2.8)

midi_note = 36
note = synthio.Note(synthio.midi_to_hz(midi_note), waveform=wave_saw, filter=lpf)
synth.press(note)

while True:
    print("%d" % lfo_sh.value)
    time.sleep(0.05)
    vA = knobA.value/65535
    vB = knobB.value/65535
    lfo_sh.offset = 100 + vA*1000
    lfo_sh.scale = lfo_sh.offset * .75
