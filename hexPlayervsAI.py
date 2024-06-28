import pygame,sys
import numpy as np
from pygame import draw
from pygame.draw import circle
from turtle import *
from math import inf
from heapq import heappush, heappop
from string import ascii_uppercase
from collections import OrderedDict
import time

# Define constants for visual styling
BORDER_LINE_WIDTH = 2
INSIDE_LINE_WIDTH = 1
DEPTH = 2  # Depth used for AI decision making, not shown in provided functions
RED = (255,0,0)  # RGB color for player 2
BLUE = (0,0, 255)  # RGB color for player 1
BG_COLOR = (28,170,156)  # Background color of the game board
LINE_COLOR = (23, 145, 135)  # Color of the grid lines

def draw_figures(screen, a, BOARD_SIZE):
    # Draws the player markers on the board as colored rectangles
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if a[row][col] == '2':
                # Draw a red rectangle for player 2's marker
                pygame.draw.rect(screen, RED, [int(col*50 + 50), int(row*50 + 50), 50, 50])
            elif a[row][col] == '1':
                # Draw a blue rectangle for player 1's marker
                pygame.draw.rect(screen, BLUE, [int(col*50 + 50), int(row*50 + 50), 50, 50])

def available_square(a, row, col):
    # Check if a square on the board is unoccupied
    if a[row][col] == '0':
        return True
    else:
        return False

def draw_lines(screen, BOARD_SIZE):
    # Draw grid lines on the board
    START = 100  # Offset to start drawing grid lines from the edge
    for i in range(BOARD_SIZE - 1):
        # Draw horizontal lines across the board
        pygame.draw.line(screen, LINE_COLOR, (50, START + 50*i), (50*(BOARD_SIZE + 1), START + 50*i), INSIDE_LINE_WIDTH)
        # Draw vertical lines down the board
        pygame.draw.line(screen, LINE_COLOR, (START + 50*i, 50), (START + 50*i, 50*(BOARD_SIZE + 1)), INSIDE_LINE_WIDTH)
    
    # Draw boundary lines around the board
    pygame.draw.line(screen, BLUE, (50, 50), (50, 50*(BOARD_SIZE + 1)), BORDER_LINE_WIDTH)
    pygame.draw.line(screen, BLUE, (50*(BOARD_SIZE + 1), 50), (50*(BOARD_SIZE + 1), 50*(BOARD_SIZE + 1)), BORDER_LINE_WIDTH)
    pygame.draw.line(screen, RED, (50, 50), (50*(BOARD_SIZE + 1), 50), BORDER_LINE_WIDTH)
    pygame.draw.line(screen, RED, (50, 50*(BOARD_SIZE + 1)), (50*(BOARD_SIZE + 1), 50*(BOARD_SIZE + 1)), BORDER_LINE_WIDTH)

def check_win(a, player):
    # Check if either player has won the game
    if gameStatus(a, '1'):
        return True  # Player 1 has a winning path
    elif gameStatus(a, '2'):
        return True  # Player 2 has a winning path
    return False

def restart(screen, a, BOARD_SIZE):
    # Reset the game to its initial state
    screen.fill(BG_COLOR)  # Clear the screen with the background color
    draw_lines(screen, BOARD_SIZE)  # Redraw the grid lines
    # Reset the game board to all zeros (unoccupied)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            a[row][col] = '0'
            
def positions(i, j, n):
    """
    Generates a list of adjacent positions for a given cell in a grid.
    Diagonal connections are considered based on grid boundaries.

    Args:
    i (int): The row index of the current cell.
    j (int): The column index of the current cell.
    n (int): The dimension of the square grid (n x n).

    Returns:
    list: A list of tuples, each representing an adjacent cell position.
    """
    positionArr = []
    # Check above the current cell
    if i is not 0:
        positionArr.append([i - 1, j])  # Directly above
        if j is not n - 1:
            positionArr.append([i - 1, j + 1])  # Upper right diagonal

    # Check below the current cell
    if i is not n - 1:
        positionArr.append([i + 1, j])  # Directly below
        if j is not 0:
            positionArr.append([i + 1, j - 1])  # Lower left diagonal

    # Check to the left and right of the current cell
    if j is not 0:
        positionArr.append([i, j - 1])  # Left
    if j is not n - 1:
        positionArr.append([i, j + 1])  # Right

    return positionArr


