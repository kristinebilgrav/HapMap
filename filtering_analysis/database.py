import sqlite3

#connect to database


class DB: 
	def __init__(self, db):
		self.conn = sqlite3.connect(db)
		
		#self.conn.row_factory = lambda cursor, row: row[0]
		self.cur = self.conn.cursor()


	#general

	#create table
	def create_table(self, insert):
		with self.conn:
			self.cur.execute(insert)



	#query
	def get_item(self, text):
		with self.conn:
			self.cur.execute(text)
			return self.cur.fetchall()

	def query(self,text):
		self.cur.execute(text)
		res = self.cur.fetchall()
		return res


	#search table names
	def search_table(self):
                #self.conn.row_factory = lambda cursor, row: row[0]
		res = self.query("""SELECT name FROM sqlite_master WHERE type= 'table' """)
		return [table[0] for table in res]
		#return self.cur.fetchall() 


        #insert many generaL
	def insert_many_general(self, text, data):
		with self.conn:
			self.cur.executemany(text, data)

	def insert_general(self, text, data):
		with self.conn:
			self.cur.execute(text, data)

	def create_index_general(self,text):
		with self.conn:
			self.cur.execute(text)

	def drop_index_general(self, text):
		with self.conn:
			self.cur.execute(text)


	#database specific

	#insert info
	def insert(self, vcf_data):
		with self.conn:
			self.cur.execute("INSERT INTO haploblock VALUES (:id, :chr, :pos, :Alt, :GT, :PS)", vcf_data)

	def insert_many(self,values):
		with self.conn:
			self.cur.executemany('INSERT INTO haploblock VALUES (?, ? , ?, ?, ?, ?)', values) 


	def create_index(self, name, columns):
		with self.conn:
			q = 'CREATE INDEX {} ON haploblock {} ;'.format(name, columns)
			self.cur.execute(q)

	def drop_index(self, name):
		with self.conn:
			text = 'DROP INDEX IF EXISTS {};'.format(name)
			self.cur.execute(text)





