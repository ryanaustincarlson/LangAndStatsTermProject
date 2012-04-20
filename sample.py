#!/usr/bin/env python

## This is essentially the same as taking `head` of the "all-data" file and setting that 
## as the training set, with the rest as the dev set

import sys

def write_data(data, filename):
  f = open(filename, 'w')
  for d in data:
    f.write('{}\n'.format(d))
  f.close()

def main():
  if len(sys.argv) != 5:
    print 'usage: %s all-data output-train output-dev dev-percent' % sys.argv[0]
    print '       dev-percent: percent of all-data that should go into dev set (0,1)'
    sys.exit(1)

  all_data = [line.strip() for line in open(sys.argv[1], 'r')]
  output_train = sys.argv[2]
  output_dev = sys.argv[3]
  dev_percent = float(sys.argv[4])

  if dev_percent <= 0 or dev_percent >= 1: raise Exception("dev-percent (%.4f) is not in range (0,1)" % dev_percent)

  cutoff_index = len(all_data) - int( len(all_data) * dev_percent )

  train_data = all_data[:cutoff_index]
  dev_data = all_data[cutoff_index:]

  write_data(train_data, output_train)
  write_data(dev_data, output_dev)


if __name__ == '__main__': main()
