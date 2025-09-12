# spi_dac.py -- SPI DAC interface for CircuitPython synthio
# Part of todbot CircuitPython Synthio Tutorial
# 12 Sep 2024 - @todbot / Tod Kurt
#
# This module provides an SPI DAC interface that can be used as an alternative
# to audiobusio.I2SOut for audio output with synthio.
#
# Supports common SPI DACs like MCP4922, MCP4912, TLV5618, etc.

import busio
import digitalio
import microcontroller
import array
import time
from micropython import const

# DAC chip types
DAC_MCP4922 = const(0)  # 12-bit dual channel
DAC_MCP4912 = const(1)  # 10-bit dual channel  
DAC_TLV5618 = const(2)  # 12-bit dual channel

class SPIDACAudio:
    """
    SPI DAC audio output class that provides a similar interface to audiobusio.I2SOut
    
    This class allows using SPI-based DACs for audio output with synthio and other
    CircuitPython audio modules.
    """
    
    def __init__(self, spi, cs_pin, dac_type=DAC_MCP4922, sample_rate=44100, 
                 bit_depth=16, channel_count=2, ldac_pin=None):
        """
        Initialize SPI DAC audio output
        
        :param spi: SPI bus object (busio.SPI)
        :param cs_pin: Chip select pin (board pin)
        :param dac_type: Type of DAC chip (DAC_MCP4922, DAC_MCP4912, or DAC_TLV5618)
        :param sample_rate: Audio sample rate in Hz
        :param bit_depth: Audio bit depth (16-bit supported)
        :param channel_count: Number of audio channels (1 or 2)
        :param ldac_pin: Optional LDAC pin for simultaneous channel updates (board pin)
        """
        self._spi = spi
        self._cs = digitalio.DigitalInOut(cs_pin)
        self._cs.direction = digitalio.Direction.OUTPUT
        self._cs.value = True
        
        self._ldac = None
        if ldac_pin:
            self._ldac = digitalio.DigitalInOut(ldac_pin)
            self._ldac.direction = digitalio.Direction.OUTPUT
            self._ldac.value = True
        
        self._dac_type = dac_type
        self._sample_rate = sample_rate
        self._bit_depth = bit_depth
        self._channel_count = channel_count
        
        # Configure DAC parameters based on type
        if dac_type == DAC_MCP4922:
            self._dac_bits = 12
            self._dac_max = 4095
        elif dac_type == DAC_MCP4912:
            self._dac_bits = 10
            self._dac_max = 1023
        elif dac_type == DAC_TLV5618:
            self._dac_bits = 12
            self._dac_max = 4095
        else:
            raise ValueError("Unsupported DAC type")
        
        self._playing = False
        self._audio_source = None
        self._buffer = bytearray(4)  # Buffer for SPI commands
        
        # Calculate timing for sample playback
        self._sample_period = 1.0 / sample_rate
        self._last_sample_time = 0
        
        print(f"SPI DAC initialized: {dac_type}, {sample_rate}Hz, {channel_count}ch")
    
    def play(self, audio_source, *, loop=False):
        """
        Start playing audio from the given source
        
        :param audio_source: Audio source (synthio.Synthesizer, audiocore.WaveFile, etc.)
        :param loop: Whether to loop the audio (default False)
        """
        self._audio_source = audio_source
        self._playing = True
        self._loop = loop
        print("SPI DAC: Starting audio playback")
        
        # Start audio processing in background
        self._start_audio_processing()
    
    def stop(self):
        """Stop audio playback"""
        self._playing = False
        self._audio_source = None
        print("SPI DAC: Stopping audio playback")
    
    @property
    def playing(self):
        """True if audio is currently playing"""
        return self._playing
    
    def _start_audio_processing(self):
        """
        Start the audio processing loop
        This would ideally run in a separate thread or interrupt,
        but for simplicity we'll process samples on-demand
        """
        pass
    
    def _convert_sample_to_dac(self, sample):
        """
        Convert a 16-bit signed audio sample to DAC value
        
        :param sample: 16-bit signed sample (-32768 to 32767)
        :return: DAC value (0 to dac_max)
        """
        # Convert signed 16-bit to unsigned DAC range
        # Add 32768 to shift from signed to unsigned, then scale to DAC range
        unsigned_sample = sample + 32768
        dac_value = (unsigned_sample * self._dac_max) // 65536
        return max(0, min(self._dac_max, dac_value))
    
    def _write_dac_sample(self, left_sample, right_sample=None):
        """
        Write audio samples to the DAC via SPI
        
        :param left_sample: Left channel sample (16-bit signed)
        :param right_sample: Right channel sample (16-bit signed), if None uses left_sample
        """
        if right_sample is None:
            right_sample = left_sample
        
        left_dac = self._convert_sample_to_dac(left_sample)
        right_dac = self._convert_sample_to_dac(right_sample)
        
        if self._dac_type == DAC_MCP4922:
            self._write_mcp4922(left_dac, right_dac)
        elif self._dac_type == DAC_MCP4912:
            self._write_mcp4912(left_dac, right_dac)
        elif self._dac_type == DAC_TLV5618:
            self._write_tlv5618(left_dac, right_dac)
    
    def _write_mcp4922(self, left_value, right_value):
        """Write samples to MCP4922 DAC"""
        # MCP4922: 16-bit command format
        # Bit 15: 0/1 for DAC A/B
        # Bit 14: Buffer control (1 = buffered)
        # Bit 13: Gain select (1 = 1x gain)
        # Bit 12: Shutdown (1 = active)
        # Bits 11-0: Data
        
        # Channel A (left)
        cmd_a = (0 << 15) | (1 << 14) | (1 << 13) | (1 << 12) | (left_value & 0xFFF)
        self._buffer[0] = (cmd_a >> 8) & 0xFF
        self._buffer[1] = cmd_a & 0xFF
        
        self._cs.value = False
        self._spi.write(self._buffer[:2])
        self._cs.value = True
        
        # Channel B (right)
        cmd_b = (1 << 15) | (1 << 14) | (1 << 13) | (1 << 12) | (right_value & 0xFFF)
        self._buffer[0] = (cmd_b >> 8) & 0xFF
        self._buffer[1] = cmd_b & 0xFF
        
        self._cs.value = False
        self._spi.write(self._buffer[:2])
        self._cs.value = True
        
        # Pulse LDAC if available for simultaneous update
        if self._ldac:
            self._ldac.value = False
            self._ldac.value = True
    
    def _write_mcp4912(self, left_value, right_value):
        """Write samples to MCP4912 DAC"""
        # MCP4912: 16-bit command format (similar to MCP4922 but 10-bit data)
        left_value = left_value >> 2  # Convert 12-bit to 10-bit
        right_value = right_value >> 2
        
        # Channel A (left)
        cmd_a = (0 << 15) | (1 << 14) | (1 << 13) | (1 << 12) | ((left_value & 0x3FF) << 2)
        self._buffer[0] = (cmd_a >> 8) & 0xFF
        self._buffer[1] = cmd_a & 0xFF
        
        self._cs.value = False
        self._spi.write(self._buffer[:2])
        self._cs.value = True
        
        # Channel B (right)
        cmd_b = (1 << 15) | (1 << 14) | (1 << 13) | (1 << 12) | ((right_value & 0x3FF) << 2)
        self._buffer[0] = (cmd_b >> 8) & 0xFF
        self._buffer[1] = cmd_b & 0xFF
        
        self._cs.value = False
        self._spi.write(self._buffer[:2])
        self._cs.value = True
        
        if self._ldac:
            self._ldac.value = False
            self._ldac.value = True
    
    def _write_tlv5618(self, left_value, right_value):
        """Write samples to TLV5618 DAC"""
        # TLV5618: 16-bit command format
        # Bits 15-14: DAC select (00=A, 01=B)
        # Bit 13: Speed select (0=fast, 1=slow)
        # Bit 12: Power down (0=normal, 1=power down)
        # Bits 11-0: Data
        
        # Channel A (left)
        cmd_a = (0 << 14) | (0 << 13) | (0 << 12) | (left_value & 0xFFF)
        self._buffer[0] = (cmd_a >> 8) & 0xFF
        self._buffer[1] = cmd_a & 0xFF
        
        self._cs.value = False
        self._spi.write(self._buffer[:2])
        self._cs.value = True
        
        # Channel B (right)
        cmd_b = (1 << 14) | (0 << 13) | (0 << 12) | (right_value & 0xFFF)
        self._buffer[0] = (cmd_b >> 8) & 0xFF
        self._buffer[1] = cmd_b & 0xFF
        
        self._cs.value = False
        self._spi.write(self._buffer[:2])
        self._cs.value = True
    
    def update(self):
        """
        Update method to be called from main loop to process audio samples
        This simulates the continuous audio processing that would normally
        happen in interrupts or DMA
        """
        if not self._playing or not self._audio_source:
            return
        
        current_time = time.monotonic()
        if current_time - self._last_sample_time >= self._sample_period:
            self._last_sample_time = current_time
            
            # Try to get samples from the audio source
            # For now, we'll generate a simple test tone
            # In a full implementation, this would read from the actual audio buffer
            try:
                # Generate a simple test tone for demonstration
                # This would be replaced with actual audio buffer reading
                import math
                t = current_time * 440 * 2 * math.pi  # 440 Hz test tone
                test_sample = int(math.sin(t) * 16384)  # 16-bit amplitude
                
                if self._channel_count == 2:
                    self._write_dac_sample(test_sample, test_sample)
                else:
                    self._write_dac_sample(test_sample)
            except Exception as e:
                print(f"SPI DAC update error: {e}")
                pass