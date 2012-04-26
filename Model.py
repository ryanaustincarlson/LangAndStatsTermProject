
class Model:

  def __init__(self):
    pass

  def get_probability(word, history):
    assert True is False

  def train(filename):
    assert True is False

  def save(filename):
    assert True is False

  def load(filename):
    assert True is False

  def probability_list(self, words):
    def probability_or_zero(word, history):
      """ if probability exists, return it; otherwise, assign zero probability """
      try:
        return self.get_probability(word, history)
      except Exception:
        return 0
    return [probability_or_zero(words[index],words[:index]) for index in xrange(len(words))]

  def write_probability_list(self, words, outfilename):
    probability_list = self.probability_list(words)
    outfile = open(outfilename, 'w')
    for prob in probability_list:
      outfile.write('{}\n'.format(prob))
    outfile.close()

