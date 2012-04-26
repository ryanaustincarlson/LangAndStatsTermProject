"""Main model for our project. This model should be responsible for
splitting up the full training set into a train and dev set, training
the sub-models on the train set, and then training the interpolation
weights on the dev set. Some thoughts on the methods:

    train(filename) -> splits the train set, trains each model, and the
    interpolation weights

    load(filename) -> maybe filename should be a file with a list of
    paths to the individual models, and this model can load each one
    individually and store the objects in some internal list.

    save(filename) -> write each of its models out to disk, and produce
    a file with the path to each model that can then be fed into 'load'.

    get_probability(word, history) -> call get_probability on each
    sub-model, and then combine the scores using the interpolation
    weights calculated during training.

"""

import os.path as path

import interpolate, sample, logging
from Model import Model
from Unigram import Unigram
from Bigram import Bigram
from Trigram import Trigram
from write_model_predictions import get_output_filename

try:
  import cPickle as pickle
except:
  import pickle

# turn logging on or off
LOGGING_LEVEL = logging.DEBUG; #LOGGING_LEVEL = None
OUTPUT_DIR = 'output/'
WEIGHTS_FILENAME = OUTPUT_DIR + 'weights.pkl'

class InterpolatedModel(Model):
    def __init__(self):
        pass

    def train(self, filename):
        logging.basicConfig(level=LOGGING_LEVEL, format="DEBUG: %(message)s")

        all_filename = filename
        directory = all_filename[:all_filename.rfind('/')+1]
        train_filename = directory + 'train.txt'
        dev_filename = directory + 'dev.txt'

        dev_percent = 0.1

        # sample all-data into train and dev sets
        sample.main( [all_filename, train_filename, dev_filename, dev_percent] )
        logging.debug('Split {} into training ({}) and development ({})'.format(all_filename, train_filename, dev_filename))
        
        # train models on training set
        self.models = []
        self.model_names = []

        def add_model(ModelClass, name):
            self.models.append( ModelClass(train_filename) )
            self.model_names.append( name )
            logging.debug('Done training {} model'.format(self.model_names[-1]))

        add_model( Unigram, 'unigram' )
        add_model( Bigram, 'bigram' )
        add_model( Trigram, 'trigram' )
        # add_model( Maxent, 'maxent' )

        dev_words = [line.strip() for line in open(dev_filename, 'r')]

        # write predictions out to disk using dev set
        model_outputs = []
        for model,model_name in zip(self.models, self.model_names):
            model_outputs.append( get_output_filename(OUTPUT_DIR, dev_filename, model_name) )
            model.write_probability_list(dev_words, model_outputs[-1])
            logging.debug('Wrote dev set predictions using {} model'.format(model_name))

        # interpolate the models, get the weights
        self.weights = interpolate.interpolate(model_outputs)

        print self.weights

    def load(self, directory_name):
        self.weights = pickle.load(open(path.join(directory_name, 'weights.pkl')))

        self.models = {}

        models['unigram'] = Unigram()
        models['unigram'].load( path.join(directory_name, 'unigram.pkl') )

        models['bigram'] = Bigram()
        models['bigram'].load( path.join(directory_name, 'bigram.pkl') )

        models['trigram'] = Trigram()
        models['trigram'].load( path.join(directory_name, 'trigram.pkl') )

    def save(self, directory_name):
        with open(path.join(directory_name, 'weights.pkl'), 'w') as f:
            pickle.dump(self.weights, f)        

        for name, model in self.models:
            model.save(path.join(directory_name, name+'.pkl'))

    def get_probability(self, word, history):
        pass

if __name__ == '__main__':
    import sys

    model = InterpolatedModel()
    model.train(sys.argv[1])
    model.save()

    model.load()
