# Connect Four Game with Minimax and Alpha-Beta Pruning

This Python code implements a game of Connect Four, where two players take turns to drop their colored discs into a grid with the goal of being the first to connect four of their discs in a row, column, or diagonal. The game supports different modes: Player vs. Player, Player vs. AI, and AI vs. AI.

## Algorithms

**Minimax Algorithm:**
Minimax is a decision-making algorithm for two-player games. It aims to find the best strategy for a player while considering the opponent's optimal choices. This algorithm evaluates possible moves by recursively simulating the game, alternating between maximizing and minimizing players, to determine the most advantageous move.

**Alpha-Beta Pruning:**
Alpha-Beta pruning is an optimization technique often used with the Minimax algorithm. It helps reduce the search space in the game tree by maintaining two bounds, alpha and beta, representing the best achievable values for the maximizing and minimizing players. If a move is found that guarantees a score outside these bounds, that branch of the tree is pruned, saving computational resources while still finding the optimal move.

## Game Features

- **Dynamic Board Size**: You can specify the number of rows and columns for the game board.
- **Smart AI Opponent**: The AI player uses the Minimax algorithm with Alpha-Beta pruning to make decisions based on the current game state. It evaluates the best moves to win or prevent the opponent from winning.
- **Finishing Move Detection**: The game checks for a winning move in all directions (horizontal, vertical, and diagonal) and declares a winner when a player connects four discs.
- **Interactive GUI**: The game has a user-friendly graphical user interface built with the Pygame library, allowing players to interact with the board.

## How to Play

1. Run the code and choose a game mode (PvP, PvAI, or AIvAI).
2. If you choose PvAI or AIvAI, the AI player(s) will make strategic moves.
3. Click on a column to drop your disc into the desired position.
4. The game will declare a winner when a player connects four discs in a row, column, or diagonal, or it will end in a draw when the board is full.

## Customization

You can customize the game by changing the board size, adjusting AI difficulty by changing the depth of the Minimax algorithm, or modifying the evaluation function to make the AI smarter.

```python
BOARDHEIGHT = int(input("Enter the number of rows: "))  # Rows
BOARDWIDTH = int(input("Enter the number of columns: "))  # Columns

# Adjust the AI depth for Minimax
col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
```
