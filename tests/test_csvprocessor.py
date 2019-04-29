import unittest
from unittest.mock import patch
import logging
from path import Path
from csvprocessor.csvprocessor import process_csvdata
class TestCSVProcessor(unittest.TestCase):
  '''
  Test CVS Processor: A simple scenario is covered.
  More complex scenarios such as the ones enumerated below, can be
  done by exploratory data analysis with more samples of data.
      1 — Unrecognized Unicode - use latin-1
      2 — Text field with an unescaped delimiter
      3 — Quoted string with an unescaped double quote
      4 — Non-standard escape characters
      5 — CRLF / Dos line endings

  '''
  def setUp(self):
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
    self.logger = logging.getLogger(__name__)
 
  @patch('pandas.read_csv')
  def test_process_csvdata(self, rd):
      '''
      Basic test case to check if file exists on an exception(bad csv file)
      '''
      infile = 'test_infile'
      outfile = 'test_outfile'
      Path(infile).touch()
      rd.side_effect = Exception('Unknown')
      process_csvdata(infile, outfile, self.logger)
      self.assertFalse(Path(outfile).isfile())