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
#             print(line)
            if len(line) == 1:
                winner = line
#                 print("Winner found and it is: " + winner)
            else:
                checkers.turn = (-1)*checkers.turn  # invert the turn
                move = [int(s) for s in line[1:len(line)-1].split(",")]
#                 print(move)
                checkers.board = checkers.movePiece(checkers.board, checkers.turn, move, False, False)
                writeString += parseBoard(checkers.board) + winner + "\n"
                checkers.anyKings()
#                 print(writeString)
    # end for
    
    writeFile.write(writeString)

def parseBoard(board):
    returnString = ""
    
    for i in range(0,len(board)):
        for j in range(0,len(board[i])):
            if isint(board[i][j]):
                returnString += str(board[i][j]) + ","
    
    return returnString

# end convertMovesToBoards






if __name__ == "__main__":
    convertMovesToBoards()
    
#end of __main__
    
    