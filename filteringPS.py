import sys

#filter 10x vep annotated file on SNPs/SVs not present in either 1KGP, SweGen or have rs number for gnomad (ex rs112750067 )
#SweGen_AF last -1 
#Several 1KGP AFs (for each population) from pos -10 - -6
#dontpass = ['10X_QUAL_FILTER', '10X_RESCUED_MOLECULE_HIGH_DIVERSITY', '10X_ALLELE_FRACTION_FILTER', '10X_PHASING_INCONSISTENT', '10X_HOMOPOLYMER_UNPHASED_INSERTION']

output = open(sys.argv[1] + '.filtered.vcf', 'w')
for line in open(sys.argv[1]):
	save = False

	if line.startswith('#'):
		output.write(line)
		continue

	swegen = line.strip('\n').split(';CSQ=')[-1].split('\t')[0].split('|')[-1]
	kgp = line.strip('\n').split(';CSQ=')[-1].split('\t')[0].split('|')[-10:-5]
	
	threshold = 0.05
	AF = False
	if len(swegen) > 0:
		if float(swegen) > threshold:
			save = True
			AF = True	
	for p in kgp:
		if len(p) > 0 and float(p) > threshold:
			save = True
			AF = True

	#filter on PASS 
	passit = ['PASS']
	filter = line.strip('\n').split('\t')[6]
	if filter in passit and AF == True:
		save = True
	
	else:
		save = False



	if save == True:
		output.write(line)
		continue
