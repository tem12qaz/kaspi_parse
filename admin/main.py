from werkzeug.middleware.dispatcher import DispatcherMiddleware

from app import app, db
from parse import Parser


app.config["APPLICATION_ROOT"] = "/kaspi"


def simple(env, resp):
    resp(b'200 OK', [(b'Content-Type', b'text/plain')])
    return [b'Hello WSGI World']


if __name__ == '__main__':
    app.wsgi_app = DispatcherMiddleware(simple, {'/kaspi': app.wsgi_app})
    parser = Parser()
    parser.start_parse(db)
    app.run(port=5001)
