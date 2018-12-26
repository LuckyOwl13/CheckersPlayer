'''
Created on Nov 9, 2018

@author: Caitlin McElwee
'''
import glob
from Checkers import Checkers
from test.test_binop import isint

def convertMovesToBoards(filePath="MoveSets/"):
    
    writeFile = open("FinalBoardStates.txt","w+")
    writeString = ""
    
    for file in glob.glob(filePath+"*.txt"):
        print(file)
                
        file = open(file,"r")
        winner = ""
        move = []
        checkers = Checkers()
        for line in file:   # load all lines in each file into moves
            line = line.strip()
            if len(line) == 1:
                winner = -1 if line == 'R' else 1	# turn it numerical
            else:
                checkers.turn = (-1)*checkers.turn  # invert the turn
                move = [int(s) for s in line[1:len(line)-1].split(",")]
                checkers.board = checkers.movePiece(checkers.board, checkers.turn, move, False, False)
                checkers.anyKings()
                
                writeString += str(winner) + "," + parseBoard(checkers.board) + str(checkers.turn*5) + "\n"
    # end for
    
    writeFile.write(writeString)
# end convertMovesToBoards


def convertMovesToValues(minThreshold,maxThreshold=7,filePath="MoveSets/"):
    
    maxThreshold = 7000
    writeFile = open("FinalBoardStates%s.txt" % (str(minThreshold) + str(maxThreshold)),"w+")
    writeString = ""
    
    for file in glob.glob(filePath+"*.txt"):
        print(file)
                
        file = open(file,"r")
        move = []
        checkers = Checkers()
        for line in file:   # load all lines in each file into moves
            line = line.strip()
            if len(line) > 1: 
                checkers.turn *= -1     # invert the turn
                move = [int(s) for s in line[1:len(line)-1].split(", ")]
                checkers.board = checkers.movePiece(checkers.board, checkers.turn, move, False, False)
                checkers.anyKings()
                
    
                numBlackThreat, numRedThreat = countThreats(checkers)
                
                boardLine = parseBoard(checkers.board)
                numBlackPiec, numRedPiec, numBlackKing, numRedKing, score = tallyPieces(boardLine)
    
                if abs(score) >= minThreshold and abs(score) <= maxThreshold:  # if a board is significantly in one player's direction 
                    writeString += str(score) \
                                        + "," + str(numBlackPiec) \
                                        + "," + str(numRedPiec) \
                                        + "," + str(numBlackKing) \
                                        + "," + str(numRedKing) \
                                        + "," + str(numBlackThreat) \
                                        + "," + str(numRedThreat) \
                                        + "," + str(checkers.turn*5 ) + "\n"
    # end for
    
    writeFile.write(writeString)


def countThreats(checkers):
    numBlackThreats = 0
    numRedThreats = 0
    
    if checkers.turn == -1:
        numRedThreats = countJumps(checkers)
        checkers.turn *= -1
        numBlackThreats = countJumps(checkers)
        checkers.turn *= -1
    else:
        numBlackThreats = countJumps(checkers)
        checkers.turn *= -1
        numRedThreats = countJumps(checkers)
        checkers.turn *= -1
    
    return numBlackThreats, numRedThreats


def countJumps(checkers):
    jumps = 0
    for i in range(0,len(checkers.board)):           # for all vertical bars
        for j in range (0,len(checkers.board[i])):   # for all horizontal spaces in given vertical bar
            if checkers.board[i][j] == checkers.turn or checkers.board[i][j] == checkers.king*checkers.turn:   # if current space is the player's piece, check the following
                if Checkers.checkValidMove(checkers, checkers.board, checkers.turn, [i,j,i-2,j-2], False)[0]: # jump UL
                    jumps += 1
                if Checkers.checkValidMove(checkers, checkers.board, checkers.turn, [i,j,i-2,j+2], False)[0]: # jump UR
                    jumps += 1
                if Checkers.checkValidMove(checkers, checkers.board, checkers.turn, [i,j,i+2,j-2], False)[0]: # jump DL
                    jumps += 1
                if Checkers.checkValidMove(checkers, checkers.board, checkers.turn, [i,j,i+2,j+2], False)[0]: # jump DR
                    jumps += 1
                    
        
    return jumps

def tallyPieces(boardLine):
    numBlackPiec = 0
    numRedPiec = 0
    numBlackKing = 0
    numRedKing = 0
    score = 0
        
    for i in range(0, len(boardLine)):
        if isint(boardLine[i]):          # if it is an integer
            score += boardLine[i]  # add piece value to score
            if   boardLine[i] ==  1: numBlackPiec += 1
            elif boardLine[i] == -1: numRedPiec += 1

            if boardLine[i] ==  2: numBlackKing += 1
            elif boardLine[i] == -2: numRedKing += 1

    return numBlackPiec, numRedPiec, numBlackKing, numRedKing, score



def parseBoard(board):
    returnList = ""
    
    for i in range(0,len(board)):
        for j in range(0,len(board[i])):
            if isint(board[i][j]):
                returnList += str(board[i][j]) + ","
    
    return returnList







if __name__ == "__main__":
    convertMovesToBoards()
    # for minThreshold in range(0,1):
    #     convertMovesToValues(minThreshold)
    #     print("\n~~ Done with minThreshold == %i, moving to next set\n" % minThreshold)
    print("\nfinished ! :D")
    
#end of __main__
    
    