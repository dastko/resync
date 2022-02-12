from wsgiref import simple_server
from config import REST_PORT, LOGGER
from app import app

if __name__ == "__main__":
    LOGGER.info(f"Binding on port {REST_PORT}.")

    httpd = simple_server.make_server('0.0.0.0', REST_PORT, app)
    httpd.serve_forever()
