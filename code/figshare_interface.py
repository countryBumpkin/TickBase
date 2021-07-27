# documentation found here: https://docs.figshare.com/#figshare_documentation_api_description

# Consumer ID: 6d4f04a795126fca09133493ede5563c33c957e3
# Consumer Secret: d4a3f0d1e710b1636d5ee171ed33ec4705bfbe8cea15b952e8b5134f6f57384e4238d9762b55a711a895e6037ed46f2066844f7714c723b39ce57977b4c1958e
from portal_interface import Portal
from briefcase import Document
import requests
import json
import pprint

'''
    This class provides interface for running queries on the figshare data repository
'''
class IFigshare(Portal):

    def __init__(self):
        # authorization credentials, found on developer page
        self.client_id = '6d4f04a795126fca09133493ede5563c33c957e3'
        self.client_secret = 'd4a3f0d1e710b1636d5ee171ed33ec4705bfbe8cea15b952e8b5134f6f57384e4238d9762b55a711a895e6037ed46f2066844f7714c723b39ce57977b4c1958e'

        # identification information
        self.tag = 'figshare'
        self.result_type = 'data'

    # override the base implementation and return success by default
    def get_code(self, r):
        return r.status_code

    # use the Mendeley API to get the paginated results of a search
    # returns a list of all data objects parsed as Documents
    def query(self, key, type='dataset'):
        base_url = 'https://api.figshare.com/v2/'
        results = []

        # iterate over 500 pages of results
        for i in range(500):
            print('page #{}'.format(i), base_url + 'articles?search={}&itemType={}&page={}'.format(key, type, i))
            r = requests.get(base_url + 'articles?search={}&itemType={}&page={}'.format(key, type, i))

            # verify success of request
            if r.status_code is not 200:
                print('ERROR: status code failure')
                continue

            # get output as json but make sure we actually get something back
            json_out = r.json()
            if json_out is None or len(json_out) == 0:
                break
            else:
                print('JSON \n\t')
                pprint.pprint(json_out)

                # iterate over the results on the current page and store them in a list of documents
                for item in json_out:
                    file = Document(title=item['title'],
                                    source='figshare',
                                    link=item['url'],
                                    doi=item['doi'],
                                    datatype=item['defined_type_name'])

                    results.append(file)

        return results

    # get all the results from a query and what file format they come in
    def get_content(self, response):
        return ('list', response)
