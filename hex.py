from termcolor import colored     #pip install termcolor
import tkinter as tk  #if not installed with python sudo apt-get install python3-tk for Ubuntu

# modules below part of Python Standard Library
import random			
import copy
from functools import partial
import math
from fractions import Fraction
import time

ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
		"Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

class HexGame:

	"""
	Representation of HexGame.
	...

	Attributes
	----------
	board_size : int
		Size of board
	hex_states : dictionary
		state of board
	move_options: list
		moves player can choose from
	who_placed_first_move_in_sequence: str
		player which placed first move in sequence
	current_round: float
		current round
    	played_moves: set
		moves already played
	winner_exists: boolean
		if winner exists
	current_player: str
		current player's turn
	"""

	def __init__(self, board_size=5):

		"""
		Initializes the HexGame class.

		Parameter
		---------
		self : class object
			Hex Game
		board_size : int
			size of board (defaults to 5)

		Returns
		-------
		None
		"""

		self.board_size = board_size
		self.create_board()

	def create_board(self):

		"""
		Creates the game board and initializes hex_states and generates move_options

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""

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

		"""
		Resets the game board and resets hex_states and regenerates move_options

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""

		self.create_board()

	def _print_all_possible_moves(self):

		"""
		Prints all possible moves

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""
		print("The possible moves are: " + str(self.move_options))

	def _print_played_moves(self):
		"""
		Prints all played moves

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""
		print("The played moves are: " + str(self.played_moves))

	def _print_total_played_moves(self):
		"""
		Prints number of moves played

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""
		print("The number of played moves are: " + str(len(self.played_moves)))

	def _print_current_round(self):
		"""
		Prints current round

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""
		print("The current round is: " + str(self.current_round))

	def _print_winner(self):
		"""
		Prints the winner of game

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""
		print(self.current_player + " is the winner!!!!")

	def get_move_x_and_y(self, move):

		"""
		Gets the x and y of move from tuple

		Parameter
		---------
		self : class object
			Hex Game
		move: tuple
			move played

		Returns
		-------
		move[0]: str
			x of move (Letter)
		move[1]: str
			y of move (Number)
		"""

		return move[0], move[1]

	def check_who_placed(self, move):

		"""
		Checks who placed the move

		Parameter
		---------
		self : class object
			Hex Game
		move: tuple
			move played

		Returns
		-------
		self.check_move(hexagon): str
			player who played move
		"""

		move_x, move_y = self.get_move_x_and_y(move)
		hexagon = self.hex_states[move_y][move_x]
		return self.check_move(hexagon)

	def check_move(self, hexagon):

		"""
		Checks hexagon for which player it belongs to

		Parameter
		---------
		self : class object
			Hex Game
		hexagon: str
			hexagon value

		Returns
		-------
		"Neither" or "P1" or "P2" : str
			player hexagon belongs to
		"""

		if hexagon == "⬡":
			return "Neither"
		elif hexagon == colored("⬢", "blue"):
			return "P1"
		elif hexagon == colored("⬢", "red"):
			return "P2"

	def increment_x(self, x_value):

		"""
		Increments x index by one

		Parameter
		---------
		self : class object
			Hex Game
		x_value: str
			letter of move

		Returns
		-------
		next letter in ALPHABET index
		"""

		return ALPHABET.index(x_value)+1
	
	def decrement_x(self, x_value):

		"""
		Deincrements x index by one

		Parameter
		---------
		self : class object
			Hex Game
		x_value: str
			letter of move

		Returns
		-------
		previous letter in ALPHABET index
		"""
		return ALPHABET.index(x_value)-1

	def index_x(self, x_value):

		"""
		gets x index

		Parameter
		---------
		self : class object
			Hex Game
		x_value: str
			letter of move

		Returns
		-------
		current letter in ALPHABET index
		"""

		return ALPHABET.index(x_value)
	
	def increment_y(self, y_value):

		"""
		increments y index by one

		Parameter
		---------
		self : class object
			Hex Game
		y_value: str
			number of move

		Returns
		-------
		str(int(y_value) + 1): str
			value + 1 as a string
		"""

		return str(int(y_value) + 1)
	
	def decrement_y(self, y_value):

		"""
		deincrements y index by one

		Parameter
		---------
		self : class object
			Hex Game
		y_value: str
			number of move

		Returns
		-------
		str(int(y_value) - 1): str
			value - 1 as a string
		"""
		return str(int(y_value) - 1)

	def is_valid_move(self, move_x, move_y):

		"""
		Checks if move is valid

		Parameter
		---------
		self : class object
			Hex Game
		move_x: int
			x index
		move_y: str
			y move

		Returns
		-------
		True or False: boolean
			depending if move is valid
		"""

		if move_x != -1 and move_x != self.board_size and move_y != "0" and move_y != str(self.board_size +1):
			return True
		return False

	def check_placement(self, move):

		"""
		Checks if who placed is same as player who started sequence

		Parameter
		---------
		self : class object
			Hex Game
		move: tuple

		Returns
		-------
		True or False: boolean
			depending if player is same 
		"""

		who_placed  = self.check_who_placed(move)
		if who_placed == self.who_placed_first_move_in_sequence:
			return True
		return False

	def case_1(self, move_x, move_y):

		"""
		Returns move above

		Parameter
		---------
		self : class object
			Hex Game
		move_x: str
			x_move
		move_y: str
			y_move

		Returns
		-------
		move_x: str
			new move_x
		move_y: str
			new move_y
		"""

		#case 1 above
		move_x = self.index_x(move_x)
		move_y = self.decrement_y(move_y)
		return move_x, move_y

	def case_2(self, move_x, move_y):

		"""
		Returns move upper right

		Parameter
		---------
		self : class object
			Hex Game
		move_x: str
			x_move
		move_y: str
			y_move

		Returns
		-------
		move_x: str
			new move_x
		move_y: str
			new move_y
		"""

		#case 2 upper right
		move_x = self.increment_x(move_x)
		move_y = self.decrement_y(move_y)
		return move_x, move_y

	def case_3(self, move_x, move_y):

		"""
		Returns move lower right

		Parameter
		---------
		self : class object
			Hex Game
		move_x: str
			x_move
		move_y: str
			y_move

		Returns
		-------
		move_x: str
			new move_x
		move_y: str
			new move_y
		"""

		#case 3 lower right
		move_x = self.increment_x(move_x)
		return move_x, move_y

	def case_4(self, move_x, move_y):

		"""
		Returns move below

		Parameter
		---------
		self : class object
			Hex Game
		move_x: str
			x_move
		move_y: str
			y_move

		Returns
		-------
		move_x: str
			new move_x
		move_y: str
			new move_y
		"""

		#case 4 below
		move_x = self.index_x(move_x)
		move_y = self.increment_y(move_y)
		return move_x, move_y

	def case_5(self, move_x, move_y):

		"""
		Returns move lower left

		Parameter
		---------
		self : class object
			Hex Game
		move_x: str
			x_move
		move_y: str
			y_move

		Returns
		-------
		move_x: str
			new move_x
		move_y: str
			new move_y
		"""

		#case 5 lower left
		move_x = self.decrement_x(move_x)
		move_y = self.increment_y(move_y)
		return move_x, move_y

	def case_6(self, move_x, move_y):

		"""
		Returns move upper left

		Parameter
		---------
		self : class object
			Hex Game
		move_x: str
			x_move
		move_y: str
			y_move

		Returns
		-------
		move_x: str
			new move_x
		move_y: str
			new move_y
		"""

		#case 6 upper left
		move_x = self.decrement_x(move_x)
		return move_x, move_y


	def add_to_reachable(self, most_recent_move, all_reachable, include_blanks):

		"""
		Adds to all_reachable if valid

		Parameter
		---------
		self : class object
			Hex Game
		most_recent_move: tuple
			most recent move
		all_reachable: set
			set of all reachable from move
		include_blanks: boolean
			whether to include moves by neither player

		Returns
		-------
		None
		"""

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
				if to_add == True or (include_blanks == True and move in self.move_options):
					self.add_to_reachable(move, all_reachable, include_blanks)
		

	def determine_if_winner(self, most_recent_move):

		"""
		Determines if winner based on move

		Parameter
		---------
		self : class object
			Hex Game
		most_recent_move: tuple
			most recent move

		Returns
		-------
		True or False: boolean
			depending on if move caused player to win
		"""

		#most recent move as ("A", 1) x,y
		all_reachable = set()

		self.who_placed_first_move_in_sequence = self.check_who_placed(most_recent_move)

		self.add_to_reachable(most_recent_move, all_reachable, False)
	
		if self.current_player == "P1":
			x_coords = []
			for value in all_reachable:
				x_coords.append(value[0])
			unique_x_coords = set(x_coords)

			#if "A" in unique_x_coords and ALPHABET[self.board_size-1] in unique_x_coords:
			if len(unique_x_coords) == self.board_size:
				#print(all_reachable)
				return True
		
		
		elif self.current_player == "P2": 
			y_coords = []
			for value in all_reachable:
				y_coords.append(value[1])
			unique_y_coords = set(y_coords)

			#if "1" in unique_y_coords and str(self.board_size) in unique_y_coords:
			if len(unique_y_coords) == self.board_size:
				#print(all_reachable)
				return True
		return False

	def print_board(self):

		"""
		Prints game board

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""

		header = colored("".join(ALPHABET[:self.board_size]),"red")
		board = header+"\n"
		spacer = ""
		for key, value in self.hex_states.items():
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

		"""
		Gets move from user

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		move: tuple
			move player inputted
		"""

		#can take as A,1  or A1 or a,1 or a1
		move = input(self.current_player + " pick a move: ")
		
		if "," in move:
			move = tuple(move.split(","))
		else:
			move = (move[0], move[1:])
		move = (move[0].upper(), move[1])
		while move not in self.move_options:
			move = input("Pick a new move: ")
			if "," in move:
				move = tuple(move.split(","))
			else:
				move = (move[0], move[1:])
			move = (move[0].upper(), move[1])
		return move

	def random_move(self):
		"""
		Gets random move from move options

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		move: tuple
			move chosen
		"""

		move = random.choice(self.move_options)
		return move

	def undo_move(self, move):

		"""
		Undos move played

		Parameter
		---------
		self : class object
			Hex Game
		move: tuple
			move played

		Returns
		-------
		None
		"""

		move_x = move[0]
		move_y = move[1]
		self.hex_states[move_y][move_x] = "⬡"
		self.move_options.append(move)
		self.played_moves.remove(move)

	def player_move(self, move):

		"""
		Does player move

		Parameter
		---------
		self : class object
			Hex Game
		move : tuple
			move to be played
		Returns
		-------
		None
		"""

		move_x = move[0]
		move_y = move[1]
		if self.current_player == "P1":
			self.hex_states[move_y][move_x] = colored("⬢", "blue")
		elif self.current_player == "P2":
			self.hex_states[move_y][move_x] = colored("⬢", "red")

		self.move_options.remove(move)
		self.played_moves.add(move)


	def swap_current_player(self):

		"""
		Swaps current player

		Parameter
		---------
		self : class object
			Hex Game
		Returns
		-------
		None
		"""

		if self.current_player == "P2":
			self.current_player = "P1"
		else:
			self.current_player = "P2"

	def player_actions(self, move_func):

		"""
		Does player actions based on move_func

		Parameter
		---------
		self : class object
			Hex Game
		move_func : function
			function to get move
		Returns
		-------
		None
		"""

		move = move_func()
		self.do_actions(move)

	def do_actions(self, move):

		"""
		Does player actions based on move

		Parameter
		---------
		self : class object
			Hex Game
		move : tuple
			move to be played
		Returns
		-------
		None
		"""

		self.player_move(move)
		self.print_board()
		self.winner_exists = self.determine_if_winner(move)
		if self.winner_exists == False:
			self.swap_current_player()

	def swap_move_func(self, move_func, p1_move_func, p2_move_func):

		"""
		Does player actions based on move_func

		Parameter
		---------
		self : class object
			Hex Game
		move_func : function
			function to get move
		p1_move_func : function
			player 1 function to get move
		p2_move_func : function
			player 2 function to get move

		Returns
		-------
		move_func : function
			new move_func
		"""

		if move_func == p2_move_func:
			move_func = p1_move_func
		else:
			move_func = p2_move_func
		return move_func

	def game(self, p1_move_func, p2_move_func):

		"""
		Allows game to be played text_based

		Parameter
		---------
		self : class object
			Hex Game
		p1_move_func : function
			player 1 function to get move
		p2_move_func : function
			player 2 function to get move

		Returns
		-------
		self.current_player: str
			player who won
		"""

		self.current_round = 0
		self.played_moves = set()
		self.winner_exists = False
		self.current_player = "P1"
		move_func = p1_move_func

		while self.winner_exists == False:
			self.player_actions(move_func)
		
			if self.winner_exists:
				self._print_winner()
				self.reset_board()
				return self.current_player

			move_func = self.swap_move_func(move_func, p1_move_func, p2_move_func)
			self.current_round += 0.5
			
	def play_game(self):

		"""
		Allows game to be played person vs person

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""

		#player one wins if line left to right and player two if line top to bottom
		self.game(self.get_move, self.get_move)		

	def as_p1(self):

		"""
		Allows game to be played person vs ai

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""

		self.game(self.get_move, partial(self.abp_id, 1))	
			
	def as_p2(self):

		"""
		Allows game to be played ai vs person

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""

		self.game(partial(self.abp_id, 1), self.get_move)

	def simulation(self):

		"""
		Allows game to be played ai vs ai

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""

		#can change
		self.game(partial(self.abp_id,1), partial(self.abp_id,1))	

	def get_segments(self):

		"""
		Gets segments on board

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		segments: dictionary
			connected segments for each move
		segments_with_blanks: dictionary
			connected segments for each move including blanks
		"""

		played_moves = copy.deepcopy(self.played_moves)
		segments = {}
		segments_with_blanks = {}
		for move in self.played_moves:
			if move in played_moves:
				all_reachable = copy.deepcopy(set())
				all_reachable_blanks = copy.deepcopy(set())
				self.who_placed_first_move_in_sequence = self.check_who_placed(move)
				self.add_to_reachable(move, all_reachable, False)
				self.add_to_reachable(move, all_reachable_blanks, True)
				for reachable_move in all_reachable:
					played_moves.remove(reachable_move)

				segments[move] = copy.deepcopy(all_reachable)
				segments_with_blanks[move] = copy.deepcopy(all_reachable_blanks)
		return segments, segments_with_blanks 

	def get_player_segment_lengths(self, segments, segments_with_blanks):

		"""
		Gets segments lengths

		Parameter
		---------
		self : class object
			Hex Game
		segments: dictionary
			connected segments for each move
		segments_with_blanks: dictionary
			connected segments for each move including blanks

		Returns
		-------
		player_segments_lengths: dictionary
			by player gets segment lengths of winning direction
		full_player_lengths: dictionary
			by player gets total segment lengths
		player_segments_lengths_blanks: dictionary
			by player gets segment lengths of winning direction with blanks
		"""

		player_segments_lengths = {"P1": {}, "P2": {}}
		full_player_lengths = {"P1": {}, "P2": {}}
		for key in segments.keys():
			player = self.check_who_placed(key)
			if player == "P1":
				x_coords = []
				for value in segments[key]:
					x_coords.append(value[0])
				unique_x_coords = set(x_coords)
				player_segments_lengths["P1"][key] = len(unique_x_coords)
				full_player_lengths["P1"][key] = len(segments[key])
				
			elif player == "P2":
				y_coords = []
				for value in segments[key]:
					y_coords.append(value[1])
				unique_y_coords = set(y_coords)
				player_segments_lengths["P2"][key] = len(unique_y_coords)
				full_player_lengths["P2"][key] = len(segments[key])
		player_segments_lengths_blanks = {"P1": {}, "P2": {}}

		for key in segments_with_blanks.keys():
			player = self.check_who_placed(key)
			if player == "P1":
				x_coords = []
				for value in segments_with_blanks[key]:
					x_coords.append(value[0])
				unique_x_coords = set(x_coords)
				player_segments_lengths_blanks["P1"][key] = len(unique_x_coords)
				
			elif player == "P2":
				y_coords = []
				for value in segments_with_blanks[key]:
					y_coords.append(value[1])
				unique_y_coords = set(y_coords)
				player_segments_lengths_blanks["P2"][key] = len(unique_y_coords)
		return player_segments_lengths, full_player_lengths, player_segments_lengths_blanks
		

	def evaluate_lengths(self, player_segments_lengths, full_player_lengths, player_segments_lengths_blanks):

		"""
		Evaluates lengths

		Parameter
		---------
		self : class object
			Hex Game
		player_segments_lengths: dictionary
			by player gets segment lengths of winning direction
		full_player_lengths: dictionary
			by player gets total segment lengths
		player_segments_lengths_blanks: dictionary
			by player gets segment lengths of winning direction with blanks

		Returns
		-------
		player_totals: dictionary
			player scores
		"""

		player_totals = {"P1":0, "P2":0}
		for key in player_segments_lengths.keys():
			for value_1, value_2, value_3 in zip(player_segments_lengths[key].values(), player_segments_lengths_blanks[key].values(), full_player_lengths[key].values()):
				if value_2 == self.board_size:
					player_totals[key] += value_1**2 + ((value_3 **2)/self.board_size)
		return player_totals

	def evaluate(self):

		"""
		Evaluates players scores

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		totals: dictionary
			player scores
		"""

		segments, segments_with_blanks = self.get_segments()
		player_segments_lengths, full_player_lengths, player_segments_lengths_blanks = self.get_player_segment_lengths(segments, segments_with_blanks)
		totals = self.evaluate_lengths(player_segments_lengths, full_player_lengths, player_segments_lengths_blanks)
		return totals

	def abp_start(self, depth):

		"""
		Alpha Beta Pruning AI initializes with heuristics

		Parameter
		---------
		self : class object
			Hex Game
		depth : int
			depth to search up to

		Returns
		-------
		best_move: tuple
			move chosen to be played
		"""

		self.original_player = self.current_player
		alpha = -math.inf
		beta = math.inf
		if depth > len(self.move_options):
			print("depth to big, setting to max")
			depth = len(self.move_options)
		v = -math.inf
		best_move = None
		middle = (1 + self.board_size)/2
		for move in copy.deepcopy(self.move_options):
			score = self.abp(depth-1, alpha, beta, move, False)
			x_value = self.index_x(move[0])+1
			y_value = int(move[1])
			x_distance = abs(x_value - middle)
			y_distance = abs(y_value - middle)
			if x_distance != 0:
				x_distance = Fraction(x_distance)
				x_distance = x_distance.denominator/x_distance.numerator
				x_distance = x_distance/100
			else:
				x_distance = self.board_size/100
			if y_distance != 0:
				y_distance = Fraction(y_distance)
				y_distance = y_distance.denominator/y_distance.numerator
				y_distance = y_distance/100
			else:
				y_distance = self.board_size/100
			if score < (25**4):
				score += (x_distance + y_distance)
				if self.original_player == "P1":
					score += y_distance
				elif self.original_player == "P2":
					score += x_distance
			if score > v:
				v = score
				best_move = move
			alpha = max(alpha, v)
		return best_move
				

	def abp(self, depth, alpha, beta, current_move, maximize):
		"""
		Alpha Beta Pruning AI

		Parameter
		---------
		self : class object
			Hex Game
		depth : int
			depth to search up to
		alpha : int
			alpha value
		beta : int
			beta value
		current_move: tuple
			move to check
		maximize: boolean
			whether to maximize or minimize

		Returns
		-------
		score or v: int
			value chosen
		"""

		if self.current_player == self.original_player:
			value = 25**4 + depth
		else:
			value = -(25**4) - depth
		if depth == 0:
			self.player_move(current_move)
			winner = self.determine_if_winner(current_move)

			if winner == True:
				score = value
			else:
				totals = self.evaluate()
				if self.original_player == "P1":
					score = totals["P1"] - totals["P2"]
				elif self.original_player == "P2":
					score = totals["P2"] - totals["P1"]
			self.undo_move(current_move)
			return score

		elif maximize == True:
			self.player_move(current_move)
			winner = self.determine_if_winner(current_move)
			if winner == True:
				score = value
				self.undo_move(current_move)
				return score
			self.swap_current_player()
			v = -math.inf
			for move in copy.deepcopy(self.move_options):
				score = self.abp(depth-1, alpha, beta, move, False)
				v = max(v, score)
				if v >= beta:
					self.undo_move(current_move)
					self.swap_current_player()
					return v
				alpha = max(alpha, v)
			self.undo_move(current_move)
			self.swap_current_player()

		elif maximize == False:
			self.player_move(current_move)
			winner = self.determine_if_winner(current_move)
			if winner == True:
				score = value
				self.undo_move(current_move)
				return score
			self.swap_current_player()
			v = math.inf
			for move in copy.deepcopy(self.move_options):
				score = self.abp(depth-1, alpha, beta, move, True)
				v = min(v, score)
				if v <= alpha:
					self.undo_move(current_move)
					self.swap_current_player()
					return v
				beta = min(beta, v)

			self.undo_move(current_move)
			self.swap_current_player()
		return v


	def abp_id(self, seconds):

		"""
		Alpha Beta Pruning AI with iterative deepening

		Parameter
		---------
		self : class object
			Hex Game
		seconds: int
			minimum time to run

		Returns
		-------
		move: tuple
			move chosen
		"""

		limit = time.time() + seconds
		depth = 1
		move = None
		while True:
			if depth > len(self.move_options):
				return move
			move = self.abp_start(depth)
			print("Depth:", depth)
			print("AI Move:", move)
			print("Time Left:", limit - time.time())
			if time.time() > limit:
				return move
			depth += 1


