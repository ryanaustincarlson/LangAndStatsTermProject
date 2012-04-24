#!/usr/bin/env python

"""usage: python interpolate-naoki.py <prob-files>
\tprob-files contain lists of probabilities generated from the same dev set (and end in .prob)"""

import numpy as np
import sys

class DegenerateEM:
    def __init__(self, prob_streams, debug=False):
        num_models        = len(prob_streams)
        self.weights1     = self._gen_random_weights(num_models)
        self.prob_streams = np.vstack(prob_streams)
        self.debug        = debug

    def train(self):
        """runs the EM algorithm to convergence"""
        self._update()
        iteration = 1

        while not self._has_converged():
            self._print_stats(iteration)
            self._update()
            iteration += 1
        self._print_stats(iteration)

    def _print_stats(self, iteration):
        """prints stats for each iteration"""
        if self.debug:
            print '-' * 40
            print 'iteration: ', iteration
            print 'weights0: ', self.weights0
            print 'weights1: ', self.weights1
            likelihood0 = self._likelihood(self.weights0)
            likelihood1 = self._likelihood(self.weights1)
            print 'average likelihood: ', likelihood1
            ratio = ((likelihood1 - likelihood0) / np.abs(likelihood1))
            print 'ratio: ', ratio

    def _gen_random_weights(self, num_models):
        """generates random weights"""
        lambd = np.random.rand(1, num_models)[0]
        lambd = lambd / np.sum(lambd)
        if np.any(lambd == 0):
            return self._gen_random_weights(num_models)
        return lambd

    def _update(self):
        """updates the weight"""
        num_models = len(self.weights1)
        num_points = self.prob_streams.shape[1]
        s = np.array([0.0] * num_models)

        for j in range(num_models):
            for i in range(num_points):
                denom = sum(weight * self.prob_streams[k, i] for
                        k, weight in enumerate(self.weights1))
                numer = self.weights1[j] * self.prob_streams[j, i]
                s[j] += float(numer) / denom
        s = s / num_points
        self.weights0 = np.copy(self.weights1)
        self.weights1 = s
        
    def _has_converged(self):
        """checks if EM algorithm has converged"""
        likelihood0 = self._likelihood(self.weights0)
        likelihood1 = self._likelihood(self.weights1)

        return ((likelihood1 - likelihood0) / np.abs(likelihood1)) < 0.00001

    def _likelihood(self, weights):
        """calculates the (log) likelihood with the given weights"""
        num_models = len(weights)
        num_points = self.prob_streams.shape[1]

        sum_outer = 0.0
        for i in range(num_points):
            sum_inner = 0.0
            for k, weight in enumerate(weights):
                sum_inner += weight * self.prob_streams[k, i]

            if sum_inner > 0.0:
                sum_outer += np.log(sum_inner)
        likelihood = sum_outer / num_points
        return likelihood

def read_probs_file(fname):
    return [float(line.strip()) for line in open(fname, 'r')]

def main():
    if len(sys.argv) == 1:
        print __doc__
        sys.exit(1)

    fnames = sys.argv[1:]
    prob_streams = [read_probs_file(fname) for fname in fnames]

    em = DegenerateEM(prob_streams, debug=True)
    em.train() # run the EM algorithm
    print em.weights1

if __name__ == '__main__':
    main()
