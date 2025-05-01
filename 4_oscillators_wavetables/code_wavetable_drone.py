# 4_oscillators_waveforms/code_wavetabledrone.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
# NOTE: on RP2040, this needs SAMPLE_RATE=22050 in synth_setup.py
#
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB
from wavetable import Wavetable

wavetable_fname = "wavetables/PLAITS02.WAV"  # from http://waveeditonline.com/

wavetable1 = Wavetable(wavetable_fname)
wavetable2 = Wavetable(wavetable_fname)
wavetable3 = Wavetable(wavetable_fname)

midi_note = 48
note = synthio.Note(synthio.midi_to_hz(midi_note-12),
                    waveform=wavetable1.waveform)
note2 = synthio.Note(synthio.midi_to_hz(midi_note-7),
                     waveform=wavetable2.waveform)
note3 = synthio.Note(synthio.midi_to_hz(midi_note),
                     waveform=wavetable3.waveform)
note3.bend = synthio.LFO(rate=0.005, scale=0.25, phase_offset=0.5)

wave_lfo = synthio.LFO(rate=0.005, waveform=np.array((0,32767), dtype=np.int16) )
wave_lfo.scale = wavetable1.num_waves
wave_lfo2 = synthio.LFO(rate=0.01, waveform=np.array((32767,0), dtype=np.int16) )
wave_lfo2.scale = wavetable1.num_waves
wave_lfo2.phase_offset = 0.25
synth.blocks.append(wave_lfo)  # add LFOs to blocks so they get run
synth.blocks.append(wave_lfo2)

synth.press( (note,note2,note3) )

while True:
    wavetable1.wave_pos =  wave_lfo.value  # copy LFO pos to wave pos
    wavetable2.wave_pos =  wave_lfo2.value
    wavetable3.wave_pos = 24 + 16.0 * (knobA.value/65535)
    print("%.2f %.2f %.2f" % (wave_lfo.value, wave_lfo2.value, wavetable3.wave_pos))
    time.sleep(0.05)
    
