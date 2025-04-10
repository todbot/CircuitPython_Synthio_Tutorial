# 2_modulation/code_tremolo_fadein.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time, random
import synthio
import ulab.numpy as np
from synth_setup import synth, knobA

fadein_pos = synthio.LFO(rate=1, once=True, waveform=np.array([0,32767], dtype=np.int16))
tremolo_lfo = synthio.LFO(rate=5, scale=0.5, offset=0.5)

fadein_tremolo_lfo = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP,
                                  1,
                                  tremolo_lfo,
                                  fadein_pos)
while True:
    midi_note = random.randint(48,60)
    note = synthio.Note(synthio.midi_to_hz(midi_note))
    note.amplitude = fadein_tremolo_lfo
    fadein_pos.retrigger()
    synth.press(note)
    for i in range(25):
        print("%.2f" % fadein_pos.value)
        time.sleep(0.05)
    #time.sleep(5)
    synth.release(note)
    time.sleep(1)
