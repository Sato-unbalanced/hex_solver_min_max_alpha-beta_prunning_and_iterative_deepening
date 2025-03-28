from termcolor import colored
import random
import copy
ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
		"Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

class Hex_Game:
	def __init__(self, board_size):
		self.board_size = board_size
		self.create_board()

	def create_board(self):
		self.hex_states = {}
		self.move_options = []
		for y in range(self.board_size):
			y_coord = str(y+1)
			self.hex_states[y_coord] = {}
			for x in range(self.board_size):
				x_coord = ALPHABET[x]
				self.hex_states[y_coord][x_coord] = "⬡"
				self.move_options.append((x_coord,y_coord))

	def reset_board(self):
		self.create_board()

	def _print_all_possible_moves(self):
		print("The possible moves are: " + str(self.move_options))

	def _print_played_moves(self):
		print("The played moves are: " + str(self.played_moves))

	def _print_current_round(self):
		print("The current round is: " + str(self.current_round))

	def _print_winner(self):
		print(self.current_player + " is the winner!!!!")

	def get_move_x_and_y(self, move):
		return move[0], move[1]

	def check_who_placed(self, move):
		move_x, move_y = self.get_move_x_and_y(move)
		hexagon = self.hex_states[move_y][move_x]
		return self.check_move(hexagon)

	def check_move(self, hexagon):
		if hexagon == "⬡":
			return "Neither"
		elif hexagon == colored("⬢", "blue"):
			return "P1"
		elif hexagon == colored("⬢", "red"):
			return "P2"

	def increment_x(self, x_value):
		return ALPHABET.index(x_value)+1
	
	def decrement_x(self, x_value):
		return ALPHABET.index(x_value)-1

	def index_x(self, x_value):
		return ALPHABET.index(x_value)
	
	def increment_y(self, y_value):
		return str(int(y_value) + 1)
	
	def decrement_y(self, y_value):
		return str(int(y_value) - 1)

	def is_valid_move(self, move_x, move_y):
		if move_x != -1 and move_x != self.board_size and move_y != "0" and move_y != str(self.board_size +1):
			return True
		return False

	def check_placement(self, move):
		who_placed  = self.check_who_placed(move)
		if who_placed == self.who_placed_first_move_in_sequence:
			return True
		return False

	def case_1(self, move_x, move_y):
		#case 1 above
		move_x = self.index_x(move_x)
		move_y = self.decrement_y(move_y)
		return move_x, move_y

	def case_2(self, move_x, move_y):
		#case 2 upper right
		move_x = self.increment_x(move_x)
		move_y = self.decrement_y(move_y)
		return move_x, move_y

	def case_3(self, move_x, move_y):
		#case 3 lower right
		move_x = self.increment_x(move_x)
		return move_x, move_y

	def case_4(self, move_x, move_y):
		#case 4 below
		move_x = self.index_x(move_x)
		move_y = self.increment_y(move_y)
		return move_x, move_y

	def case_5(self, move_x, move_y):
		#case 5 lower left
		move_x = self.decrement_x(move_x)
		move_y = self.increment_y(move_y)
		return move_x, move_y

	def case_6(self, move_x, move_y):
		#case 6 upper left
		move_x = self.decrement_x(move_x)
		return move_x, move_y


	def add_to_reachable(self, most_recent_move, all_reachable):
		#recursive function

		all_reachable.add(most_recent_move)
		most_recent_move_x = most_recent_move[0]
		most_recent_move_y = most_recent_move[1]

		for case in range(1,7):
			if case == 1:
				move_x, move_y = self.case_1(most_recent_move_x, most_recent_move_y)
			elif case == 2:
				move_x, move_y = self.case_2(most_recent_move_x, most_recent_move_y)
			elif case == 3:
				move_x, move_y = self.case_3(most_recent_move_x, most_recent_move_y)
			elif case == 4:
				move_x, move_y = self.case_4(most_recent_move_x, most_recent_move_y)
			elif case == 5:
				move_x, move_y = self.case_5(most_recent_move_x, most_recent_move_y)
			elif case == 6:
				move_x, move_y = self.case_6(most_recent_move_x, most_recent_move_y)

			move = (ALPHABET[move_x], move_y) 
			if move not in all_reachable and self.is_valid_move(move_x, move_y):
				to_add = self.check_placement(move)
				if to_add == True:
					self.add_to_reachable(move, all_reachable)


	def determine_if_winner(self, most_recent_move):
		#most recent move as ("A", 1) x,y
		all_reachable = set()

		self.who_placed_first_move_in_sequence = self.check_who_placed(most_recent_move)

		self.add_to_reachable(most_recent_move, all_reachable)
		#print(all_reachable)
	
		if self.current_player == "P1":
			x_coords = []
			for value in all_reachable:
				x_coords.append(value[0])
			unique_x_coords = set(x_coords)
			print(unique_x_coords)
			#if "A" in unique_x_coords and ALPHABET[self.board_size-1] in unique_x_coords:
			if len(unique_x_coords) == self.board_size:
				self.winner_exists = True
		
		
		elif self.current_player == "P2": 
			y_coords = []
			for value in all_reachable:
				y_coords.append(value[1])
			unique_y_coords = set(y_coords)
			print(unique_y_coords)
			#if "1" in unique_y_coords and str(self.board_size) in unique_y_coords:
			if len(unique_y_coords) == self.board_size:
				self.winner_exists = True
		

	def print_board(self):
		header = colored("".join(ALPHABET[:self.board_size]),"red")
		board = header+"\n"
		spacer = ""
		for key, value in self.hex_states.items():
			#print(key, "and", value)
			board += spacer
			board += colored(str(key), "blue")
			for key_2, value_2 in self.hex_states[key].items():
				board += value_2
			board += colored(str(key), "blue")
			board += "\n"
			if int(key) != 9:
				spacer += " "
		board += spacer + header
		print(board)
	

	def get_move(self):
		#can take as A,1  or A1 or a,1 or a1
		move = input(self.current_player + " pick a move: ")
		
		if "," in move:
			move = tuple(move.split(","))
		else:
			move = (move[0], move[1])
		move = (move[0].upper(), move[1])
		while move not in self.move_options:
			move = input("Pick a new move: ")
			if "," in move:
				move = tuple(move.split(","))
			else:
				move = (move[0], move[1])
			move = (move[0].upper(), move[1])
		return move

	def random_move(self):
		move = random.choice(self.move_options)
		#print("The move:", move)
		return move

	def player_move(self, move):
		move_x = move[0]
		move_y = move[1]
		if self.current_player == "P1":
			self.hex_states[move_y][move_x] = colored("⬢", "blue")
		elif self.current_player == "P2":
			self.hex_states[move_y][move_x] = colored("⬢", "red")

		self.print_board()
		#print(move)
		#self._print_all_possible_moves()
		self.move_options.remove(move)
		self.played_moves.add(move)


	def swap_current_player(self):
		if self.current_player == "P2":
			self.current_player = "P1"
		else:
			self.current_player = "P2"

	def player_actions(self, move_func):
		move = move_func()
		self.player_move(move)
		self.evaluate()
		self.determine_if_winner(move)
		self.swap_current_player()


	def swap_move_func(self, move_func, p1_move_func, p2_move_func):
		if move_func == p2_move_func:
			move_func = p1_move_func
		else:
			move_func = p2_move_func
		return move_func

	def game(self, p1_move_func, p2_move_func):
		self.current_round = 0
		self.played_moves = set()
		self.winner_exists = False
		self.current_player = "P1"
		move_func = p1_move_func

		while self.winner_exists == False:
			self.player_actions(move_func)
		
			if self.winner_exists:
				self._print_winner()
				return self.current_player

			move_func = self.swap_move_func(move_func, p1_move_func, p2_move_func)
			self.current_round += 0.5
			
	def play_game(self):
		#player one wins if line left to right and player two if line top to bottom
		self.game(self.get_move, self.get_move)		

	def simulation(self):
		self.game(self.random_move, self.random_move)	

	def get_segments(self):
		played_moves = copy.deepcopy(self.played_moves)
		#key is initial move of segment
		segments = {}
		for move in self.played_moves:
			if move in played_moves:
				all_reachable = copy.deepcopy(set())
				self.who_placed_first_move_in_sequence = self.check_who_placed(move)
				self.add_to_reachable(move, all_reachable)
				for reachable_move in all_reachable:
					played_moves.remove(reachable_move)

				segments[move] = copy.deepcopy(all_reachable)
		return segments

	def get_player_segment_lengths(self, segments):
		player_segments_lengths = {"P1": {}, "P2": {}}
		for key in segments.keys():
			player = self.check_who_placed(key)
			if player == "P1":
				x_coords = []
				for value in segments[key]:
					x_coords.append(value[0])
				unique_x_coords = set(x_coords)
				player_segments_lengths["P1"][key] = len(unique_x_coords)
				
			elif player == "P2":
				y_coords = []
				for value in segments[key]:
					y_coords.append(value[1])
				unique_y_coords = set(y_coords)
				player_segments_lengths["P2"][key] = len(unique_y_coords)
		return player_segments_lengths
		

	def evaluate_lengths(self, player_segments_lengths):
		player_totals = {"P1":0, "P2":0}
		for key in player_segments_lengths.keys():
			for value in player_segments_lengths[key].values():
				player_totals[key] += value * value
		print("Totals: ", player_totals)
		return player_totals

	def evaluate(self):
		segments = self.get_segments()
		player_segments_lengths  = self.get_player_segment_lengths(segments)
		totals = self.evaluate_lengths(player_segments_lengths)
		return totals


if __name__ == "__main__":
	hex = Hex_Game(5)
	hex.simulation()
	hex.reset_board()
	hex.play_game()
