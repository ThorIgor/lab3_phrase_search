import os
import pickle

from utils.two_words_index_builder import TWIndexBuilder

if __name__ == "__main__":
    twb = TWIndexBuilder()

    if not os.listdir("input"):
        raise FileExistsError()
    
    input = [os.path.join("input", f) for f in os.listdir("input") if os.path.isfile(os.path.join("input", f)) and f[-3:] == 'txt']
    tw_index = twb.map_reduce(input)

    for key, val in list(tw_index.items())[:5]:
        print(f"Key: {key}")
        print(f"Val: {val}")

    with open("output/tw_index.pickle", "wb") as f:
        pickle.dump(tw_index, f)
    