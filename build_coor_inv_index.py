import os
import pickle

from utils.coor_inv_index_builder import CoorInvIndexBuilder

if __name__ == "__main__":
    cib = CoorInvIndexBuilder()

    if not os.listdir("input"):
        raise FileExistsError()
    
    input = [os.path.join("input", f) for f in os.listdir("input") if os.path.isfile(os.path.join("input", f)) and f[-3:] == 'txt']
    coor_index = cib.map_reduce(input)

    for key, val in list(coor_index.items())[:5]:
        print(f"Key: {key}")
        print(f"Val: {list(val.keys())}")

    with open("output/coor_index.pickle", "wb") as f:
        pickle.dump(coor_index, f)