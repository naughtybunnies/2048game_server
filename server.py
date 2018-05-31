from mpi4py import MPI
from shared_folder.src import game2048

import numpy
import sys
import socket

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

def moveBoardLeft(board):
    board.moveLeft()

def main():
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    moves =[moveBoardLeft]
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
                size = data[0]
                strData = data[1]
                listBoard = deSerializeState(size, strData)
                gameBoard = game2048(listBoard)
                for move in moves:
                    move(gameBoard)

                #print(board)
                #data = data + "go UP"
                #data = bytes("Welcome to my chat server", encoding='utf-8')
                conn.sendall(data)
                conn.close()
if __name__ == "__main__" :
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
