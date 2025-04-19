# 6_effects/code_flange.py
# part of todbot circuitpython synthio tutorial
# 14 Apr 2025 - @todbot / Tod Kurt
import time
import ulab.numpy as np
import synthio
import audiodelays, audiofilters
from synth_setup import mixer, synth, SAMPLE_RATE, CHANNEL_COUNT, knobA

time.sleep(1)

# be sure to create and attach LFO *before* creating Echo
echo_lfo = synthio.LFO(rate=0.01, scale=15, offset=30)  
echo1 = audiodelays.Echo(
    max_delay_ms = 1000,
    delay_ms = echo_lfo,
    decay = 0.75,
    sample_rate = SAMPLE_RATE,
    channel_count = CHANNEL_COUNT,
    freq_shift = True,
    buffer_size = 1024,
)

mixer.voice[0].play(echo1)  # plug effect into the mixer (unplugs synth)
echo1.play(synth)           # and plug synth into effect

while True:
  print("ping")
  synth.press(48)
  time.sleep(1)
  synth.release(48)
  time.sleep(2.0)
