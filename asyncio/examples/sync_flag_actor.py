import random
import logging
import time
import requests
import os

import ray

FLAGS = ['CN', 'IN', 'US', 'ID', 'BR', 'PK', 'NG', 'BD', 'JP', 'MX', 'PH', 'VN', 'ET', 'EG', 'DE', 'IR', 'TR', 'CD', 'FR', 'GR']
FLAGS_URL = "http://flupy.org/data/flags"
BASE_DIR = "./downloads"


@ray.remote
class SyncFlagActor:

    def run_tasks(self, cc, verbose=False):
        if verbose:
            print(f"Started task-id='{ray.get_runtime_context().get_task_id()}'")
        result = self.do_task(cc)
        if verbose:
            print(f"finished task=i='{ray.get_runtime_context().get_task_id()}' with result='{result}'")
        return result

    def do_task(self, flag):
        file_name = f"{flag.lower()}.gif"
        url = f"{FLAGS_URL}/{file_name}"
        resp = requests.get(url)
        image = resp.content
        path = os.path.join(BASE_DIR, file_name)
        with open(path, 'wb') as fp:
            fp.write(image)
        resp.close()

        return flag
        
if __name__ == "__main__":

    if ray.is_initialized:
        ray.shutdown()
    ray.init(logging_level=logging.ERROR)

    verbose = True
    start = time.time()
    sync_actor= SyncFlagActor.remote()
    results = ray.get([sync_actor.run_tasks.remote(cc, verbose) for cc in FLAGS])
    print(f"SyncFlagActor: Time elapsed:{time.time() - start:.2f}")
    print(results)