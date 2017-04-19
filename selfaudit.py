#selfaudit.py
'''
Compares a Nagios Report to itself, reporting a CSV that 
has all services in Nagios and all boxes with those services.
'''

import csv
import itertools

def lib_checks(nag_library):
	'''
	Imports services that are wanting to be checked from CSV file.
	'''
	auditchecks = []
	for it in nag_library:
		for ser in it['services']:
			if ser not in auditchecks:
				auditchecks.append(ser)
	
	auditchecks.sort()
	
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
					'service': str.lower(row[1])
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
	for it in nag_library:
		temp = []
		temp.append(it['host'])
		for checks in auditchecks:
			if checks in it['services']:
				temp.append('x')
			else:
				temp.append('')
		for ser in it['services']:
			if ser not in auditchecks:
				temp.append(ser)
		new_nag_library.append(temp)
	
	return new_nag_library
	
					
def csv_file_writer(filename, audchecks, library):
	'''
	Writes the library to the given filename as a CSV file.
	'''
	with open(filename,'w', newline='') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(audchecks)
		for item in library:
			writer.writerow(item)	


#Builds libraries from CSV files and groups them together
#change filenames passed to lib_build_sort if you want to read from different csv files
reportlib = lib_build_sort('reportservices.csv')	
newreportlib = group_lib(reportlib)

auditchecks = lib_checks(newreportlib)


#Creates the error reports
audit_library = make_chart(newreportlib, auditchecks)



#Writes csv versions of the audit that can be imported into google sheets/excel
#Make new files or clear these file names out after each run
csv_file_writer('SelfAudit.csv', auditchecks, audit_library)


		
