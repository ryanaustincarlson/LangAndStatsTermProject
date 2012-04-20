#!/usr/bin/env aython

import unittest
try:
     import cPickle as pickle
except:
     import pickle

from Trigram import Trigram

class TestPickle(unittest.TestCase):
  def setUp(self):
    self.model = Trigram()
    self.model.train('./data/trainA.txt')

  def test_pickle(self):
    pkl = pickle.dumps(self.model, protocol=1)
    pickled_model = pickle.loads(pkl)

    word = 'CC'
    history = ['NNP', 'RB', 'JJ']

    self.assertEquals(self.model.get_probability(word, history),
                      pickled_model.get_probability(word, history))

if __name__ == '__main__':
  unittest.main()
