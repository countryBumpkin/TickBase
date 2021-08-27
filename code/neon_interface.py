import json
import pandas as pd
import requests
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

    # use python string parsing to check important elements of the dict contain the keyword
    def __contains__(self, dict_item, key):
        contains_key = False
        keys = dict_item.keys()
        print('dict keys list =', keys)

        # iterate through all keys in dictionary and check if associated string contains relevant data
        for dict_key in keys:
            print('dict key =', dict_key)
            # check if data type is iterable
            if hasattr(dict_item[dict_key], '__iter__') and dict_item[dict_key] is not None:
                if key in dict_item[dict_key]:
                    print('found match')
                    return True
                else:
                    print('empty')
            elif type(dict_item[dict_key]) is not bool and dict_item[dict_key] is not None and key in dict_item[dict_key]:
                print('found match')
                return True
            else:
                print('completely empty')

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
            print('RAW JSON\n\t', result)

            # iterate through results and check for our key word in each field
            for item in result['data']:
                if self.__contains__(item, key):
                    # save the metadata for later reference
                    print('RAW DOC\n\t', item)
                    print('item contains key')

                    doc = Document(title=item['productName'],
                                    link=item['productCode'],
                                    abstract=item['productAbstract'],
                                    source=item['productScienceTeam'],
                                    keywords=item['keywords'],
                                    doi=item['productCodeLong'],
                                    datatype=item['productPublicationFormatType'])

                    docs.append(doc)

                else:
                    print("item doesn't contain key")

            return docs

        else:
            print('ERROR, bad query, status code =', r.status_code)
            return None
