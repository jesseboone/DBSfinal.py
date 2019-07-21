import re

def fail () :
	fr.write("Query failed, syntactical error\n\n")
	return

def getField (line, field) :
	l = line.split(field, 1)
	if l[0] == line :
		return 'NA'
	else :
		l = l[1].lstrip(":")
		l = l.split()
		return l[0]

def condtrue(cond, line) :
	#<, >, =, <=, >=, <>
		if cond == '' :
			return True
		elif "<>" in cond :
			c = cond.split("<>")
			if c[0] not in line :
			 	return False
			if int(str(getField(line, c[0]))) == int(str(c[1])) :
				return False
			else :
				return True
		elif "<=" in cond :
			c = cond.split("<=")
			if c[0] not in line :
			 	return False
			if int(str(getField(line, c[0]))) > int(str(c[1])) :
				return False
			else :
				return True
		elif ">=" in cond :
			c = cond.split(">=")
			if c[0] not in line :
			 	return False
			if int(str(getField(line, c[0]))) < int(str(c[1])) :
				return False
			else :
				return True
		elif "=" in cond :
			c = cond.split("=")
			if c[0] not in line :
			 	return False
			if int(str(getField(line, c[0]))) == int(str(c[1])) :
				return True
			else :
				return False
		elif ">" in cond :
			c = cond.split(">")
			if c[0] not in line :
			 	return False
			if int(str(getField(line, c[0]))) <= int(str(c[1])) :
				return False
			else :
				return True
		elif "<" in cond :
			c = cond.split("<")
			if c[0] not in line :
			 	return False
			if int(str(getField(line, c[0]))) >= int(str(c[1])) :
				return False
			else :
				return True
	
def printexceptDocID(line) :
	line = re.sub("DocID:\d+ *", "", line)
	line = line.rstrip("\n")
	fr.write(line)
	return

def allTrue(conditions, line) :
	for cond in conditions :
		if not condtrue(cond, line) :
			return False
	return True

def query (str1) :
	l = str1.split("],[", 1)
	if l[0].startswith("[") and l[1].endswith("]") :
		l[1] = l[1].rstrip("]")
		l[0] = l[0].lstrip("[")
	else :
		fail()
		return
	#print (l)
	conditions = l[0].split(",")
	fields = l[1].split(",")
	fd = open("data.txt", "r")
	with open('data.txt') as fd: #building the list of DocIDs
		for line in fd:
			if allTrue(conditions, line) :
				for field in fields :
					if field == '' :
						printexceptDocID(line)
					else :
						fr.write(field + ':' + getField(line, field) + " ")
				fr.write("\n")
	fd.close()
	fr.write("\n")
	return

def checkField (str1, field, f) :
	l = str1.split(field, 1)
	if l[0] == str1 :
		return
	else :
		l = l[1].split()
		f.add(l[0])
		return

def count (str1) :
	count = 0
	l = str1.split("],[", 1)
	if l[0].startswith("[") and l[1].endswith("]") :
		l[1] = l[1].rstrip("]")
		l[0] = l[0].lstrip("[")
	else :
		fail()
		return

	if l[1] == '0' :
		#for each line, add to count
		fd = open("data.txt", "r")
		with open('data.txt') as fd: #building the list of l[0]s
			for line in fd:
				if l[0] in line:
					count+=1 
		fd.close()
		fr.write(str(l[0]) + ":" + str(count) + "\n\n")
		return
	elif l[1] == '1' :
		#for each line, add to set (if unique)
		f = set()
		fd = open("data.txt", "r")
		with open('data.txt') as fd: #building the set of unique l[0]s
			for line in fd: 
				#split and add if unique value?
				checkField(line,l[0],f)
		fd.close()
		fr.write(str(l[0]) + ":" + str(len(f)) + "\n\n")
		return
	else :
		fail()
		return

def getDocID (str1) :
	l = str1.split("DocID:", 1)
	if l[0] == str1 :
		return -1
	else :
		l = l[1].split()
		return int(l[0])

def insert (str1) :
	num = getDocID(str1)
	if num == -1 : #if it doesn't have an id, give it one not taken
		num = max(DocIDlist)+1
		str1 = "DocID:" + str(num) + " " + str1 #put it at the beginning of the string
	elif num in DocIDlist : #else if a duplicate id, handle that
		fr.write("Duplicate DocID!\n\n")
		return;
	#write it to file
	fd = open('data.txt','a')
	fd.write("\n" + str1)
	fr.write(str1 + "\n\n")
	return

def pick (str1) :
	l = str1.split("(", 1)
	if str1.endswith(')'):
		l[1] = l[1].rstrip(')')
		if l[0] == 'query' :
			query(l[1])
		elif l[0] == 'count' :
			count(l[1])
		elif l[0] == 'insert' :
			insert(l[1])
		else :
			fail()
		return
	else :
		fail()
		return

def parse (str1) :
	l = str1.split(".", 1)
	if l[0] != 'final' :
		fail()
		return
	else :
		pick(l[1])
		return


#main here

DocIDlist = list()
fr = open("results.txt", "w")

fd = open("data.txt", "r")
with open('data.txt') as fd: #building the list of DocIDs
	for line in fd:
		DocIDlist.append(getDocID(line))
fd.close()

with open('queries.txt') as fq: #parsing all the queries
	for str1 in fq:
		fr.write(">" + str1)
		str1 = str1.rstrip('\n')
		parse(str1)
fq.close()
fr.close()
# fd.close()


