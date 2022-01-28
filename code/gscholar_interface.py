from portal_interface import Portal
import requests

'''
    This interface is not ready to work currently. Searches rquire using a paid endpoint or making your own spider for web crawling.
'''
class GScholar(Portal):

    def __init__(self):
        self.tag = 'gscholar'
        self.base_url = 'https://google-search3.p.rapidapi.com/api/v1/scholar/q='

    def get_queryURL(self, key='', page=0):
        #return self.base_url + '&q={}&start={}'.format(key, page)
        return self.base_url + key

    def get_tag(self):
        return self.tag

    def get_content(self, response):
        return ('text', response)

    def query(self, key, parameters={}):
        """
        headers = {
                    "x-rapidapi-key": "b7bea820b9msh1b9ca37d8f3c9e1p1d6b57jsn8cd9a057f35b",
                    "x-rapidapi-host": "google-search3.p.rapidapi.com",
                    "useQueryString": True
                  }

        url = self.get_queryURL(key, 0)
        print(url)
        return requests.get(url, params=headers)
        """
        url = "https://google-search3.p.rapidapi.com/api/v1/scholar/q={}".format(key)

        headers = {
                    'x-rapidapi-key': "54f896f3cfmsh5f56479704e9899p123546jsn61616fb0468e",
                    'x-rapidapi-host': "google-search3.p.rapidapi.com"
                  }

        response = requests.get(url, headers=headers)
        print('\turl =', url)
        print('\ttext result =', response.text)

        """
        if len(results['results']) <= 0:
            print('ERROR no results from search')
        else:
            # parse Results
            print('TODO: parse results')
        """
        #return response.text
        return None # TODO: remove when fully implemented, replace with list of Document objects
