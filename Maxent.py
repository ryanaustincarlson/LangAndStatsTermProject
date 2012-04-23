#!/usr/bin/env python

import sys
import maxent
from maxent.cmaxent import MaxentModel

from Model import Model
from Feature import Feature

class Maxent(Model):
    def __init__(self, history_length=30):
        Model.__init__(self)
        self.feature_functions = self.load_feature_functions()
        self.history_length    = history_length

    def get_probability(self, word, history):
        features = self.generate_features(word, history)
        prob_dist = self.model.eval_all(features)

        for tag, prob in prob_dist:
            if tag == word:
                return prob
        return 0.0

    def load_data(self, filename):
        words = [line.strip() for line in open(filename, 'r')]

        for index in xrange(len(words)):
            word = words[index]
            start_index = index - self.history_length \
                if index - self.history_length > 0 else 0 # look at the most recent N tags
            history = words[start_index:index]
            yield word, history

    def train(self, filename):
        data = self.load_data(filename)
        m = MaxentModel()

        m.begin_add_event()
        for word, history in data:
            features = self.generate_features(word, history)
            m.add_event(features, word)
        m.end_add_event()

        m.train()
        self.model = m

    def generate_features(self, word, history):
        features = []
        for func in self.feature_functions:
            val = func(word, history)
            features.append((func.__name__, val))
        return features

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
