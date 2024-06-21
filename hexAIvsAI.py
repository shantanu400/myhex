import pygame,sys
import numpy as np
from pygame import draw
from pygame.draw import circle
from turtle import *
from math import inf
from heapq import heappush, heappop
from string import ascii_uppercase
from collections import OrderedDict

# pygame.init()

# WIDTH = 350
# HEIGHT = 350
BORDER_LINE_WIDTH = 2
INSIDE_LINE_WIDTH = 1
# BOARD_SIZE = 5
# BOARD_ROWS = 5
# BOARD_COLS = 5
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CIRCLE_COLOR = (239, 231, 200)
CROSS_WIDTH = 25
SPACE = 55
CROSS_COLOR =(66, 66, 66)

DEPTH = 2
RED = (255,0,0)
BLUE = (0,0, 255)
BG_COLOR = (28,170,156)
LINE_COLOR = (23, 145, 135)

# screen = pygame.display.set_mode((WIDTH,HEIGHT))
# pygame.display.set_caption('TIC TAC TOE')
# screen.fill(BG_COLOR)

# board
# board = np.zeros( (BOARD_ROWS, BOARD_COLS) )
# print(board)
 

def draw_figures(screen, a, BOARD_SIZE):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if a[row][col] == '2':
                pygame.draw.rect(screen, RED, [int(col*50 + 50), int(row*50 + 50),50,50])
                # pygame.draw.circle(screen, CIRCLE_COLOR, (int(col*200 + 200), int(row*200 + 200)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif a[row][col] == '1':
                pygame.draw.rect(screen, BLUE, [int(col*50 + 50), int(row*50 + 50),50,50])
                # pygame.draw.line(screen, CROSS_COLOR, (col*200 + 100 + SPACE, row*200 + 300 - SPACE), (col*200 + 300 - SPACE, row*200 + 100 + SPACE), CROSS_WIDTH)
                # pygame.draw.line(screen, CROSS_COLOR, (col*200 + 100 + SPACE, row*200 + 100 + SPACE), (col*200 + 300 - SPACE, row*200 + 300 - SPACE), CROSS_WIDTH)

# def mark_square(row, col, player):
#     board[row][col] = player

def available_square(a, row, col):
    if a[row][col] == '0':
        return True
    else:
        return False

# def is_board_full():
#     for row in range(BOARD_ROWS):
#         for col in range(BOARD_COLS):
#             if board[row][col] == 0:
#                 return False
#     return True

def draw_lines(screen, BOARD_SIZE):

    START = 100 
    for i in range(BOARD_SIZE - 1):
        pygame.draw.line(screen, LINE_COLOR, (50, START + 50*i), (50*(BOARD_SIZE + 1), START + 50*i), INSIDE_LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (START + 50*i, 50), (START + 50*i, 50*(BOARD_SIZE + 1)), INSIDE_LINE_WIDTH)
    
    pygame.draw.line(screen, BLUE, (50, 50), (50, 50*(BOARD_SIZE + 1)), BORDER_LINE_WIDTH)
    # 4 vertical
    pygame.draw.line(screen, BLUE, (50*(BOARD_SIZE + 1), 50), (50*(BOARD_SIZE + 1), 50*(BOARD_SIZE + 1)), BORDER_LINE_WIDTH)
    # 3 horizontal
    pygame.draw.line(screen, RED, (50, 50), (50*(BOARD_SIZE + 1), 50), BORDER_LINE_WIDTH)
    # 4 horizontal
    pygame.draw.line(screen, RED, (50, 50*(BOARD_SIZE + 1)), (50*(BOARD_SIZE + 1), 50*(BOARD_SIZE + 1)), BORDER_LINE_WIDTH)



def check_win(a, player):

    if gameStatus(a, '1'):
        return True
    elif gameStatus(a, '2'):
        return True
    return False

def restart(screen, a, BOARD_SIZE):
    screen.fill(BG_COLOR)
    draw_lines(screen)
    player = 1
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            a[row][col] = '0'

# draw_lines()

# player = 1
# game_over = False

def positions(i, j, n):
    positionArr = []
    if i is not 0:
        positionArr.append([i - 1, j])
        if j is not n - 1:
            positionArr.append([i - 1, j + 1])
    if i is not n - 1:
        positionArr.append([i + 1, j])
        if j is not 0:
            positionArr.append([i + 1, j - 1])
    if j is not 0:
        positionArr.append([i, j - 1])
    if j is not n - 1:
        positionArr.append([i, j + 1])
    return positionArr
 
 
def score(val, player):
    if val == '0':
        return 1
    elif val == player:
        return 0
 
 
def h(a, player):
    transpose = [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]
    if player == '2':
        a = transpose
    parents = [(j, 0) for j in range(len(a))]
    visited = {}
    priorityQ = []
    n = len(a)
    for pair in parents:
        val = score(a[pair[0]][pair[1]], player)
        if a[pair[0]][pair[1]] == '0':
            visited[str(pair[0]) + str(pair[1])] = 1
            heappush(priorityQ, (1, str(pair[0]) + str(pair[1])))
        elif a[pair[0]][pair[1]] == player:
            visited[str(pair[0]) + str(pair[1])] = 0
            heappush(priorityQ, (0, str(pair[0]) + str(pair[1])))
 
    while priorityQ:
        parent = heappop(priorityQ)
        parentPos = parent[1]
        parentVal = parent[0]
        if parentPos[1] == str(n - 1):
            return parentVal
        children = positions(int(parentPos[0]), int(parentPos[1]), n)
        for child in children:
            temp = score(a[child[0]][child[1]], player)
            if temp is not None:
                val = parentVal + temp
                if str(child[0]) + str(child[1]) not in visited.keys() or visited[str(child[0]) + str(child[1])] > val:
                    val = parentVal + score(a[child[0]][child[1]], player)
                    visited[str(child[0]) + str(child[1])] = val
                    heappush(priorityQ, (val, str(child[0]) + str(child[1])))
 
 
 
