#!/usr/bin/env python

import nltk

def nltk_tags():
    vocab = [line.strip() for line in open('data/vocabulary.txt', 'r')]

    # grab all the tags
    tags = []
    for sent in nltk.corpus.treebank.tagged_sents():
        tags += [tag for word,tag in sent]

    print len(tags)

    remap_dict = {
            '.':'<PERIOD>',
            ':':'<COLON>',
            ',':'<COMMA>',
            '(':'<LEFTPAR>',
            ')':'<RIGHTPAR>',
            }

    # remap tags to what we actually use 
    # really just punctuation is different
    for i in xrange(len(tags)):
        tag = tags[i]
        if tag in remap_dict:
            tags[i] = remap_dict[tag]

    new_tags = []
    for tag in tags:
        if tag in vocab:
            new_tags.append( tag )
    tags = new_tags

    for tag in tags: print tag

if __name__ == '__main__':
    nltk_tags()
