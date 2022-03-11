import sys
import json
import statistics
import database

#reads bubbles, output path, statistics of path and individuals in path (different file)
#tables in db

#load dictionary
f = open(sys.argv[1])
my_vars = json.load(f)

output = open(sys.argv[2], 'w')
#idoutput = open(sys.argv[2] + 'IDs.txt', 'w')
header = ['pathnumber', 'start', 'end', 'length', 'median', 'average']
output.write('\t'.join(header) + '\n')

#if want to see frq plot over how many has each kmer
#kmercount_out = open(sys.argv[2], 'w')
#header = ['kmer', 'indiv']
#kmercount_out.write('\t'.join(header) + '\n')


db = database.DB('/proj/nobackup/sens2017106/kristine/hapmap/hapmap.db')

#set of kmers with several connections
branches = set([])
starts =set([])


for chr in my_vars:
	#find which kmers have branches, and which are starting kmers
	connected = set([])
	for kmer in my_vars[chr]:
		if len(my_vars[chr][kmer]) > 1:

			#filter indv
			approvedkcon = 0
			for kcon in my_vars[chr][kmer]:
				if my_vars[chr][kmer][kcon] < 4:
					continue
				approvedkcon +=	1
			if approvedkcon	> 1:
				branches.add(kmer)

		ks = list(my_vars[chr][kmer].keys())
		for k1 in ks:
			connected.add(k1)

	#match
	starts = set(set(my_vars[chr].keys()).difference(connected))

	#loop through every kmer that has branch/and starts
	pathnumber = 0
	for k in branches.union(starts):

		#save the path continuing from this kmer, save id count
		for subk in my_vars[chr][k]:

			pathnumber += 1

			#connecting kmer
			j=subk

			#filtering on branching kmers and amount of individuals
			if j in branches:
				continue

			if my_vars[chr][k][j] < 4:
				continue


			#if not in above, add to path and the id
			path=[str(pathnumber), j] #k or not k starting kmer, but cannot connect in same way
			pathid = [str(pathnumber)]

			jsplit =j.split()

			#search for ids with the kmer
#			q = ''' SELECT id FROM cleanblock WHERE (chr = '{}' AND pos = '{}' AND alt='{}') INTERSECT SELECT id FROM cleanblock WHERE (chr = '{}' AND pos = '{}' AND alt='{}'); '''.format(chr, jsplit[1], jsplit[2], chr, jsplit[-2], jsplit[-1])
#			varq = db.get_item(q) #list of tuples with id 


			#add all ids to pathid
#			for res in varq:
#				if res[0] not in pathid:
#					pathid.append(res[0])


			count = [my_vars[chr][k][j]]

			#while not a branching or starting kmer look at connecting kmer
			while j not in branches and j in my_vars[chr]:


				i=list(my_vars[chr][j].keys())[0]

				if my_vars[chr][j][i] < 4:
					break

					
				count.append(my_vars[chr][j][i])

				#view = [i, str(my_vars[chr][j][i])]
				#kmercount_out.write('\t'.join(view) + '\n')


				j = i
				path.append(j)


			start = path[1]
			end = path[-1]
			amount = len(path)-1

			median = statistics.median(sorted(count))
			average = sum(count)/len(count)
			myout = [str(pathnumber), start, end, str(amount),str(median), str(average) ]

			#print(count)
			#print('\t'.join(myout))
			output.write('\t'.join(myout) + '\n')
			output.write('\t'.join(path) + '\n')
#			idoutput.write('\t'.join(pathid) + '\n')
			#print('writing output')

print('done')
