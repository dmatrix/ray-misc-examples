import random
import logging
import time
import asyncio
import random

import ray

MAX_CONCURRENCY = 10
MAX_RANDOM = MAX_CONCURRENCY * 2

@ray.remote
class AsyncActor:

   async def run_tasks(self, i, type, verbose=False):
        if verbose:
            print(f"run:{i} {type}-started task-id='{ray.get_runtime_context().get_task_id()}'")
        # simulate some heavy duty work
        result = await self.do_task(i)
        if verbose:
            print(f"run:{i} {type}-finished task=i='{ray.get_runtime_context().get_task_id()}' with result='{result}'")
        return i

   async def do_task(self, i):
        await asyncio.sleep(random.randint(i, MAX_RANDOM))
        return i
        
if __name__ == "__main__":

    if ray.is_initialized:
        ray.shutdown()
    ray.init(logging_level=logging.ERROR)

    # regular ray.get
    actor = AsyncActor.remote()
    start = time.time()
    results = ray.get([actor.run_tasks.remote(id, "regular", verbose=True) for id in range(1, 11)])
    print(results)
    print(f"Regular AsyncActor: Time elapsed:{time.time() - start:.2f}")
    print("---" * 10)

    # AsyncActor
    # Only 2 tasks will be running concurrently. Once 2 finish, 
    # the next 2 should run.
    for conc in range(1, MAX_CONCURRENCY + 1):
        async_actor= AsyncActor.options(max_concurrency=conc).remote()
        start = time.time()
        results = ray.get([async_actor.run_tasks.remote(i, "async", verbose=True) for i in range(1, 11)])
        print(f"Max concurrency={conc}; AsyncActor: Time elapsed:{time.time() - start:.2f}")
        print(results)
        print("---" * 10)