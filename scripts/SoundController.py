import pygame
from scripts.GlobalIndex import *

volumeValue = 1

pygame.mixer.init()

soundAttack  = pygame.mixer.Sound('./sounds/attack.mp3')
soundChange  = pygame.mixer.Sound('./sounds/change.mp3')
soundLose  = pygame.mixer.Sound('./sounds/lose.mp3')
soundWin  = pygame.mixer.Sound('./sounds/win.mp3')
soundClick  = pygame.mixer.Sound('./sounds/click.mp3')

def soundMenuPlay(isSound):
    # if data.getSound():
    if isSound:
        pygame.mixer.music.load('./sounds/chill1.mp3')
        pygame.mixer.music.play(-1)

def soundBackGroundStop(isSound):
    pygame.mixer.music.stop()
    
    # if data.getSound():
    if isSound:
        soundChangePlay(isSound)

def soundGamePlay(isSound):
    # if data.getSound():
    if isSound:
        pygame.mixer.music.load('./sounds/chill2.mp3')
        pygame.mixer.music.play(-1)

def soundAttackPlay(isSound):
    # if data.getSound():
    if isSound:
        soundAttack.set_volume(volumeValue)
        soundAttack.play()

def soundChangePlay(isSound):
    # if data.getSound():
    if isSound:
        soundChange.set_volume(0.3)
        soundChange.play()

def soundLosePlay(isSound):
    # if data.getSound():
    if isSound:
        soundLose.set_volume(volumeValue)
        soundLose.play()

def soundWinPlay(isSound):
    # if data.getSound():
    if isSound:
        soundWin.set_volume(volumeValue)
        soundWin.play()

def soundClickPlay(isSound):
    # if data.getSound():
    if isSound:
        soundClick.set_volume(volumeValue)
        soundClick.play()
