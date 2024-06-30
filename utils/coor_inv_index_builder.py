from nltk.tokenize import word_tokenize

import multiprocessing
from collections import defaultdict

def nested_defaultdict():
    return defaultdict(list)

class CoorInvIndexBuilder:

    def map(self, file: str):
        with open(file, "r", encoding='utf8') as f:
            words = word_tokenize(f.read().lower().replace("\n", " "))
            words = [word for word in words if word.isalpha()]
            pairs = [(word, file, i) for i, word in enumerate(words)]
            return pairs

    def reduce(self, pairs: list):
        term_doc_dict = defaultdict(nested_defaultdict)
        for term, file, i in pairs:
            term_doc_dict[term][file].append(i)
        return term_doc_dict

    def map_reduce(self, files: list[str]):
        with multiprocessing.Pool() as pool:
            map_results = pool.map(self.map, files)
            flattened_map_results = [p for l in map_results for p in l]
            term_doc_dict = self.reduce(flattened_map_results)

        return term_doc_dict