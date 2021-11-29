import requests

class Portal:

    # authenticate if necessary, set base url
    def __init__(self):
        self.tag = 'base_untagged'
        self.result_type = 'base_unknown'
        self.base_url = 'https://scholar.google.com'

    # query the database of this interface and return the parsed results
    def query(self, key, parameters={}):
        return requests.get(self.base_url + '?q=' + key)

    # return code from response
    def get_code(self, response):
        return response.status_code

    # return interface type
    def get_tag(self):
        return self.tag

    # return result type, like article or data
    def get_resultType(self):
        return self.result_type

    # return content of request if successful and tag data type
    # only used in interfaces where queries are made with Requests
    def get_content(self, response):
        is_JSON = True

        # try getting json
        try:
            out = response.json()
        except:
            is_JSON = False
            print('no json version')
        # try getting html
        try:
            out = response.text
        except:
            print('no text version')
        # mark what type of data this is
        if is_JSON:
            tag = 'json'
        else:
            tag = 'html'
        return (tag, out)
