import functools
from collections import defaultdict
from Model import Model

try:
    import cPickle as pickle
except:
    import pickle

class NgramModelException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class NgramModel(Model):
    def __init__(self, n, backoff_model=None, filename=None):
        ''' optional filename parameter since we often want to train on initialization '''
        self.n = n
        self.backoff_model = backoff_model
        if filename: self.train(filename)

    def train(self, filename):
        def get_ngrams(n, words):
            for i in xrange(len(words) - n):
                yield words[i:i+n]

        words = [line.strip() for line in open(filename, 'r')]
        ddict_int = functools.partial(defaultdict, int)
        self.ngrams = defaultdict(ddict_int)

        for gram in get_ngrams(self.n, words):
            context = tuple(gram[:-1]) if self.n > 1 else ()
            word = gram[-1]
            self.ngrams[context][word] += 1

        for context, counts in self.ngrams.items():
            total = float(sum(counts.values()))
            for k in counts:
                counts[k] /= total
  
    def get_probability(self, word, history):
        context = tuple(history[-(self.n - 1):]) if self.n > 1 else ()
        if not self.ngrams[context][word] and self.backoff_model:
            return float(self.backoff_model.get_probability(word, history))
        else:
            return float(self.ngrams[context][word])
  
    def save(self, filename):
        pickle.dump(self.ngrams, open(filename, 'w'))
  
    def load(self, filename, backoff_model=None):
        self.ngrams = pickle.load(open(filename, 'r'))
        self.backoff_model = backoff_model
    
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
