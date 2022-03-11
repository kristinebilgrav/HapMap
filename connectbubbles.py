
import sys

#create database
#input all info in tables
#get unique path numbers with starts and ends
#query 

def read_stats_line(line, info_dict, start_dict, end_dict ):
	
	#save pathnumber
	pathnumber = line.split('\t')[0]
	info_dict[pathnumber] = []

	#start of starting-kmer
	start1 = line.split('\t')[1].split()[1:3]
	start = ' '.join(start1)
	if start not in start_dict:
		start_dict[start] =[]
	start_dict[start].append(pathnumber)

	#end of ending kmer
	end1 = line.split('\t')[2].split()[-2:]
	end = ' '.join(end1)
	if end not in end_dict:
		end_dict[end] = []
	end_dict[end].append(pathnumber)

	info_dict[pathnumber].append(start)
	info_dict[pathnumber].append(end)

	#adding stats to dictionary
	length = line.split('\t')[3]
	median = line.split('\t')[4]
	average = line.rstrip('\n').split('\t')[-1]
	
	info_dict[pathnumber].append(length)
	info_dict[pathnumber].append(median)
	info_dict[pathnumber].append(average)

	return info_dict, start_dict, end_dict


def make_connections(startnumber, endnumber, lists_to_connect):
	##  explain ##
	for c in lists_to_connect:
		if endnumber in c:
			indx = c.index(endnumber)
			new_connection = c[:indx+1]
			new_connection.append(startnumber)
			lists_to_connect.append(new_connection)
			return lists_to_connect


number_to_info = {}
starts = {}
ends = {}
full_paths = {}

count = 0 
#add all starts and end to respective dictonaries
for line in open(sys.argv[1]):
	if line.startswith('pathid'):
		continue

	count += 1
	#path stats lines
	if count % 2 == 0:
		read_stats_line(line, number_to_info, starts, ends)


	else:
		pathnumber = line.split('\t')[0]
		path = line.rstrip('\n').split('\t')[1:]
		full_paths[pathnumber] = path



to_connect = []

startSet = set(starts)
endSet = set(ends)

already_connected = set([])
for s in startSet.intersection(endSet):
	#print('starts', starts[s])
	#print('ends', ends[s])

	for e in ends[s]:
		if e in already_connected:
			for st in starts[s]:
				make_connections(st, e, to_connect)
				already_connected.add(st)
				

		for i in range(0, len(starts[s])):
			newlist =[e]
			newlist.append(starts[s][i])
			to_connect.append(newlist)
			already_connected.add(e)
			already_connected.add(starts[s][i])


#def do_stats():


longest = 0
allnewlengths= []
allsnps= []
for connecting in to_connect:
	newsnplength = 0
	newaverage = 0
	if len(connecting) > longest:
		longest = len(connecting)

	#find sequence length of new contigs
	cstart = int(number_to_info[connecting[0]][0].split()[0]) #find start using pathnumber
	cend = int(number_to_info[connecting[-1]][1].split()[0]) 
	seqlength = cend-cstart

	if seqlength < 0:
		print('negative')
		sequence = []
#		for c in connecting:
			
#			print(number_to_info[c])

	newpath = []
	for k in connecting:
		newsnplength += float(number_to_info[k][-3])*2
		newaverage +=  float(number_to_info[k][-1])

		newpath += full_paths[k]

#	print(newpath)
	allsnps.append(newsnplength)

#	print(newlength, newaverage)
#	if newaverage < 15:
#		continue

	allnewlengths.append(seqlength)


#print(sorted(allnewlengths))
#print(len(allnewlengths))
print(sorted(allsnps))
#print('most to connect', longest)




chr15len = 102531392
half = chr15len/2

uptohalf = 0
numberstohalf = []
for contig in reversed(sorted(allnewlengths)):
	if uptohalf < half:
		uptohalf += int(contig)
		numberstohalf.append(contig)

	else: 
		n50 = contig
		print('n50 bp', n50)
		print('n50 kb', n50/1000)
		print(half)
		#print(numberstohalf)
		l50 = len(numberstohalf)
		print('l50',l50)
		quit()



print('uptohalf', uptohalf)
