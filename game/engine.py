import time
import json
import sys

sys.path.append('C:/Users/moner/Documents/Projekty/lab08/')

from game.utils import is_adjacent, valid_moves, print_board

class ShishimaGame:
    def __init__(self):
        self.scores = {'X': 0, 'O': 0}
        self.initialize_game()

    def initialize_game(self):
        self.board = [' ' for _ in range(9)]
        self.board[4] = ' '  
        self.positions = {'X': [], 'O': []}
        self.current_turn = 0
        self.players = ['X', 'O']

    def save_game(self):
        game_state = {
            'board': self.board,
            'positions': self.positions,
            'current_turn': self.current_turn
        }
        with open('C:/Users/moner/Documents/Projekty/lab08/save/shishima_game_save.json', 'w') as file:
            json.dump(game_state, file)
        print("Game saved successfully!")

    def load_game(self, filename):
        with open(filename, 'r') as file:
            game_state = json.load(file)
        self.board = game_state['board']
        self.positions = game_state['positions']
        self.current_turn = game_state['current_turn']
        print("Game loaded successfully!")

    def set_pawns(self, player, positions):
        for pos in positions:
            if pos == 4 or pos not in range(9) or self.board[pos] != ' ':
                print("Invalid position, please try again.")
                continue
            elif len(self.positions[player]) > 0 and not any(is_adjacent(pos, existing) for existing in self.positions[player]):
                print("Invalid position, pawns must be adjacent to at least one other. Try again.")
                continue
            else:
                self.board[pos] = player
                self.positions[player].append(pos)

    def move_pawns(self, player, start, end):
        if player not in self.positions:
            raise ValueError(f"Player {player} does not exist")
        movable_pawns = {pos: valid_moves(pos, self.board) for pos in self.positions[player] if valid_moves(pos, self.board)}
        
        if not movable_pawns:
            print("No moves available for any pawns. Skipping turn.")
            return
        if start in movable_pawns:
            print("Valid moves:", movable_pawns[start])
            if end in movable_pawns[start]:
                self.board[start] = ' '
                self.board[end] = player
                self.positions[player].remove(start)
                self.positions[player].append(end)
                self.save_game()
            else:
                print("Invalid move, try again.")
        else:
            print("Not your pawn or no moves available, try again.")

    def check_win(self, player):
        lines = [[0, 4, 8], [2, 4, 6], [1, 4, 7], [3, 4, 5]]
        for line in lines:
            if all(self.board[pos] == player for pos in line):
                self.scores[player] += 1
                return True
        return False

    def play_game(self):
        self.set_pawns()
        game_over = False
        while not game_over:
            current_player = self.players[self.current_turn % 2]
            if any(valid_moves(pos, self.board) for pos in self.positions[current_player]):
                self.move_pawn(current_player)
                if self.check_win(current_player):
                    print_board(self.board)
                    print(f"Player {current_player} wins! Current score: X={self.scores['X']}, O={self.scores['O']}")
                    play_again = input("Do you want to play again? (yes/no): ").lower()
                    if play_again == 'yes':
                        self.initialize_game()
                        self.set_pawns()
                    else:
                        game_over = True
            else:
                print(f"No moves available for {current_player}. Skipping turn.")
                time.sleep(2)
            self.current_turn += 1
