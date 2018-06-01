from mpi4py import MPI
from src import game2048
from src import datastructure
from src import generateNode

import numpy
import sys
import socket
import copy

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

def moveup(board):
    #print("MOVE UP")
    newBoard = board.moveUp()
    #printBoard(newBoard)
    return newBoard

def moveleft(board):
    #print("MOVE LEFT")
    newBoard = board.moveLeft()
    #printBoard(newBoard)
    return newBoard

def movedown(board):
    print("MOVE DOWN")
    newBoard = board.moveDown()
    #printBoard(newBoard)
    return newBoard

def moveright(board):
    print("MOVE RIGHT")
    newBoard = board.moveRight()
    #printBoard(newBoard)
    return newBoard

def fillBoard(board, num, actions):
    print("FILL NUMBER ",num)
    for i,row in enumerate(board):
        for j,col in enumerate(row):
            if col == 0:
                filledBoard = copy.deepcopy(board)
                filledBoard[i][j] = num
                printBoard(filledBoard)

def main():

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
                listBoard = deSerializeState(size, strData)
                #print(listBoard)
                gameBoard = game2048.board(size, listBoard)
                #gameBoard.getBoard()
                generateNode.genNodeController(gameBoard, moves)

                #print(board)
                #data = data + "go UP"
                #data = bytes("Welcome to my chat server", encoding='utf-8')
                try :
                    conn.sendall(data)
                finally:
                    conn.close()

if __name__ == "__main__" :

    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))

    moves = [[moveleft,'l'], [moveright,'r'], [moveup,'u'], [movedown,'d']]

    main()

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
