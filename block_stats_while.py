import sys
import json
import statistics

#reads bubbles, output path and statistics of path


#load dictionary
f = open(sys.argv[1])
my_vars = json.load(f)

output = open(sys.argv[2], 'w')
header = ['start', 'end', 'SVNs', 'Count']
output.write('\t'.join(header) + '\n')


#kmercount_out = open(sys.argv[2], 'w')
#header = ['kmer', 'indiv']
#kmercount_out.write('\t'.join(header) + '\n')




#set of kmers with several connections
branches = set([])
starts =set([])

#save subk and see if k in them - if not save in starts

for chr in my_vars:
	#find which kmers have branches
	connected = set([])
	for kmer in my_vars[chr]:
		if len(my_vars[chr][kmer]) > 1:
			branches.add(kmer)

		ks = list(my_vars[chr][kmer].keys())
		for k1 in ks:
			connected.add(k1)

	#match
	starts = set(set(my_vars[chr].keys()).difference(connected))

	#loop through every kmer that has branch/or all kmers
	for k in branches.union(starts):
		#save the path continuing from this kmer, save count
		for subk in my_vars[chr][k]:

			#print(my_vars[chr][k])
			#print(my_vars[chr][k][subk])

			j=subk
			if j in branches:
				continue

			if my_vars[chr][k][j] < 4:
				continue

			path=[j]
			count = [my_vars[chr][k][j]]
			while j not in branches and j in my_vars[chr]:


				i=list(my_vars[chr][j].keys())[0]
				count.append(my_vars[chr][j][i])

				#view = [i, str(my_vars[chr][j][i])]
				#kmercount_out.write('\t'.join(view) + '\n')
				
				j = i
				path.append(j)


			start = path[0]
			end = path[-1]
			amount = len(path)
			median = statistics.median(sorted(count))
			average = sum(count)/len(count)
			myout = [start, end, str(amount),str(median), str(average) ]
			#print('\t'.join(myout))
			#print(path)
			output.write('\t'.join(myout) + '\n')
			output.write('\t'.join(path) + '\n')
