"""
Genera un PDF de una sola pagina con el QR de Home (home.png) en un
tamano exacto de 10x10 cm, listo para imprimir.

Uso:
    python scripts/generar_pdf_home_10x10.py

El PDF queda en: qr_generados/Home_QR_10x10.pdf
"""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QR_DIR = os.path.join(BASE_DIR, 'qr_generados')
IMG_PATH = os.path.join(QR_DIR, 'home.png')
OUT_PATH = os.path.join(QR_DIR, 'Home_QR_10x10.pdf')

TAMANO = 10 * cm  # 10x10 cm exactos


def main():
    if not os.path.exists(IMG_PATH):
        print(f"No se encontró {IMG_PATH}")
        return

    c = canvas.Canvas(OUT_PATH, pagesize=(TAMANO, TAMANO))

    img = ImageReader(IMG_PATH)
    iw, ih = img.getSize()

    # Ajusta la imagen dentro del cuadro 10x10, manteniendo proporción
    # y centrada, con fondo blanco si no es perfectamente cuadrada.
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, TAMANO, TAMANO, fill=1, stroke=0)

    ratio = min(TAMANO / iw, TAMANO / ih)
    w, h = iw * ratio, ih * ratio
    x = (TAMANO - w) / 2
    y = (TAMANO - h) / 2
    c.drawImage(img, x, y, width=w, height=h, mask='auto')

    c.showPage()
    c.save()
    print(f"Listo. PDF generado en: {OUT_PATH}")


if __name__ == '__main__':
    main()