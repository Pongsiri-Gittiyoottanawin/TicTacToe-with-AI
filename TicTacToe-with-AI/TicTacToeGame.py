import numpy as np
import copy
import random
import AI

from flask import Flask, url_for, render_template, request

# list that contanin all posible positions to win the game  (two-dimensional list 8 rows 3 columns)
winning_combinations = [[0,1,2], [3,4,5], [6,7,8], 
                        [0,3,6], [1,4,7], [2,5,8], 
                            [0,4,8], [2,4,6]]

class Board:
    ''' The Board class represents the game board and state of the game in the Tic-Tac-Toe game.
    It has a 9x1 numpy array representing the game board, which is initially set to all zeros. 
    It also has lists to store the positions marked by player 1 (X) and player 2 (O) on the game board
    and a list of valid moves that can be made on the game board
    '''
    def __init__(self):
        self.board = np.zeros((9,)).astype(int)
        self.o_positions = []
        self.x_positions = []
        self.valid_moves = list(set(range(9)))
    

    def mark_down(self, action, player):
        ''' Marks the given position with the symbol of the given player on the game board 
        '''
        self.board[action] = player
        
        # update positions(index) on the board of each symbol
        self.x_positions = [i for i,j in enumerate(self.board) if j == 1]
        self.o_positions = [i for i,j in enumerate(self.board) if j == 2]
        
        # update the valid moves (avalible moves)
        self.valid_moves = list(set(range(9)) - set(self.x_positions + self.o_positions))
    

    def is_final_state(self):
        ''' check if the current state is a final state (reach terminal or base case) then return the result 
            @return 0 if there is no win yet
            @return 1 if player 1 win (X)
            @return 2 if player 2 win (O)
            This is an excellent method to adapt to AI later especially Agent Minimax
            
        '''
        
        # check win X
        for win in winning_combinations:
            if all(p in self.x_positions for p in win):
                return 1
        
        # check win O    
        for win in winning_combinations:
            if all(p in self.o_positions for p in win):
                return 2
        
        # no win yet
        return 0
    
    def display_board(self):
        ''' display a board on the console (display only using for testing or debuging)
        '''

        # copy the current board then change copy board type from int to str
        curr_board = copy.deepcopy(self.board)
        curr_board = curr_board.astype(str)
        # loop through the copy board to assign symbol
        for i in range(len(curr_board)):
            if curr_board[i] == "1":
                curr_board[i] = "X"
            elif curr_board[i] == "2":
                curr_board[i] = "O"
            else:
                curr_board[i] = "_"
                
        print(curr_board.reshape([3,3]))
    
    
    # Two methods below is using for deploy on web
    
    def get_board(self):
        ''' Returns the current state of the game board as a list of strings that have assigned symbol
        '''

        # copy the current board then change copy board type from int to str
        curr_board = copy.deepcopy(self.board)
        curr_board = curr_board.astype(str)
        # loop through the copy board to assign symbol
        for i in range(len(curr_board)):
            if curr_board[i] == "1":
                curr_board[i] = "X"
            elif curr_board[i] == "2":
                curr_board[i] = "O"
            else:
                curr_board[i] = ""
                
        return curr_board
    
    def check_valid(self, poss):
        temp = self.get_board()
        if temp[poss] == "":
            return True


class Game:
    ''' This class provides method to play and manupulate the game'''

    def __init__(self):
        self.board = Board() # creating board's object
        self.player = 1 # assign the initial player to 1 that means X always plays first
        self.running = True
        #self.board.display_board() # display initial board on terminal (for testing or debuging)
        
        
    
    def make_move(self, action):
        ''' This method Makes a move on the game board and checks if the game has ended.'''
        
        # call mark down for make move
        self.board.mark_down(action, self.player)
        
        #self.board.display_board() # display the board (for testing or debuging)
        
        # checks if the game has ended
        self.check_end()
        
        # Switches to the next player's turn.
        self.next_turn()
    
    def check_end(self):
        global head # head using for web version
        case = self.board.is_final_state()
        if case == 1:
            #print("X win")
            head = "X win"
            self.running = False
        elif case == 2:
            #print("O win")
            head = "O win"
            self.running = False
        elif len(self.board.valid_moves) == 0:
            #print("Draw")
            head = "Draw"
            self.running = False
    
    def next_turn(self):
        self.player = self.player % 2 + 1
    
    def reset(self):
        ''' Reset the game'''
        self.__init__()

