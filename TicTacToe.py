#header files
import pygame as pyg
import sys as s
from pygame.locals import *
import time

#important variables
turn = 'X'
win_turn = None
draw = False
wt = 500
ht = 500
bg_color = (240, 230, 140)
table_line = (32, 32, 32)

#TicTacToe board
table = [[None]*3, [None]*3, [None]*3]

#main window
pyg.init()
fps = 30
CLOCK = pyg.time.Clock()
screen = pyg.display.set_mode((wt, ht+100), 0, 32)
pyg.display.set_caption("Tic Tac Toe")

#loading the images
opening = pyg.image.load('Props/tic_tac_toe.png')
x_img = pyg.image.load('Props/x.png')
o_img = pyg.image.load('Props/o.png')

#loading sound
start_sound = pyg.mixer.Sound('Props/start_sound.wav')

#image resize
x_img = pyg.transform.scale(x_img, (100, 100))
o_img = pyg.transform.scale(o_img, (100, 100))
opening = pyg.transform.scale(opening, (wt, ht+100))

#game layout
def game_layout():

    screen.blit(opening, (0, 0))
    pyg.display.update()
    start_sound.play()
    time.sleep(3.5)
    screen.fill(bg_color)
    start_sound.stop()

    # Drawing Vlines
    pyg.draw.line(screen, table_line, (wt/3, 0), (wt/3, ht), 10)
    pyg.draw.line(screen, table_line, (wt/3*2, 0), (wt/3*2, ht), 10)
    # Drawing Hlines
    pyg.draw.line(screen, table_line, (0, ht/3), (wt, ht/3), 10)
    pyg.draw.line(screen, table_line, (0,ht/3*2), (wt, ht/3*2), 10)
    check_status()

def check_status():
    global draw
    if win_turn == None:
        message = turn + "'s Turn"
    else:
        message = win_turn + " won!"
        #win_turn = None
    if draw:
        message = 'Game Draw!'
    font = pyg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))
    # copy the rendered message onto the board
    screen.fill ((0,0,128), (0, 500, 500, 100))
    text_rect = text.get_rect(center=(wt/2, 600-50))
    screen.blit(text, text_rect)
    pyg.display.update()
    if(win_turn != None):
        time.sleep(1)

def check_win():
    global table, win_turn,draw

    # checking for winning rows
    for r in range (0,3):
        if ((table [r][0] == table[r][1] == table[r][2]) and(table [r][0] is not None)):
            win_turn = table[r][0]
            pyg.draw.line(screen, 	(0,128,128), (0, (r + 1)*ht/3 - ht/6), (wt, (r + 1)*ht/3 - ht/6 ), 4)
            break

    # checking for winning columns
    for c in range (0, 3):
        if (table[0][c] == table[1][c] == table[2][c]) and (table[0][c] is not None):
            win_turn = table[0][c]
            pyg.draw.line (screen, 	(0,128,128),((c + 1)* wt/3 - wt/6, 0), ((c + 1)* wt/3 - wt/6, ht), 4)
            break

    # checking for diagonal winning
    if (table[0][0] == table[1][1] == table[2][2]) and (table[0][0] is not None):
        # front diagonal
        win_turn = table[0][0]
        pyg.draw.line (screen, 	(0,128,128), (0, 0), (500, 500), 4)
    if (table[0][2] == table[1][1] == table[2][0]) and (table[0][2] is not None):
        # rear diagonal
        win_turn = table[0][2]
        pyg.draw.line (screen, 	(0,128,128), (0, 500), (500, 0), 4)

    if(all([all(r) for r in table]) and win_turn is None ):
        draw = True
    check_status()

def drawturn(r,c):
    global table, turn

    #for xx changing
    if r==1:
        xx = 30
    elif r==2:
        xx = wt/3 + 30
    else:
        xx = wt/3*2 + 30

    #for yy changing
    if c==1:
        yy = 30
    elif c==2:
        yy = ht/3 + 30
    else:
        yy = ht/3*2 + 30

    table[r-1][c-1] = turn
    if(turn == 'X'):
        screen.blit(x_img, (yy,xx))
        turn = 'O'
    else:
        screen.blit(o_img, (yy,xx))
        turn = 'X'
    pyg.display.update()

def click():
    #get coordinates of mouse click
    x, y = pyg.mouse.get_pos()
    #get cumn of mouse click (1-3)
    if(x<wt/3):
        c = 1
    elif (x<wt/3*2):
        c = 2
    elif(x<wt):
        c = 3
    else:
        c = None
    #get r of mouse click (1-3)
    if(y<ht/3):
        r = 1
    elif (y<ht/3*2):
        r = 2
    elif(y<ht):
        r = 3
    else:
        r = None
    #print(r,c)
    if(r and c and table[r-1][c-1] is None):
        global turn
        #draw the x or o on screen
        drawturn(r, c)
        check_win()

def reset_game():
    global table, win_turn, turn, draw

    time.sleep(1)
    if(win_turn != None):
        turn = win_turn
    else:
        turn = 'X';
    draw = False
    game_layout()
    win_turn=None
    table = [[None]*3,[None]*3,[None]*3]

# main game
game_layout()
while(True):
    for event in pyg.event.get():
        if event.type == QUIT:
            s.exit()
        elif event.type is MOUSEBUTTONDOWN:
            # the user clicked; place an X or O
            click()
            if(win_turn != None or draw == True):
                reset_game()
    pyg.display.update()
    CLOCK.tick(fps)