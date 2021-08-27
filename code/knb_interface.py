from portal_interface import Portal
from briefcase import Document
import requests
import json

'''
	This class retrieves data from the KNB repository.
	API: https://knb.ecoinformatics.org/api
'''
class IKNB(Portal):

	def __init__(self):
		self.tag = 'knb'
		self.result_type = 'data'

	# override the base implementation and return success by default
	def get_code(self, response):
		return response.status_code

	# use the Mendeley API to get the paginated results of a search
	# returns a list of all data objects parsed as Documents
	def query(self, key, type='TABULAR_DATA'):
		key = key.replace(' ', '+')
		response_list = []
		for i in range(500):
			start = i*100
			rows = 100
			section = 'abstract'
			tformat = 'json'
			search_string = "{}:{}&rows={}&start={}&wt={}&fl=dataUrl,abstract,keywords,title,author,identifier".format(section, key, rows, start, tformat)
			print('page #', i, 'https://knb.ecoinformatics.org/knb/d1/mn/v2/query/solr/q={}'.format(search_string))
			r = requests.get('https://knb.ecoinformatics.org/knb/d1/mn/v2/query/solr/q={}'.format(search_string))

			r_json = None

			# convert json to dict
			try:
				r_json = r.json()
			except:
				print('decode error')
				print(r.text)


			json_docs = r_json['response']
			print('number of results found =', json_docs['numFound'])

			# make sure there are some results to parse
			if json_docs['numFound'] == 0 or len(json_docs['docs']) == 0 or json_docs['start'] > json_docs['numFound']:
				break
			else:
				# get each search result from file
				i = 0
				for item in json_docs['docs']:
					i = i + 1
					response_list.append(item)

				print('i =', i)

		results = []

		# check that result is good
		if r.status_code == 200:
			for item in response_list:
				print('RAW DOC\n\t', item)
				# convert to Document list
				keys = item.keys()
				title = ''
				doi = ''
				authors = ''
				keywords = ''
				abstract = ''

				# verify keys are in the dictionary
				if 'title' in keys:
					title = item['title']
				if 'identifier' in keys:
					doi = item['identifier']
				if 'author' in keys:
					authors = item['author']
				if 'keywords' in keys:
					keywords = item['keywords']
				if 'abstract' in keys:
					abstract = item['abstract']

				file = Document(title=title,
								link=item['dataUrl'],
								abstract=abstract,
								keywords=keywords,
								authors=authors,
								doi=doi,
								datatype=type)
				results.append(file)

			return results

	# return tuple with data type and response from this object
	def get_content(self, response):
		return ('list', response)
