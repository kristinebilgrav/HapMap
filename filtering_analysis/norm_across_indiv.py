import database

'''
find median snvs in individual across a chr. create score above/below
'''
db = database.DB('misc_hapmap.db')

table = 'unfiltered_snvs'

#for each chr in an indiv find median
data_dict = {}
q = ''' SELECT id, chr, GROUP_CONCAT(snvs) FROM {} GROUP BY id AND chr ;'''.format(table)
for res in db.query(q):
    print(res)
    if res[0] not in data_dict:
        data_dict[res[0]] = {}
    if res[1] not in data_dict[res[0]]:
        data_dict[res[0]][res[1]] = res[1:]
    print(data_dict)
    quit()
