from mpi4py import MPI
import numpy
import sys

comm =  MPI.COMM_SELF.Spawn(
            sys.executable,
            args=['py_slave.py'],
            maxprocs=5
        )
#N = numpy.array(100, 'i')
N = [[0],[1,2],1,]
comm.Bcast(N, root=MPI.ROOT)
#PI = numpy.array(0.0, 'd')
#comm.Reduce(None, [PI, MPI.DOUBLE], op=MPI.SUM, root=MPI.ROOT)
comm.Disconnect()
