# 2_modulation/code_lerpbend.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time, random
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB

while True:
    # set bend start pitch based on current note, up or down one octave
    bend_amount = random.uniform(-1, 1)
    # pick a new bend time 0.1 to 0.5
    bend_time = random.uniform(0.1, 0.5)
    # or if you want to use the knobs
    #bend_amount = -1 + knobA.value/65535 * 2  
    #bend_time = (knobB.value/65535) * 0.4 + 0.1
    
    # this LFO automatically runs the lerp position from 0-1 over a given time
    lerp_pos = synthio.LFO(once=True, rate=1/bend_time,
                           waveform=np.array((0,32767), dtype=np.int16))
    # this MathOperation ranges from "start_val" to "end_val" over "bend_time"
    # where "start_val" is our bend_amount and "end_val" is 0 (our root pitch)
    bend_lerp = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP,
                             bend_amount, 0.0, lerp_pos)
    note = synthio.Note(synthio.midi_to_hz(random.randint(48,60)))
    note.bend = bend_lerp   # attach our lerp to the bend

    print("bending from %.2f in %.2f seconds" % (bend_lerp.a, 1/lerp_pos.rate))

    synth.press(note)
    time.sleep(1)  # wait for bend to happen
    synth.release(note)
    time.sleep(0.1)
