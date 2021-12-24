from Bio import Entrez
from portal_interface import Portal
from briefcase import Document
import requests
import json
from time import sleep

'''
    This class retrieves data from the Pub Med repository.
'''
class IPubMed(Portal):

    def __init__(self):
        self.tag = 'pubmed'
        self.result_type = 'mixed'

    # override the base implementation and return success by default
    def get_code(self, response):
        return response.status_code

    def _get_authors(self, author_list):
        authors = ''
        i = 0
        for author in author_list:
            if i == 0:
                authors = author
            else:
                authors = authors + ', ' + author
            i = i + 1

        return authors

    # use the Mendeley API to get the paginated results of a search
    # returns a list of all data objects parsed as Documents
    def query(self, key, type='TABULAR_DATA'):
            #sleep(180)
            Entrez.email = "A.N.Other@example.com"  # Always tell NCBI who you are
            handle = Entrez.esearch(db="pubmed", term=key)
            record_XML = Entrez.read(handle)

            # Documents list
            results = []
            key_list = ['Id', 'Title', 'Source', 'AuthorList', 'DOI']

            for id in record_XML['IdList']:
                handle = Entrez.esummary(db="pubmed", id=id)
                record = Entrez.read(handle)
                print('RAW DOC\n\t',record[0])

                #print('DOCUMENT \nTitle: {}'.format(record[0][key_list[1]]))

                # data
                infoDict = {}
                for key in key_list:
                    try:
                        infoDict[key] = record[0][key]
                        #print('keyval record=', record[0][key])
                        #print(infoDict[key], 'vs', record[0][key])
                    except:
                        print('error getting', key, 'from', id)
                        infoDict[key] = ''

                print("\tDOCUMENT\n\t\tid: {}\n\t\tTitle: {}\n\t\tSource: {}\n\t\tAuthors: {}\n\t\tDOI: {}".format(infoDict['Id'],
                                                                                                                    infoDict['Title'],
                                                                                                                    infoDict['Source'],
                                                                                                                    infoDict['AuthorList'],
                                                                                                                    infoDict['DOI']))

                epubd = ''
                if 'EPubDate' in key_list:
                    epubd = infoDict['EPubDate']
                elif 'PubDate' in key_list:
                    epubd = infoDict['PubDate']                                                                                                    

                # put in document
                doc = Document(title=infoDict['Title'], authors=self._get_authors(infoDict['AuthorList']), 
                                source=infoDict['Source'], date=epubd, 
                                doi=infoDict['DOI'], datatype='unkown')
                results.append(doc)

            return results

    # return tuple with data type and response from this object
    def get_content(self, response):
        return ('list', response)
