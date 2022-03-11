import sys
import database

db = database.DB('/proj/nobackup/sens2017106/kristine/hapmap/hapmap.db')


chr_of_interest = list(range(1, 23))
chr_of_interest.append('X')
chr_of_interest.append('Y')

for chr in chr_of_interest:
	chr = str(chr)
	q = '''SELECT pos, alt FROM haploblock WHERE chr = '{}'  '''.format(chr)
	SNPq = db.get_item(q)

	SNP_dict = {}
	SNP_dict[chr] = {}
	for res in SNPq:
		SNP = '''{} {}'''.format(res[0], res[1])
		if SNP not in SNP_dict[chr]:
			SNP_dict[chr][SNP] = 0
		SNP_dict[chr][SNP] += 1

keepvars= []
for chr in SNP_dict:
	for snp in SNP_dict[chr]:
		if SNP_dict[chr][snp] < 5:
			continue
		else:
			snp = snp.split() 
			keep = '''SELECT * FROM haploblock WHERE chr = '{}' AND pos = '{}' AND alt= '{}' '''.format(chr, snp[0], snp[1])
			keepq = db.get_item(keep)
			for k in keepq:
				keepvars.append(k)
				print(keepvars)
				quit()

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


