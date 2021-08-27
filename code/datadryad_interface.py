# https://datadryad.org/api/v2/docs/#/default/get_search

import requests
import pprint
from portal_interface import Portal
from briefcase import Document

class IDataDryad(Portal):

    def __init__(self):
        self.tag = 'data_dryad'
        self.result_type = 'data'

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

                for item in embedded['stash:datasets']:
                    pprint.pprint(item)
                    try:
                        file = Document(title=item['title'],
                                        authors=item['authors'],
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
