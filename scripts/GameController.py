import pygame
import time
import ctypes
from scripts.TicTacToe import TicTacToe
from scripts.Algorithms import *
from scripts.GlobalIndex import *
from scripts.SoundController import *

def init(matrix):
    global tictactoe
    tictactoe = TicTacToe(matrix, False, -1)
    tictactoe.setTime(None)

    

def textFormat(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, True, textColor)
    return newText

def gameOption(isMachine, isCross, algorithms):
    tictactoe.setIsMachine(isMachine)

    tictactoe.resetMatrix()
    tictactoe.setPlayerRule(-1 if isCross else 1)
    tictactoe.setScore([0, 0])
    tictactoe.setAlgorithms(algorithms)

    tictactoe.setTime(None)
    tictactoe.setMiniTime(None)


def checkMatrix(screen, initData, matrix):
    for col in range(matrix.shape[0]):
        for row in range(matrix.shape[1]):
            coord = ((col*initData[0] + (1/6)*initData[0]+10), (row*initData[0] + (1/6)*initData[0]+10))

            if matrix[row][col] == -1:
                screen.blit(initData[1],coord)
            elif matrix[row][col] == 1:
                screen.blit(initData[2],coord)

def gameStatus(screen, initData, isCross, isSound, board_size):
    isWin = checkWinner(tictactoe.getMatrix(), board_size)
    if isWin != None:
        if isWin == 0:
            if chooseOption(screen, initData, "Hòa", "Chơi tiếp", "Thoát",board_size, isSound):
                tictactoe.resetMatrix()
                tictactoe.setRule(-1)
                tictactoe.setPlayerRule(-1 if isCross else 1)
                tictactoe.setTime(None)
                tictactoe.setMiniTime(None)

                userScore, rivalScore = tictactoe.getScore()
                tictactoe.setScore([userScore, rivalScore])

                reloadScreenGame(screen, initData, board_size)
            else:
                tictactoe.resetMatrix()
                return True
        elif tictactoe.getIsMachine():
            if tictactoe.getPlayerRule() == isWin:
                soundWinPlay(isSound)
                if chooseOption(screen, initData, "Thắng", "Chơi tiếp", "Thoát",board_size, isSound):
                    tictactoe.resetMatrix()
                    tictactoe.setRule(-1)
                    tictactoe.setPlayerRule(-1 if isCross else 1)
                    tictactoe.setTime(None)
                    tictactoe.setMiniTime(None)

                    userScore, rivalScore = tictactoe.getScore()
                    tictactoe.setScore([userScore + 1, rivalScore])
                    reloadScreenGame(screen, initData, board_size)
                else:
                    tictactoe.resetMatrix()
                    return True
            else:
                soundLosePlay(isSound)
                if chooseOption(screen, initData, "Thua cuộc", "Chơi lại", "Thoát",board_size, isSound):
                    tictactoe.resetMatrix()
                    tictactoe.setRule(-1)
                    tictactoe.setPlayerRule(-1 if isCross else 1)
                    tictactoe.setTime(None)
                    tictactoe.setMiniTime(None)

                    userScore, rivalScore = tictactoe.getScore()
                    tictactoe.setScore([userScore, rivalScore + 1])
                    reloadScreenGame(screen, initData, board_size)
                else:
                    tictactoe.resetMatrix()
                    return True
        else:
            if isWin == 1:
                mess = "O thắng"
            elif isWin == -1:
                mess = "X thắng"
            if chooseOption(screen, initData, mess, "Chơi tiếp", "Thoát",board_size, isSound):
                tictactoe.resetMatrix()
                tictactoe.setRule(-1)
                tictactoe.setPlayerRule(-1 if isCross else 1)
                tictactoe.setTime(None)
                tictactoe.setMiniTime(None)

                userScore, rivalScore = tictactoe.getScore()
                tictactoe.setScore([userScore + 1, rivalScore])

                reloadScreenGame(screen, initData, board_size)
            else:
                tictactoe.resetMatrix()
                return True


    return False

