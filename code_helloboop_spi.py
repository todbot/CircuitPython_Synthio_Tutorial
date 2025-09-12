# code_helloboop_spi.py -- synthio hello world with SPI DAC
# part of todbot circuitpython synthio tutorial
# 12 Sep 2024 - @todbot / Tod Kurt
#
# This is the hello world example modified to use SPI DAC instead of I2S
#
# Hardware needed:
# - Raspberry Pi Pico (or compatible)
# - SPI DAC chip like MCP4922, MCP4912, or TLV5618
# - Wiring per synth_setup_spi.py
#
import time
import random
from synth_setup_spi import synth, update_audio

# simple pentatonic scale  C, D, E, G, A
notes = (60, 62, 64, 67, 69)

print("hello boop! (SPI DAC version)")

while True:
    # pick a random note from the scale
    note_num = random.choice(notes)
    
    # play it
    synth.press(note_num)
    
    # wait a bit, then release it
    time.sleep(0.25)
    synth.release(note_num)
    
    # wait a bit more before next note
    time.sleep(0.25)
    
    # IMPORTANT: Update the SPI DAC audio processing
    update_audio()