def vacantPlaces(a):
    nextLIst = []
    for i in range(len(a)):
        for j in range(len(a)):
            if a[i][j] is '0':
                pairs = (chr(65 + i), j)
                nextLIst.append(pairs)
    return nextLIst
 
 
def check(a, x, player, visited):
    if a[x[0]][x[1]] == str(player):
        pathList = positions(x[0], x[1], len(a))
        for y in pathList:
            if str(y) not in visited.keys():
                if a[y[0]][y[1]] == str(player):
                    visited[str(y)] = True
                    if y[1] == len(a) - 1:
                        return 302
                    val = check(a, y, player, visited)
                    if val == 302:
                        return 302
    return 404
 
 
def gameStatus(a, player):
    transpose = [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]
    if player == '2':
        a = transpose
    firstList = [(j, 0) for j in range(len(a))]
    for i in firstList:
        visited = {str([i[0], i[1]]): True}
        result = check(a, i, player, visited)
        if result == 302:
            return True
    return False
 
 
def minimax(a, d, player1, player2, start):
    h1 = h(a, player2)
    if h1 == 0:
        if player2 == start:
            return 1000, '99'
        else:
            return -1000, '99'
    if d <= 0:
        h2 = h(a, player1)
        return h1 - h2, '99'
 
    else:
        seats = vacantPlaces(a)
        valList = OrderedDict()
        for pair in seats:
            x = ord(pair[0]) - 65
            y = int(pair[1])
            newA = list(map(list, a))
            newA[x][y] = player1
            val, kkl = minimax(newA, d - 1, player2, player1, start)
            valList[str(x) + str(y)] = val
        if player1 is start:
            pos = sorted(valList.items(), key=lambda bla: bla[1], reverse=True)[0][0]
            maxVal = sorted(valList.items(), key=lambda bla: bla[1], reverse=True)[0][1]
            return maxVal, pos
        else:
            pos = sorted(valList.items(), key=lambda bla: bla[1])[0][0]
            minVal = sorted(valList.items(), key=lambda bla: bla[1])[0][1]
            return minVal, pos
 
def start(a, n, d):

    BOARD_SIZE = n
    WIDTH = (n + 2)*50
    HEIGHT = (n + 2)*50
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('HEX AI vs AI')
    screen.fill(BG_COLOR)
    draw_lines(screen, BOARD_SIZE)
    draw_figures(screen, a, BOARD_SIZE)
    player1 = '1'
    player2 = '2'
    steps = OrderedDict()
    player = 1
    game_over = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0] #x
                mouseY = event.pos[1] #y
                # print(mouseX)
                # print(mouseY)
                x = int((mouseY - 50)//50)
                y = int((mouseX - 50)//50)
                # print(clicked_row)
                # print(clicked_col)

                # if available_square(a, x, y):
                #     if player == 1:
                #         a[x][y] = str(player1)
                #         player1, player2 = player2, player1
                #         if(check_win(a,1)):
                #             game_over = True
                #             print("Player 1 Won!")
                #         player = 2 
                #     draw_figures(screen, a, BOARD_SIZE)
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                if event.key == pygame.K_a:
                        val, pos = minimax(a, d, player1, player2, player1)
                        x = int(pos[0])
                        y = int(pos[1])
                        a[x][y] = str(player1)
                        pos1 = chr(int(pos[0]) + 65)
                        pos2 = pos[1]
                        pos = pos1 + pos2
                        steps[pos] = player1
                        player1, player2 = player2, player1
                        # x = int(pos[0])
                        # y = int(pos[1])
                        # mark_square(x, y, 1)
                        if(gameStatus(a,'1')):
                            game_over = True
                            print("Player 1 Won!")
                        player = 2
                        draw_figures(screen, a, BOARD_SIZE)
                if event.key == pygame.K_b:
                        val, pos = minimax(a, d, player1, player2, player1)
                        x = int(pos[0])
                        y = int(pos[1])
                        a[x][y] = str(player1)
                        pos1 = chr(int(pos[0]) + 65)
                        pos2 = pos[1]
                        pos = pos1 + pos2
                        steps[pos] = player1
                        player1, player2 = player2, player1
                        # x, y = minimax(2, DEPTH)
                        # x = int(pos[0])
                        # y = int(pos[1])
                        # mark_square(x, y, 2)
                        if(gameStatus(a,'2')):
                            game_over = True
                            print("Player 2 Won!")
                        player = 1
                        draw_figures(screen, a, BOARD_SIZE)

        pygame.display.update()
    
def printing(steps):
    for i in steps:
        print(str(steps[i]) + ' ' + str(i))
 
 
def main():
        n, d = input().split()
        n = int(n)
        d = int(d)
        a = []
        for i in range(n):
            b = [str(j) for j in input().split()]
            a.append(b)
        start(a, n, d)
 
 
if __name__ == "__main__":
    main()