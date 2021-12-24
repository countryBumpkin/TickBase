from portal_interface import Portal
from briefcase import Document
import requests

'''
    This class provides a way to query the Springer Nature database. Springer is a global publisher @ https://www.springernature.com/gp
    API: https://dev.springernature.com/
'''
class ISpringer(Portal):

    def __init__(self):
        self.api_key = '5efe481dfaa6f39356851521737a4c35'
        self.tag = 'springernature'
        self.result_type = 'mixed'

    # parse the list of creators and put them in a list
    def _get_creators_(self, creator_list):
        str_out = ''
        i = 0

        print('creator list ', creator_list)

        for person in creator_list:
            first_last = person['creator'].split(',')
            name = first_last[1] + ' ' + first_last[0] # rearrange to 'first_name last_name'

            if i == 0:
                str_out = name
            else:
                str_out = str_out + ', ' + name    

            i = i + 1

        return str_out

    def __convert_to_Document__(self, item):
        title = item['title']
        abstract = item['abstract']
        doi = item['doi']
        url_container = item['url']
        url1 = url_container[0]
        url = url1['value']
        authors = self._get_creators_(item['creators'])

        doc = Document(title=title,
                        abstract=abstract,
                        doi=doi,
                        link=url,
                        authors=authors,
                        datatype=item['contentType'])

        return doc

    # override the base implementation and return success by default
    def get_code(self, response):
        return response.status_code

    # get string datatype and requests formatted response in tuple
    def get_content(self, response):
        return ('list', response)

    # search the database for items whose metadata contains the keyword passed to this function
    # content_filter: 'None' means don't remove any results, 'Data' means keep only data, 'Articles' means keep just articles
    def query(self, key='', content_filter='None'):
        baseURL = 'http://api.springernature.com/metadata/json{}'
        num_docs = 100
        i = 0

        # list of document objects from the search
        docs = []

        while num_docs == 100:
            search_string = '?q={}&s={}&p=100&api_key={}'.format(key, i*100, self.api_key)
            r = requests.get(baseURL.format(search_string))

            if r.status_code < 400:
                # parse results and store in list
                r_json = r.json()
                print('RAW DOC\n\t', r_json, '\n\t', type(r_json))
                json_resultsf = r_json['result']
                first_elem = json_resultsf[0]
                num_docs = first_elem['recordsDisplayed']

                # documents returned
                records = r_json['records']

                for item in records:
                    #if content_filter is not 'None' and content_filter != item['contentType']:
                    print('RAW DOC\n\t', item)
                    docs.append(self.__convert_to_Document__(item))

            else:
                print('page not found')
                break
            # increment the number of pages iterated through
            i = i + 1

        return docs
