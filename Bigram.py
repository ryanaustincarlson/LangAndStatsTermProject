from NgramModel import NgramModel

class Bigram(NgramModel):
    def __init__(self):
        NgramModel.__init__(self, 2)

def main():
    import sys
    if len(sys.argv) != 2:
        print 'usage: %s training-filename' % sys.argv[0]

    training_filename = sys.argv[1]

    model = Bigram()
    model.train(training_filename)
  
    print model.get_probability('CC', ['NNP','RB'])
    print model.get_probability('NN', ['NNP','RB'])
    print model.get_probability('RB', ['NNP','RB'])
    print model.get_probability('<COMMA>', ['NNP','RB'])

if __name__ == '__main__':
    main()
