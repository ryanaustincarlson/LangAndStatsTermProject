#!/usr/bin/env python

## This is essentially the same as taking `head` of the "all-data" file and setting that 
## as the training set, with the rest as the dev set

import sys

def write_data(data, filename):
  f = open(filename, 'w')
  for d in data:
    f.write('{}\n'.format(d))
  f.close()

def main(args):

  all_data = [line.strip() for line in open(args[0], 'r')]
  output_train = args[1]
  output_dev = args[2]
  dev_percent = float(args[3])

  if dev_percent <= 0 or dev_percent >= 1: raise Exception("dev-percent (%.4f) is not in range (0,1)" % dev_percent)

  cutoff_index = len(all_data) - int( len(all_data) * dev_percent )

  train_data = all_data[:cutoff_index]
  dev_data = all_data[cutoff_index:]

  write_data(train_data, output_train)
  write_data(dev_data, output_dev)


if __name__ == '__main__': 
    if len(args) != 5:
        print 'usage: %s all-data output-train output-dev dev-percent' % args[0]
        print '       dev-percent: percent of all-data that should go into dev set (0,1)'
        sys.exit(1)

    main(sys.argv[1:])
