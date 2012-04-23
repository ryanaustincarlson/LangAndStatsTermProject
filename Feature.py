#!/usr/bin/env python

class Feature:
    """Define feature functions below"""
    @staticmethod
    def contains_NNP(word, history):
        return 'NNP' in history

    @staticmethod
    def contains_RB(word, history):
        return 'RB' in history

    @staticmethod
    def contains_JJ(word, history):
        return 'JJ' in history

    @staticmethod
    def contains_DT(word, history):
        return 'DT' in history


if __name__ == '__main__':
    methods = [getattr(Feature, method) for method in dir(Feature)
               if callable(getattr(Feature, method))]

    word = 'NNP'
    history = ['FOO', 'DT', 'NNP', 'BAR', 'BAZ']

    feature = {}
    for func in methods:
        feature[func.__name__] = func(word, history)

    print feature
