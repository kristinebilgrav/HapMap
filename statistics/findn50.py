import sys

lens=[]
for line in open(sys.argv[1]):
	line = line.rstrip('\n')
	start = line.split('\t')[1]
	end = line.split('\t')[2]
	thislen = int(end) -int(start)
	lens.append(thislen)

chr=sys.argv[1].split('_')[0]
chrlen= 0
for inp in open(sys.argv[2]):
	if chr == inp.split('\t')[0]:
		chrlen = float(inp.split('\t')[1])

half= chrlen/2
gettohalf=0
numbtohalf = []

nout = open(sys.argv[3], 'a')
for l in reversed(sorted(lens)):
	if gettohalf < half:
		gettohalf += float(l)
		numbtohalf.append(l)
	else:
		n50 = l
		n50kb = float(l)/1000
		l50 = len(numbtohalf)

		print('n50', n50kb, 'l50', l50)
		print(half, gettohalf)
		put = [chr, str(n50kb), str(l50)]
		nout.write('\t'.join(put) + '\n')
		quit()
