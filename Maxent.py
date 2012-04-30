#!/usr/bin/env python

import sys
import maxent
from maxent.cmaxent import MaxentModel

from Model import Model
import Feature

maxent.set_verbose(100)

class Maxent(Model):
    def __init__(self, history_length=30):
        Model.__init__(self)
        self.history_length    = history_length

    def get_probability(self, word, history):
        features  = self.generate_features(word, history)
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

        m.train(iter=50)
        self.model = m

    def generate_features(self, word, history):
        history  = self.pad_history(history)
        features = Feature.eval(word, history)
        return features

    def pad_history(self, history):
        """Pads 'START' tag if history length is less than history_length"""
        if len(history) < self.history_length:
            history = ['START'] * (self.history_length - len(history)) + history
        return history

    def save(self, filename):
        """Saves the model to a file. Just calls the internal model's
        save function. We discard the value of history_length and 
        feature_funcs. We assume history_length will always be the same,
        and we just reload the feature_funcs.

        """
        self.model.save(filename)

    def load(self, filename):
        """Loads a maxent model from disk."""
        self.model = MaxentModel()
        self.model.load(filename)


def main():
    if len(sys.argv) != 2:
        print 'usage: %s training-filename' % sys.argv[0]
        sys.exit(1)

    training_filename = sys.argv[1]
    model_file = 'maxent_save_test.mdl'

    model = Maxent(history_length=30)
    model.train(training_filename)
    p1 = model.get_probability('CC', ['NNP', 'RB', 'JJ'])
    p2 = model.get_probability('NN', ['NNP', 'RB', 'JJ'])
    p3 = model.get_probability('RB', ['NNP', 'RB', 'JJ'])
    model.save(model_file)

    model2 = Maxent(history_length=30)
    model2.load(model_file)
    assert p1 == model2.get_probability('CC', ['NNP', 'RB', 'JJ']) 
    assert p2 == model2.get_probability('NN', ['NNP', 'RB', 'JJ'])
    assert p3 == model2.get_probability('RB', ['NNP', 'RB', 'JJ'])

if __name__ == '__main__':
    main()
