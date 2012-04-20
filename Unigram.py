from NgramModel import NgramModel

class Unigram(NgramModel):
  def __init__(self):
    NgramModel.__init__(self, 1)

def main():
  import sys
  if len(sys.argv) != 2:
    print 'usage: %s training-filename' % sys.argv[0]

  training_filename = sys.argv[1]

  model = Unigram()
  model.train(training_filename)

  print model.get_probability('CC', ['NNP','RB'])
  print model.get_probability('NN', ['NNP','RB'])
  print model.get_probability('RB', ['NNP','RB'])
  print model.get_probability('<COMMA>', ['NNP','RB']) # should throw an error

if __name__ == '__main__':
  main()
