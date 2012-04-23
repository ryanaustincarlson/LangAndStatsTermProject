#!/usr/bin/env python

import sys
from nltk.classify import MaxentClassifier

from Model import Model

class Maxent(Model):
    def __init__(self):
        Model.__init__(self)
        self.feature_functions = self.load_feature_functions()

    def get_probability(self, word, history):
        feature = self.generate_feature(word, history)
        prob_dist = self.model.prob_classify(feature)
        return prob_dist.prob(word)

    def train(self, filename):
        words = [line.strip() for line in open(filename, 'r')]
        train_feats = []

        for index in xrange(len(words)):
            word    = words[index]
            start_index = index - 30 if index - 30 > 0 else 0 # look at the most recent 30 tags
            history = words[start_index:index]
            train_feats.append( (self.generate_feature(word, history), word) )

        self.model = MaxentClassifier.train(train_feats, algorithm='iis', trace=0,
                                            max_iter=1, min_lldelta=0.5)

    def generate_feature(self, word, history):
        feature = {}
        for func in self.feature_functions:
            feature.update( func(word, history) )
        return feature

    def load_feature_functions(self):
        return [getattr(self, method) for method in dir(self)
                if callable(getattr(self, method))
                and method.startswith('feature')]

    # Define feature functions below:
    # The method names MUST start with 'feature'
    def feature_contains_NNP(self, word, history):
        return {'nnp': 'NNP' in history}

    def feature_contains_RB(self, word, history):
        return {'rb':  'RB' in history}

def main():
    if len(sys.argv) != 2:
        print 'usage: %s training-filename' % sys.argv[0]
        sys.exit(1)

    training_filename = sys.argv[1]

    model = Maxent()
    model.train(training_filename)
    print model.get_probability('CC', ['NNP', 'RB', 'JJ'])
    print model.get_probability('NN', ['NNP', 'RB', 'JJ'])
    print model.get_probability('RB', ['NNP', 'RB', 'JJ'])

if __name__ == '__main__':
    main()
