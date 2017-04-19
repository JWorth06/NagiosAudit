#nagiosaudit2.py
'''
Reports The nodes that do not have a given list of checks into a csv file.
'''

import csv
import itertools

def audit_checks(filename):
	'''
	Imports services that are wanting to be checked from CSV file.
	'''
	auditchecks = []
	with open(filename, 'r') as f:
		items = csv.reader(f)
		for item in items:
			auditchecks = item
	
	return auditchecks

def lib_build_sort(filename):
	'''
	Builds and returns a list of dictionaries for a host/service CSV and sorts based on host name.
	'''
	
	lib = []
	with open(filename, 'r') as f:
		rows = csv.reader(f)
		headers = next(rows)
		for row in rows:
				row[0] = str.lower(row[0])
				record = {
					'host': row[0],
					'service': row[1]
					}
				lib.append(record)

	lib.sort(key = lambda holding: holding['host'])
	
	return lib

def group_lib(sortedlib):
	'''
	Groups library so each host is connected to a list of services in the dictionary.
	'''

	groupedlib = []
	for name,items in itertools.groupby(sortedlib, key=lambda holding: holding['host']):
		holder = []
		for it in items:
			holder.append(it['service'])
		record = {
			'host': name,
			'services': holder
			}
		groupedlib.append(record)
	return groupedlib
	
def make_chart(nag_library, auditchecks):
	'''
	Makes a chart with host, audit checks, and then extra checks listed by name.
	The audit checks are marked with an 'x' if they exist and blank if they don't exist.
	'''
	new_nag_library = []
	for checks in auditchecks:
		temp = []
		temp.append(checks)
		for it in nag_library:
			if checks not in it['services']:
				temp.append(it['host'])
		new_nag_library.append(temp)
	
	return new_nag_library
	
					
def csv_file_writer(filename, library):
	'''
	Writes the library to the given filename as a CSV file.
	'''
	with open(filename,'w', newline='') as csv_file:
		writer = csv.writer(csv_file)
		for item in library:
			writer.writerow(item)	


#Builds libraries from CSV files and groups them together
#change filenames passed to lib_build_sort if you want to read from different csv files
reportlib = lib_build_sort('reportservices.csv')	
newreportlib = group_lib(reportlib)

auditchecks = audit_checks('auditchecks.csv')


#Creates the audit library
audit_library = make_chart(newreportlib, auditchecks)



#Writes csv versions of the audit that can be imported into google sheets/excel
#Make new files or clear these file names out after each run
csv_file_writer('BlankSpaces.csv', audit_library)


		
