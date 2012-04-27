#!/usr/bin/env python

import features_naoki
import features_peter
import features_ryan

def load_features():
    return features_naoki.get_feature_funcs('data/vocabulary.txt') + \
           features_peter.get_feature_funcs('resources/valid_rules.txt') + \
           features_ryan.get_feature_funcs()

