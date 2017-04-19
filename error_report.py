#error_report.py
'''
Compares a 
'''


import csv
import itertools

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
	
def remove_match(primary_lib, secondary_lib):
	'''
	Removes services from the secondary_lib that perfectly match host + service name in primary_lib.
	Then removes empty hosts from secondary_lib and returns it.
	'''

	
	for items_one in primary_lib:
		for items_two in secondary_lib:
			if items_one['host'] == items_two['host']:
				for ser in items_one['services']:
					if ser in items_two['services']:
						items_two['services'].remove(ser)

								
	new = []
	
	for it in secondary_lib:
		if it['services']:
			holder = []
			holder.append(it['host'])
			for a in it['services']:
				holder.append(a)
			new.append(holder)
						
	return new
					
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
ccmlib = lib_build_sort('ccmservices.csv')	
newccmlib = group_lib(ccmlib)

reportlib = lib_build_sort('reportservices.csv')
newreportlib = group_lib(reportlib)


#Creates the error reports
ccmerror = remove_match(newreportlib, newccmlib)

#clears and rebuilds ccm library
del newccmlib[:]
newccmlib = group_lib(ccmlib)

reporterror = remove_match(newccmlib, newreportlib)


#Writes csv versions of the error reports that can be imported into google sheets/excel
#Make new files or clear these file names out after each run
csv_file_writer('ccmerrors.csv', ccmerror)
csv_file_writer('reporterrors.csv', reporterror)

		
