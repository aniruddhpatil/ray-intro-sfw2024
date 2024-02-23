import ray
import time

n_list = [i for i in range(100)]

ray.init(address="ray://0.0.0.0:10001")


def serial_square(n):
    return n**2


@ray.remote
def distributed_square(n):
    return n**2


serial_start = time.time()
serial_square_list = []
for item in n_list:
    serial_square_list.append(item**2)
print("Normal Time {}".format(time.time() - serial_start))

ray_start = time.time()
ray_square_list = [distributed_square.remote(item) for item in n_list]
print("Ray Time {}".format(time.time()-ray_start))

ray.shutdown()