def human(board):
    ''' Using for playing on console only '''
    move = int(input("เลือกช่อง 1-9: ")) - 1
    # if the input that the player fill is not valid (not in valid moves)
    while move not in board.valid_moves:
        move = int(input("! กรุณาเลือกช่อง 1-9 !: ")) - 1   
    return move

def rnd_bot(board):
    ''' Create a random bot that chooses a random position from current valid moves'''
    valid_moves = board.valid_moves
    # avoid it from random the None list
    if len(valid_moves) != 0:
        return random.choice(valid_moves)
    return None


def testing():
    game = Game()
    board = game.board
    #agentMaxV = AI.AgentMaxV(board,2)
    agentMinimax = AI.AgentMinimax(board, 2)

    i = 0
    while 1:
        if game.running == True:
            if game.player == 1 and game.running == True:
                game.make_move(human(board))
                print()
            if game.player == 2 and game.running == True :
                game.make_move(agentMinimax.eval())
                print() 
        else:
            print("----------------------------")
            game.reset()
            board = game.board
            #agentMaxV = AI.AgentMaxV(board,2)
            agentMinimax = AI.AgentMinimax(board, 2)

#testing()


# The codes below are usig for deploy The tictactoe game with AI on web

# Create a list that represents a cell in the table (Tic Tac Toe board table 3*3)
table = ["top_left","top_mid","top_right","mid_left","mid_mid","mid_righ","bot_left","bot_mid","bot_right"]

# The title above table
head = "Tic Tac Toe"

def reset(gamemode):
    ''' this function use for reset the game and send gamemode to new game
    '''
    global board, head, agentMaxV, agentMinimax
    game.reset()
    board = game.board
    
    if gamemode == 1:
        head = "Player vs Player"
    if gamemode == 2:
        head = "Player vs Random (Easy)" 
    if gamemode == 3:
        head = "Player vs AgentMaxV (Normal)"
        agentMaxV = AI.AgentMaxV(board, 2)
    if gamemode == 4:
        head = "Player vs AgentMinimax (Hard)"
        agentMinimax = AI.AgentMinimax(board, 2)


# initial Flask framework
app = Flask('__name__')

# main route

@app.route('/', methods=['GET', 'POST'])
def main():
    global game, gamemode
    game = Game()
    gamemode = 1
    reset(gamemode)
    return (render_template('main.html',show_position=copy.deepcopy(board.get_board()),head=head))



@app.route('/play', methods=['GET','POST'])
def play():
    global game, board, head, gamemode
    if request.method == 'POST':
        if game.running == True:
            for (i,v) in enumerate(table):
                if request.form.get(v) == 'click':
                    if board.check_valid(i):
                        game.make_move(i)
                    
                        # choose the competitor based on game mode
                        if game.running == True:
                            if gamemode == 2:
                                move = rnd_bot(board)
                                if move is not None:
                                    game.make_move(move)
                            
                            if gamemode == 3:
                                move = agentMaxV.play()
                                if move is not None:
                                    game.make_move(move)
                                
                            if gamemode == 4:
                                move = agentMinimax.eval()
                                if move is not None:
                                    game.make_move(move)
    
    return (render_template('main.html',show_position=copy.deepcopy(board.get_board()),head=head))


# route each game mode to send the game mode to the main route
@app.route('/gamemode1', methods=['GET','POST'])
def gamemode1():
    global game, board, head, gamemode
    gamemode = 1
    reset(gamemode)
    return (render_template('main.html',show_position=copy.deepcopy(board.get_board()),head=head))

@app.route('/gamemode2', methods=['GET','POST'])
def gamemode2():
    global game, board, head, gamemode
    gamemode = 2
    reset(gamemode)
    return (render_template('main.html',show_position=copy.deepcopy(board.get_board()),head=head))

@app.route('/gamemode3', methods=['GET','POST'])
def gamemode3():
    global game, board, head, gamemode
    gamemode = 3
    reset(gamemode)
    return (render_template('main.html',show_position=copy.deepcopy(board.get_board()),head=head))

@app.route('/gamemode4', methods=['GET','POST'])
def gamemode4():
    global game, board, head, gamemode
    gamemode = 4
    reset(gamemode)
    return (render_template('main.html',show_position=copy.deepcopy(board.get_board()),head=head))


# run the program
if __name__ == '__main__' :
    app.run(debug=True)
  
    