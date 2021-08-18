from dcxml import dcxml
from dspace import DSpace
from crawler import Crawler
from mendeleydata_interface import IMendeley_Data
from doiresolver import DOIResolver
import requests
import unittest

# test framework for the DSpace interface
class TestDSpace(unittest.TestCase):

    def test_all(self):
        points = self.test_authenticate() + self.test_crawler_integration() + self.test_single_item() + self.test_get_items() + self.test_get_item() + self.test_update_item() + self.test_update_items() + self.test_get_metadata() + self.test_delete_items()
        print('TEST RESULTS:\n\tscore = ', str(points) + '/9', sep='')

    # test authenticating a session
    def test_authenticate(self):
        dspc = DSpace(username='garrettrwells@gmail.com', passwd='GW091799')
        dspc.authenticate()
        container = dspc.get_status()
        dspc.logout()

        self.assertEqual(container, True)

        return 1

    # test importing data from search
    def test_crawler_integration(self):
    
        try:
            gs = IMendeley_Data()
            da_craw = Crawler(repository_interface=gs, csv_path='C:/Users/deepg/Documents/TickBase/searches/test_search.csv')
            da_craw.search_all()
            da_craw.export_to_dspace(cid='67720a66-6412-4f76-8f18-80d516633cee', uname='garrettrwells@gmail.com', passwd='GW091799')
            return 1
        except:
            print('FAILED: test_crawler_integration()')
            return 0

    # test creation of a single item
    def test_single_item(self):
        try:
            a = DSpace(username='garrettrwells@gmail.com', passwd='GW091799')
            a.authenticate()
            a.create_item(cid='67720a66-6412-4f76-8f18-80d516633cee', title='test 2', author='H. G. Wells', description='test upload', doi='10.12345/123124')
            #a.delete_item('123456789/18')
            a.get_items()
            a.logout()
            return 1
        except:
            print('FAILED: test_single_item()')
            return 0

    # test updating a single item
    def test_update_item(self):
        try:
            dspc = DSpace(username='garrettrwells@gmail.com', passwd='GW091799')
            dspc.authenticate()
            item = dspc.get_item(uuid='2e003b53-da42-45a9-9172-c8f1cfeb2ece')
            dspc.update_item(ditem=item)
            return 1

        except:
            print('FAILED: test_update_item()')
            return 0

    # test updating all items in a collection
    def test_update_items(self):
        try:
            dspc = DSpace(username='garrettrwells@gmail.com', passwd='GW091799')
            dspc.authenticate()
            dspc.update_items(cids=['67720a66-6412-4f76-8f18-80d516633cee'])
            return 1
        except:
            print('FAILED: test_update_items()')
            return 0

    # test getting a single item from dspace
    def test_get_item(self):
        try:
            dspce = DSpace(username='garrettrwells@gmail.com', passwd='GW091799')
            dspce.authenticate()

            print(dspce.get_item('2e003b53-da42-45a9-9172-c8f1cfeb2ece'))
            return 1
        except:
            print('FAILED: test_get_item()')
            return 0

    # test getting all items from a collection
    def test_get_items(self):
        try:
            a = DSpace(username='garrettrwells@gmail.com', passwd='GW091799')
            a.authenticate()
            #a.get_communities()
            #a.get_collections()
            #a.get_bitstreams()
            #a.get_handle(handle = '123456789/3')
            items = a.get_items(cid='67720a66-6412-4f76-8f18-80d516633cee')
            print(items)
            a.logout()
            return 1
        except:
            print('FAILED: test_get_items()')
            return 0

    def test_delete_items(self):
        dspc = DSpace(username='garrettrwells@gmail.com', passwd='GW091799')
        dspc.authenticate()
        dspc.empty_collection('67720a66-6412-4f76-8f18-80d516633cee')
        res_size = len(dspc.get_items(cid='67720a66-6412-4f76-8f18-80d516633cee'))
        if res_size <= 4:
            return 1
        else:
            print('FAILED: test_delete_items(), ', res_size, 'items remain')
            return 0

    def test_get_metadata(self):
        dspc = DSpace(username='garrettrwells@gmail.com', passwd='GW091799')
        dspc.authenticate()
        meta = dspc.get_item_metadata('2e003b53-da42-45a9-9172-c8f1cfeb2ece')
        if meta != None:
            print('Metadata\n\t', meta)
            return 1

        else:
            print('FAILED: test_get_metadata()')
            return 0

# test framework for the DOIResolver program
class TestDOIResolver:

    def test_all(self):
        points = self.test_resolve_meta() + self.test_authors_tostr()

        print('TEST RESULTS:\n\tscore = ', points, '/2', sep='')

    # make sure the doi resolver is outputting real data
    def test_resolve_meta(self):
        doi = '10.1109/5.771073'

        dres = DOIResolver()
        meta = dres.get_meta(doi)

        print('meta:', meta)

        if meta != None:
            return 1

        else:
            return 0

    def test_authors_tostr(self):
        doi = '10.1109/5.771073'

        dres = DOIResolver()
        meta = dres.get_meta(doi)

        authors = dres.authors_to_str(meta['author'])
        print('authors:', authors)

        if authors != '':
            return 1

        return 0

    def test_get_meta_bulk(self):
        doiR = DOIResolver()
        all_keys = []

        with open("C:/Users/deepg/Documents/TickBase/code/test_dois.csv", 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                temp_row = row[0].replace('[\'', '')
                temp_row = temp_row.replace('\']', '')
                print(temp_row)

                meta = doiR.get_meta(doi=temp_row)
                temp_keys = meta.keys()
                for key in temp_keys:
                    if key not in all_keys:
                        print('some doi meta missing', key)
                        all_keys.append(key)

                print('\n\t\t', meta)

        print('ALL KEYS FOUND:\n\t', all_keys)


print(TestDSpace().test_all())
#print(TestDOIResolver().test_all())
'''
a.create_community(id=000, name='Test Community', handle='1234/1', link='/rest/communities/000',
                    expand=["parentCommunity","collections","subCommunities","logo","all"], logo=None, parentCommunity=None,
                    copyrightText='', introductoryText='', shortDesc='', sidebarText='', countItems=0, subCommunities=[], collections=[])
'''


#r = requests.get('http://dspace-dev.nkn.uidaho.edu:8080/rC:\Users\deepg\Documents\TickBase\searchesst/collections/123456789/2')

#print(r.json())
#a.get_status()
