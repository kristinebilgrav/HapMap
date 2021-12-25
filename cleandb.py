import sys
import database

db = database.DB('/proj/nobackup/sens2017106/kristine/hapmap/hapmap.db')

chr = str(sys.argv[1])
q = '''SELECT pos, alt FROM haploblock WHERE chr = '{}'  '''.format(chr)
SVq = db.get_item(q)

SV_dict = {}
SV_dict[chr] = {}
for res in SVq:
	SV = '''{} {}'''.format(res[0], res[1])
	if SV not in SV_dict[chr]:
		SV_dict[chr][SV] = 0
	SV_dict[chr][SV] += 1

keepvars= []
for chr in SV_dict:
	for sv in SV_dict[chr]:
		if SV_dict[chr][sv] < 5:
			continue
		else:
			sv = sv.split()
			keep = '''SELECT * FROM haploblock WHERE chr = '{}' AND pos = '{}' AND alt= '{}' '''.format(chr, sv[0], sv[1])
			keepq = db.get_item(keep)
			for k in keepq:
				keepvars.append(k)
#print(keepvars)

#insert into table

#create table
tables = db.search_table()

if 'cleanblock' not in tables:
	info = ("CREATE TABLE IF NOT EXISTS cleanblock (id TEXT, chr TEXT, pos INTEGER, alt TEXT, GT TEXT, PS INTEGER)")
	db.create_table(info)
else:
	db.drop_index_general('DROP INDEX clean_id_chr_pos_alt_PS')
	db.drop_index_general('DROP INDEX clean_phaseset')

ins = '''INSERT INTO cleanblock VALUES (?, ? , ?, ?, ?, ?) '''
db.insert_many_general(ins, keepvars)

indx1 = '''CREATE INDEX clean_phaseset ON cleanblock (PS, chr, pos, alt, id) '''
db.create_index_general(indx1)
indx2 = '''CREATE INDEX clean_id_chr_pos_alt_PS ON cleanblock (id, chr, pos, alt, PS) '''
db.create_index_general(indx2)


