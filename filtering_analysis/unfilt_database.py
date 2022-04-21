import sys
import database

#read bins


db = database.DB('hapmap.db')


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

	q = '''SELECT id, COUNT(*) FROM haploblock WHERE chr = '{}' AND pos BETWEEN {} AND {} GROUP BY(id) '''.format(chr, start, end)
	varq = db.get_item(q)

	for r in varq:
		id = r[0]
		bincount = r[1]

		res =(id, chr, start, end, bincount)

		myres.append(res)


db2 = database.DB('misc_hapmap.db')

#create table
tables = db2.search_table()

if 'unfilt_database' not in tables:
	print('create table')
	info = ("CREATE TABLE IF NOT EXISTS unfilt_database (id TEXT, chr TEXT, start INTEGER, stop INTEGER, snvs INTEGER)")
	db2.create_table(info)
	indx1 = '''CREATE INDEX unfilt_db_id_start_stop_snvs ON unfilt_database (id, chr, start, stop, snvs) '''
	db2.create_index_general(indx1)


ins = '''INSERT INTO unfilt_database VALUES (?, ? , ?, ?, ?) '''
db2.insert_many_general(ins, myres)


