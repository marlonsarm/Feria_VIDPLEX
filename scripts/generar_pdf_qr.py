"""
Arma un PDF con TODOS los códigos QR del proyecto, organizado y listo
para entregar/imprimir:
  1. Portada
  2. Accesos especiales: Admin, Home, Video DVH
  3. Los 41 vidrios, en cuadricula, cada uno con su codigo (VP-001, etc.)
     como titulo para diferenciarlos.

No necesita base de datos ni tunel: solo lee los PNG que ya existen en
qr_generados/ y app/static/img/.

Uso:
    pip install reportlab --break-system-packages   (si no lo tienes)
    python scripts/generar_pdf_qr.py

El PDF queda en: qr_generados/Catalogo_QR_VidPlex.pdf
"""
import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QR_DIR = os.path.join(BASE_DIR, 'qr_generados')
IMG_DIR = os.path.join(BASE_DIR, 'app', 'static', 'img')
OUT_PATH = os.path.join(QR_DIR, 'Catalogo_QR_VidPlex.pdf')

NEGRO = (0.04, 0.04, 0.04)
NARANJA = (0.894, 0.341, 0.180)  # #E4572E
GRIS = (0.6, 0.6, 0.6)

ANCHO, ALTO = A4


def _fondo_pagina(c):
    c.setFillColorRGB(*NEGRO)
    c.rect(0, 0, ANCHO, ALTO, fill=1, stroke=0)


def _titulo_pagina(c, texto, y=ALTO - 30 * mm):
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(ANCHO / 2, y, texto)
    c.setStrokeColorRGB(*NARANJA)
    c.setLineWidth(1.2)
    c.line(ANCHO / 2 - 40 * mm, y - 6 * mm, ANCHO / 2 + 40 * mm, y - 6 * mm)


def portada(c):
    _fondo_pagina(c)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(ANCHO / 2, ALTO / 2 + 20 * mm, "VIDPLEX")
    c.setFillColorRGB(*NARANJA)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(ANCHO / 2, ALTO / 2 + 5 * mm, "CATÁLOGO DE CÓDIGOS QR")
    c.setFillColorRGB(*GRIS)
    c.setFont("Helvetica", 11)
    c.drawCentredString(ANCHO / 2, ALTO / 2 - 5 * mm, "Accesos y vidrios del catálogo digital")
    c.showPage()


def pagina_accesos(c):
    _fondo_pagina(c)
    _titulo_pagina(c, "ACCESOS ESPECIALES")

    accesos = [
        (os.path.join(IMG_DIR, 'admin_qr.png'), "Panel de administración"),
        (os.path.join(QR_DIR, 'home.png'), "Inicio (Home)"),
        (os.path.join(QR_DIR, 'video_dvh.png'), "Video DVH · vidplex.com"),
    ]

    tam = 55 * mm
    espacio = 15 * mm
    total_ancho = tam * 3 + espacio * 2
    x0 = (ANCHO - total_ancho) / 2
    y0 = ALTO / 2 - tam / 2

    for i, (ruta, etiqueta) in enumerate(accesos):
        x = x0 + i * (tam + espacio)
        if os.path.exists(ruta):
            img = ImageReader(ruta)
            iw, ih = img.getSize()
            ratio = min(tam / iw, tam / ih)
            w, h = iw * ratio, ih * ratio
            c.drawImage(img, x + (tam - w) / 2, y0 + (tam - h) / 2, width=w, height=h, mask='auto')
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + tam / 2, y0 - 8 * mm, etiqueta)

    c.showPage()


def paginas_vidrios(c):
    archivos = sorted(
        f for f in os.listdir(QR_DIR)
        if re.match(r'^VP-\d{3}\.png$', f)
    )
    if not archivos:
        return

    cols, filas = 3, 3
    por_pagina = cols * filas
    tam = 48 * mm
    esp_x = 12 * mm
    esp_y = 20 * mm
    total_ancho = tam * cols + esp_x * (cols - 1)
    total_alto = tam * filas + esp_y * (filas - 1)
    x0 = (ANCHO - total_ancho) / 2
    y0_base = ALTO - 45 * mm

    for pagina_i in range(0, len(archivos), por_pagina):
        lote = archivos[pagina_i:pagina_i + por_pagina]
        _fondo_pagina(c)
        _titulo_pagina(c, f"VIDRIOS · Página {pagina_i // por_pagina + 1}")

        for idx, nombre_archivo in enumerate(lote):
            fila = idx // cols
            col = idx % cols
            x = x0 + col * (tam + esp_x)
            y = y0_base - total_alto - fila * (tam + esp_y) + (filas - 1) * (tam + esp_y)

            ruta = os.path.join(QR_DIR, nombre_archivo)
            img = ImageReader(ruta)
            iw, ih = img.getSize()
            ratio = min(tam / iw, tam / ih)
            w, h = iw * ratio, ih * ratio
            c.drawImage(img, x + (tam - w) / 2, y + (tam - h) / 2, width=w, height=h, mask='auto')

            ref_code = nombre_archivo.replace('.png', '')
            c.setFillColorRGB(*NARANJA)
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(x + tam / 2, y - 6 * mm, ref_code)

        c.showPage()


def main():
    if not os.path.isdir(QR_DIR):
        print(f"No existe la carpeta {QR_DIR}. Corre primero generar_qr.py")
        return

    c = canvas.Canvas(OUT_PATH, pagesize=A4)
    portada(c)
    pagina_accesos(c)
    paginas_vidrios(c)
    c.save()
    print(f"Listo. PDF generado en: {OUT_PATH}")


if __name__ == '__main__':
    main()