def vacantPlaces(a):
    """
    Finds all unoccupied (vacant) places on the game board.

    Args:
    a (list): 2D list representing the game board.

    Returns:
    list: A list of tuples representing vacant positions in the format (row, column).
    """
    nextList = []
    for i in range(len(a)):
        for j in range(len(a)):
            if a[i][j] is '0':  # Check if the position is unoccupied
                pairs = (chr(65 + i), j)  # Create a tuple (row as letter, column index)
                nextList.append(pairs)
    return nextList


def check(a, x, player, visited):
    """
    Recursively checks for a winning path starting from a specific cell.

    Args:
    a (list): 2D list representing the game board.
    x (tuple): Current cell coordinates (row, column).
    player (str): Current player's marker.
    visited (dict): Dictionary of visited cells to avoid revisits.

    Returns:
    int: 302 if a winning path is found, otherwise 404.
    """
    # Check if the current cell contains the player's marker.
    if a[x[0]][x[1]] == str(player):
        # Generate a list of positions adjacent to the current cell (x[0], x[1]).
        pathList = positions(x[0], x[1], len(a))

        # Iterate over each position in the path list.
        for y in pathList:
            # Check if the position has not been visited yet to avoid cycles.
            if str(y) not in visited.keys():
                # Verify if the current adjacent position contains the player's marker.
                if a[y[0]][y[1]] == str(player):
                    # Mark this position as visited by adding it to the visited dictionary.
                    visited[str(y)] = True

                    # Check if the current position is in the last column of the board,
                    # which means the player has reached the far right column and possibly completed a path.
                    if y[1] == len(a) - 1:
                        return 302  # Return 302 to indicate a winning path has been found.

                    # Recursively call check to continue pathfinding from the current adjacent cell.
                    val = check(a, y, player, visited)
                    # If a winning path is found downstream, propagate the 302 response back up the call stack.
                    if val == 302:
                        return 302

    # Return 404 if no winning path is found from the current cell.
    return 404



def gameStatus(a, player):
    """
    Determines if the specified player has won by checking all possible paths.

    Args:
    a (list): 2D list representing the game board.
    player (str): The marker of the current player.

    Returns:
    bool: True if the player has won, otherwise False.
    """
    transpose = [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]
    if player == '2':
        a = transpose  # Transpose the board to check vertical paths horizontally
    firstList = [(j, 0) for j in range(len(a))]  # Start points for checking paths
    for i in firstList:
        visited = {str([i[0], i[1]]): True}
        result = check(a, i, player, visited)
        if result == 302:
            return True
    return False

def score(val, player):
    """
    Determines the scoring for a cell based on its current occupant relative to the player.

    Args:
    val (str): The current occupant of the cell ('0' for empty, '1' or '2' for players).
    player (str): The marker of the player evaluating the board.
    

    Returns:
    int: 1 for empty cells, making them more attractive strategically; 0 for cells occupied by the player, 
         indicating no benefit from re-visiting.
    """
    if val == '0':
        return 1  # Unoccupied cells score higher to encourage exploration.
    elif val == player:
        return 0  # Cells occupied by the player offer no additional score.
