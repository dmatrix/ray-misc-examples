import ray
from tasks_helper_utils import generate_batch_of_images, get_URLs, download_batch_images, transform_image   
import numpy as np
import os

if __name__ == "__main__":
    if ray.is_initialized():
        ray.shutdown()
    ray.init()
    
    # create a data directory if does not exist
    data_dir = "./data_images"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    urls = get_URLs()

    # generate a batch of images
    batch_gen = generate_batch_of_images.remote(urls, batch_size=10)
    for idx, batch in enumerate(batch_gen):
        images = ray.get(batch)
        print(f"Batch no: {idx}; images/batch:{len(images)}\n")
        print(f"batch={images}\n")
        results = download_batch_images.remote(images, './data_images')
        transformed_images = [transform_image(image) for image in ray.get(results)]
        print(f"transformed_images={transformed_images}\n")
    ray.shutdown()  


    
    

