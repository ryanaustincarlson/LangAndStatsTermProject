#!/usr/bin/env python

import sys, logging

# models
from Unigram import Unigram
from Bigram import Bigram 
from Trigram import Trigram

OUTPUT_DIR_DEFAULT = 'output'

# turn logging on or off
LOGGING_LEVEL = logging.DEBUG; #LOGGING_LEVEL = None

# want the format of output to be
#   output_dir/dev_filename-model_name.probs
def get_output_filename(output_dir, dev_filename, model_name):
  file_ext_index = dev_filename.rfind('.'); directory_index = dev_filename.rfind('/')
  if file_ext_index > 0: dev_filename = dev_filename[:file_ext_index]
  if directory_index > 0: dev_filename = dev_filename[directory_index+1:]
  if not output_dir.endswith('/'): output_dir += '/'

  return output_dir + dev_filename + '-' + model_name + '.probs'

def main(args):
  logging.basicConfig(level=LOGGING_LEVEL, format="DEBUG: %(message)s")

  if len(args) < 3 or len(args) > 4:
    print 'usage: %s training-file dev-file [output-dir]' % args[0]
    print '       output-dir is optional, default is "%s"' % OUTPUT_DIR_DEFAULT
    sys.exit(1)

  training_filename = args[1]
  dev_filename = args[2]
  output_dir = args[3] if len(args) == 4 else OUTPUT_DIR_DEFAULT

  logging.debug('Training models...')

  # train all the models!
  unigram_model = Unigram(training_filename)
  logging.debug('Done training unigram model')
  bigram_model = Bigram(training_filename)
  logging.debug('Done training bigram model')
  trigram_model = Trigram(training_filename)
  logging.debug('Done training trigram model')

  dev_words = [line.strip() for line in open(dev_filename, 'r')]

  # write predictions out to disk
  unigram_model.write_probability_list(dev_words, get_output_filename(output_dir, dev_filename, 'unigram'))
  logging.debug('Wrote dev set predictions using unigram model')
  bigram_model.write_probability_list(dev_words, get_output_filename(output_dir, dev_filename, 'bigram'))
  logging.debug('Wrote dev set predictions using bigram model')
  trigram_model.write_probability_list(dev_words, get_output_filename(output_dir, dev_filename, 'trigram'))
  logging.debug('Wrote dev set predictions using trigram model')

if __name__ == '__main__': main(sys.argv)
