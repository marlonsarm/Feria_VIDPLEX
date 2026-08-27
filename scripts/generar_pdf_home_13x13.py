"""
Genera un PDF con varios QR de Home (home.png) en tamano exacto de
13x13 cm cada uno, 4 QRs por hoja (2x2), listo para imprimir.

Uso:
    python scripts/generar_pdf_home_13x13.py

El PDF queda en: qr_generados/Home_QR_13x13_CMYK.pdf
"""
import os
import numpy as np
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QR_DIR = os.path.join(BASE_DIR, 'qr_generados')
IMG_PATH = os.path.join(QR_DIR, 'home.png')
OUT_PATH = os.path.join(QR_DIR, 'Home_QR_13x13_CMYK.pdf')
TEMP_CMYK_PATH = os.path.join(QR_DIR, '_home_cmyk_temp.jpg')

TAMANO = 13 * cm       # 13x13 cm exactos por cada QR
COLUMNAS = 2            # QRs por fila
FILAS = 2                # QRs por columna
POR_PAGINA = COLUMNAS * FILAS   # 4 QRs por hoja
TOTAL_QR = 30             # cuantos QRs en TOTAL quieres (no hojas)
CANTIDAD_PAGINAS = -(-TOTAL_QR // POR_PAGINA)  # hojas necesarias (redondeo hacia arriba)
PAGINA_ANCHO = TAMANO * COLUMNAS
PAGINA_ALTO = TAMANO * FILAS


def _rgb_a_cmyk(img_rgb):
    """Convierte una imagen RGB a CMYK real (formula estandar de
    separacion de color usada en preprensa/imprenta)."""
    img_rgb = img_rgb.convert("RGB")
    r, g, b = img_rgb.split()
    R = np.array(r, dtype=float) / 255.0
    G = np.array(g, dtype=float) / 255.0
    B = np.array(b, dtype=float) / 255.0

    K = 1 - np.maximum(np.maximum(R, G), B)
    denom = np.where(K < 1, 1 - K, 1)
    C = np.where(K < 1, (1 - R - K) / denom, 0)
    M = np.where(K < 1, (1 - G - K) / denom, 0)
    Y = np.where(K < 1, (1 - B - K) / denom, 0)

    C = (C * 255).astype('uint8')
    M = (M * 255).astype('uint8')
    Y = (Y * 255).astype('uint8')
    K = (K * 255).astype('uint8')

    return Image.merge("CMYK", (
        Image.fromarray(C), Image.fromarray(M),
        Image.fromarray(Y), Image.fromarray(K),
    ))


def _preparar_imagen_cmyk(ruta_png, ruta_salida_jpg):
    """Abre el PNG, lo aplana sobre fondo blanco, lo convierte a CMYK
    real, y lo guarda como JPEG CMYK."""
    img = Image.open(ruta_png)

    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        fondo = Image.new("RGB", img.size, (255, 255, 255))
        fondo.paste(img.convert("RGBA"), mask=img.convert("RGBA").split()[3])
        img = fondo

    cmyk = _rgb_a_cmyk(img)
    cmyk.save(ruta_salida_jpg, format="JPEG", quality=95)
    return cmyk.size


def main():
    if not os.path.exists(IMG_PATH):
        print(f"No se encontró {IMG_PATH}")
        return

    print("Convirtiendo home.png a CMYK real...")
    iw, ih = _preparar_imagen_cmyk(IMG_PATH, TEMP_CMYK_PATH)

    c = canvas.Canvas(OUT_PATH, pagesize=(PAGINA_ANCHO, PAGINA_ALTO))
    img_reader = ImageReader(TEMP_CMYK_PATH)

    ratio = min(TAMANO / iw, TAMANO / ih)
    w, h = iw * ratio, ih * ratio

    print(f"Generando {TOTAL_QR} QRs de 13x13 cm en {CANTIDAD_PAGINAS} páginas ({POR_PAGINA} por hoja)...")
    qr_puestos = 0
    for i in range(CANTIDAD_PAGINAS):
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                if qr_puestos >= TOTAL_QR:
                    break
                celda_x = col * TAMANO
                celda_y = (FILAS - 1 - fila) * TAMANO  # de arriba hacia abajo
                x = celda_x + (TAMANO - w) / 2
                y = celda_y + (TAMANO - h) / 2
                c.drawImage(img_reader, x, y, width=w, height=h, mask=None)
                qr_puestos += 1
        c.showPage()

    c.save()
    os.remove(TEMP_CMYK_PATH)
    print(f"Listo. PDF generado en: {OUT_PATH}")
    print(f"  - {TOTAL_QR} QRs de 13x13 cm en {CANTIDAD_PAGINAS} páginas, en CMYK.")


if __name__ == '__main__':
    main()