def h(a, player):
    # Transpose the board if evaluating for player '2' to simplify path checking.
    # This is useful if player '2' needs to connect horizontally and the algorithm naturally checks vertical paths.
    transpose = [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]
    if player == '2':
        a = transpose
    
    # Identify the starting points for path checking, typically the first column for vertical connections.
    parents = [(j, 0) for j in range(len(a))]
    
    # Dictionary to track visited cells to avoid cycles and repeated work.
    visited = {}
    
    # Priority queue to efficiently explore the most promising paths first based on their scores.
    priorityQ = []
    
    # The board dimension (assuming square grid for simplicity).
    n = len(a)
    
    # Initialize the priority queue with cells from the first column, scoring them based on their state.
    for pair in parents:
        val = score(a[pair[0]][pair[1]], player)
        if a[pair[0]][pair[1]] == '0':
            visited[str(pair[0]) + str(pair[1])] = 1
            heappush(priorityQ, (1, str(pair[0]) + str(pair[1])))
        elif a[pair[0]][pair[1]] == player:
            visited[str(pair[0]) + str(pair[1])] = 0
            heappush(priorityQ, (0, str(pair[0]) + str(pair[1])))
    
    # Process each cell in the priority queue to find the best path.
    while priorityQ:
        parent = heappop(priorityQ)
        parentPos = parent[1]
        parentVal = parent[0]
        
        # Check if the current cell is on the far right column, which may indicate a winning path.
        if parentPos[1] == str(n - 1):
            return parentVal
        
        # Explore adjacent cells to continue the path.
        children = positions(int(parentPos[0]), int(parentPos[1]), n)
        for child in children:
            temp = score(a[child[0]][child[1]], player)
            if temp is not None:
                val = parentVal + temp
                # Update path scores and re-evaluate paths if a better score is found.
                if str(child[0]) + str(child[1]) not in visited.keys() or visited[str(child[0]) + str(child[1])] > val:
                    val = parentVal + score(a[child[0]][child[1]], player)
                    visited[str(child[0]) + str(child[1])] = val
                    heappush(priorityQ, (val, str(child[0]) + str(child[1])))

 
def minimax(a, d, player1, player2, start):
    """
    Implements the Minimax algorithm to determine the best move for the current player based on a recursive analysis of potential future game states.
    
    Args:
    a (list): Current state of the game board, a 2D list.
    d (int): Remaining depth of recursion the algorithm will explore.
    player1 (str): Marker for Player 1.
    player2 (str): Marker for Player 2.
    start (str): Marker for the player whose turn it is to move.

    Returns:
    tuple: A tuple containing the maximum score achievable and the best move's position as ('score', 'position').
    """
    # Evaluate the current board state for player2 using a heuristic function.
    h1 = h(a, player2)
    # Check if the heuristic value indicates a terminal state (win/lose) or no moves possible.
    if h1 == 0:
        # If the heuristic function returns 0 and it's player2's turn, player2 is in a winning position.
        if player2 == start:
            return 1000, '99'  # Return a high positive score indicating a win for player2.
        else:
            return -1000, '99'  # Return a high negative score indicating a loss for player2.
    
    # If the recursive depth limit has been reached, compare the heuristic evaluations of both players.
    if d <= 0:
        h2 = h(a, player1)
        return h1 - h2, '99'  # Return the difference in heuristic values as the score and '99' as a dummy position.

    # If the depth limit has not been reached, explore further moves.
    else:
        # Find all vacant places on the board to consider for future moves.
        seats = vacantPlaces(a)
        valList = OrderedDict()  # To store scores for each possible move.
        
        # Evaluate each possible move by simulating the move and recursively calling minimax.
        for pair in seats:
            x = ord(pair[0]) - 65  # Convert row character to index.
            y = int(pair[1])        # Column index.
            newA = list(map(list, a))  # Create a copy of the board.
            newA[x][y] = player1       # Make the move for player1.
            
            # Recursively call minimax to evaluate this potential board state.
            val, kkl = minimax(newA, d - 1, player2, player1, start)
            valList[str(x) + str(y)] = val  # Store the evaluated score for this move.
        
        # Determine the best move based on whether the function is maximizing or minimizing.
        if player1 is start:
            # If it's player1's turn, find the move with the maximum score.
            pos = sorted(valList.items(), key=lambda bla: bla[1], reverse=True)[0]
            maxVal = pos[1]
            return maxVal, pos[0]  # Return the score and position of the best move.
        else:
            # If it's not player1's turn, find the move with the minimum score (player1 is the adversary here).
            pos = sorted(valList.items(), key=lambda bla: bla[1])[0]
            minVal = pos[1]
            return minVal, pos[0]  # Return the score and position of the best move.
