# [Synthio Tutorial](..): MIDI

<!--ts-->
* [Synthio Tutorial: MIDI](#synthio-tutorial-midi)
   * [Using adafruit_midi for NoteOn/NoteOff](#using-adafruit_midi-for-noteonnoteoff)
   * [Using TMIDI for NoteOn/NoteOff](#using-tmidi-for-noteonnoteoff)
   * [Keeping track of playing notes](#keeping-track-of-playing-notes)
   * [Responding to velocity](#responding-to-velocity)
   * [Responding to pitch-bend](#responding-to-pitch-bend)
   * [Responding to CCs](#responding-to-ccs)
   * [Implementing portamento](#implementing-portamento)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->
<!-- Added by: tod, at: Sun Mar 30 14:20:36 PDT 2025 -->

<!--te-->

## Using adafruit_midi for NoteOn/NoteOff

```py
# 5_midi/code_midi.py
import usb_midi
import adafruit_midi
from adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from synth_setup import synth

# create a MIDI parser using the USB MIDI input port, listening to channel 1
midi_usb = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], in_channel=0 )

while True:
    if msg := midi.receive():
        print("midi:",msg)
        # noteOn must have velocity > 0
        if isinstance(msg, NoteOn) and msg.velocity != 0:
            synth.press( msg.note )
        # some synths do noteOff as noteOn w/ zero velocity
        elif isinstance(msg,NoteOff) or isinstance(msg,NoteOn) and msg.velocity==0:
            synth.release( msg.note )
```

## Using TMIDI for NoteOn/NoteOff

```py
# 5_midi/code_tmidi.py
import usb_midi
import tmidi
from synth_setup import synth

# create a MIDI parser using USB MIDI input and output ports
midi_usb = tmidi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1])

while True:
    if msg := midi_usb.receive():
        print("midi:", msg)
        # noteOn must have velocity > 0
        if msg.type == tmidi.NOTE_ON and msg.velocity != 0:
            synth.press(msg.note)
        # some synths do noteOff as noteOn w/ zero velocity
        elif msg.type in (tmidi.NOTE_OFF, tmidi.NOTE_ON) and msg.velocity == 0:
            synth.release(msg.note)
```

## Keeping track of playing notes

If you just pass in MIDI note numbers to `synth.press()` you do not need to
keep track of which notes, `synthio` will do that for you. But for the more complex
`Note` objects, we need to keep track of those so we can properly call `synth.release()`
on them.

A simple solution is to use a Python dict, with keys as the MIDI note number
and value being the `Note` object.

```py
# 5_midi/code_notetrack.py
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
```

## Responding to velocity

Generally, MIDI key velocity is mapped to the amplitude envelope in some way.
At the simplest, higher velocity = louder note. But velocity is also mapped
to amplitude envelope attack time to emulate a harder vs softer striking of a string.


```py
# 5_midi/code_velocity.py
import usb_midi
import synthio
import tmidi
from synth_setup import synth

midi_usb = tmidi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1])

notes_playing = {}  # keys = midi_notes, vals = Note objs

while True:
    if msg := midi_usb.receive():
        print("midi:", msg)
        # noteOn must have velocity > 0
        if msg.type == tmidi.NOTE_ON and msg.velocity != 0:
            velocity_normalized = msg.velocity/127
            note = synthio.Note(synthio.midi_to_hz(msg.note),
                                envelope = synthio.Envelope(
                                    # attack level goes up with higher velocity
                                    attack_level = 0.5 + 0.5 * velocity_normalized,
                                    # sustain level goes up with higher velocity
                                    sustain_level = 0.5 + 0.4 * velocity_normalized,
                                    # attack time is faster with higher velocity
                                    attack_time = 1.0 - 0.9 * velocity_normalized,
                                    # release time is faster with higher velocity
                                    release_time = 1.5 - 1.2 * velocity_normalized,),
                                )
            synth.press(note)
            notes_playing[msg.note] = note
        elif msg.type in (tmidi.NOTE_OFF, tmidi.NOTE_ON) and msg.velocity == 0:
            if note := notes_playing.get(msg.note):
                synth.release(note)
```

## Responding to pitch-bend

## Responding to CCs

## Implementing portamento
