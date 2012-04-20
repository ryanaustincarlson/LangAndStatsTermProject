from Model import Model

class NgramModelException(Exception):
  def __init__(self, message):
    self.message = message
  def __str__(self):
    return repr(self.message)

class NgramModel(Model):
  def __init__(self, n):
    self.n = n

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
  n = 1
  filename = 'data/trainA.txt'

  model = NgramModel(4)
  model.train(filename)

  for tag in ['VBZ','NN','RB','<COMMA>']:
    try:
      print model.get_probability(tag, ['CC', 'NNP','RB'])
    except Exception as e:
      print e.message

if __name__ == '__main__': main()
