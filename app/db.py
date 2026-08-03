import pymysql
import pymysql.cursors
from flask import g, current_app


def get_db():
    """Devuelve la conexión MySQL de este request (la crea si no existe)."""
    if 'db' not in g:
     g.db = pymysql.connect(
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_NAME'],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
            charset='utf8mb4',
            connect_timeout=5,
            read_timeout=8,
            write_timeout=8,
        )
    else:
        # La conexión puede llevar rato abierta (mismo worker, requests seguidos).
        # Si el servidor MySQL la cerró por inactividad, reconectamos en vez de fallar.
        try:
            g.db.ping(reconnect=True)
        except Exception:
            g.pop('db', None)
            return get_db()
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
