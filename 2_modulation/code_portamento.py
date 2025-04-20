# 2_modulation/code_portamento.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time, random
import synthio
import ulab.numpy as np
from synth_setup import synth, knobA

class Glider:
    """Attach a Glider to note.bend to implement portamento"""
    def __init__(self, glide_time, midi_note):
        self.pos = synthio.LFO(once=True, rate=1/glide_time,
                               waveform=np.array((0,32767), dtype=np.int16))
        self.lerp = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP,
                                 0, 0, self.pos)
        self.midi_note = midi_note

    def update(self, new_midi_note):
        """Update the glide destination based on new midi note"""
        self.lerp.a = self.lerp.value  # current value is now start value
        self.lerp.b = self.lerp.a + self.bend_amount(self.midi_note, new_midi_note)
        self.pos.retrigger()  # restart the lerp
        self.midi_note = new_midi_note

    def bend_amount(self, old_midi_note, new_midi_note):
        """Calculate how much note.bend has to happen between two notes"""
        return (new_midi_note - old_midi_note)  * (1/12)

    @property
    def glide_time(self):
        return 1/self.pos.rate
    @glide_time.setter
    def glide_time(self, glide_time):
        self.pos.rate = 1/glide_time

glide_time = 0.25
midi_notes = [48, 36, 24, 36]
new_midi_note = midi_notes[0]

# create a portamento glider and attach it to a note
glider = Glider(glide_time, new_midi_note)
note = synthio.Note(synthio.midi_to_hz(new_midi_note), bend=glider.lerp)
synth.press(note)   # start the note sounding

i=0
while True:
    glider.glide_time = 0.5 * (knobA.value/65535) 
    new_midi_note = midi_notes[i]  # new note to glide to
    i = (i+1) % len(midi_notes)
    print("new: %d old: %d glide_time: %.2f" % (new_midi_note, glider.midi_note, glider.glide_time))
    glider.update(new_midi_note)  # glide up to new note
    time.sleep(0.5)
