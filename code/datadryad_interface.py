# https://datadryad.org/api/v2/docs/#/default/get_search

import requests
import pprint
from portal_interface import Portal
from briefcase import Document

'''
    Interface for querying Data Dryad data repository. https://datadryad.org/stash/
'''
class IDataDryad(Portal):

    def __init__(self):
        self.tag = 'data_dryad'
        self.result_type = 'data'

    # parse dictionary of authors and convert to array of author names in "last, first" format
    def _get_authors(self, dict_arr):
        author_list = []

        for author in dict_arr:
            last_first = author['lastName'] + ', ' + author['firstName']
            author_list.append(last_first)

        return author_list

    # converting the author objects to a string of names
    def _get_authors_str(self, dict_arr):
        author_str = ''
        count = 0

        #print('authors before extraction ', dict_arr)

        for author in dict_arr:
            if count == 0:
                author_str = author['firstName'] + ' ' + author['lastName']

            elif count >= 0:
                author_str = author_str + ', ' + author['firstName'] + ' ' + author['lastName']

            print(author)
            count = count + 1

        return author_str

    def query(self, key='', type='dataset'):
        self.base_url = 'https://datadryad.org/api/v2'
        results = []

        for i in range(500):
            r = requests.get(self.base_url + '/search?q={}&page={}&per_page=100'.format(key, i))

            if r.status_code != 200:
                break
            else:
                json_out  = r.json()

                print('RAW DOC\n\t', json_out)

                # make sure there are results on this page
                count = json_out['count']
                if count <= 0:
                    continue

                print('page #{}, count={}'.format(i, count))

                embedded = json_out['_embedded']
                authors = ''

                for item in embedded['stash:datasets']:
                    if 'authors' in item.keys():
                        authors = self._get_authors(item['authors'])
                    else:
                        authors = ''
                    pprint.pprint(item)
                    try:
                        file = Document(title=item['title'],
                                        authors= authors,
                                        link='https://default_link',
                                        abstract=item['abstract'],
                                        source='',
                                        doi=item['identifier'],
                                        date=item['publicationDate'],
                                        datatype=type)

                        results.append(file)
                    except:
                        print('ERROR adding doc failed')

        return results

    def get_content(self, response):
        return ('list', response)
