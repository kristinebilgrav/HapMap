
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

if chr == 'Y' or chr == 'X':
#	for id in ids:
#
#
#
#		if id in cluster0 = skip
#		else: 
#

query2 = []
loop =[]
for id in ids:
	print(id)
	for GT in ["1|0","0|1" ]:
		qstart = time.time()
		q = '''SELECT chr, GROUP_CONCAT(pos, ';'), GROUP_CONCAT(alt, ';') FROM haploblock WHERE (GT= '{}' OR GT = '1|1') AND chr = '{}' AND  id = '{}' GROUP BY PS HAVING COUNT(pos) >=3;  '''.format(GT , chr, id)
		myq = db.get_item(q) #tuple
		query2.append(time.time() - qstart)

		count = 0
		for res in myq:
			count += 1
			if count > 20:
				print(sum(query2) )
				print(sum(query2)/count )
				print(sum(loop))
				print(sum(loop)/count)
				quit()

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
