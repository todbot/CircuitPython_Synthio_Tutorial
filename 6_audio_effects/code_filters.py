# 6_effects/code_filters.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
import time, random
import synthio
import audiodelays, audiofilters
from synth_setup import mixer, synth, SAMPLE_RATE, CHANNEL_COUNT, knobA

time.sleep(1)

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
  print("ping")
  synth.press(48)
  time.sleep(1)
  synth.release(48)
  time.sleep(2.0)
