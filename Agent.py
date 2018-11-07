'''
Created on Sep 26, 2018

@author: Caitlin ☼
'''

from Checkers import Checkers
from test.test_typechecks import Integer
from tkinter.constants import CURRENT
import time
import copy
from test.test_binop import isint

class GameTree(object):
    
    checkers = None
    depth = 0
    player = 0
    
    root = None
    
    
    def __init__(self,checkers,depth,player):
        self.checkers = checkers    # The board being played on
        self.depth = depth          # How many moves ahead does the agent check
        self.player = player        # If the agent is R (-1) or B (1) 
        
    # end 
    
    # board: the given board state BEFORE the stated move
    # player: whose turn we're checking for
    # depth: How many moves ahead being checked still. Depth=1 means one move's worth of evals down to check. Used for establishing base-case
    # move: the initial move to be performed on the given board
    def fillTree(self,board,player,depth,move):
        top = Node(move,copy.deepcopy(board))
        
        #    generate the boardstate root's move would make 
        newBoard = Checkers.movePiece(self.checkers, copy.deepcopy(board), player, move, False, False)
        
        if depth >= 2: # This will not go beyond depths of 2 (Add lowest children cared about)
            availMoves = Checkers.movesAvailable(Checkers(), copy.deepcopy(newBoard), ((-1)*player), False)
            for i in range(0,len(availMoves)):
                
                newChild = self.fillTree(copy.deepcopy(newBoard), ((-1)*player), (depth - 1), availMoves[i])
                #    make a new child node given A) the move it represents, and B) the boardstate that represents (created by movePiece)
                top.addChild(newChild)
#                 print("Running on depth = %s" % (depth-1))
#                 print("just generated a child")
            #    end for
        #    end if
#         print("Is depth (%s) >= 3?" % depth)
#         if depth >= 3: # This will not go beyond depths of 3 (so it still generates grandchildren)
#             print("\t\tGenerating grandchildren")
#             for i in range(0,len(childs)):
#                 grandChild = self.fillTree(childs[i].getValue(), ((-1)*player), depth, childs[i].getName())
#                 top.addChild(grandChild)
#             # end for 
#         # end if
        
        return top
    # end filllTree
     
    def printTree(self):
        print(self.root)#.toString(0)
    
# end Class



class Node:
    name = None
    value = None
    children = []
    
    def __init__(self,name,value):
        self.name = name    # for Checkers, this is the move
        self.value = value  # for Checkers, this is the board state
        
    def addChild(self,child):
        if len(self.children) is 0:
            self.children = [child]
        else:
            self.children += [child]
    
    def getChildren(self):
        return self.children
    
    def getName(self):
        return self.name
    
    def getValue(self):
        return self.value
    
    def clearChildren(self):
        self.children = []
    
#     def toString(self, level):
#         print ('\t' * level + '%s' % self)
# #         print (len(self.children))
#         for i in range(0,len(self.children)):
#             self.children[i].toString(level+1)
    def __repr__(self,level=0):
        ret = "\t"*level+repr(self.name)+"\n"
        if len(self.children) > 0:
            for i in range(0,len(self.children)):
                ret += self.children[i].__repr__(level+1)
        return ret
#         return str(self.name)
#end Class

##########################
###### MINI-MAX A-B ######
##########################

class AlphaBeta:
    
    infinity = float('inf')
    player = 0
    depth = 0
    
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, depth, player):        
        self.depth = depth
        self.player = player
        return

    def alpha_beta_search(self, node):
        best_val = -self.infinity
        beta = self.infinity

        successors = self.getSuccessors(node)
        best_state = None
        for state in successors:
            value = self.min_value(state, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = state
        print ("AlphaBeta:  Utility Value of Root Node: = " + str(best_val))
        print ("AlphaBeta:  Best State is: " + str(best_state.name))
        return best_state   # returns a node

    def max_value(self, node, alpha, beta):
#         print ("AlphaBeta-->MAX: Visited Node :: " + str(node.name))
        if self.isTerminal(node):
            return self.getUtility(node)
        value = -self.infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = max(value, self.min_value(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta):
#         print ("AlphaBeta-->MIN: Visited Node :: " + str(node.name))
        if self.isTerminal(node):
            return self.getUtility(node)
        value = self.infinity

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
        return self.scoreNode(node)
    
    def scoreNode(self, node):
        print()
        board = Checkers.movePiece(checkers, node.value, self.player*((-1)**(self.depth+1)), node.name, False, False)
        score = 0
        
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):   # for every space in the board
                if isint(board[i][j]):          # if it is an integer
                    score += self.player * board[i][j]  # add score (accounting for who we're emulating) to score
        # end for loops
#         print(str(node.name) + " has a score of " + str(score) + " for player " + str(self.player))
#         Checkers.printBoard(self, node.value)
        return score    # when done with that, return score



if __name__ == "__main__":
    print("We're Agenting in here")
    
    checkers = Checkers()
    
    i = 3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     
#     print("AI will play team B")
#     black = AlphaBeta(3,1)
#      
#     while checkers.nextTurn():
#         checkers.printBoard(checkers.board)
#         print("It is %s's turn" % checkers.whoseTurn())
#         if checkers.whoseTurn() == "R":
#             checkers.board = checkers.getMove(copy.deepcopy(checkers.board),checkers.turn,False)
#         else:
#             best_move = black.alpha_beta_search(Node([0,0,0,0], copy.deepcopy(checkers.board))).name    # Find best move, save it as best_move
#             checkers.board = checkers.movePiece(copy.deepcopy(checkers.board), checkers.turn, best_move, False, False)  # Make that move
#             
#         checkers.anyKings()
#         print("~~~~~~~~~~~~~~~ Next Turn")  # signal it is the AI's turn
#     # end while     
#      
#     print("Player %s cannot make any moves !" % ('B' if (checkers.turn == 1) else 'R'))
#     print("Player %s wins !" % ('R' if (checkers.turn == 1) else 'B'))
    
    
     
    times = []
    print("\nabout to run with depth = %i" % i)
    start_time = time.time()
      
    moveSet = Node([0,0,0,0],checkers.board)
    for move in checkers.movesAvailable(checkers.board, checkers.turn, False):
        gametree = GameTree(checkers,i,checkers.turn)  
        moveSet.addChild(gametree.fillTree(gametree.checkers.board, gametree.player, gametree.depth, move))
    elapsed_time = time.time() - start_time
    times += [elapsed_time]
    print("done !")
#   
    abp = AlphaBeta(i,1)
    best_node = abp.alpha_beta_search(moveSet)
#     print("Printing again: " + str(best_node.name))
    
    print("Depth == %i, took %s seconds" % (i, elapsed_time))
    
    
    
# end FILE    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    