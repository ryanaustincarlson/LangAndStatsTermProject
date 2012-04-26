#!/usr/bin/env python

import random, math, sys

def read_probs_file(fname):
  return [float(line.strip()) for line in open(fname, 'r')]

def randomly_generate_weights(num_weights):
  weights = []
  for i in xrange(num_weights):
    while True:
      rand = random.uniform(0,1)
      if rand > 0 and rand < 1:
        break

    weights.append(rand)

  weights_sum = math.fsum(weights)

  for i in xrange(len(weights)):
    weights[i] /= weights_sum

  return weights

def run_algorithm_until_convergence(probability_models, initial_weights, convergence_num):

  num_types = len(probability_models[0])

  # translate all numbers into equation notation so its easier to check
  # that the equation is right
  N = num_types
  K = len(initial_weights)
  P = probability_models

  def update(weights):
    l = weights # l := lambda

    new_weights = []
    for j in xrange(K):

      N_sum = 0
      for i in xrange(N):
        numerator = l[j] * P[j][i]

        denominator = 0
        for k in xrange(K):
          denominator += l[k] * P[k][i]
          #print l[k], P[k][i]
        N_sum += (float(numerator) / denominator)
      new_weights.append( 1.0 / N * N_sum )

    return new_weights
  
  def check_convergence(old_weights, new_weights):
    def log_likelihood(weights):
      l = weights # l := lambda
      N_sum = 0

      for i in xrange(N):
        K_sum = 0
        for k in xrange(K):
          K_sum += l[k] * P[k][i]

        N_sum += math.log(K_sum)
      return float(N_sum) / N
    
    old_likelihood = log_likelihood(old_weights)
    new_likelihood = log_likelihood(new_weights)

    percent_change = float(new_likelihood - old_likelihood) / math.fabs(new_likelihood)

    return (
        percent_change <= convergence_num, 
        new_likelihood, 
        float(new_likelihood) / old_likelihood
        )

  weights = initial_weights
  print "Initial Weights:", [round(weight, 6) for weight in weights], '\n'
  iteration = 1
  while True:
    new_weights = update(weights)
    print "Iteration %d" % iteration
    print "\tWeights:", [round(weight, 6) for weight in new_weights]

    convergence_stats = check_convergence(weights, new_weights)
    has_converged = convergence_stats[0]
    average_likelihood = convergence_stats[1]
    ratio = convergence_stats[2]

    print "\tAverage Log-Likelihood:", average_likelihood
    print "\tLog-Likelihood Ratio:", ratio

    if has_converged: break
    weights = new_weights
    iteration += 1
    print

  return new_weights

def count_zeros(probabilities):
  print 'zero counts:', [sum((1 for prob in prob_model if prob == 0)) for prob_model in probabilities]

def interpolate(args):
  fnames = args

  directory = ''
  if '/' in fnames[0]:
    directory = fnames[0][:fnames[0].rfind('/')+1]

  models_file = open(directory + 'model-order.txt', 'w')
  for fname in fnames: models_file.write(fname + '\n')
  models_file.close()
  print 'Model order written to {}'.format(models_file.name)

  probabilities = [read_probs_file(fname) for fname in fnames]

  #probabilities = [probabilities[0], probabilities[1], probabilities[0]]

  #uniform_model = [1.0/4000]*len(probabilities[0])
  #probabilities.append(uniform_model)

  #count_zeros(probabilities)

  weights = randomly_generate_weights(len(probabilities))
  convergence_num = 0.0001

  weights = run_algorithm_until_convergence(probabilities, weights, convergence_num)

  weights_file = open(directory + 'weights.txt', 'w')
  for weight in weights: weights_file.write('{}\n'.format(weight))
  weights_file.close()
  print 'Weights written to {}'.format(weights_file.name)

  return weights

def main(args):

    weights = interpolate(args)



if __name__ == '__main__':
  if len(sys.argv) == 1:
      print 'usage: %s <prob-files>' % sys.argv[0]
      print '       prob-files contain lists of probabilities generated from the same dev set (and end in .prob)'
      sys.exit(1)

  main(sys.argv[1:])

