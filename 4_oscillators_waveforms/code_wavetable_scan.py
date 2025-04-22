# 4_oscillators_waveforms/code_wavetable_scan.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB
from wavetable import Wavetable

wavetable_fname = "wavetables/PLAITS02.WAV"  # from http://waveeditonline.com/

wavetable1 = Wavetable(wavetable_fname)

midi_note = 48
note = synthio.Note(synthio.midi_to_hz(midi_note), waveform=wavetable1.waveform)
synth.press(note)

# create a positive ramp-up-down LFO to scan through the waveetable
wave_lfo = synthio.LFO(rate=0.05, waveform=np.array((0,32767), dtype=np.int16))
wave_lfo.scale = wavetable1.num_waves
synth.blocks.append(wave_lfo)  # this activates LFO when not attached to Note

while True:
    # regularly copy LFO to wave_pos by hand
    wavetable1.wave_pos =  wave_lfo.value
    wave_lfo.rate =  (knobA.value/65535) * 0.25
    print("wave_pos:%.2f" % wavetable1.wave_pos)
    time.sleep(0.01)

