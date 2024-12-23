# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 20:56:02 2024

@author: axelf
"""

import tkinter as tk
import random
import copy as deepcopy_module
import math

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

#represent each state of the game board
class MCTSNode:
    def __init__(self, board, parent=None):
        self.board = board
        self.parent = parent
        self.children = {}
        self.wins = 0
        self.visits = 0

    def is_fully_expanded(self):
        return len(self.children) == 4  # 4 possible moves (up, down, left, right)

    def get_untried_moves(self):
        possible_moves = ['up', 'down', 'left', 'right']
        return [move for move in possible_moves if move not in self.children]

    def best_child(self, c_param=1.4):
        # UCB1 formula: win rate + exploration parameter * sqrt(ln(total visits) / node visits)
        choices_weights = [
            (child.wins / child.visits) + c_param * math.sqrt(math.log(self.visits) / child.visits)
            for child in self.children.values()
        ]
        return list(self.children.values())[choices_weights.index(max(choices_weights))]


#handle the search algorithm
class MCTS:
    def __init__(self, board, iterations=1000):
        self.root = MCTSNode(board)
        self.iterations = iterations

    def best_move(self):
        for _ in range(self.iterations):
            node = self.select(self.root)
            if node.visits == 0:
                result = self.simulate(node.board)
            else:
                node = self.expand(node)
                result = self.simulate(node.board)
            self.backpropagate(node, result)
        return max(self.root.children, key=lambda move: self.root.children[move].wins)

    def select(self, node):
        while node.is_fully_expanded():
            node = node.best_child()
        return node

    def expand(self, node):
        move = random.choice(node.get_untried_moves())
        new_board = self.get_next_state(node.board, move,score)
        child_node = MCTSNode(new_board, parent=node)
        node.children[move] = child_node
        return child_node

    def simulate(self, board):
        sim_board = deepcopy_module.deepcopy(board)
        sim_score = 0  # Local score variable for simulation
        while not self.is_terminal(sim_board):
            move = random.choice(['up', 'down', 'left', 'right'])
            sim_board, sim_score = self.get_next_state(sim_board, move, sim_score)
        return sim_score


    def backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent

    # Helper function to get the board after applying a move
    def get_next_state(self, board, move, score):
        new_board = deepcopy_module.deepcopy(board)
        if move == 'up':
            new_board, score = move_up(new_board, score)
        elif move == 'down':
            new_board, score = move_down(new_board, score)
        elif move == 'left':
            new_board, score = move_left(new_board, score)
        elif move == 'right':
            new_board, score = move_right(new_board, score)
        return new_board, score


    # Function to determine if a board state is terminal (no moves left or 2048 achieved)
    def is_terminal(self, board):
        return is_game_over(board) or any(2048 in row for row in board)

    # Function to calculate the score based on the board (sum of tiles, etc.)
    def get_score(self,board):
        return sum(sum(row) for row in board)  # Use Python's built-in sum function


#move function with an AI-driven approach

def ai_play(board, iterations=1000):
    mcts = MCTS(board, iterations=iterations)
    best_move = mcts.best_move()

    # Apply the best move to the game board
    if best_move == 'up':
        move_up(board)
    elif best_move == 'down':
        move_down(board)
    elif best_move == 'left':
        move_left(board)
    elif best_move == 'right':
        move_right(board)



def play_game_with_ai(board, iterations=200):
    while not is_game_over(board):
        ai_play(board, iterations)
        add_new_tile(board)  # Add a new tile after AI moves



# Initialize score
score = 0

# Initialize the board with two tiles
def initialize_board():
    board = [[0] * 4 for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)
    return board

# Add a new tile to an empty cell
def add_new_tile(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

# Update the grid based on the current board state
def update_grid_gui(board, grid_labels,score_label):
    global score
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value == 0:
                grid_labels[i][j].config(text="", bg="#cdc1b4")
            else:
                grid_labels[i][j].config(text=str(value), bg=get_tile_color(value))
    score_label.config(text="Score: " + str(score))

def get_tile_color(value):
    tile_colors = {
        2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
        32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
        512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
    }
    return tile_colors.get(value, "#cdc1b4")  # Default color


# Define movement functions

# Helper to compress the tiles (move them to one side without merging)
def compress(board):
    new_board = [[0] * 4 for _ in range(4)]
    for i in range(4):
        position = 0
        for j in range(4):
            if board[i][j] != 0:
                new_board[i][position] = board[i][j]
                position += 1
    return new_board

def merge(board, score):
    new_board = [row[:] for row in board]  # Copy board to avoid unintended changes
    for i in range(4):
        for j in range(3):
            if new_board[i][j] == new_board[i][j + 1] and new_board[i][j] != 0:
                new_board[i][j] *= 2
                score += new_board[i][j]  # Add merged value to score
                new_board[i][j + 1] = 0
    return new_board, score

def move_left(board, score):
    if  isinstance(board, tuple):
        board, score = board
    new_board  = compress(board)
    new_board , score = merge(new_board , score)
    new_board  = compress(new_board )
    return new_board , score


def move_right(board, score):
    if  isinstance(board, tuple):
        board, score = board
    new_board  = [row[::-1] for row in board]  # Reverse the rows
    new_board , score = move_left(new_board , score)
    new_board  = [row[::-1] for row in new_board ]  # Reverse the rows back
    return new_board , score

def move_up(board, score):
    if  isinstance(board, tuple):
        board, score = board
    new_board  = list(map(list, zip(*board)))  # Transpose the board
    new_board, score = move_left(new_board , score)
    new_board  = list(map(list, zip(*new_board )))  # Transpose back
    return new_board , score

def move_down(board, score):
    if  isinstance(board, tuple):
        board, score = board
    new_board  = list(map(list, zip(*board)))  # Transpose the board
    new_board , score = move_right(new_board , score)
    new_board  = list(map(list, zip(*new_board )))  # Transpose back
    return new_board , score


# Check if any moves are available
def is_game_over(board):
    if not isinstance(board, list):
        print("Error: board is not a 2D list:", board)
        return True  # Treat it as game over if board is invalid

    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
            if i < 3 and board[i][j] == board[i + 1][j]:
                return False
            if j < 3 and board[i][j] == board[i][j + 1]:
                return False
    return True

# Function for AI-controlled gameplay with GUI update
def ai_play_with_gui(board, grid_labels, root, score_label, iterations=1000):
    global score
    
    mcts = MCTS(board, iterations=iterations)
    best_move = mcts.best_move()

    if best_move == 'up':
        board, score = move_up(board, score)
    elif best_move == 'down':
        board, score = move_down(board, score)
    elif best_move == 'left':
        board, score = move_left(board, score)
    elif best_move == 'right':
        board, score = move_right(board, score)

    add_new_tile(board)
    print("Board after move:", board)  # Debug print
    update_grid_gui(board, grid_labels, score_label)

    # If game is not over, repeat the AI move with delay
    if not is_game_over(board):
        root.after(50, ai_play_with_gui, board, grid_labels, root, score_label)
    else:
        print("Game Over! Final Score:", score)
        root.destroy()  # Close the window when the game is over

# Function to run the game with AI in Tkinter GUI
def run_ai_game_gui():
    global score
    root = tk.Tk()
    root.title("2048 AI")
    root.geometry("400x400")
    root.config(bg="#bbada0")

    # Initialize board and GUI labels
    board = initialize_board()
    grid_labels = [[None] * 4 for _ in range(4)]
    # Score Label (Updated)
    score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 16, "bold"), bg="#bbada0", fg="#f9f6f2")
    score_label.grid(row=0, column=0, columnspan=4, pady=(10, 20))  # Increased bottom padding
    
    # Create grid for board
    for i in range(4):
        for j in range(4):
            label = tk.Label(root, text="", width=4, height=2,
                             font=("Helvetica", 24, "bold"), bg="#cdc1b4", relief="solid", borderwidth=2)
            label.grid(row=i + 1, column=j, padx=5, pady=5)  # Game grid starts from row 1
            grid_labels[i][j] = label


    update_grid_gui(board, grid_labels,score_label)

    # Start AI gameplay
    root.after(50, ai_play_with_gui, board, grid_labels, root, score_label)
    root.mainloop()
    
#Run a game with the graphic interface
#run_ai_game_gui()

#Loop multiple game
def run_multiple_games(num_games, iterations=1000):
    global score
    scores = []  # List to store the scores of all games

    for game in range(num_games):
        # Initialize the board and score for each game
        board = initialize_board()
        score = 0

        # Run the game until it ends
        while not is_game_over(board):
            mcts = MCTS(board, iterations=iterations)
            best_move = mcts.best_move()

            if best_move == 'up':
                board, score = move_up(board, score)
            elif best_move == 'down':
                board, score = move_down(board, score)
            elif best_move == 'left':
                board, score = move_left(board, score)
            elif best_move == 'right':
                board, score = move_right(board, score)

            add_new_tile(board)  # Add a new tile after AI makes a move

        # Store the final score of the game
        scores.append(score)
        print(f"Game {game + 1}/{num_games} finished. Final Score: {score}")

    # Print summary of results
    print("\nSummary of Results:")
    for idx, game_score in enumerate(scores):
        print(f"Game {idx + 1}: {game_score}")
    print(f"Average Score: {sum(scores) / len(scores):.2f}")

# Run the loop for multiple games (without interface)
run_multiple_games(num_games=50, iterations=200)  # Adjust num_games as needed



