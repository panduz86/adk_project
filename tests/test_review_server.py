import os
import sys
import pytest
import json
from datetime import datetime

# Ensure project root is on sys.path so tests can import top-level modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wine_cellar.mcp_servers import review_server

# Access the underlying functions from the MCP tools
def get_tool_function(tool_name):
    """Helper to get the underlying function from an MCP tool"""
    tool = getattr(review_server, tool_name)
    # FastMCP tools have the original function in the 'fn' attribute
    return tool.fn if hasattr(tool, 'fn') else tool


@pytest.fixture
def reset_reviews():
    """Reset REVIEWS to original state before each test"""
    from wine_cellar.shared_library.wine_data import FAKE_REVIEWS
    review_server.REVIEWS = FAKE_REVIEWS.copy()
    yield
    # Cleanup after test
    review_server.REVIEWS = FAKE_REVIEWS.copy()


class TestCreateReview:
    """Tests for create_review function"""
    
    def test_create_review_success(self, reset_reviews):
        create_review_fn = get_tool_function('create_review')
        result = create_review_fn(
            wine_name="Test Wine",
            vintage=2020,
            rating=4.5,
            tasting_notes="Excellent wine with fruity notes",
            reviewer_name="Test Reviewer",
            price=50.0
        )
        
        data = json.loads(result)
        assert data["status"] == "success"
        assert "review_id" in data["data"]
        assert "created successfully" in data["data"]["message"]
        
        # Verify the review was actually added
        review_id = data["data"]["review_id"]
        assert review_id in review_server.REVIEWS
        assert review_server.REVIEWS[review_id]["wine_name"] == "Test Wine"
        assert review_server.REVIEWS[review_id]["rating"] == 4.5
    
    def test_create_review_with_defaults(self, reset_reviews):
        create_review_fn = get_tool_function('create_review')
        result = create_review_fn(
            wine_name="Another Test Wine",
            vintage=2019,
            rating=3.5,
            tasting_notes="Good wine"
        )
        
        data = json.loads(result)
        assert data["status"] == "success"
        review_id = data["data"]["review_id"]
        assert review_server.REVIEWS[review_id]["reviewer_name"] == "Anonymous"
        assert review_server.REVIEWS[review_id]["price"] is None
    
    def test_create_review_invalid_rating_too_low(self, reset_reviews):
        create_review_fn = get_tool_function('create_review')
        result = create_review_fn(
            wine_name="Bad Rating Wine",
            vintage=2020,
            rating=0.5,
            tasting_notes="Test notes"
        )
        
        data = json.loads(result)
        assert data["status"] == "error"
        assert "Rating must be between 1 and 5" in data["data"]
    
    def test_create_review_invalid_rating_too_high(self, reset_reviews):
        create_review_fn = get_tool_function('create_review')
        result = create_review_fn(
            wine_name="Bad Rating Wine",
            vintage=2020,
            rating=5.5,
            tasting_notes="Test notes"
        )
        
        data = json.loads(result)
        assert data["status"] == "error"
        assert "Rating must be between 1 and 5" in data["data"]
    
    def test_create_review_has_timestamp(self, reset_reviews):
        create_review_fn = get_tool_function('create_review')
        result = create_review_fn(
            wine_name="Timestamp Test Wine",
            vintage=2021,
            rating=4.0,
            tasting_notes="Testing timestamp"
        )
        
        data = json.loads(result)
        review_id = data["data"]["review_id"]
        created_at = review_server.REVIEWS[review_id]["created_at"]
        
        # Verify timestamp is in ISO format and recent
        datetime.fromisoformat(created_at)  # Should not raise exception


class TestGetReview:
    """Tests for get_review function"""
    
    def test_get_review_success(self, reset_reviews):
        get_review_fn = get_tool_function('get_review')
        result = get_review_fn("rev001")
        
        data = json.loads(result)
        assert data["status"] == "success"
        assert data["data"]["id"] == "rev001"
        assert data["data"]["wine_name"] == "Château Margaux"
        assert data["data"]["rating"] == 5.0
    
    def test_get_review_not_found(self, reset_reviews):
        get_review_fn = get_tool_function('get_review')
        result = get_review_fn("nonexistent")
        
        data = json.loads(result)
        assert data["status"] == "error"
        assert "not found" in data["data"]


