# 5_midi/code_midi_notetrack.py

import usb_midi
import synthio
import ulab.numpy as np
import tmidi
from synth_setup import synth

# saw wavs sound cool
wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)

midi_usb = tmidi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1])

notes_playing = {}  # keys = midi_note, value = synthio.Note
while True:
    if msg := midi_usb.receive():
        print("midi:", msg)
        # noteOn must have velocity > 0
        if msg.type == tmidi.NOTE_ON and msg.velocity != 0:
            note = synthio.Note(synthio.midi_to_hz(msg.note), waveform=wave_saw)
            notes_playing[msg.note] = note   # save Note by midi note
            synth.press(note)
        # some synths do noteOff as noteOn w/ zero velocity
        elif msg.type in (tmidi.NOTE_OFF, tmidi.NOTE_ON) and msg.velocity == 0:
            # get Note object for note playing with this midi note
            if note := notes_playing.get(msg.note):
                synth.release(note)
