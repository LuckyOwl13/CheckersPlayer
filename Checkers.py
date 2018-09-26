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
        
    def printBoard(self):
        print("The current board is:")
        print("\t | 0 1 2 3 4 5 6 7")
        print("\t------------------")
        for i in range(0,len(self.board)):
            printString = ("\t%i| " % i)
            for j in range (0,len(self.board[i])):
                space = self.board[i][j]
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
    
    def movePiece(self, isJump):
        move = [int(s) for s in input("What is your move? ").split(' ')]
        print("move: %s" % move)        
        moveCheck = self.checkValidMove(move, isJump)

        if moveCheck[0]:    # if the move is valid 
            self.board[move[2]][move[3]] = self.board[move[0]][move[1]] # copy piece into the new position ...
            self.board[move[0]][move[1]] = 0                            # and take piece out of old spot
            if moveCheck[1]: self.board [move[0]+(move[2]-move[0])//2]\
                                        [move[1]+(move[3]-move[1])//2] = 0   # if it was a jump, remove jumped piece
            if moveCheck[2]: 
                print("You can make another move ! ")
                self.printBoard()
                self.movePiece(moveCheck[2])
        else: 
            self.movePiece(False)   # if given a bad move, retry recursively
#           self.nextTurn() # change to next turn
    # end movePiece
    # checks if the given move is valid to do
    # move -> the potential move
    # isJump -> if this move is right after a jump. If so, can only jump again (no single-steps)
    def checkValidMove(self,move,isJump):
        
        if ((move[0] < len(self.board)) & \
            (move[0] >= 0) & \
            (move[1] < len(self.board[move[2]])) & \
            (move[1] >= 0) & \
            (move[2] < len(self.board)) & \
            (move[2] >= 0) & \
            (move[3] < len(self.board[move[2]])) & \
            (move[3] >= 0)):  # if the piece selected and potential move are within bounds 
            if ((self.turn == self.board[move[0]][move[1]]) | (self.turn*self.king == self.board[move[0]][move[1]])):   # if the (normal or king) piece matches the turn
                if ((not isJump) & \
                    (move[2] == move[0] + self.turn) & \
                    (abs(move[3] - move[1]) == 1) & \
                    (self.board[move[2]][move[3]] == 0)):    # if the piece is being moved one forward
                    # print("only one hop")
                    return True, False, False
                elif ((move[2] == move[0] + self.turn*2) & \
                      (abs(move[3] - move[1]) == 2) & \
                     ((self.board[move[0] + (move[2] - move[0])//2][move[1] + (move[3] - move[1])//2] == self.turn*(-1)) | \
                      (self.board[move[0] + (move[2] - move[0])//2][move[1] + (move[3] - move[1])//2] == self.turn*(-1)*self.king)) & \
                      (self.board[move[2]][move[3]] == 0)):    # elif the piece is jumping another piece (moving forward)
                    # print("two hops this time !")
                    
                    if (self.checkMoreJumps([move[2], move[3], self.board[move[0]][move[1]]])[0]): # if there are more jumps possible
                        # print("Yes jumps!")
                        return True, True, True
                    else:
                        # print("No jumps :(")
                        return True, True, False
                elif ((not isJump) & \
                      (abs(self.board[move[0]][move[1]]) == self.king) & \
                      (move[2] == move[0] - self.turn) & \
                      (abs(move[3] - move[1]) == 1) & \
                      (self.board[move[2]][move[3]] == 0)):    # if the piece is being moved backward (if it is a king or already jumping)
                    # print("King hops where it likes")
                    return True, False, False
                elif (((abs(self.board[move[0]][move[1]]) == self.king) | isJump) & \
                       (move[2] == move[0] - self.turn*2) & \
                       (abs(move[3] - move[1]) == 2) & \
                      ((self.board[move[0] + (move[2] - move[0])//2][move[1] + (move[3] - move[1])//2] == self.turn*(-1)) | \
                       (self.board[move[0] + (move[2] - move[0])//2][move[1] + (move[3] - move[1])//2] == self.turn*(-1))) & \
                       (self.board[move[2]][move[3]] == 0)): # if the piece is jumping another (moving backwards)
                    # print("King power ! :D")
                    
                    if (self.checkMoreJumps([move[2], move[3], self.board[move[0]][move[1]]])[0]): # if there are more jumps
                        return True, True, True
                    else:
                        return True, True, False 
                else: 
                    print("Invalid move, bad coords")
                    return False, False, False
            else: 
                print("Invalid move, self.turn > self.board[move[0][1]]")
                return False, False, False
        else: 
            print("Invalid move, out of bounds")
            return False, False, False
    # end checkValidMove
    
    
    def nextTurn(self):
        self.turn *= -1          
        for i in range(0,len(self.board)):          # for all positions on the board
            for j in range (0,len(self.board[i])):  
                if self.board[i][j] == self.turn:   # if there is at least one piece for the next play 
                    return True     # return True
        
        return False                # else return False (game over)
    # end changeTurn
    
    # So for each jump__, it does these checks:
    #     Is the new jump vertically within bounds?
    #     Is the new jump horizontal within bounds?
    #     Is the piece capable of this jump (right color / king?)
    #     Is the destination spot open?
    #     Is there an enemy piece in the space between?
    def checkMoreJumps(self,position):
        #    position[ vertical location, horizontal location, piece sign
        # print(position)
        
        # each jump__ returns ( (destination space is empty) & (intervening space has enemy piece) )
        # initial bounds-checking for array before it breaks
        if (position[0] > 1) & (position[1] > 1):  
            # print("UL possible")
            jumpUL = ((self.board[position[0]-2][position[1]-2] == 0) & \
                     ((self.board[position[0]-1][position[1]-1] == self.turn*-1) | (self.board[position[0]-1][position[1]-1] == self.turn*-1*self.king)))
        else: jumpUL = False
        if (position[0] > 1) & (position[1] < 6):  
            # print("UR possible")  
            jumpUR = ((self.board[position[0]-2][position[1]+2] == 0) & \
                     ((self.board[position[0]-1][position[1]+1] == self.turn*-1) | (self.board[position[0]-1][position[1]+1] == self.turn*-1*self.king)))
        else: jumpUR = False
        if (position[0] < 6) & (position[1] > 1):  
            # print("DR possible")  
            jumpDL = ((self.board[position[0]+2][position[1]-2] == 0) & \
                     ((self.board[position[0]+1][position[1]-1] == self.turn*-1) | (self.board[position[0]+1][position[1]-1] == self.turn*-1*self.king)))
        else: jumpDL = False
        if ((position[0] < 6) & (position[1] < 6)):  
            # print("DL possible")  
            jumpDR = ((self.board[position[0]+2][position[1]+2] == 0) & \
                     ((self.board[position[0]+1][position[1]+1] == self.turn*-1) | (self.board[position[0]+1][position[1]+1] == self.turn*-1*self.king)))
        else: jumpDR = False
            
        jumpYes = jumpUL | jumpUR | jumpDL | jumpDR 
                
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




checkers = Board()

checkers.printBoard()
checkers.movePiece(False)

while checkers.nextTurn():
    checkers.printBoard()
    checkers.movePiece(False)
    checkers.anyKings()
# end while

print ("Player %s wins !" % ('R' if (checkers.turn == 1) else 'B'))






















