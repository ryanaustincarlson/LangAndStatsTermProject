#!/usr/bin/env python

import sys
from nltk.classify import MaxentClassifier

from Model import Model
from Feature import Feature

class Maxent(Model):
    def __init__(self, history_length=30):
        Model.__init__(self)
        self.feature_functions = self.load_feature_functions()
        self.history_length    = history_length

    def get_probability(self, word, history):
        feature = self.generate_feature(word, history)
        prob_dist = self.model.prob_classify(feature)
        return prob_dist.prob(word)

    def train(self, filename):
        words = [line.strip() for line in open(filename, 'r')]
        train_feats = []

        for index in xrange(len(words)):
            word = words[index]
            start_index = index - self.history_length \
                if index - self.history_length > 0 else 0 # look at the most recent N tags
            history = words[start_index:index]
            train_feats.append( (self.generate_feature(word, history), word) )

        self.model = MaxentClassifier.train(train_feats, algorithm='iis', trace=0,
                                            max_iter=1, min_lldelta=0.5)

    def generate_feature(self, word, history):
        feature = {}
        for func in self.feature_functions:
            feature[func.__name__] = func(word, history)
        return feature

    def load_feature_functions(self):
        return [getattr(Feature, method) for method in dir(Feature)
                if callable(getattr(Feature, method))]

def main():
    if len(sys.argv) != 2:
        print 'usage: %s training-filename' % sys.argv[0]
        sys.exit(1)

    training_filename = sys.argv[1]

    model = Maxent(history_length=30)
    model.train(training_filename)
    print model.get_probability('CC', ['NNP', 'RB', 'JJ'])
    print model.get_probability('NN', ['NNP', 'RB', 'JJ'])
    print model.get_probability('RB', ['NNP', 'RB', 'JJ'])

if __name__ == '__main__':
    main()
