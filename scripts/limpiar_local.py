"""
Borra TODOS los productos de la base de datos LOCAL y los reemplaza
por los 41 vidrios reales (los mismos que ya están en producción,
ya actualizados con los nombres/categorías correctos).

OJO: este script está pensado para correr con el .env apuntando a
localhost (tu base de datos local de pruebas). NO lo corras con el
.env apuntando a Railway/producción, o borrarías los datos reales.

Uso:
    python scripts/limpiar_local.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.db import get_db
from vidrios_data_COMPLETO import VIDRIOS

app = create_app()

with app.app_context():
    db = get_db()
    cur = db.cursor()

    # Seguridad: confirmar que estamos en localhost antes de borrar nada
    host = app.config.get('DB_HOST', '')
    if 'railway' in host.lower() or 'rlwy' in host.lower() or 'proxy' in host.lower():
        print(f"DETENIDO: el DB_HOST actual es '{host}', parece ser producción.")
        print("Este script solo debe correr contra tu base de datos LOCAL.")
        sys.exit(1)

    print(f"Conectado a: {host} (se ve como base local, continuando...)")

    cur.execute("SELECT COUNT(*) as total FROM productos")
    antes = cur.fetchone()['total']
    print(f"Productos antes de limpiar: {antes}")

    # Borra todo lo que exista en la tabla
    cur.execute("DELETE FROM productos")
    print("Tabla productos vaciada.")

    # Vuelve a insertar solo los 41 correctos
    for v in VIDRIOS:
        cur.execute("""
            INSERT INTO productos (ref_code, nombre, tipo_vidrio, descripcion, especificaciones, imagen_principal, categoria, activo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (v["ref_code"], v["nombre"], v["tipo_vidrio"], v["descripcion"], v["especificaciones"], v["imagen_principal"], v.get("categoria"), v["activo"]))

    db.commit()

    cur.execute("SELECT COUNT(*) as total FROM productos")
    despues = cur.fetchone()['total']
    print(f"Productos después de limpiar: {despues}")
    print("Listo. Base de datos local sincronizada con los 41 vidrios reales.")
    