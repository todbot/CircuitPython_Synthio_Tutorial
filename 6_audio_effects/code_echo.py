# 6_effects/code_echo.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
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
    midi_note = random.randint(36,64)  # knobA controls echo mix
    echo1.mix = knobA.value/65535
    print("playing %d mix: %.2f" % (midi_note,echo1.mix))
    synth.press(midi_note)
    time.sleep(0.1)
    synth.release(midi_note)
    time.sleep(1)



