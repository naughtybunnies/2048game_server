from mpi4py import MPI
from time import time
from src import game2048
from src import datastructure
from src import generateNode
from src import evaluation

import numpy
import sys
import socket
import copy

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

comm = MPI.COMM_WORLD
pSize = comm.Get_size()
rank = comm.Get_rank()

def deSerializeState(size,strBoard):
    listBoard = strBoard.split(" ")
    rows = []
    for i in range(size):
        row = []
        for j in range(size):
            #print(listBoard[size*i+j], end=' ')
            row.append(int(listBoard[size*i+j]))
        rows.append(row)
    return rows

def printBoard(board):
    for row in board:
        print(row)
    print()
def moveleft(board):
    newboard = []
    for line in board :
        line = datastructure.queue(line)
        line = line.compress()
        newboard.append(line)

    if(checkBoardEqual(board, newboard)):
        pass
    else:
        #printBoard(newboard)
        return newboard
        '''
        self.boardMatrix = newboard
        self.updateScore()
        return self.addtile()
        '''

def moveright(board):
    newboard = []
    tempmatrix = [[0 for i in range(len(board))] for j in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board)):
            tempmatrix[i][j] = board[i][j]

    for line in tempmatrix:
        line.reverse()
        line = datastructure.queue(line)
        line = line.compress()
        line.reverse()
        newboard.append(line)

    if(checkBoardEqual(board, newboard)):
        pass
    else:
        #printBoard(newboard)
        return newboard
        '''
        self.boardMatrix = newboard
        self.updateScore()
        return self.addtile()
        '''

def moveup(board):
    ## takang then move left
    newboard = []
    takangboard = [[board[i][j] for i in range(len(board))] for j in range(len(board))]
    for line in takangboard:
        line = datastructure.queue(line)
        line = line.compress()
        newboard.append(line)
    newboard = [[newboard[i][j] for i in range(len(board))] for j in range(len(board))]
    if(checkBoardEqual(board, newboard)):
        pass
    else:
        #printBoard(newboard)
        return(newboard)
        '''
        self.boardMatrix = newboard
        self.updateScore()
        return self.addtile()
        '''

def movedown(board):
    newboard = []
    takangboard = [[board[i][j] for i in range(len(board))] for j in range(len(board))]
    for line in takangboard:
        line.reverse()
        line = datastructure.queue(line)
        line = line.compress()
        line.reverse()
        newboard.append(line)
    newboard = [[newboard[i][j] for i in range(len(board))] for j in range(len(board))]

    if(checkBoardEqual(board, newboard)):
        pass
    else:
        #printBoard(newboard)
        return(newboard)
        '''
        self.boardMatrix = newboard
        self.updateScore()
        return self.addtile()
        '''

def checkBoardEqual( board1, board2):
        for i in range(len(board1)):
            for j in range(len(board2)):
                if(board1[i][j] != board2[i][j]):
                    return 0
        return 1



def fillBoard(board, num, actions):
    print("FILL NUMBER ",num)
    for i,row in enumerate(board):
        for j,col in enumerate(row):
            if col == 0:
                filledBoard = copy.deepcopy(board)
                filledBoard[i][j] = num
                printBoard(filledBoard)

def main():

    moves = [[moveleft,'l'], [moveright,'r'], [moveup,'u'], [movedown,'d']]

    nodesGenerated = False

    if rank == 0:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        s.bind((HOST, PORT))
        nodes = None
        while 1 :
            s.listen()
            conn, addr = s.accept()
            #with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data: break
                recvTime = time()
                data = data.decode()
                data = data.split(',') # data[0] is board size, data[1] is board data
                size = int(data[0])
                strData = data[1]
                print("DESERIALIZING",end=" ")
                listBoard = deSerializeState(size, strData)
                print("DONE")

                print("GENERATING NODES",end=" ")
                #print(listBoard)
                #gameBoard.getBoard()
                nodes = generateNode.genNodeController(listBoard, moves)
                genNodeTime = time()
                nodesGenerated = True
                print("DONE")
                break
            #endwhile
            #print("nodesGenerated: ",nodesGenerated)
            if nodesGenerated: break
        #endwhile
    #endif
    else:
        nodes = None
        splitNodes = None
    if rank == 0 and nodes is not None:
        splitNodes = [nodes[i::pSize] for i in range(pSize)]
    '''
        for i,splitNode in enumerate(splitNodes):
            for j,row in enumerate(splitNode):
                print(row)
    '''
    comm.Barrier()
    nodes = comm.scatter(splitNodes, root=0)

    if nodes is not None:
        maxScore = 0
        bestNode = None
        #print("RANK",rank,"HAS",len(nodes),"NODES")
        #print("RANK",rank,"IS EVALUATING")
        for node in nodes :
            p = evaluation.slopedBoard(node[1])
            score = node[2]*p
            if maxScore < score :
                maxScore = score
                bestNode = node
                bestNode[2] = score
            #endif
        #endfor
        #print("RANK",rank,"DONE")
        comm.Barrier()
        comm.send(bestNode, dest=0, tag=1)
    #endif

    bestNodes = comm.gather(bestNode, root=0)

    if rank == 0 :
        bestNode = [0,0,0]
        #print("BEST NODES LIST")
        for n in bestNodes:
            print(n)

        for node in bestNodes :
            if bestNode[2] < node[2]:
                bestNode = node
        #print("BEST NODE")
        #print(bestNode)
        nextMove = bestNode[0][0]
        #print("NEXT MOVE: ",nextMove)
        dataTosend = bytes(nextMove, encoding="utf-8")
        #dataTosend = bytes(bestNode[0][0], encoding='utf-8')
        conn.send(dataTosend)
        conn.close()
        replyTime = time()
        print("genNodeTime - recvTime", genNodeTime-recvTime, " replyTime - recvTime", replyTime-recvTime)
    #endif

#########################################################################################################

while 1 :
    main()

