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

from Model import Model

class InterpolatedModel(Model):
    def __init__(self):
        pass

    def train(self, filename):
        pass

    def load(self, filename):
        pass

    def save(self, filename):
        pass

    def get_probability(self, word, history):
        pass

if __name__ == '__main__':
    pass
