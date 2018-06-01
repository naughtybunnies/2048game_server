from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

print("SIZE: ",size)
if rank == 0:
    data = [(i+1)**2 for i in range(size)]
else:
    data = None
data = comm.scatter(data, root=0)
assert data == (rank+1)**2

if rank == 0:
    print("RANK: ",rank)
    print("DATA: ",data)
else:
    print("RANK: ",rank)
    print("DATA: ",data)
