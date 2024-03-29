"""Module with utilities for testing models on input data streams.

"""
import math

from InterpolatedModel import InterpolatedModel

VOCAB_FILE = 'data/vocabulary.txt'

def next_tag_probs(model, history, vocabulary):
    """Returns a list of probabilities for each word in the
    vocabulary given the model and the history.

    """
    tag_probs = [model.get_probability(v, history)
                 for v in vocabulary]
    return zip(tag_probs, vocabulary)

def perplexity(token_probs):
    """Returns the perplexity of list of probabilities
    in the token_probs list

    """
    log_probs = [math.log(p, 2) for p in token_probs]
    avg_ll = sum(log_probs) / float(len(log_probs))
    return 2 ** (-avg_ll)

def predict(model, history, vocabulary):
    """Pass the model, history, and vocabulary to this function.
    Returns a 2-tuple in which the most likely token is the first
    item, and a dictionary mapping tokens to likelihoods is the
    second item.

    """
    tag_probs = next_tag_probs(model, history, vocabulary)
    prediction = max(tag_probs)[1]
    tag_probs = dict( [(v,p) for p,v in tag_probs ])
    return prediction, tag_probs

if __name__ == '__main__':
    import sys, logging
    logging.basicConfig(level=logging.DEBUG, format="DEBUG: %(message)s")
    
    if len(sys.argv) != 2:
        print 'usage: python model_testing.py <model directory>'
        sys.exit(1)

    m = InterpolatedModel()
    m.load(sys.argv[1])
    vocabulary = [l.strip() for l in open(VOCAB_FILE)]

    history = []
    token_probs = []
    correct_predictions = 0

    prediction, tag_probs = predict(m, history, vocabulary)
    print ' '.join('{0:.3e}'.format(tag_probs[v]) for v in vocabulary)
    sys.stdout.flush()

    line = sys.stdin.readline()
    while line:
        token = line.strip()

        if token == prediction: correct_predictions += 1
        history.append(token)
        token_probs.append(tag_probs[token])

        prediction, tag_probs = predict(m, history[-30:], vocabulary) # temporary fix
        print ' '.join('{0:.3e}'.format(tag_probs[v]) for v in vocabulary)
        sys.stdout.flush()
        line = sys.stdin.readline()

    print '{0} {1}'.format(float(correct_predictions) / len(history),
                           perplexity(token_probs))
    sys.stdout.flush()

