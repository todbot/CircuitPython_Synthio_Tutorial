# [Synthio Tutorial](.#sections): 7. Audio Effects

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


## Which chips/boards can run audio effects?

## Quick Demo

## How effects work in synthio

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

## Make a chorus effect

```py
# 6_effects/code_chorus.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
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

## Playing with chorus

```py
# 6_effects/code_chorus.py
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

## audiodelays PitchShift

## audiofilters Distortion

## audiofilters Filter

```py
# 6_effects/code_stackedfilters_lfo.py
# part of todbot circuitpython synthio tutorial
# 14 Apr 2025 - @todbot / Tod Kurt
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
