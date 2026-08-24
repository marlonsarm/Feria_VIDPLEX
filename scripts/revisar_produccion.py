import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.db import get_db

app = create_app()

with app.app_context():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT p.ref_code, p.nombre, m.orden, m.url
        FROM producto_media m
        JOIN productos p ON p.id = m.producto_id
        WHERE m.tipo = 'imagen'
        ORDER BY p.ref_code, m.orden
    """)
    for row in cur.fetchall():
        print(row)