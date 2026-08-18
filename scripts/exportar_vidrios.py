"""
Lee TODOS los vidrios que existen realmente en la base de datos
(sin importar de qué script vinieron) y los escribe en un archivo
nuevo: scripts/vidrios_data_COMPLETO.py

Uso:
    python scripts/exportar_vidrios.py

Después de correrlo, abre scripts/vidrios_data_COMPLETO.py: ahí vas
a tener los 36 (o los que sean) vidrios reales, listos para editar
con la información técnica correcta de cada uno.
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
    cur.execute(
        "SELECT ref_code, nombre, tipo_vidrio, descripcion, especificaciones, "
        "imagen_principal, activo, categoria FROM productos ORDER BY ref_code"
    )
    productos = cur.fetchall()

    out_path = os.path.join(os.path.dirname(__file__), 'vidrios_data_COMPLETO.py')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('# Exportado automaticamente desde la base de datos real.\n')
        f.write(f'# Total de vidrios encontrados: {len(productos)}\n\n')
        f.write('VIDRIOS = [\n')
        for p in productos:
            def esc(v):
                if v is None:
                    return ''
                return str(v).replace('\\', '\\\\').replace('"', '\\"')
            f.write('    {\n')
            f.write(f'        "ref_code": "{esc(p["ref_code"])}",\n')
            f.write(f'        "nombre": "{esc(p["nombre"])}",\n')
            f.write(f'        "tipo_vidrio": "{esc(p["tipo_vidrio"])}",\n')
            f.write(f'        "descripcion": "{esc(p["descripcion"])}",\n')
            f.write(f'        "especificaciones": "{esc(p["especificaciones"])}",\n')
            f.write(f'        "imagen_principal": "{esc(p["imagen_principal"])}",\n')
            f.write(f'        "categoria": "{esc(p.get("categoria"))}",\n')
            f.write(f'        "activo": {1 if p["activo"] else 0},\n')
            f.write('    },\n')
        f.write(']\n')

    print(f"Listo. Se exportaron {len(productos)} vidrios a: {out_path}")