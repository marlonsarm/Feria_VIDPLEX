"""
PASO FINAL: deja el catalogo solo con los 41 vidrios reales,
numerados de forma simple VP-001 a VP-041.

1) Borra definitivamente los 30 vidrios genericos de prueba
   (los que tenian codigo entre VP-001 y VP-036).
2) Renombra los 41 vidrios reales (actualmente VP-037 a VP-077)
   para que queden VP-001 a VP-041, en el mismo orden.

Uso:
    python scripts/finalizar_catalogo.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.db import get_db

app = create_app()

# Los 30 genericos que hay que borrar (VP-013 a VP-018 de refrigeracion
# ya se borraron antes, no hace falta repetirlos aqui).
GENERICOS_A_BORRAR = [
    "VP-001", "VP-002", "VP-003", "VP-004", "VP-005", "VP-006",
    "VP-007", "VP-008", "VP-009", "VP-010", "VP-011", "VP-012",
    "VP-019", "VP-020", "VP-021", "VP-022", "VP-023", "VP-024",
    "VP-025", "VP-026", "VP-027", "VP-028", "VP-029", "VP-030",
    "VP-031", "VP-032", "VP-033", "VP-034", "VP-035", "VP-036",
]

with app.app_context():
    db = get_db()
    cur = db.cursor()

    # --- Paso 1: borrar los 30 genericos (y sus referencias) ---
    placeholders = ", ".join(["%s"] * len(GENERICOS_A_BORRAR))
    cur.execute(f"SELECT id, ref_code FROM productos WHERE ref_code IN ({placeholders})", GENERICOS_A_BORRAR)
    genericos = cur.fetchall()
    ids_genericos = [p["id"] for p in genericos]

    if ids_genericos:
        id_placeholders = ", ".join(["%s"] * len(ids_genericos))
        cur.execute(f"DELETE FROM lead_producto WHERE producto_id IN ({id_placeholders})", ids_genericos)
        cur.execute(f"DELETE FROM escaneos WHERE producto_id IN ({id_placeholders})", ids_genericos)
        cur.execute(f"DELETE FROM producto_media WHERE producto_id IN ({id_placeholders})", ids_genericos)
        cur.execute(f"DELETE FROM productos WHERE id IN ({id_placeholders})", ids_genericos)
        db.commit()
        print(f"Borrados {len(genericos)} vidrios genericos.")
    else:
        print("No se encontraron vidrios genericos para borrar (puede que ya estuvieran borrados).")

    # --- Paso 2: renumerar los 41 reales de VP-037..VP-077 a VP-001..VP-041 ---
    cur.execute(
        "SELECT id, ref_code FROM productos WHERE ref_code BETWEEN 'VP-037' AND 'VP-077' ORDER BY ref_code"
    )
    reales = cur.fetchall()

    if len(reales) != 41:
        print(f"\nADVERTENCIA: se esperaban 41 vidrios reales, se encontraron {len(reales)}.")
        print("Se van a renumerar los que se encontraron, en orden, empezando en VP-001.")

    print(f"\nRenumerando {len(reales)} vidrios reales...")
    for i, p in enumerate(reales, start=1):
        nuevo_code = f"VP-{i:03d}"
        cur.execute("UPDATE productos SET ref_code = %s WHERE id = %s", (nuevo_code, p["id"]))
        print(f"  {p['ref_code']} -> {nuevo_code}")

    db.commit()
    print(f"\nListo. El catalogo ahora tiene solo los {len(reales)} vidrios reales, numerados VP-001 a VP-{len(reales):03d}.")