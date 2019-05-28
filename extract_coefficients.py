from xml.dom import minidom
import os
import activation



def extract ():
	# download_location = "downloads"
	download_location = "output"
	search_list = activation.request_search_list()
	print search_list
	coeffs_for_assets = []
	for search in search_list:
		metadata_files = {}
		for file in os.listdir(download_location + "/" + search['item_id'] + "/" ):
		    if file.endswith(".xml"):
		        metadata_files[os.path.splitext(file)[0]] = os.path.join(download_location + "/" + search['item_id'] + "/", file)

		print metadata_files

		coeffs_values = {}
		for key,metadata in metadata_files.items():
			xmldoc = minidom.parse(metadata)
			nodes = xmldoc.getElementsByTagName("ps:bandSpecificMetadata")

			# XML parser refers to bands by numbers 1-4
			coeffs = {}
			for node in nodes:
			    bn = node.getElementsByTagName("ps:bandNumber")[0].firstChild.data
			    if bn in ['1', '2', '3', '4']:
			        i = int(bn)
			        value = node.getElementsByTagName("ps:reflectanceCoefficient")[0].firstChild.data
			        coeffs[i] = float(value)

			print "Conversion coefficients:", coeffs
			coeffs_values[search['item_id']] = coeffs
		coeffs_for_assets.append(coeffs_values)
	print coeffs_for_assets
	return coeffs_for_assets