class TestListReviews:
    """Tests for list_reviews function"""
    
    def test_list_reviews_all(self, reset_reviews):
        list_reviews_fn = get_tool_function('list_reviews')
        result = list_reviews_fn()
        
        data = json.loads(result)
        assert data["status"] == "success"
        assert "reviews" in data["data"]
        assert data["data"]["count"] > 0
        assert len(data["data"]["reviews"]) == data["data"]["count"]
    
    def test_list_reviews_filter_by_wine_name(self, reset_reviews):
        list_reviews_fn = get_tool_function('list_reviews')
        result = list_reviews_fn(wine_name="Barolo")
        
        data = json.loads(result)
        assert data["status"] == "success"
        assert data["data"]["count"] >= 2  # We know there are at least 2 Barolo reviews
        for review in data["data"]["reviews"]:
            assert "barolo" in review["wine_name"].lower()
    
    def test_list_reviews_filter_by_min_rating(self, reset_reviews):
        list_reviews_fn = get_tool_function('list_reviews')
        result = list_reviews_fn(min_rating=4.5)
        
        data = json.loads(result)
        assert data["status"] == "success"
        for review in data["data"]["reviews"]:
            assert review["rating"] >= 4.5
    
    def test_list_reviews_filter_by_both(self, reset_reviews):
        list_reviews_fn = get_tool_function('list_reviews')
        result = list_reviews_fn(wine_name="Château Margaux", min_rating=4.5)
        
        data = json.loads(result)
        assert data["status"] == "success"
        for review in data["data"]["reviews"]:
            assert "château margaux" in review["wine_name"].lower()
            assert review["rating"] >= 4.5
    
    def test_list_reviews_empty_results(self, reset_reviews):
        # Clear all reviews
        review_server.REVIEWS = {}
        list_reviews_fn = get_tool_function('list_reviews')
        result = list_reviews_fn()
        
        data = json.loads(result)
        assert data["status"] == "success"
        assert data["data"]["count"] == 0
        assert data["data"]["reviews"] == []
        assert "No reviews found" in data["data"]["message"]
    
    def test_list_reviews_no_matches(self, reset_reviews):
        list_reviews_fn = get_tool_function('list_reviews')
        result = list_reviews_fn(wine_name="NonExistent Wine")
        
        data = json.loads(result)
        assert data["status"] == "success"
        assert data["data"]["count"] == 0


class TestDeleteReview:
    """Tests for delete_review function"""
    
    def test_delete_review_success(self, reset_reviews):
        # Verify review exists first
        assert "rev001" in review_server.REVIEWS
        
        delete_review_fn = get_tool_function('delete_review')
        result = delete_review_fn("rev001")
        
        data = json.loads(result)
        assert data["status"] == "success"
        assert "deleted successfully" in data["data"]["message"]
        assert data["data"]["review_id"] == "rev001"
        
        # Verify review was actually deleted
        assert "rev001" not in review_server.REVIEWS
    
    def test_delete_review_not_found(self, reset_reviews):
        delete_review_fn = get_tool_function('delete_review')
        result = delete_review_fn("nonexistent")
        
        data = json.loads(result)
        assert data["status"] == "error"
        assert "not found" in data["data"]


class TestGetAverageRating:
    """Tests for get_average_rating function"""
    
    def test_get_average_rating_success(self, reset_reviews):
        get_average_rating_fn = get_tool_function('get_average_rating')
        result = get_average_rating_fn("Château Margaux")
        
        data = json.loads(result)
        assert data["status"] == "success"
        assert "average_rating" in data["data"]
        assert data["data"]["review_count"] >= 2
        # Check that average is calculated correctly (we know there are 5.0 and 4.5 ratings)
        assert 4.5 <= data["data"]["average_rating"] <= 5.0
    
    def test_get_average_rating_single_review(self, reset_reviews):
        get_average_rating_fn = get_tool_function('get_average_rating')
        result = get_average_rating_fn("Malbec Reserva")
        
        data = json.loads(result)
        assert data["status"] == "success"
        assert data["data"]["review_count"] == 1
        assert data["data"]["average_rating"] == 4.6
    
    def test_get_average_rating_not_found(self, reset_reviews):
        get_average_rating_fn = get_tool_function('get_average_rating')
        result = get_average_rating_fn("NonExistent Wine")
        
        data = json.loads(result)
        assert data["status"] == "error"
        assert "No reviews found" in data["data"]
    
    def test_get_average_rating_case_insensitive(self, reset_reviews):
        get_average_rating_fn = get_tool_function('get_average_rating')
        result = get_average_rating_fn("barolo")
        
        data = json.loads(result)
        assert data["status"] == "success"
        assert data["data"]["review_count"] >= 2


