import sys
import database

'''
takes binfile $1 and table in hapmapdb $2 
finds either snv count in specified bin per individual (alt2) OR across all individuals (alt1)
outputs in new database (misc_hapmap) OR file
'''


def read_per_indiv(table, chr, binstart, binend, mylist):
	
	q = '''SELECT id, COUNT(*) FROM {} WHERE chr = '{}' AND pos BETWEEN {} AND {} GROUP BY(id) '''.format(table, chr, binstart, binend)
	res = db.get_item(q)

	for r in res:
		id = r[0]
		bincount = r[1] #bincount for the individual
		inp =(id, chr, binstart, binend, bincount)
		mylist.append(inp)

	return mylist



def output_inDB(table, resultlist, my2db):

	db2 = database.DB(my2db)

	#create table
	tables = db2.search_table()

	newtable = table + '_snvcount'
	if newtable not in tables:
		print('create table', newtable)
		info = ("CREATE TABLE IF NOT EXISTS {} (id TEXT, chr TEXT, start INTEGER, stop INTEGER, snvs INTEGER)".format(newtable))
		db2.create_table(info)
		indx1 = '''CREATE INDEX {}_id_start_stop_snvs ON unfilt_database (id, chr, start, stop, snvs) '''.format(newtable)
		db2.create_index_general(indx1)


	ins = '''INSERT INTO {} VALUES (?, ? , ?, ?, ?) '''.format(newtable)
	db2.insert_many_general(ins, resultlist)


def read_perbin(table, chr, binstart, binend):

	q = '''SELECT chr, pos, alt, GROUP_CONCAT(id) FROM {} WHERE chr ='{}' AND pos BETWEEN {} AND {} GROUP BY pos, alt;'''.format(table, chr, start, end)
	varq = db.get_item(q)

	bincount = len(varq)


	res =(chr, start, end, bincount)
	return res


def output_inFile(lst, file):
	output = open(file, 'w')
	for tupl in lst:
		lst = [str(i) for i in tupl]
		output.write('\t'.join(lst) + '\n')

	return 'done writing file'


#main
db = database.DB('hapmap.db')
table = str(sys.argv[2])

#read bin file to get bins to search
myres = []
for line in open(sys.argv[1]):
	line = line.split('\t')
	try: 
		chr = int(line[0])
	except:
		chr = str(line[0])
		
	start = int(line[1])
	end = int(line[2])


	#Alt 1: across ALL indiv, output in file
	out = read_perbin(table, chr, start, end)
	myres.append(out)

	#Alt 2: per individual - output in DB
#	read_per_indiv(table, chr, start, end, myres)


output_inFile(myres, table+'_snvcount.txt')
#output_inDB(table, myres, 'misc_hapmap.db')
