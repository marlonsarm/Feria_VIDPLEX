"""
Genera un PNG de QR por cada producto activo en la base de datos.

Uso:
    python scripts/generar_qr.py

Requiere las variables de entorno del .env (DB_*, SITE_URL).
Los QR quedan en la carpeta qr_generados/, listos para imprimir.

Usa corrección de errores nivel H (alta): el QR se sigue leyendo aunque
hasta ~30% del código esté sucio, doblado o tape parcialmente con el logo.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

SITE_URL = os.environ.get('SITE_URL', 'http://localhost:5000').rstrip('/')
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'qr_generados')
LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app', 'static', 'img', 'logo.png')


def conectar_db():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=int(os.environ.get('DB_PORT', 3306)),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', ''),
        database=os.environ.get('DB_NAME', 'vidplex'),
        cursorclass=pymysql.cursors.DictCursor,
    )


def generar_qr_individual(ref_code):
    url = f"{SITE_URL}/producto/{ref_code}"

    qr = qrcode.QRCode(
        error_correction=ERROR_CORRECT_H,
        box_size=12,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Si existe un logo en app/static/img/logo.png, lo centra sobre el QR
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH).convert("RGBA")
        qr_w, qr_h = img.size
        logo_size = int(qr_w * 0.20)
        logo.thumbnail((logo_size, logo_size))
        pos = ((qr_w - logo.size[0]) // 2, (qr_h - logo.size[1]) // 2)
        fondo_logo = Image.new("RGBA", logo.size, "WHITE")
        fondo_logo.paste(logo, (0, 0), logo)
        img.paste(fondo_logo, pos)

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, f"{ref_code}.png")
    img.save(out_path)
    return out_path, url


def main():
    db = conectar_db()
    cur = db.cursor()
    cur.execute("SELECT ref_code, nombre FROM productos WHERE activo = 1 ORDER BY ref_code")
    productos = cur.fetchall()
    db.close()

    if not productos:
        print("No hay productos activos en la base de datos.")
        return

    print(f"Generando {len(productos)} código(s) QR en '{OUT_DIR}/' ...\n")
    for p in productos:
        path, url = generar_qr_individual(p['ref_code'])
        print(f"  {p['ref_code']:<10} -> {path}   ({url})")

    print("\nListo. Imprime cada PNG junto a su vidrio correspondiente en el stand.")


if __name__ == '__main__':
    main()
