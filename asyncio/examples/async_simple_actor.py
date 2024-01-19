import ray
import asyncio
import time

@ray.remote
class AsyncActor:
    # Multiple invocation of this method can be running in
    # the event loop at the same time
    async def run_concurrent(self, type):
        print(f"started {type}-task-id='{ray.get_runtime_context().get_task_id()}'")
        await asyncio.sleep(2) # concurrent workload here
        print(f"finished {type}-task-id='{ray.get_runtime_context().get_task_id()}'")
        return type

actor = AsyncActor.remote()

start = time.time()
# regular ray.get
results = ray.get([actor.run_concurrent.remote("regular") for _ in range(4)])
print(results)
print(f"Regular AsyncActor: Time elapsed:{time.time() - start:.2f}")
print("---" * 10)

# async ray.get
async def async_get():
    results = await asyncio.gather(*[actor.run_concurrent.remote("async") for _ in range(4)])
    print(results)
    
start = time.time()
asyncio.run(async_get())
print(f"AsyncActor: Time elapsed:{time.time() - start:.2f}")
