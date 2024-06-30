import pickle
from argparse import ArgumentParser
from collections import defaultdict

from nltk.tokenize import word_tokenize

def tok_query(query):
    return [w for w in word_tokenize(query.lower().replace("\n", " ")) if w.isalpha()]

def search_tw(query, tw_index):
    q_toks = tok_query(query)

    for w in q_toks:
        if (None, w) not in tw_index:
            return None

    if len(q_toks) < 1:
        return None
    elif len(q_toks) == 1:
        return tw_index[(None, q_toks[0])]
    else:
        docs = None
        w1 = q_toks[0]
        for w2 in q_toks[1:]:
            if docs is None:
                docs = set(tw_index[(w1, w2)])
            else:
                docs&=set(tw_index[(w1, w2)])
            w1 = w2
        return docs


def search_co(query, coor_index):
    q_toks = tok_query(query)

    for w in q_toks:
        if w not in coor_index:
            return None, len(q_toks)
    
    if len(q_toks) < 1:
        return None, len(q_toks)
    elif len(q_toks) == 1:
        return list(coor_index[q_toks[0]].keys()), len(q_toks)
    else:
        w1 = q_toks[0]
        coors = coor_index[w1]
        for w2 in q_toks[1:]:
            found = defaultdict(list)
            for doc in coors:
                for pos in coors[doc]:
                    if pos+1 in coor_index[w2][doc]:
                        found[doc].append(pos+1)
            coors = found
            if not coors:
                print(coors)
                print(w2)
                coors = None
                break
        return coors, len(q_toks)

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-i", "--index", help = "which index to use for search (tw - two words, co - coordinate) (defualt: tw)", type = str, default="tw")
    parser.add_argument("-s", "--search", help = "search query", type = str, default="This ebook is for the use of anyone anywhere in the United States")

    args = parser.parse_args()

    if args.index == 'tw':
        with open("output/tw_index.pickle", "rb") as f:
            tw_index = pickle.load(f)
        result = search_tw(args.search, tw_index)
        print(result)
    elif args.index == 'co':
        with open("output/coor_index.pickle", "rb") as f:
            co_index = pickle.load(f)
        result, l = search_co(args.search, co_index)
        if result is None:
            print("Found nothing")
        else:
            for key in result:
                coors = [[result[key][j]-(l-i-1) for i in range(l+1)] for j in range(len(result[key]))]
                print(f"Doc: {key}")
                print(f"Coor: {coors}")
                with open(key, "r", encoding = "utf8") as f:
                    print(f"Text: {tok_query(f.read())[coors[0][0]:coors[0][-1]]}")