# Synthio Tutorial: MIDI

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
<!-- Added by: tod, at: Tue Mar 25 17:34:52 PDT 2025 -->

<!--te-->

## Using adafruit_midi for NoteOn/NoteOff

```py
# 1_getting_started/code_midi.py
import usb_midi
import adafruit_midi
from adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from synth_setup import synth

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
# 1_getting_started/code_midi.py
import usb_midi, tmidi
from synth_setup import synth

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

## Responding to velocity

## Responding to pitch-bend

## Responding to CCs

## Implementing portamento
