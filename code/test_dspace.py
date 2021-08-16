from dcxml import dcxml
from dspace import DSpace
from crawler import Crawler
from mendeleydata_interface import IMendeley_Data
from doiresolver import DOIResolver
import requests

# test framework for the DSpace interface
class TestDSpace:

    def test_all(self):
        points = self.test_authenticate() + self.test_crawler_integeration() +
                    self.test_single_item() + self.get_items() +
                    self.test_get_item() + self.test_update_item() + self.test_delete_items()
        print('TEST RESULTS:\n\tscore = ', str(points) + '/2', sep='')

    # test authenticating a session
    def test_authenticate(self):
        dspc = DSpace(username='garrettrwells@gmail.com', passwd='GW091799')
        dspc.authenticate()
        container = dspc.get_status()
        if container: 
            points = 1
        else:
            points = 0
        dspc.logout()

        return points

    # test importing data from search
    def test_crawler_integration(self):
    
        try:
            gs = IMendeley_Data()
            da_craw = Crawler(repository_interface=gs, csv_path='C:/Users/deepg/Documents/TickBase/searches/test_search.csv')
            da_craw.search_all()
            da_craw.export_to_dspace(cid='67720a66-6412-4f76-8f18-80d516633cee', uname='garrettrwells@gmail.com', passwd='GW091799')
            return 1
        except:
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
            return 0

    # test updating a single item
    def test_update_item(self):
        try:
            dspc = DSpace(username='garrettrwells@gmail.com', passwd='GW091799')
            dspc.authenticate()
            item = dspc.get_item(uuid='195dea78-0729-46f0-bb63-40bf4ed1908d')
            dspc.update_item(ditem=item)
            return 1

        except:
            return 0

    # test getting a single item from dspace
    def test_get_item(self):
        try:
            dspce = DSpace(username='garrettrwells@gmail.com', passwd='GW091799')
            dspce.authenticate()

            print(dspce.get_item('195dea78-0729-46f0-bb63-40bf4ed1908d'))
            return 1
        except:
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
            return 0

    def test_delete_items(self):
        dspc = DSpace(username='garrettrwells@gmail.com', passwd='GW091799')
        dspc.authenticate()
        dspc.empty_collection('67720a66-6412-4f76-8f18-80d516633cee')
        if len(dspc.get_items(cid='67720a66-6412-4f76-8f18-80d516633cee')) == 0:
            return 1
        else:
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


print(TestDSpace().test_update_item())
#print(TestDOIResolver().test_all())
'''
a.create_community(id=000, name='Test Community', handle='1234/1', link='/rest/communities/000',
                    expand=["parentCommunity","collections","subCommunities","logo","all"], logo=None, parentCommunity=None,
                    copyrightText='', introductoryText='', shortDesc='', sidebarText='', countItems=0, subCommunities=[], collections=[])
'''


#r = requests.get('http://dspace-dev.nkn.uidaho.edu:8080/rC:\Users\deepg\Documents\TickBase\searchesst/collections/123456789/2')

#print(r.json())
#a.get_status()
