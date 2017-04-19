#adaudit.py

import csv
import itertools

def hr_build_sort(filename):
	'''
	
	'''
	
	lib = []
	with open(filename, 'r') as f:
		rows = csv.reader(f)
		headers = next(rows)
		for row in rows:
				row[0] = str.lower(row[0])
				if row[2] == "":
					first = str.lower(row[1])
				else:
					first = str.lower(row[2])
				row[3] = str.lower(row[3])
				row[4] = str.lower(row[4])
				row[7] = str.lower(row[7])
				record = {
					'lastname': row[0],
					'firstname': first,
					'email': row[3],
					'job': row[4],
					'boss': row[7],
					'location': row[5]
					}
				lib.append(record)

	lib.sort(key = lambda holding: holding['lastname'])
	
	return lib
	
	
def ad_build_sort(filename):
	'''
	
	'''
	
	lib = []
	with open(filename, 'r') as f:
		rows = csv.reader(f)
		headers = next(rows)
		for row in rows:
				row[0] = str.lower(row[0])
				row[1] = str.lower(row[1])
				row[4] = str.lower(row[4])
				row[9] = str.lower(row[9])
				row[5] = str.lower(row[5])
				record = {
					'lastname': row[1],
					'firstname': row[0],
					'email': row[4],
					'job': row[9],
					'boss': row[5],
					'location': row[7]
					}
				lib.append(record)

	lib.sort(key = lambda holding: holding['lastname'])
	
	return lib
	
	
def lib_compare_ifnamesmatch(hrlib, adlib):
	'''
	
	'''
	
	error_report = []
	for hrdict in hrlib:
		for addict in adlib:
			if addict['lastname'] == hrdict['lastname'] and addict['firstname'] == hrdict['firstname']:
				temp_name = hrdict['boss'].split(",")
				temp_location = hrdict['location'][:5]
				error = []
				if addict['email'] != hrdict['email']:
					error.append(hrdict['email'])
					error.append(addict['email'])
				if addict['job'] != hrdict['job']:
					error.append(hrdict['job'])
					error.append(addict['job'])				
				if temp_name[0] not in addict['boss']:
					error.append(hrdict['boss'])
					error.append(addict['boss'])
				if temp_location not in addict['location']:
					error.append(hrdict['location'])
					error.append(addict['location'])						
				record = {
					'lastname': addict['lastname'],
					'firstname': addict['firstname'],
					'errors': error
					}
				#if record['errors']:
				error_report.append(record)
	
	return error_report

	'''
def lib_compare_mismatchednames(hrlib, adlib, errorreport)
	
	for addict in adlib:
		for hrdict in hrlib:
			if addict['lastname'] == hrdict['lastname'] and addict['firstname'] != hrdict['firstname']:
				record = {
					'lastname': addict['lastname'],
					'firstname': addict['firstname'],
					'errors': ""
					}
				errorreport.append(record)
				
	for addict in adlib:
		'''
				
def clear_matches(library_cleared, library_safe):
	for dict1 in library_safe:
			for dict2 in library_cleared:
				if dict2['lastname'] == dict1['lastname'] and dict2['firstname'] == dict1['firstname']:
					library_cleared.remove(dict2)
					
	return library_cleared
				
	
def convert_dict_to_list(lib):
	'''
	'''
	
	temp = []
	for it in lib:
		holder = []
		for this in it:
			holder.append(it[this])
		temp.append(holder)
		
	return temp
	
	
def csv_file_writer(filename, library):
	'''
	Writes the library to the given filename as a CSV file.
	'''
	with open(filename,'w', newline='') as csv_file:
		writer = csv.writer(csv_file)
		for item in library:
			writer.writerow(item)	
			
			
hrlib = hr_build_sort('hrreport.csv')
adlib = ad_build_sort('adreport.csv')

error_report = lib_compare_ifnamesmatch(hrlib, adlib)

clearedadlib = clear_matches(adlib,hrlib)
adlib = ad_build_sort('adreport.csv')
clearedhrlib = clear_matches(hrlib,adlib)

#new_error_report = lib_compare_mismatchednames(hrlib,adlib,error_report)

readable_error = convert_dict_to_list(error_report)
readable_adlib = convert_dict_to_list(clearedadlib)
readable_hrlib = convert_dict_to_list(clearedhrlib)

csv_file_writer('adaudit_errors.csv', readable_error)
csv_file_writer('adlib_mistmatch.csv', readable_adlib)
csv_file_writer('hrlib_mismatch.csv', readable_hrlib)

