'''
Created on Sep 7, 2018

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
    def ABTreeSearch(self,board,turn,depth):
        moveSet = []
        
        for state in self.movesAvailable(state):
            print("nice")
            
            
        
        if depth > 1: # if this is not the base-case, run below recursion first
            moveSet = self.ABTreeSearch(board, turn, depth - 1)
        # end if
        
        
        
        
        
        
        
    # end ABTreeSearch
    
    # state:  a board being considered for moves
    # player: who's pieces are being considered
    def movesAvailable(self, state, player):
        moveSet = []
        
        for i in range(0,len(state)):
            for j in range (0,len(state[i])):
                if state[i][j] == player:
                    if 
        
        
        
        
        
        return [state]
    #e end movesAvailable
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# end Class