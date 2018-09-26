'''
Created on Sep 26, 2018

@author: Caitlin ☼
'''

from Checkers import Checkers

class Agent(object):
    
    checkers = Checkers()
    depth = 0
    player = 0
    
    
    def __init__(self,checkers,depth,player):
        self.checkers = checkers    # The board being played on
        self.depth = depth          # How many moves ahead does the agent check
        self.player = player        # If the agent is R (-1) or B (1) 
    # end 
    
    # The way to check for all moves is a tree-search algorithm;
    # The most efficient tree-search algorithm is Alpha-Beta (AB) Pruning;
    # AB-Pruning requires depth-first search.
    # 
    # The way I will approach this with recursion bc I can't be stopped.
    #    Base Case: Depth = 1
    #    
    def ABTreeSearch(self,board,player,depth):
        moveSet = []
        
        for state in self.movesAvailable(state,player):
            print("nice")
            
            
        
        if depth > 1: # if this is not the base-case, run below recursion first
            moveSet = self.ABTreeSearch(board, turn, depth - 1)
        # end if
        
        
        
        
        
        
        
    # end ABTreeSearch
    
    # state:  a board being considered for moves
    # player: who's pieces are being considered
    def movesAvailable(self, state, player):
        moveSet = []
        
        for i in range(0,len(state)):           # for all vertical bars
            for j in range (0,len(state[i])):   # for all horizontal spaces in given vertical bar
                if state[i][j] == player:       # if current space is the player's piece, check the following
                    if Checkers.checkValidMove(state, player, [i,j,i-1,j-1], False): # hop UL
                        moveSet += [[i,j,i-1,j-1]]
                    if Checkers.checkValidMove(state, player, [i,j,i-1,j+1], False): # hop UR
                        moveSet += [[i,j,i-1,j+1]]
                    if Checkers.checkValidMove(state, player, [i,j,i+1,j-1], False): # hop DL
                        moveSet += [[i,j,i+1,j-1]]
                    if Checkers.checkValidMove(state, player, [i,j,i+1,j+1], False): # hop DR
                        moveSet += [[i,j,i+1,j+1]]
                    if Checkers.checkValidMove(state, player, [i,j,i-2,j-2], False): # jump UL
                        moveSet += [[i,j,i-2,j-2]]
                    if Checkers.checkValidMove(state, player, [i,j,i-2,j+2], False): # jump UR
                        moveSet += [[i,j,i-2,j+2]]
                    if Checkers.checkValidMove(state, player, [i,j,i+2,j-2], False): # jump DL
                        moveSet += [[i,j,i+2,j-2]]
                    if Checkers.checkValidMove(state, player, [i,j,i+2,j+2], False): # jump DR
                        moveSet += [[i,j,i+2,j+2]]
        
        return moveSet
    #e end movesAvailable
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# end Class