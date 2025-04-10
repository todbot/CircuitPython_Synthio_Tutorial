# [Synthio Tutorial](.#sections): 5. MIDI

<!--ts-->
   * [Using adafruit_midi for NoteOn/NoteOff](#using-adafruit_midi-for-noteonnoteoff)
   * [Using TMIDI for NoteOn/NoteOff](#using-tmidi-for-noteonnoteoff)
   * [Keeping track of playing notes](#keeping-track-of-playing-notes)
   * [Responding to velocity](#responding-to-velocity)
   * [Responding to pitch-bend](#responding-to-pitch-bend)
   * [Responding to CCs](#responding-to-ccs)
   * [Implementing portamento](#implementing-portamento)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->
<!-- Added by: tod, at: Wed Apr  9 17:31:36 PDT 2025 -->

<!--te-->

## Using adafruit_midi for NoteOn/NoteOff

In most CircuitPython MIDI examples, you will see [`adafruit_midi`](https://docs.circuitpython.org/projects/midi/en/latest/api.html)
used as the MIDI parser. It's full-featured and pretty easy to use.
It let's you filter events based on channel when you construct the parser.
Since every MIDI message type is represented by its own class,
it requires you to import every message type you could conceivably receive.

The below example is the same from the Getting Started section: a simple
square-wave MIDI synth.

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

The [`tmidi`](https://circuitpython-tmidi.readthedocs.io/en/latest/api.html) library
is much more stripped down. It is based on [`winterbloom_smolmidi`](https://github.com/wntrblm/Winterbloom_SmolMIDI), which is intentionally
minimal and low-level. It's my belief that `tmidi` is more efficent at handling
higher MIDI rates since it's less complex.  In regular use for noteOn/noteOff,
it's very similar to `adafruit_midi`.  The examples in this tutorial use `tmidi`
but translating to `adafruit_midi` is pretty simple.
Here is the Getting Started example again.

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

A simple solution is to use a Python dict, let's call it `notes_playing`,
with keys as the MIDI note number and value being the `Note` object that's sounding.

In this example, the synth voice is two sawtooth oscillators, detuned slightly,
so we keep them both as the value of the `notes_playing` dict.

```py
# 5_midi/code_midi_notetrack.py
import usb_midi
import synthio
import ulab.numpy as np
import tmidi
from synth_setup import synth, knobA

# saw wavs sound cool
wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)

midi_usb = tmidi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1])

notes_playing = {}  # keys = midi_note, value = (synthio.Note1, synthio.Note2)
while True:
    DETUNE = 1 + 0.01*(knobA.value/65535)  # lets knobA control how much detune
    if msg := midi_usb.receive():
        print("midi:", msg)
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
```

## Responding to velocity

Generally, MIDI key velocity is mapped to the amplitude envelope in some way.
At the simplest, higher velocity = louder note. But velocity is also mapped
to amplitude envelope attack time to emulate a harder vs softer striking of a string.


```py
# 5_midi/code_midi_velocity.py
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

From the [modulation section](README-2-Modulation.md) you'll recall the `note.bend`
property.

```py


```

## Responding to CCs

```py
```

## Implementing portamento

Portamento, or "glide", is the sliding of an instrument's note from one pitch to another.
This is different from pitch bend, which is usually a temporary deviation from a set pitch.

In `synthio`, we don't have an explicit portamento feature. We can implement it in a
variety of ways.  One way is to add a `MathOperation.CONSTRAINED_LERP` to the `note.frequency`.


```py
import time, random
import synthio
from synth_setup import synth, knobA

midi_note = 48
note = synthio.Note(synthio.midi_to_hz(midi_note))
synth.press(note)   # start the note sounding

while True:
    new_midi_note = random.randint(36, 72)
    new_pitch = synthio.midi_to_hz(new_midi_note)


```
