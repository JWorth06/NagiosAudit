#vm_info_check.py
'''
Compares a csv exported from vminfo with a Nagios audit report of Hosts and exports a csv of
the extras that exist in each.
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
				record = str.lower(row[0])
				lib.append(record)

	lib.sort()
	
	return lib

	
def remove_match(primary_lib, secondary_lib):
	'''
	Removes services from the secondary_lib that perfectly match host + service name in primary_lib.
	Then removes empty hosts from secondary_lib and returns it.
	'''

	
	for items_one in primary_lib:
		for items_two in secondary_lib:
			if items_one == items_two:
				secondary_lib.remove(items_two)
				
	return secondary_lib
					
def csv_file_writer(filename, library):
	'''
	Writes the library to the given filename as a CSV file.
	'''
	with open(filename,'w', newline='') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(library)	


#Builds libraries from CSV files and groups them together
#change filenames passed to lib_build_sort if you want to read from different csv files
vminfo = lib_build_sort('vm_inventory.csv')	

reportlib = lib_build_sort('reporthosts.csv')


#Creates the extra reports
vminfo_extras = remove_match(reportlib, vminfo)

#clears and rebuilds vminfo library
del vminfo[:]
vminfo = lib_build_sort('vm_inventory.csv')

nagios_extras = remove_match(vminfo, reportlib)


#Writes csv versions of the error reports that can be imported into google sheets/excel
#Make new files or clear these file names out after each run
csv_file_writer('vminfo_extras.csv', vminfo_extras)
csv_file_writer('nagios_extras.csv', nagios_extras)

		
