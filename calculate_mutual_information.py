#!/usr/bin/env python

"""
Calculates mutual information of trigger pairs
among all possible tag pairs and lists them in order of decreasing mutual information

Refer to p.17 of:
Ronald Rosenfeld, A Maximum Entropy Approach to Adaptive Statistical Language Modeling
"""

import numpy as np

def load_data(filename):
    words = [line.strip() for line in open(filename, 'r')]

    for index in xrange(len(words)):
        word = words[index]

        if index > 30:
            history = words[index-30:index]
        else:
            history = ['START'] * (30-index) + words[0:index]
        yield word, history

def entropy(counts):
    probs = counts / float(np.sum(counts))
    probs = probs[np.nonzero(probs)]
    return -np.sum(probs * np.log2(probs))

def calc_mutual_information(A, B):
    data = load_data('data/trainA.txt')

    As = []
    Bs = []

    for word, history in data:
        As.append( A in history[:-2] )
        Bs.append( word == B)

    counts_AB = np.histogram2d(As, Bs, bins=2)[0]
    counts_A  = np.histogram(As, bins=2)[0]
    counts_B  = np.histogram(Bs, bins=2)[0]

    entropy_AB = entropy(counts_AB)
    entropy_A  = entropy(counts_A)
    entropy_B  = entropy(counts_B)

    return entropy_A + entropy_B - entropy_AB

def main():
    vocab = [line.strip() for line in open('data/vocabulary.txt')]

    results = [(calc_mutual_information(A, B), A, B) for A in vocab for B in vocab]
    results.sort()
    results.reverse()

    for mutual_information, A, B in results:
        print '%s\t%s\t%s' % (A, B, mutual_information)

if __name__ == '__main__':
    main()

