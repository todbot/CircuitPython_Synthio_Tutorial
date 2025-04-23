
# [Synthio Tutorial](.#sections): 4. Oscillators & Wavetables

<!--ts-->
   * [About Oscillators](#about-oscillators)
   * [Change a note's oscillator waveform](#change-a-notes-oscillator-waveform)
   * [Mixing between waveforms](#mixing-between-waveforms)
   * [Use a Wavetable](#use-a-wavetable)
   * [Wavetable scanning](#wavetable-scanning)
   * [Use a WAV as an oscillator](#use-a-wav-as-an-oscillator)
   * [Fatter sounds with detuned oscillators](#fatter-sounds-with-detuned-oscillators)
   * [Fun with wavetables: wavetabledrone](#fun-with-wavetables-wavetabledrone)
   * [Research links](#research-links)
   * [Next Steps](#next-steps)
<!--te-->

## About Oscillators

Most synthesizers have a small selection of waveforms as the starting point
for a sound, perhaps: square wave, saw wave, and sine wave.  Some synths allow you to
"morph" between these waveshapes, gradually turning a sine into a square, for instance.
Some synths provide a square wave with an modulatable pulse width, giving a characteristic sound.
But in almost all cases, the waveforms are these simple shapes.
You can do a lot with these simple shapes.

In `synthio`, instead of these small selection of waveforms to choose from, we
can instead assign *any buffer of numbers as our waveform*!  This is amazing and
one of synthio's best features. Also, the waveform can be changed at any time to
alter the sound of the waveform. (Unfortunately, there's no way to tell `synthio`
exactly *when* in the waveform to switch to the new one, so you can get glitches
if you shift to waveform that's very different)

## Change a note's oscillator waveform

To use a different waveform than the stock square wave,
assign the `.waveform` property of the `synthio.Note` object.
You can do this when constructing the `Note` object or while the Note is sounding.

Creating good waveforms is a whole other topic, but we can use some math and
`numpy` commands to help us make some simple ones, like in this example below.

This is similar to the `numpy` commands we used to generate custom LFO waveforms,
but unlike LFO waveforms, a `Note`'s waveform doesn't interpolate between values
for us.

There are two main parameters when creating waveforms: how many samples in the wave
(`NUM_SAMPLES`) and the maximum amplitude of the those samples (`VOLUME`).  For
complex waves, having more samples will be a more accurate representation of your
sound at the expense of using up more RAM.  The maximum amplitude of a waveform
in `synthio` is a +/-32767, since internally the samples are stored as 16-bit
signed integers. In practice, it's usually good to have your waveform's max
be a little understand to help prevent clipping.

These waveforms are "single-cycle" waveforms to `synthio`. They're meant to represent
once oscillation and if your waveform contains more than one oscillation, the pitch
of your waveform will not match what `synthio` thinks it is.

```py
# 4_oscillators/code_waveform1.py
import time, random
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB

NUM = 256    # number of samples in a waveform
VOL = 32000  # loudness (volume) of samples, np.int16 ranges from 0-32767

# sine wave, just like in trig class
wave_sine = np.array(np.sin(np.linspace(0, 2*np.pi, NUM, endpoint=False)) * VOL, dtype=np.int16)

# sawtooth wave, looks like a downward ramp
wave_saw = np.linspace(VOL, -VOL, num=NUM, dtype=np.int16)

# square wave, like the default
wave_square = np.concatenate((np.ones(NUM // 2, dtype=np.int16) * VOL,
                              np.zeros(NUM // 2, dtype=np.int16) * -VOL))

# 'noise' wave made with random numbers (not a very good random noise)
wave_noise = np.array([random.randint(-VOL, VOL) for i in range(NUM)], dtype=np.int16)

my_waves = [wave_sine, wave_saw, wave_square, wave_noise]
my_wave_names = ["sine", "saw", "square", "noise"]

note1 = synthio.Note(0)  # start a note playing with default waveform
synth.press(note1)
wi=0  # wave index into my_waves
while True:
    note1.frequency = synthio.midi_to_hz(32 + int((knobA.value/65535)*32))
    note1.waveform = my_waves[wi]  # pick new wave for playing note
    print("wave:", wi, my_wave_names[wi])
    time.sleep( (knobB.value/65535) )  # knobB controls tempo
    wi=(wi+1) % len(my_waves)  # pick a new waveform
```
> [4_oscillators_waveforms/code_waveform1.py](./4_oscillators_waveforms/code_waveform1.py)


```
[ ... TBD video of code_waveform1.py TBD ... ]
```

## Mixing between waveforms

Many synths have the ability to "morph" between two different waveform shapes,
like sine wave to saw wave. With `synthio` waveforms, we can do that too, by taking
two existing waveforms and mixing them together.

The `numpy` library can help here. It efficiently performs operations on arrays
of numbers (our waveform). So we can use `numpy` to create a simple `lerp()`
function that mixes between two numpy arrays, resulting in a mixed waveform.

Note we have to do this mixing "by hand", we cannot use `synthio.MathOperation.CONSTRAINED_LERP`
because it only works on single values, not arrays/lists.
(But in a future example, you'll see how we *can* use a `synthio.LFO` for our mix position.
We just have to copy "by hand" the value from the LFO to our `lerp()` function)

In this example, a Note is played playing a wave that's the mix between a
sine wave and a saw wave.  The mix speed is controlled by knobA and knobB controls
the pitch of the continuously-sounding Note.
As the mix goes from sine wave to saw wave, it sounds almost like
the sawtooth wave is being filtered down.  This is one of the neat aspects
of doing this kind of wave mixing: we can fake filter sweeps just by mixing waves!
You'll see much more of this in the wavetable examples.

```py
# 4_oscillators_waveforms/code_wavemix.py
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB

NUM = 256    # number of samples in a waveform
VOL = 32000  # loudness (volume) of samples, np.int16 ranges from 0-32767

wave_sine = np.array(np.sin(np.linspace(0, 2*np.pi, NUM, endpoint=False)) * VOL, dtype=np.int16)
wave_saw = np.linspace(VOL, -VOL, num=NUM, dtype=np.int16)
# empty buffer we copy wave mix into
wave_empty = np.zeros(NUM, dtype=np.int16)

note = synthio.Note(frequency=220, waveform=wave_empty)
synth.press(note)

# mix between values a and b, works with numpy arrays too,  t ranges 0-1
def lerp(a, b, t):  return (1-t)*a + t*b

wave_pos = 0
while True:
  print("%.2f" % wave_pos)
  mix_speed = 0.001 + (knobA.value/65535) * 0.2  # 0.001 - 0.2
  note.waveform[:] = lerp(wave_sine, wave_saw, wave_pos)
  note.frequency = synthio.midi_to_hz(48 + (knobB.value/65535)*12)
  wave_pos = (wave_pos + mix_speed) % 1.0  # move our mix position
  time.sleep(0.01)
```
> [4_oscillators_waveforms/code_wavemix.py](./4_oscillators_waveforms/code_wavemix.py)

```
[ ... TBD video of code_wavemix.py TBD ... ]
```


## Use a Wavetable

In the `code_waveform1` example above, the waves were put in an array so we could switch
them out easily. This is how wavetables work.

Wavetables let us store several different (potentially harmonically related) waveforms
in a single unit and call each wave up indepedently.  There was a (now defunct) [site
called waveeditonline.com](https://web.archive.org/web/20221128075225/https://waveeditonline.com/)
that had a wonderful collection of free waveforms in a wavetable format, each wavetable stored as a
standard WAV file.  While the waveditonline site is gone, the "wav-files.zip] bundle it
provided lives on in various places (like [the wav-files.zip bundle here from Jul 2023](https://github.com/todbot/CircuitPython_Synthio_Tutorial/releases/download/0.3/wav-files-waveeditonline-Jul2023.zip))  Since CircuitPython can read WAV files, we can use those wavetables
to easily add new sonic textures to our synths.

In the "4_oscillators_wavetables" directory of this tutorial,
there is a "wavetables" directory containing some good wavetables from waveeditonline.
Copy the entire "wavetables" directory to the CIRCUITPY drive.
The example below will look in there. Also install the `adafruit_wave` library.
It's availble from the [CircuitPython bundle](https://circuitpython.org/libraries)
or installable with `circup install adafruit_wave` from the commandline.

In the example below, there is a small `Wavetable` class that makes loading a
wavetable and selecting a waveform within the wavetable eaiser. That class is
also available as [`wavetable.py`](4_oscillators_waveforms/wavetable.py) for your own use.
When the example is running, use knobA to pick a waveform within a wavetable and
use the button to select another wavetable.
It's amazing how many different sounds you can get so easily by using wavetables!

```py
# 4_oscillators_waveforms/code_wavetable.py
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, keys, knobA
import adafruit_wave

wave_dir = "/wavetables/"  # wavetables from old http://waveeditonline.com/
wavetables = ["BRAIDS01.WAV","DRONE.WAV","SYNTH_VO.WAV","PPG_BES.WAV"]
wavetable_num_samples = 256  # number of samples per wave in wavetable
wti = 0  # index into wavetables list

class Wavetable:
    """ A 'waveform' for synthio.Note uses a WAV containing a wavetable
    and provides a scannable wave position."""
    def __init__(self, filepath, wave_len=256):
        self.w = adafruit_wave.open(filepath)
        self.wave_len = wave_len  # how many samples in each wave
        if self.w.getsampwidth() != 2 or self.w.getnchannels() != 1:
            raise ValueError("unsupported WAV format")
        self.waveform = np.zeros(wave_len, dtype=np.int16) # empty buf to fill
        self.num_waves = self.w.getnframes() // self.wave_len
        self.set_wave_pos(0)

    def set_wave_pos(self, pos):
        """Pick which wave to use in the wavetable"""
        pos = min(max(pos, 0), self.num_waves-1)  # constrain
        samp_pos = int(pos) * self.wave_len  # get sample position
        self.w.setpos(samp_pos) # seek to wavetable location
        waveA = np.frombuffer(self.w.readframes(self.wave_len), dtype=np.int16)
        self.waveform[:] = waveA  # copy into buf
        self._wave_pos = pos

wavetable1 = Wavetable(wave_dir+wavetables[wti])  # load up wavetable

midi_note = 45  # A2
note = synthio.Note(synthio.midi_to_hz(midi_note), waveform=wavetable1.waveform)
synth.press(note)  # start note sounding
pos = 0  # last knob position
while True:
    if key := keys.events.get():  # button pushed
        if key.pressed:
            wti = (wti+1) % len(wavetables)  # go to next index
            wavetable1 = Wavetable(wave_dir+wavetables[wti])  # load new wavet
            note.waveform = wavetable1.waveform   # attach to note
    new_pos = (knobA.value / 65535) * wavetable1.num_waves
    pos = int((new_pos*0.5) + pos*0.5)  # filter knob input
    wavetable1.set_wave_pos(pos)   # pick new wavetable
    print("%s: wave num:%d" % (wavetables[wti], pos))
    time.sleep(0.01)
```
> [4_oscillators_waveforms/code_wavetable.py](./4_oscillators_waveforms/code_wavetable.py)

```
[ ... TBD video of code_wavetable.py TBD ... ]
```

## Wavetable scanning

As you use the knob to scan the wavetable above, you may notice how jarring it
is two switch between two waves that aren't very related.  The `Wavetable` class
can be expanded so that it mixes between adjacent waves in the wavetable,
much like the `code_wavemix.py` example above. This makes for a much smoother
scanning along the wavetable.

First let's move the Wavetable class to its own file and add in the wave mixing:

```py
# 4_oscillators_waveforms/wavetable.py
import ulab.numpy as np
import synthio
import adafruit_wave
class Wavetable:
    """ A 'waveform' for synthio.Note that uses a wavetable w/ a scannable wave position."""
    def __init__(self, filepath, wave_len=256):
        self.w = adafruit_wave.open(filepath)
        self.wave_len = wave_len  # how many samples in each wave
        if self.w.getsampwidth() != 2 or self.w.getnchannels() != 1:
            raise ValueError("unsupported WAV format")
        self.waveform = np.zeros(wave_len, dtype=np.int16)  # empty buffer we'll copy into
        self.num_waves = self.w.getnframes() // self.wave_len
        self._wave_pos = 0

    @property
    def wave_pos(self): return self._wave_pos

    @wave_pos.setter
    def wave_pos(self, pos):
        """Pick where in wavetable to be, morphing between waves"""
        pos = min(max(pos, 0), self.num_waves-1)  # constrain
        samp_pos = int(pos) * self.wave_len  # get sample position
        self.w.setpos(samp_pos)
        waveA = np.frombuffer(self.w.readframes(self.wave_len), dtype=np.int16)
        self.w.setpos(samp_pos + self.wave_len)  # one wave up
        waveB = np.frombuffer(self.w.readframes(self.wave_len), dtype=np.int16)
        pos_frac = pos - int(pos)  # fractional position between wave A & B
        self.waveform[:] = Wavetable.lerp(waveA, waveB, pos_frac) # mix waveforms A & B
        self._wave_pos = pos

    # mix between values a and b, works with numpy arrays too, t ranges 0-1
    def lerp(a, b, t):  return (1-t)*a + t*b
```

Save that file to the CIRCUITPY drive and we can use that in an updated wavetable
scanning example.  In the example below, let's also use a `synthio.LFO` to do
the waveetable scanning for us. The knobA controls the scan rate and knobB
controls the pitch as before, but check out how smooth the fades between waves
are! It can sound really great. Moving through certain wavetables can sound like
a complex modular synth patch when all we're doing is moving around the wavetable.
This is the feature that really sold me on `synthio`.

```py
# 4_oscillators_waveforms/code_wavetable_scan.py
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB
from wavetable import Wavetable

wavetable_fname = "wavetables/PLAITS02.WAV"  # from http://waveeditonline.com/

wavetable1 = Wavetable(wavetable_fname)

midi_note = 48
note = synthio.Note(synthio.midi_to_hz(midi_note), waveform=wavetable1.waveform)
synth.press(note)

# create a positive ramp-up-down LFO to scan through the waveetable
wave_lfo = synthio.LFO(rate=0.05, waveform=np.array((0,32767), dtype=np.int16))
wave_lfo.scale = wavetable1.num_waves
synth.blocks.append(wave_lfo)  # this activates LFO when not attached to Note

while True:
    # regularly copy LFO to wave_pos by hand
    wavetable1.wave_pos =  wave_lfo.value
    wave_lfo.rate =  (knobA.value/65535) * 0.25
    print("wave_pos:%.2f" % wavetable1.wave_pos)
    time.sleep(0.01)
```

```
[ ... TBD video of code_wavetable_scan.py TBD ... ]
```


## Use a WAV as an oscillator

Since `synthio` oscillator waveforms live in RAM and WAV files are normally
big compared to available RAM.  You can see what the largest sample you can load
by looking at `synthio.waveform_max_length`.
On RP2040, `synthio.waveform_max_length=16384`. This means you will need to
curate and downsample a WAV to fit as a `synthio` waveform.

In the "4_oscillators_waveforms" directory, there is a shortened and down-sampled
version of the famous "Amen break" drumloop, called `amen1_8k_s16.wav`. Copy
that file to the CIRCUITPY drive for the example below.  It's been down-sampled
to 8kHz sample rate and lasts for 1.75 seconds. This gives 14001 samples, just
small enough to fit.

Beacuse `synthio` thinks of its oscillator waveforms as single-cycle waves,
when using it with a standard WAV file, the `Note.frequency` needed
to get the WAV to play back normally is based on the WAV size
and the original sample rate and the number of samples in the WAV. The example
shows how to calculate the WAV file duration and use that to set `.frequency`.

But for the samples we can load, it means we have fine-grained control over their
speed and pitch!  Check out the example where knobA controls the pitch of the
drum loop.

```py
# 4_oscillators_wavetables/code_wavewav.py
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA
import adafruit_wave

# reads in entire wave into RAM
# return tuple of (memoryview on the WAV, sample_rate, num_samples)
def read_waveform(filename):
    with adafruit_wave.open(filename) as w:
        if w.getsampwidth() != 2 or w.getnchannels() != 1:
            raise ValueError("unsupported format")
        return (memoryview(w.readframes(w.getnframes())).cast('h'),
                w.getframerate(), w.getnframes())

wave_wav, sample_rate, num_samples = read_waveform("/amen1_8k_s16.wav")
duration = num_samples / sample_rate
print("sample_rate:%d num_samples:%d duration:%.2f" % (sample_rate, num_samples, duration))

note = synthio.Note(frequency=1/duration, waveform=wave_wav)
synth.press(note)

while True:
    note.frequency = (1/duration) * (0.25 + (knobA.value / 65535) * 1.5)
    print("note freq:%6.3f duration:%5.2f" % (note.frequency, 1/note.frequency))
    time.sleep(0.2)
```

```
[ ... TBD video of code_wavewav.py TBD ... ]
```


## Fatter sounds with detuned oscillators

Typical synthesizer architectures have two or three oscillators
(with potentially different waveforms) that sound together and then fed
through the amplifier (controlled by the amplitude envelope) and filter (controlled
by the filter envelope).  While `synthio` only has a single oscillator in its
voice architecture, we can double- or triple-up those voices, triggering them
at the same time, to approximate this type of typical synth.  Yes, the filters get doubled,
but the modulators (amp & filter envs) can be shared and it does open the possibily
of having different filters on each oscillator.
(And it does mean we could use different filters for each oscillator, something most
synths *cannot* do!)

One technique to quickly make a synth patch sound better is to detune its oscillators.
We have fine-grained control over a `synthio.Note`'s frequency with `note.frequency`,
so we can do use that to "detune" oscilators to get a "fatter" sound.  We could
even attach a very subtle LFO to `note.bend` to emulate the small tuning fluctuations
of an analog synth.

Also good to note that `synthio.midi_to_hz()` allows a floating-point
value for the MIDI note number.  This allows you to detune more musically
than doing it on frequency.

The example below sets up "knobA" to control the number of oscillators sounding
(from 1 to 6) and "knobB" controls how much detune between each oscillator.

```py
# 4_oscillators_wavetables/code_detune.py
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB

midi_note = 45
while True:
    num_oscs = int(knobA.value/65535 * 6 + 1)  # up to 6 oscillators
    detune = (knobB.value/65535) * 0.01  # up to 10% detune
    print(f"num_oscs: {num_oscs} detune: {detune}")
    notes = []  # holds note objs being pressed
    # simple detune, always detunes up
    for i in range(num_oscs):
        f = synthio.midi_to_hz(midi_note) * (1 + i*detune)  # detune!
        notes.append( synthio.Note(f) )
    synth.press(notes)
    time.sleep(0.5)
    synth.release(notes)
    time.sleep(0.1)
```

```
[ ... TBD video of code_detune.py TBD ... ]
```


## Fun with wavetables: wavetabledrone

Now we have some ability to load and play wavetables, let's use them to make
a slowly evolving dronesynth with some oscillators scanning at different rates
through a harmonically-rich wavetable.

```py
# 4_oscillators_wavetables/code_wavetabledrone.py
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB
from wavetable import Wavetable

wavetable_fname = "wavetable/PLAITS02.WAV"  # from http://waveeditonline.com/

wavetable1 = Wavetable(wavetable_fname)
wavetable2 = Wavetable(wavetable_fname)
wavetable3 = Wavetable(wavetable_fname)

midi_note = 48
note = synthio.Note(synthio.midi_to_hz(midi_note-12), waveform=wavetable1.waveform)
note2 = synthio.Note(synthio.midi_to_hz(midi_note-7), waveform=wavetable2.waveform)
note3 = synthio.Note(synthio.midi_to_hz(midi_note), waveform=wavetable3.waveform)
note3.bend = synthio.LFO(rate=0.01, scale=0.5)
note4 = synthio.Note(synthio.midi_to_hz(midi_note-24), waveform=wavetable3.waveform)

wave_lfo = synthio.LFO(rate=0.005, waveform=np.array((0,32767), dtype=np.int16) )
wave_lfo.scale = wavetable1.num_waves
wave_lfo2 = synthio.LFO(rate=0.01, waveform=np.array((32767,0), dtype=np.int16) )
wave_lfo2.scale = wavetable1.num_waves
wave_lfo2.phase_offset = 0.25
synth.blocks.append(wave_lfo)
synth.blocks.append(wave_lfo2)

synth.press( (note,note2,note3,note4) )

while True:
    wavetable1.wave_pos =  wave_lfo.value
    wavetable2.wave_pos =  wave_lfo2.value
    wavetable3.wave_pos = 0 + 16.0 * (knobA.value/65535)
    print("%.2f %.2f %.2f" % (wave_lfo.value, wave_lfo2.value, wavetable3.wave_pos))
    time.sleep(0.05)
```

```
[ ... TBD video of code_wavetabledrone.py TBD ... ]
```




## Research links

- [waveeditonline.com](https://waveeditonline.com/) ([archived homepage](https://web.archive.org/web/20221128075225/https://waveeditonline.com/))
- [deeper look at single-cycle waveforms](https://blog.synthesizerwriter.com/2020/10/a-deeper-look-at-single-cycle-waveforms.html)
- [free wavetables](https://forum.vital.audio/t/free-wavetables-128-wavetables-serum-format-plus-single-cycle-waveforms-from-a-huge-forthcoming-collection/13344)

## Next Steps

We now have enough control over `synthio` to make just about any sound.
So let's figure out how to control the sounds with [MIDI](README-5-MIDI.md).
