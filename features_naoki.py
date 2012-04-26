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

def get_feature_funcs(vocab_fname):
    tags  = [line.strip() for line in open(vocab_fname, 'r')]

    feature_funcs = []
    feature_funcs.extend(tag_count_func(tag) for tag in tags)
    feature_funcs.extend(distance_from_last_tag_func(tag) for tag in tags)
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

