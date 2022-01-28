'''
    @author Garrett Wells
    @date   12/31/2021
'''

import json
import pandas as pd
import requests
# Levenshtein partial string matching
from fuzzywuzzy import fuzz
from portal_interface import Portal
from briefcase import Document

'''
    Interface for querying the Neon API

    Neon organizes data in releases which contain up-to-date data. This class then checks results for keywords and returns any matches in a list of
    Document objects.
'''
class INeon(Portal):

    def __init__(self):
        self.tag = 'neon'
        self.result_type = 'data'

    # use python string parsing to check if important elements of the dict contain the keyword
    def __contains__(self, dict_item, key):
        keys = dict_item.keys()
        print('dict keys list =', keys)

        # iterate through all key-value pairs in dictionary and check for keyword
        for dict_key in keys:
            match_ratio = 0
            if isinstance(dict_item[dict_key], str):
                match_ratio = fuzz.partial_ratio(key, dict_item[dict_key])

            print('\n\tmatch_ratio:', match_ratio)

            # check iterable types for the key
            if match_ratio >= 85:
                print('ITEM CONTAINS KEY: \'', key, '\'', '\n\t', dict_item[dict_key])
                return True

            else:
                print(type(dict_item[dict_key]), 'DOESN\'T CONTAIN KEY:\n\t', key, '\n\t', dict_item[dict_key])

        return False

    # override the base implementation and return error code from response
    def get_code(self, response):
        return response.status_code

    def get_content(self, response):
        return ('list', response)

    # given a keyword, searches the Neon database for related data and retrieves relevant metadata
    def query(self, key):
        path = 'https://data.neonscience.org/api/v0/products'
        # download all data in current release as a list of json objects
        r = requests.get(path)

        # list to store matching metadata
        docs = []

        # check for http error codes
        if r.status_code < 400:
            result = r.json()
            print('RAW JSON\n\t', result.keys(), '\n\t', result)

            # iterate through results and check for our keyword in each returned result
            for item in result['data']:
                # ensure NEON result contains search keyword
                if self.__contains__(item, key):
                    # save the metadata for later reference
                    print('RAW DOC\n\t', item)

                    doc = Document(title=item['productName'],
                                    link=item['productCode'],
                                    abstract=item['productAbstract'],
                                    source=item['productScienceTeam'],
                                    keywords=item['keywords'],
                                    doi=item['productCodeLong'],
                                    datatype=item['productPublicationFormatType'])

                    docs.append(doc)

                else:
                    print("MISSING SEARCH KEY: \'", key, '\'')

            return docs

        else:
            print('ERROR, bad query, status code =', r.status_code)
            return None
