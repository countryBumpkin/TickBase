#!/usr/bin/env python3

'''
	Command line interface for using tick crawler program to query known scientific databases and store that data.
	Data is either stored in a DSpace server or CSV files that can be read by humans or parsed later to retrieve the data.

	@author: Garrett Wells
	@date: 08-31-2021
'''
import os
import csv
import getpass

from crawler import Crawler
from gscholar_interface import GScholar
from mendeley_interface import IMendeley
from mendeleydata_interface import IMendeley_Data
from figshare_interface import IFigshare
from datadryad_interface import IDataDryad
#from mendeley import Mendeley
from knb_interface import IKNB
from springer_interface import ISpringer
from neon_interface import INeon
from pubmed_interface import IPubMed
from lter_interface import ILTER
# data structures, data verification, and external object interfaces
from briefcase import Briefcase
from doichecker import doichecker
from dspace7 import DSpace

class CrawlerApp:

	# login credentials for DSpace
	logged_in = False
	login_cred = ()
	uname = ''
	psswd = ''
	cid = ''


	# DSpace session stored from previous login
	dsession = None

	def __init__(self):
		dsession = None
		self.logged_in = False
		self.control_loop()

	# print logo/title for this app and any pertinent information
	def print_header(self):
		self.clear_screen()

		header = 	    "_________                         .__                  \n"\
						"\_   ___ \_______ _____  __  _  __|  |   ____   ______  \n"\
						"/    \  \/\_  __ \__   \ \ \/ \/ /|  |  / __ \_  __   \ \n"\
						"\     \____|  | \/ / __ \_\     / |  |__\  ___/ |  | \/ \n"\
						" \______  /|__|   (____  / \/\_/  |____/ \___  >|__|    \n"\
						"        \/             \/                    \/         \n"\
				 		'\nCRAWLER: a scientific database search program'\
				 		'\nby Garrett Wells for Tick Base 2021'

		print(header)

	# clear screen with newline characters
	def clear_screen(self):
		tsize = os.get_terminal_size()
		print(tsize)

		for i in range(0, tsize[1]):
			print('\n')

	# print menu of actions and functions supported
	def print_menu(self):
		function_list = ['exit', 'run single query', 'run query batch from .csv', 'export collected data to DSpace', 'manage collection']

		print('MENU')

		i = 0
		for fun_str in function_list:
			print('[{}]\t{}'.format(i, fun_str))
			i = i + 1


	# print an indexed list of all databases we support querying
	def print_database_menu(self):
		db_list = ['Google Scholar', 'Mendeley', 'Mendeley Data', 'Figshare', 'Data Dryad', 'KNB', 'Springer Nature', 'Neon', 'PubMed', 'LTER']
		
		print('DATABASES')

		i = 0
		for db_str in db_list:
			print('[{}]\t{}'.format(i, db_str))
			i = i + 1

	# log in to DSpace if not logged in already
	def _login(self):
		# login/authenticate
		uname, psswd, baseurl = self._get_login_credentials()
		try:
			self.dsession = DSpace(username=uname, passwd=psswd, base_url=baseurl) 
			self.dsession.authenticate()
			self.logged_in = True
		except:
			print('FAILED TO LOGIN')
			return

	# get a collection id from the user
	def _get_cid(self):
		cid = ''

		# get collection id
		confirmed = False
		while not confirmed:
			cid = self._print_cids()
			print('CID Entered =', cid)
			confirmation = input('confirm CID as correct?(Y\\N):')
			if confirmation == 'Y' or confirmation == 'y' or confirmation == 'yes' or confirmation == 'Yes':
				confirmed = True

			else:
				retry = input('try again?(Y\\N):')
				if retry != 'Y' or retry != 'y' or retry != 'yes' or retry != 'Yes':
					print('proceeding...')
				else:
					print('canceling operation.')
					return None

		return cid

	# print the CIDs that are available on the DSpace server and allow user to choose one
	# which is then returned
	def _print_cids(self):
		if self.dsession == None or not self.logged_in:
			self._login()

		# print menu of collections available to modify
		print("CHOOSE COLLECTION TO EDIT")
		cid = ''
		collections = self.dsession.get_collections(False) # set debug flag to false
		#print(collections)
		i = 0
		for collection in collections:
			print('[{}] {}: {}'.format(i, collection['name'], collection['uuid']))

		selection = int(input('SELECT COLLECTION: '))
		if selection in range(0, len(collections)):
			cid = collections[selection]['uuid']

		return cid


	# get base url, username, password and return as a tuple
	def _get_login_credentials(self):
		self.clear_screen()

		# tell user what these credentials are for
		print('ENTER LOGIN CREDENTIALS FOR DSPACE')
		print('username: john.doe@gmail.com\npassword: john_is_not_a_doe\n')

		uname = ''
		psswd = ''
		baseurl = ''

		# add username and password entry
		confirmed = False
		while not confirmed:
			uname = input('username: ')
			passwd = getpass.getpass(prompt='password: ', stream=None) 

			confirmation = input('confirm username and password as correct?(Y\\N):')
			if confirmation == 'Y' or confirmation == 'y' or confirmation == 'yes' or confirmation == 'Yes':
				confirmed = True

			else:
				retry = input('try again?(Y\\N):')
				if retry != 'Y' or retry != 'y' or retry != 'yes' or retry != 'Yes':
					print('proceeding...')
				else:
					print('canceling operation.')
					return None

		# Check if base url needs to change and change it if needed
		print('BASE URL:', baseurl)
		selection = input('Change base DSpace URL?(Y/N):')
		if selection == 'Y' or selection == 'y' or selection == 'yes' or selection == 'Yes':
				confirmed = False 

		while not confirmed:
			baseurl = input('Change base DSpace URL?(Y/N)')

			confirmation = input('confirm username and password as correct?(Y\\N):')
			if confirmation == 'Y' or confirmation == 'y' or confirmation == 'yes' or confirmation == 'Yes':
				confirmed = True

			else:
				retry = input('try again?(Y\\N):')
				if retry != 'Y' or retry != 'y' or retry != 'yes' or retry != 'Yes':
					print('proceeding...')
				else:
					print('canceling operation.')
					return None

		self.uname = uname
		self.psswd = passwd
		self.login_cred = (uname, passwd, baseurl)

		return self.login_cred

		# clear to signify end of process
		self.clear_screen()

	# control loop for managing data already in a collection
	def manage_collection(self):

		self.clear_screen()
		# login/authenticate
		if not self.logged_in:
			self._login()

		# have user choose a CID to work with
		cid = self._get_cid()

		menu = ['empty collection', 'print collection summary', 'get collection contents']

		i = 0
		for item in menu:
			print('[', i, '] ', item, sep='')
			i = i + 1

		selection = input("EXECUTE:")
		selection = int(selection)

		if selection in range(0, len(menu)):
	
			if selection == 0:
				print('EMPTYING COLLECTION')
				self.dsession.empty_collection(cid)

			elif selection == 1:
				print('not implemented yet')

			elif selection == 2:
				print('not implemented yet')



	# submit single keyword query to database
	def query_single(self):
		print('running single query')
		query = input('enter keyword for search: ')
		# print list of databases
		self.print_database_menu()
		database = input('select database to search: ')
		# run search
		self.search(db=int(database), q=query)

	# submit search csv to database to query
	def query_multiple(self):
		print('running multiple query')
		# print menu of known .csv files
		filename = ''

		try:
			i = 0
			csv_file_list = os.listdir('searches')
			if csv_file_list == []:
				print('OUTPUT: no search option, but \'searches\' folder present, try creating CSV of search terms in that folder')
				return

			for file in csv_file_list:
				print('[{}] {}'.format(i, file))
				i = i + 1

			choice = input('choose CSV search file: ')
			filename = 'searches/' + csv_file_list[int(choice)]

		except:
			print('OUTPUT: no directory of search CSV files currently, try making \'searches\' folder with csv of query terms')
			return

		# choose database
		self.print_database_menu()
		choice = input('choose database: ')
		self.search(db=choice, csv_path=filename)

	# parse a csv file and upload to dspace
	def convert_csv_to_dspace(self):
		# print list of possible .csv data files to export
		print('CONVERTABLE CSVs:')
		csv_list = []
		try:
			print('[0] upload all CSVs')
			csv_list = os.listdir('../data_dump')
			i = 1
			for csv_str in csv_list:
				print('[{}]'.format(i), csv_str)
				i = i + 1
		except:
			print('failed to find folder \'data_dump\' in the current working directory')
			return
		
		# get input to choose data file to export
		selection = int(input('choose CSV to export:'))

		# export to dspace
		if not self.logged_in:
			self._login()

		# have user choose collection ID to use
		self.dsession.get_collections()
		cid = self._get_cid()

		

		if selection == 0:
			for csv in csv_list:
				case = self.dsession.export_to_Briefcase("data_dump/" + csv)
				case.export_to_dspace(cid=cid, dspace=self.dsession)

		else:		
			case = self.dsession.export_to_Briefcase("data_dump/" + csv_list[selection-1])
			case.export_to_dspace(cid=cid, dspace=self.dsession)

		# clear screen to signify end of process
		self.clear_screen()

	# update system doi checker with all known item DOIs from a collection
	def update_doi_checker(self, cid=''):
		# login to DSpace
		if not self.logged_in:
			self._login()

		# get list of item UUIDs in DSpace collection
		item_list = self.dsession.get_items(cid, False)
		print(item_list)

		# parse DOIs from items
		doi_list = []
		for item in item_list:
			# get doi from each item and place in a list
			# TODO fix get_item_metadata
			meta = self.dsession.get_item_metadata(item)
			if 'dc.metadata.other' in meta.keys():
				tmp = (meta['dc.identifier.other'])[0]
				doi = tmp['value']	
				doi_list.append(doi)
				print('\t', doi)

		dchecker = doichecker()
		dchecker.create_inheritance(doi_list)

	# search a database using crawler by passing in the database to search and the query to run
	def search(self, db=0, q='', csv_path=''):
		export_toDSpace = False
		uname = ''
		psswd = '' 
		baseurl = ''

		# export results to DSpace if desired
		selection = input('EXPORT TO DSPACE?(Y\\N):')
		if selection == 'Y' or selection == 'y' or selection == 'yes' or selection == 'Yes':
			export_toDSpace = True
			# if exporting results to dspace, make sure there are no DOI duplicates in DSpace by updating DOI checker
			cid = ''
			print('WARNING: If adding results to pre-existing collection in DSpace it is wise to update DOI database on machine to prevent duplicates in DSpace.')
			ans = input('Update DOI database?(Y/N):')
			if ans == 'Y' or ans == 'y' or ans == 'yes' or ans == 'Yes':
				cid = self._get_cid() # user enter cid
				self.update_doi_checker(cid) # create file with all DOIs

			# ensure user logged in
			if not self.logged_in:
				self._login()
				if cid == '': # make sure cid is defined
					cid = self._get_cid()

		#print('searching database', db, 'for', q, 'or using', csv_path)
		# interface object references
		interface_list = [GScholar, IMendeley, IMendeley_Data, IFigshare, IDataDryad, IKNB, ISpringer, INeon, IPubMed, ILTER]

		# verify user choice is in list -> create instance of interface
		inter = None
		if int(db) in range(len(interface_list)):
			inter = interface_list[int(db)]()
		else:
			#print('invalid db choice')
			print('\tdb =', db, '/', range(len(interface_list)))
			return

		a = None
		# gracefully exits from failure and allows continued execution
		#try:
		if csv_path != '':
			a = Crawler(repository_interface=inter, csv_path=csv_path)
			a.search_all()
		
		else:
			a = Crawler(repository_interface=inter, csv_path='')
			a.search(keywords=[[q]])
		
		# export to DSpace if flag is set
		if export_toDSpace and self.logged_in:
			a.export_to_dspace(cid=cid, uname=self.uname, passwd=self.psswd)
		elif export_toDSpace:
			a.export_to_dspace(cid=cid, uname=login_cred[0], passwd=login_cred[1])

		# clear screen to signify end of process
		self.clear_screen()



	'''
		print menu to command line, take input, execute input for program
	'''
	def control_loop(self):

		function_list = [self.query_single, self.query_multiple, self.convert_csv_to_dspace, self.manage_collection]
		self.print_header()

		flag = True

		while(flag):
			# print menu
			self.print_header()
			self.print_menu()
			# get/check menu choice
			selection = input('EXECUTE: ')

			# validate input
			if selection == '0' or selection == 'q' or selection == 'quit' or selection == 'exit':
				print('Goodbye!')
				return

			elif int(selection) in range(len(function_list) + 1):
				#print('valid selection, running')
				s_code = int(selection) - 1 # offset by one because first option is exit...
				function_list[s_code]() # run selected function
			else:
				print('incoherent input: \'', selection, '\'')
				


CrawlerApp()
