import random
import logging
import time

import ray

@ray.remote
class ThreadedActor:

    def run_tasks(self, i, verbose=False):
        if verbose:
            print(f"Started task-id='{ray.get_runtime_context().get_task_id()}'")
        result = self.do_task(i)
        if verbose:
            print(f"finished task=i='{ray.get_runtime_context().get_task_id()}' with result='{result}'")
        return i

    def do_task(self, i):
        time.sleep(random.randint(1, 5))
        return i
        
if __name__ == "__main__":

    if ray.is_initialized:
        ray.shutdown()
    ray.init(logging_level=logging.ERROR)

    verbose = True
    start = time.time()
    threaded_actor= ThreadedActor.options(max_concurrency=5).remote()
    results = ray.get([threaded_actor.run_tasks.remote(i, verbose) for i in range(1, 11)])
    print(f"ThreadedActor: Time elapsed:{time.time() - start:.2f}")
    print(results)