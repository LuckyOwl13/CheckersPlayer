'''
Created on Sep 7, 2018

@author: Caitlin ☼
'''

from Checkers import Checkers

class Agent(object):
    
    board = Checkers()
    
    
    def __init__(self,board,depth):
        self.board = board 
        self.depth = depth
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
        
        for movesAvailable(state):
            
            
            
        
        if depth > 1: # if this is not the base-case, run below recursion first
            moveSet = self.ABTreeSearch(board, turn, depth - 1)
        # end if
        
        
        
        
        
        
        
    # end ABTreeSearch
    
    def movesAvailable(self, state):
        
    #e end movesAvailable
    
    
# end Class