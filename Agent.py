'''
Created on Sep 26, 2018

@author: Caitlin ☼
'''

from Checkers import Checkers
import time
import copy
import random
from test.test_binop import isint
import os, sys

# Nabbed the following from: https://stackoverflow.com/questions/8391411/suppress-calls-to-print-python
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
        
# end of nabbing

class TreeGenerator(object):
    
    checkers = None
    depth = 0
    player = 0
    
    root = None
    
    
    def __init__(self,checkers,player,depth):
        self.checkers = checkers    # an instance of Checkers for passing as 'self' when Checkers methods need them
        self.depth = depth          # How many moves ahead does the agent check
        self.player = player        # If the agent is R (-1) or B (1) 
        
    # end 
    
    # board: the given board state BEFORE the stated move
    # player: whose turn we're checking for
    # depth: How many moves ahead being checked still. Depth=1 means one move's worth of evals down to check. Used for establishing base-case
    # move: the initial move to be performed on the given board
    def fillSubTree(self,board,player,depth,move):
        top = Node(move,copy.deepcopy(board))
        
        #    generate the boardstate root's move would make 
        newBoard = Checkers.movePiece(self.checkers, copy.deepcopy(board), player, move, False, False)
        
        if depth > 1: # This will not go beyond depths of 1 (Add lowest children cared about)
            availMoves = Checkers.movesAvailable(Checkers(), copy.deepcopy(newBoard), ((-1)*player), False)
            for i in range(0,len(availMoves)):
                
                newChild = self.fillSubTree(copy.deepcopy(newBoard), ((-1)*player), (depth - 1), availMoves[i])
                #    make a new child node given A) the move it represents, and B) the boardstate that represents (created by movePiece)
                top.addChild(newChild)
        
        return top
    # end filllTree
    
    def getTree(self, board):
        
        tree = Node([0,0,0,0],[])   # create dummy node
        for move in Checkers.movesAvailable(Checkers(), board, self.player, False):  # for all moves available to make
            tree.addChild(self.fillSubTree(board, self.player, 1, move)) # fill their trees and add to the 
# TODO ~~~~~~~~~~~~~~~~~~~~ Doesn't need to do this
        return tree
    # end getTrees()
     
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
    treeGen = None
    
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, depth, player):        
        self.depth = depth
        self.player = player
        return

    def alpha_beta_search(self, node):
        best_val = -9999
        beta = self.infinity

        successors = node.getChildren()
        best_states = None
        for state in successors:
            value = self.min_value(state, best_val, beta, self.depth)
            if value == best_val:   # if this node is same value as current best node
                best_states += [state]  # add it to the list
            elif value > best_val:  # else if this node is better than current nodes
                best_val = value        # wipe the slate
                best_states = [state]
#         print ("AlphaBeta:  Utility Value of Root Node: = " + str(best_val))
#         print ("AlphaBeta:  Best State is: " + str(best_state.name))
        if best_states == None:  # if there were no possible states (e.g loses)
            return Node([-1,-1,-1,-1],[])
        else:
            return best_states[random.randint(0,len(best_states)-1)]  # returns a random node of equally best value

    def max_value(self, node, alpha, beta, depth):
#         print ("AlphaBeta-->MAX: Visited Node :: " + str(node.name))
        if depth == 1:
            return self.getUtility(node)
        value = -self.infinity

        successors = self.getSuccessors(node, self.player*(-1))
        for state in successors:
            value = max(value, self.min_value(state, alpha, beta, depth-1))
            if value >= beta:
                if beta == self.infinity: print("~~~~~~~~~ Value has an error: value = " + str(value))
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta, depth):
#         print ("AlphaBeta-->MIN: Visited Node :: " + str(node.name))
        if depth == 1:
            return self.getUtility(node)
        value = self.infinity

        successors = self.getSuccessors(node, self.player)
        for state in successors:
            value = min(value, self.max_value(state, alpha, beta, depth-1))
            if value <= alpha:  # if the current value is lower than the previous lowest value so far
                if alpha == -self.infinity: print("~~~~~~~~~ Value has an error: value = " + str(value))
                return value    # return it, it's now our chosen value
            beta = min(beta, value) #otherwise set it as our lowest here (if it is) then keep going

        return value
    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes...
    def getSuccessors(self, node, player):
        assert node is not None
        return treeGen.fillSubTree(node.value, player, 2, node.name).getChildren()

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, node):
        assert node is not None
        return len(node.children) == 0

    def getUtility(self, node):
        assert node is not None
        return self.scoreNode(Checkers.movePiece(checkers, node.value, self.player*((-1)**(self.depth+1)), node.name, False, False))
    
    def scoreNode(self, board):
        score = 0
        
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):   # for every space in the board
                if isint(board[i][j]):          # if it is an integer
                    score += self.player * board[i][j]  # add score (accounting for who we're emulating) to score
        # end for loops
#         print(str(node.name) + " has a score of " + str(score) + " for player " + str(self.player))
#         Checkers.printBoard(self, node.value)
        return score    # when done with that, return score

# end ABPruner



