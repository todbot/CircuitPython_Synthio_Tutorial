# synth_setup_spi.py -- Getting synthio up and running with SPI DAC
# part of todbot circuitpython synthio tutorial
# 12 Sep 2024 - @todbot / Tod Kurt
#
# This version uses an SPI DAC instead of I2S DAC for audio output
#
import board
import synthio
import audiomixer
import keypad
import analogio
import busio
from audiobusio_spi import SPIOut, DAC_MCP4922

SAMPLE_RATE = 22050  # Lower sample rate for better performance with SPI
CHANNEL_COUNT = 2
BUFFER_SIZE = 1024   # Smaller buffer for SPI

# what we have plugged into the breadboard
button_pins = (board.GP28,)
knobA_pin = board.GP26
knobB_pin = board.GP27

# SPI DAC pins (adjust for your wiring)
spi_sck_pin = board.GP18  # SPI clock
spi_mosi_pin = board.GP19  # SPI data out
spi_cs_pin = board.GP20    # Chip select
spi_ldac_pin = board.GP21  # LDAC pin (optional, for simultaneous channel updates)

# Initialize SPI bus
spi = busio.SPI(clock=spi_sck_pin, MOSI=spi_mosi_pin)

# hook up external stereo SPI DAC board (e.g., MCP4922)
audio = SPIOut(spi=spi, 
               cs=spi_cs_pin, 
               dac_type=DAC_MCP4922,
               sample_rate=SAMPLE_RATE,
               channel_count=CHANNEL_COUNT,
               ldac=spi_ldac_pin)

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

# Helper function to update audio in main loop
def update_audio():
    """Call this in your main loop to update SPI DAC audio output"""
    audio.update()

print("SPI DAC synth setup complete!")
print("Don't forget to call update_audio() in your main loop!")