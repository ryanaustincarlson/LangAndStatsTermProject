#!/usr/bin/env python

import features_naoki
import features_peter
import features_ryan

import warnings

def load_feature_funcs():
    """deprecated"""
    warnings.warn('load_feature_funcs is deprecated')
    feature_funcs = []
    feature_funcs.extend( features_naoki.get_feature_funcs('data/vocabulary.txt') )
    feature_funcs.extend( features_peter.get_feature_funcs('resources/valid_rules.txt') )
    feature_funcs.extend( features_ryan.get_feature_funcs() )
    return feature_funcs

def eval(word, history):
    """Each feature_foo.eval() should return a list of 2-tuples,
    where the 1st element of the tuple is name of the feature
    and the 2nd element of the tuple is the corresponding value
    """
    features = []
    features.extend( features_naoki.eval(word, history) )
    features.extend( features_peter.eval(word, history) )
    features.extend( features_ryan.eval(word, history) )
    return features
