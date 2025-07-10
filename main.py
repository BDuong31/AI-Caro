import pygame
# from moviepy import VideoFileClip
# from moviepy.video.fx import Resize
from PIL import Image
from scripts.ScreenController import *
from scripts.GlobalIndex import *
from scripts.engine_alphazero import initialize_ai

# clip = VideoFileClip(intro_path)
# clip.preview()

GAME_TYPE = 1
MODEL_PATH = "/Users/bduong/Documents/caro-ai-13/scripts/lib/saves/MyTicTacToeRun_01/best_001_04050.dat" 

initialize_ai(GAME_TYPE, MODEL_PATH)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Group 2 - Python - Tic Tac Toe')
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

asyncio.run(mainScreen(screen, font_path))