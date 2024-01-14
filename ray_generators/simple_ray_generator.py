import ray
import time
import random
import numpy as np

"""
The Ray generator is useful when:
 1) You want to reduce heap memory or object store memory usage by yielding and 
 garbage collecting (GC) the output before the task finishes.
 2) You are familiar with the Python generator and want the equivalent programming models.
"""

@ray.remote
def generative_task() -> object:
    """"
    A task that generates a random numpy array 
    matrix of N between 0 and 100. 0 is a signal to stop
    """
    print(f"task id: {ray.get_runtime_context().get_task_id()}")

    time.sleep(0.005)
    dim = random.randint(0, 100)
    if dim == 0:
        yield np.random.randint(dim, size=(dim, dim))
    else: 
        yield np.random.randint(dim, size=(dim, dim)) * 0.05
    
def process_numbers(numbers: list[object]) -> int:
    """
    A task that processes a list of np arrays
    """
    sums = [np.sum(arr) for arr in numbers]
    return sum(sums)

if __name__ == "__main__":
    if ray.is_initialized():
        ray.shutdown()
    ray.init()

    # generate a list of np arrays
    np_arrays = []
    # Generate a list of nummp
    while True:
        gen = generative_task.remote()
        # fet the array from the generator
        arr = ray.get(next(gen))
        if np.all(arr == 0):
            print("Stopping the generator")
            ray.cancel(gen)
            break
        # append the results
        np_arrays.append(arr)
        # print(f"Generated list of np arrays: {np_arrays}")
    
    # process the numbers
    result = process_numbers(np_arrays)
    print(f"sum of numbers: {result:.2f}")
