import os
from flask import Flask, render_template, g, request
from dotenv import load_dotenv
from . import db as db_module


def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cambia-esta-clave')
    app.config['DB_HOST'] = os.environ.get('DB_HOST', 'localhost')
    app.config['DB_PORT'] = int(os.environ.get('DB_PORT', 3306))
    app.config['DB_USER'] = os.environ.get('DB_USER', 'root')
    app.config['DB_PASSWORD'] = os.environ.get('DB_PASSWORD', '')
    app.config['DB_NAME'] = os.environ.get('DB_NAME', 'vidplex')
    app.config['BASE_URL'] = os.environ.get('SITE_URL', 'http://127.0.0.1:5000')
    

    # Cookie de sesión del admin: solo por HTTPS y no accesible por JS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'

    db_module.init_app(app)

    @app.after_request
    def _cache_static(response):
        if request.path.startswith('/static/'):
            response.headers['Cache-Control'] = 'public, max-age=86400'
        return response


    from .routes import bp
    app.register_blueprint(bp)

    @app.errorhandler(404)
    def _not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(Exception)
    def _handle_error(e):
        # Cualquier error no controlado (DB caída, timeout, etc.) muestra
        # una página amigable en vez de un traceback en el celular del cliente.
        app.logger.exception('Error no controlado: %s', e)
        db = g.pop('db', None)
        if db is not None:
            try:
                db.close()
            except Exception:
                pass
        return render_template('404.html'), 500

    return app