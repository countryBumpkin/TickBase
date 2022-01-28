'''
    @author Garrett Wells
    @date   12/31/2021
'''

import csv

csv_path = 'keywordsAll.csv'

def get_keys_in_list(csv_path='', column=2):
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        #res = list(reader)
        for row in reader:
            rows.append(row[column])
            #print('row, col=2\n\t',row[column])

        #print('\n\tROWS', rows)

    return rows

def write_list_to_csv(key_list, csv_path=''):
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in range(len(key_list)):
            print('\twriting=', key_list[i])
            writer.writerows(key_list[i])

def write_to_file(path, keyList):
    with open(path, 'w') as file:
        for key in keyList:
            file.write(key + ',\n')


# load in the keys from Reno's list
keys_ranked = get_keys_in_list(csv_path='keywordsAll.csv', column=2)
print('\nKEYS RANKED\n\t', keys_ranked[0:500])
# load keys from our unranked list
keys_unranked = get_keys_in_list(csv_path='search_keys.csv', column=0)
print('\nKEYS UNRANKED\n\t', keys_unranked)

# check all for matches
new_keys = []
count = 1
for key in keys_ranked[0:500]:
    key = key.strip().lower()
    has_match = False
    for unranked_key in keys_unranked:
        unranked_key = unranked_key.strip().lower()
        print('\tunranked key=\'{}\''.format(unranked_key), '\t\t\tkey=\'{}\''.format(key))
        if (key in unranked_key) or (key == unranked_key):
            print('\t\t\tMATCH')
            print('\t\t\tcase1 =', (key in unranked_key))
            print('\t\t\tcase2 =', (key == unranked_key))
            has_match = True

    if not has_match:
        new_keys.append(key)


print('\nNEW KEYS:\n\t', new_keys)
write_to_file('new_keys.csv', new_keys)
# output keys not known in our list to a csv
#write_list_to_csv(new_keys, csv_path='new_keys.csv')
