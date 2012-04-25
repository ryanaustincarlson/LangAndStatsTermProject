import sys
import random
import math

epsilon = 1e-5

def log_likelihood(lambdas, models):
    ll = 0.0
    for w in zip(*models):
        ll += math.log(sum(i*j for i,j in zip(lambdas, w)))
    return ll

def update_lambda(idx, lambdas, models):
    new_val = 0.0
    for w in zip(*models):
        numer = lambdas[idx] * w[idx]
        denom = sum(i*j for i,j in zip(lambdas, w))
        new_val += numer / denom
    return new_val / len(models[0])

def em(lambdas, models, iteration):
    new_lambdas = []
    for i in range(len(lambdas)):
        new_lambdas.append(update_lambda(i,lambdas,models))

    ll_old = log_likelihood(lambdas, models) / len(models[0])
    ll_new = log_likelihood(new_lambdas, models) / len(models[0])
    eps = (ll_new - ll_old) / math.fabs(ll_new)

    print 'lambdas     %d: %s' % (iteration, lambdas)
    print 'Average LL  %d: %f' % (iteration, ll_new)
    print 'Ratio       %d: %f\n' % (iteration, eps)

    return (new_lambdas, eps)

def main(argv):
    models = []
    for f in argv:
        models.append([float(x.strip()) for x in open(f)])

    random.seed()
    lambdas = [random.random() for x in argv]
    lambdas = [x / sum(lambdas) for x in lambdas]

    iteration = 1
    print "INIT lambdas: %s\n" % lambdas
    lambdas, eps = em(lambdas, models, iteration)
    while eps > epsilon:
        iteration += 1
        lambdas, eps = em(lambdas, models, iteration)

    print "FINAL: ", lambdas
    assert(sum(lambdas) - 1.0 < .001)

if __name__ == '__main__': main(sys.argv[1:])
