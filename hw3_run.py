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
from botocore.exceptions import ClientError

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
                # hard code username
                username = 'userX'
                outputFilename = 'data/' + filename.split('.')[0] + '.annot.vcf'
                try: # handle s3 exception
                    s3.upload_file(Bucket = 'gas-results', Filename = '/home/ubuntu/anntools/' + outputFilename, Key = 'angelo23/' + username + '/' + outputFilename.split('/')[1])
                except ClientError:
                    print('Upload Output File Error.')
                logFilename = 'data/' + filename + '.count.log'
                try: # handle s3 exception
                    s3.upload_file(Bucket = 'gas-results', Filename = '/home/ubuntu/anntools/' + logFilename, Key = 'angelo23/' + username + '/'+ logFilename.split('/')[1])
                except ClientError:
                    print('Upload Log File Error.')
                os.system('rm /home/ubuntu/anntools/' + outputFilename)
                os.system('rm /home/ubuntu/anntools/' + logFilename)
                os.system('rm ' + sys.argv[1])
        else:
                print("A valid .vcf file must be provided as input to this program.")

### EOF
