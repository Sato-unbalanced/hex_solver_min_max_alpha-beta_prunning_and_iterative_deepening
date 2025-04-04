from termcolor import colored
import random
import copy
import tkinter as tk
from functools import partial
import math
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
		#print("Move:", move)
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
		print(move)
		#move = str(move[0]) + str(move[1])
		#print(move)
		self.do_actions(move)

	def do_actions(self, move):
		#print(move)
		#move = (move[0],move[1])
		self.player_move(move)
		self.evaluate()
		self.determine_if_winner(move)
		if self.winner_exists == False:
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
				self.reset_board()
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

class Hex_Game_UI(Hex_Game):


	def on_enter(self, item, event=None):
		if self.current_player == "P1":
			color = "lightblue"
		elif self.current_player == "P2":
			color = "lightcoral"
		self.canvas.itemconfigure(item, fill=color)

	def on_leave(self, item, event=None):
    		self.canvas.itemconfigure(item, fill="white")

	def player_move_ui(self, id):
		#overwrites text based version
    		move = (id[0], id[1:])
    		print(move)
    		return move

	def player_vs_player(self, id):
		if self.winner_exists == False:
    			move = self.player_move_ui(id)
    			self.do_actions(move)
    			self.current_round += 0.5
		if self.winner_exists:
    			self._print_winner()
    			#self.canvas.destroy()
    			self.root.quit()
    			return self.current_player

	def player_vs_ai(self, id):
		if self.type == 2:
			move_func = self.p2_move_func
		elif self.type == 3:
			move_func = self.p1_move_func

		if self.winner_exists == False:
    			move = self.player_move_ui(id)
    			self.do_actions(move)
    			self.current_round += 0.5
    			move = move_func()
    			print(move)
    			str_move = str(move[0]) + str(move[1])
    			self.modify_hexagon(self.hexagons[str_move])
    			self.do_actions(move)
    			self.current_round += 0.5
		if self.winner_exists:
    			self._print_winner()
    			#self.canvas.destroy()
    			self.root.quit()
    			return self.current_player


	def time_limit_reached(self):
    		print("Time limit reached!")
    		self.root.quit()

	def ai_vs_ai(self):
		move_func = self.p1_move_func
		while True:
			if self.winner_exists == False:
    				move = move_func()
    				print(move)
    				str_move = str(move[0]) + str(move[1])
    				self.modify_hexagon(self.hexagons[str_move])
    				self.do_actions(move)
    				self.current_round += 0.5
    				move_func = self.swap_move_func(move_func, self.p1_move_func, self.p2_move_func)

			if self.winner_exists:
    				self._print_winner()
				# Schedule the time_limit_reached function to be called after 10000 milliseconds (10 seconds)
    				self.root.after(10000, self.time_limit_reached)
    				tk.mainloop()
    				#self.canvas.destroy()
    				return self.current_player

	def clicked(self, item, id, event=None):
		self.modify_hexagon(item)
		if self.type == 1:
    			self.player_vs_player(id)
		elif self.type == 2 or self.type==3:
			self.player_vs_ai(id)

	def create_hexagon(self, fill="white", outline="black", text="text"):
		points = []
		for i in range(6):
			angle_rad = math.radians(60 * i)
			x = self.hex_x + self.hex_size * math.cos(angle_rad)
			y = self.hex_y + self.hex_size * math.sin(angle_rad)
			#swap y and x for hexagon with line on top keep for point on top
			points.append(y)
			points.append(x)
		hexagon = self.canvas.create_polygon(points, fill=fill, outline=outline)
		self.canvas.tag_bind(hexagon, "<Enter>", partial(self.on_enter, hexagon))
		self.canvas.tag_bind(hexagon, "<Leave>", partial(self.on_leave, hexagon))

		#what clicked does will differ based on type

		self.canvas.tag_bind(hexagon,"<Button-1>",partial(self.clicked, hexagon, text))
		return hexagon

	def create_hexagon_text(self, text, text_color="black", fill="white", outline="black"):
		hexagon = self.create_hexagon(fill, outline, text)
		text_id = self.create_text(text, text_color)
		return hexagon

	def create_text(self, text, text_color="black"):
		text_id = self.canvas.create_text(self.hex_y, self.hex_x, text=text, font=("Arial", self.text_size, "bold"), fill=text_color, anchor="center")

	def modify_hexagon(self, item):
		if self.current_player == "P1":
			color = "blue"
		elif self.current_player == "P2":
			color = "red"
		self.canvas.itemconfigure(item, fill=color)
		self.canvas.tag_unbind(item, "<Button-1>")
		self.canvas.tag_unbind(item, "<Enter>")
		self.canvas.tag_unbind(item, "<Leave>")

	def generate_ui(self):

		self.root = tk.Tk()
		self.canvas =tk.Canvas(self.root, width= 1000 ,height= 1000, bg = 'white')
		self.canvas.pack()

		self.ui_text_color = "black"
		self.hex_size = 400/self.board_size
		self.text_size = int(self.hex_size/2)
		print(self.hex_size)
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
		
		#add numbers and letters
		self.hex_x = self.hex_size * 2
		self.hex_y = self.hex_size
		for y in range(self.board_size):
			y_coord = str(y+1)
			self.create_text(y_coord, "blue")
			self.hex_x += self.hex_size*6/4
			self.hex_y += self.hex_size*6.4/8
		self.hex_y = self.hex_size + self.hex_size*6.2/4*(self.board_size+1)
		self.hex_x = self.hex_size * 2
		for y in range(self.board_size):
			y_coord = str(y+1)
			self.create_text(y_coord, "blue")
			self.hex_x += self.hex_size*6/4
			self.hex_y += self.hex_size*6.4/8

		self.hex_x = self.hex_size/2
		self.hex_y = self.hex_size*2
		for x in range(self.board_size):
			x_coord = ALPHABET[x]
			self.create_text(x_coord, "red")
			self.hex_y += self.hex_size*1.75

		self.hex_x = self.hex_size/2 + self.hex_size*6/4*(self.board_size+1)
		self.hex_y = self.hex_size + self.hex_size/2.2 + self.hex_size*6.4/8*(self.board_size)
		for x in range(self.board_size):
			x_coord = ALPHABET[x]
			self.create_text(x_coord, "red")
			self.hex_y += self.hex_size*1.75

		self.update_canvas_size()


		if self.type == 3:
    			move = self.p1_move_func()
    			print(move)
    			str_move = str(move[0]) + str(move[1])
    			self.modify_hexagon(self.hexagons[str_move])
    			self.do_actions(move)
    			self.current_round += 0.5
		elif self.type == 4:
			self.ai_vs_ai()
			return

		tk.mainloop()
		#self.canvas.pack_forget()

	def update_canvas_size(self):
		self.canvas.update_idletasks()
		bbox = self.canvas.bbox("all")
		if bbox:
			self.canvas.config(width=bbox[2] - bbox[0] + self.hex_size * 2, height=bbox[3] - bbox[1] + self.hex_size*2)

	def ui_game(self, type=1, p1_move_func=None, p2_move_func=None):
		#four options for type, 1: player vs player, 2: player vs ai, 3: ai vs player, 4: ai vs ai
		#only need to pass move function for types 2,3, or 4.
		self.current_round = 0
		self.played_moves = set()
		self.winner_exists = False
		self.current_player = "P1"
		self.type = type
		#makes more sense to make self instead of passing like in text-based since works differently
		self.p1_move_func = p1_move_func
		self.p2_move_func = p2_move_func
		self.generate_ui()
		self.reset_board()

	def play_game(self):
		#player one wins if line left to right and player two if line top to bottom
		self.ui_game()	

	def as_p1(self):
		self.ui_game(2, self.random_move, self.random_move)	

	def as_p2(self):
		self.ui_game(3, self.random_move, self.random_move)

	def simulation(self):
		self.ui_game(4, self.random_move, self.random_move)	

	def reset_board(self):
		self.create_board()
		#self.canvas.destroy()
		self.root.destroy()


if __name__ == "__main__":
	#hex = Hex_Game(5)
	#hex.simulation()
	hex = Hex_Game_UI(5)
	hex.play_game()
	#hex.reset_board()
	#hex.play_game()
	hex.as_p1()
	hex.as_p2()
	hex.simulation()
	#hex.ui_game(type=1, p1_move_func=hex.random_move, p2_move_func=hex.random_move)
	#hex.reset_board()
	#hex.ui_game_ai()
	#hex.simulation()
	#hex.reset_board()
	#hex.play_game()
