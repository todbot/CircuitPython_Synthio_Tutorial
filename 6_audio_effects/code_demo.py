# 6_audio_effects/code_demo.py -- show off some audio effects
import time, audiofilters, audiodelays, audiocore, synthio
from synth_setup import mixer, BUFFER_SIZE, CHANNEL_COUNT, SAMPLE_RATE
cfg = { 'buffer_size': BUFFER_SIZE,
        'channel_count': CHANNEL_COUNT,
        'sample_rate': SAMPLE_RATE }
effects = (
     audiodelays.Chorus(**cfg, mix = 1.0,
                        max_delay_ms = 100,
                        delay_ms = synthio.LFO(rate=0.2),
                        voices = 3),
     audiodelays.Echo(**cfg, mix = 0.6,
                      max_delay_ms = 300,
                      delay_ms = 300,
                      decay = 0.6),
     audiofilters.Distortion(**cfg, mix = 1.0,
                             mode = audiofilters.DistortionMode.OVERDRIVE,
                             soft_clip = True,
                             pre_gain = 30,
                             post_gain = -20),
     audiofilters.Filter(**cfg, mix=1.0,
                         filter = synthio.Biquad(synthio.FilterMode.LOW_PASS,
                                                 frequency=100, Q=1.2)),
     audiofilters.Filter(**cfg, mix=1.0,
                         filter = synthio.Biquad(synthio.FilterMode.HIGH_PASS,
                                                 frequency=1000, Q=1.2)),
    )

mixer.voice[0].level = 1.0
mywav = audiocore.WaveFile("amen1_44k_s16.wav")
i = 0
while True:
    effect = effects[i]  # pick a new effect
    print("i:", i, effect)
    mixer.voice[0].play(effect)
    effect.play(mywav, loop=True)
    time.sleep(3.5)
    i = (i+1) % len(effects)
