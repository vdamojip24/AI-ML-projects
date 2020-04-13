import numpy as np


def terminal_test(board):
	#got this code from human player class
	for i, col in enumerate(board.T):
		if 0 in col:
			return False
	return True


def possible_actions(board):
	valid_moves = []
	for col in range(7):
		for row in reversed(range(6)):#start at bottom row
			if(board[row][col] == 0):
				valid_moves.append((row,col))
				break
	return valid_moves

# def resulting_board(board, action, player_number):

# 	new_board = np.zeros([6,7]).astype(np.uint8)
# 	for row in reversed(range(6)):
# 		for i,col_val in enumerate(board[row]):
# 			new_board[row][i] = col_val
	
# 	for row in reversed(range(6)):
# 		for i,col_val in enumerate(new_board[row]):
# 			if i == action and new_board[row][i] == 0:
# 				new_board[row][i] = player_number
# 				return new_board,row
# 	return new_board,row

def resulting_board(board,row,col,player_num):
	board[row][col] = player_num
	return board

def reset_board(board,row,col):
	board[row][col] = 0
	return board


#def max_val(self,board, alpha, beta, depth, player_num, enemy):
def max_val(board, alpha, beta, depth, player_num, enemy):
	if(terminal_test(board) or depth == 5): #cut off at 5 because depth 6 takes too long
		return(evaluation_function(board))
		#return self.evaluation_function(board,player_num)
	#v = -inf 
	v = -1000000
	for row,col in possible_actions(board):
		#board[row][col] = 2
		board = resulting_board(board,row,col,player_num)
		v = max(v, min_val(board, alpha, beta, depth+1, player_num, enemy))
		#v = max(v, min_val(self,board, alpha, beta, depth+1, player_num, enemy))	
		board = reset_board(board,row,col)#reset board val back to original board

		if v >= beta:
			return v
		alpha = max(alpha,v)
	return v

#def min_val(self,board, alpha, beta, depth, player_num, enemy):
def min_val(board, alpha, beta, depth, player_num, enemy):

	if(terminal_test(board) or depth == 5): #cut off at 5 because depth 6 takes too long
		return evaluation_function(board)
		#return self.evaluation_function(board,player_num)
	
	#v = inf
	v = 1000000
	for row,col in possible_actions(board):
		#board[row][col] = 1
		board = resulting_board(board,row,col,enemy)
		v = min(v, max_val(board,alpha,beta, depth+1, player_num, enemy))
		#v = min(v, max_val(self,board,alpha,beta, depth+1, player_num, enemy))
		board = reset_board(board,row,col) #reset board back to original board

		if v <= alpha:
			return v
		beta = min(beta,v)
	return v							

def max_val_expectimax(board,depth, player_num, enemy):
	
	if(terminal_test(board) or depth == 4): #goes slowly after depth 4
		return evaluation_function(board)
	
	v = -1000000
	for row,col in possible_actions(board):
		#board[row][col] = 1
		board = resulting_board(board,row,col,player_num)
		v = max(v, exp_val(board,depth+1, player_num, enemy))
		board = reset_board(board,row,col) #reset back to original board
	return v

def exp_val(board,depth, player_num, enemy):
	
	if(terminal_test(board) or depth == 4): #goes slowly after depth 4
		return evaluation_function(board)

	v = 0
	#num_possible_Actions = len(possible_actions(board)) #don't want to call this twice
	num_possible_Actions = 0
	for row,col in possible_actions(board):
		num_possible_Actions += 1
		#board[row][col] = 2
		board = resulting_board(board,row,col,enemy)
		v += max_val_expectimax(board,depth+1,player_num, enemy)
		board = reset_board(board,row,col) 
	return v/num_possible_Actions #equal probablity of picking a column


def evaluation_function(board):
	# 	"""
	# 	Given the current stat of the board, return the scalar value that 
	# 	represents the evaluation function for the current player
	   
	# 	INPUTS:
	# 	board - a numpy array containing the state of the board using the
	# 			following encoding:
	# 			- the board maintains its same two dimensions
	# 				- row 0 is the top of the board and so is
	# 				  the last row filled
	# 			- spaces that are unoccupied are marked as 0
	# 			- spaces that are occupied by player 1 have a 1 in them
	# 			- spaces that are occupied by player 2 have a 2 in them

	# 	RETURNS:
	# 	The utility value for the current board
	# 	"""

	   

	player_count = 0
	opponent_count = 0
	temp1_count = 0
	temp2_count = 0

	for row in board:
		for col in row:
			if col == 1:
				temp1_count += 1
			if col == 2:
				temp2_count += 1
        
		if(temp1_count > temp2_count):
			player_count += 5
		if(temp2_count > temp1_count):
			opponent_count += 5
        
		if(temp1_count - temp2_count == 1):
			player_count += 50
		if(temp1_count - temp2_count == 2):
			player_count += 100
		if(temp1_count - temp2_count == 3):
			player_count += 200
		if(temp2_count - temp1_count == 1):
			opponent_count += 50
		if(temp2_count - temp1_count == 2):
			opponent_count += 100
		if(temp2_count - temp1_count == 3):
			opponent_count += 200
		temp1_count = 0
		temp2_count = 0

	return (player_count - opponent_count)




