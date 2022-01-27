"""
    DSpace API 2.0

    Compatible with DSpace 7.x backend.

    @author:    Garrett Wells
    @date:      12/31/21
"""

import os
import csv
import json
import requests
import warnings
from bs4 import BeautifulSoup
from doiresolver import DOIResolver
from briefcase import Briefcase
from briefcase import Document

# Class provides API for DuraSpace development
class DSpace:

    # DSpace 7.x as of 12/20/21
    _nkn_base_url = 'https://data.tickbase.net/server/api/'
    _csrf_tkn = ''      # token received in cookie from server with each request to verify source of requests, changes periodically
    _bearer_tkn = ''    # JWT authentication token, received on successful authentication
    _r_session = requests.Session() # create persistent storage for cookies and headers

    def __init__(self, username='', passwd='', base_url='', csrf_token=''):
        self.username = username
        self.passwd = passwd

        # default value of session id, shows not logged in if ''
        # may be able to use system without logging in but getting session status will not
        # be available
        self._brearer_tkn = ''

        if base_url == '':
            self.base_url = self._nkn_base_url
        else:
            self.base_url = base_url

    # Parse all items from the container and return as a list of UUIDs
    def _parse_objects_for_items(self, item_containers):
        item_uuids = []
        # iterate and retrieve all item UUIDs
        for i in item_containers:
            item = (i["_embedded"])['indexableObject']
            #print('DSPACE ', item['uuid'])
            item_uuids.append(item['uuid'])

        return item_uuids

    # Take in list of authors formatted as "last, first" and convert to list of dictionary objects
    # that can be imported to dspace.
    def _authors_to_dspace_object(self, author_str_list):
        if author_str_list == None:
            return []

        author_list = [] # list of dspace dictionaries
        for i in author_str_list:
            author = {
                        "value": i,
                        "language": None,
                        "authority": None,
                        "confidence": -1,
                        "place": 0  
                    }
            # add author to output list
            author_list.append(author)

        return author_list

    # Check if REST API is installed
    def api_running(self):
        r = requests.get(self.base_url+'/test')
        if r.text == 'REST api is running':
            return True
        else:
            return False


    # attempt to authenticate, return true if successful
    def authenticate(self):
        self.get_status() # get an updated crsf token

        payload={
        'user': self.username,
        'password': self.passwd
        }

        r = self._r_session.post(self.base_url+'authn/login', data=payload)
        
        if r.status_code != 200:
            print('[ERROR](', r.status_code, '): failed to reach ', self.base_url+'authn/login')
            print(r.text)
            return False
        else:
            print('[SUCCESS] authenticated, HTTP code ', r.status_code)
            self._bearer_tkn = r.headers['Authorization']
            self._r_session.headers.update({'Authorization': r.headers['Authorization'], 'X-XSRF-TOKEN': r.headers['DSPACE-XSRF-TOKEN']})
            return True



    # log the current user out of the database
    def logout(self):
        r = requests.post(self.base_url + '/api/authn/logout')


    # get status of the user token/API as a boolean, true if connected
    def get_status(self, debug=False):
        if self._bearer_tkn == '':
            print('[WARNING] get_status() not conclusive because you are not logged in currently.\nIf login is not required you may still be able to use server, but you can\'t use this function.')

        r = self._r_session.get(self.base_url+'authn/status')

        # update CSRF token if available
        if 'DSPACE-XSRF-COOKIE' in r.cookies.keys():
            self._r_session.headers.update({'DSPACE-XSRF-COOKIE': r.cookies['DSPACE-XSRF-COOKIE'], 'X-XSRF-TOKEN': r.cookies['DSPACE-XSRF-COOKIE']})

        if r.status_code != 200:
            print('(', r.status_code, ') AUTHN STATUS \n\t', 'False')
            print(r.text)
            if r.status_code < 400: print('\tCSRF: ', self._csrf_token, '\n\tAuthorization: ', self._bearer_tkn)
            return False

        else: 
            json_out = r.json() # get json output
            if debug:
                print('(', r.status_code, ') AUTHN STATUS \n\t', json_out['authenticated'])
            if 'DSPACE-XSRF-COOKIE' in r.cookies.keys():
                self._csrf_token = r.cookies['DSPACE-XSRF-COOKIE'] # update csrf token

            #print('set CSRF Token: ', self._csrf_token)
            return json_out['authenticated']

    '''
        Get the status of the connection to dspace and return a dictionary with the following information:

            okay: boolean state of connection, true if good connection
            authenticated: true if the session has a valid JSESSIONID, can only be true if user has submitted email and passwd using /login
            email: email of the user whose account was used for authentication
            fullname: name/role associated with this account
            apiVersion: version of the API running on server
            sourceVersion: version of code on server
            '''
    def get_session_status(self):
        r = self._r_session.get(self.base_url+'authn/status')
        # update CSRF token
        if 'DSPACE-XSRF-COOKIE' in r.cookies.keys():
            self._csrf_token = r.cookies['DSPACE-XSRF-COOKIE']

        return json_output 


    # get the DSpace metadata for a single item specified by the uuid
    def get_item_metadata(self, uuid):
        r = requests.get(self.base_url + 'core/items/{}'.format(uuid))

        if r.status_code != 200:
            print(uuid)
            raise Exception('unable to get item: ' + uuid + '\n\t' + r.text)

        # update CSRF token if possible
        if 'DSPACE-XSRF-COOKIE' in r.cookies.keys():
            self._r_session.headers.update({'DSPACE-XSRF-COOKIE': r.cookies['DSPACE-XSRF-COOKIE'], 'X-XSRF-TOKEN': r.cookies['DSPACE-XSRF-COOKIE']})
        """
        else:
            # convert from DSpace complex metadata format to simple key value pair dict
            dense_meta = {} # dictionary with simple key, value pairs
            for meta in r.json():
                dense_meta[meta['key']] = meta['value']
                return dense_meta
        """
        return r.json()['metadata']


    # Get an array of all the communities in the repository
    def get_communities(self, debug=True):
        communities = []
        offset = 0

        # run loop infinitely or until server can't give full page of results
        while True:
            r = requests.get(self.base_url+'/communities?offset={}&limit=100'.format(offset))

            # make sure request went through, otherwise throw error
            if r.status_code != 200:
                raise Exception('connnection to '+self.base_url+' failed')

                communities.append(r.json())

            # check if there are more results beyond this page
            if len(r.json()) < 100:
                break
            else:
                offset = offset + 100

        # print info about all communities returned
        if debug:
            for i in r.json():
                print('COMMUNITY \'{}\':'.format(i['name']))
                print('\tUUID:', i['uuid'], '\n\tHANDLE:', i['handle'])

                return communities


    # Get an array of all the collections in the repository as dictionaries
    def get_collections(self, debug=True):
        collection_json = [] # list of uuids retreived from DSpace
        page = 0
        page_limit = 1

        # run loop infinitely or until server can't give full page of results
        while page < page_limit:
            r = self._r_session.get(self.base_url+'core/collections?page={}'.format(page))

            # make sure request went through, otherwise throw error
            if r.status_code != 200:
                raise Exception('connnection to '+self.base_url+' failed')
            else:
                # update CSRF token if possible
                if 'DSPACE-XSRF-COOKIE' in r.cookies.keys():
                    self._r_session.headers.update({'DSPACE-XSRF-COOKIE': r.cookies['DSPACE-XSRF-COOKIE'], 'X-XSRF-TOKEN': r.cookies['DSPACE-XSRF-COOKIE']})

            # get json content
            json_out = r.json()
            embedded_content = json_out['_embedded']

            # iterate over the collection returned, is an array of dictionaries
            collections = embedded_content['collections']
            for item in collections:
                collection_json.append(item)

            # check page limits
            page_limit = (json_out['page'])['totalPages']
            # move to next page
            page = page + 1

            # print info about all communities returned
            if debug:
                for i in collections:
                    print('COLLECTION \'{}\':'.format(i['name']))
                    print('\tUUID:', i['uuid'], '\n\tHANDLE:', i['handle'])

        return collection_json


    # Get an array of all the item UUIDs in a collection
    def get_items(self, cid='', debug=False):
        print("[WARNING] please wait, retrieving item IDs, may take a while for large collections")
        item_uuids = []

        # create url with {} for string formatting and page iteration
        if cid == '': # get all items in dspace
            url = self.base_url + '/core/items?page={}'
        else: # get only the items in specified collection
            url = self.base_url + '/discover/search/objects?page={}&dsoType=item&scope='+cid

        i = 0           # default num pages of results left to retrieve
        page_limit = 1  # last page returned

        # run loop infinitely or until server can't give full page of results
        while True and i < page_limit:
            # set page
            r = self._r_session.get(url.format(i))
            # make sure request went through, otherwise throw error
            if r.status_code >= 400:
                raise Exception('connnection to '+self.base_url+' failed')
                print(r.text)
            else:
                if debug:
                    print("[SUCCESS]")
                    print(r.text)

                # update CSRF token if possible
                if 'DSPACE-XSRF-COOKIE' in r.cookies.keys():
                    self._r_session.headers.update({'DSPACE-XSRF-COOKIE': r.cookies['DSPACE-XSRF-COOKIE'], 'X-XSRF-TOKEN': r.cookies['DSPACE-XSRF-COOKIE']})

            # process results
            r_json = r.json()
            embedded_content = r_json["_embedded"] # contains searchResult
            searchResults = embedded_content["searchResult"]
            items = (searchResults["_embedded"])["objects"] # gets list of item containers containing metadata
            page_data = searchResults["page"] # returns dict with page num, results length
            # get list of UUIDs for lookup
            item_uuids += self._parse_objects_for_items(items)
            # check limit
            page_limit = page_data['totalPages'] 
            if debug: print("PAGE LIMIT = ", page_limit, " PAGE ", i , "/", page_limit)
            # increment page index
            i = i+1

        # print info about all communities returned
        if debug:
            """for i in r.json():
                print('ITEM \'{}\':'.format(i['name']))
                print('\tUUID:', i['uuid'], '\n\tHANDLE:', i['handle'])
            """
            print("RETRIEVED ", len(item_uuids), " ITEMS")

        return item_uuids


    # get the metadata from DSpace for an item identified by UUID
    def get_item(self, uuid):
        r = self._r_session.get(self.base_url+'/core/items/'+uuid)

        if r.status_code != 200:
            raise Exception('connection to '+self.base_url+' failed')
        else:
            # update CSRF token if possible
            if 'DSPACE-XSRF-COOKIE' in r.cookies.keys():
                self._r_session.headers.update({'DSPACE-XSRF-COOKIE': r.cookies['DSPACE-XSRF-COOKIE'], 'X-XSRF-TOKEN': r.cookies['DSPACE-XSRF-COOKIE']})
            print('After Get Item:', r.json())
            return r.json()


    # update the metadata record for an item using a list structure or the doi of the item
    def update_item(self, ditem, new_meta={}):
        doi = ''
        if ditem is {} and new_meta is {}:
            raise Exception('insufficient information, need dspace item json object or doi resolver json object')

        elif ditem is not {}:
            # get metadata so we can get DOI to resolve
            #print('DITEM UUID:', ditem['uuid'])
            dspace_meta = self.get_item_metadata(ditem['uuid'])

            # handle errors with bad/insufficient metadata
            if 'dc.identifier' not in dspace_meta.keys() or dspace_meta['dc.identifier'] == '':
                print('no doi attached to object\n\t\t', dspace_meta)
                return

                doi = dspace_meta['dc.identifier']
                dres = DOIResolver()
                new_meta = dres.get_meta(doi)
            #print('NEW META:\n\t\t', new_meta)

            # check for keys before adding them to metadata
            abstract = ''
            URL = ''
            authors = ''
            publisher = ''
            date = ''
            if 'abstract' in new_meta.keys():
                abstract = new_meta['abstract']
                if 'URL' in new_meta.keys():
                    URL = new_meta['URL']
                    if 'author' in new_meta.keys():
                        authors = dres.authors_to_str(new_meta['author'])
                        if 'publisher' in new_meta.keys():
                            publisher = new_meta['publisher']

            # format metadata and upload
            payload = json.dumps([
                {
                'key': "dc.identifier.uri", 
                'value': URL, 
                'language': None
                },
                {
                'key': 'dc.contributor.author',
                'value': authors,
                'language': None
                },
                {
                'key': 'dc.publisher',
                'value': publisher,
                'language': None
                },
                {
                'key': 'dc.description.abstract',
                'value': abstract,
                'language': None
                },
                {
                'key': 'dc.date',
                'value': dres.get_date(new_meta),
                'language': None
                }
                ])

            headers = {
            'Content-Type': 'application/json'
            }

            r = requests.post(self.base_url + '/items/{}/metadata'.format(ditem['uuid']), headers=headers, data=payload, cookies=self.session_id)

            if r.status_code != 200:
                raise Exception('could not update item', r.text)

    """
        Create an item from basic metadata fields that are common across almost all 
        databases and upload to DSpace collection.
    """
    def create_item(self, cid, title, authors, description, doi):
        # get supplemental metadata by resolving DOI to get best version of metadata
        dres = DOIResolver()
        sup_meta = {}
        if doi != '':
            try: # randomly resolving metadata has failed...
                sup_meta = dres.get_meta(doi)
            except:
                sup_meta = {}
            else:
                sup_meta = {}

        # get abstract from resolved DOI
        if 'abstract' in sup_meta.keys():
            abstract = sup_meta['abstract']
        else:
            abstract = ''

        # clean all text fields to remove HTML tags
        if description != None: description = BeautifulSoup(description, 'lxml').text
        if abstract != None: abstract = BeautifulSoup(abstract, 'lxml').text
        if title != None: title = BeautifulSoup(title, 'lxml').text

        # construct new item object with metadata using dublin core identifiers, convert json dict to string
        # JSON format used as of DSpace 7
        payload = json.dumps({
          "name": title,
          "metadata": {
            "dc.contributor.author": self._authors_to_dspace_object(authors),
            "dc.date.issued": [
              {
                "value": dres.get_date(sup_meta),
                "language": None,
                "authority": None,
                "confidence": -1,
                "place": 0
              }
            ],
            "dc.description": [
              {
                "value": description,
                "language": None,
                "authority": None,
                "confidence": -1,
                "place": 0
              }
            ],
            "dc.description.abstract": [
              {
                "value": abstract,
                "language": None,
                "authority": None,
                "confidence": -1,
                "place": 0
              }
            ],
            "dc.identifier.citation": [
              {
                "value": None,
                "language": None,
                "authority": None,
                "confidence": -1,
                "place": 0
              }
            ],
            "dc.identifier.other": [
              {
                "value": doi,
                "language": None,
                "authority": None,
                "confidence": -1,
                "place": 0
              }
            ],
            "dc.identifier.uri": [
              {
                "value": None,
                "language": None,
                "authority": None,
                "confidence": -1,
                "place": 0
              }
            ],
            "dc.title": [
              {
                "value": title,
                "language": None,
                "authority": None,
                "confidence": -1,
                "place": 0
              }
            ]
          },
          "inArchive": True,
          "discoverable": True,
          "withdrawn": False,
          "entityType": None,
          "type": "item"
        })

        r = self._r_session.post(self.base_url+'core/items?owningCollection={}'.format(cid), headers={'content-type': 'application/json'}, data=payload)

        # check status of item post and print message if unsuccessful
        if r.status_code >= 400: # anything above 400 is a critical failure
            print('({})\n\t{}'.format(r.status_code, r.text))
        else:
            # update CSRF token if possible
            if 'DSPACE-XSRF-COOKIE' in r.cookies.keys():
                self._r_session.headers.update({'DSPACE-XSRF-COOKIE': r.cookies['DSPACE-XSRF-COOKIE'], 'X-XSRF-TOKEN': r.cookies['DSPACE-XSRF-COOKIE']})
            print('[SUCCESS] ', r.status_code)


    # remove an item from the collection, requires item UUID
    def delete_item(self, item_id):
        if '/' in item_id:
            raise Exception('Identifier passed to delete item is invalid, contains \'\/\' try using UUID instead of handle')

        r = self._r_session.delete(self.base_url+'core/items/{id}'.format(id=item_id))

        # 200 is good, 204 is good but no content
        if r.status_code >= 400:
            raise Exception('({})\n\t{}'.format(r.status_code, r.text))
        else:
            # update CSRF token if possible
            if 'DSPACE-XSRF-COOKIE' in r.cookies.keys():
                self._r_session.headers.update({'DSPACE-XSRF-COOKIE': r.cookies['DSPACE-XSRF-COOKIE'], 'X-XSRF-TOKEN': r.cookies['DSPACE-XSRF-COOKIE']})


    # delete all items from the dspace collection specified
    def empty_collection(self, cid):
        item_uuids = self.get_items(cid=cid)
        print(item_uuids)
        print("NUM ITEMS RETRIEVED: ", len(item_uuids))
        for item in item_uuids:
            print(item)
            self.delete_item(item)

    '''
        iterate through csv and convert each entry into a dspace 'item'
        then create a new dspace collection and place items in the collection.

        TODO: decide whether this is a helpful feature or not 
    '''
    def export_to_Briefcase(self, filepath):
        # list of XML objects formatted as dspace 'items' to add to the repository
        items = []

        case = Briefcase()

        # currently just prints out the key word
        with open(filepath, 'r') as csv_file:
            r = csv.reader(csv_file)
            for row in r:
                doc = Document(title=row[7], 
                    authors=row[1], link='', abstract=row[0], 
                    source=row[6], keywords=row[5], doi=row[2], datatype=row[3], date=row[4])
                
                case.add(doc.to_dictionary())

                return case