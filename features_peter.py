"""A grammar rule is defined to be a 2-tuple in which the first item is
the name of the grammar rule (a string), and the second item is a list
of all of the constituents of the rule where the first item is the
'oldest' consitituent and the last item in the list is the 'newest'
constituent.

"""

import itertools
from collections import defaultdict
import pdb

vocabulary = [l.strip() for l in open('data/vocabulary.txt')]

def eval(word, history):
    feats = []
    for func in _my_features:
        feats.append((func.__name__, func(word, history)))
    feats.extend(unigram_features(word, history))
    feats.extend(bigram_features(word, history))
    return feats

def get_feature_funcs(rule_filename):
    feature_funcs = [grammar_rule_to_function(n, c)
                     for n, c in grammar_rule_dict(rule_filename).items()]
    return feature_funcs

def unigram_features(word, history):
    return [('unigram_{}'.format(v), word == v) for v in vocabulary]

def bigram_features(word, history):
    if len(history) > 0:
        bigram = tuple([history[-1], word])
        return [('bigram_{}_{}'.format(v1, v2), bigram == (v1,v2))
                for v1, v2 in itertools.product(vocabulary, vocabulary)]
    else:
        return [('bigram_{}_{}'.format(v1, v2), False)
                for v1, v2 in itertools.product(vocabulary, vocabulary)]

def grammar_rule_dict(filename):
    rule_dict = defaultdict(list)
    for name, constits in grammar_rules_from_file(filename):
        rule_dict[name].append(constits)
    return rule_dict

def grammar_rule_to_function(name, constits):
    def feature_func(word, history):
        seq = list(history)
        seq.append(word)
        for c in constits:
            if len(seq) < len(c):
                continue
            else:
                alignment = zip(reversed(seq), reversed(c))
                if all(x == y for x, y in alignment):
                    return 1
        return 0 

    feature_func.__name__ = 'feature_makes_constit_{0}'.format(name)
    return feature_func

def grammar_rules_from_file(filename):
    for line in (l.strip().split() for l in open(filename)):
        yield (line[0], line[2:])

_my_features = get_feature_funcs('resources/valid_rules.txt')

if __name__ == '__main__':
    test_corpus = [('JJ', ['FOO', 'BAR', 'JJ']),
            ('NNP', ['NNP', 'NNP', 'NNPS']),
            ('NN', ['FOO', 'BAR', 'DT'])]
    feature_funcs = get_feature_funcs('resources/valid_rules.txt')

    for w, h in test_corpus:
        print w, h
        for func in feature_funcs:
            if func(w,h):
                print func.__name__


