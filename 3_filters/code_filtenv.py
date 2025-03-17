# 3_filters/code_filtenv.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time, random, synthio
import ulab.numpy as np
from synth_setup import synth, knobA, knobB

synth.envelope = synthio.Envelope(attack_time=0.0, release_time=0.5)

wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)

filter_attack_lfo = synthio.LFO(once=True, rate=1.0, offset=500, scale=2000,
                                waveform=np.array((0,32767), dtype=np.int16))
filter_release_lfo = synthio.LFO(once=True, rate=1.5, offset=500, scale=2000,
                                 waveform=np.array((32767,0), dtype=np.int16))

midi_note = 60
midi_notes = (60, 60+3, 60+5, 60-12, 60+12)
while True:
    midi_note = random.choice(midi_notes)
    # press a note with attack filter
    note = synthio.Note(midi_note, waveform=wave_saw)
    note.filter = synthio.BlockBiquad(synthio.FilterMode.LOW_PASS, 
                                      frequency=filter_attack_lfo, Q=1.8)
    filter_attack_lfo.retrigger()
    synth.press(note)  # trigger amp env and filter lfo
            
    # wait for attack phase to complete, hold a bit, then
    # release the note
    for i in range(30):
        print("up filter freq: %.1f" % note.filter.frequency.value)
        time.sleep(0.01)
    #time.sleep(1.0)
    
    note.filter.frequency = filter_release_lfo
    filter_release_lfo.retrigger()
    synth.release(note)  # trigger amp env release
    
    #time.sleep(1.0)  # let the release happen
    for i in range(30):
        print("down filter freq: %.1f" % note.filter.frequency.value)
        time.sleep(0.01)

