from typing import List
import time

import numpy
import numpy as np
import ray

# Explain the behavior of this example
# 1. Actor invoking a remote task
# 2. What's the expected behavior: Are the tasks going to be distributed?
# 3. slow_method will be distributed across cores


@ray.remote
def slow_method(num: int, dims=10) -> List[numpy.array]:
    dot_products = []
    for _ in range(num):
        # Create a dims x dims matrix
        x = np.random.rand(dims, dims)
        y = np.random.rand(dims, dims)
        # Create a dot product of itself
        dot_products.append(np.dot(x, y))
    return dot_products


@ray.remote
class SlowActor(object):

    # Actor method invokes a Ray remote task
    def method(self, num, dims) -> None:
        res = [slow_method.remote(i, 5_000) for i in range(num)]
        ray.get(res)


if __name__ == '__main__':

    # Create an instance of SlowActor
    start = time.time()
    slow_actor = SlowActor.remote()
    results = slow_actor.method.remote(5, 5_000)
    print(ray.get(results))
    elapsed = time.time() - start
    print(f"Time elapsed: {elapsed:.2f}")