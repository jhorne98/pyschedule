#!/usr/bin/env python3

import pymysql
import sys
import getopt
import warnings
from datetime import datetime

def main(argv):
	# set sql command based on operator
	try:
		opts, args = getopt.getopt(argv, "hri:d:", ["read", "insert=", "delete="])
	except getopt.GetoptError:
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("pyschedule.py -i <input>")
			sys.exit()
		elif opt in ("-r", "--read"):
			execSql = "select * from task;"
			execParams = None
		elif opt in ("-i", "--insert"):
			execSql = "insert into task (name, course, due, day) values (%s, %s, %s, %s);"
			execParams = (argv[1], argv[2], argv[3], argv[4])
		elif opt in ("-d", "delete"):
			execSql = "delete from task where id = %s;"
			execParams = (argv[1])
	
	# useful but cheaty
	warnings.simplefilter("ignore")
	
	# connect to the mysql db
	db = pymysql.connect("localhost", "", "", "pyscheduler")

	# make a cursor object
	cursor = db.cursor()

	# create the task table if it does not exist
	createTableSql = """create table if not exists task (
				id int(11) not null auto_increment,
				name varchar(256) not null,
				course varchar(128),
				due date not null,
				day varchar(10),
				primary key (id)
			);"""

	cursor.execute(createTableSql)
	
	try:
		# execute the sql command
		cursor.execute(execSql, execParams)
		db.commit()
	except:
		db.rollback()

	if execParams == None:
		template = "{0:<8}| {1:30}| {2:12}| {3:7}| {4:10}"
		print(template.format("ID", "TASK", "COURSE", "DUE", "DAY"))
		print(template.format("-", "-", "-", "-", "-"))
		for row in cursor.fetchall():
			print(template.format(row[0],
				row[1],
				row[2],
				datetime.strftime(row[3], "%-m/%d"),
				row[4]))

	#print(execParams)

	db.close()

if __name__ == '__main__':
	main(sys.argv[1:])
