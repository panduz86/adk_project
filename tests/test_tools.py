import os
import sys
import pytest

# Ensure project root is on sys.path so tests can import top-level modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools import retrieve_wines, retrieve_wines_subset


def test_retrieve_wines_count_and_structure():
    wines = retrieve_wines()
    assert isinstance(wines, list)
    assert len(wines) == 10
    # Check structure of first item
    w = wines[0]
    for key in ["name", "producer", "year", "colour", "country_origin", "grape_variety", "best_meals"]:
        assert key in w


def test_subset_filter_colour():
    reds = retrieve_wines_subset(colour="red")
    assert all(w["colour"] == "red" for w in reds)


def test_subset_filter_country_and_limit():
    fr = retrieve_wines_subset(country="France", limit=2)
    assert len(fr) <= 2
    assert all(w["country_origin"] == "France" for w in fr)


def test_subset_filter_grape_substring():
    sauv = retrieve_wines_subset(grape="Sauvignon")
    assert any("Sauvignon" in w["grape_variety"] or "sauvignon" in w["grape_variety"].lower() for w in sauv)


def test_subset_year_range():
    r = retrieve_wines_subset(year_min=2015, year_max=2016)
    assert all(2015 <= w["year"] <= 2016 for w in r)


def test_subset_best_meal_matching():
    seafood = retrieve_wines_subset(best_meal="seafood")
    assert any("seafood" in ",".join(m.lower() for m in w["best_meals"]) for w in seafood)


def test_name_contains():
    # Use an ASCII substring that matches the existing data (e.g. 'Margaux')
    res = retrieve_wines_subset(name_contains="Margaux")
    assert any("margaux" in w["name"].lower() for w in res)
