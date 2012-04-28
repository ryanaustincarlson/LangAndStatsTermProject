#!/usr/bin/env python

import unittest
try:
     import cPickle as pickle
except:
     import pickle

from Trigram import Trigram
from Unigram import Unigram

class TestPickle(unittest.TestCase):
  def setUp(self):
    self.model = Trigram()
    self.model.train('./data/trainA.txt')

  #def test_pickle(self):
  #  pkl = pickle.dumps(self.model, protocol=1)
  #  pickled_model = pickle.loads(pkl)

  #  word = 'CC'
  #  history = ['NNP', 'RB', 'JJ']

  #  self.assertEquals(self.model.get_probability(word, history),
  #                    pickled_model.get_probability(word, history))


  def test_model_pickle(self):
    model = Unigram()
    model.train('./data/trainA.txt')

    fname = '/tmp/test_unigram.pkl'
    model.save(fname)

    loaded_model = Unigram()
    loaded_model.load(fname)

    word = 'CC'
    history = ['NNP', 'RB', 'JJ']

    self.assertEquals( model.get_probability(word, history),
        loaded_model.get_probability(word, history) )


if __name__ == '__main__':
  unittest.main()
