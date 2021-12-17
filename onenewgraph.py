import sys
import json
import database
import time

#connect db
db = database.DB('/proj/nobackup/sens2017106/kristine/hapmap/hapmap.db')

#chr_of_interest = list(range(1, 23))
#chr_of_interest.append('X')
#chr_of_interest.append('Y')

start = time.time()
idq = '''SELECT DISTINCT id FROM haploblock ;  '''
ids = [id[0] for id in db.get_item(idq)] #list with ids

#print('unique id q ',time.time() - start)

master_dict = {}

kcon_time = []

chr = sys.argv[1]
if chr not in master_dict:
	master_dict[chr] = {}

for id in ids:
	print(id)
	for GT in ["1|0","0|1" ]:
		qstart = time.time()
		q = '''SELECT chr, GROUP_CONCAT(pos, ';'), GROUP_CONCAT(alt, ';') FROM haploblock WHERE (GT= '{}' OR GT = '1|1') AND chr = '{}' AND  id = '{}' GROUP BY PS HAVING COUNT(pos) >=3;  '''.format(GT , chr, id)
		myq = db.get_item(q) #tuple
		#print('query 2', time.time() - qstart)

		for res in myq:
			pos = res[1].split(';')
			alt = res[2].split(';')
			for i in range(0, len(pos) - 1 ):
				j = i+1
				kmer_list = [chr, pos[i], alt[i], chr , pos[j], alt[j]]
				kmer = ' ' .join([str(k) for k in kmer_list])

				kmerstart = time.time()
				if kmer not in master_dict[chr]:
					master_dict[chr][kmer] = {}

				k0_list = kmer_list[0:3]
				k0 = ' '.join([str(k) for k in k0_list])
				connecting = [k for k in master_dict[chr] if k0 in k and kmer != k]
				#print(kmer, connecting)

				for kcon in connecting:
					if kmer not in master_dict[chr][kcon]:
						master_dict[chr][kcon][kmer] = 0
					master_dict[chr][kcon][kmer] += 1

			

				kcon_time.append(time.time()-kmerstart)

			#print(kcon_time)
		#print(master_dict)
f = open(chr + '_graph.json', 'w')
json.dump(master_dict, f)
f.close()
quit()
