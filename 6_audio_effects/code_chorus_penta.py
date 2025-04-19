# 6_effects/code_chorus_penta.py
# part of todbot circuitpython synthio tutorial
# 14 Apr 2025 - @todbot / Tod Kurt
import time, random
import ulab.numpy as np
import synthio
import audiodelays, audiofilters
from synth_setup import mixer, synth, SAMPLE_RATE, CHANNEL_COUNT, knobA, knobB

time.sleep(1)

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
    midi_note = 48 + random.choice(scale_pentatonic)
    notes = [synthio.Note(synthio.midi_to_hz(midi_note), waveform=wave_saw, filter=lpf),]
    if knobB.value > 32000:
        notes.append(synthio.Note(synthio.midi_to_hz(midi_note+7), waveform=wave_saw, filter=lpf))
    vA = knobA.value/65535
    #chorus1.delay_ms.offset = (knobB.value/65535)*25 + 0.001
    chorus1.mix = knobA.value/65535
    print("playing %d mix: %.2f %d" % (midi_note,vA, len(notes)))
    synth.press(notes)
    time.sleep(0.1)
    synth.release(notes)
    time.sleep(0.25 if i%2 else 0.12 )  # give it a little groove
    i=i+1
