import os
import csv
import json
import requests
import warnings
from bs4 import BeautifulSoup

# Class provides API for DuraSpace development
class DSpace:

    _nkn_base_url = 'http://dspace-dev.nkn.uidaho.edu:8080/rest'

    def __init__(self, username='', passwd='', base_url='', csrf_token=''):
        self.username = username
        self.passwd = passwd
        self.csrf_token = csrf_token

        # default value of session id, shows not logged in if ''
        # may be able to use system without logging in but getting session status will not
        # be available
        self.session_id = ''

        if base_url == '':
            self.base_url = self._nkn_base_url
        else:
            self.base_url = base_url + '/rest'

    # Check if REST API is installed
    def api_running(self):
        r = requests.get(self.base_url+'/test')
        if r.text == 'REST api is running':
            return True
        else:
            return False

    # Attempt to authenticate, return true if successful
    def authenticate(self):
        #data = 'email={}&password={}'.format('garrettrwells@gmail.com', 'GW091799')
        data = {
            'email': 'garrettrwells@gmail.com',
            'password': 'GW091799'
        }

        r = requests.post(self.base_url + '/login', data=data)

        if r.status_code != 200:
            print(self.base_url+'/login')
            raise Exception('failed authentication, HTTP code ' + str(r.status_code))
            return False
        else:
            print('successful authentication, HTTP code ', r.status_code)
            # get the JSESSIONID which will be used to authenticate future requests
            self.session_id = r.cookies
            print(r.cookies['JSESSIONID'])
            return True

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
        r = requests.get(self.base_url+'/status')
        json_output = r.json()

        return json_output

    # log the current user out of the database
    def logout(self):
        r = requests.post(self.base_url + '/logout', cookies=self.session_id)

    # get status of tyhe user token/API
    def get_status(self):
        if self.session_id == '':
            print('Warning: get_status() not conclusive because you are not logged in currently.\nIf login is not required you may still be able to use server, but you can\'t use this function.')
            return

        r = requests.get(self.base_url+'/status')

        if r.status_code != 200:
            warnings.warn('connection to '+self.base_url+' failed')
        else:
            print(r.json())

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

    # Get an array of all the collections in the repository
    def get_collections(self, debug=True):
        collections = []
        offset = 0

        # run loop infinitely or until server can't give full page of results
        while True:
            r = requests.get(self.base_url+'/collections?offset={}&limit=100'.format(offset))

            # make sure request went through, otherwise throw error
            if r.status_code != 200:
                raise Exception('connnection to '+self.base_url+' failed')

            collections.append(r.json())

            # check if there are more results beyond this page
            if len(r.json()) < 100:
                break
            else:
                offset = offset + 100

        # print info about all communities returned
        if debug:
            for i in r.json():
                print('COLLECTION \'{}\':'.format(i['name']))
                print('\tUUID:', i['uuid'], '\n\tHANDLE:', i['handle'])

        return collections

    # Get an array of all the items in the repository
    def get_items(self, debug=True):
        items = []
        offset = 0

        # run loop infinitely or until server can't give full page of results
        while True:
            r = requests.get(self.base_url+'/items?offset={}&limit=100'.format(offset))

            # make sure request went through, otherwise throw error
            if r.status_code != 200:
                raise Exception('connnection to '+self.base_url+' failed')

            items.append(r.json())

            # check if there are more results beyond this page
            if len(r.json()) < 100:
                break
            else:
                offset = offset + 100

        # print info about all communities returned
        if debug:
            for i in r.json():
                print('ITEM \'{}\':'.format(i['name']))
                print('\tUUID:', i['uuid'], '\n\tHANDLE:', i['handle'])

        return items

    # Get an array of all the collections in the repository
    def get_bitstreams(self, debug=True):
        bitstreams = []
        offset = 0

        # run loop infinitely or until server can't give full page of results
        while True:
            r = requests.get(self.base_url+'/bitstreams?offset={}&limit=100'.format(offset))

            # make sure request went through, otherwise throw error
            if r.status_code != 200:
                raise Exception('connnection to '+self.base_url+' failed')

            bitstreams.append(r.json())

            # check if there are more results beyond this page
            if len(r.json()) < 100:
                break
            else:
                offset = offset + 100

        # print info about all communities returned
        if debug:
            for i in r.json():
                print('BITSTREAMS \'{}\':'.format(i['name']))
                print('\tUUID:', i['uuid'], '\n\tHANDLE:', i['handle'])

        return bitstreams

    # return the object specified by the handle passed to this function
    def get_handle(self, handle=''):
        if handle == '':
            raise Exception('handle is empty, please input a value')

        r = requests.get(self.base_url+'/handle/{}'.format(handle))

        if r.status_code != 200:
            raise Exception('connection to '+self.base_url+' failed')
        else:
            print('After Get Handle:', r.json())
            return r.json()

    # Create a new community
    def create_community(self, id=000, name='', handle='', type='community', link='/rest/communities/000',
                        expand=["parentCommunity","collections","subCommunities","logo","all"], logo=None, parentCommunity=None,
                        copyrightText='', introductoryText='', shortDesc='', sidebarText='', countItems=0, subCommunities=[], collections=[]):

        '''
        community_obj = { "id":id,
                          "name":name,
                          "handle":handle,
                          "type":type,
                          "link":link,
                          "expand":expand,
                          "logo":logo,
                          "parentCommunity":parentCommunity,
                          "copyrightText":copyrightText,
                          "introductoryText":introductoryText,
                          "shortDescription":shortDesc,
                          "sidebarText":sidebarText,
                          "countItems":countItems,
                          "subcommunities":subCommunities,
                          "collections":collections
                        }'''

        community_obj = {
            'id': '12345',
            'name': name,
            'link': link,
            'handle': handle
        }

        r = requests.put(self.base_url + '/communities', data=community_obj)

    # TODO implement this function
    def create_collection(self, community=''):
        print('Implement create collection!')

    # create an item and add to collection
    def create_item(self, cid, title, author, description, doi):
        # check connection and authentication status and provide error handling
        try:
            status = get_session_status()
            if not status['authenticated']:
                raise Exception('Not authenticated, call authenticate() before attempting to get status')
        except:
            raise Exception('Connection Failed while checking status in create_item()')

        # construct new item object with metadata using dublin core identifiers
        payload = json.dumps(
                    {
                        "metadata": [
                            {
                                "key": "dc.contributor.author",
                                "value": author
                            },
                            {
                                "key": "dc.description",
                                "value": description
                            },
                            {
                                "key": "dc.title",
                                "value": title
                            },
                            {
                                "key": "dc.identifier",
                                "value": doi
                            }
                        ]
                    }
                )

        # construct headers with session id(authentication key) and submit request
        headers = {
            'Authorization': 'Bearer 999C94C5A92473D707225B890C08C398',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID='+self.session_id['JSESSIONID']
        }
        r = requests.request("POST", self.base_url+'/collections/{}/items'.format(cid), headers=headers, data=payload)

        # Check status of item post and print message if unsuccessful
        if r.status_code != 200:
            print('HTTP ERROR RESPONSE:\n\t',r.text)
        else:
            print('SUCCESS: ', r.status_code)

    # remove an item from the collection, requires UUID instead of handle
    def delete_item(self, item_id):
        if uuid.contains('/'):
            raise Exception('Identifier passed to delete item is invalid, contains \'\/\' try using UUID instead of handle')

        r = requests.delete(self.base_url+'/items/{id}'.format(id=item_id))

        if r.status_code != 200:
            raise Exception('Unable to remove item from collection, connection failed\n\tHTTP CODE:{}\n\tHTTP BODY{}'.format(r.status_code, r.text))


    '''
        iterate through csv and convert each entry into a dspace 'item'
        then create a new dspace collection and place items in the collection
    '''
    def import_csv(self, filepath):

        # list of XML objects formatted as dspace 'items' to add to the repository
        items = []

        with open(filepath, 'r') as csv_file:
            r = csv.reader(csv_file)

            for row in r:
                print(row[1])
