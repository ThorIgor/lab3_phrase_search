from nltk.tokenize import word_tokenize

import multiprocessing
from collections import defaultdict


class TWIndexBuilder:

    def map(self, file: str):
        with open(file, "r", encoding='utf8') as f:
            words = word_tokenize(f.read().lower().replace("\n", " "))
            words = [word for word in words if word.isalpha()]
            pair = None
            pairs = []
            for w in words:
                if pair is None:
                    pair = (None, w)
                    pairs.append((pair, file))
                else:
                    pair = (pair[-1], w)
                    pairs.append((pair, file))
                    pairs.append(((None, w), file))
            return pairs

    def reduce(self, pairs: list):
        term_doc_dict = defaultdict(list)
        for term, file in pairs:
            if file not in term_doc_dict[term]:
                term_doc_dict[term].append(file)
        return term_doc_dict

    def map_reduce(self, files: list[str]):
        with multiprocessing.Pool() as pool:
            map_results = pool.map(self.map, files)
            flattened_map_results = [p for l in map_results for p in l]
            term_doc_dict = self.reduce(flattened_map_results)

        return term_doc_dict