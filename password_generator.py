import getopt
import json
from random import choice, randint

import inflect
import sys
import os

from dictionary_builder import DictionaryBuilder


class PasswordGenerator:

    def __init__(self, num_similar_words=200, min_length=4, max_length=10, vector_type="glove-twitter-50"):
        self.infl = inflect.engine()
        self.infl.classical(zero=False, herd=False, persons=False, ancient=True)
        try:
            with open('dictionary.json', 'r') as file:
                self.pos_tagged_lists = json.load(file)
        except IOError:
            print("generating dictionary")
            builder = DictionaryBuilder(num_similar_words=num_similar_words, min_length=min_length,
                                        max_length=max_length, vector_type=vector_type)
            self.pos_tagged_lists = builder.write_dictionary()

    def generate_password(self):
        position = randint(0, 1)
        if position == 0:
            password = str(randint(10, 99)) + '-'
            password += self.random_uppercase(self.infl.plural_verb(self.get_word_type('verb'))) + '-'
        else:
            password = self.random_uppercase(self.get_word_type('verb')) + '-'
            password += str(randint(10, 99)) + '-'
        password += self.random_uppercase(self.infl.plural_adj(self.get_word_type('adj'))) + '-'
        noun = self.get_word_type('noun')
        if noun[-1] == 's':
            noun = noun[:-1]
        password += self.random_uppercase(self.infl.plural_noun(noun))
        return password

    @staticmethod
    def random_uppercase(word):
        has_uppercase = False
        new_word = ''
        for c in word:
            if has_uppercase:
                new_word += c
            else:
                ch = choice((0, 1))
                new_word += (str.lower, str.upper)[ch](c)
                if ch:
                    has_uppercase = True
        return new_word

    def get_word_type(self, pos_type):
        return choice(self.pos_tagged_lists[pos_type])


def main(argv):
    amount = 200
    minlength = 3
    maxlength = 10
    vector_type = "glove-twitter-50"
    passwords = 1

    try:
        opts, args = getopt.getopt(argv, "a:l:h:p:m:g", ["amount=", "minlength=", "maxlength=", "passwords=", "model=",
                                                         "generate-dictionary"])
    except getopt.GetoptError:
        with open('help', 'r') as file:
            print(file.read())
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-a", "--amount"):
            amount = int(arg)
        elif opt in ("-l", "--minlength"):
            minlength = int(arg)
        elif opt in ("-h", "--maxlength"):
            maxlength = int(arg)
        elif opt in ("-p", "--passwords"):
            passwords = int(arg)
        elif opt in ("-m", "--model"):
            vector_type = str(arg)
        elif opt in ("-g", "--generate-dictionary"):
            try:
                os.remove("dictionary.json")
            except:
                continue

    generator = PasswordGenerator(num_similar_words=amount, min_length=minlength, max_length=maxlength,
                                  vector_type=vector_type)
    password_list = []

    for i in range(passwords):
        password = generator.generate_password()
        password_list.append(password)
        print(password)

    return password_list


if __name__ == "__main__":
    main(sys.argv[1:])
