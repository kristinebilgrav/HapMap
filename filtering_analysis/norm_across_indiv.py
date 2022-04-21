import database
import statistics
import sys

'''
find median snvs in individual across a chr. create score above/below
'''
db = database.DB('misc_hapmap.db')

table = 'connectedA'
newtable  = 'connectedA_norm'

#for each chr in an indiv find median
data_dict = {}
newins = []
q = ''' SELECT chr, GROUP_CONCAT(start), GROUP_CONCAT(stop), GROUP_CONCAT(snvs) FROM {} GROUP BY chr ;'''.format(table)
for res in db.query(q):
    allsnvs = [int(i) for i in res[-1].split(',')]
    start = [j for j in res[1].split(',')]
    stop = [j for j in res[2].split(',')]
    median = statistics.median(allsnvs)
    mymin = min(allsnvs)
    mymax = max(allsnvs)
#    if res[0] not in data_dict:
#        data_dict[res[0]] = {}
#        data_dict[res[0]][res[1]]=
    for v in range(0, len(allsnvs)-1):
        vnorm = (allsnvs[v]-mymin)/(mymax-mymin)
        newcount = (res[0], start[v], stop[v], vnorm)
        newins.append(newcount)

tables = db.search_table()
prefix = 'connectedA_norm'
if newtable not in tables:
    info = ("CREATE TABLE IF NOT EXISTS {} ( chr TEXT, start INTEGER, stop INTEGER, snvs FLOAT)".format(newtable))
    db.create_table(info)
    indx1 = '''CREATE INDEX {}_id_start_stop_snvs ON {} ( chr, start, stop, snvs) '''.format(prefix, newtable)
    db.create_index_general(indx1)

ins = '''INSERT INTO {} VALUES ( ?, ?, ?, ?) '''.format(newtable)
db.insert_many_general(ins, newins)
