from mpi4py import MPI
from shared_folder.src import datastructure
import numpy
import sys
import socket

def deSerializeState(size,listBoard):
    rows = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(listBoard[i*size+j])
        print(row)
        rows.append(row)
    return rows


def main():
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT)),nn
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
                board = deSerializeState(data[0],data[1])

                ## data = data + "go UP"
                ## data = bytes("Welcome to my chat server", encoding='utf-8')
                conn.sendall(data)

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
