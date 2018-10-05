'''
Created on Sep 7, 2018

@author: Caitlin ☼
'''
from distutils.command.check import check

class Checkers(object):
    '''
    classdocs
    '''
    board = []
    turn = 0    # Is it W's (1)
    king = 2
    
    def __init__(self):
        '''
        Constructor
        '''
        self.board = [[' ',1,' ',1,' ',1,' ',1],
                      [1,' ',1,' ',1,' ',1,' '],
                      [' ',1,' ',1,' ',1,' ',1],
                      [0,' ',0,' ',0,' ',0,' '],
                      [' ',0,' ',0,' ',0,' ',0],
                      [-1,' ',-1,' ',-1,' ',-1,' '],
                      [' ',-1,' ',-1,' ',-1,' ',-1],
                      [-1,' ',-1,' ',-1,' ',-1,' ']]
        self.turn = -1
    # end init
        
    def printBoard(self,board):
        print("The current board is:")
        print("\t | 0 1 2 3 4 5 6 7")
        print("\t------------------")
        for i in range(0,len(board)):
            printString = ("\t%i| " % i)
            for j in range (0,len(board[i])):
                space = board[i][j]
                if isinstance(space, int):
                    if space == -1: letter = 'R'
                    elif space == 0: letter = '-'
                    elif space == 1: letter = 'B'
                    elif space == -1*self.king: letter = 'r'
                    elif space == self.king: letter = 'b'
                else: letter = space                
                
                printString += letter + " "
            print(printString)
        print("It is %s's turn" % self.whoseTurn())
    # end printBoard
    
    def whoseTurn(self):
        if self.turn == -1: return 'R'
        else: return 'B'
    # end whoseTurn
    
    def getMove(self,board,turn,isJump=False):
        move = [int(s) for s in input("What is your move? ").split(' ')]
        return self.movePiece(board, turn, move, isJump)
    
    def movePiece(self, board, turn, move, isJump=False, human=True):
        print("move: %s" % move)   
        
        moveCheck = self.checkValidMove(board, turn, move, isJump)

        if moveCheck[0]:    # if the move is valid 
            board[move[2]][move[3]] = board[move[0]][move[1]] # copy piece into the new position ...
            board[move[0]][move[1]] = 0                            # and take piece out of old spot
            if moveCheck[1]: board [move[0]+(move[2]-move[0])//2]\
                                        [move[1]+(move[3]-move[1])//2] = 0   # if it was a jump, remove jumped piece
            if False: # moveCheck[2]:    # removed for simplicity
                print("You can make another move ! ")
                self.printBoard(board)
                self.getMove(board, turn, moveCheck[2])
        elif not human: 
            ["complain about it"]
        else:
            print(moveCheck[3])
            self.getMove(board, turn, False)   # if given a bad move, retry recursively
        # end else    
        return board
    # end movePiece
    
    
    # checks if the given move is valid to do
    # move -> the potential move
    # isJump -> if this move is right after a jump. If so, can only jump again (no single-steps)
    def checkValidMove(self,board,turn,move,isJump=False):
        
        if ( (move[0] < len(board)) and \
             (move[0] >= 0) and \
             (move[1] < len(board[move[0]])) and \
             (move[1] >= 0) and \
             (move[2] < len(board)) and \
             (move[2] >= 0) and \
             (move[3] < len(board[move[2]])) and \
             (move[3] >= 0) ):  # if the piece selected and potential move are within bounds 
            if ((turn == board[move[0]][move[1]]) or (turn*self.king == board[move[0]][move[1]])):   # if the (normal or king) piece matches the turn
                if ((not isJump) and \
                    (move[2] == move[0] + turn) and \
                    (abs(move[3] - move[1]) == 1) and \
                    (board[move[2]][move[3]] == 0)):    # if the piece is being moved one forward
                    # print("only one hop")
                    return True, False, False
                elif ((move[2] == move[0] + turn*2) and \
                      (abs(move[3] - move[1]) == 2) and \
                     ((board[move[0] + (move[2] - move[0])//2][move[1] + (move[3] - move[1])//2] == turn*(-1)) or \
                      (board[move[0] + (move[2] - move[0])//2][move[1] + (move[3] - move[1])//2] == turn*(-1)*self.king)) and \
                      (board[move[2]][move[3]] == 0)):    # elif the piece is jumping another piece (moving forward)
                    # print("two hops this time !")
                    
                    if (self.checkMoreJumps(board,[move[2], move[3], board[move[0]][move[1]]])[0]): # if there are more jumps possible
                        # print("Yes jumps!")
                        return True, True, True
                    else:
                        # print("No jumps :(")
                        return True, True, False
                elif ((not isJump) and \
                      (abs(board[move[0]][move[1]]) == self.king) and \
                      (move[2] == move[0] - turn) and \
                      (abs(move[3] - move[1]) == 1) and \
                      (board[move[2]][move[3]] == 0)):    # if the piece is being moved backward (if it is a king or already jumping)
                    # print("King hops where it likes")
                    return True, False, False
                elif (((abs(board[move[0]][move[1]]) == self.king) or isJump) and \
                       (move[2] == move[0] - turn*2) and \
                       (abs(move[3] - move[1]) == 2) and \
                      ((board[move[0] + (move[2] - move[0])//2][move[1] + (move[3] - move[1])//2] == turn*(-1)) or \
                       (board[move[0] + (move[2] - move[0])//2][move[1] + (move[3] - move[1])//2] == turn*(-1))) and \
                       (board[move[2]][move[3]] == 0)): # if the piece is jumping another (moving backwards)
                    # print("King power ! :D")
                    
                    if (self.checkMoreJumps(board,[move[2], move[3], board[move[0]][move[1]]])[0]): # if there are more jumps
                        return True, True, True
                    else:
                        return True, True, False 
                else: 
                    return False, False, False, "Invalid move, bad coords"
            else: 
                return False, False, False, "Invalid move, that space does not contain a piece of yours"
        else: 
            return False, False, False, "Invalid move, out of bounds"
    # end checkValidMove
    
    # board:  a board being considered for moves
    # player: who's pieces are being considered
    # parent: parent node to potential move
    # isJump: if this previous move was a jump
    def movesAvailable(self, board, player, isJump=False):
        moveSet = []        
        
        for i in range(0,len(board)):           # for all vertical bars
            for j in range (0,len(board[i])):   # for all horizontal spaces in given vertical bar
                if board[i][j] == player:       # if current space is the player's piece, check the following
                    
                    if Checkers.checkValidMove(self, board, player, [i,j,i-1,j-1], False): # hop UL
                        moveSet += [[i,j,i-1,j-1]]
                    if Checkers.checkValidMove(self, board, player, [i,j,i-1,j+1], False): # hop UR
                        moveSet += [[i,j,i-1,j+1]]
                    if Checkers.checkValidMove(self, board, player, [i,j,i+1,j-1], False): # hop DL
                        moveSet += [[i,j,i+1,j-1]]
                    if Checkers.checkValidMove(self, board, player, [i,j,i+1,j+1], False): # hop DR
                        moveSet += [[i,j,i+1,j+1]]
                    if Checkers.checkValidMove(self, board, player, [i,j,i-2,j-2], isJump): # jump UL
                        moveSet += [[i,j,i-2,j-2]]
                    if Checkers.checkValidMove(self, board, player, [i,j,i-2,j+2], isJump): # jump UR
                        moveSet += [[i,j,i-2,j+2]]
                    if Checkers.checkValidMove(self, board, player, [i,j,i+2,j-2], isJump): # jump DL
                        moveSet += [[i,j,i+2,j-2]]
                    if Checkers.checkValidMove(self, board, player, [i,j,i+2,j+2], isJump): # jump DR
                        moveSet += [[i,j,i+2,j+2]]
        
        return moveSet
    # end movesAvailable    
    
    
    def nextTurn(self):
        self.turn *= -1          
        if len(self.movesAvailable(self.board,self.turn)) > 0:
            return True     # if current player has moves available, return True (game continues)
        else:
            self.printBoard(self.board)
            return False    # else return False (game over)
    # end changeTurn
    
    # So for each jump__, it does these checks:
    #     Is the new jump vertically within bounds?
    #     Is the new jump horizontal within bounds?
    #     Is the piece capable of this jump (right color / king?)
    #     Is the destination spot open?
    #     Is there an enemy piece in the space between?
    def checkMoreJumps(self,board,position):
        #    position[ vertical location, horizontal location, piece sign
        # print(position)
        
        # each jump__ returns ( (destination space is empty) and (intervening space has enemy piece) )
        # initial bounds-checking for array before it breaks
        if (position[0] > 1) and (position[1] > 1):  
            # print("UL possible")
            jumpUL = ((board[position[0]-2][position[1]-2] == 0) and \
                     ((board[position[0]-1][position[1]-1] == self.turn*-1) or (board[position[0]-1][position[1]-1] == self.turn*-1*self.king)))
        else: jumpUL = False
        if (position[0] > 1) and (position[1] < 6):  
            # print("UR possible")  
            jumpUR = ((board[position[0]-2][position[1]+2] == 0) and \
                     ((board[position[0]-1][position[1]+1] == self.turn*-1) or (board[position[0]-1][position[1]+1] == self.turn*-1*self.king)))
        else: jumpUR = False
        if (position[0] < 6) and (position[1] > 1):  
            # print("DR possible")  
            jumpDL = ((board[position[0]+2][position[1]-2] == 0) and \
                     ((board[position[0]+1][position[1]-1] == self.turn*-1) or (board[position[0]+1][position[1]-1] == self.turn*-1*self.king)))
        else: jumpDL = False
        if ((position[0] < 6) and (position[1] < 6)):  
            # print("DL possible")  
            jumpDR = ((board[position[0]+2][position[1]+2] == 0) and \
                     ((board[position[0]+1][position[1]+1] == self.turn*-1) or (board[position[0]+1][position[1]+1] == self.turn*-1*self.king)))
        else: jumpDR = False
            
        jumpYes = jumpUL or jumpUR or jumpDL or jumpDR 
                
        return jumpYes, jumpUL, jumpUR, jumpDL, jumpDR
    
    def anyKings(self):
        for i in {1, 3, 5, 7}:
            if self.board[0][i] == -1:
                print("King me !")
                self.board[0][i] *= self.king
        
        for i in {0, 2, 4, 6}:
            if self.board[7][i] == 1:
                print("King me !")
                self.board[7][i] *= self.king
    # end anyKings
# end Class




checkers = Checkers()

checkers.printBoard(checkers.board)
checkers.board = checkers.getMove(checkers.board[:],checkers.turn,False)

while checkers.nextTurn():
    checkers.printBoard(checkers.board)
    checkers.board = checkers.getMove(checkers.board[:],checkers.turn,False)
    checkers.anyKings()
# end while

print ("Player %s wins !" % ('R' if (checkers.turn == 1) else 'B'))






















