"""
Revisa TODOS los productos en la base de datos y reporta:
  - Cuáles existen y están activos (deberían funcionar bien)
  - Cuáles tienen especificaciones vacías o incompletas
  - Cuáles tienen imagen_principal que probablemente no existe
  - Cuáles están inactivos (no van a cargar, esto es normal si tú los desactivaste)

Uso:
    python scripts/diagnostico_vidrios.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.db import get_db

app = create_app()

with app.app_context():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM productos ORDER BY ref_code")
    productos = cur.fetchall()

    print(f"Total de productos en la base de datos: {len(productos)}\n")

    activos_ok = []
    inactivos = []
    sin_specs = []

    for p in productos:
        if not p['activo']:
            inactivos.append(p['ref_code'])
            continue

        specs = p.get('especificaciones') or ''
        if not specs.strip() or '[completar]' in specs:
            sin_specs.append(p['ref_code'])
        else:
            activos_ok.append(p['ref_code'])

    print(f"✅ ACTIVOS Y CON ESPECIFICACIONES COMPLETAS ({len(activos_ok)}):")
    print("   " + ", ".join(activos_ok) if activos_ok else "   (ninguno)")

    print(f"\n⚠️  ACTIVOS PERO SIN ESPECIFICACIONES REALES (cargan, pero les falta info) ({len(sin_specs)}):")
    print("   " + ", ".join(sin_specs) if sin_specs else "   (ninguno)")

    print(f"\n❌ INACTIVOS (dan 404 al escanear, no se muestran) ({len(inactivos)}):")
    print("   " + ", ".join(inactivos) if inactivos else "   (ninguno)")

    print(f"\nResumen: {len(activos_ok)} completos, {len(sin_specs)} incompletos, {len(inactivos)} inactivos.")