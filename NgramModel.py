from Model import Model

class NgramModelException(Exception):
  def __init__(self, message):
    self.message = message
  def __str__(self):
    return repr(self.message)

class NgramModel(Model):
  def __init__(self, n, filename=None):
    ''' optional filename parameter since we often want to train on initialization '''
    self.n = n
    if filename: self.train(filename)

  def train(self, filename):
    import nltk
    words = [line.strip() for line in open(filename, 'r')]
    self.model = nltk.NgramModel(self.n, words)

  def get_probability(self, word, history):
    if self.n == 1:
      history = '' # if unigram, throw away the history
    else:
      history = history[-(self.n-1):] # otherwise, grab the last (n-1) entries

    if len(history) < self.n-1:
      raise NgramModelException("history (%s) is too short" % history)

    try:
      return self.model.prob(word, history)
    except Exception:
      raise NgramModelException("word (%s) not found in history (%s)" % (word, history))
    
def main():
  from pprint import pprint
  n = 2
  filename = 'data/trainA.txt'
  probability_list_outfilename = 'output/probability_list_test.txt'

  model = NgramModel(n)
  model.train(filename)

  for tag in ['VBZ','NN','RB','<COMMA>']:
    try:
      print model.get_probability(tag, ['CC', 'NNP','RB'])
    except Exception as e:
      print e.message

  sequence = [ 'CC', 'NNP', 'RB', 'VBZ', 'DT', 'JJ', 'NN', 'VBG', 'DT', 'NN', 'IN', 'JJ', 'NNS', 'IN', 'DT', 'NN', '<PERIOD>', 'IN', 'CD', 'NNP']
  probability_list = model.probability_list(sequence)
  pprint(zip(sequence,probability_list))
  
  model.write_probability_list(sequence, probability_list_outfilename)



if __name__ == '__main__': main()
