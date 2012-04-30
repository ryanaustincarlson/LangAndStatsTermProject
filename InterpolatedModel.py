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

import os
import os.path as path

import interpolate, sample, logging, tempfile
from pprint import pprint
from write_model_predictions import get_output_filename

from Model import Model
from Unigram import Unigram
from Bigram import Bigram
from Trigram import Trigram
from Fourgram import Fourgram
from Fivegram import Fivegram
from Sixgram  import Sixgram
from Sevengram import Sevengram
from Eightgram import Eightgram
from Maxent import Maxent

try:
  import cPickle as pickle
except:
  import pickle

# turn logging on or off
LOGGING_LEVEL = logging.DEBUG; #LOGGING_LEVEL = None

class InterpolatedModel(Model):
    def __init__(self):
        self.model_names = [
                'unigram',
                'bigram',
                'trigram',
                'fourgram',
                'fivegram',
                'sixgram',
                'sevengram',
                'eightgram',
                'maxent',
                ]

    def train(self, filename, output_dir):
        logging.basicConfig(level=LOGGING_LEVEL, format="DEBUG: %(message)s")

        all_filename = filename

        try:
            os.mkdir(output_dir)
        except OSError: # directory already exists
            pass

        train_filename = path.join(output_dir, 'train.txt')
        dev_filename = path.join(output_dir, 'dev.txt')

        dev_percent = 0.1

        # sample all-data into train and dev sets
        sample.main( [all_filename, train_filename, dev_filename, dev_percent] )
        logging.debug('Split {0} into training ({1}) and development ({2})'.format(all_filename, train_filename, dev_filename))
        
        # train models on training set
        self.models = {}

        def add_model(ModelClass, name):
            self.models[name] = ModelClass()
            self.models[name].train(train_filename)

            logging.debug('Done training {0} model'.format(name))

        add_model( Unigram,  'unigram' )
        add_model( Bigram,   'bigram' )
        add_model( Trigram,  'trigram' )
        add_model( Fourgram, 'fourgram' )
        add_model( Fivegram, 'fivegram' )
        add_model( Sixgram,  'sixgram' )
        add_model( Sevengram, 'sevengram')
        add_model( Eightgram, 'eightgram')
        add_model( Maxent,   'maxent' )

        #self.models['bigram'].backoff_model   = self.models['unigram']
        #self.models['trigram'].backoff_model  = self.models['bigram']
        #self.models['fourgram'].backoff_model = self.models['trigram']
        #self.models['fivegram'].backoff_model = self.models['fourgram']
        #self.models['sixgram'].backoff_model  = self.models['fivegram']

        dev_words = [line.strip() for line in open(dev_filename, 'r')]

        # write predictions out to disk using dev set
        model_outputs = []
        model_output_dir = tempfile.mkdtemp()
        logging.debug('Temporary Output Directory: {0}'.format(model_output_dir))
        for model_name in self.model_names:
            model = self.models[model_name]

            model_outputs.append( path.join( model_output_dir, model_name + '.probs' ) )
            model.write_probability_list(dev_words, model_outputs[-1])
            logging.debug('Wrote dev set predictions using {0} model'.format(model_name))

        # interpolate the models, get the weights
        weights_list = interpolate.interpolate(model_outputs)
        logging.debug('Weights: {0}'.format(weights_list))

        self.weights = dict( zip( self.model_names, weights_list ) )

    def load(self, directory_name):
        self.weights = pickle.load(open(path.join(directory_name, 'weights.pkl')))

        self.models = {}

        def load_model(name, ModelClass):
            self.models[name] = ModelClass()
            self.models[name].load( path.join(directory_name, name + '.pkl') )
            logging.debug("Loaded {0} model from disk".format(name))

        load_model('unigram',  Unigram)
        load_model('bigram',   Bigram)
        load_model('trigram',  Trigram)
        load_model('fourgram', Fourgram)
        load_model('fivegram', Fivegram)
        load_model('sixgram',  Sixgram)
        load_model('sevengram', Sevengram)
        load_model('eightgram', Eightgram)
        load_model('maxent',   Maxent)

        #self.models['bigram'].backoff_model   = self.models['unigram']
        #self.models['trigram'].backoff_model  = self.models['bigram']
        #self.models['fourgram'].backoff_model = self.models['trigram']
        #self.models['fivegram'].backoff_model = self.models['fourgram']
        #self.models['sixgram'].backoff_model  = self.models['fivegram']

    def save(self, directory_name):
        if not path.isdir(directory_name): os.makedirs(directory_name)

        with open(path.join(directory_name, 'weights.pkl'), 'w') as f:
            pickle.dump(self.weights, f)        
            logging.debug("Saved weights to disk")

        for name, model in self.models.items():
            model.save(path.join(directory_name, name+'.pkl'))
            logging.debug("Saved {0} model to disk".format(name))

    def get_probability(self, word, history):
        prediction = 0
        for model_name, model in self.models.items():
            prediction += model.get_probability(word, history) * self.weights[model_name]
        return prediction


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print 'usage: {0} all-data output_dir'.format(sys.argv[0])
        sys.exit(1)

    model = InterpolatedModel()
    model.train(sys.argv[1], sys.argv[2])
    model.save(sys.argv[2])

    #model.load(sys.argv[2])
