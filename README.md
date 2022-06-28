# HapMap

Consist of several modules and analysis parts

# Build graph
Takes phased VCF, filters, creates sqlite database with informative SNPs. 

Uses database to build de bruijn graph (json). 

Takes json and connects graph into short () and long () contigs. 

Finally writes to vcf

# Statistics
Looks at switch error and N50

Also analysis of annotated graph. 


# Matching
Matching graph with dataset

python3 setup.py build_ext --inplacemodul

python3 main.py chr
