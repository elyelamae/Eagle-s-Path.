import pygame
import os

# Initialize Pygame
pygame.init()

# Set up the font
font = pygame.font.Font(None, 74)  # Adjust the font size as needed

# Create a surface with the rendered text
title_text = font.render("Get Ready", True, (0, 0, 0))  # Black color

# Define the path
output_path = 'images/getready.png'

# Create directory if it doesn't exist
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save the surface as a PNG file
pygame.image.save(title_text, output_path)

# Quit Pygame
pygame.quit()
