import d1_client
from briefcase import Document
import requests
from portal_interface import Portal
import xml.etree.ElementTree as ET
#print(dir(d1_client.util))
'''
c = d1_client.solr_client.SolrConnection()

search_result = c.search({
  'q': 'id:[* TO *]', # Filter for search
  'rows': 10, # Number of results to return
  'fl': 'formatId', # List of fields to return for each result
})

pprint.pprint(search_result)
'''
class ILTER(Portal):

    def __init__(self):
        self.tag = 'LTER'
        self.result_type = 'mixed'

    def get_code(self, response):
        return response.status_code

    def get_content(self, response):
        return ('list', response)

    def query(self, key):
        self.base_url = 'https://pasta.lternet.edu/package/search/eml?{}'
        query_str = 'q=' + key + '&fl=title,author,doi,abstract,resources'

        r = requests.get(self.base_url.format(query_str))

        if r.status_code == 200:
            # parse xml
            docs = []

            root = ET.fromstring(r.text)
            print('\tXML:\n\t\t', r.text)
            print('\t\tattributes:', root.attrib)

            # iterate over each document returned by LTER
            for child in root:
                print('\t\tTAG:', child.tag)
                print(child)

                resDict = {}

                for grandchild in child:
                    print('\t\tgrandchild tag =', grandchild.tag, ' text =', grandchild.text)
                    resDict[grandchild.tag] = grandchild.text

                doc = Document(title=resDict['title'], authors=resDict['authors'], abstract=resDict['abstract'], doi=resDict['doi'], datatype='unkown')
                docs.append(doc)

            return docs

        else:
            return []
