import pandas as pd
import numpy as np
from dcxml import dcxml
import os
from collections import defaultdict

'''
	This is a data structure specifically for collecting lists of formatted article metadata. 
	The Briefcase consists of a list of Document objects.
	Metadata can be added and retrieved easily, converted to excel, csv, and dspace collections. 
'''
class Briefcase:

	def __init__(self):
		self.container = pd.DataFrame()
		self.containerDict = []

	# add a new row to the table of data
	def add(self, row={}):
		self.container = self.container.append(row, ignore_index=True)
		self.containerDict.append(row)
		# clean frame so that we don't have duplicate sources
		#self.container.drop_duplicates( subset=['URL'], inplace=True)

	def is_empty(self):
		return self.container.empty

	def to_excel(self, filename='briefcase'):
		self.container.to_excel(filename, index=False)

	def to_csv(self, filename='briefcase'):
		self.container.to_csv(filename, index=False)

	# convert briefcase contents to a DuraSpace Simple Archive containing metadata in dublin core XML files
	def to_batch(self, archive_name='briefcase'):
		# make new archive directory
		try:
			os.mkdir(archive_name)
		except:
			print('batch directory already exists')

		os.chdir(archive_name)

		print('DIRECTORY HEIRARCHY:\n\t', os.getcwd())
		count = 0
		for row in self.containerDict:
			os.mkdir('item_' + f'{count:03}')
			os.chdir('item_' + f'{count:03}')

			print(row)
			fname = 'dublin_core' + '.xml'
			with open(fname, 'w', encoding='utf-8') as file:
				dc_data = {
					'contributor': row['Authors'],
					'date.accessioned': 'TODO_accessioned',
					'date.available': 'TODO_available',
					'date.issued': 'TODO_issued',
					'identifier': row['DOI'],
					'identifier.citation': 'TODO_bibliographic_citation_here',
					'identifier.govdoc': 'TODO_gov_document#',
					'identifier.isbn': 'TODO_int_std_book#',
					'identifier.issn': 'TODO_int_std_serial#',
					'identifier.ismn': 'TODO_ismn_here',
					'identifier.other': 'TODO_other_id_here',
					'identifier.uri': 'TODO_uri_here',
					'description': row['Abstract'],
					'description.abstract': 'TODO_abstract_here',
					'description.provenance': 'TODO_provenance_here',
					'description.sponsorship': 'TODO_sponsorship_here',
					'format': 'TODO_format',
					'format.extent': 'TODO_format_extent',
					'format.medium': 'TODO_medium',
					'format.mimetype': 'TODO_mimetype',
					'language.iso': 'TODO_iso',
					'publisher': 'TODO_publisher',
					'subject': 'TODO_search_key_here',
					'title': row['Title'],
					'title.alternative': row['Title'],
					'type': row['Datatype'],
				}
				xml = dcxml(dc_data).tostring()

				file.write(xml)
			file.close()
			os.chdir('..')
			count = count + 1

	# convert all documents in this container to metadata items that can be posted to dspace
	def export_to_dspace(self, cid='', dspace=None):
		if dspace is None:
			raise Exception('no dspace connection provided, use DSpace library to submit valid connection')

		if cid is None:
			raise Exception('no cid, collection identifier, was specified')

		# iterate through container elements and convert each to a dspace item
		for doc in self.containerDict:
			dspace.create_item(
						cid=cid,
						title=doc['Title'],
						author=doc['Authors'],
						description=doc['Abstract'],
						doi=doc['DOI']
						)

	# print contents of the dataframe
	def print(self):
		print('\nBriefcase Contains: ---------------\n', self.container)

'''
	data holder for data parsed from data repos, allows conversion from repo metadata tags to 
	bconsistent metadata tags
'''
class Document:

	def __init__(self, title='', authors='', link='https://default_link', abstract='', source='', keywords='', doi='', datatype='unkown', date=''):
		self.title = title
		self.authors = authors
		self.link = link
		self.source = source
		self.abstract = abstract
		self.keywords = keywords
		self.doi = doi
		self.datatype = datatype
		self.date = date

		# provide all data in dictionary format too
		self.data = {}
		self.data['Title'] = title 
		self.data['Authors'] = authors
		self.data['Source'] = source
		if link != 'https://default_link': self.data['Link'] = link
		self.data['Abstract'] = abstract
		self.data['Keywords'] = keywords
		self.data['DOI'] = doi
		self.data['Datatype'] = datatype
		self.data['Date'] = date

	def get_title(self):
		return self.data['Title']

	def get_doi(self):
		return self.data['DOI']

	def get_link(self):
		return self.data['Link']

	def get_source(self):
		return self.data['Source']

	# convert the stored data to a json data object, currently just dumps the json data to a string
	# TODO: decide how to handle the data
	def to_json(self):
		output = json.dumps(self.data)
		print(output)
		return output

	# convert contents of Document object to a dictionary object
	def to_dictionary(self):
		return self.data

	# convert the information stored into a Dublin Core XML string
	def to_dc_XML(self):
		dc_data = {
			'title': [self.data['title']],
			'creator': str(self.data['Authors']),
			'description': [str(self.data['Abstract'])],
			'identifier': [str(self.data['DOI'])],
			'type': [str(self.data['Datatype'])],
		}
		xml = simpledc.tostring(dc_data)
		print('\n\t', xml)
		return xml

	# print contents of the Document in an easy to read format
	def print(self):
		print('DOCUMENT')
		print('\tTITLE:', self.data['Title'])
		# NOTE: removed because not this is not collected from every data publication/repo 
		#print('\tTYPE:', doc.type)
		print('\tSOURCE:', self.data['Source'])
		print('\tKEYWORDS:', self.data['Keywords'])
		print('\tABSTRACT:', self.data['Abstract'])
		print('\tLINK:', self.data['Link'])
		print('\tAUTHORS:', self.data['Authors'])
		print('\tDOI:', self.data['DOI'])
		print('\tDATE:', self.data['Date'])