class AIPlayer:
	def __init__(self, player_number):
		self.player_number = player_number
		self.type = 'ai'
		self.player_string = 'Player {}:ai'.format(player_number)




	def get_alpha_beta_move(self, board):
		"""
		Given the current state of the board, return the next move based on
		the alpha-beta pruning algorithm

		This will play against either itself or a human player

		INPUTS:
		board - a numpy array containing the state of the board using the
				following encoding:
				- the board maintains its same two dimensions
					- row 0 is the top of the board and so is
					  the last row filled
				- spaces that are unoccupied are marked as 0
				- spaces that are occupied by player 1 have a 1 in them
				- spaces that are occupied by player 2 have a 2 in them

		RETURNS:
		The 0 based index of the column that represents the next move
		"""
		
		#raise NotImplementedError('Whoops I don\'t know what to do')

		player_num = self.player_number
		if(player_num == 1):
			enemy = 2
		else:
			enemy = 1


		possible_vals = []
		alpha = -1000000
		beta = 1000000
		depth = 0

		#max_v = max_val(board,alpha,beta, depth+1, player_num, enemy) #dont want to compute max_val twice (slows down ai)
		#assume you start at max node
		for row,col in possible_actions(board):
			#board[row][col] = 2
			board = resulting_board(board,row,col,player_num)
			#call max with -1000000 instead of v because v isnt initialized 
			v = max(-1000000, min_val(board,alpha,beta,depth+1, player_num, enemy))
			#v = max(-1000000, min_val(self,board,alpha,beta,depth+1, player_num, enemy))
			board = reset_board(board,row,col) #reset back to original board
			possible_vals.append((row,col,v))
			
		###get max util val###
		max_util = -1000000
		for row,col,v in possible_vals:
			if v >= max_util:
				max_util = v
		#print(max_util)

		#get col of max util val
		for index_val_pair in possible_vals:
			if max_util in index_val_pair:
				return index_val_pair[1]
		return 5 #for testing purposes







	def get_expectimax_move(self, board):
		"""
		Given the current state of the board, return the next move based on
		the expectimax algorithm.

		This will play against the random player, who chooses any valid move
		with equal probability

		INPUTS:
		board - a numpy array containing the state of the board using the
				following encoding:
				- the board maintains its same two dimensions
					- row 0 is the top of the board and so is
					  the last row filled
				- spaces that are unoccupied are marked as 0
				- spaces that are occupied by player 1 have a 1 in them
				- spaces that are occupied by player 2 have a 2 in them

		RETURNS:
		The 0 based index of the column that represents the next move
		"""
		
		depth = 0
		#v = -1000000
		possible_vals = []

		if(terminal_test(board)):
			evaluation_function(board)

		player_num = self.player_number
		if(player_num == 1):
			enemy = 2
		else:
			enemy = 1					

		###assume you start at max node
		for row,col in possible_actions(board):
			#board[row][col] = 1
			board = resulting_board(board,row,col,player_num)
			#v = max(v, exp_val(board,depth+1,player_num,enemy))
			v = max(-1000000, exp_val(board,depth+1,player_num,enemy))
			board = reset_board(board,row,col) #make sure board isn't modified
			possible_vals.append((row,col,v))
			
		#get max util value
		max_util = -1000000
		for row,col,v in possible_vals:
			if v >= max_util:
				max_util = v
		
		#get column index of max util value
		for index_val_pair in possible_vals:
			if max_util in index_val_pair:
				return index_val_pair[1]
		return 5 #for testing purposes



		raise NotImplementedError('Whoops I don\'t know what to do')




class RandomPlayer:
	def __init__(self, player_number):
		self.player_number = player_number
		self.type = 'random'
		self.player_string = 'Player {}:random'.format(player_number)

	def get_move(self, board):
		"""
		Given the current board state select a random column from the available
		valid moves.

		INPUTS:
		board - a numpy array containing the state of the board using the
				following encoding:
				- the board maintains its same two dimensions
					- row 0 is the top of the board and so is
					  the last row filled
				- spaces that are unoccupied are marked as 0
				- spaces that are occupied by player 1 have a 1 in them
				- spaces that are occupied by player 2 have a 2 in them

		RETURNS:
		The 0 based index of the column that represents the next move
		"""
		valid_cols = []
		for col in range(board.shape[1]):
			if 0 in board[:,col]:
				valid_cols.append(col)

		return np.random.choice(valid_cols)


class HumanPlayer:
	def __init__(self, player_number):
		self.player_number = player_number
		self.type = 'human'
		self.player_string = 'Player {}:human'.format(player_number)

	def get_move(self, board):
		"""
		Given the current board state returns the human input for next move

		INPUTS:
		board - a numpy array containing the state of the board using the
				following encoding:
				- the board maintains its same two dimensions
					- row 0 is the top of the board and so is
					  the last row filled
				- spaces that are unoccupied are marked as 0
				- spaces that are occupied by player 1 have a 1 in them
				- spaces that are occupied by player 2 have a 2 in them

		RETURNS:
		The 0 based index of the column that represents the next move
		"""

		valid_cols = []
		for i, col in enumerate(board.T):
			if 0 in col:
				valid_cols.append(i)

		move = int(input('Enter your move: '))

		while move not in valid_cols:
			print('Column full, choose from:{}'.format(valid_cols))
			move = int(input('Enter your move: '))

		#print(board)
		#print(possible_actions(board))
		#print(utility_value(board))
		#print(board)
		#board = np.ones([6,7]).astype(np.uint8)
		#print(resulting_board(board, 5, 2))
		#print(board.T)
		#print(board)

		return move

