# 6_audio_effects/code_demo.py -- show off some audio effects
# part of todbot circuitpython synthio tutorial
# 20 Apr 2025 - @todbot / Tod Kurt
#
import time, audiofilters, audiodelays, audiocore, synthio
from synth_setup import mixer, BUFFER_SIZE, CHANNEL_COUNT, SAMPLE_RATE
cfg = { 'buffer_size': BUFFER_SIZE,
        'channel_count': CHANNEL_COUNT,
        'sample_rate': SAMPLE_RATE }
effects = (
     audiofilters.Filter(**cfg, mix=1.0,  # mostly no filtering, pass-through
                         filter = synthio.Biquad(synthio.FilterMode.LOW_PASS,
                                                 frequency=20000, Q=0.8)),
     audiofilters.Filter(**cfg, mix=1.0,
                         filter = synthio.Biquad(synthio.FilterMode.LOW_PASS,
                                                 frequency=200, Q=1.2)),
     audiodelays.Chorus(**cfg, mix = 0.6,
                        max_delay_ms = 150, voices = 3,
                        delay_ms = synthio.LFO(rate=0.6, offset=10, scale=5)),
     audiodelays.Echo(**cfg, mix = 0.6,
                      max_delay_ms = 330, delay_ms = 330, decay = 0.6),
     audiofilters.Distortion(**cfg, mix = 1.0,
                             mode = audiofilters.DistortionMode.OVERDRIVE,
                             soft_clip = True, pre_gain = 40, post_gain = -20),
     audiodelays.PitchShift(**cfg, mix=1.0,
                            semitones = synthio.LFO(rate=2/3.5, scale=6)),     
    )

mixer.voice[0].level = 1.0
#mywav = audiocore.WaveFile("amen1_44k_s16.wav")
mywav = audiocore.WaveFile("amen3_44k_s16.wav")
i = 0
while True:
    effect = effects[i]  # pick a new effect
    print(i, effect)
    mixer.voice[0].play(effect)    # plug effect into mixer
    effect.play(mywav, loop=True)  # plug wavfile into effect
    time.sleep(3.5)   # loop is 3.5/2 seconds long
    i = (i+1) % len(effects)