class HexGameUI(HexGame):

	"""
	Representation of HexGameUI.
	...

	Attributes
	----------
	Includes Most attributes from HexGame
	
	root: Tkinter root
		root screen
	canvas: Tkinter canvas
		canvas
	ui_text_color: str
		text color for UI
	self.hex_size: int
		size of hex
	text_size: int
		size of text
	hex_x = int
		position x
	hex_y = int
		position y
	hexagons = dictionary
		hexagons canvas item value by id
	type = int
		type of move
	p1_move_func = function
		player 1 move function
	p2_move_func = function
		player 2 move function
	
	"""

	def on_enter(self, item, event=None):

		"""
		Adds color on enter

		Parameter
		---------
		self : class object
			Hex Game UI
		item: canvas item
			hexagon
		event: event to do
			None
		Returns
		-------
		None
		"""

		if self.current_player == "P1":
			color = "lightblue"
		elif self.current_player == "P2":
			color = "lightcoral"
		self.canvas.itemconfigure(item, fill=color)

	def on_leave(self, item, event=None):

		"""
		Removes color on exit

		Parameter
		---------
		self : class object
			Hex Game UI
		item: canvas item
			hexagon
		event: event to do
			None
		Returns
		-------
		None
		"""

		self.canvas.itemconfigure(item, fill="white")

	def player_move_ui(self, id):

		"""
		Player move for UI

		Parameter
		---------
		self : class object
			Hex Game UI
		id: str
			hexagon id
		Returns
		-------
		move: tuple
			move to be played
		"""

		move = (id[0], id[1:])
		print(move)
		return move

	def player_vs_player(self, id):

		"""
		Player vs player hex ui game

		Parameter
		---------
		self : class object
			Hex Game UI
		id: str
			hexagon id
		Returns
		-------
		self.current_player: str
			player who won
		"""

		if self.winner_exists == False:
    			move = self.player_move_ui(id)
    			self.do_actions(move)
    			self.current_round += 0.5
    			if self.winner_exists:
    				self._print_winner()
    				self.unbind_all()
    				self.root.after(10000, self.time_limit_reached)
    				return self.current_player

	def player_vs_ai(self, id):

		"""
		Player vs ai hex ui game

		Parameter
		---------
		self : class object
			Hex Game UI
		id: str
			hexagon id
		Returns
		-------
		self.current_player: str
			player who won
		"""

		if self.type == 2:
			move_func = self.p2_move_func
		elif self.type == 3:
			move_func = self.p1_move_func

		if self.winner_exists == False:
    			move = self.player_move_ui(id)
    			self.do_actions(move)
    			self.current_round += 0.5
    			if self.winner_exists:
    				self._print_winner()
    				self.unbind_all()
    				self.root.after(10000, self.time_limit_reached)
    				return self.current_player

    			move = move_func()
    			str_move = str(move[0]) + str(move[1])
    			self.modify_hexagon(self.hexagons[str_move])
    			self.do_actions(move)
    			self.current_round += 0.5
    			if self.winner_exists:
    				self._print_winner()
    				self.unbind_all()
    				self.root.after(10000, self.time_limit_reached)
    				return self.current_player


	def unbind_all(self):

		"""
		Unbinds all iterations to hexagons

		Parameter
		---------
		self : class object
			Hex Game UI
		Returns
		-------
		None
		"""

		for item in self.hexagons.values():
			self.canvas.tag_unbind(item, "<Button-1>")
			self.canvas.tag_unbind(item, "<Enter>")
			self.canvas.tag_unbind(item, "<Leave>")

	def time_limit_reached(self):

		"""
		Quits root after time is reached used with self.root.after

		Parameter
		---------
		self : class object
			Hex Game UI
		Returns
		-------
		None
		"""

    		#print("Time limit reached!")
		self.root.quit()

	def ai_vs_ai(self):

		"""
		ai vs ai hex ui game

		Parameter
		---------
		self : class object
			Hex Game UI
		Returns
		-------
		self.current_player: str
			player who won
		"""

		while True:
			if self.winner_exists == False:
    				move = self.move_func()
    				str_move = str(move[0]) + str(move[1])
    				self.modify_hexagon(self.hexagons[str_move])
    				self.do_actions(move)
    				self.current_round += 0.5
    				self.move_func = self.swap_move_func(self.move_func, self.p1_move_func, self.p2_move_func)
    				self.root.after(10, self.ai_vs_ai)
    				return

			if self.winner_exists:
    				self._print_winner()
				# Schedule the time_limit_reached function to be called after 10000 milliseconds (10 seconds)
    				self.unbind_all()
    				self.root.after(10000, self.time_limit_reached)
    				return self.current_player

	def clicked(self, item, id, event=None):

		"""
		Modifies color on clicked and does game

		Parameter
		---------
		self : class object
			Hex Game UI
		item: canvas item
			hexagon
		event: event to do
			None
		Returns
		-------
		None
		"""

		self.modify_hexagon(item)
		if self.type == 1:
    			self.player_vs_player(id)
		elif self.type == 2 or self.type==3:
			self.player_vs_ai(id)

	def create_hexagon(self, fill="white", outline="black", text="text"):

		"""
		Creates hexagon

		Parameter
		---------
		self : class object
			Hex Game UI
		fill: str
			hexagon fill color
		outline: str
			hexagon outline color
		text: str
			text represents hexagon id
		Returns
		-------
		hexagon: canvas item
			hexagon
		"""

		points = []
		for i in range(6):
			angle_rad = math.radians(60 * i)
			x = self.hex_x + self.hex_size * math.cos(angle_rad)
			y = self.hex_y + self.hex_size * math.sin(angle_rad)
			points.append(y)
			points.append(x)
		hexagon = self.canvas.create_polygon(points, fill=fill, outline=outline)
		self.canvas.tag_bind(hexagon, "<Enter>", partial(self.on_enter, hexagon))
		self.canvas.tag_bind(hexagon, "<Leave>", partial(self.on_leave, hexagon))
		self.canvas.tag_bind(hexagon,"<Button-1>",partial(self.clicked, hexagon, text))
		return hexagon

	def create_hexagon_text(self, text, text_color="black", fill="white", outline="black"):

		"""
		Creates hexagon with text

		Parameter
		---------
		self : class object
			Hex Game UI
		text: str
			text represents hexagon id and text to show
		text_color: str
			text color
		fill: str
			hexagon fill color
		outline: str
			hexagon outline color
		Returns
		-------
		hexagon: canvas item
			hexagon
		"""

		hexagon = self.create_hexagon(fill, outline, text)
		text_id = self.create_text(text, text_color)
		return hexagon

	def create_text(self, text, text_color="black"):

		"""
		Creates text

		Parameter
		---------
		self : class object
			Hex Game UI
		text: str
			text represents hexagon id and text to show
		text_color: str
			text color
		Returns
		-------
		None
		"""

		text_id = self.canvas.create_text(self.hex_y, self.hex_x, text=text, font=("Arial", self.text_size, "bold"), fill=text_color, anchor="center")

	def modify_hexagon(self, item):

		"""
		Modify current hexagon fill color and unbinds preventing further changes

		Parameter
		---------
		self : class object
			Hex Game UI
		item: canvas item
			hexagon
		Returns
		-------
		None
		"""

		if self.current_player == "P1":
			color = "blue"
		elif self.current_player == "P2":
			color = "red"
		self.canvas.itemconfigure(item, fill=color)
		self.canvas.tag_unbind(item, "<Button-1>")
		self.canvas.tag_unbind(item, "<Enter>")
		self.canvas.tag_unbind(item, "<Leave>")

	def generate_ui(self):

		"""
		Generates Hex Game UI game board

		Parameter
		---------
		self : class object
			Hex Game UI
		Returns
		-------
		None
		"""

		self.root = tk.Tk()
		self.canvas =tk.Canvas(self.root, width= 1000 ,height= 1000, bg = 'white')
		self.canvas.pack()

		self.ui_text_color = "black"
		self.hex_size = 400/self.board_size
		self.text_size = int(self.hex_size/2)
		self.hex_x = self.hex_size * 2
		self.hex_y = self.hex_size * 2
		self.hexagons = {}
		shifter = self.hex_y


		for y in range(self.board_size):
			y_coord = str(y+1)
			for x in range(self.board_size):
				x_coord = ALPHABET[x]
				text = x_coord + y_coord
				hexagon = self.create_hexagon_text(text=text)
				self.hexagons[text] = hexagon
				self.hex_y += self.hex_size*6.9/4
			self.hex_x += self.hex_size*6/4
			shifter += self.hex_size*6.9/8
			self.hex_y = shifter
		
		#left numbers
		self.hex_x = self.hex_size * 2
		self.hex_y = self.hex_size
		for y in range(self.board_size):
			y_coord = str(y+1)
			self.create_text(y_coord, "blue")
			self.hex_x += self.hex_size*6/4
			self.hex_y += self.hex_size*6.4/8

		#right numbers
		self.hex_x = self.hex_size * 2
		self.hex_y = 720 + self.hex_size

		#self.hex_size*6.5/4*(self.board_size+1)
		for y in range(self.board_size):
			y_coord = str(y+1)
			self.create_text(y_coord, "blue")
			self.hex_x += self.hex_size*6/4
			self.hex_y += self.hex_size*8/9

		#top letters
		self.hex_x = self.hex_size/2
		self.hex_y = self.hex_size*2
		for x in range(self.board_size):
			x_coord = ALPHABET[x]
			self.create_text(x_coord, "red")
			self.hex_y += self.hex_size*1.75
		
		#bottom letters
		self.hex_x = self.hex_size/2 + self.hex_size*6/4*(self.board_size+1)
		self.hex_y = self.hex_size + self.hex_size/2.2 + self.hex_size*6.4/8*(self.board_size)
		for x in range(self.board_size):
			x_coord = ALPHABET[x]
			self.create_text(x_coord, "red")
			self.hex_y += self.hex_size*1.75

		self.update_canvas_size()


		if self.type == 3:
			#does first move
    			move = self.p1_move_func()
    			str_move = str(move[0]) + str(move[1])
    			self.modify_hexagon(self.hexagons[str_move])
    			self.do_actions(move)
    			self.current_round += 0.5
		elif self.type == 4:
			self.move_func = self.p1_move_func
			self.root.after(10, self.ai_vs_ai)

		tk.mainloop()

	def update_canvas_size(self):

		"""
		Updates Hex Game UI game board size based on hexagon size

		Parameter
		---------
		self : class object
			Hex Game UI
		Returns
		-------
		None
		"""

		self.canvas.update_idletasks()
		bbox = self.canvas.bbox("all")
		if bbox:
			self.canvas.config(width=bbox[2] - bbox[0] + self.hex_size * 2, height=bbox[3] - bbox[1] + self.hex_size*2)

	def ui_game(self, type=1, p1_move_func=None, p2_move_func=None):

		"""
		Allows game to be played with UI

		Parameter
		---------
		self : class object
			Hex Game
		type: int
			type of version to player
		p1_move_func : function
			player 1 function to get move
		p2_move_func : function
			player 2 function to get move

		Returns
		-------
		None
		"""

		#four options for type, 1: player vs player, 2: player vs ai, 3: ai vs player, 4: ai vs ai
		#only need to pass move function for types 2 ,3, or 4.
		self.current_round = 0
		self.played_moves = set()
		self.winner_exists = False
		self.current_player = "P1"
		self.type = type
		self.p1_move_func = p1_move_func
		self.p2_move_func = p2_move_func
		self.generate_ui()
		self.reset_board()

	def play_game(self):

		"""
		Allows game to be played person vs person UI

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""

		#player one wins if line left to right and player two if line top to bottom
		self.ui_game()	

	def as_p1(self):

		"""
		Allows game to be played person vs ai UI

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""

		self.ui_game(2, None, partial(self.abp_id, 1))	
			

	def as_p2(self):

		"""
		Allows game to be played ai vs person UI

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""

		self.ui_game(3, partial(self.abp_id, 1), None)

	def simulation(self):

		"""
		Allows game to be played ai vs ai UI

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""

		self.ui_game(4, partial(self.abp_id, 1), partial(self.abp_id, 1))
		#self.ui_game(4, self.random_move, partial(self.abp_id, 10))	

	def reset_board(self):

		"""
		Resets the game board and resets hex_states and regenerates move_options and root

		Parameter
		---------
		self : class object
			Hex Game

		Returns
		-------
		None
		"""

		self.create_board()
		self.root.destroy()


if __name__ == "__main__":
	hex = HexGame(5)
	hex.play_game()
	hex.as_p1()
	hex.as_p2()
	hex.simulation()
	hex = HexGameUI(5)
	hex.play_game()
	hex.as_p1()
	hex.as_p2()
	hex.simulation()
