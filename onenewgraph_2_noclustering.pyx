import sys
import json
import database
import time

#connect db
def main(str chr):
	db = database.DB('/proj/nobackup/sens2017106/kristine/hapmap/hapmap.db')

	start = time.time()
	cdef str idq = '''SELECT DISTINCT id FROM cleanblock ;  '''

	cdef list ids= []
	cdef tuple id_tuple

	for id_tuple in db.get_item(idq):
		ids.append(id_tuple[0])

	cdef dict master_dict = {}
	cdef list kcon_time = []

	if chr not in master_dict:
		master_dict[chr] = {}

	cdef list query2 = []
	cdef list loop = []

	cdef str GT

	cdef str kmer_a
	cdef str kmer_b

	cdef int i
	cdef int j
	cdef int k

	cdef list pos
	cdef list alt
	cdef str id

	for id in ids:
		print(id)
		for GT in ["1|0","0|1" ]:
			qstart = time.time()
			q = '''SELECT chr, GROUP_CONCAT(pos, ';'), GROUP_CONCAT(alt, ';') FROM cleanblock WHERE (GT= '{}' OR GT = '1|1') AND chr = '{}' AND  id = '{}' GROUP BY PS HAVING COUNT(pos) >=3;  '''.format(GT , chr, id)
			myq = db.get_item(q) #tuple
			query2.append( time.time() - qstart)
			for res in myq:
	
				pos = res[1].split(';')
				alt = res[2].split(';')
				loop2start = time.time()
				for i in range(0, len(pos) - 2 ):
					j = i+1
					k = j+1

					kmer_a="{} {} {} {} {} {}".format(chr, pos[i], alt[i], chr , pos[j], alt[j])
					kmer_b="{} {} {} {} {} {}".format(chr, pos[j], alt[j], chr , pos[k], alt[k])
					
					kmerstart = time.time()
					if not kmer_a in master_dict[chr]:
						master_dict[chr][kmer_a] = {}
	
					if not kmer_b in master_dict[chr][kmer_a]:
						master_dict[chr][kmer_a][kmer_b] = 0

					master_dict[chr][kmer_a][kmer_b] +=1			
					kcon_time.append(time.time()-kmerstart)

				loopend = time.time() - loop2start
				loop.append(loopend)
			
			#print(kcon_time)
		#print(master_dict)
	f = open(chr + '_graph.json', 'w')
	json.dump(master_dict, f)
	f.close()
	quit()
