import sys
import gzip
import sqlite3
import os
#os.system('module load bioinfo-tools pysam')
#import pysam
import argparse

#sqlite3.paramstyle = 'named'
#create database & table
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute("CREATE TABLE gps (chr INTEGER, pos INTEGER, GT TEXT, PS INTEGER)")

#insert info
def insert(vcf_data):
        with conn:
                cur.execute("INSERT INTO gps VALUES (:chr, :pos, :GT, :PS)", vcf_data)

def get_item(i):
        with conn:
                cur.execute('SELECT * FROM gps WHERE chr=:chr', {'chr':i})
                return cur.fetchall()

if 'gz' in sys.argv[1]:
        for line in gzip.open(sys.argv[1]):
                if line.startswith(b'#'):
                        continue
                vcf_data = {}
                line = line.strip(b'\n').split(b'\t')
                chr = line[0].replace(b'chr', b'')
                try:
                    	vcf_data['chr'] = int(chr)
                except:
                       	vcf_data['chr'] = chr.decode('utf-8')
                pos = line[1]
                vcf_data['pos'] =int( pos)
                info = line[8].split(b':')
                if b'GT' in info:
                        i = info.index(b'GT')
                        GT = line[9].split(b':')[i]
                        vcf_data['GT'] = GT.decode('utf-8')

                if b'PS' in info:
                        i = info.index(b'PS')
                        PS = line[9].split(b':')[i]
                        try:
                                vcf_data['PS'] = int(PS)
                        except:
                                vcf_data['PS'] = PS.decode('utf-8')
                insert(vcf_data)


q = {'chr':1}
w = get_item(6)
print(w)
conn.commit()