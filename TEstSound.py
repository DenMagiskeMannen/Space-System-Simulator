# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 19:02:57 2024

@author: teodo
"""
import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Load the sound file
sound_effect = pygame.mixer.Sound('shabom.mp3')

# Function to change the pitch
def change_pitch(sound, pitch_factor):
    sound_array = pygame.sndarray.array(sound)
    # Resample the array
    indices = np.round(np.arange(0, len(sound_array), pitch_factor))
    indices = indices[indices < len(sound_array)].astype(int)
    pitched_sound_array = sound_array[indices]
    # Convert the numpy array back to a Sound object
    pitched_sound = pygame.sndarray.make_sound(pitched_sound_array)
    return pitched_sound

# Set up the display
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Play Sound on Button Press with Pitch Change")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define the button
button_rect = pygame.Rect(150, 120, 100, 50)

# Set the pitch factor (1.0 is normal, >1 is higher pitch, <1 is lower pitch)
pitch_factor = 0.9

# Main loop
running = True
while running:
    screen.fill(WHITE)
    
    # Draw the button
    pygame.draw.rect(screen, RED, button_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                # Change the pitch and play the sound
                altered_sound = change_pitch(sound_effect, pitch_factor)
                altered_sound.play()

    pygame.display.flip()

pygame.quit()

