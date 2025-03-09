# 1_getting_started/code_helloboop.py -- Getting synthio up and running
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
import time
import random
import board
import synthio
import audiobusio

# how we have our circuit wired up or pico_test_synth
i2s_bck_pin = board.GP20
i2s_lck_pin = board.GP21
i2s_dat_pin = board.GP22

# hook up external stereo I2S audio DAC board
audio = audiobusio.I2SOut(bit_clock=i2s_bck_pin, word_select=i2s_lck_pin, data=i2s_dat_pin)
# make the synthesizer
synth = synthio.Synthesizer(sample_rate=44100, channel_count=2)
# plug synthesizer into audio output
audio.play(synth)

midi_note = 60  # midi note to play, 60 = C4

while True:
    print("boop!")
    synth.press(midi_note) # start note playing
    time.sleep(0.1)
    synth.release(midi_note) # release the note we pressed
    time.sleep(0.4)
    midi_note = random.randint(32,72)   # pick a new random note

