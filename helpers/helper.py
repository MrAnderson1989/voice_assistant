
import pygame

# Function to play audio
def play_audio(audio_file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