def indexShow(screen):
    cur_time = time.time()
    elapsed_time = cur_time - tictactoe.getTime()    
    elapsed_time = convertSecondsToTime(elapsed_time)
    mess_time = f"{elapsed_time[0]} : {elapsed_time[1]} : {elapsed_time[2]}"
    text_time = textFormat(mess_time, font_path, 30, (117,236,155)) 
    screen.blit(text_time, (670, 275))

    elapsed_mini_time = cur_time - tictactoe.getMiniTime()
    elapsed_mini_show_time = convertSecondsToTime(elapsed_mini_time)
    mess_mini_time = f"{elapsed_mini_show_time[0]} : {elapsed_mini_show_time[1]} : {elapsed_mini_show_time[2]}"
    if tictactoe.getRule() == tictactoe.getPlayerRule():
        text_mini_time = textFormat(mess_mini_time, font_path, 20, (255,255,255)) 
    else:
        text_mini_time = textFormat(mess_mini_time, font_path, 20, (255,0,0)) 
    screen.blit(text_mini_time, (710, 197))

    userScore, rivalScore = tictactoe.getScore()
    
    text_userScore = textFormat(str(userScore), font_path, 90, (255,255,255)) 
    text_rivalScore = textFormat(str(rivalScore), font_path, 90, (0,0,0)) 
    screen.blit(text_userScore, (627, 463))
    screen.blit(text_rivalScore, (627, -15))
    

    return elapsed_mini_time

