import sys 
sys.path.append("src")
from controllers.constructor import app

if __name__ == "__main__":
    app.run(debug=True)
