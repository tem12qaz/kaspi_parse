from app import app, db
from parse import Parser

if __name__ == '__main__':
    parser = Parser()
    parser.start_parse(db)
    app.run()
