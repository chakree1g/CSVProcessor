====================
Problem Statement
====================

This program reads from the provided CSV file and combines its information with data from the `API`_ and outputs a new CSV file.

.. _API: http://interview.wpengine.io/v1/docs/

-------------------
Details
-------------------
Input  CSV file with the following columns including a header row containing:

+----------+-------------+-----------+-----------+
|Account ID| Account Name| First Name| Created On|
+----------+-------------+-----------+-----------+

and a Restful Status API::

 http://interview.wpengine.io/v1/accounts/{account_id}

that returns information in a JSON format::

{"account_id": 12345, "status": "good", "created_on": "2011-01-12"}

where the "Account ID" in the CSV lines up with the "account_id" in the API and the "created_on" in API represents when the status was set

For every line of data in the CSV, we want to

* Pull the information from the API for the Account ID
* Merge it with the CSV data to output into a new CSV with columns:

+----------+----------+-----------+-------+--------------+
|Account ID|First Name| Created On| Status| Status set On|
+----------+----------+-----------+-------+--------------+

------------------
Installation
------------------
Download wpe_merge-0.1.0.tar.gz with py2.7 or py3.4 environment

pip install wpe_merge-0.1.0.tar.gz

------------------
Usage
------------------
The program must be invoked as follows:: 

 wpe_merge [-v] [-h]  <input_file> <output_file>
 -v --verbose
 -h --help
 For example:
 wpe_merge data/input.csv output.csv
 wpe_merge -v data/input.csv output.csv
 

