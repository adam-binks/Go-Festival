import ast
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
# The database info is stored in sqlite_config.txt, which is not on the GitHub repo
# It's just a dictionary with values for the keys: DATABASE, SECRET_KEY, USERNAME and PASSWORD
with open(url_for('static', filename='sqlite_config.txt')) as f:
    app.config.update(ast.literal_eval(f.read()))  # use ast.literal_eval() to prevent injection of malicious code

app.config.from_envvar('FLASKR_SETTINGS', silent=True)



def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row # so we can use dicts rather than tuples
    return rv


# initialise the database from schema.sql
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as schema:
        db.cursor().executescript(schema.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialised the database')


# open a new database connection if there is none yet for the current application context.
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


# close the db again at the end of a request
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_festivals():
    db = get_db()
    festivals = db.execute('SELECT title, festival_date, location from Festival').fetchall()
    return render_template('show_festivals.html', festivals=festivals)