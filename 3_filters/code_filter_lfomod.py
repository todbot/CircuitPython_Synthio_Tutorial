# 3_filters/code_filter_lfomod.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time, random, synthio
import ulab.numpy as np
from synth_setup import synth, knobA, knobB

# extend the amplitude envelope release so we can hear the filter release
synth.envelope = synthio.Envelope(attack_time=0.0, release_time=1.5)

# use a saw wave sound oscillator instead of square wave to hear the filter better
wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)

filt_attack_time = 1.0
filt_release_time = 1.5
filt_min_freq = 500
filt_max_freq = 2000

# LFO to use as the ramp up in frequency on key press
filter_attack_lfo = synthio.LFO(once=True, rate=filt_attack_time,
                                offset=min_freq, scale=max_freq,
                                waveform=np.array((0,32767), dtype=np.int16))
# LFO to use to ramp down the frequency on key release
filter_release_lfo = synthio.LFO(once=True, rate=filt_release_time,
                                 offset=min_freq, scale=max_freq,
                                 waveform=np.array((32767,0), dtype=np.int16))

while True:
    midi_note = random.randint(48,72)  # pick a new note to play
    # press a note with attack filter
    note = synthio.Note(midi_note, waveform=wave_saw)
    note.filter = synthio.BlockBiquad(synthio.FilterMode.LOW_PASS,
                                      frequency=filter_attack_lfo, Q=1.8)
    filter_attack_lfo.retrigger()
    synth.press(note)  # trigger amp env and filter lfo

    # wait for attack phase to complete, hold a bit, then
    #for i in range(50):
    #    print("up filter freq: %.1f" % note.filter.frequency.value)
    #    time.sleep(0.02)
    time.sleep(1.0)

    # release the note
    note.filter.frequency = filter_release_lfo
    filter_release_lfo.retrigger()
    synth.release(note)  # trigger amp env release

    # let the release happen
    # for i in range(50):
    #     print("down filter freq: %.1f" % note.filter.frequency.value)
    #     time.sleep(0.02)
    time.sleep(1.0)

