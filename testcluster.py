import sys 
import numpy as np 
from sklearn.cluster import KMeans #anaconda source /home/kbilgrav/anaconda3/bin/activate
import database
#connect db
db = database.DB('/proj/nobackup/sens2017106/kristine/hapmap/hapmap.db')

chr = sys.argv[1]

idq = '''SELECT DISTINCT id FROM cleanblock ;  '''
ids = [id[0] for id in db.get_item(idq)] #list with ids

#big query asking for X and Y
#q = '''SELECT * FROM cleanblock WHERE chr='Y'; '''

labels = {}
if chr == 'Y' or chr == 'X':
	#cluster to find out if male or female
	#male cluster will have higher amounts of variants 

	#np.array of amounts of insertions in an individual on Y chr

	vars = []
	#also search for x -> [0, 6000, 111000]
	for id in ids:
		q = ''' SELECT COUNT(*) FROM cleanblock WHERE id ='{}' AND chr='{}' UNION ALL SELECT COUNT(*) FROM cleanblock WHERE id ='{}' AND chr='{}';  '''.format(id, 'Y', id, 'X')
		varq = db.get_item(q)

		if id not in labels: 
			labels[id] = [varq[0][0], varq[1][0]]

		alist = [varq[0][0], varq[1][0] ]
		vars.append( alist)

	vars = np.array(vars)
	#print(vars)

	n_clusters = 2
	n_samples = len(ids)
	n_init = 62 #number of times to recalculate the centroid
 
	kmeans = KMeans(n_clusters = n_clusters, init = "k-means++", n_init = 40, max_iter = 62, random_state = 42)
	kmeans.fit(vars)
	print(kmeans.labels_)
	cluster = kmeans.labels_
	print(labels)
	print(kmeans.cluster_centers_)

	#if female 1: continue as normal on X, ignore Y
	

	#if male 0: treat X as one PS and Y as one (ignore GT)
	for i in labels: 
		item_number = list(labels.keys()).index(i)
		cluster_id = cluster[item_number]
		#if cluster_id == 0:
			


#class sklearn.cluster.KMeans(init = 'random', nclusters = 2, n_init = 10, max_iter = 62,  random_state=42)


