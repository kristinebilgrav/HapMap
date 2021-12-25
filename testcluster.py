import sys 
import numpy as np 
from sklearn.cluster import KMeans
import database
#connect db
db = database.DB('/proj/nobackup/sens2017106/kristine/hapmap/hapmap.db')

chr = sys.argv[1]

idq = '''SELECT DISTINCT id FROM haploblock ;  '''
ids = [id[0] for id in db.get_item(idq)] #list with ids


if chr == 'Y' or chr == 'X':
	#cluster to find out if male or female
	#male cluster will have higher amounts of variants 

	#np.array of 

	vars = np.array()

	#if female: continue as normal on X, ignore Y

	#if male: treat X as one PS and Y as one (ignore GT)


kcon_time = []

start = time.time()
