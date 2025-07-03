import pygame
from moviepy import VideoFileClip
from moviepy.video.fx import Resize
from PIL import Image
from scripts.ScreenController import *
from scripts.GlobalIndex import *

# clip = VideoFileClip(intro_path)
# clip.preview()

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Group 2 - Python - Tic Tac Toe')
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

asyncio.run(mainScreen(screen, font_path))