import sys
import gzip as gz
import database
import pysam
#module load bioinfo-tools pysam

#vcf to read
f = pysam.TabixFile(sys.argv[1])

def fetch_region(chr, s, e):
	reads = f.fetch(chr, s, e)

	count = 0
	for read in reads:
		count += 1

	return count


#create database 

db = database.DB('misc_hapmap.db')

#create table
tables = db.search_table()

if 'unfiltered_snvs' not in tables:
	info = ("CREATE TABLE IF NOT EXISTS unfiltered_snvs (id TEXT, chr TEXT, start INTEGER, stop INTEGER, snvs INTEGER)")
	db.create_table(info)
	indx1 = '''CREATE INDEX id_start_stop_snvs ON unfiltered_snvs (id, chr, start, stop, snvs) '''
	db.create_index_general(indx1)

id = sys.argv[1].split('/')[7]
print(id)
bin = []

#read bin file to get bins to search
myres = []
for line in open(sys.argv[2]):
	line = line.split('\t')
	try: 
		chr = int(line[0])
	except:
		chr = str(line[0])
		
	start = int(line[1])
	end = int(line[2])
	bincount = fetch_region(chr, start, end)	
	res =(id, chr, start, end, bincount)
	myres.append(res)

ins = '''INSERT INTO unfiltered_snvs VALUES (?, ? , ?, ?, ?) '''
db.insert_many_general(ins, myres)


