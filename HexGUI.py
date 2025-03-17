#
# Class: CPSC 481 Spring 2025
# Project Group : 10
# Project members: Dominic Davis, Daniel Garcia, Yuval Noiman, Eduardo Salvador-Martinez
# Program Name: HexGUI.py
# GUI coded By : Dominic Davis
# Description : Python tkinter GUI for the HEX Game
#                        This program currently let two players play the Hex game manually.
#
#                        Each player alternatively enter the Hex Cell ID to mark their selection
#                        If Player 1 connect first the Hex Cells from Top to Bottom, the player become winner
#                        If Player 2 connect first the Hex Cells from Left to Right, the player become winner
#                        Functionality to evaluate a winner will be added later.

# import the tkinter GUI components and functionalities
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

# Root of the GUI
root = Tk()

# Title of the GUI
root.title('HEX Game')

# Hex geometry
# for 5x5 Hex grid
xpattern = 5
ypattern = 5
geometry_size = '400x450'
canvas_width = 340
canvas_height = 330

# Size of the GUI
root.geometry(geometry_size)

# List to store all Hex cell IDs
hex_cell_ids = []

# List to store current status of each Hex cell
hex_cell_stat = []

# List for Hex cell boundaries
hex_cell_boundaries = []

# Variable for user response
pv = StringVar()

# Label source of Hex cell IDs
xlabels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']

# Current Player
current_player = [1]

# Player 1 Name
player_name1 = "Human Player 1"
# Player 1 Color
player_1_color = "red"

# Player 2 Name
player_name2 = "Human Player 2"
# Player 2 Color
player_2_color = "blue"

# Player Name to be displayed
player_name = Label(root, text=player_name1, foreground=player_1_color, font='TkDefaultFont 16')

# for 5 x 5
canvas_color = "yellow"
canvas = Canvas(root, bg = canvas_color, width=canvas_width, height=canvas_height)
canvas.pack()

# Instruction for Hex cell ID entry
player_instr = Label(root, text="Enter Hex cell ID" , font='TkDefaultFont 16')

# User entry from Player
user_entry = Entry(root, textvariable=pv)

# to clear user entry
def clearEntry():
	pv.set('')

# to alternate players
def alternatePlayer():
	if (current_player[0] == 1):
		current_player[0]  = 2
		player_name.configure(text=player_name2, foreground=player_2_color)
		return

	if (current_player[0] == 2):
		current_player[0]  = 1
		player_name.configure(text=player_name1,  foreground=player_1_color)
		return

# to get Hex cell index
def getHexCellIndex(cell_ID):
	# get the index of cell
	cell_index = hex_cell_ids.index(cell_ID)

	return cell_index

# to validate user selection of cell ID
def validateCell(cell_ID):
	cell_exists = hex_cell_ids.count(cell_ID)

	# verify if cell ID is valid
	if (cell_exists <= 0):
		messagebox.showinfo("Error", "Invalid Hex cell ID entered. Enter another Hex cell ID.")
		clearEntry()
		user_entry.focus()
		return -1

	return cell_exists

# to get current status of each hex cell
def getHexCellStatus(cell_ID):

	# get the index of cell
	cell_index = getHexCellIndex(cell_ID)
	if (cell_index < 0):
		return -1

	if (cell_index >= 0):
		# get the current status of cell
		cell_status = hex_cell_stat[cell_index]

		if (cell_status == 1):
			messagebox.showinfo("Error", "Hex cell already marked by "+player_name1+" Enter another Hex cell ID.")
			clearEntry()
			user_entry.focus()
			return 1

		if (cell_status == 2):
			messagebox.showinfo("Error", "Hex cell already marked by "+player_name2+" Enter another Hex cell ID.")
			clearEntry()
			user_entry.focus()
			return 2

	return cell_status

# to create the Hexagonal cell
def hex(hx, hy, tx, ty, hex_cell_id):
	# calculate Hex cell boundaries
	b11 = hx+30
	b12 = hy+50
	b21 = hx+50
	b22 = hy+30
	b31 = hx+70
	b32 = hy+50
	b41 = hx+70
	b42 = hy+80
	b51 = hx+50
	b52 = hy+100
	b61 = hx+30
	b62 = hy+80
	b71 = hx+30
	b72 = hy+50

	# create Hex cell boundaries
	canvas.create_line((b11, b12), 
                                       (b21, b22), 
                                       (b31, b32), 
                                       (b41, b42), 
                                       (b51, b52), 
                                       (b61, b62), 
                                       (b71, b72),
                                  width=3, fill='black')	

	# Place ID to each Hex cell
	canvas.create_text((tx, ty), text=hex_cell_id, 	fill='black', font='TkDefaultFont 16')

	# store Hex cell boundaries for each cell
	boundaries = []
	boundaries.append(b11)
	boundaries.append(b12)
	boundaries.append(b21)
	boundaries.append(b22)
	boundaries.append(b31)
	boundaries.append(b32)
	boundaries.append(b41)
	boundaries.append(b42)
	boundaries.append(b51)
	boundaries.append(b52)
	boundaries.append(b61)
	boundaries.append(b62)
	boundaries.append(b71)
	boundaries.append(b72)

	# store the full boundaries for that cell
	hex_cell_boundaries.append(boundaries)

	# store the Hex cell IDs
	hex_cell_ids.append(hex_cell_id)

	# set initial status of each Hex cell to 0
	hex_cell_stat.append(0)