def start(a, n, d):
    # Initialize the game settings and window
    BOARD_SIZE = n  # Number of cells in one row or column
    WIDTH = (n + 2) * 50  # Window width, calculated to give padding around the grid
    HEIGHT = (n + 2) * 50  # Window height, same padding as width
    pygame.init()  # Initialize all imported Pygame modules
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set up the display window
    pygame.display.set_caption('HEX Player vs AI')  # Window title
    screen.fill(BG_COLOR)  # Fill the background with a predefined color
    
    draw_lines(screen, BOARD_SIZE)  # Draw grid lines on the board

    # Initialize player settings
    player1 = '1'  # Identifier for Player 1
    player2 = '2'  # Identifier for Player 2
    steps = OrderedDict()  # Tracks the sequence of moves
    player = 1  # Active player indicator, starting with Player 1
    game_over = False  # Flag to check if the game has ended

    # Main event loop
    while True:
        for event in pygame.event.get():  # Poll for any pending events
            if event.type == pygame.QUIT:  # Window close button clicked
                sys.exit()

            # Handle mouse button clicks
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]  # Get X coordinate of the mouse position
                mouseY = event.pos[1]  # Get Y coordinate of the mouse position
                x = int((mouseY - 50) // 50)  # Compute grid row index
                y = int((mouseX - 50) // 50)  # Compute grid column index

                # Check if the selected square is available
                if available_square(a, x, y):
                    a[x][y] = str(player1)  # Place the player's marker
                    player1, player2 = player2, player1  # Switch players
                    if(gameStatus(a, '1')):  # Check if the game is won
                        game_over = True
                        print("Player 1 Won!")
                    player = 2  # Next player's turn
                    draw_figures(screen, a, BOARD_SIZE)  # Redraw the board with updated markers

            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart(screen, a, BOARD_SIZE)  # Restart the game
                    start(a, n, d)  # Call start recursively to reinitialize the game

                if event.key == pygame.K_i:
                    val, pos = minimax(a, d, player1, player2, player1)  # Run minimax algorithm
                    x = int(pos[0])
                    y = int(pos[1])
                    a[x][y] = str(player1)  # Update the board with AI's chosen move
                    player1, player2 = player2, player1  # Switch turns
                    if(gameStatus(a, '2')):  # Check if AI's move won the game
                        game_over = True
                        print("Player 2 Won!")
                    player = 1  # Switch back to human player
                    draw_figures(screen, a, BOARD_SIZE)  # Redraw the board

        pygame.display.update()  # Update the display to show the new board state
def main():
    # Try block to handle input errors
    try:
        n = int(input("Enter the board size n: "))  # Input for board size
        d = int(input("Enter the level of the game d: "))  # Input for game difficulty/depth

        # Create an n x n board initialized to zero
        a = [['0' for _ in range(n)] for _ in range(n)]
        print("A new game board of size {}x{} has been created:".format(n, n))
        for row in a:
            print(" ".join(row))  # Print the initial state of the board

        start(a, n, d)  # Start the game

    except ValueError as e:  # Catch and print errors related to invalid input
        print("Invalid input! Please enter valid integers for board size and game level.")
    except Exception as e:  # Catch other exceptions
        print("An unexpected error occurred:", str(e))

if __name__ == "__main__":
    main()  # Execute the main function if the file is run as a script
