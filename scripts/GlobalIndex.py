import pygame
from scripts.Client import Client

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 30
GRID_SIZE = 19

icon_path = './textures/images/icon.png'
logo_path = './textures/images/logo.png'
button_path = './textures/images/button.png'
robot_icon_path = './textures/images/robot-icon.png'
user_icon_path = './textures/images/user-icon.png'
sound_icon_path = './textures/images/sound.png'
info_icon_path = './textures/images/info-icon.png'
start_icon_path = './textures/images/start-icon.png'
square_path = './textures/images/square.png'
x_path = './textures/images/x.png'
o_path = './textures/images/o.png'
x2_path = './textures/images/x2.png'
menu_continue_path = './textures/images/option1.png'
menu_init_path = './textures/images/option2.png'
menu_game_path = './textures/images/option3.png'
game_button_path = './textures/images/gamebutton.png'
game_button_AI_combat_path = './textures/images/gamebuttonAICombat.png'
info_menu_path = './textures/images/info.png'
font_path = './fonts/AndikaNewBasic-B.ttf'
intro_path = './textures/videos/intro.mp4'

fpsClock = pygame.time.Clock()

client = Client()
client.connect()