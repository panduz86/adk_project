from .wine_data import WINES

def retrieve_wines():
	"""Return the list of wines in the wine cellar.

	Each wine is represented as a dictionary with the following keys:
	- name: wine name
	- producer: winery or producer
	- year: vintage year (int)
	- colour: 'red'|'white'|'rosé'|'sparkling'
	- country_origin: country of origin
	- grape_variety: primary grape or blend description
	- best_meals: list of meal pairing suggestions

	Returns a dict with "status" and "data" keys
	"""
	result = {
		"status" : "success",
		"data" : WINES
	}
	return result


