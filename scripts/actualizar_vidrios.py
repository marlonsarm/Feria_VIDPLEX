import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.db import get_db
from vidrios_data_COMPLETO import VIDRIOS

app = create_app()

MEDIA_MAP = {
    "/static/img/vidrios/blanco%202.png": "/static/img/vidrios/blanco%201%20%20HH.png",
    "/static/img/vidrios/azul%20ocean%202.png": "/static/img/vidrios/azul%20ocean%201%20HH.png",
    "/static/img/vidrios/azul%20medium%202.png": "/static/img/vidrios/azul%20medium%201%20HH.png",
    "/static/img/vidrios/violeta%201.png": "/static/img/vidrios/violeta%202%20HH.png",
    "/static/img/vidrios/gris%20asahi%201.png": "/static/img/vidrios/gris%20asahi%202%20HH.png",
    "/static/img/vidrios/verde%20dvh%20estructural%202.png": "/static/img/vidrios/verde%20dvh%20estructural%20%201%20HH.png",
    "/static/img/vidrios/naranja%20tangerin%202.png": "/static/img/vidrios/naranja%20tangerin%201%20HH.png",
    "/static/img/vidrios/verde%20esmeralda%201.jpeg": "/static/img/vidrios/verde%20esmeralda%202%20HH.jpeg",
    "/static/img/vidrios/incoloro%202.png": "/static/img/vidrios/incoloro%201%20HH.png",
    "/static/img/vidrios/rojo%20dip%201.png": "/static/img/vidrios/rojo%20dip%202%20HH.png",
}

with app.app_context():
    db = get_db()
    cur = db.cursor()

    for v in VIDRIOS:
        cur.execute("SELECT id FROM productos WHERE ref_code = %s", (v["ref_code"],))
        existe = cur.fetchone()

        if existe:
            producto_id = existe["id"]
            cur.execute("""
                UPDATE productos 
                SET nombre=%s, tipo_vidrio=%s, descripcion=%s, especificaciones=%s, imagen_principal=%s, categoria=%s, activo=%s
                WHERE ref_code=%s
            """, (v["nombre"], v["tipo_vidrio"], v["descripcion"], v["especificaciones"], v["imagen_principal"], v.get("categoria"), v["activo"], v["ref_code"]))
            print(f"Actualizado: {v['ref_code']}")
        else:
            cur.execute("""
                INSERT INTO productos (ref_code, nombre, tipo_vidrio, descripcion, especificaciones, imagen_principal, categoria, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (v["ref_code"], v["nombre"], v["tipo_vidrio"], v["descripcion"], v["especificaciones"], v["imagen_principal"], v.get("categoria"), v["activo"]))
            producto_id = cur.lastrowid
            print(f"Insertado: {v['ref_code']}")

        en_uso_url = MEDIA_MAP.get(v["imagen_principal"])
        if en_uso_url:
            cur.execute("""
                DELETE FROM producto_media 
                WHERE producto_id=%s AND tipo='imagen' AND orden IN (1,2)
            """, (producto_id,))
            cur.execute("""
                INSERT INTO producto_media (producto_id, tipo, url, orden)
                VALUES (%s, 'imagen', %s, 1)
            """, (producto_id, v["imagen_principal"]))
            cur.execute("""
                INSERT INTO producto_media (producto_id, tipo, url, orden)
                VALUES (%s, 'imagen', %s, 2)
            """, (producto_id, en_uso_url))
            print(f"   -> Media actualizada (Muestra + En uso): {v['ref_code']}")

    db.commit()
    print("Listo. Vidrios y media actualizados.")