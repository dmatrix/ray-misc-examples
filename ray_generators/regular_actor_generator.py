import ray
from typing import List
import numpy as np

@ray.remote
class GenRandomBatches:
    """
    A generator that yields a list of random numpy arrays of random size
    """
    def __init__(self, batch_size, total_size) -> None:
        self._batch_size =  batch_size
        self._total_size = total_size

    def get_batch(self) -> List[np.ndarray]:
        """
        A task that generates a random numpy arrays of random size
        """
        for dim in range(self._total_size // self._batch_size):
            yield [np.random.randint(dim, size=(dim, dim)) * 0.05 for i in range(self._batch_size)]

    def get_batch_size(self) -> int:
        """
        A task that returns the batch size
        """
        return self._batch_size
    
    def get_total_size(self) -> int:
        """
        A task that returns the total size
        """
        return self._total_size
    
    def convert_to_vector(self, batch: List[np.ndarray]) -> np.ndarray:
        """
        A task that converts a list of numpy arrays to a vector
        """
        return np.array(batch).flatten()
    
if __name__ == "__main__":
    if ray.is_initialized():
        ray.shutdown()
    ray.init()

    print(f"Ray version: {ray.__version__}")
    
    # Create couple of actors
    actor_1 = GenRandomBatches.remote(10, 100)
    actor_2 = GenRandomBatches.remote(20, 100)
    actors = [actor_1, actor_2] 

    # Iterate over the actors' generators and print the results  
    for actor in actors:
        batch = ray.get(actor.get_batch.remote())
        # Print the results of each actore generator
        for idx, arr in enumerate(batch):
            print(f"batch no: {idx}; array size: {ray.get(arr)[0].shape}")
            print(f"batch's first array: {ray.get(arr)[0]}")
            print(f"batch size: {ray.get(actor.get_batch_size.remote())}")
            print(f"total size: {ray.get(actor.get_total_size.remote())}")
            print(f"sum of vector: {sum(ray.get(actor.convert_to_vector.remote(arr))):.2f}")
            print("---" * 10)
    ray.shutdown()