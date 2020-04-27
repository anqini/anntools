# run.py
#
# Copyright (C) 2011-2019 Vas Vasiliadis
# University of Chicago
#
# Wrapper script for running AnnTools
#
##
__author__ = 'Vas Vasiliadis <vas@uchicago.edu>'

import os
import sys
import time
import driver
import boto3

"""A rudimentary timer for coarse-grained profiling
"""
class Timer(object):
  def __init__(self, verbose=True):
    self.verbose = verbose

  def __enter__(self):
    self.start = time.time()
    return self

  def __exit__(self, *args):
    self.end = time.time()
    self.secs = self.end - self.start
    if self.verbose:
      print(f"Approximate runtime: {self.secs:.2f} seconds")

if __name__ == '__main__':
        # Call the AnnTools pipeline
        if len(sys.argv) > 1:
                with Timer():
                        driver.run(sys.argv[1], 'vcf')
                filename = sys.argv[1].split('/')[-1]
                s3 = boto3.client('s3')
                outputFilename = 'data/' + filename.split('.')[0] + '.annot.vcf'
                s3.upload_file(Bucket = 'gas-results', Filename = '/home/ubuntu/anntools/' + outputFilename, Key = 'angelo23/' + outputFilename.split('/')[1])
                logFilename = 'data/' + filename + '.count.log'
                s3.upload_file(Bucket = 'gas-results', Filename = '/home/ubuntu/anntools/' + logFilename, Key = 'angelo23/' + logFilename.split('/')[1])
                os.system('rm ' + outputFilename)
                os.system('rm ' + logFilename)
        else:
                print("A valid .vcf file must be provided as input to this program.")

### EOF
