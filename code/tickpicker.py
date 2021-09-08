'''
	Command line interface for using tick crawler program to query known scientific databases and store that data.
	Data is either stored in a DSpace server or CSV files that can be read by humans or parsed later to retrieve the data.

	@author: Garrett Wells
	@date: 08-31-2021
'''
import os
import csv

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
from dspace import DSpace

class CrawlerApp:

	def __init__(self):
		self.control_loop()

	# print logo/title for this app and any pertinent information
	def print_header(self):
		header = 	    '          _____                    _____                    _____                    _____                    _____            _____                    _____          '\
						'\n         /\\    \\                  /\\    \\                  /\\    \\                  /\\    \\                  /\\    \\          /\\    \\                  /\\    \\         '\
						'\n        /::\\    \\                /::\\    \\                /::\\    \\                /::\\____\\                /::\\____\\        /::\\    \\                /::\\    \\        '\
						'\n       /::::\\    \\              /::::\\    \\              /::::\\    \\              /:::/    /               /:::/    /       /::::\\    \\              /::::\\    \\       '\
						'\n      /::::::\\    \\            /::::::\\    \\            /::::::\\    \\            /:::/   _/___            /:::/    /       /::::::\\    \\            /::::::\\    \\      '\
						'\n     /:::/\\:::\\    \\          /:::/\\:::\\    \\          /:::/\\:::\\    \\          /:::/   /\\    \\          /:::/    /       /:::/\\:::\\    \\          /:::/\\:::\\    \\     '\
						'\n    /:::/  \\:::\\    \\        /:::/__\\:::\\    \\        /:::/__\\:::\\    \\        /:::/   /::\\____\\        /:::/    /       /:::/__\\:::\\    \\        /:::/__\\:::\\    \\    '\
						'\n   /:::/    \\:::\\    \\      /::::\\   \\:::\\    \\      /::::\\   \\:::\\    \\      /:::/   /:::/    /       /:::/    /       /::::\\   \\:::\\    \\      /::::\\   \\:::\\    \\   '\
						'\n  /:::/    / \\:::\\    \\    /::::::\\   \\:::\\    \\    /::::::\\   \\:::\\    \\    /:::/   /:::/   _/___    /:::/    /       /::::::\\   \\:::\\    \\    /::::::\\   \\:::\\    \\  '\
						'\n /:::/    /   \\:::\\    \\  /:::/\\:::\\   \\:::\\____\\  /:::/\\:::\\   \\:::\\    \\  /:::/___/:::/   /\\    \\  /:::/    /       /:::/\\:::\\   \\:::\\    \\  /:::/\\:::\\   \\:::\\____\\ '\
						'\n/:::/____/     \\:::\\____\\/:::/  \\:::\\   \\:::|    |/:::/  \\:::\\   \\:::\\____\\|:::|   /:::/   /::\\____\\/:::/____/       /:::/__\\:::\\   \\:::\\____\\/:::/  \\:::\\   \\:::|    |'\
						'\n\\:::\\    \\      \\::/    /\\::/   |::::\\  /:::|____|\\::/    \\:::\\  /:::/    /|:::|__/:::/   /:::/    /\\:::\\    \\       \\:::\\   \\:::\\   \\::/    /\\::/   |::::\\  /:::|____|'\
						'\n \\:::\\    \\      \\/____/  \\/____|:::::\\/:::/    /  \\/____/ \\:::\\/:::/    /  \\:::\\/:::/   /:::/    /  \\:::\\    \\       \\:::\\   \\:::\\   \\/____/  \\/____|:::::\\/:::/    / '\
						'\n  \\:::\\    \\                    |:::::::::/    /            \\::::::/    /    \\::::::/   /:::/    /    \\:::\\    \\       \\:::\\   \\:::\\    \\            |:::::::::/    /  '\
						'\n   \\:::\\    \\                   |::|\\::::/    /              \\::::/    /      \\::::/___/:::/    /      \\:::\\    \\       \\:::\\   \\:::\\____\\           |::|\\::::/    /   '\
						'\n    \\:::\\    \\                  |::| \\::/____/               /:::/    /        \\:::\\__/:::/    /        \\:::\\    \\       \\:::\\   \\::/    /           |::| \\::/____/    '\
						'\n     \\:::\\    \\                 |::|  ~|                    /:::/    /          \\::::::::/    /          \\:::\\    \\       \\:::\\   \\/____/            |::|  ~|          '\
						'\n      \\:::\\    \\                |::|   |                   /:::/    /            \\::::::/    /            \\:::\\    \\       \\:::\\    \\                |::|   |          '\
						'\n       \\:::\\____\\               \\::|   |                  /:::/    /              \\::::/    /              \\:::\\____\\       \\:::\\____\\               \\::|   |          '\
						'\n        \\::/    /                \\:|   |                  \\::/    /                \\::/____/                \\::/    /        \\::/    /                \\:|   |          '\
						'\n         \\/____/                  \\|___|                   \\/____/                  ~~                       \\/____/          \\/____/                  \\|___|          '\
				 		'\nCRAWLER: a scientific database search program'\
				 		'\nby Garrett Wells for Tick Base 2021'

		print(header)

	# print menu of actions and functions supported
	def print_menu(self):
		function_list = ['run single query', 'run query batch from .csv', 'export collected data to DSpace']

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
			csv_list = os.listdir('data_dump')
			i = 0
			for csv_str in csv_list:
				print('[{}]'.format(i), csv_str)
				i = i + 1
		except:
			print('failed to find folder \'data_dump\' in the current working directory')
			return
		
		# get input to choose data file to export
		selection = input('choose CSV to export:')
		# export to dspace
		baseurl = input('site url:')
		uname = input('username:')
		passwd = input('password:')
		dspace = DSpace(username=uname, passwd=passwd, base_url=baseurl)
		dspace.import_csv(selection)
		


	# search a database using crawler by passing in the database to search and the query to run
	def search(self, db=0, q='', csv_path=''):
		print('searching database', db, 'for', q, 'or using', csv_path)
		# interface object references
		interface_list = [GScholar, IMendeley, IMendeley_Data, IFigshare, IDataDryad, IKNB, ISpringer, INeon, IPubMed, ILTER]

		# verify user choice is in list -> create instance of interface
		inter = None
		if int(db) in range(len(interface_list)):
			inter = interface_list[int(db)]()
		else:
			print('invalid db choice')
			print('\tdb =', db, '/', range(len(interface_list)))
			return

		a = None
		# gracefully exits from failure and allows continued execution
		try:
			if csv_path != '':
					a = Crawler(repository_interface=inter, csv_path=csv_path)
					a.search_all()
			
			else:
				a = Crawler(repository_interface=inter, csv_path=query)
				a.search_all()

			# export results to DSpace if desired
			selection = input('EXPORT TO DSPACE?(Y\\N):')
			if selection == 'Y' or selection == 'y' or selection == 'yes' or selection == 'Yes':
				print('exporting...')
				cid = ''

				confirmed = False
				while not confirmed:
					cid = input('enter CID:')
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
							return

				# TODO: add username and password entry
				psswd = input('pasword:')
				uname = input('username:')	
				a.export_to_dspace(cid = int(cid), uname=uname, passwd=psswd)


		except:
			print('search of', interface_list[int(db)].__name__, 'failed for an unknown reason')



	'''
		print menu to command line, take input, execute input for program
	'''
	def control_loop(self):

		function_list = [self.query_single, self.query_multiple, self.convert_csv_to_dspace]
		self.print_header()

		flag = True

		while(flag):
			# print menu
			self.print_menu()
			# get/check menu choice
			selection = input('EXECUTE: ')

			# validate input
			if selection == 'q' or selection == 'quit' or selection == 'exit':
				print('ending control loop')
				return

			elif int(selection) in range(len(function_list)):
				print('valid selection, running')
				s_code = int(selection)
				function_list[s_code]() # run selected function
			else:
				print('incoherent input: \'', selection, '\'')
				


CrawlerApp()