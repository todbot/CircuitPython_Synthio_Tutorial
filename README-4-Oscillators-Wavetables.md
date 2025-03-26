
# Synthio Tutorial: Oscillators & Wavetables

<!--ts-->
* [Synthio Tutorial: Oscillators &amp; Wavetables](#synthio-tutorial-oscillators--wavetables)
   * [About Oscillators](#about-oscillators)
   * [Change a note's oscillator waveform](#change-a-notes-oscillator-waveform)
      * [Making waveforms with ulab.numpy](#making-waveforms-with-ulabnumpy)
   * [Making custom waveforms](#making-custom-waveforms)
   * [Mixing between waves](#mixing-between-waves)
   * [Fatter sounds with detuned oscillators](#fatter-sounds-with-detuned-oscillators)
   * [Use a WAV as an oscillator](#use-a-wav-as-an-oscillator)
   * [Use a Wavetable](#use-a-wavetable)
   * [Wavetable scanning](#wavetable-scanning)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->
<!-- Added by: tod, at: Tue Mar 25 17:34:47 PDT 2025 -->

<!--te-->

## About Oscillators

Most synthesizers have a small selection of waveforms as the starting point
for a sound, perhaps: square wave, saw wave, and sine wave.  Some synths allow you to
"morph" between these waveshapes, gradually turning a sine into a square, for instance.
Some synths provide a square wave with an modulatable pulse width, giving a characteristic sound.
But in almost all cases, the waveforms are these simple shapes.
You can do a lot with these simple shapes.

In `synthio`, instead of these small selection of waveforms to choose from, we
can instead assign any buffer of numbers as our waveform!  This is amazing and
one of synthio's best features. Also, the waveform can be changed at any time to
alter the sound of the waveform. (Unfortunately, there's no way to tell `synthio`
exactly *when* in the waveform to switch to the new one, so you can get glitches
if you shift to waveform that's very different)

## Change a note's oscillator waveform

### Making waveforms with `ulab.numpy`

When dealing with waveforms, the [`ulab.numpy`](https://docs.circuitpython.org/en/latest/shared-bindings/ulab/numpy/index.html) library
([Learn Guide](https://learn.adafruit.com/ulab-crunch-numbers-fast-with-circuitpython/ulab-numpy-phrasebook),
[ulab book](https://micropython-ulab.readthedocs.io/en/latest/ulab-intro.html))
is very handy as it's designed to operate on large lists of numbers.
It's based on [`numpy`](https://numpy.org/doc/stable/reference/arrays.html), so one
can often find `numpy` tips that work with `ulab.numpy`.

For `synthio`, the most useful part is the basic creation of numpy arrays, with functions like:
- `np.array([0,1,2,3], dtype=np.int16)`
  -- create a 4-element numpy array of 16-bit signed integers with the contents of the Python list
- `np.linspace(-100, 100, num=50, dtype=np.int16)`
  -- create a 50-element numpy array of 16-bit signed integers, ranging from -100 to 100

Any numpy array of `dtype=np.int16` can be used as a `synthio.LFO` waveform or a `synthio.Note.waveform`.

When dealing with waveforms, the [`ulab.numpy`](https://docs.circuitpython.org/en/latest/shared-bindings/ulab/numpy/index.html) library
([Learn Guide](https://learn.adafruit.com/ulab-crunch-numbers-fast-with-circuitpython/ulab-numpy-phrasebook))
is very handy as it's designed to operate on large lists of numbers.

## Making custom waveforms

To use a custom waveforom, just assign the `.waveform` property of the `synthio.Note` object.
You can do this when constructing the `Note` object or while the Note is sounding.

Creating good waveforms is a whole other topic, but we can use some math and
`numpy` commands to help us make some simple ones, like in this example:

```py
# 4_oscillators/code_waveform1.py
import time
import ulab.numpy as np
import synthio
from synth_setup import synth

NUM_SAMPLES = 256
VOLUME = 32000  # np.int16 ranges from -32678 to 32767, this gives a little headroom

wave_sine = np.array(np.sin(np.linspace(0, 2*np.pi, NUM_SAMPLES, endpoint=False)) * VOLUME, dtype=np.int16)

wave_saw = np.linspace(VOLUME, -VOLUME, num=NUM_SAMPLES, dtype=np.int16)

wave_square = np.concatenate((np.ones(NUM_SAMPLES // 2, dtype=np.int16) * VOLUME,
                              np.zeros(NUM_SAMPLES // 2, dtype=np.int16) * -VOLUME))

wave_noise = np.array([random.randint(-VOLUME, VOLUME) for i in range(NUM_SAMPLES)], dtype=np.int16)

# collect waves created into a list for easy access
my_waves = [wave_sine, wave_saw, wave_square, wave_noise]

midi_note = 48
note1 = synthio.Note(synthio.midi_to_hz(midi_note))
synth.press(note1)   # start the note sounding, so we can change the waveform while it plays
time.sleep(0.5)  # let default full-scale square wave sound a bit
i=0
while True:
    i=(i+1) % len(my_waves)  # pick a new waveform
    note1.waveform = my_waves[i]  # set new waveform
    time.sleep(0.3)
```

## Mixing between waves

```py
# 4_oscillators/code_wavemix.py
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA

NUM_SAMPLES = 256
VOLUME = 32000

wave_sine = np.array(np.sin(np.linspace(0, 2*np.pi, NUM_SAMPLES, endpoint=False)) * VOLUME, dtype=np.int16)
wave_saw = np.linspace(VOLUME, -VOLUME, num=NUM_SAMPLES, dtype=np.int16)
# empty buffer we copy wave mix into
wave_empty = np.zeros(SAMPLE_SIZE, dtype=np.int16)

note = synthio.Note(frequency=220, waveform=wave_empty)
synth.press(note)

# mix between values a and b, works with numpy arrays too,  t ranges 0-1
def lerp(a, b, t):  return (1-t)*a + t*b

wave_pos = 0
while True:
  print(wave_pos)
  note.waveform[:] = lerp(wave_sine, wave_saw, wave_pos)
  wave_pos = (wave_pos + 0.01) % 1.0
  time.sleep(0.01)
```

## Fatter sounds with detuned oscillators

```py
# 4_oscillators_wavetables/code_detune.py
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB

midi_note = 45
while True:
    num_oscs = int(knobA.value/65535 * 6 + 1)  # up to 6 oscillators
    detune = (knobB.value/6535) * 0.01  # up to 10% detune
    print(f"num_oscs: {num_oscs} detune: {detune}")
    notes = []  # holds note objs being pressed
    # simple detune, always detunes up
    for i in range(num_oscs):
        f = synthio.midi_to_hz(midi_note) * (1 + i*detune)
        notes.append( synthio.Note(f) )
    synth.press(notes)
    time.sleep(0.5)
    synth.release(notes)
    time.sleep(0.1)
```

## Use a WAV as an oscillator


## Use a Wavetable

Note in the above example, the waves were put in an array so we could switch
them out easily. This is basically how wavetables work.



## Wavetable scanning
