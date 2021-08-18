import requests
import json


'''
	Resolves DOIs for the user and prints/returns the metadata attached to the DOI.

	DOI: digital object identifier, a unified system for identifying journal articles and providing stable access to them through a single standard system. Protects against changes to where the material is published.

	Source: https://www.doi.org
	Content Negotiation: https://citation.crosscite.org/docs.html
'''
class DOIResolver:
	# keys included in all resolved doi metadata objects
	doi_keys = ['type', 'id', 'categories', 'language', 'author', 'issued', 'abstract', 'DOI', 'publisher', 'title', 'URL', 'copyright', 'version']

	def __init__(self):
		self.base_url = 'https://doi.org'

	# convert a list of authors in a dictionary to a string that can be processed by dspace
	def authors_to_str(self, author_list):
		#print('author_list:\n\t', author_list)
		author_string = ''
		num = 0
		for author in author_list:
			if num == 0:
				if 'given' in author.keys():
					author_string = '{given} {family}'.format(given=author['given'], family=author['family'])
				elif 'literal' in author.keys():
					author_string = author['literal']
				else:
					print('error not sure what this is')
			elif num >= 1:
				if 'given' in author.keys():
					author_string = author_string + ', {given} {family}'.format(given=author['given'], family=author['family'])
				elif 'literal' in author.keys():
					author_string = author_string + ', ' + author['literal']
				else:
					print('error not sure what this is')

			num = num+1

		return author_string

	'''
		get the metadata associated with this doi(as dict, list, etc), should be comprehensive, as in all metadata available

		https://www.doi.org/doi_handbook/1_Introduction.html (SECTION 1.6.3 DOI Name Syntax)

			DOIs consist of two parts separated by a '/': 1) the unique naming authority and 2) the unique identifier string

		the attributes contained in the dictionary will not be consistent across repositories, but here are are a few for example.
			['type', 'id', 'categories', 'language', 'author', 'issued', 'abstract', 'DOI', 'publisher', 'title', 'URL', 'copyright', 'version']

			['type', 'id', 'categories', 'language', 'author', 'issued', 'abstract', 'DOI', 'publisher', 'title', 'URL', 'copyright', 'version', 'contributor', 'indexed', 'reference-count', 'content-domain', 'created', 'source', 'is-referenced-by-count', 'prefix', 'member', 'container-title', 'original-title', 'deposited', 'score', 'subtitle', 'short-title', 'references-count', 'relation']
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