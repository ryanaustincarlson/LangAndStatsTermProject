#!/usr/bin/env python

import features_naoki
import features_peter
import features_ryan

def load_features():
    features = []
    features.extend( features_naoki.get_feature_funcs('data/vocabulary.txt') )
    features.extend( features_peter.get_feature_funcs('resources/valid_rules.txt') )
    features.extend( features_ryan.get_feature_funcs() )
    return features

