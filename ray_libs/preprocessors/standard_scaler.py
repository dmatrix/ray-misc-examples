import ray
from ray.data.preprocessors import StandardScaler
from data_utils import gen_pandas_data

if __name__ == "__main__":

    ds = ray.data.from_pandas(gen_pandas_data())
    print("----" * 5)
    print("dataset before first fit & transform StandardScaler ....")
    print(ds.show(5))

    preproc = StandardScaler(["amount"])
    ds_trans = preproc.fit_transform(ds)
    print("----" * 5)
    print("dataset after first fit & transform StandardScaler ....")
    print(ds_trans.show(5))