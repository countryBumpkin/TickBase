from dcxml import dcxml
from dspace import DSpace
import requests
a = DSpace(username='garrettrwells@gmail.com', passwd='GW091799')
a.authenticate()
#a.get_communities()
#a.get_collections()
#a.get_bitstreams()
#a.get_handle(handle = '123456789/3')
#a.create_item(cid='67720a66-6412-4f76-8f18-80d516633cee', title='test 2', author='H. G. Wells', description='test upload', doi='10.12345/123124')
#a.delete_item('123456789/18')
a.get_items()
'''
a.create_community(id=000, name='Test Community', handle='1234/1', link='/rest/communities/000',
                    expand=["parentCommunity","collections","subCommunities","logo","all"], logo=None, parentCommunity=None,
                    copyrightText='', introductoryText='', shortDesc='', sidebarText='', countItems=0, subCommunities=[], collections=[])
'''
a.logout()

#r = requests.get('http://dspace-dev.nkn.uidaho.edu:8080/rest/collections/123456789/2')

#print(r.json())
#a.get_status()
