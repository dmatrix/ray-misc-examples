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
def generative_task(debug=True) -> object:
    """"
    A task that generates a random numpy arrays of random size
    matrix of N between 0 and 100. 0 is a signal to stop
    """
    if debug:
        print(f"task id: {ray.get_runtime_context().get_task_id()}")

    time.sleep(0.005)
    dim = random.randint(0, 100)
    if dim == 0:
        yield np.random.randint(dim, size=(dim, dim))
    else: 
        yield np.random.randint(dim, size=(dim, dim)) * 0.05
    
def process_arrays(numbers: list[object]) -> int:
    """
    A task that processes a list of np arrays. This is a simple, however,
    you can imagine a more complex task that does some processing and
    updates a database, for example.
    """
    sums = [(np.sum(arr) * (idx+1)) for idx, arr in enumerate(numbers)]
    return sum(sums)

if __name__ == "__main__":
    if ray.is_initialized():
        ray.shutdown()
    ray.init()
    debug = False
    np_arrays = []
    # Generate a list of nummpy arrays on demandusing Ray Generators
    while True:
        gen = generative_task.remote(debug=debug)
        # fet the array from the generator
        arr = ray.get(next(gen))
        if np.all(arr == 0):
            if debug:
                print("Stopping the generator")
            ray.cancel(gen)
            break
        # append the results
        np_arrays.append(arr)
        if debug:
          print(f"Generated list of np arrays: {np_arrays}")
    
    # process the list of np arrays
    result = process_arrays(np_arrays)
    print(f"Sum of all numpy arrays: {result:.2f}")
