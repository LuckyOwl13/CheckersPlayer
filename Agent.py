'''
Created on Sep 26, 2018

@author: Caitlin ☼
'''

from Checkers import Checkers
from test.test_typechecks import Integer
from tkinter.constants import CURRENT
import time
import copy

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
#         Checkers.printBoard(self, board)
#         tempBoard = copy.deepcopy(board)
        newBoard = Checkers.movePiece(self.checkers, copy.deepcopy(board), player, move, False, False) 
#         Checkers.printBoard(self, board)
        
        
#         print("Is depth (%s) >= 2?" % depth)
        if depth >= 2: # This will not go beyond depths of 2 (Add lowest children cared about)
#             print("\tGenerating children")
#             print("\tFor reference,")
#             Checkers.printBoard(self, newBoard.copy())
            availMoves = Checkers.movesAvailable(Checkers(), copy.deepcopy(newBoard), ((-1)*player), False)
#             print("\t%i" % len(availMoves))
            #             childs = []
            for i in range(0,len(availMoves)):
                
#                 nextBoard = Checkers.movePiece(self.checkers, newBoard, ((-1)*player), availMoves[i], False, False)
                newChild = self.fillTree(copy.deepcopy(newBoard), ((-1)*player), (depth - 1), availMoves[i])
                #    make a new child node given A) the move it represents, and B) the boardstate that represents (created by movePiece)
#                 newChild = Node(availMoves[i],Checkers.movePiece(self.checkers, newboard, ((-1)*player), availMoves[i], False, False))
#                 childs += [newChild]
#                 print(childs)
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
#         print("at level %s" % level)
#         print("# of children: %s" % len(self.children))
        if len(self.children) > 0:
            for i in range(0,len(self.children)):
#                 print("adding next child: #%s" % i)
                ret += self.children[i].__repr__(level+1)
        return ret
#         return str(self.name)
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



if __name__ == "__main__":
    print("We're Agenting in here")
    
    times = []
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for i in range(1,11):
        checker = Checkers()
        checker.nextTurn()
        gametree = GameTree(checker,i,checker.turn)
        
        print("\nabout to run with depth = %i" % i)
        start_time = time.time()
        gametree.root = gametree.fillTree(gametree.checkers.board, gametree.player, gametree.depth, [5,0,4,1])
        elapsed_time = time.time() - start_time
        times += [elapsed_time]
        print("done !")
    #     print(gametree.root)
    #     print(len(gametree.root.getChildren()))
    #     print(gametree.root.getChildren())
        gametree.printTree()
        
        print("Depth == %i, took %s seconds" % (i, elapsed_time))
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     checker = Checkers()
#     checker.nextTurn()
#     gametree = GameTree(checker,2,checker.turn)
#      
#     print("\nabout to run with depth = 2")
#     start_time = time.time()
#     gametree.root = gametree.fillTree(gametree.checkers.board, gametree.player, gametree.depth, [5,0,4,1])
#     elapsed_time = time.time() - start_time
#      
#     print("done ! Took %s seconds" % (elapsed_time))
# #     print(gametree.root)
# #     print(len(gametree.root.getChildren()))
# #     print(gametree.root.getChildren())
#     gametree.printTree()
#     
#     print("Again, took %s seconds" % (elapsed_time))
#      
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     checker = Checkers()
#     checker.nextTurn()
#     gametree = GameTree(checker,5,checker.turn)     
#       
#     print("\nabout to run with depth = 5")
#     start_time = time.time()
#     gametree.root = gametree.fillTree(gametree.checkers.board, gametree.player, gametree.depth, [5,0,4,1])
#         
#     elapsed_time = time.time() - start_time
#         
#     print("done ! Took %s seconds" % (elapsed_time))
# #     print(gametree.root)
# #     print(gametree.root.getChildren())
#     gametree.printTree()
#     
#     print("Again, took %s seconds" % (elapsed_time))
    
    
    print("All times:")
    for i in range(0,len(times)):
        print("\tDepth of %i => time of %s seconds (%s minutes)" % (i, times[i], (times[i]/60)))
    
    
    
    
    
    
    
    
    