"""
Shared wine and review data for the wine cellar system.
Used by both tools.py and review_server.py
"""

WINES = [
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

# Fake reviews for the wines
FAKE_REVIEWS = {
    "rev001": {
        "id": "rev001",
        "wine_name": "Château Margaux",
        "vintage": 2015,
        "rating": 5.0,
        "tasting_notes": "Exceptional complexity with notes of blackcurrant, cedar, and tobacco. Silky tannins and a long, elegant finish. A masterpiece from Margaux.",
        "reviewer_name": "Sophie Dubois",
        "price": 450.0,
        "created_at": "2023-08-15T14:30:00"
    },
    "rev002": {
        "id": "rev002",
        "wine_name": "Château Margaux",
        "vintage": 2015,
        "rating": 4.5,
        "tasting_notes": "Beautiful structure with ripe fruit and elegant oak integration. Needs a few more years to fully open up.",
        "reviewer_name": "James Wilson",
        "price": 445.0,
        "created_at": "2024-02-10T19:45:00"
    },
    "rev003": {
        "id": "rev003",
        "wine_name": "Sassicaia",
        "vintage": 2016,
        "rating": 4.8,
        "tasting_notes": "Bold and powerful with layers of dark berries, graphite, and Mediterranean herbs. Classic Super Tuscan excellence.",
        "reviewer_name": "Marco Rossi",
        "price": 220.0,
        "created_at": "2023-11-22T16:20:00"
    },
    "rev004": {
        "id": "rev004",
        "wine_name": "Cloudy Bay Sauvignon Blanc",
        "vintage": 2020,
        "rating": 4.3,
        "tasting_notes": "Vibrant and fresh with tropical fruit, passion fruit, and citrus notes. Crisp acidity makes it perfect for seafood.",
        "reviewer_name": "Emma Thompson",
        "price": 35.0,
        "created_at": "2023-06-05T12:15:00"
    },
    "rev005": {
        "id": "rev005",
        "wine_name": "Riesling Kabinett",
        "vintage": 2018,
        "rating": 4.6,
        "tasting_notes": "Perfectly balanced sweet and sour with notes of green apple, lime, and petrol. Outstanding minerality and length.",
        "reviewer_name": "Hans Mueller",
        "price": 28.0,
        "created_at": "2024-01-18T10:30:00"
    },
    "rev006": {
        "id": "rev006",
        "wine_name": "Champagne Brut",
        "vintage": 2014,
        "rating": 4.9,
        "tasting_notes": "Exquisite mousse with brioche, toasted almond, and citrus. Creamy texture and persistent bubbles. Celebration in a glass!",
        "reviewer_name": "Charlotte Laurent",
        "price": 85.0,
        "created_at": "2023-12-31T20:00:00"
    },
    "rev007": {
        "id": "rev007",
        "wine_name": "Barolo",
        "vintage": 2013,
        "rating": 4.7,
        "tasting_notes": "Classic Nebbiolo character with rose petal, tar, and red cherry. Firm tannins softening beautifully. Pairs wonderfully with truffle pasta.",
        "reviewer_name": "Giuseppe Bianchi",
        "price": 95.0,
        "created_at": "2024-03-12T18:45:00"
    },
    "rev008": {
        "id": "rev008",
        "wine_name": "Priorat Garnacha",
        "vintage": 2017,
        "rating": 4.4,
        "tasting_notes": "Intense and concentrated with dark fruit, licorice, and mineral notes. Powerful yet refined with a long finish.",
        "reviewer_name": "Carlos García",
        "price": 65.0,
        "created_at": "2023-09-28T15:10:00"
    },
    "rev009": {
        "id": "rev009",
        "wine_name": "Chablis",
        "vintage": 2019,
        "rating": 4.5,
        "tasting_notes": "Pure and precise with green apple, lemon zest, and flinty minerality. Unoaked Chardonnay at its finest.",
        "reviewer_name": "Pierre Moreau",
        "price": 42.0,
        "created_at": "2023-07-14T13:25:00"
    },
    "rev010": {
        "id": "rev010",
        "wine_name": "Rosé Provence",
        "vintage": 2021,
        "rating": 4.2,
        "tasting_notes": "Delicate pale pink color with notes of strawberry, watermelon, and white flowers. Refreshing and perfect for summer.",
        "reviewer_name": "Isabelle Petit",
        "price": 30.0,
        "created_at": "2023-05-20T11:00:00"
    },
    "rev011": {
        "id": "rev011",
        "wine_name": "Malbec Reserva",
        "vintage": 2018,
        "rating": 4.6,
        "tasting_notes": "Rich and velvety with plum, blackberry, and hints of chocolate. Full-bodied with smooth tannins. Excellent value!",
        "reviewer_name": "Diego Fernández",
        "price": 38.0,
        "created_at": "2024-04-08T17:30:00"
    },
    "rev012": {
        "id": "rev012",
        "wine_name": "Barolo",
        "vintage": 2013,
        "rating": 5.0,
        "tasting_notes": "Absolutely stunning! Ethereal aromatics of rose, truffle, and dried cherry. Complex, elegant, and age-worthy. A profound wine.",
        "reviewer_name": "Lucia Ferrero",
        "price": 98.0,
        "created_at": "2023-10-15T19:00:00"
    },
    "rev013": {
        "id": "rev013",
        "wine_name": "Cloudy Bay Sauvignon Blanc",
        "vintage": 2020,
        "rating": 4.0,
        "tasting_notes": "Good expression of Marlborough Sauvignon Blanc with typical grassy notes and citrus. Clean and refreshing finish.",
        "reviewer_name": "Sarah Mitchell",
        "price": 33.0,
        "created_at": "2024-05-03T14:20:00"
    }
}
