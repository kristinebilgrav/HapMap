
import sys

def read_stats_line(line, info_dict, start_dict, end_dict ):
	
	#save pathnumber
	pathnumber = line.split('\t')[0]
	info_dict[pathnumber] = []

	#start of starting-kmer
	fullstart = line.split('\t')[1]
	start1 = line.split('\t')[1].split()[1:3]
	start = ' '.join(start1)
	if start not in start_dict:
		start_dict[start] =[]
	start_dict[start].append(pathnumber)

	#end of ending kmer
	fullend = line.split('\t')[2]
	end1 = line.split('\t')[2].split()[-2:]
	end = ' '.join(end1)
	if end not in end_dict:
		end_dict[end] = []
	end_dict[end].append(pathnumber)

	info_dict[pathnumber].append(fullstart)
	info_dict[pathnumber].append(fullend)

	#adding stats to dictionary
	length = line.split('\t')[3]
	median = line.split('\t')[4]
	average = line.rstrip('\n').split('\t')[-1]
	
	info_dict[pathnumber].append(length)
	info_dict[pathnumber].append(median)
	info_dict[pathnumber].append(average)

	return info_dict, start_dict, end_dict


def connect_end(startnumber, endnumber, lists_to_connect):
	##  explain ##
	for c in lists_to_connect:

		if endnumber in c:
			if endnumber == c[-1]:
				c.append(startnumber)
				return lists_to_connect
			else:
				indx = c.index(endnumber)
				new_connection = c[:indx+1]
				new_connection.append(startnumber)
				lists_to_connect.append(new_connection)
				return lists_to_connect

def connect_start(startnumber, endnumber, lists_to_connect):
	for c in lists_to_connect:
		if startnumber in c:
			if startnumber == c[0]:
				c.insert(0, endnumber)
			else:
				indx = c.index(startnumber)
				new_connection =[endnumber]+ c[indx:]
				lists_to_connect.append(new_connection)
				return lists_to_connect


def write_newpath_length(list_connecting, info_dict, all_paths ):
	## explain  ##

	newpath = []

	#find sequence length of new contigs
	start = info_dict[list_connecting[0]][0]
	cstart = int(start.split()[1]) #find start using pathnumber
	end = info_dict[list_connecting[-1]][1]
	cend = int(end.split()[-2])
	seqlength = cend-cstart

	newaverage = 0
	for c in list_connecting:
		newpath += all_paths[c]
		newaverage += float(info_dict[c][-1])
	newaverage = newaverage/len(list_connecting)
	return newpath, seqlength, start, end, newaverage

## main ##

print('connecting blocks')

# read file #
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


print('done reading file')

print('starting matching')

# match connections #
to_connect = []

startSet = set(starts)
endSet = set(ends)

already_connected = set([])

#for s in sorted( list(startSet.intersection(endSet)) ):
#go through those that match - keep the rest as is
for s in startSet.intersection(endSet):

	for e in ends[s]:
		for st in starts[s]:

			if st in already_connected and e in already_connected:
				connect_end(st, e, to_connect) #problem resulting in negative

			elif st in already_connected:
				connect_start(st, e, to_connect)

			elif e in already_connected:
				connect_end(st, e, to_connect)

			else:
				newlist =[e]
				newlist.append(st)
				to_connect.append(newlist)

			already_connected.add(st)
		already_connected.add(e)

#		print(to_connect)

print('done matching, writing paths')


# find new lengths #

allnewlengths= []
all_new_paths = []


chr = sys.argv[1].split('_')[0]


bedoutput = open(sys.argv[1] + 'connected.bed', 'w')
chroutput = open(sys.argv[1] + 'connected.txt', 'w')
header = ['pathnumber', 'start', 'end', 'snplength', 'average']
chroutput.write('\t'.join(header) + '\n')


newid = 0
for connecting in to_connect:
	newsnplength = 0
	newaverage = 0

	res = write_newpath_length(connecting, number_to_info, full_paths)
	snps = len(res[0])*2
	all_new_paths.append(res[0])
	allnewlengths.append(res[1])
	newid += 1

	chrlst = [str(newid), res[2], res[3], str(snps), str(res[-1])]
	#chroutput.write('\t'.join(chrlst) + '\n')

	bedlst = [chr, res[2].split()[1], res[3].split()[-2]]
	bedoutput.write('\t'.join(bedlst) + '\n')
	if int(res[2].split()[1]) > int(res[3].split()[-2]):
		print(connecting)
		print(res)
		print(bedlst)

for p in startSet - startSet.intersection(endSet):
	for n in starts[p]:
		newid += 1
		if int(number_to_info[n][2]) < 2:
			continue
		oldpathlst = [str(newid), number_to_info[n][0], number_to_info[n][1], number_to_info[n][2], number_to_info[n][-1]]
		chroutput.write('\t'.join(oldpathlst) +'\n')


print('done')

# find n50, l50 #
chrlen = 0
for fields in open(sys.argv[2]):
	if chr == fields.split('\t')[0]:
		chrlen = int(fields.split('\t')[1])


print(chr, 'length', chrlen)
commonoutput = open(sys.argv[3], 'a')

#print(sorted(allnewlengths))

half = chrlen/2
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
		lst = [str(chr), str(n50/1000), str(l50)]
		commonoutput.write('\t'.join(lst) + '\n')
		quit()



print('uptohalf', uptohalf)
