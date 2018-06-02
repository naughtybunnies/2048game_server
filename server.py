from mpi4py import MPI
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
size = comm.Get_size()
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
        s.bind((HOST, PORT))
        nodes = None
        while 1 :
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data: break
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
                    nodesGenerated = True
                    print("DONE")
                    break

                    #print(board)
                    #data = data + "go UP"
                    #data = bytes("Welcome to my chat server", encoding='utf-8')
                    '''
                    try :
                        conn.sendall(data)
                    finally:
                        conn.close()
                    '''
                #endwhile
            print("nodesGenerated: ",nodesGenerated)
            if nodesGenerated: break
        #endwhile
    #endif
    else:
        nodes = None
        splitNodes = None
    if rank == 0:
        splitNodes = [nodes[i::size] for i in range(size)]
        print("SPLIT NODES SIZE:",len(splitNodes))
        for i,splitNode in enumerate(splitNodes):
            print("SPLIT NODE ",i,"LENGTH:",len(splitNode))
            for j,row in enumerate(splitNode):
                print(row)

    #print("RANK ",rank," REACHED BARRIER")
    comm.Barrier()
    nodes = comm.scatter(splitNodes, root=0)

    if nodes is not None:
        maxScore = 0
        bestNode = None
        print("RANK",rank,"HAS",len(nodes),"NODES")
        print("RANK",rank,"IS EVALUATING")
        for node in nodes :
            p = evaluation.slopedBoard(node[1])
            score = node[2]*p
            if maxScore < score :
                maxScore = score
                bestNode = node
                bestNode[2] = score
            #endif
        #endfor
        print("RANK",rank,"DONE")
        comm.Barrier()
        comm.send(bestNode, dest=0, tag=1)
    #endif


    if rank == 0 :
        bestNode = [0,0,0]
        bestNodes = []
        for p in range(size):
            recvNode = comm.recv(source=p, tag=1)
            print("RECEIVED :",recvNode)
            bestNodes.append(recvNode)
        print("BEST NODES LIST")
        for n in bestNodes:
            print(n)
        for node in bestNodes :
            if bestNode[2] < node[2]:
                bestNode = node
        dataTosend = bytes(bestNode[0][0], encoding='utf-8')
        try :
            conn.sendall(dataTosend)
        finally:
            conn.close()

#########################################################################################################

while 1 :
    main()
    '''
    if rank == 0:
        print("SIZE: ",size)
        # Socket Communication
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = 50007              # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        main()
    else:
        nodes = None
    '''

'''
if __name__ == "__main__" :
    # Socket Communication
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    main()
'''

'''
    comm =  MPI.COMM_SELF.Spawn(
                sys.executable,
                args=['py_slave.py'],
                maxprocs=5
            )
    N = numpy.array(100, 'i')
    comm.Bcast([N, MPI.INT], root=MPI.ROOT)
    PI = numpy.array(0.0, 'd')
    comm.Reduce(None, [PI, MPI.DOUBLE], op=MPI.SUM, root=MPI.ROOT)
    print(PI)
    comm.Disconnect()
'''
