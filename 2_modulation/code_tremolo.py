# 2_modulation/code_tremolo.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time, random
import synthio
from synth_setup import synth, knobA

def lfo_set_min_max(lfo, lmin=0.0, lmax=1.0):
    lfo.scale = (lmax - lmin)/2
    lfo.offset = lmax - lfo.scale

while True:
    midi_note = random.randint(48,60)
    note = synthio.Note(synthio.midi_to_hz(midi_note))
    note.amplitude = synthio.LFO(rate=5) 
    
    knobA_val = 1 - (knobA.value / 65535)  # convert 0-65535 to 1-0
    lfo_set_min_max(note.amplitude, knobA_val, 1)
    print("tremolo:%.2f lfo scale:%.2f offset:%.2f"
          % (1-knobA_val, note.amplitude.scale, note.amplitude.offset))
    synth.press(note)
    time.sleep(0.5)
    synth.release(note)
    time.sleep(0.2)
