import pygame
import os
import math
import array
import numpy as np

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.sound_enabled = True
        
        # Create simple sound effects programmatically
        self.create_sounds()
    
    def create_sounds(self):
        """Create simple sound effects"""
        try:
            # Navigation sound (beep)
            self.create_beep_sound('navigate', 800, 0.1)
            
            # Selection sound (higher beep)
            self.create_beep_sound('select', 1200, 0.15)
            
            # Error sound (lower beep)
            self.create_beep_sound('error', 400, 0.2)
            
            # Success sound (chord)
            self.create_success_sound()
            
        except Exception as e:
            print(f"Sound initialization failed: {e}")
            self.sound_enabled = False
    
    def create_beep_sound(self, name: str, frequency: int, duration: float):
        """Create a simple beep sound"""
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []
        
        for i in range(frames):
            time = float(i) / sample_rate
            wave = 4096 * math.sin(frequency * 2 * math.pi * time)
            arr.append([int(wave), int(wave)])
        
        sound = pygame.sndarray.make_sound(np.array(arr, dtype=np.int16))
        self.sounds[name] = sound
    
    def create_success_sound(self):
        """Create a success chord sound"""
        sample_rate = 22050
        duration = 0.3
        frames = int(duration * sample_rate)
        arr = []
        
        # Create a simple chord (C major)
        frequencies = [523, 659, 784]  # C, E, G
        
        for i in range(frames):
            time = float(i) / sample_rate
            wave = 0
            for freq in frequencies:
                wave += 1365 * math.sin(freq * 2 * math.pi * time)
            
            # Add fade out
            fade = 1.0 - (time / duration)
            wave *= fade
            
            arr.append([int(wave), int(wave)])
        
        sound = pygame.sndarray.make_sound(np.array(arr, dtype=np.int16))
        self.sounds['success'] = sound
    
    def play_sound(self, sound_name: str):
        """Play a sound effect"""
        if self.sound_enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Failed to play sound {sound_name}: {e}")
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled
