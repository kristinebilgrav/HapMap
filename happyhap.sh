#!/bin/bash -l
#SBATCH -A sens2017106
#SBATCH -p core
#SBATCH -n 2
#SBATCH -t 7-00:00:00
#SBATCH -J happyHAP

module load python3 sqlite bioinfo-tools pysam

#$1 file with paths to all files
#$2 chromosome

#create DB (check scripts included)
#python /proj/nobackup/sens2017106/kristine/hapmap/haploop.py $1

#filter db
#python /proj/nobackup/sens2017106/kristine/hapmap/HapMap/cleandbfaster.py

# ----------build---------- #

#create graph - give chr
#source /home/kbilgrav/anaconda3/bin/activate
#python /proj/nobackup/sens2017106/kristine/hapmap/HapMap/build/main.py $2

#connect graph
#python /proj/nobackup/sens2017106/kristine/hapmap/HapMap/build/connect_kmers.py $2_graph.json $2_graph_connectedA.txt

#connect bubbled paths
ref=/proj/sens2017106/reference_material/fasta/human_g1k_v37.fasta.fai
#connected=/proj/nobackup/sens2017106/kristine/hapmap/all_50stats.txt
#python /proj/nobackup/sens2017106/kristine/hapmap/HapMap/build/connectbubbles.py $2_graph_connectedA.txt $ref $connected

#statistics
module load bioinfo-tools BEDTools
#bedtools sort -i $2_graph_connectedA.txtconnected.bed > $2_graph_connectedB.bed
#rm $2_graph_connectedA.txtconnected.bed

#n50 unique
#bedtools merge -i $2_graph_connectedB.bed -d 0 > $2_graph_connectedB_merged.bed
#uniquen50=/proj/nobackup/sens2017106/kristine/hapmap/unique_n50.txt
#python /proj/nobackup/sens2017106/kristine/hapmap/HapMap/statistics/findn50.py $2_graph_connectedB_merged.bed $ref $uniquen50

#genome coverage
#A=/proj/nobackup/sens2017106/kristine/hapmap/human_37_chr$2.bed
#bedtools coverage -a $A -b $2_graph_connectedB.bed -d > $2_graph_base_coverage.bed

#cat *_graph_connectedB.bed > all_graphs_connected.bed
#bedtools sort -i all_graphs_connected.bed > all_graphs_connected_sorted.bed
all_bed=all_graphs_connected_sorted.bed
MB=/proj/nobackup/sens2017106/kristine/hapmap/human.37.1MB.bed
#bedtools coverage -a $MB -b all_graphs_connected_sorted.bed > all_graphs_connected_sorted_genomecov.bed

#bedtools genomecov -bga -i $all_bed -g $ref > all_graphs_connected_sorted_genomecov.bed
#sed -i -e 's/^/hs/' all_graphs_connected_sorted_genomecov.bed


# ----------filtering--analysis---------- #


#python /proj/nobackup/sens2017106/kristine/hapmap/HapMap/filtering_analysis/unfilt_database.py $MB
#python /proj/nobackup/sens2017106/kristine/hapmap/HapMap/filtering_analysis/filt_database.py $MB
#python3 /proj/nobackup/sens2017106/kristine/hapmap/HapMap/filtering_analysis/count_graph_variants.py $MB $2_graph.json
#python3 /proj/nobackup/sens2017106/kristine/hapmap/HapMap/filtering_analysis/count_snv_connectedA.py $MB $2_graph_connectedA.txt

#python reorg_snv --

# ------------genome--coverage-------------- #

#find genome coverage - using script
#ref=/proj/sens2017106/reference_material/fasta/human_g1k_v37.fasta.fai
#python3 /proj/nobackup/sens2017106/kristine/hapmap/findgenomecoverage.py $2_graph_co.txt $ref /proj/nobackup/sens2017106/kristine/hapmap/haploblockgenomecoverage.txt

#make bed file
#python3 makebedfile.py $2_graph_counted.txt $2_graph_hbpos.bed


# -----------match-------------- #

#matching with HRC
#module load bioinfo-tools HaplotypeReferenceConsortium/r1.1
#HRC=$HRC_ROOT/HRC.r1-1.GRCh37.wgs.mac5.sites.vcf.gz

#python3 /proj/nobackup/sens2017106/kristine/hapmap/HapMap/match_graph/matchpaths.py $2_graph_counted.txt $HRC

#match with 1KGP
#1KGP_phase3_paths.txt
outputfile=/proj/nobackup/sens2017106/kristine/hapmap/graphmap1kgp.txt
python3 /proj/nobackup/sens2017106/kristine/hapmap/HapMap/match_graph/matchpaths_1kgpphase3.py $1_graph_connectedA.txt $2 $outputfile
