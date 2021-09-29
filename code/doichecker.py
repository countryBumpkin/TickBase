import csv
import traceback

'''
    Takes a DOI and checks against all other seen DOIs for duplicates.
'''
class doichecker:

    doi_list = []

    def __init__(self):
        self.doi_list = []
        try:
            file = open('doilist.csv', 'x')
            file.close()
        except:
            print('doi csv list file already exists')

    # If running from a different machine without access to the master key of seen DOIs, supplement with list of database contents
    def create_inheritance(self, doi_list):
        for doi in doi_list:
            # make sure doi not already known to prevent database bloat
            if not self.duplicate(doi):
                self.appenddoi(doi)

    # return true if a duplicate doi is passed in
    def duplicate(self, doi):
        duplicate = False

        # check fast access list of DOIs (self.doi_list)
        # check inherited file of all previously seen DOIs
        if doi in self.doi_list:
            print('match found in fast access list')
            duplicate = True
        else:
            self.appenddoi(doi, target=0)

        if self.duplicate_in_file(doi):
            print('match found in file')
            duplicate = True
        else:
            self.appenddoi(doi, target=1)

        return duplicate

    # check the hereditary file in working directory for duplicate doi
    def duplicate_in_file(self, doi):
        with open('doilist.csv', 'r') as file:
            r = csv.reader(file)

            #print("reader fieldnames =", r.fieldnames)
            try:
                # iterate over DOIs in file and check against questionable DOI
                for row in r:
                    if row[0] == doi:
                        print('\tmatches', doi, '==', row[0])
                        return True
                    else:
                        print('\t', row[0], ' doesn\'t match', doi)

                    print(row[0])
                    # append doi to end of file
                    if row[0] != '':
                        self.doi_list.append(row[0], target=1)
            except:
                print('Failed to read rows')
                traceback.print_exc()

        file.close()
        return False

    # add doi to file
    def appenddoi(self, doi, target=0):
        # append to fast access list
        if target = 0:
            self.doi_list.append(doi)

        else:
            # append to file list
            print('appending to csv list file')
            with open('doilist.csv', 'a') as file:
                file.write(doi + ',\n')
            file.close()
