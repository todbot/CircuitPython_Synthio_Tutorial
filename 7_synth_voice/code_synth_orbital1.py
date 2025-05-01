import time, random
import synthio
from synth_setup import synth, knobA, knobB

import todsynth
import synth_orbital1

p = todsynth.Patch()
p.filter_attack_time= 0.1
p.filter_release_time= 0.99
p.release_time = 1.0

#s = todsynth.Synth(synth)
s = synth_orbital1.Orbital1Synth(synth, p)

while True:
    midi_note = random.choice( (52, 52+7, 52+4, 52+9) )
    midi_note2 = midi_note+7
    print("press", midi_note)
    s.press(midi_note)
    s.press(midi_note2)
    time.sleep(0.1)
    print("release")
    s.release(midi_note)
    s.release(midi_note2)
    time.sleep(.4)
