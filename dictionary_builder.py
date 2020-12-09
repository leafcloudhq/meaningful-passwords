import json
import re

import gensim.downloader as api
from nltk.corpus import wordnet as wn


class DictionaryBuilder:

    def __init__(self, num_similar_words, min_length, max_length, vector_type):
        self.pos_tagged_sets = {"adj": set(), "noun": set(), "verb": set()}
        self.model = api.load(vector_type)
        self.num_similar_words = num_similar_words
        self.min_length = min_length
        self.max_length = max_length

    def write_dictionary(self):
        dictionary = self.create_dictionary()
        self.pos_tagged_sets = self.pos_tag(dictionary)
        self.print_dictionary_info()

        with open('dictionary.json', 'w') as outfile:
            json.dump(self.pos_tagged_sets, outfile)
        return self.pos_tagged_sets

    def create_dictionary(self):
        with open('context.json', 'r') as file:
            context = json.load(file)
        wordlist = list(context['wordlist'])
        similar = list(context['similar'])
        negative = list(context['negative'])
        dictionary = {}
        for word in wordlist:
            if word in self.model:
                dictionary = {**dictionary, **dict(
                    self.model.most_similar(positive=[self.model[word]] + similar, negative=negative,
                                            topn=self.num_similar_words))}
            else:
                print(word, "is not in the word-vector model, skipping")
        return self.clean(dictionary)

    def clean(self, dictionary):
        dictionary = dictionary.keys()
        dictionary = [
            word for word in dictionary if
            self.min_length <= len(word) <= self.max_length and re.match('^[a-zA-Z]*$', word)
        ]
        return dictionary

    def print_dictionary_info(self):
        total_size = 0
        for key in self.pos_tagged_sets.keys():
            size = len(self.pos_tagged_sets[key])
            total_size += size
            print(size, "words are a", key)
        print("total size of the dictionary is", total_size, "words")

    def pos_tag(self, dictionary):
        for w in dictionary:
            syns = wn.synsets(w)
            if syns:
                tag = syns[0].lexname().split('.')[0]
                if tag not in self.pos_tagged_sets:
                    continue
                if tag == "adv":
                    self.convert_and_add(w, "happily", "happy")
                else:
                    self.pos_tagged_sets[tag].add(w)

        return self.to_lists(self.pos_tagged_sets)

    @staticmethod
    def to_lists(sets):
        return {k: list(v) for k, v in sets.items()}

    def convert_and_add(self, pos, neg, inp):
        positive = [inp, pos]
        negative = [neg]
        all_similar = self.model.most_similar(positive, negative, topn=1)

        w = all_similar[0][0]
        syns = wn.synsets(w)
        if syns:
            tag = syns[0].lexname().split('.')[0]
            if tag == "adj":
                self.pos_tagged_sets[tag].add(w)
        return
