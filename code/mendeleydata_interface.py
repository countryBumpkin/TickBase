# documentation found here: https://datasearch.elsevier.com/api/docs#/search/search
from portal_interface import Portal
from mendeley import Mendeley
from briefcase import Document
import requests
import json

'''
    Interface for getting data from the mendeley/elsevier data repository
    Currently set to filter all data and retain only data based repositories
    API: https://dev.elsevier.com/
'''
class IMendeley_Data(Portal):

    def __init__(self):
        # authorization credentials, found on developer page
        self.client_id = 10195
        self.client_secret = 'O3Em123707vg3BdX'

        self.__authorize__()

        # identification information
        self.tag = 'mendeleydata'
        self.result_type = 'data'

    # use Mendeley library to create a new session that can be used to access the Mendeley API
    def __authorize__(self):
        mend = Mendeley(client_id=self.client_id, client_secret=self.client_secret)
        auth = mend.start_client_credentials_flow()
        self.session = auth.authenticate()
        return self.session

    # override the base implementation and return success by default
    def get_code(self):
        return 200

    # use the Mendeley API to get the paginated results of a search
    # returns a list of all data objects parsed as Documents
    def query(self, key, type='TABULAR_DATA'):
        response_list = []
        for i in range(5):
            print('page #', i, 'https://api.datasearch.elsevier.com/api/v2/search?query=+{}&page={}&type={}&repositoryType=NON_ARTICLE_BASED_REPOSITORY'.format(key, i, type))
            r = requests.get('https://api.datasearch.elsevier.com/api/v2/search?query=+{}&page={}&type={}&repositoryType=NON_ARTICLE_BASED_REPOSITORY'.format(key, i, type))

            r_json = None

            # convert json to dict
            try:
                r_json = r.json()
                print('\n\t\t', r_json)
            except:
                #print('decode error')
                break

            # make sure there are some results to parse
            if r_json['count'] == 0 or len(r_json['results']) == 0:
                #print('\nNO RESULTS\n')
                break
            else:
                # get each search result from file
                for item in r_json['results']:
                    response_list.append(item)

        results = []

        # check that result is good
        if r.status_code == 200:
            for item in response_list:
                #print(item['containerTitle'])
                #print('\t', item)
                # convert to Document list
                keys = item.keys()
                doi = ''
                authors = ''

                if 'doi' in keys:
                    doi = item['doi']

                if 'authors' in keys:
                    authors = self._get_authors(item['authors'])
                    print('AUTHORS:\n\t', authors)

                file = Document(title=item['containerTitle'],
                                source=item['source'],
                                link=item['containerURI'],
                                authors=authors,
                                doi=doi,
                                datatype=item['containerDataTypes'])

                results.append(file)

        else:
            try:
                print('ERROR:', results.status_code)
            except:
                print('ERROR: can\'t get status code')

        return results

    def get_content(self, response):
        return ('list', response)

    # parse a list of mendeley.common.Person objects to get the associated authors
    def _get_authors(self, auth_list):
        #print(type(auth_list), auth_list)
        #auth_list = auth_list[0]
        #print(type(auth_list), type(auth_list.first_name))
        authors = ''
        i = 0

        if auth_list is None:
            return 'None'

        for person in auth_list:
            print('PERSON:\n\t', person)
            if person is not None:
                has_first = False
                if i == 0:
                    if 'firstName' in person.keys():
                        has_first = True
                        authors = person['firstName']

                    if 'lastName' in person.keys():
                        if has_first:
                            authors = authors + ' ' + person['lastName']
                        else:
                            authors = person['lastName']

                elif i < len(auth_list):
                    if 'firstName' in person.keys():
                        authors = authors + ', ' + person['firstName']

                    if 'lastName' in person.keys():
                        if has_first:
                            authors = authors + ' ' + person['lastName']
                        else:
                            authors = authors + ', ' + person['lastName']
            i = i + 1

        if authors == '':
            return 'None'
        else:
            return authors
