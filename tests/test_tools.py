import os
import sys
import pytest

# Ensure project root is on sys.path so tests can import top-level modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools import retrieve_wines


def test_retrieve_wines_count_and_structure():
    wines = retrieve_wines()
    assert "status" in wines
    assert wines["status"] == "success"
    assert "data" in wines
    assert isinstance(wines["data"], list)
    assert len(wines["data"]) == 10
    # Check structure of first item
    w = wines["data"][0]
    for key in ["name", "producer", "year", "colour", "country_origin", "grape_variety", "best_meals"]:
        assert key in w
