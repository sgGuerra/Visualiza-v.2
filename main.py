import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
from views.interfaz_view import InterfazView

def main():
    app = InterfazView()
    app.iniciar()

if __name__ == "__main__":
    main()