class TestSearchReviews:
    """Tests for search_reviews function"""
    
    def test_search_reviews_success(self, reset_reviews):
        search_reviews_fn = get_tool_function('search_reviews')
        result = search_reviews_fn("truffle")
        
        data = json.loads(result)
        assert data["status"] == "success"
        assert data["data"]["count"] >= 1
        assert data["data"]["keyword"] == "truffle"
        for review in data["data"]["reviews"]:
            assert "truffle" in review["tasting_notes"].lower()
    
    def test_search_reviews_no_results(self, reset_reviews):
        search_reviews_fn = get_tool_function('search_reviews')
        result = search_reviews_fn("nonexistentkeyword")
        
        data = json.loads(result)
        assert data["status"] == "success"
        assert data["data"]["count"] == 0
        assert data["data"]["reviews"] == []
        assert "No reviews found" in data["data"]["message"]
    
    def test_search_reviews_case_insensitive(self, reset_reviews):
        search_reviews_fn = get_tool_function('search_reviews')
        result = search_reviews_fn("CITRUS")
        
        data = json.loads(result)
        assert data["status"] == "success"
        assert data["data"]["count"] >= 1
        for review in data["data"]["reviews"]:
            assert "citrus" in review["tasting_notes"].lower()
    
    def test_search_reviews_partial_match(self, reset_reviews):
        search_reviews_fn = get_tool_function('search_reviews')
        result = search_reviews_fn("fruit")
        
        data = json.loads(result)
        assert data["status"] == "success"
        # Should match "fruit", "fruity", "tropical fruit", etc.
        assert data["data"]["count"] >= 1


class TestIntegrationScenarios:
    """Integration tests simulating real-world usage"""
    
    def test_create_and_retrieve_review(self, reset_reviews):
        # Create a review
        create_review_fn = get_tool_function('create_review')
        get_review_fn = get_tool_function('get_review')
        create_result = create_review_fn(
            wine_name="Integration Test Wine",
            vintage=2022,
            rating=4.2,
            tasting_notes="Testing integration with vanilla notes",
            reviewer_name="Integration Tester",
            price=45.0
        )
        
        create_data = json.loads(create_result)
        review_id = create_data["data"]["review_id"]
        
        # Retrieve it
        get_result = get_review_fn(review_id)
        get_data = json.loads(get_result)
        
        assert get_data["status"] == "success"
        assert get_data["data"]["wine_name"] == "Integration Test Wine"
        assert get_data["data"]["rating"] == 4.2
    
    def test_create_list_and_delete_workflow(self, reset_reviews):
        create_review_fn = get_tool_function('create_review')
        list_reviews_fn = get_tool_function('list_reviews')
        delete_review_fn = get_tool_function('delete_review')
        
        initial_count_result = list_reviews_fn()
        initial_count = json.loads(initial_count_result)["data"]["count"]
        
        # Create
        create_result = create_review_fn(
            wine_name="Workflow Test Wine",
            vintage=2021,
            rating=3.8,
            tasting_notes="Workflow test notes"
        )
        review_id = json.loads(create_result)["data"]["review_id"]
        
        # List (should have one more)
        list_result = list_reviews_fn()
        list_data = json.loads(list_result)
        assert list_data["data"]["count"] == initial_count + 1
        
        # Delete
        delete_result = delete_review_fn(review_id)
        assert json.loads(delete_result)["status"] == "success"
        
        # List again (should be back to original count)
        final_list_result = list_reviews_fn()
        final_count = json.loads(final_list_result)["data"]["count"]
        assert final_count == initial_count
    
    def test_multiple_reviews_average_calculation(self, reset_reviews):
        wine_name = "Multi Review Test Wine"
        create_review_fn = get_tool_function('create_review')
        get_average_rating_fn = get_tool_function('get_average_rating')
        
        # Create multiple reviews
        create_review_fn(wine_name, 2020, 4.0, "First review")
        create_review_fn(wine_name, 2020, 5.0, "Second review")
        create_review_fn(wine_name, 2020, 3.0, "Third review")
        
        # Check average
        avg_result = get_average_rating_fn(wine_name)
        avg_data = json.loads(avg_result)
        
        assert avg_data["status"] == "success"
        assert avg_data["data"]["review_count"] == 3
        assert avg_data["data"]["average_rating"] == 4.0  # (4+5+3)/3 = 4.0
