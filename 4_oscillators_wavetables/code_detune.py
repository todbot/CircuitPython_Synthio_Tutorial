# 4_oscillators_waveforms/code_detune.py
# part of todbot circuitpython synthio tutorial
# 14 Apr 2025 - @todbot / Tod Kurt
#
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB

wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)  # saw osc

midi_note = 45
while True:
    num_oscs = int(knobA.value/65535 * 6 + 1)  # up to 7 oscillators
    detune = (knobB.value/65535) * 0.01  # up to 10% detune
    print("num_oscs: %d detune: %.4f" % (num_oscs,detune))
    notes = []  # holds note objs being pressed
    # simple detune, always detunes up
    for i in range(num_oscs):
        f = synthio.midi_to_hz(midi_note) * (1 + i*detune)  # detune!
        notes.append( synthio.Note(f, waveform=wave_saw) )
    synth.press(notes)
    time.sleep(0.5)
    synth.release(notes)
    time.sleep(0.1)
