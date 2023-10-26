import numpy as np
import random, pygame, math, sys

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BOARDHEIGHT = int(input("enter number of rows: ")) # rows
BOARDWIDTH = int(input("enter number of columns: ")) # columns
entry = None
while entry != 1 and entry != 2 and entry != 3:
    entry = int(input("Please choose game mode:press 1 for P v P, 2 for P v AI, 3 for AI v Ai: "))
if entry == 1:
    AI1 = False
    AI2 = False
elif entry == 2:
    AI1 = False
    AI2 = True
elif entry == 3:
    AI1 = True
    AI2 = True
board = np.zeros((BOARDHEIGHT, BOARDWIDTH))
player1Tile = 1
player2Tile = 2
game_over = False
pygame.init()
SPACESIZE = min(int(800/BOARDWIDTH), int(700/BOARDHEIGHT))
RADIUS = int(SPACESIZE / 100 * 45)
WINDOWWIDTH = BOARDWIDTH * SPACESIZE
WINDOWHEIGHT = (BOARDHEIGHT) * SPACESIZE
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.update()
turn = random.randint(1, 2)

def available_row(board, column):
    # Returns number of the highest available row based on columns
    for row in range(BOARDHEIGHT):
        if board[row][column] == 0:
            return row

def best_reachable_score(board, tile):
    # Calculates best score according to available choices.
    score = 0
    if tile == player2Tile:
        opponent = player1Tile
    elif tile == player1Tile:
        opponent = player2Tile
    # More score for choosing center column because it may cause more winning choices in future.
    center_array = [int(i) for i in list(board[:, BOARDWIDTH // 2])]
    center_count = center_array.count(tile)
    score += center_count * 3
    # Horizontal
    for row in range(BOARDHEIGHT):
        row_array = [int(i) for i in list(board[row, :])]
        for column in range(BOARDWIDTH - 3):
            period = row_array[column:column + 4]
            if period.count(tile) == 4:
                score += 100
            elif period.count(tile) == 3 and period.count(0) == 1:
                score += 5
            elif period.count(tile) == 2 and period.count(0) == 2:
                score += 2
            # blocking opponent
            if period.count(opponent) == 3 and period.count(0) == 1:
                score -= 6
    # Vertical
    for column in range(BOARDWIDTH):
        col_array = [int(i) for i in list(board[:, column])]
        for row in range(BOARDHEIGHT - 3):
            period = col_array[row:row + 4]
            if period.count(tile) == 4:
                score += 100
            elif period.count(tile) == 3 and period.count(0) == 1:
                score += 5
            elif period.count(tile) == 2 and period.count(0) == 2:
                score += 2
            # blocking opponent
            if period.count(opponent) == 3 and period.count(0) == 1:
                score -= 6
    # + diagonal
    for row in range(BOARDHEIGHT - 3):
        for column in range(BOARDWIDTH - 3):
            period = [board[row + i][column + i] for i in range(4)]

            if period.count(tile) == 4:
                score += 100
            elif period.count(tile) == 3 and period.count(0) == 1:
                score += 5
            elif period.count(tile) == 2 and period.count(0) == 2:
                score += 2
            # blocking opponent
            if period.count(opponent) == 3 and period.count(0) == 1:
                score -= 6
    # - diagonal
    for row in range(BOARDHEIGHT - 3):
        for column in range(BOARDWIDTH - 3):
            period = [board[row + 3 - i][column + i] for i in range(4)]
            if period.count(tile) == 4:
                score += 100
            elif period.count(tile) == 3 and period.count(0) == 1:
                score += 5
            elif period.count(tile) == 2 and period.count(0) == 2:
                score += 2
            # blocking opponent
            if period.count(opponent) == 3 and period.count(0) == 1:
                score -= 6
    return score


def minimax(board, depth, alpha, beta, maximizer):
    available = []
    for column in range(BOARDWIDTH):
        if board[BOARDHEIGHT - 1][column] == 0:
            available.append(column)

    final = finishing_move(board, player1Tile) or finishing_move(board, player2Tile) or len(available) == 0
    if depth == 0 or final:
        if final:
            if finishing_move(board, player2Tile):
                return (None, 10000)
            elif finishing_move(board, player1Tile):
                return (None, -10000)
            else:  # Game is over
                return (None, 0)
        else:  # Depth is 0 and finally we can check the best available option at leaves
            return (None, best_reachable_score(board, player2Tile))

    if maximizer == True:
        value = -math.inf
        column = random.choice(available)
        for col in available:
            row = available_row(board, col)
            board_copy = board.copy()
            board_copy[row][col] = player2Tile
            new_score = minimax(board_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            # alpha beta pruning
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(available)
        for col in available:
            row = available_row(board, col)
            board_copy = board.copy()
            board_copy[row][col] = player1Tile
            new_score = minimax(board_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            # alpha beta pruning
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def greedy(board, tile):
    available = []
    for column in range(BOARDWIDTH):
        if board[BOARDHEIGHT - 1][column] == 0:
            available.append(column)
    best_score = 0
    best_col = random.choice(available)
    for col in available:
        row = available_row(board, col)
        temp_board = board.copy()
        temp_board[row][col] = tile
        score = best_reachable_score(temp_board, tile)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

def finishing_move(board, tile):
    # Horizontal check
    for column in range(BOARDWIDTH - 3):
        for row in range(BOARDHEIGHT):
            if board[row][column] == tile and board[row][column+1] == tile and board[row][column+2] == tile and board[row][column+3] == tile:
                return True
    # Vertical Check
    for column in range(BOARDWIDTH):
        for row in range(BOARDHEIGHT - 3):
            if board[row][column] == tile and board[row+1][column] == tile and board[row+2][column] == tile and board[row+3][column] == tile:
                return True
    # + diagonal check
    for column in range(BOARDWIDTH - 3):
        for row in range(BOARDHEIGHT - 3):
            if board[row][column] == tile and board[row+1][column+1] == tile and board[row+2][column+2] == tile and board[row+3][column+3] == tile:
                return True
    # - diagonal check
    for column in range(BOARDWIDTH - 3):
        for row in range(3, BOARDHEIGHT):
            if board[row][column] == tile and board[row-1][column+1] == tile and board[row-2][column+2] == tile and board[row-3][column+3] == tile:
                return True

def draw_board(board):
    for column in range(BOARDWIDTH):
        for row in range(BOARDHEIGHT):
            # Draws a blue background with white circles
            pygame.draw.rect(screen, BLUE, (column * SPACESIZE, row * SPACESIZE, SPACESIZE, SPACESIZE))
            pygame.draw.circle(screen, WHITE, (int(column * SPACESIZE + SPACESIZE / 2), int(row * SPACESIZE+ SPACESIZE / 2)), RADIUS)

    for column in range(BOARDWIDTH):
        for row in range(BOARDHEIGHT):
            # Draws red or yellow circles according to the matrix
            if board[row][column] == player1Tile:
                pygame.draw.circle(screen, RED, (int(column * SPACESIZE + SPACESIZE / 2), WINDOWHEIGHT - int(row * SPACESIZE + SPACESIZE / 2)), RADIUS)
            elif board[row][column] == player2Tile:
                pygame.draw.circle(screen, YELLOW, (int(column * SPACESIZE + SPACESIZE / 2), WINDOWHEIGHT - int(row * SPACESIZE + SPACESIZE / 2)), RADIUS)
    pygame.display.update()

draw_board(board)
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Player 1 without AI
            if turn == 1 and AI1 == False:
                posx = event.pos[0]
                col = int(math.floor(posx / SPACESIZE))
                if board[BOARDHEIGHT - 1][col] == 0:
                    row = available_row(board, col)
                    board[row][col] = player1Tile
                    if finishing_move(board, player1Tile):
                        game_over = True
                    turn += 1
                    draw_board(board)
            # Player 2 without AI
            elif turn == 2 and AI2 == False:
                posx = event.pos[0]
                col = int(math.floor(posx / SPACESIZE))
                if board[BOARDHEIGHT - 1][col] == 0:
                    row = available_row(board, col)
                    board[row][col] = player2Tile
                    if finishing_move(board, player2Tile):
                        game_over = True
                    turn -= 1
                    draw_board(board)

    # player 1 with AI
    if turn == 1 and AI1 == True and not game_over:
        #col = greedy(board, player1Tile)
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
        if board[BOARDHEIGHT - 1][col] == 0:
            row = available_row(board, col)
            board[row][col] = player1Tile
            if finishing_move(board, player1Tile):
                game_over = True
            draw_board(board)
            turn += 1

    # Player 2 with AI
    elif turn == 2 and AI2 == True and not game_over:
        #col = greedy(board, player2Tile)
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
        if board[BOARDHEIGHT - 1][col] == 0:
            row = available_row(board, col)
            board[row][col] = player2Tile
            if finishing_move(board, player2Tile):
                game_over = True
            draw_board(board)
            turn -= 1

while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        pygame.display.update()