#!/bin/bash -l
#SBATCH -A sens2017106
#SBATCH -p core
#SBATCH -n 2
#SBATCH -t 2-00:00:00
#SBATCH -J happyHAP

module load python3 sqlite bioinfo-tools pysam

#PATH=/proj/nobackup/sens2017106/kristine/hapmap

#$1 file with paths to all files 
#$2 chromosome

#create DB (check scripts included)
#python /proj/nobackup/sens2017106/kristine/hapmap/haploop.py $1

#filter db 
#python /proj/nobackup/sens2017106/kristine/hapmap/HapMap/cleandbfaster.py

# ----------build----------- #

#create graph - give chr
#source /home/kbilgrav/anaconda3/bin/activate
#python /proj/nobackup/sens2017106/kristine/hapmap/HapMap/main.py $2 

#connect graph 
#python /proj/nobackup/sens2017106/kristine/hapmap/HapMap/build/connect_kmers.py $2_graph.json $2_graph_contigs.txt

#connect bubbled paths
ref=/proj/sens2017106/reference_material/fasta/human_g1k_v37.fasta.fai
connected=/proj/nobackup/sens2017106/kristine/hapmap/all_n50stats.txt

#mv /proj/nobackup/sens2017106/kristine/hapmap/$2_graph_connectedA.txt /proj/nobackup/sens2017106/kristine/hapmap/$2_graph_contigs.txt
#mv /proj/nobackup/sens2017106/kristine/hapmap/$2_graph_connectedA.txtIDs.txt /proj/nobackup/sens2017106/kristine/hapmap/$2_graph_contigIDs.txt

#python HapMap/build/connectbubbles.py $2_graph_contigs.txt $ref $2_graph_contigs_connections $connected

#write to vcf 
fasta=/proj/sens2017106/reference_material/fasta/human_g1k_v37.fasta
#python HapMap/build/makeVCF.py $2_graph_contigs.txt $2_graph_contigs_connections.txt $2_graph.vcf $fasta

# --------statistics-------#

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

#Switch Error Rate
ser_file=/proj/nobackup/sens2017106/kristine/hapmap/LR_SER.txt
python HapMap/statistics/switcherror.py $1 $ser_file


#-------coverage-------#

#genome coverage per 1MB bin
#cat *_graph_connectedB.bed > all_graphs_connected.bed
#bedtools sort -i all_graphs_connected.bed > all_graphs_connected_sorted.bed
all_bed=all_graphs_connected_sorted.bed
MB=/proj/nobackup/sens2017106/kristine/hapmap/human.37.1MB.bed
#bedtools coverage -a $MB -b all_graphs_connected_sorted.bed > all_graphs_connected_sorted_genomecov.bed

#bedtools genomecov -bga -i $all_bed -g $ref > all_graphs_connected_sorted_genomecov.bed

#sed -i -e 's/^/hs/' all_graphs_connected_sorted_genomecov.bed
#awk -F "\t" 'OFS="\t" { print $1, $2 , $3 , $4 }' all_graphs_percontig_cov.bed  > all_graphs_percontig_cov2.bed



#coverage per contig bin
#cat *_graph_connectedB_merged.bed > all_graphs_connectedB_merged.bed
#bedtools sort -i all_graph_connectedB_merged.bed > all_graph_connectedB_merged_sorted.bed
binfile=all_graph_connectedB_merged_sorted.bed
covfile=all_graphs_connected_sorted.bed
#bedtools coverage -a  -b all_graphs_connected_sorted.bed > all_graphs_connected_sorted_genomecov.bed

#get the contig bin and snvs

#python3 /proj/nobackup/sens2017106/kristine/hapmap/HapMap/filtering_analysis/count_snv_connectedA.py $2_graph_connectedB_merged.bed $2_graph_connectedA.txt $2_graph_permerged_snvcount.txt
#cat *_graph_permerged_snvcount.txt > all_graph_permerged_snvcount.txt
#sed -i -e 's/^/hs/'

# ------filtering--------- #

#check filtering
#python3 $PATH/HapMap/filtering_analysis/count_graph_variants.py $MB $2_graph.json
#python3 $PATH/HapMap/filtering_analysis/count_snv_connectedA.py $MB $2_graph_connectedA.txt
#python HapMap/filtering_analysis/count_snv_DB.py $MB tabelname

# ------ #


#find genome coverage - using script
#ref=/proj/sens2017106/reference_material/fasta/human_g1k_v37.fasta.fai
#python3 /proj/nobackup/sens2017106/kristine/hapmap/findgenomecoverage.py $2_graph_co.txt $ref /proj/nobackup/sens2017106/kristine/hapmap/haploblockgenomecoverage.txt

#make bed file
#python3 makebedfile.py $2_graph_counted.txt $2_graph_hbpos.bed

# ------------matching------------- #

#matching with HRC
#module load bioinfo-tools HaplotypeReferenceConsortium/r1.1
#HRC=$HRC_ROOT/HRC.r1-1.GRCh37.wgs.mac5.sites.vcf.gz 

#python3 /proj/nobackup/sens2017106/kristine/hapmap/matchpaths.py $2_graph_counted.txt $HRC

#match with 1KGP
#1KGP_phase3_paths.txt
#split to seperate files:
#bcftools view -c1 -Oz -s $kgpsample -o $1

#outputfile=/proj/nobackup/sens2017106/kristine/hapmap/graphmap1kgp.txt
#python3 /proj/nobackup/sens2017106/kristine/hapmap/HapMap/matchpaths_1kgpphase3.py $1_graph_connectedA.txt $2 $outputfile

#python3 HapMap/match_graph/matchpaths_block_multisamplevcf.py $1_graph_connectedA.txt $2 $1_connnected_kgp.txt

module load bioinfo-tools BEDTools tabix bcftools
#bedtools sort -header  -i $2 | bgzip /dev/stdin -c > $2
#tabix $1_graph_sort.vcf.gz
#tabix $2.gz

#bcftools isec $1_graph_sort.vcf.gz $2 -p $3.isec.out
#rm $3.isec.out/0001.vcf
#rm $3.isec.out/0003.vcf
#rm $3.isec.out/sites.txt


#python HapMap/match_graph/matchanalysis.py paths.text chr_path_cov.txt
#python HapMap/match_graph/matchjaccard.py  14_graph.vcf chr14_random_isec.txt chr14_random_isec_002.txt


# ---------annotation-----------#
#sbatch VEP.sh $1_graph_sort.vcf.gz $1_graph_sort_annotated.vcf
