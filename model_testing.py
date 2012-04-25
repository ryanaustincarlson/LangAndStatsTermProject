"""Module with utilities for testing models on input data streams.

"""
import math

def next_tag_probs(model, history, vocabulary):
    """Returns a list of probabilities for each word in the
    vocabulary given the model and the history.

    """
    tag_probs = []
    for v in vocabulary:
        p = model.get_probability(v, history)
        tag_probs.append(p)
    return tag_probs

def perplexity(token_probs):
    """Returns the perplexity of list of probabilities
    in the token_probs list

    """
    log_probs = [math.log(p, 2) for p in token_probs]
    avg_ll = sum(log_probs) / float(len(log_probs))
    return 2 ** (-avg_ll)

def load_model(model_path):
    pass

if __name__ == '__main__':
    import sys
    
    if not len(sys.argv) == 2:
        print 'usage: python model_testing.py <path to model>'
        sys.exit(1)

    m = load_model(sys.argv[1])
    for line in sys.stdin:

