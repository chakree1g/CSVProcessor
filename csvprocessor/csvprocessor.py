import pandas as pd
import os.path
from .accountstatus import AccountStatus
import logging
from argparse import ArgumentParser
def get_args():
  '''
  Description
  This function parses cmdline args for our  simple application

  Params
  :return: parsed argument list
  :rtype:  argparse.Namespace
  '''
  parser = ArgumentParser()
  parser.add_argument('infile', help='Input CSV file', type=str)
  parser.add_argument('outfile', help='Output CSV file', type=str)
  parser.add_argument('-v','--verbose', help='verbose logging', action='store_true')
  args = parser.parse_args()
  return args

def process_dataframe(df, logger):
  '''
  Description
  This function processing a dataframe by, 
  (a) getting account status for each account, 
  (b) Merge the status with original dataframe and
  (c) returns a new set of fields per the requirement

  Params
  :param pandas.DataFrame df: input dataframe
  :param logging.logger logger: logger object using in logging.
  :return: merged dataframe
  :rtype: pandas.DataFrame
  '''
  udf =  df[['Account ID']].apply(AccountStatus(logger), axis=1)
  logger.debug("Merging Account status with input data...")
  rdf = pd.merge(df, udf, how='left', left_on=['Account ID'], right_on=['Account ID'])
  return rdf[['Account ID', 'First Name', 'Created On', 'Status', 'Status Set On']]


def process_csvdata(infile, outfile, logger):
  '''
  Description
  This functing processcsv input file and writes out process data to file.
  One Enhancement for the future is to  break down input CSV into'chunks'
  and process them in a batches.

  Params
  :param str infile: Input CSV file
  :param str outfile: Output CSV file
  :param logging.logger logger: logger object using in logging.
  '''
  try:
    df = pd.read_csv(infile, encoding='latin-1', parse_dates=['Created On'])
  except Exception as e:
    logger.exception("Exception: %s while processing CSV File %s...", e, infile)
    return
  logger.debug("Reading CSVFile %s done...", infile)
  odf = process_dataframe(df, logger)
  logger.debug("Processing data completed...")
  odf.to_csv(outfile, encoding='latin-1', index=False)
  logger.debug("Writing to CSV File %s done.", outfile)

def main():
  '''
  Description
  This is the main driver, parses args sets up logging
  and finally processes CSV data
  '''
  args = get_args()
  log_level = logging.ERROR
  if args.verbose:
    log_level = logging.INFO
  logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=log_level)
  logger = logging.getLogger(__name__)
  logger.info("Starting to process CSVFile %s", args.infile)
  if os.path.isfile(args.infile):
    process_csvdata(args.infile, args.outfile, logger)
  else:
    logger.error("CSVFile %s does NOT exist", args.infile)
