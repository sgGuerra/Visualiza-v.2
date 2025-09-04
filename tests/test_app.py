import sys
import os
sys.path.append("src")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from controllers.constructor import app

def test_app_creation():
    """Test that the Flask app is created successfully"""
    assert app is not None
    assert app.name == 'src.controllers.app'
    print("PASS: Flask app creation test passed")

def test_routes():
    """Test that routes are registered correctly"""
    with app.test_client() as client:
        # Test the index route
        response = client.get('/')
        assert response.status_code == 200
        print("PASS: Index route test passed")

if __name__ == "__main__":
    test_app_creation()
    test_routes()
    print("All tests passed!")
