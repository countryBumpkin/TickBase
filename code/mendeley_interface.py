'''
    @author Garrett Wells
    @date   12/31/2021
'''

# found here: https://mendeley-python.readthedocs.io/en/latest/usage.html
from portal_interface import Portal
from mendeley import Mendeley
from briefcase import Document
import requests

'''
    An interface for performing queries on the Mendeley data repository.

    Requires client authentication to use. Currently this is configured by Garrett Wells (garrettrwells@gmail.com) but will likely expire in the future.
        To authentication tutorial/info:    https://dev.mendeley.com/reference/topics/authorization_client_credentials.html
        To access Developer Portal:         https://dev.mendeley.com/reference/topics/authorization_overview.html

'''
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
            if doc.identifiers != None and 'doi' in doc.identifiers.keys():
                doi = doc.identifiers['doi']

            print('RAW DOC\n\t', doc)
            print('\tDOC\n\t\t', doc.id, doi)
            auth_list = self._get_authors(doc.authors)
            print('\tAUTHORS:\n\t\t', auth_list)
            file = Document(title=doc.title, source=doc.source, link=doc.link, 
                abstract=doc.abstract, authors=auth_list, datatype=doc.type, 
                date=doc.year, keywords=doc.keywords, doi=doi)
            results.append(file)
            file.print()

        print('len = ', len(results), results)
        if len(results) > 0:
            return results
        else:
            return None

    def _get_authors(self, author_list):
        if author_list is None:
            return None

        authors_list = []

        for persn in author_list:
            if persn is not None:
                print('adding ', persn)
                if persn.last_name is not None and persn.first_name is not None:
                    authors_list.append(persn.last_name + ', ' + persn.first_name)
                else:
                    authors_list.append(persn.last_name)

            else:
                print('person is none')

        return authors_list

    # parse a list of mendeley.common.Person objects to get the associated authors
    def _get_authors_str(self, auth_list):
        #for author in auth_list:
            #print(author.first_name, ' ', author.last_name)
        authors = ''
        i = 0
        if auth_list is None:
            return 'None'

        for person in auth_list:
            if person is not None:
                has_first = False # reset flag
                if i == 0:
                    if person.first_name is not None:
                        has_first = True
                        authors = person.first_name

                    if person.last_name is not None:
                        if has_first:
                            authors = authors + ' ' + person.last_name
                        else:
                            authors = person.last_name

                else:
                    if person.first_name is not None:
                        has_first = True
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
