

from pprint import pprint

def subsets():

  all_groups = []
  all_groups.append( ['JJ','JJR','JJS'] ) # adjectives
  all_groups.append( ['NN','NNS','NNP','NNPS'] ) # nouns
  all_groups.append( ['PRP','PRP$'] ) # pronouns
  all_groups.append( ['RB','RBR'] ) # adverbs
  all_groups.append( ['VB','VBD','VBG','VBN','VBP','VBZ'] ) # verbs
  all_groups.append( ['WDT','WP','WRB'] ) # wh_words
  all_groups.append( ['<COLON>','<COMMA>','<LEFTPAR>','<PERIOD>','<RIGHTPAR>'] ) # punctuation
  all_groups.append( ['CC'] ) # coordinating conjunction
  all_groups.append( ['CD'] ) # cardinal number
  all_groups.append( ['DT'] ) # determiner
  all_groups.append( ['EX'] ) # existential THERE
  all_groups.append( ['IN'] ) # preposition or subordinating conjunction
  all_groups.append( ['MD'] ) # modal
  all_groups.append( ['POS'] ) # possessive ending
  all_groups.append( ['RP'] ) # particle
  all_groups.append( ['TO'] ) # TO
  all_groups.append( ['CC', 'CD', 'DT', 'EX', 'IN', 'MD', 'POS', 'RP', 'TO'] ) #other

  def vocab(group, lookback):
    def subsets_specific(word, history):

      # check the last *lookback* entries in the history and check if one of the tags
      # in the given group is there
      return reduce(lambda x,y: x or y, [tag in history[-lookback:] for tag in group])

    subsets_specific.__name__ = 'subsets_specific_{0}'.format(group)
    return subsets_specific

  min_lookback = 1
  max_lookback = 3

  functions = []
  for lookback in range(min_lookback, max_lookback+1):
    for group in all_groups:
      functions.append( vocab(group, lookback) )

  return functions

def get_feature_funcs():
  return subsets()

def main():

  word = 'NNP'
  history = ['NNP', 'CD','<COMMA>']

  #functions = contains()
  functions = subsets()
  #functions = contains() + subsets()
  for fcn in functions:
    print fcn( word, history ),'\t',
    print fcn.__name__
    #if fcn( word, history ):
    #  print 'hey!'
    #else:
    #  print

if __name__ == '__main__': main()

