import functools
from collections import defaultdict
from Model import Model
import pdb

try:
    import cPickle as pickle
except:
    import pickle

vocabulary = [l.strip() for l in open('data/vocabulary.txt')]

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

    @staticmethod
    def good_turing_estimate(count, freq_counts, cutoff=8):
        if count > 8:
            return float(count)
        elif count == 0:
            return freq_counts[1] / float(sum(r*c for r, c in freq_counts.items()))
        else:
            return float(count + 1) * freq_counts[count+1] / freq_counts[count]

    def train(self, filename):
        def get_ngrams(n, words):
            for i in xrange(len(words) - n):
                yield words[i:i+n]

        words = [line.strip() for line in open(filename, 'r')]

        # add nltk words
        words += [line.strip() for line in open('data/nltk_tags.txt', 'r')]

        ddict_int = functools.partial(defaultdict, int)
        self.histories = defaultdict(int)
        self.ngrams = defaultdict(int)
        self.hist_freq_counts = defaultdict(int)
        self.ngram_freq_counts = defaultdict(int)

        for history in get_ngrams(self.n-1, words):
            self.histories[tuple(history)] += 1

        for ngram in get_ngrams(self.n, words):
            self.ngrams[tuple(ngram)] += 1

        for count in self.histories.values():
            self.hist_freq_counts[count] += 1
            
        for count in self.ngrams.values():
            self.ngram_freq_counts[count] += 1

        self.num_histories = float(sum(self.histories.values()))
        self.num_ngrams = float(sum(self.ngrams.values()))

    def get_probability(self, word, history):
        def good_turing(ngram):
            count = self.ngrams[ngram]
            if count > 8:
                return self.ngrams[ngram] / float(self.num_ngrams)
            elif count == 0:
                return self.ngram_freq_counts[1] / float(self.num_ngrams)
            else:
                return ( (r+1) * self.ngram_freq_counts[r+1] /
                         self.ngram_freq_counts[r] / self.num_ngrams)

        if len(history) < self.n - 1:
            return 0.0
        else:
            history = history[-(self.n - 1):] if self.n > 1 else []
            ngram = tuple(history + [word])
            all_ngrams = [tuple(history + [v]) for v in vocabulary]
            return good_turing(ngram) / sum(good_turing(n) for n in all_ngrams)
  
    def save(self, filename):
        pickle_tuple = (self.histories,
                        self.ngrams,
                        self.hist_freq_counts,
                        self.ngram_freq_counts,
                        self.num_histories,
                        self.num_ngrams)
        pickle.dump(pickle_tuple, open(filename, 'w'))
  
    def load(self, filename, backoff_model=None):
        (self.histories, self.ngrams, self.hist_freq_counts,
         self.ngram_freq_counts, self.num_histories, self.num_ngrams) = pickle.load(open(filename))
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
