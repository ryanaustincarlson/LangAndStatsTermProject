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
    def __init__(self, n, filename=None):
        ''' optional filename parameter since we often want to train on initialization '''
        self.n = n
        if filename: self.train(filename)

    def train(self, filename):
        words = [line.strip() for line in open(filename, 'r')]
        int_def_dict = functools.partial(defaultdict, int)
        self.ngrams = defaultdict(int_def_dict)
        for i in xrange(len(words) - self.n):
            seq = words[i:i+self.n]
            context = tuple(words[:-1])
            word = words[-1]
            self.ngrams[context][word] += 1
        for context, counts in self.ngrams.items():
            total = float(sum(counts.values()))
            for k in counts:
                counts[k] /= total
  
    def get_probability(self, word, history):
        seq = tuple(history[-(self.n-1):] + [word])
        return float(self.ngrams[seq])
  
    def save(self, filename):
        pickle.dump(self.ngrams, open(filename, 'w'))
  
    def load(self, filename):
        self.ngrams = pickle.load(open(filename, 'r'))
    
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
