from fastmcp import FastMCP
from datetime import datetime
from typing import Optional
import uuid
import json
import sys
from pathlib import Path

# Add the parent directory to the path to import shared_library
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from wine_cellar.shared_library.wine_data import FAKE_REVIEWS

mcp = FastMCP("Wine Review MCP Server")

# In-memory storage initialized with fake data
REVIEWS = FAKE_REVIEWS.copy()

@mcp.tool()
def create_review(
    wine_name: str,
    vintage: int,
    rating: float,
    tasting_notes: str,
    reviewer_name: str = "Anonymous",
    price: Optional[float] = None
) -> str:
    """
    Create a new wine review.
    
    Args:
        wine_name: Name of the wine
        vintage: Year of the vintage
        rating: Rating from 1-5 stars
        tasting_notes: Detailed tasting notes
        reviewer_name: Name of the reviewer (default: Anonymous)
        price: Optional price of the wine
    
    Returns:
        JSON string with status and data fields
    """
    if not 1 <= rating <= 5:
        return json.dumps({
            "status": "error",
            "data": "Rating must be between 1 and 5"
        })
    
    review_id = str(uuid.uuid4())[:8]
    REVIEWS[review_id] = {
        "id": review_id,
        "wine_name": wine_name,
        "vintage": vintage,
        "rating": rating,
        "tasting_notes": tasting_notes,
        "reviewer_name": reviewer_name,
        "price": price,
        "created_at": datetime.now().isoformat()
    }
    
    return json.dumps({
        "status": "success",
        "data": {
            "message": f"Review created successfully! ID: {review_id}",
            "review_id": review_id
        }
    })


@mcp.tool()
def get_review(review_id: str) -> str:
    """
    Get a specific review by ID.
    
    Args:
        review_id: The unique review identifier
    
    Returns:
        JSON string with status and data fields
    """
    if review_id not in REVIEWS:
        return json.dumps({
            "status": "error",
            "data": f"Review {review_id} not found"
        })
    
    review = REVIEWS[review_id]
    return json.dumps({
        "status": "success",
        "data": review
    })


@mcp.tool()
def list_reviews(
    wine_name: Optional[str] = None,
    min_rating: Optional[float] = None
) -> str:
    """
    List all reviews, optionally filtered.
    
    Args:
        wine_name: Filter by wine name (partial match)
        min_rating: Filter by minimum rating
    
    Returns:
        JSON string with status and data fields
    """
    if not REVIEWS:
        return json.dumps({
            "status": "success",
            "data": {
                "message": "No reviews found in the database.",
                "reviews": [],
                "count": 0
            }
        })
    
    filtered = list(REVIEWS.values())
    
    if wine_name:
        filtered = [r for r in filtered if wine_name.lower() in r['wine_name'].lower()]
    
    if min_rating is not None:
        filtered = [r for r in filtered if r['rating'] >= min_rating]
    
    return json.dumps({
        "status": "success",
        "data": {
            "reviews": filtered,
            "count": len(filtered)
        }
    })


@mcp.tool()
def delete_review(review_id: str) -> str:
    """
    Delete a review by ID.
    
    Args:
        review_id: The unique review identifier
    
    Returns:
        JSON string with status and data fields
    """
    if review_id not in REVIEWS:
        return json.dumps({
            "status": "error",
            "data": f"Review {review_id} not found"
        })
    
    wine_name = REVIEWS[review_id]['wine_name']
    del REVIEWS[review_id]
    return json.dumps({
        "status": "success",
        "data": {
            "message": f"Review {review_id} for '{wine_name}' deleted successfully",
            "review_id": review_id
        }
    })


@mcp.tool()
def get_average_rating(wine_name: str) -> str:
    """
    Get the average rating for a specific wine.
    
    Args:
        wine_name: Name of the wine
    
    Returns:
        JSON string with status and data fields
    """
    matching = [r for r in REVIEWS.values() if wine_name.lower() in r['wine_name'].lower()]
    
    if not matching:
        return json.dumps({
            "status": "error",
            "data": f"No reviews found for '{wine_name}'"
        })
    
    avg_rating = sum(r['rating'] for r in matching) / len(matching)
    return json.dumps({
        "status": "success",
        "data": {
            "wine_name": wine_name,
            "average_rating": round(avg_rating, 2),
            "review_count": len(matching)
        }
    })


@mcp.tool()
def search_reviews(keyword: str) -> str:
    """
    Search reviews by keywords in tasting notes.
    
    Args:
        keyword: Keyword to search for in tasting notes
    
    Returns:
        JSON string with status and data fields
    """
    matching = [
        r for r in REVIEWS.values() 
        if keyword.lower() in r['tasting_notes'].lower()
    ]
    
    if not matching:
        return json.dumps({
            "status": "success",
            "data": {
                "message": f"No reviews found containing '{keyword}'",
                "reviews": [],
                "count": 0
            }
        })
    
    return json.dumps({
        "status": "success",
        "data": {
            "keyword": keyword,
            "reviews": matching,
            "count": len(matching)
        }
    })



if __name__ == "__main__":
    mcp.run(transport="http", port=8002)