# to mark the selected Hex cell by the current Player
def markHex():
	# capture user entry for cell ID
	uv = pv.get()

	# validate length
	if (len(uv) < 2):
		messagebox.showinfo("Error", "Invalid Hex cell ID entered. Enter another Hex cell ID.")
		clearEntry()
		user_entry.focus()
		return -1

	# convert into uppercase
	uv = uv.upper()

	# Validate the selected Hex cell
	valid_cell = validateCell(uv)

	# Get Hex cell status
	if (valid_cell > 0):
		cell_status = getHexCellStatus(uv)
		if (cell_status <0):
			return
		if (cell_status == 1):
			return
		if (cell_status == 2):
			return

		# if the Hex cell is not marked
		if (cell_status == 0):

			# Fill the Hex cell
			hexFill(uv)

			# Update the mark
			cell_index = hex_cell_ids.index(uv)

			if (cell_index >= 0):
				if (current_player[0] == 1):
					hex_cell_stat[cell_index] = 1

				if (current_player[0] == 2):
					hex_cell_stat[cell_index] = 2

				# change player
				alternatePlayer()
				# clear user entry value
				clearEntry()


# to fill the Hex cell
def hexFill(cell_ID):
	# get the index of cell
	cell_index = hex_cell_ids.index(cell_ID)

	if (cell_index >= 0):
		# get the cell reference
		hc = hex_cell_boundaries[cell_index]

		# get the cell boundaries
		b11,b12,b21,b22,b31,b32,b41,b42,b51,b52,b61,b62,b71,b72 = hc

		# for Hex cell ID 
		tx = (b11 - 30) + 50
		ty = (b12 - 50) + 65

		if (current_player[0] == 1):
			canvas.create_polygon((b11, b12),(b21, b22),(b31, b32),(b41, b42),(b51, b52),(b61, b62),(b71, b72),
                                 	 fill=player_1_color, smooth=False)	
			canvas.create_text((tx, ty), text=cell_ID, 	fill='black', font='TkDefaultFont 16')
			user_entry.focus()
			return

		if (current_player[0] == 2):
			canvas.create_polygon((b11, b12),(b21, b22),(b31, b32),(b41, b42),(b51, b52),(b61, b62),(b71, b72),
                                 	 fill=player_2_color, smooth=False)	
			canvas.create_text((tx, ty), text=cell_ID, 	fill='white', font='TkDefaultFont 16')
			user_entry.focus()
			return

# Button to mark the selected Hex cell
mark_button = Button(root, text='Mark Hex', command=markHex)

# main 
def main():
	# variables for Hex cell construction
	xp = 0
	yp = 0
	# for x and y axis shift
	xshift = 20
	yshift = 50
	# for add on to x axis
	hxadd = 40
	# x and y values for cell border
	hx = 0
	hy = 0
	# x and y values for Cell label
	tx = 0
	ty = 0

	# for Player 1 direction (Vertical) top side marking 
	if (xpattern == 5):
		canvas.create_rectangle(30, 10, 310, 20, fill=player_1_color)

	# for Player 2 direction (Horizontal) Left side marking 
	if (ypattern == 5):
		canvas.create_rectangle(10, 20, 20, 310, fill=player_2_color)

	# Create the Hex GUI
	# for each Row
	while(yp < ypattern):
		# for each Column

		while(xp < xpattern):

			# x value for Cell ID
			tx = hx + 50

			# y value for the Cell ID
			ty = hy + 65

			#  create the hex cell ID
			hex_cell_id = str(yp+1) + xlabels[xp]

			# create the Hex cell
			hex(hx, hy, tx, ty, hex_cell_id)

			# change the values for the next cell in xpattern
			hx = hx + hxadd
			hy = yp * yshift
			xp = xp + 1

		# change the values for the next cell in ypattern
		xp = 0
		yp = yp + 1
		hx = yp * xshift
		hy = yp * yshift

	# Label for the Player
	player_name.pack()

	# Instruction for Hex cell ID entry
	player_instr.pack()

	# User entry from Player
	user_entry.pack()
	user_entry.takefocus = 1

	# Button to mark the selected Hex cell
	mark_button.pack()
	mark_button.takefocus = 0

	# for Player 1 direction (Vertical) bottom side marking 
	if (xpattern == 5):
		canvas.create_rectangle(30, 310, 310, 320, fill=player_1_color)

	# for Player 2 direction (Horizontal) Right side marking 
	if (ypattern == 5):
		canvas.create_rectangle(320, 20, 330, 310, fill=player_2_color)

	# get Player input
	user_entry.focus()

	# Disable root resize
	root.resizable(False, False)

	# Loop the GUI
	root.mainloop()

# run the main function
if __name__ == "__main__":
	main()

# End of HexGUI.py
