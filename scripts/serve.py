import sys
from pathlib import Path
from wsgiref.simple_server import make_server

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from passenger_wsgi import application


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    print(f"Serving Global Consult at http://{host}:{port}")
    make_server(host, port, application).serve_forever()
