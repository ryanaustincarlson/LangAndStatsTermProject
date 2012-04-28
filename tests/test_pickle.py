#!/usr/bin/env python

import unittest
try:
     import cPickle as pickle
except:
     import pickle

from Unigram  import Unigram
from Bigram   import Bigram
from Trigram  import Trigram
from Fourgram import Fourgram
from Fivegram import Fivegram
from Maxent   import Maxent

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
    models  = [Unigram, Bigram, Trigram, Fourgram, Fivegram]

    for model in models:
      m = model()
      m.train('./data/trainA.txt')

      fname = '/tmp/test_%s.pkl' % (model)
      m.save(fname)

      loaded_m = model()
      loaded_m.load(fname)

      word = 'CC'
      history = ['NNP', 'RB', 'JJ']

      self.assertEquals( m.get_probability(word, history),
          loaded_m.get_probability(word, history) )


if __name__ == '__main__':
  unittest.main()
