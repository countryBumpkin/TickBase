from dcxml import dcxml
from dspace import DSpace
from crawler import Crawler
from mendeleydata_interface import IMendeley_Data
import requests

def test_crawler_integration():
    gs = IMendeley_Data()
    da_craw = Crawler(repository_interface=gs, csv_path='C:/Users/deepg/Documents/TickBase/searches/test_search.csv')
    da_craw.search_all()

    da_craw.export_to_dspace(cid='67720a66-6412-4f76-8f18-80d516633cee', uname='garrettrwells@gmail.com', passwd='GW091799')

def test_single_item():
    a = DSpace(username='garrettrwells@gmail.com', passwd='GW091799')
    a.authenticate()
    a.create_item(cid='67720a66-6412-4f76-8f18-80d516633cee', title='test 2', author='H. G. Wells', description='test upload', doi='10.12345/123124')
    #a.delete_item('123456789/18')
    a.get_items()
    a.logout()

def test_get():
    a = DSpace(username='garrettrwells@gmail.com', passwd='GW091799')
    a.authenticate()
    a.get_communities()
    a.get_collections()
    a.get_bitstreams()
    a.get_handle(handle = '123456789/3')
    a.logout()

test_crawler_integration()
'''
a.create_community(id=000, name='Test Community', handle='1234/1', link='/rest/communities/000',
                    expand=["parentCommunity","collections","subCommunities","logo","all"], logo=None, parentCommunity=None,
                    copyrightText='', introductoryText='', shortDesc='', sidebarText='', countItems=0, subCommunities=[], collections=[])
'''


#r = requests.get('http://dspace-dev.nkn.uidaho.edu:8080/rC:\Users\deepg\Documents\TickBase\searchesst/collections/123456789/2')

#print(r.json())
#a.get_status()
