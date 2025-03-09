# synth_setup.py -- Getting synthio up and running
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
# 
import time
import random
import board
import synthio
import audiobusio
import audiomixer

SAMPLE_RATE = 44100

# what we have plugged into the breadboard or pico_test_synth
sw_pins = (board.GP28,)
knob_pin = board.GP26
i2s_bck_pin = board.GP20
i2s_lck_pin = board.GP21
i2s_dat_pin = board.GP22

# hook up external stereo I2S audio DAC board
audio = audiobusio.I2SOut(bit_clock=i2s_bck_pin, word_select=i2s_lck_pin, data=i2s_dat_pin)

# add a mixer to give us a buffer
mixer = audiomixer.Mixer(sample_rate=SAMPLE_RATE, channel_count=2, buffer_size=2048)

# make the actual synthesizer
synth = synthio.Synthesizer(sample_rate=SAMPLE_RATE, channel_count=2)

# plug the mixer into the audio output
audio.play(mixer)

# plug the synth into the first 'voice' of the mixer
mixer.voice[0].play(synth)
mixer.voice[0].level = 0.25  # 0.25 usually better for headphones

# more on this later, but makes it sound nicer
synth.envelope = synthio.Envelope(attack_time=0.0, release_time=0.6)
