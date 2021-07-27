import csv
import traceback

'''
    Takes a DOI and checks against all other seen DOIs for duplicates.

    TODO: implement a file containing memory of seen DOIs to check against
'''
class doichecker:

    doi_list = []

    def __init__(self):
        self.doi_list = []

    # return true if a duplicate doi is passed in
    def duplicate(self, doi):
        duplicate = False

        # check fast access list of DOIs
        # check file
        if doi in self.doi_list or self.duplicate_in_file(doi):
            print('match found')
            duplicate = True

        self.appenddoi(doi)
        return duplicate

    # check the file for duplicate doi
    def duplicate_in_file(self, doi):
        with open('doilist.csv', 'w+') as file:
            r = csv.reader(file)

            #print("reader fieldnames =", r.fieldnames)
            try:
                for row in r:
                    if row[2] == doi:
                        print('\tmatches', doi, '==', row[2])
                        return True

                    print(row[2])
                    if row[2] != '':
                        self.doi_list.append(row[2])
            except:
                print('Failed to read rows')
                traceback.print_exc()

        return False

    # add doi to file
    def appenddoi(self, doi):
        # append to fast access list
        self.doi_list.append(doi)
        # append to file list
        with open('doilist.csv', 'w') as file:
            file.write(doi + ',\n')
