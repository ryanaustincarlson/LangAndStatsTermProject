#!/usr/bin/env python

import sys

from NgramModel import NgramModel

class Sixgram(NgramModel):
  def __init__(self):
    NgramModel.__init__(self, 6)

def main():
  if len(sys.argv) != 2:
    print 'usage: %s training-filename' % sys.argv[0]
    sys.exit(1)

  training_filename = sys.argv[1]

  model = Sixgram()
  model.train(training_filename)

  print model.get_probability('CC', ['NNP', 'RB', 'JJ'])
  print model.get_probability('NN', ['NNP', 'RB', 'JJ'])
  print model.get_probability('RB', ['NNP', 'RB', 'JJ'])

if __name__ == '__main__':
  main()
