import sys
import database

db = database.DB('/proj/nobackup/sens2017106/kristine/hapmap/hapmap.db')

print('filtering db')

chr_of_interest = list(range(1, 23))
chr_of_interest.append('X')
chr_of_interest.append('Y')

tables = db.search_table()
print(tables)
#create table
if 'cleanblock' not in tables:
	info = ("CREATE TABLE IF NOT EXISTS cleanblock (id TEXT, chr TEXT, pos INTEGER, alt TEXT, GT TEXT, PS INTEGER)")
	db.create_table(info)
	indx1 = '''CREATE INDEX clean_phaseset ON cleanblock (PS, chr, pos, alt, id) '''
	db.create_index_general(indx1)
	indx2 = '''CREATE INDEX clean_id_chr_pos_alt_PS ON cleanblock (id, chr, pos, alt, PS) '''
	db.create_index_general(indx2)

for chr in chr_of_interest:
	chr = str(chr)
	q = '''SELECT * FROM haploblock WHERE chr = '{}'  '''.format(chr)
	SNPq = db.get_item(q)

	SNP_dict = {}
	SNP_dict[chr] = {}
	for res in SNPq:
		SNP = '''{} {}'''.format(res[2], res[3])

		if SNP not in SNP_dict[chr]:
			SNP_dict[chr][SNP] = []
		SNP_dict[chr][SNP].append(res)

	print(chr, 'graph done')

	keepvars= []
	for snp in SNP_dict[chr]:
		if len(SNP_dict[chr][snp]) > 5:
			for var in SNP_dict[chr][snp]:
				keepvars.append(var)


	#insert into table

	ins = '''INSERT INTO cleanblock VALUES (?, ? , ?, ?, ?, ?) '''
	db.insert_many_general(ins, keepvars)


print('done')
