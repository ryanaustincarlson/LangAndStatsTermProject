#!/usr/bin/env python

def load_pairs(fname):
    pairs = []
    with open(fname, 'r') as f:
        for line in f:
            a, b, mi = line.strip().split('\t')
            if float(mi) > 0.001:
                pairs.append( (a, b) )
    return pairs

TAGS      = [line.strip() for line in open('data/vocabulary.txt', 'r')]
TAG_PAIRS = load_pairs('resources/tagpairs_mutual_information.txt')

def trigger_pair_feats(word, history):
    features = []
    for tag_a, tag_b in TAG_PAIRS:
        feature_name = 'feature_trigger_pair_{0}_{1}'.format(tag_a, tag_b)
        if word == tag_b and tag_a in history[:-2]:
            features.append( (feature_name, True) )
        else:
            features.append( (feature_name, False) )
    return features

def distance_from_last_tag_feats(word, history):
    features = []
    for tag in TAGS:
        feature_name = 'feature_distance_from_last_{0}'.format(tag)
        if not tag in history:
            features.append( (feature_name, 0) )
        else:
            hist = list(history)
            hist.reverse()
            features.append( (feature_name, hist.index(tag) + 1) )
    return features

def tag_count_feats(word, history):
    features = []
    for tag in TAGS:
        feature_name = 'feature_count_{0}'.format(tag)
        features.append( (feature_name, history.count(tag)) )
    return features

def eval(word, history):
    feature_funcs = [
            trigger_pair_feats,
            distance_from_last_tag_feats,
            tag_count_feats,
            ]

    features = []
    for func in feature_funcs:
        features.extend( func(word, history) )
    return features

if __name__ == '__main__':
    test_corpus = [
            ('JJ', ['FOO', 'JJ', 'BAR', 'JJ']),
            ('NNP', ['RB', 'NNP', 'NNP', 'NNPS']),
            ('NN', ['CC', 'FOO', 'BAR', 'DT']),
            ('<RIGHTPAR>', ['<LEFTPAR>', 'CC', 'NNP', 'PRP']),
            ('CD', ['CD', 'CC', 'CC', 'NNP', 'PRP']),
            ]
    feature_funcs = get_feature_funcs('data/vocabulary.txt')

    for word, history in test_corpus:
        print word, history
        for func in feature_funcs:
            val = func(word, history)
            if val:
                print func.__name__, val

