import requests
import json

'''
	Resolves DOIs for the user and prints/returns the metadata attached to the DOI. Also parses out the
	metadata from complicated fields (authors, date of creation)

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

		# iterate through list and convert to string with format
		# first last, first last, etc
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
		convert issued/deposited field to a conventional date, accepts either the full dictionary from a resolved doi(get_meta()) or will take just the dictionary value associated with 'issued'
			{'date-parts': [[2017]]}
			OR
			{'indexed': {'date-parts': [[2020, 7, 30]], 'date-time': '2020-07-30T11:48:08Z', 'timestamp': 1596109688711}, 'reference-count': 0,
			'publisher': 'Frontiers Media SA', 'content-domain': {'domain': [], 'crossmark-restriction': False}, 'DOI': '10.3389/fcimb.2019.00477.s001',
			'type': 'component', 'created': {'date-parts': [[2020, 1, 21]], 'date-time': '2020-01-21T05:22:03Z', 'timestamp': 1579584123000},
			'source': 'Crossref', 'is-referenced-by-count': 0, 'title': 'Image_1.tiff', 'prefix': '10.3389', 'member': '1965', 'container-title': [], 'original-title': [], 'deposited': {'date-parts': [[2020, 1, 21]], 'date-time': '2020-01-21T05:22:03Z', 
			'timestamp': 1579584123000}, 'score': 1.0, 'subtitle': [], 'short-title': [], 'issued': {'date-parts': [[None]]}, 'references-count': 0, 'URL': 'http://dx.doi.org/10.3389/fcimb.2019.00477.s001', 'relation': {}} 
	'''
	def get_date(self, meta):
			
		if 'issued' in meta.keys():
			meta = meta['deposited']
		elif 'created' in meta.keys():
			meta = meta['created']
		elif 'deposited' in meta.keys():
			meta = meta['deposited']

		raw = meta['date-parts'][0]

		year = ''
		month = ''
		day = ''
		i = 0

		for segment in raw:
			if i == 0:
				year = str(segment)
			elif i == 1:
				month = str(segment) + '/'
			elif i == 2:
				day = str(segment) + '/'

			i = i + 1

		date = month + day + year
		print('RAW\n\t\t', raw, '\nDATE\n\t\t', date)
		return date



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