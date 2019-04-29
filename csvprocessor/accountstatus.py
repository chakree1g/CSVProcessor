import requests
import pandas as pd
import os
class AccountStatus:
  '''
  This Class will get the status of user accounts using the WP-Engine API.
  To use this implementation BASE_URL environment variable should be set. It defaults to /v1/accounts.
  '''
  def __init__(self, logger):
    '''
    Params
    :param logging.logger logger: logger handle for logging

    Description
    Inits AccountStatus object
    '''
    self.req_url = os.environ.get('BASE_URL', 'http://interview.wpengine.io/v1/accounts')
    self.status = 'unknown'
    self.status_so = None
    self.acc_num = None
    self.logger = logger
    self.logger.debug("Initialising new Acc Obj")
  
  def __call__(self, acc_obj):
    '''
    Description
    This method makes the object 'callable'
    '''
    return self.get_account_status(acc_obj)
    
  def get_account_status(self, acc_obj):
    '''
    Description
    This method is call back, primarily applied per dataframe.
    It requests Account status and creates and returns a  'row' as pandas.Series obj

    Params
    :param dict acc_obj: account ID dict
    :return: Account stats (Account ID','Status','Status Set On')
    :rtype: pandas.Series
    '''
    try:
     self.acc_num = acc_obj['Account ID']
     self.logger.debug("Account ID: %s", self.acc_num)
    except KeyError:
      self.logger.exception("Generating Null record:Account ID cannot be retrieved")
      rps = pd.Series({'Account ID': self.acc_num, 'Status':self.status, 'Status Set On':self.status_so})
      return rps
    try:
      self.logger.info("Requesting account status from  %s", self.req_url+'/{}'.format(self.acc_num))
      res = requests.get(self.req_url+'/{}'.format(self.acc_num))
    except requests.exceptions.ConnectionError as c_err:
      self.logger.exception("Generating Null record:Connection Error %s", self.req_url+'/{}'.format(self.acc_num), c_err)
    except requests.exceptions.Timeout as t_err:
      self.logger.exception("Generating Null record:Connection Timeout %s", self.req_url+'/{}'.format(self.acc_num), t_err)
    except requests.exceptions.RequestException as d_err:
      self.logger.exception("Generating Null record:Request failure %s", self.req_url+'/{}'.format(self.acc_num), d_err)
    if res.status_code == 200:
      resd = res.json()
      self.status = resd['status']
      self.status_so = resd['created_on']
      self.logger.info("Generating Valid record for Account ID: %s", self.acc_num)
    elif res.status_code == 404:
      self.logger.error("Generating Null record:Account ID %s Not Found", self.acc_num)
      self.status = 'not found'
    else:
      self.logger.error("Generating Null record:Account ID %s unknown error %s", self.acc_num, res.status_code)
    rps = pd.Series({'Account ID': self.acc_num, 'Status':self.status, 'Status Set On':self.status_so})
    return rps
