# found here: https://mendeley-python.readthedocs.io/en/latest/usage.html
from portal_interface import Portal
from mendeley import Mendeley
from briefcase import Document
import requests

class IMendeley(Portal):

    def __init__(self):
        # authorization credentials, found on developer page
        self.client_id = 10195
        self.client_secret = 'O3Em123707vg3BdX'

        self.__authorize__()

        # identification information
        self.tag = 'mendeley'
        self.result_type = 'article'

    # use Mendeley library to create a new session that can be used to access the Mendeley API
    def __authorize__(self):
        mend = Mendeley(client_id=self.client_id, client_secret=self.client_secret)
        auth = mend.start_client_credentials_flow()
        self.session = auth.authenticate()
        return self.session

    # return the identification tag that lists what data portal this interface supports
    def get_tag(self):
        return self.tag

    # return the tag that denotes what type of result should be expected
    def get_resultType(self):
        return self.result_type

    # override the base implementation and return success by default
    def get_code(self):
        return 200

    # use the Mendeley API to get the paginated results of a search
    # returns a list of all data objects parsed as Documents
    def query(self, key):
        catalog_search = self.session.catalog.search(key)
        # Document list
        results = []

        for doc in catalog_search.iter():
            doi = ''
            if 'doi' in doc.identifiers.keys():
                doi = doc.identifiers['doi']

            print('RAW DOC\n\t', doc)
            print('DOC\n\t', doc.id, doi)
            auth_list = self._get_authors(doc.authors)
            print('AUTHORS:\n\t', auth_list)
            file = Document(title=doc.title, source=doc.source, link=doc.link, 
                abstract=doc.abstract, authors=auth_list, datatype=doc.type, 
                date=doc.year, keywords=doc.keywords, doi=doi)
            results.append(file)
            file.print()

        print('len = ', len(results), results)
        return results

    # parse a list of mendeley.common.Person objects to get the associated authors
    def _get_authors(self, auth_list):
        #print(type(auth_list), auth_list)
        #print(type(auth_list[0]), type(auth_list[0].first_name))
        authors = ''
        i = 0

        if auth_list is None:
            return 'None'

        for person in auth_list:
            if person is not None:
                has_first = False
                if i == 0:
                    if person.first_name is not None:
                        has_first = True
                        authors = person.first_name

                    if person.last_name is not None:
                        if has_first:
                            authors = authors + ' ' + person.last_name
                        else:
                            authors = person.last_name

                elif i < len(auth_list):
                    if person.first_name is not None:
                        authors = authors + ', ' + person.first_name

                    if person.last_name is not None:
                        if has_first:
                            authors = authors + ' ' + person.last_name
                        else:
                            authors = authors + ', ' + person.last_name
            i = i + 1

        if authors == '':
            return 'None'
        else:
            return authors

    def get_content(self, response):
        return ('list', response)
