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
	wines = [
		{
			"name": "Château Margaux",
			"producer": "Château Margaux",
			"year": 2015,
			"colour": "red",
			"country_origin": "France",
			"grape_variety": "Cabernet Sauvignon-Merlot blend",
			"best_meals": ["roast beef", "lamb", "mature cheeses"]
		},
		{
			"name": "Sassicaia",
			"producer": "Tenuta San Guido",
			"year": 2016,
			"colour": "red",
			"country_origin": "Italy",
			"grape_variety": "Cabernet Sauvignon-Cabernet Franc",
			"best_meals": ["grilled steak", "game", "tomato-based pasta"]
		},
		{
			"name": "Cloudy Bay Sauvignon Blanc",
			"producer": "Cloudy Bay",
			"year": 2020,
			"colour": "white",
			"country_origin": "New Zealand",
			"grape_variety": "Sauvignon Blanc",
			"best_meals": ["seafood", "goat cheese", "fresh salads"]
		},
		{
			"name": "Riesling Kabinett",
			"producer": "Dr. Loosen",
			"year": 2018,
			"colour": "white",
			"country_origin": "Germany",
			"grape_variety": "Riesling",
			"best_meals": ["spicy Asian food", "pork", "light fish dishes"]
		},
		{
			"name": "Champagne Brut",
			"producer": "Bollinger",
			"year": 2014,
			"colour": "sparkling",
			"country_origin": "France",
			"grape_variety": "Chardonnay-Pinot Noir-Pinot Meunier",
			"best_meals": ["oysters", "fried chicken", "celebrations"]
		},
		{
			"name": "Barolo",
			"producer": "G.D. Vajra",
			"year": 2013,
			"colour": "red",
			"country_origin": "Italy",
			"grape_variety": "Nebbiolo",
			"best_meals": ["truffle dishes", "braised beef", "aged cheeses"]
		},
		{
			"name": "Priorat Garnacha",
			"producer": "Clos Mogador",
			"year": 2017,
			"colour": "red",
			"country_origin": "Spain",
			"grape_variety": "Garnacha (Grenache) blend",
			"best_meals": ["barbecue", "stews", "strong cheeses"]
		},
		{
			"name": "Chablis",
			"producer": "Domaine William Fèvre",
			"year": 2019,
			"colour": "white",
			"country_origin": "France",
			"grape_variety": "Chardonnay",
			"best_meals": ["shellfish", "light fish", "creamy sauces"]
		},
		{
			"name": "Rosé Provence",
			"producer": "Domaines Ott",
			"year": 2021,
			"colour": "rosé",
			"country_origin": "France",
			"grape_variety": "Cinsault-Grenache-Syrah blend",
			"best_meals": ["Mediterranean salads", "grilled vegetables", "light seafood"]
		},
		{
			"name": "Malbec Reserva",
			"producer": "Catena Zapata",
			"year": 2018,
			"colour": "red",
			"country_origin": "Argentina",
			"grape_variety": "Malbec",
			"best_meals": ["grilled red meat", "empanadas", "spicy sausages"]
		}
	]

	result = {
		"status" : "success",
		"data" : wines
	}
	return result


