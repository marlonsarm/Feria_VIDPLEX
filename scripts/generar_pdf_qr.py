"""
Arma un PDF con TODOS los códigos QR del proyecto, organizado y listo
para entregar/imprimir en blanco y negro (sin colores):
  1. Portada
  2. Accesos especiales: Admin, Home, Video DVH
  3. Los 41 vidrios, en cuadricula, cada uno con su codigo (VP-001, etc.),
     nombre y separador como texto para diferenciarlos.

No necesita base de datos ni tunel: solo lee los PNG que ya existen en
qr_generados/ y app/static/img/, y los datos de texto desde
vidrios_data_COMPLETO.py.

Uso:
    pip install reportlab --break-system-packages   (si no lo tienes)
    python scripts/generar_pdf_qr.py

El PDF queda en: qr_generados/Catalogo_QR_VidPlex.pdf
"""
import os
import re
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vidrios_data_COMPLETO import VIDRIOS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QR_DIR = os.path.join(BASE_DIR, 'qr_generados')
IMG_DIR = os.path.join(BASE_DIR, 'app', 'static', 'img')
OUT_PATH = os.path.join(QR_DIR, 'Catalogo_QR_VidPlex.pdf')

# Solo blanco y negro, sin colores.
NEGRO = (0, 0, 0)
BLANCO = (1, 1, 1)

ANCHO, ALTO = A4

PRODUCTOS_POR_REF = {p["ref_code"]: p for p in VIDRIOS}

RE_SEPARADOR = re.compile(r"Separador:\s*([^|]+)")


def _obtener_separador(especificaciones):
    if not especificaciones:
        return ""
    m = RE_SEPARADOR.search(especificaciones)
    if not m:
        return ""
    return m.group(1).strip()


def _fondo_pagina(c):
    c.setFillColorRGB(*BLANCO)
    c.rect(0, 0, ANCHO, ALTO, fill=1, stroke=0)


def _titulo_pagina(c, texto, y=ALTO - 30 * mm):
    c.setFillColorRGB(*NEGRO)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(ANCHO / 2, y, texto)
    c.setStrokeColorRGB(*NEGRO)
    c.setLineWidth(1.2)
    c.line(ANCHO / 2 - 40 * mm, y - 6 * mm, ANCHO / 2 + 40 * mm, y - 6 * mm)


def _texto_ajustado(c, texto, cx, y, max_ancho_pt, fuente="Helvetica",
                     tam_max=7.5, tam_min=5):
    tam = tam_max
    while tam > tam_min and stringWidth(texto, fuente, tam) > max_ancho_pt:
        tam -= 0.5

    if stringWidth(texto, fuente, tam) > max_ancho_pt:
        recortado = texto
        while recortado and stringWidth(recortado + "...", fuente, tam) > max_ancho_pt:
            recortado = recortado[:-1]
        texto = recortado + "..." if recortado else texto

    c.setFont(fuente, tam)
    c.drawCentredString(cx, y, texto)


def portada(c):
    _fondo_pagina(c)
    c.setFillColorRGB(*NEGRO)
    c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(ANCHO / 2, ALTO / 2 + 20 * mm, "VIDPLEX")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(ANCHO / 2, ALTO / 2 + 5 * mm, "CATÁLOGO DE CÓDIGOS QR")
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
        c.setFillColorRGB(*NEGRO)
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
    tam = 44 * mm
    esp_x = 14 * mm
    esp_y = 30 * mm
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
            producto = PRODUCTOS_POR_REF.get(ref_code)

            cx = x + tam / 2
            max_ancho_pt = (tam + esp_x * 0.6)

            c.setFillColorRGB(*NEGRO)
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(cx, y - 6 * mm, ref_code)

            if producto:
                c.setFillColorRGB(*NEGRO)
                _texto_ajustado(
                    c, producto.get("nombre", ""), cx, y - 11 * mm,
                    max_ancho_pt, fuente="Helvetica-Bold", tam_max=7.5, tam_min=5
                )

                separador = _obtener_separador(producto.get("especificaciones", ""))
                if separador:
                    c.setFillColorRGB(*NEGRO)
                    _texto_ajustado(
                        c, separador, cx, y - 15.5 * mm,
                        max_ancho_pt, fuente="Helvetica", tam_max=7, tam_min=5
                    )

        c.showPage()


def main():
    if not os.path.isdir(QR_DIR):
        print(f"No existe la carpeta {QR_DIR}. Corre primero generar_qr.py")
        return

    faltantes = [f for f in os.listdir(QR_DIR) if re.match(r'^VP-\d{3}\.png$', f)]
    sin_datos = [f.replace('.png', '') for f in faltantes if f.replace('.png', '') not in PRODUCTOS_POR_REF]
    if sin_datos:
        print("Aviso: estos QR no tienen datos en vidrios_data_COMPLETO.py "
              f"(se imprimirán solo con el código): {', '.join(sin_datos)}")

    c = canvas.Canvas(OUT_PATH, pagesize=A4)
    portada(c)
    pagina_accesos(c)
    paginas_vidrios(c)
    c.save()
    print(f"Listo. PDF generado en: {OUT_PATH}")


if __name__ == '__main__':
    main()