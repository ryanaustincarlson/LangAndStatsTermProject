#!/usr/bin/env python

import unittest

from Unigram  import Unigram
from Bigram   import Bigram
from Trigram  import Trigram
from FourGram import FourGram
from FiveGram import FiveGram

class TestModels(unittest.TestCase):
    def setUp(self):
        self.vocab = [line.strip() for line in open('./data/vocabulary.txt')]

    def test_probability_sums_to_one(self):
        models  = [Unigram, Bigram, Trigram, FourGram, FiveGram]
        history = ['NNP', 'RB', 'VBZ', 'DT', 'JJ', 'NN']

        for model in models:
            m = model()
            m.train('./data/trainA.txt')

            probs = [m.get_probability(vocab, history) for vocab in self.vocab]
            self.assertAlmostEquals( sum(probs), 1.0, places=1 )


if __name__ == '__main__':
    unittest.main()
