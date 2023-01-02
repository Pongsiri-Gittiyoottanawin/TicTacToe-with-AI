import copy
import numpy
import random

winning_combinations = [[0,1,2], [3,4,5], [6,7,8], 
                        [0,3,6], [1,4,7], [2,5,8], 
                            [0,4,8], [2,4,6]]

class AgentMaxV:
    ''' The AgentMax class is an AI agent that plays Tic-Tac-Toe by using an objective function 
        it chooses the action that gives the highest score from the function called the V function
        The formula to calculate V functions is 
        V(b) = X(b) - O(b) + 1 
        X(b) is the summation of X symbols in the board that hasn't any O symbol in each line
        O(b) is the summation of the O symbols in the board that hasn't any X symbol in each line  
        This method was adapted from Parinya Sanguansat. Artificial Intelligence with Machine Learning
    '''

    def __init__(self, board, player):
        self.board = board
        self.player = player
    
    def determine_side(self):
        ''' determines which positions on the game board belong to the agent's player 
            and which belong to the opponent.
        '''
        # if it's play as X
        if self.player == 1:
            self.side = self.board.x_positions
            self.opp = self.board.o_positions
        # if it's play as O
        else:
            self.side = self.board.o_positions
            self.opp = self.board.x_positions
    
    def play(self):
        ''' determines the next move to make by evaluating the potential value of each possible move 
            and choosing the move that maximizes the value.
        '''
        self.determine_side()
        valid_moves = self.board.valid_moves
        
        V = [-100] * 9 # Create a list V to store each value from each move
        # Try every possible move to find the best move (the move that give highest value)
        for move in valid_moves: 
            temp_move = self.side + [move]
            # calculate a value of the move position by calling evaluate the function then store it in V
            V[move], critical_moves = self.eval(temp_move)
            # the critical move is the list that stores the positions that can make the opposite win in the next turn
            if len(critical_moves) > 2:
                # we don't want to let the opposite win so we will block it!
                moves = [move for move in critical_moves if move in valid_moves]
                return random.choice(moves)
        
        # chose the best moves
        maxV = max(V)
        # find all the index that value is equal to maxV
        ibest_moves = [move for move,value in enumerate(V) if value == maxV]
        return random.choice(ibest_moves)
    
    def eval(self, temp_move):
        ''' Calculate V function'''
        opp_val, self_val, critical_moves = self.cal_val(temp_move)
        
        # self_val is The summation of self-symbols that hasn't any opposite symbol in each line.
        # opp_val is The summation of opposite symbol that hasn't any self symbol in the line.
        return 1 + self_val - opp_val, critical_moves
    
    def cal_val(self, temp_move):
        ''' Calculate the score of each symbol that meet the conditions ( X(b), O(b) )'''
        opp_val = self_val = 0
        critical_moves = []
        for win in winning_combinations:
            self_count = [i in temp_move for i in win]
            opp_count = [i in self.opp for i in win]
            
            # Calculate other score
            if not any(self_count):
                temp_opp_count = opp_count.count(True)
                opp_val += temp_opp_count
                # If current state has the criticalmove
                if temp_opp_count == 2:
                    critical_moves = win
            
            # Calculate self score
            if not any(opp_count):
                self_val += self_count.count(True)
        return opp_val, self_val, critical_moves
        
class AgentMinimax:
    ''' An AI agent that plays Tic-Tac-Toe using the minimax algorithm which is a Backtracking Algorithm 
    that is used in decision-making to find the optimal move for a player in a two-player game. 
    It works by using recursive function called minimax to explore all the possible moves and game states in the game tree,
    starting from the root node (which represents the current state of the game) 
    and going all the way down to the leaf nodes (which represent the final stages of the game) for considering the scores of all possible moves at each step 
    '''
    
    def __init__(self,board, player=2):
        self.board = board
        self.player = player
    
    def minimax(self, board, maximizing):
        '''  This is the core recursive function of the minimax algorithm.
        At each node of the tree, the algorithm determines the optimal move for the current player, 
        these returned scores determine the optimal move for the current player at the current node. 
        If the agent is trying to maximize their score, it will choose the move that leads to the child node with the highest score. 
        If the agent is trying to minimize the score of their opponent, it will choose the move that leads to the child node with the lowest score.
        it will continue recursively until reaches the terminal state 
        '''
        
        # check if reach the terminal case
        case = board.is_final_state()
        
        # player 1 wins
        if case == 1:
            return 1, None
        
        # player 2 wins
        if case == 2:
            return -1, None
        
        # draw
        elif len(board.valid_moves) == 0:
            return 0, None
        
        # X's turn
        if maximizing:
            max_eval = -100
            best_move = None
            valid_moves = board.valid_moves
            
            for move in valid_moves:
                temp_board = copy.deepcopy(board)
                temp_board.mark_down(move, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        
        # O's trun
        elif not maximizing:
            min_eval = 100
            best_move = None
            valid_moves = board.valid_moves
            
            for move in valid_moves:
                temp_board = copy.deepcopy(board)
                temp_board.mark_down(move, 2)
                #temp_board.display_board()
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move
        
    
    def eval(self):
        main_board = copy.deepcopy(self.board)
        # avoid the large number of recursion when play first as X by using random
        if len(main_board.valid_moves) == 9:
            move = random.choice(main_board.valid_moves)
        else:
            # Determine if Agent is trying to maximize or minimize the score
            maximizing = True if self.player == 1 else False
            eval, move = self.minimax(main_board, maximizing)
            
        return move  