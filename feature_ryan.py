
VOCAB = [line.strip() for line in open('data/vocabulary.txt', 'r')]

from pprint import pprint

# this is actually just a degenerate case of the subsets function below
def contains():
  def vocab(v):
    def contains_specific(word, history):
      #print v,
      return v in history
    return contains_specific
  return [vocab(v) for v in VOCAB]

def subsets():
  from itertools import combinations
  def vocab(vlist):
    def subsets_specific(word, history):
      #print 'vlist:',vlist,
      return reduce(lambda x,y: x or y, [v in history for v in vlist])
    return subsets_specific

  min_choose = 1
  max_choose = 3

  functions = []
  for choose in range(min_choose, max_choose+1):
    functions += [vocab(v) for v in combinations(VOCAB, choose)]
  return functions

ALL_FUNCTIONS = subsets()

def main():

  word = 'NNP'
  history = ['NNP','<COMMA>']

  #functions = contains()
  functions = subsets()
  #functions = contains() + subsets()
  for fcn in functions:
    print fcn( word, history )
    #if fcn( word, history ):
    #  print 'hey!'
    #else:
    #  print

if __name__ == '__main__': main()

