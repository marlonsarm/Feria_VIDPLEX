import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.db import get_db
from vidrios_data import VIDRIOS

app = create_app()

with app.app_context():
    db = get_db()
    cur = db.cursor()

    for v in VIDRIOS:
        cur.execute("SELECT id FROM productos WHERE ref_code = %s", (v["ref_code"],))
        existe = cur.fetchone()

        if existe:
            cur.execute("""
                UPDATE productos 
                SET nombre=%s, tipo_vidrio=%s, descripcion=%s, especificaciones=%s, imagen_principal=%s, activo=%s
                WHERE ref_code=%s
            """, (v["nombre"], v["tipo_vidrio"], v["descripcion"], v["especificaciones"], v["imagen_principal"], v["activo"], v["ref_code"]))
            print(f"Actualizado: {v['ref_code']}")
        else:
            cur.execute("""
                INSERT INTO productos (ref_code, nombre, tipo_vidrio, descripcion, especificaciones, imagen_principal, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (v["ref_code"], v["nombre"], v["tipo_vidrio"], v["descripcion"], v["especificaciones"], v["imagen_principal"], v["activo"]))
            print(f"Insertado: {v['ref_code']}")

    db.commit()
    print("Listo. Vidrios actualizados.")