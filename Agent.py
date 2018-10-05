'''
Created on Sep 26, 2018

@author: Caitlin ☼
'''

from Checkers import Checkers
from test.test_typechecks import Integer
from tkinter.constants import CURRENT

class GameTree(object):
    
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
    #    Else Case: 
    
    
    # board: the given board state
    # player: whose turn we're checking for
    # depth: How many moves ahead being checked still. Depth=1 means one move's worth of  evals down to check. Used for establishing base-case
    def ABTreeBearch(self,board,player,depth,currentBest=(9999*(-1)^depth)):
        bestMove = []
        for move in self.movesAvailable(board,player):
            moveBoard = Checkers.movePiece(self, board[:], player, move, False)
            moveResult = self.ABTreeSearch(self,moveBoard,player*(-1),depth-1,currentBest)
            if (player == self.player) & (moveResult[4] > currentBest):   
                # this move is better than previous moves and we're going for max
                currentBest = moveResult[4]
                bestMove = moveResult[:]
            elif (player != self.player) & (moveResult[4] > currentBest):   
                # this move is better than previous moves and we're going for max
                currentBest = moveResult[4]
                bestMove = moveResult[:]
        
        if depth > 1: # if this is not the base-case, run below recursion first
            moveSet = self.ABTreeSearch(board, player, depth - 1)
        # end if
        
        
        
        
        
        
        return bestMove
    # end ABTreeSearch
    
    # board: the given board state
    # player: whose turn we're checking for
    # depth: How many moves ahead being checked still. Depth=1 means one move's worth of  evals down to check. Used for establishing base-case
    def ABTreeSearch(self,board,player,depth):
        bestMove = []
         
        currentParent = Node(board)
        for level in range(depth):  # for every level down to max depth
            for i in range(level):
                currentParent = currentParent.getChildren()
            
            for move in self.movesAvailable(board,player):
                moveBoard = Checkers.movePiece(self, board[:], player, move, False)
                moveResult = self.ABTreeSearch(self,moveBoard,player*(-1),depth-1,currentBest)
                if (player == self.player) & (moveResult[4] > currentBest):   
                    # this move is better than previous moves and we're going for max
                    currentBest = moveResult[4]
                    bestMove = moveResult[:]
                elif (player != self.player) & (moveResult[4] > currentBest):   
                    # this move is better than previous moves and we're going for max
                    currentBest = moveResult[4]
                    bestMove = moveResult[:]
            
            if depth > 1: # if this is not the base-case, run below recursion first
                moveSet = self.ABTreeSearch(board, player, depth - 1)
            # end if
        
        
        
        
        
        
        return bestMove
    # end ABTreeSearch
    
    
    # state:  a board being considered for moves
    # player: who's pieces are being considered
    def movesAvailable(self, state, player, parent, isJump):
        moveSet = []
        
        for i in range(0,len(state)):           # for all vertical bars
            for j in range (0,len(state[i])):   # for all horizontal spaces in given vertical bar
                if state[i][j] == player:       # if current space is the player's piece, check the following
                    if Checkers.checkValidMove(state, player, [i,j,i-1,j-1], False): # hop UL
                        moveSet += [[i,j,i-1,j-1]]
                        parent.addChild(Checkers.movePiece(self, board, turn, isJump))
                    if Checkers.checkValidMove(state, player, [i,j,i-1,j+1], False): # hop UR
                        moveSet += [[i,j,i-1,j+1]]
                    if Checkers.checkValidMove(state, player, [i,j,i+1,j-1], False): # hop DL
                        moveSet += [[i,j,i+1,j-1]]
                    if Checkers.checkValidMove(state, player, [i,j,i+1,j+1], False): # hop DR
                        moveSet += [[i,j,i+1,j+1]]
                    if Checkers.checkValidMove(state, player, [i,j,i-2,j-2], isJump): # jump UL
                        moveSet += [[i,j,i-2,j-2]]
                    if Checkers.checkValidMove(state, player, [i,j,i-2,j+2], isJump): # jump UR
                        moveSet += [[i,j,i-2,j+2]]
                    if Checkers.checkValidMove(state, player, [i,j,i+2,j-2], isJump): # jump DL
                        moveSet += [[i,j,i+2,j-2]]
                    if Checkers.checkValidMove(state, player, [i,j,i+2,j+2], isJump): # jump DR
                        moveSet += [[i,j,i+2,j+2]]
        
        return moveSet
    # end movesAvailable  
# end Class



class Node:
    children = []
    name = ""
    
    def __init__(self,value,name):
        self.value = value  # for Checkers, this is the board state
        self.name = name    # for Checkers, this is the move
        
    def addChild(self,Node):
        self.children += Node
    
    def getChildren(self):
        return self.children
    
    def getValue(self):
        return self.value
#end Class

##########################
###### MINI-MAX A-B ######
##########################

class AlphaBeta:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, game_tree):
        self.game_tree = game_tree  # GameTree
        self.root = game_tree.root  # GameNode
        return

    def alpha_beta_search(self, node):
        infinity = float('inf')
        best_val = -infinity
        beta = infinity

        successors = self.getSuccessors(node)
        best_state = None
        for state in successors:
            value = self.min_value(state, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = state
        print ("AlphaBeta:  Utility Value of Root Node: = " + str(best_val))
        print ("AlphaBeta:  Best State is: " + best_state.Name)
        return best_state

    def max_value(self, node, alpha, beta):
        print ("AlphaBeta-->MAX: Visited Node :: " + node.Name)
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = -infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = max(value, self.min_value(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta):
        print ("AlphaBeta-->MIN: Visited Node :: " + node.Name)
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = min(value, self.max_value(state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value
    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes...
    def getSuccessors(self, node):
        assert node is not None
        return node.children

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, node):
        assert node is not None
        return len(node.children) == 0

    def getUtility(self, node):
        assert node is not None
        return node.value



