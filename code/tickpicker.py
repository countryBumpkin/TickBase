'''
	Command line interface for using tick crawler program to query known scientific databases and store that data.
	Data is either stored in a DSpace server or CSV files that can be read by humans or parsed later to retrieve the data.

	@author: Garrett Wells
	@date: 08-31-2021
'''
import os

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

# print menu of actions and functions supported
def print_menu():
	menu_str = 	'''
	MENU
		[0] run single query
		[1] run query batch from .csv
		[2] export collected data to DSpace
	'''

	print(menu_str)

# print an indexed list of all databases we support querying
def print_database_menu():
	menu_str = '''
	DATABASES
		[0]  Google Scholar
		[1]  Mendeley
		[2]  Mendeley Data
		[3]  Figshare
		[4]  Data Dryad
		[5]  KNB
		[6]  Springer Nature
		[7]  Neon
		[8]  PubMed
		[9] LTER
	'''
	print(menu_str)


# search a database using crawler by passing in the database to search and the query to run
def search(db=0, q='', csv_path=''):

	inter = None

	if db == 0: # google scholar
		inter = GScholar()

	elif db == 1: # mendeley
		inter = IMendely()

	elif db == 2: # mendeley data
		inter = IMendeley_Data()

	elif db == 3: # figshare
		inter = IFigshare()

	elif db == 4: # data dryad
		inter = IDataDryad()

	elif db == 5: # knb
		inter = IKNB()

	elif db == 6: # springer nature
		inter = ISpringer()

	elif db == 7: # neon
		inter = INeon()

	elif db == 8: # pubmed
		inter = IPubMed()

	elif db == 9: # LTER
		inter = ILTER()

	else:
		return

	if csv_path != '':
		print('search1')
		a = Crawler(repository_interface=inter, csv_path=csv_path)
		a.search_all()

	else:
		print('search2')
		a = Crawler(repository_interface=inter, csv_path=query)
		a.search_all()


'''
	print menu to command line, take input, execute input for program
'''
def control_loop():
	flag = True

	while(flag):
		# print menu
		print_menu()
		# get/check menu choice
		selection = input('EXECUTE: ')

		# validate input
		if selection == 'q' or selection == 'quit' or selection == 'exit':
			print('ending control loop')
			return

		elif int(selection) in range(10):
			s_code = int(selection)

			# execute chosen option
			if s_code == 0: # run single query
				query = input('enter keyword for search: ')
				# print list of databases
				print_database_menu()
				database = input('select database to search: ')
				# run search
				search(db=database, q=query)

			elif s_code == 1: # run batch of queries
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
				print_database_menu()
				choice = input('choose database: ')
				search(db=choice, csv_path=filename)


			elif s_code == 2: # export pre-collected data to dspace
				print('implement option 2')
				# TODO: print list of possible .csv data files to export
				# TODO: get input to choose data file to export
				# TODO: read file and export to dspace!!!

control_loop()