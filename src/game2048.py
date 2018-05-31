import random
import math
from src import datastructure

class board:
    boardMatrix = []
    size = 0
    p4 = 0.1
    score = 0

    def __init__(self, size, p4 = 0.1):
        self.size = size
        self.initBoardMatrix(size)
        self.score = 0

    def initBoardMatrix(self, size):
        self.boardMatrix = [[0 for i in range(size)] for j in range(size)]
        rand1 = 0
        rand2 = 0
        while(rand1 == rand2):
            rand1 = random.randint(0, size*size - 1)
            rand2 = random.randint(0, size*size - 1)
        if(random.random() <= self.p4):
            self.boardMatrix[int(rand1/size)][int(rand1%size)] = 4
        else:
            self.boardMatrix[int(rand1/size)][int(rand1%size)] = 2

        if(random.random() <= self.p4):
            self.boardMatrix[int(rand2/size)][int(rand2%size)] = 4
        else:
            self.boardMatrix[int(rand2/size)][int(rand2%size)] = 2

    def moveLeft(self, test=0):
        ## feed each row into queue
        ## do compress
        ## do fill
        newboard = []
        for line in self.boardMatrix:
            line = datastructure.queue(line)
            line = line.compress()
            newboard.append(line)

        if(self.checkBoardEqual(self.boardMatrix, newboard)):
            print("hit border")
            return 0
        else:
            if(not test):
                self.boardMatrix = newboard
                self.updateScore()
                return self.addtile()

    def moveRight(self, test=0):
        ## feed each row into queue
        ## do compress
        ## do fill
        newboard = []
        tempmatrix = [[0 for i in range(len(self.boardMatrix))] for j in range(len(self.boardMatrix))]
        print("boardmatrix before: "+str(self.boardMatrix))
        for i in range(len(self.boardMatrix)):
            for j in range(len(self.boardMatrix)):
                tempmatrix[i][j] = self.boardMatrix[i][j]

        for line in tempmatrix:
            line.reverse()
            line = datastructure.queue(line)
            line = line.compress()
            line.reverse()
            newboard.append(line)
        print("boardmatrix after:  "+str(self.boardMatrix))
        print("tempmatrix after:   "+str(tempmatrix))
        print("newboard :          "+str(newboard))
        if(self.checkBoardEqual(self.boardMatrix, newboard)):
            print("hit border")
            return 0
        else:
            if(not test):
                self.boardMatrix = newboard
                self.updateScore()
                return self.addtile()

    def moveUp(self, test=0):
        ## takang then move left
        newboard = []
        takangboard = [[self.boardMatrix[i][j] for i in range(len(self.boardMatrix))] for j in range(len(self.boardMatrix))]
        for line in takangboard:
            line = datastructure.queue(line)
            line = line.compress()
            newboard.append(line)
        newboard = [[newboard[i][j] for i in range(len(self.boardMatrix))] for j in range(len(self.boardMatrix))]
        if(self.checkBoardEqual(self.boardMatrix, newboard)):
            print("hit border")
            return 0
        else:
            if(not test):
                self.boardMatrix = newboard
                self.updateScore()
                return self.addtile()

    def moveDown(self, test=0):
        newboard = []
        takangboard = [[self.boardMatrix[i][j] for i in range(len(self.boardMatrix))] for j in range(len(self.boardMatrix))]
        for line in takangboard:
            line.reverse()
            line = datastructure.queue(line)
            line = line.compress()
            line.reverse()
            newboard.append(line)
        newboard = [[newboard[i][j] for i in range(len(self.boardMatrix))] for j in range(len(self.boardMatrix))]

        if(self.checkBoardEqual(self.boardMatrix, newboard)):
            ## the board is the same
            print("Hit border")
            return 0
        else:
            if(not test):
                self.boardMatrix = newboard
                self.updateScore()
                return self.addtile()

    def updateScore(self):
        score = 0
        for line in self.boardMatrix:
            for tile in line:
                if(tile == 0):
                    pass
                else:
                    tile_score = int((math.log(tile,2)-1)*tile)
                    score += tile_score
                    print("tile = "+str(tile)+" score = "+str(tile_score))
        self.score = score

    def getScore(self):
        return self.score

    def addtile(self):
        pos = random.randint(0, self.size*self.size)
        count = 0
        avail = []
        for i in range(self.size):
            for j in range(self.size):
                if(self.boardMatrix[i][j] == 0):
                    avail.append((i,j))
        if(len(avail)==0):
            return 0
        else:
            pos = random.randint(0, len(avail)-1)
            self.boardMatrix[avail[pos][0]][avail[pos][1]] = self.randomNum()
            return 1

    def randomNum(self):
        if(random.randint(1,100) <= 100*self.p4):
            return 4
        else:
            return 2

    def getBoard(self):
        print("GETBOARD : "+str(self.boardMatrix))
        print("")
        return self.boardMatrix

    def checkBoardEqual(self, board1, board2):
        for i in range(len(board1)):
            for j in range(len(board2)):
                if(board1[i][j] != board2[i][j]):
                    return 0
        return 1



    def __repr__(self):
        string = ""
        for line in self.boardMatrix:
            for tile in line:
                string = string + str(tile) + "\t"
            string = string + "\n"
        return  string

class tile:
    Xpos = 0
    Ypos = 0
    value = 0

    def __init__(self, position_x, position_y, value):
        self.Xpos = position_x
        self.Ypos = position_y
        self.value = value

