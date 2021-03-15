import requests
import json
import time
import sys
from termcolor import colored

# Center names that provide AZ or MOD only in the area surrounding Bucharest
AZ = ['Centrul Medical Veridia', 'Centrul multifunctional Sf Andrei', 'Circul Metropolitan Bucuresti', 'Grand Arena Mall', 'Institutul National de Endocrinologie C. I. Parhon', 'Centrul Medical Magurele', 'Sala de Sport Chitila', 'Centrul Cultural Aurel Stroe', 'Centrul Medical Mediurg', 'SCOALA GIMNAZIALA GEORGE ENESCU SINAIA - SALA DE SPORT', 'SALA SPORT -MIZIL', 'Centrul de Vaccinare -incinta Ateneu Nicolae Bălănescu Giurgiu', 'Centrul de vaccinare Floresti Stoenesti (containere)', 'Centrul 2_Sala sport - Liceul Viceamiral Ioan Balanescu', 'Centrul 2_CENTRUL DE ZI ARLECHINO TARGOVISTE', 'CENTRUL IMPREUNA VOM REUSI TARGOVISTE', 'SALA DE FESTIVITATI']
MOD = ['CMU REGINA MARIA - Policlinica Cotroceni', 'CMU REGINA MARIA - Policlinica The Light', 'Centru vaccinare Balotesti', 'Dispensar Medical Glina', 'Centru 3_Sala de Sport a Primariei Otopeni', 'Centru de vaccinare local Jilava', 'Primaria Veche Călugăreni', 'SALĂ DE SPORT - Școala Gimnazială - Mihăilești', 'CENTRU DE VACCINARE BALENI', 'CENTRU DE VACCINARE RAZVAD, SALA DE SPORT', 'Centru 3_Spitalul de Pediatrie Ploiesti', 'SALA DE SPORT BUCOV']

cookie = 'NTNlMzRhMzYtYTExYS00NWU4LTg1MmItMTcxNTU1YWY3ZmI5'
identificationCode = '1980618460030'
recipientID = '4376821'
countyID = 'null'
localityID = 'null'

total = 510
page = 0
found = False
MAX_PER_PAGE = 20

counties = {
	59: 'B/IF',
	52: 'GR',
	29: 'PH',
	15: 'DB',
	51: 'CL',
	10: 'BZ',
	3: 'AG'
}

names = {
	'B/IF': 59,
	'GR': 52,
	'PH': 29,
	'DB': 15,
	'CL': 51,
	'BZ': 10,
	'AG': 3
}

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
	"accept": "application/json, text/plain, */*",
	"accept-encoding": "gzip, deflate, br",
	"accept-language": "ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7",
	"content-type": "application/json",
	"sec-ch-ua": '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
	"sec-ch-ua-mobile": "?0",
	"sec-fetch-dest": "empty",
	"sec-fetch-mode": "cors",
	"sec-fetch-site": "same-origin",
	"cookie": "SESSION=" + cookie,
	"Referer": "https://programare.vaccinare-covid.gov.ro/",
	"Referrer-Policy": "strict-origin-when-cross-origin",
	"origin": "https://programare.vaccinare-covid.gov.ro",
}

# If no parameter is provided, look up all counties
if len(sys.argv) == 2:
	if sys.argv[1] not in names:
		print("Parameter should be one of: B/IF, GR, PH, DB, CL, AG, BZ")
		exit()
	countyID = names[sys.argv[1]]

while True:
	data = '{"countyID":' + str(countyID) + ',"localityID":' + localityID + ',"name":null,"identificationCode":"' + identificationCode + '","masterPersonnelCategoryID":-4,"personnelCategoryID":32,"recipientID":' + recipientID + '}'
	
	# Query MAX_PER_PAGE results at a time (API limit)
	while (page * MAX_PER_PAGE) < total:
		url = 'https://programare.vaccinare-covid.gov.ro/scheduling/api/centres?page=' + str(page) + '&size=' + str(MAX_PER_PAGE) + '&sort=,'
		r = requests.post(url, data=data, headers=headers)
		results = r.json()

		# Iterate results and find avaialble slots
		for result in results['content']:
			if result['availableSlots'] != 0:
			
				# Determine the type of vaccine
				if result['name'] in AZ:
					print("<AZ>", end=' ')
				elif result['name'] in MOD:
					print("<MOD>", end=' ')
				elif countyID != 'null':
					print(colored('<PFZ>', 'red'), end=' ')
					print('\a', end=' ')
				else:
					print('<?>', end=' ')
					
				# Print details about the identified entry
				print("Slots:", result['availableSlots'], "->", "Judet:", result['countyName'] + ",", result['name'])
				found = True
			
		page += 1
	
	# No results found
	if not found:
		print('[' + counties[countyID] + '] No results')
	print('-------------------------------------------')
	
	found = False
	page = 0
	# Delay
	#time.sleep(5)



