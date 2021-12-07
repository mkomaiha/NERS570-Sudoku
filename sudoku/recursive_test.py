import recursiveSolver as rs
from time import time
b1 = rs.RS(0,9999)
b2 = rs.RS(1,9999)
b3 = rs.RS(2,9999)
b4 = rs.RS(3,9999)

t0 = time()
b1.recursive_solver()
t1 = time()
b2.recursive_solver()
t2 = time()
b3.recursive_solver()
t3 = time()
b4.recursive_solver()
t4 = time()

print("Elapsed time for easy:",t1-t0)
print("Elapsed time for medium:",t2-t1)
print("Elapsed time for hard:",t3-t2)
print("Elapsed time for extreme:",t4-t3)

