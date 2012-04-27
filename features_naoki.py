#!/usr/bin/env python

def tag_count_func(tag):
    def feature_func(word, history):
        return history.count(tag)

    feature_func.__name__ = 'feature_count_{0}'.format(tag)
    return feature_func

def distance_from_last_tag_func(tag):
    def feature_func(word, history):
        if not tag in history:
            return 0
        else:
            hist = list(history)
            hist.reverse()
            return hist.index(tag) + 1

    feature_func.__name__ = 'feature_distance_from_last_{0}'.format(tag)
    return feature_func


def trigger_pairs_func(tag_a, tag_b):
    def feature_func(word, history):
        if word == tag_b and tag_a in history[:-3]:
            return 1
        else:
            return 0
    feature_func.__name__ = 'feature_trigger_pair_{0}_{1}'.format(tag_a, tag_b)
    return feature_func

def load_pairs(fname):
    pairs = []
    with open(fname, 'r') as f:
        for line in f:
            a, b, mi = line.strip().split('\t')
            if float(mi) > 0.001:
                pairs.append( (a, b) )
    return pairs

def get_feature_funcs(vocab_fname):
    tags      = [line.strip() for line in open(vocab_fname, 'r')]
    tag_pairs = load_pairs('resources/tagpairs_mutual_information.txt')

    feature_funcs = []
    feature_funcs.extend(tag_count_func(tag) for tag in tags)
    feature_funcs.extend(distance_from_last_tag_func(tag) for tag in tags)
    feature_funcs.extend(trigger_pairs_func(tag_a, tag_b) for tag_a, tag_b in tag_pairs)
    return feature_funcs

if __name__ == '__main__':
    test_corpus = [('JJ', ['FOO', 'JJ', 'BAR', 'JJ']),
            ('NNP', ['RB', 'NNP', 'NNP', 'NNPS']),
            ('NN', ['CC', 'FOO', 'BAR', 'DT'])]
    feature_funcs = get_feature_funcs('data/vocabulary.txt')

    for word, history in test_corpus:
        print word, history
        for func in feature_funcs:
            val = func(word, history)
            if val:
                print func.__name__, val

