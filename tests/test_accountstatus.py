import pandas.testing as ptest
import pandas as pd
import requests
import unittest
from unittest.mock import patch
import logging
from csvprocessor.accountstatus import AccountStatus
class TestAccountStatus(unittest.TestCase):
  '''
  Test account status 
  '''
  def setUp(self):
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
    self.logger = logging.getLogger(__name__)

  def test_get_account_status_valid(self):
   '''
   Test that account status is returned for the right account id
   '''
   accs = AccountStatus(self.logger)
   accs_ps = pd.Series({'Account ID':12345, 'Status':'good', 'Status Set On':'2011-01-12'})
   ptest.assert_series_equal(accs.get_account_status({'Account ID':12345}), accs_ps)

  def test_get_account_status_invalid(self):
   '''
   Test that account status is returned for the invalid account id
   '''
   accs = AccountStatus(self.logger)
   accs_ps = pd.Series({'Account ID':1, 'Status':'not found', 'Status Set On':None})
   ptest.assert_series_equal(accs.get_account_status({'Account ID':1}), accs_ps)
  
  def test_get_account_status_bad_obj(self):
   '''
   Test that account status is returned for the bad account object
   '''
   accs = AccountStatus(self.logger)
   accs_ps = pd.Series({'Account ID':None, 'Status':'unknown', 'Status Set On':None})
   ptest.assert_series_equal(accs.get_account_status({}), accs_ps)

  @patch('requests.get')
  def test_get_account_status_api_errors(self,api_get):
   '''
   Test that account status is returned for API errors
   '''
   api_resp = unittest.mock.Mock()
   
   '''
   TC 4.1: Test for connection error exception
   '''
   api_resp.side_effect = requests.exceptions.ConnectionError()
   api_get.return_val = api_resp
   accs = AccountStatus(self.logger)
   accs_ps = pd.Series({'Account ID':12345, 'Status':'unknown', 'Status Set On':None})
   ptest.assert_series_equal(accs.get_account_status({'Account ID':12345}), accs_ps)
   
   '''
   TC 4.2: Test for connection timeout exception
   '''
   api_resp.side_effect = requests.exceptions.Timeout()
   api_get.return_val = api_resp
   accs = AccountStatus(self.logger)
   accs_ps = pd.Series({'Account ID':12345, 'Status':'unknown', 'Status Set On':None})
   ptest.assert_series_equal(accs.get_account_status({'Account ID':12345}), accs_ps)
   
   '''
   TC 4.3: Test for general request exception
   '''
   api_resp.side_effect = requests.exceptions.RequestException()
   api_get.return_val = api_resp
   accs = AccountStatus(self.logger)
   accs_ps = pd.Series({'Account ID':12345, 'Status':'unknown', 'Status Set On':None})
   ptest.assert_series_equal(accs.get_account_status({'Account ID':12345}), accs_ps)
     
if __name__ == '__main__':
    unittest.main()
