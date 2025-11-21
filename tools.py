def retrieve_wines():
	"""Return a hardcoded list of wines in the wine cellar.

	Each wine is represented as a dictionary with the following keys:
	- name: wine name
	- producer: winery or producer
	- year: vintage year (int)
	- colour: 'red'|'white'|'rosé'|'sparkling'
	- country_origin: country of origin
	- grape_variety: primary grape or blend description
	- best_meals: list of meal pairing suggestions

	This is intentionally small and static for use as a tool by agents.
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

	return wines


def retrieve_wines_subset(
	colour=None,
	country=None,
	grape=None,
	producer=None,
	year_min=None,
	year_max=None,
	best_meal=None,
	name_contains=None,
	limit=None,
):
	"""Return a filtered subset of wines from the cellar.

	All parameters are optional. Filtering rules:
	- `colour`, `country`, `grape`, `producer`: case-insensitive exact match (grape and producer will check substring)
	- `year_min`, `year_max`: integer bounds inclusive
	- `best_meal`: case-insensitive substring match against any suggested meal
	- `name_contains`: case-insensitive substring match against the wine name
	- `limit`: maximum number of results to return (None = no limit)

	Returns a list of wine dicts (same structure as `retrieve_wines`).
	"""
	wines = retrieve_wines()

	def matches(w):
		if colour and w.get("colour", "").lower() != colour.lower():
			return False
		if country and w.get("country_origin", "").lower() != country.lower():
			return False
		if grape and grape.lower() not in w.get("grape_variety", "").lower():
			return False
		if producer and producer.lower() not in w.get("producer", "").lower():
			return False
		if year_min and w.get("year") < year_min:
			return False
		if year_max and w.get("year") > year_max:
			return False
		if best_meal:
			bm = best_meal.lower()
			meals = [m.lower() for m in w.get("best_meals", [])]
			if not any(bm in m for m in meals):
				return False
		if name_contains and name_contains.lower() not in w.get("name", "").lower():
			return False
		return True

	results = [w for w in wines if matches(w)]

	if limit is not None:
		try:
			n = int(limit)
			if n >= 0:
				results = results[:n]
		except Exception:
			pass

	return results

