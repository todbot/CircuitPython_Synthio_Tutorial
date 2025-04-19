# 6_effects/code_chorus.py
# part of todbot circuitpython synthio tutorial
# 14 Apr 2025 - @todbot / Tod Kurt
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
