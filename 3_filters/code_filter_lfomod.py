# 3_filters/code_filter_lfomod.py
import time, synthio
import ulab.numpy as np
from synth_setup import synth, knobA, knobB
midi_note = 60
note = synthio.Note(synthio.midi_to_hz(midi_note))
# make a custom waveform, a sawtooth wave, more on this later
note.waveform = np.linspace(32000, -32000, num=128, dtype=np.int16)

filter_lfo = synthio.LFO(rate=0.75, offset=4000, scale=3500)

filter1 = synthio.Biquad(synthio.FilterMode.LOW_PASS,
                              frequency=filter_lfo, Q=1.5)
note.filter = filter1
synth.press(note)

while True:
    print("note freq: %6.2f filter freq: %6.2f Q: %1.2f" %
          (note.frequency, filter1.frequency.value, filter1.Q))
    time.sleep(0.05)
