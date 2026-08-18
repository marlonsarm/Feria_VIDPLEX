"""
Borra DEFINITIVAMENTE los 30 vidrios genéricos de prueba
(design, confort, control-solar, seguridad, alto-desempeno originales),
dejando solo los reales que se cargaron después.

Borra primero cualquier registro relacionado (escaneos, vínculos con
leads) para no violar las llaves foráneas, y al final borra el
producto en sí. Es IRREVERSIBLE.

Uso:
    python scripts/borrar_vidrios_genericos.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.db import get_db

app = create_app()

REF_CODES_A_BORRAR = [
    # Refrigeracion (categoria eliminada por completo)
    "VP-013", "VP-014", "VP-015", "VP-016", "VP-017", "VP-018",
]

with app.app_context():
    db = get_db()
    cur = db.cursor()

    placeholders = ", ".join(["%s"] * len(REF_CODES_A_BORRAR))

    cur.execute(
        f"SELECT id, ref_code FROM productos WHERE ref_code IN ({placeholders})",
        REF_CODES_A_BORRAR
    )
    productos = cur.fetchall()
    ids = [p["id"] for p in productos]

    if not ids:
        print("No se encontró ninguno de esos ref_code en la base de datos.")
    else:
        id_placeholders = ", ".join(["%s"] * len(ids))

        cur.execute(f"DELETE FROM lead_producto WHERE producto_id IN ({id_placeholders})", ids)
        print(f"Vínculos con leads borrados: {cur.rowcount}")

        cur.execute(f"DELETE FROM escaneos WHERE producto_id IN ({id_placeholders})", ids)
        print(f"Escaneos borrados: {cur.rowcount}")

        cur.execute(f"DELETE FROM producto_media WHERE producto_id IN ({id_placeholders})", ids)
        print(f"Galería (producto_media) borrada: {cur.rowcount}")

        cur.execute(f"DELETE FROM productos WHERE id IN ({id_placeholders})", ids)
        print(f"Productos borrados: {cur.rowcount}")

        db.commit()
        print(f"\nListo. Se borraron {len(productos)} vidrios genéricos:")
        for p in productos:
            print(f"  - {p['ref_code']}")