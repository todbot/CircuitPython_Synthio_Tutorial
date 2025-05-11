# [Synthio Tutorial](.#sections): 6. Audio Effects

<!--ts-->
   * [Which chips/boards can run audio effects?](#which-chipsboards-can-run-audio-effects)
   * [Quick Demo](#quick-demo)
   * [How effects work in synthio](#how-effects-work-in-synthio)
   * [How to chain effects](#how-to-chain-effects)
   * [Add a delay effect with Echo](#add-a-delay-effect-with-echo)
   * [Make a flange effect with echo](#make-a-flange-effect-with-echo)
   * [Make a chorus effect](#make-a-chorus-effect)
   * [Playing with chorus](#playing-with-chorus)
   * [audiodelays PitchShift](#audiodelays-pitchshift)
   * [audiofilters Distortion](#audiofilters-distortion)
   * [audiofilters Filter](#audiofilters-filter)
<!--te-->

In CircuitPython 10+, there are multiple core libraries for audio effects:

- [`audiodelays`](https://docs.circuitpython.org/en/latest/shared-bindings/audiodelays)
  -- effects that work on small copies of an input signal
  - `Echo`
  - `MultiTapDelay`
  - `Chorus`
  - `PitchShift`
- [`audiofilters`](https://docs.circuitpython.org/en/latest/shared-bindings/audiofilters/)
  -- effects that alter the frequency composition of an input signal
  - `Filter`
  - `Distortion`
- [`audiofreeverb`](https://docs.circuitpython.org/en/latest/shared-bindings/audiofreeverb)
  -- Reverb effect

Note that these apply to the entire audio output of a `synthio.Synthesizer`,
not on a per-note basis.  In fact, these effects are not specific to `synthio`
at all and can be used on other sources of audio like playing WAV files or MP3 files.
This is really cool as we can apply these effects to sample-based instruments
like drum machines or to incoming audio from a microphone.

## Which chips/boards can run audio effects?

Currently the best chipset to use for audio effects is RP2350.
So the demos below will use a Raspberry Pi Pico 2.

Also note that you must be running CircuitPython version 10+.
As of Apr 2025, you need to be running "Absolute Newest" CircuitPython to get
all these effects.

## Quick Demo

Since we can use any audio source, let's use the partial Amen Break from before
(but a stereo 44.1k version) and run it through some various effects to see how
the different effects sound.

```py
# 6_audio_effects/code_demo.py -- show off some audio effects
import time, audiofilters, audiodelays, audiocore, synthio
from synth_setup import mixer, BUFFER_SIZE, CHANNEL_COUNT, SAMPLE_RATE
cfg = { 'buffer_size': BUFFER_SIZE,
        'channel_count': CHANNEL_COUNT,
        'sample_rate': SAMPLE_RATE }
effects = (
     audiofilters.Filter(**cfg, mix=1.0,  # mostly no filtering, pass-through
                         filter = synthio.Biquad(synthio.FilterMode.LOW_PASS,
                                                 frequency=20000, Q=0.8)),
     audiofilters.Filter(**cfg, mix=1.0,
                         filter = synthio.Biquad(synthio.FilterMode.LOW_PASS,
                                                 frequency=200, Q=1.2)),
     audiodelays.Chorus(**cfg, mix = 0.6,
                        max_delay_ms = 150, voices = 3,
                        delay_ms = synthio.LFO(rate=0.6, offset=10, scale=5)),
     audiodelays.Echo(**cfg, mix = 0.6,
                      max_delay_ms = 330, delay_ms = 330, decay = 0.6),
     audiofilters.Distortion(**cfg, mix = 1.0,
                             mode = audiofilters.DistortionMode.OVERDRIVE,
                             soft_clip = True, pre_gain = 40, post_gain = -20),
     audiodelays.PitchShift(**cfg, mix=1.0,
                            semitones = synthio.LFO(rate=2/3.5, scale=6)),
    )

mixer.voice[0].level = 1.0
mywav = audiocore.WaveFile("amen3_44k_s16.wav")
i = 0
while True:
    effect = effects[i]  # pick a new effect
    print(i, effect)
    mixer.voice[0].play(effect)    # plug effect into mixer
    effect.play(mywav, loop=True)  # plug wavfile into effect
    time.sleep(3.5)   # loop is 3.5/2 seconds long
    i = (i+1) % len(effects)
```
> [6_audio_effects/code_demo.py](./6_audio_effects/code_demo.py) and [synth_setup.py](./6_audio_effects/synth_setup.py)

> [watch demo video](https://www.youtube.com/watch?v=nyv7XlQ1d00)

{% include youtube.html id="nyv7XlQ1d00" alt="code_demo demo" %}


## How effects work in CircuitPython

From our experience with `audiomixer.Mixer`, we've seen how the flow of audio
is like a guitar pedal effects chain:
plug the mixer into the audio output, plug the synth into the mixer.

The CircuitPython audio effects work the exact same way.
Every effect has an input and an output, just like a guitar pedal.
To use an effect, insert it into the chain where you want the effect to occur.
In the above example, we keep re-plug a new effect in between the mixer and the WaveFile.
And this means you can plug the output of one effect into another effect.

Every effect has a "mix" control that lets you select how much of the effect
you want want to apply: `effect.mix=0.0` is just the "dry" uneffected signal
and `effect.mix=1.0` is the full "wet" effected signal.  Note that this mix
control is what some call "post-fader". That is, the full signal is still being fed
into the effect and the mix control is selecting how much of the effect.

(The alternative is "pre-fader", where the mix control selects how much of the
signal is sent to the effect. In most cases it doesn't matter much. The biggest
place you may notice it is when using delay/echo effects and trying to adjust
mix in a rhythmic way)


## How to chain effects



## Add a delay effect with Echo

```py
# 6_effects/code_echo.py
import time, random
import synthio
import audiodelays
from synth_setup import mixer, synth, SAMPLE_RATE, CHANNEL_COUNT, knobA

echo1 = audiodelays.Echo(
    mix = 0.5,
    max_delay_ms = 300,
    delay_ms = 300,
    decay = 0.8,
    sample_rate = SAMPLE_RATE,    # note we need these, just like for audiomixer
    channel_count = CHANNEL_COUNT,
)

mixer.voice[0].play(echo1)  # plug echo into the mixer (unplugs synth)
echo1.play(synth)           # and plug synth into echo

while True:
    midi_note = random.randint(36,64)
    echo1.mix = knobA.value/65535  # knobA controls echo mix
    print("playing %d mix: %.2f" % (midi_note,echo1.mix))
    synth.press(midi_note)
    time.sleep(0.1)
    synth.release(midi_note)
    time.sleep(1)
```
> [6_audio_effects/code_echo.py](./6_audio_effects/code_echo.py) and [synth_setup.py](./6_audio_effects/synth_setup.py)


## Make a flange effect with echo

```py
# 6_effects/code_flange.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
import time
import ulab.numpy as np
import synthio
import audiodelays
from synth_setup import mixer, synth, SAMPLE_RATE, CHANNEL_COUNT, knobA

# be sure to create and attach LFO *before* creating Echo
echo_lfo = synthio.LFO(rate=0.01, scale=15, offset=30)
echo1 = audiodelays.Echo(
    max_delay_ms = 1000,
    delay_ms = echo_lfo,
    decay = 0.75,
    sample_rate = SAMPLE_RATE,
    channel_count = CHANNEL_COUNT,
)
mixer.voice[0].play(echo1)  # plug effect into the mixer (unplugs synth)
echo1.play(synth)           # and plug synth into effect

while True:
  print("ping")
  synth.press(48)
  time.sleep(1)
  synth.release(48)
  time.sleep(2.0)
```
> [6_audio_effects/code_flange.py](./6_audio_effects/code_flange.py) and [synth_setup.py](./6_audio_effects/synth_setup.py)


## Make a chorus effect

```py
# 6_effects/code_chorus.py
import time, random
import synthio
import audiodelays, audiofilters
from synth_setup import mixer, synth, SAMPLE_RATE, CHANNEL_COUNT, knobA

chorus1 = audiodelays.Chorus(
    channel_count=CHANNEL_COUNT,
    sample_rate=SAMPLE_RATE,
    mix = 0.5,
    voices = 3,
    max_delay_ms = 50,
    delay_ms = synthio.LFO(rate=0.5, offset=15, scale=5),
)

mixer.voice[0].play(chorus1)  # plug effect into the mixer (unplugs synth)
chorus1.play(synth)           # and plug synth into effect

while True:
    midi_note = random.randint(36,64)
    v = knobA.value/65535
    chorus1.mix = v
    print("playing %d mix: %.2f" % (midi_note,v))
    synth.press(midi_note)
    time.sleep(0.5)
    synth.release(midi_note)
    time.sleep(1)
```
> [6_audio_effects/code_chorus.py](./6_audio_effects/code_chorus.py) and [synth_setup.py](./6_audio_effects/synth_setup.py)


## Playing with chorus

```py
# 6_effects/code_chorus_penta.py
import time, random
import ulab.numpy as np
import synthio
import audiodelays, audiofilters
from synth_setup import mixer, synth, SAMPLE_RATE, CHANNEL_COUNT, knobA, knobB

chorus1 = audiodelays.Chorus(
    channel_count=CHANNEL_COUNT,
    sample_rate=SAMPLE_RATE,
    mix = 0.5,
    voices = 3,
    max_delay_ms = 50,
    delay_ms = synthio.LFO(rate=0.5, offset=15, scale=5),
)
mixer.voice[0].play(chorus1)  # plug effect into the mixer (unplugs synth)
chorus1.play(synth)           # and plug synth into effect

# make a quicky saw wave for chorus demo
wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)
# and a filter to tame the high end
lpf = synthio.Biquad(synthio.FilterMode.LOW_PASS, frequency=3000, Q=1.25)

scale_pentatonic = [0, 2, 4, 7, 9, 12, 14, 16, 19, 21]  # two octaves of offsets

i=0
while True:
    midi_note = 48 + random.choice(scale_pentatonic)  # 48 = base note
    notes = [synthio.Note(synthio.midi_to_hz(midi_note), waveform=wave_saw, filter=lpf),]
    # if knobB past midpoint, add a second note a fifth above (seven semitones)
    if knobB.value > 32000:
        notes.append(synthio.Note(synthio.midi_to_hz(midi_note+7), waveform=wave_saw, filter=lpf))
    vA = knobA.value/65535
    chorus1.mix = knobA.value/65535
    print("playing %d mix: %.2f notes:%d" % (midi_note,vA,len(notes)))
    synth.press(notes)
    time.sleep(0.1)
    synth.release(notes)
    time.sleep(0.25 if i%2 else 0.12 )  # give it a little groove
    i=i+1
```
> [6_audio_effects/code_chorus_penta.py](./6_audio_effects/code_chorus_penta.py) and [synth_setup.py](./6_audio_effects/synth_setup.py)


## audiodelays PitchShift

## audiofilters Distortion

## audiofilters Filter

```py
# 6_effects/code_stackedfilters_lfo.py
import time, random
import synthio
import audiodelays, audiofilters
from synth_setup import mixer, synth, SAMPLE_RATE, CHANNEL_COUNT, knobA

filter1 = audiofilters.Filter(buffer_size=1024,
                              channel_count=CHANNEL_COUNT,
                              sample_rate=SAMPLE_RATE,
                              mix=1.0)
filter2 = audiofilters.Filter(buffer_size=1024,
                              channel_count=CHANNEL_COUNT,
                              sample_rate=SAMPLE_RATE,
                              mix=1.0)
filter1.filter = synthio.Biquad(synthio.FilterMode.LOW_PASS, frequency=2000, Q=2.25)
filter2.filter = synthio.Biquad(synthio.FilterMode.LOW_PASS, frequency=2000, Q=2.25)
filter1.filter.frequency = synthio.LFO(rate=2, offset=1000, scale=800)
filter2.filter.frequency = synthio.LFO(rate=2, offset=1000, scale=800)

mixer.voice[1].play(filter1)  # plug filter1 into the mixer (unplugs synth)
filter1.play(filter2)         # plug filter2 into filter1
filter2.play(synth)           # and plug synth into filter2

while True:
  synth.press(48)
  time.sleep(1)
  synth.release(48)
  time.sleep(2.0)

```
> [6_audio_effects/code_stackedfilters_lfo.py](./6_audio_effects/code_stackedfilters_lfo.py) and [synth_setup.py](./6_audio_effects/synth_setup.py)


## Fun with effects: Freeze Effect