if __name__ == "__main__":
    print("We're Agenting in here")
    
    filePath = "MoveSets/"
    saveString = ""
    
    redMaxDepth = 8     # deepest Red will go
    blackMaxDepth = 8   # deepest Black will go
    turnMax = 100   # max # of turns
    
    gameMax = 10
    print('Will play %i games per match' % gameMax)
    for gameNum in range(1,gameMax+1):  # play this many games
        for redDepth in range(1,redMaxDepth+1):         # with this deep a red AI
            for blackDepth in range(1,blackMaxDepth+1):   # and  this deep a black AI 
                with HiddenPrints():
                    saveString = ""     # clear out saveString
                    checkers = Checkers()
    #                 checkers.nextTurn()    # uncomment for Black to go firsts
                    
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    print("\n\n\n")
                    print("AI will play full game of up to " + str(turnMax) + " moves")
                    print("Red depth = %i, Black depth = %i" % (redDepth,blackDepth))
                    red = AlphaBeta(redDepth,-1)
                    black = AlphaBeta(blackDepth,1)
                    
                    counter = 0     # counter for turns taken
                    concede = False # flag for an AI concedes
                    while checkers.nextTurn() and not concede and counter < turnMax:
                        checkers.printBoard(checkers.board)
                        player = checkers.whoseTurn()
                        print("It is %s's turn" % player)
                        if player == "R":
                            depth = redDepth
                        else:
                            depth = blackDepth
                            
                        start_time = time.time()
                        treeGen = TreeGenerator(copy.deepcopy(checkers), checkers.turn,depth)
                        tree = treeGen.getTree(copy.deepcopy(checkers.board))
                        print("~~~~~~~~ Time to generate potential moves: " + str(time.time() - start_time))
                        start_time = time.time()
                        best_move = None
                        if player == "R":
                            best_move = red.alpha_beta_search(tree)    # Find best move, save it as best_move
                        else:
                            best_move = black.alpha_beta_search(tree)    # Find best move, save it as best_move
                        print("~~~~~~~~ Time to ABP through said tree: " + str(time.time() - start_time))
                        print(str(best_move))
                        if (best_move.name == [-1,-1,-1,-1]):
                            concede = True
                        else:
                            checkers.board = checkers.movePiece(copy.deepcopy(checkers.board), checkers.turn, best_move.name, False, False)  # Make that move
                            
                            saveString += str(best_move.name) + "\n"
                            
                            checkers.anyKings()
                            counter += 1
                            print("~~~~~~~~~~~~~~~ Next Turn (#%s)" % counter)  # signal it is the AI's turn
                        
                    # end while     
                    
                    if concede:
                        checkers.turn = checkers.turn*(-1)  
                        print("Player %s has conceded !" %
                                    (('B' if (checkers.turn == 1) else 'R')))
                    elif counter >= turnMax: # if max # of turns reached
                        print("No more moves allowed!")
                        print("Player %s has the better board !" %   
                                ('R' if (red.scoreNode(checkers.board) > black.scoreNode(checkers.board)) else 'B'))
                    else:   # if the game ended normally
                        print("Player %s cannot make any moves !" % ('B' if (checkers.turn == 1) else 'R'))
                    
                    
                    winner = 'R' if (checkers.turn == 1) else 'B'
                    print("Player %s wins !" % winner)
         
                    file = open(filePath + "gameR%iB%iG%i.txt" % (redDepth,blackDepth,gameNum), "w")  # create or overwrite a file 
                    file.write(winner + "\n" + saveString)  # write saveString to file
                # end with HiddenPrints()
                print("Finished game %s red %i black %i" % ('{:02d}'.format(gameNum),redDepth,blackDepth))
     
     
     
     
     
     
#     print("AI will play team B")
#     black = AlphaBeta(depth,1,checkers)
#        
#     while checkers.nextTurn():
#         checkers.printBoard(checkers.board)
#         print("It is %s's turn" % checkers.whoseTurn())
#         if checkers.whoseTurn() == "R":
#             checkers.board = checkers.getMove(copy.deepcopy(checkers.board),checkers.turn,False)
#         else:
#             start_time = time.time()
#             treeGen = TreeGenerator(copy.deepcopy(checkers), checkers.turn,depth)
#             tree = treeGen.getTree(copy.deepcopy(checkers.board))
#             print("~~~~~~~~ Time to generate potential moves: " + str(time.time() - start_time))
#             start_time = time.time()
#             best_move = black.alpha_beta_search(tree)    # Find best move, save it as best_move
#             print("~~~~~~~~ Time to ABP through said tree: " + str(time.time() - start_time))
#             print(str(best_move))
#             checkers.board = checkers.movePiece(copy.deepcopy(checkers.board), checkers.turn, best_move.name, False, False)  # Make that move
#               
#         checkers.anyKings()
#         print("~~~~~~~~~~~~~~~ Next Turn")  # signal it is the AI's turn
#     # end while     
#        
#     print("Player %s cannot make any moves !" % ('B' if (checkers.turn == 1) else 'R'))
#     print("Player %s wins !" % ('R' if (checkers.turn == 1) else 'B'))
    
    
      
#     times = []
#     print("\nabout to run with depth = %i" % i)
#     start_time = time.time()
#     
#     treeGen = TreeGenerator(checkers,checkers.turn,i)
#     tree = treeGen.getTree(checkers.board)
#        
# #     tree = Node([0,0,0,0],checkers.board)
# #     
# #     for move in checkers.movesAvailable(checkers.board, checkers.turn, False):
# #         gametree = TreeGenerator(checkers,i,checkers.turn)  
# #         tree.addChild(gametree.fillSubTree(gametree.checkers.board, gametree.player, gametree.depth, move))
#     elapsed_time = time.time() - start_time
#     times += [elapsed_time]
#     print("done !")
# #   
#     abp = AlphaBeta(i,1)
#     best_node = abp.alpha_beta_search(tree)
#     print("Best move: " + str(best_node.name))
#      
#     print("Depth == %i, took %s seconds" % (i, elapsed_time))
#      
    
    
# end FILE    
    
    
    
    
    
    
    
