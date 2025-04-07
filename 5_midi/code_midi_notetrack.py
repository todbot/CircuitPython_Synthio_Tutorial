# 5_midi/code_midi_notetrack.py
import usb_midi
import synthio
import ulab.numpy as np
import tmidi
from synth_setup import synth, knobA

DETUNE = 1.001  # how much to detune the second voice

# saw wavs sound cool
wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)

midi_usb = tmidi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1])

notes_playing = {}  # keys = midi_note, value = (synthio.Note1, synthio.Note2)

print("listening to USB MIDI")
while True:
    DETUNE = 1 + 0.01*(knobA.value/65535)  # lets knobA control how much detune
    if msg := midi_usb.receive():
        print("midi:", msg, "detune:", DETUNE)
        # noteOn must have velocity > 0
        if msg.type == tmidi.NOTE_ON and msg.velocity != 0:
            notes = (synthio.Note(synthio.midi_to_hz(msg.note), waveform=wave_saw),
                     synthio.Note(synthio.midi_to_hz(msg.note*DETUNE), waveform=wave_saw))
            notes_playing[msg.note] = notes   # save Notes with midi note key
            synth.press(notes)
        # some synths do noteOff as noteOn w/ zero velocity
        elif msg.type in (tmidi.NOTE_OFF, tmidi.NOTE_ON) and msg.velocity == 0:
            # get Note object for note playing with this midi note
            if notes := notes_playing.get(msg.note):
                synth.release(notes)
