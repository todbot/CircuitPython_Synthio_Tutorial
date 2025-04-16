# 3_filters/code_filter_handmod.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
import time
import synthio
from synth_setup import synth
midi_note = 48
filter_types = (synthio.FilterMode.LOW_PASS,
                synthio.FilterMode.HIGH_PASS,
                synthio.FilterMode.NOTCH,
                )
i=0     # which filter we're trying
note = synthio.Note(synthio.midi_to_hz(midi_note))
synth.press(note)

while True:
    print("selecting filter_type", filter_types[i])
    filter1 = synthio.Biquad(filter_types[i], frequency=3000, Q=1.2)
    note.filter = filter1
    
    while filter1.frequency > 250:
        print("changing filter frequency: %d" % filter1.frequency)
        filter1.frequency = filter1.frequency * 0.95  # do modulation by hand
        time.sleep(0.05)
    i = (i+1) % len(filter_types)  # go to next filter type
