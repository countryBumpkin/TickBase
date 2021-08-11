import requests
import json


'''
	Resolves DOIs for the user and prints/returns the metadata attached to the DOI.

	DOI: digital object identifier, a unified system for identifying journal articles and providing stable access to them through a single standard system. Protects against changes to where the material is published.

	Source: https://www.doi.org
	Content Negotiation: https://citation.crosscite.org/docs.html
'''
class DOIResolver:

	def __init__(self):
		self.base_url = 'https://doi.org'

	# convert a list of authors in a dictionary to a string that can be processed by dspace
	def authors_to_str(self, author_list):
		author_string = ''
		num = 0
		for author in author_list:
			if num == 0:
				author_string = '{given} {family}'.format(given=author['given'], family=author['family'])
			elif num >= 1:
				author_string = author_string + ', {given} {family}'.format(given=author['given'], family=author['family'])

			num = num+1

		return author_string

	'''
		get the metadata associated with this doi(as dict, list, etc), should be comprehensive, as in all metadata available
	'''
	def get_meta(self, doi):
		print('DOI:\n\t', doi)
		
		if doi == '':
			raise Exception('Empty DOI')

		header = {
					'Accept': 'application/vnd.citationstyles.csl+json'
				}

		r = requests.get(self.base_url+'/'+doi, headers=header)

		if r.status_code != 200:
			raise Exception('Error getting metadata:\n\t'+r.text)
			return None
		else:
			#json_formatted = json.dumps(r.json(), indent=4)
			#print('DOI metadata:\n\t', json_formatted)
			#print('response text:\n\t', r.text)
			return r.json()