def evenInput(screen, initData, buttonArray, isCross, isSound,board_size, online):
    elapsed_mini_time = indexShow(screen)

    # if tictactoe.getIsMachine():
    if (tictactoe.getIsMachine() or online != None) and elapsed_mini_time > 1:
            if tictactoe.getRule() != tictactoe.getPlayerRule():
                if online != None:
                    tickMachine(screen, initData, None, False, isSound,board_size, online)
                else:
                    tickMachine(screen, initData, tictactoe.getAlgorithms(), False, isSound,board_size, None)
                show(tictactoe.getMatrix())
                

    click = False
    pos_mouse = [0, 0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos_mouse = pygame.mouse.get_pos()

            if tictactoe.getIsMachine():
                if tictactoe.getRule() == tictactoe.getPlayerRule():
                    tick(screen, pos_mouse, initData, isSound,board_size, None)
            else:
                if online != None and tictactoe.getRule() == tictactoe.getPlayerRule():
                    tick(screen, pos_mouse, initData, isSound,board_size, online)
                else:
                    tick(screen, pos_mouse, initData, isSound,board_size, None)

            # print(pos_mouse)
            
            # pygame.draw.rect(screen, (73, 97, 230), buttonArray[0])
            # pygame.draw.rect(screen, (73, 97, 230), buttonArray[1])
            # pygame.draw.rect(screen, (73, 97, 230), buttonArray[2])
            # pygame.draw.rect(screen, (73, 97, 230), buttonArray[3])
            giveupButton(buttonArray[3], pos_mouse, screen, initData, isCross, isSound, board_size)
            backButton(buttonArray[1], pos_mouse, screen, initData, isSound, board_size)
            suggestButton(buttonArray[2], pos_mouse, screen, initData, isSound, board_size)
            
            click = True
    
    return [pos_mouse, click]

            
def tick(screen, pos_mouse, initData, isSound,board_size, online):
    print("tick")
    pos_col = int(pos_mouse[0] / initData[0])
    pos_row = int(pos_mouse[1] / initData[0])

    if (pos_col > board_size) or (pos_col < 0) or (pos_row > board_size) or (pos_row < 0):
        return

    if tictactoe.getMatrix()[pos_row][pos_col] == 0:
        soundAttackPlay(isSound)

        if tictactoe.getSuggest():
            reloadScreenGame(screen, initData, board_size)
            checkMatrix(screen, initData, tictactoe.getMatrix())

        coord = ((pos_col*initData[0] + (1/6)*initData[0]+10), (pos_row*initData[0] + (1/6)*initData[0]+10))

        if tictactoe.getRule() == -1:
            screen.blit(initData[1],coord)
        elif tictactoe.getRule() == 1:
            screen.blit(initData[2],coord)

        tictactoe.setMatrix(pos_row, pos_col, tictactoe.getRule())
        tictactoe.changeRule(tictactoe.getRule())
        tictactoe.setMiniTime(None)
        tictactoe.addHistory([pos_row, pos_col])

        if online != None:
           client.makeMove(pos_row, pos_col)


def tickMachine(screen, initData, algorithms, isAICombat, isSound,board_size, online):
    print("tickMachine")

    if algorithms != None:
        if algorithms == 1:
            pos_col, pos_row = greedy(tictactoe.getMatrix(), -tictactoe.getPlayerRule(), board_size)
            # pos_col, pos_row = AStar(tictactoe.getMatrix(), -tictactoe.getPlayerRule())
        elif algorithms == 2:
            pos_col, pos_row = AStar(tictactoe.getMatrix(), -tictactoe.getPlayerRule(), board_size)
            # pos_col, pos_row = MinimaxAlphaBeta(tictactoe.getMatrix(), -tictactoe.getPlayerRule())
        elif algorithms == 3:
            pos_col, pos_row = AlphaZero(tictactoe.getMatrix(), -tictactoe.getPlayerRule())
    
    if online != None:
        print("load")
        pos_row, pos_col = client.updateMove()
        if (pos_row <= -1 or pos_col <= -1):
            pygame.quit()
            ctypes.windll.user32.MessageBoxW(0, "Đối thủ đã bỏ chạy!", "Thông báo", 0x40 | 0x1)


    soundAttackPlay(isSound)
    coord = ((pos_col*initData[0] + (1/6)*initData[0]+10), (pos_row*initData[0] + (1/6)*initData[0]+10))

    if isAICombat:
        if tictactoe.getRule() == -1:
            screen.blit(initData[1],coord)
        elif tictactoe.getRule() == 1:
            screen.blit(initData[2],coord)
    else:
        if tictactoe.getPlayerRule() == -1:
            screen.blit(initData[2],coord)
        elif tictactoe.getPlayerRule() == 1:
            screen.blit(initData[1],coord)
    
     
    tictactoe.setMiniTime(None)
    tictactoe.setMatrix(pos_row, pos_col, tictactoe.getRule())
    tictactoe.changeRule(tictactoe.getRule())
    # show(tictactoe.getMatrix())
    tictactoe.addHistory([pos_row, pos_col])


def chooseOption(screen, initData, message, yesMess, noMess,board_size, isSound):
    while True:
        # screen.fill((115, 166, 45))
        
        option_menu = pygame.image.load(menu_game_path)
        screen.blit(option_menu, (0, 0))
        
        no_button = pygame.Rect(690, 312, 150, 50)
        yes_button = pygame.Rect(690, 380, 150, 50)

        text_mess = textFormat(message, font_path, 30, (255,255,255)) 
        screen.blit(text_mess, (650, 210))
        text_mess = textFormat(noMess, font_path, 20, (0,0,0)) 
        screen.blit(text_mess, (695, 320))
        text_mess = textFormat(yesMess, font_path, 20, (0,0,0)) 
        screen.blit(text_mess, (695, 390))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos_mouse = pygame.mouse.get_pos()
                # print(pos_mouse)

                if no_button.collidepoint((pos_mouse[0], pos_mouse[1])):
                    soundClickPlay(isSound)
                    reloadScreenGame(screen, initData, board_size)
                    return False
                if yes_button.collidepoint((pos_mouse[0], pos_mouse[1])):
                    soundClickPlay(isSound)
                    reloadScreenGame(screen, initData, board_size)
                    
                    return True
        
        pygame.display.update()
        fpsClock.tick(FPS)

def reloadScreenGame(screen, initData, board_size):
    tictactoe.setSuggest(False)

    res = (WINDOW_HEIGHT/board_size - 1)
    borders = int((WINDOW_HEIGHT - res * board_size)/ 2)
    screen.fill((141, 95, 24))
    for i in range(board_size):
            for j in range(board_size):
                screen.blit(initData[3],(i*res+borders,j*res+borders))

def exitButton(screen, initData, exitButton, pos_mouse, isSound,board_size, online):
    if exitButton.collidepoint((pos_mouse[0], pos_mouse[1])):
        if chooseOption(screen, initData, "Thoát", "Thoát", "Hủy",board_size, isSound):
            if online != None:
                client.logout()
                pygame.quit()

                ctypes.windll.user32.MessageBoxW(0, "Đối thủ đã bỏ chạy!", "Thông báo", 0x40 | 0x1)
            return True
        else:
            checkMatrix(screen, initData, tictactoe.getMatrix())

def giveupButton(giveupButton, pos_mouse, screen, initData, isCross, isSound, board_size):
    if giveupButton.collidepoint((pos_mouse[0], pos_mouse[1])):
        soundClickPlay(isSound)

        if chooseOption(screen, initData, "Đầu hàng", "Đầu hàng", "Hủy", board_size, isSound):
            tictactoe.resetMatrix()
            tictactoe.setRule(-1)
            tictactoe.setPlayerRule(-1 if isCross else 1)
            tictactoe.setTime(None)
            tictactoe.setMiniTime(None)

            userScore, rivalScore = tictactoe.getScore()
            tictactoe.setScore([userScore, rivalScore + 1])

            reloadScreenGame(screen, initData, board_size)
        else:
            checkMatrix(screen, initData, tictactoe.getMatrix())

def backButton(backButton, pos_mouse, screen, initData, isSound, board_size):
    if backButton.collidepoint((pos_mouse[0], pos_mouse[1])):
        soundClickPlay(isSound)

        pos_x, pos_o = tictactoe.getHistory()

        if pos_x == None and pos_o == None:
            return
        
        if tictactoe.getIsMachine():
            if pos_o != None:
                tictactoe.setMatrix(pos_o[0], pos_o[1], 0)
            
            tictactoe.setMatrix(pos_x[0], pos_x[1], 0)
        else:
            if pos_o != None:
                tictactoe.setMatrix(pos_o[0], pos_o[1], 0)
            else:
                tictactoe.setMatrix(pos_x[0], pos_x[1], 0)
        
        if tictactoe.getIsMachine() and tictactoe.getPlayerRule() == 1:
            tictactoe.setRule(1)
        else:
            tictactoe.setRule(-1)
        reloadScreenGame(screen, initData, board_size)
        checkMatrix(screen, initData, tictactoe.getMatrix())

def suggestButton(suggestButton, pos_mouse, screen, initData, isSound, board_size):
    if suggestButton.collidepoint((pos_mouse[0], pos_mouse[1])):
        soundClickPlay(isSound)
        
        if not tictactoe.getSuggest():
            pos_col, pos_row = AStar(tictactoe.getMatrix(),tictactoe.getPlayerRule(), board_size)

            tictactoe.setSuggest(True)
            coord = ((pos_col*initData[0] + (1/6)*initData[0]+10), (pos_row*initData[0] + (1/6)*initData[0]+10))

            screen.blit(initData[4],coord)


def evenInputAICombat(screen, initData, algorithms_A, algorithms_B,board_size, isSound):
    elapsed_mini_time = indexShow(screen)

    # if tictactoe.getIsMachine():
    if elapsed_mini_time > 2:
        if tictactoe.getRule() == -1:
            tickMachine(screen, initData, algorithms_A, True, isSound,board_size, None)
        elif tictactoe.getRule() == 1:
            tickMachine(screen, initData, algorithms_B, True, isSound,board_size, None)
        # show(tictactoe.getMatrix())
                

    click = False
    pos_mouse = [0, 0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos_mouse = pygame.mouse.get_pos()

            # print(pos_mouse)
            
            click = True
    
    return [pos_mouse, click]