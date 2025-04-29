# synth_setup.py -- Getting synthio up and running
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import board
import synthio
import audiobusio
import audiomixer
import keypad
import analogio

SAMPLE_RATE = 44100
CHANNEL_COUNT = 2
BUFFER_SIZE = 2048

# what we have plugged into the breadboard or pico_test_synth
button_pins = (board.GP28,)
knobA_pin = board.GP26
knobB_pin = board.GP27
i2s_bck_pin = board.GP20
i2s_lck_pin = board.GP21
i2s_dat_pin = board.GP22

# hook up external stereo I2S audio DAC board
audio = audiobusio.I2SOut(bit_clock=i2s_bck_pin, word_select=i2s_lck_pin, data=i2s_dat_pin)

# add a mixer to give us a buffer
mixer = audiomixer.Mixer(sample_rate=SAMPLE_RATE, channel_count=CHANNEL_COUNT, buffer_size=BUFFER_SIZE)

# make the actual synthesizer
synth = synthio.Synthesizer(sample_rate=SAMPLE_RATE, channel_count=CHANNEL_COUNT)

# plug the mixer into the audio output
audio.play(mixer)

# plug the synth into the first 'voice' of the mixer
mixer.voice[0].play(synth)
mixer.voice[0].level = 0.25  # 0.25 usually better for headphones, 1.0 for speakers

# more on this later, but makes it sound nicer
synth.envelope = synthio.Envelope(attack_time=0.0, release_time=0.6)

# add key reading with debouncing
keys = keypad.Keys( button_pins, value_when_pressed=False, pull=True)

knobA = analogio.AnalogIn(knobA_pin)
knobB = analogio.AnalogIn(knobB_pin)
