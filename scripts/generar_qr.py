"""
Genera un PNG de QR por cada producto activo en la base de datos.

Uso:
    python scripts/generar_qr.py

Requiere las variables de entorno del .env (DB_*, SITE_URL).
Los QR quedan en la carpeta qr_generados/, listos para imprimir.

Usa corrección de errores nivel H (alta): el QR se sigue leyendo aunque
hasta ~30% del código esté sucio, doblado o tape parcialmente con el logo.

Cada QR sale con:
  - El logo VidPlex centrado (en un círculo/óvalo blanco, como una tarjeta).
  - Un marco blanco alrededor de todo el código.
  - Un texto debajo (por defecto: "VIDPLEX transformó este vidrio").
"""
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import numpy as np
import pymysql
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from dotenv import load_dotenv

load_dotenv()

SITE_URL = os.environ.get('SITE_URL', 'http://localhost:5000').rstrip('/')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE_DIR, 'qr_generados')
LOGO_PATH = os.path.join(BASE_DIR, 'app', 'static', 'img', 'logo_DEFINITIVO.png')

# Texto que aparece debajo del QR (puedes cambiarlo aquí)
TEXTO_QR = "Escanéa y descubre por qué este vidrio es único"

# --- Configuración visual ---
# Si es True: el fondo del QR y de la franja de texto queda TRANSPARENTE
# (solo se ve la tinta negra) — pensado para imprimir en vinilo/sticker
# transparente y pegarlo sobre el vidrio. Si es False: usa COLOR_FONDO sólido.
FONDO_TRANSPARENTE = False

COLOR_QR = "#110F0D"        # negro casi puro (igual al de la placa del logo, para que se vea integrado)
COLOR_FONDO = "#FFFFFF"     # gris clarito (se usa cuando FONDO_TRANSPARENTE = False)
COLOR_TEXTO = "#110F0D"     # color del texto de abajo
MARGEN_MARCO = 16           # grosor del marco alrededor del QR
ALTO_FRANJA_TEXTO = 84      # alto de la franja donde va el texto (más grande = letra más grande)
RADIO_ESQUINAS = 22         # redondeo de las esquinas de la tarjeta final

# Renderiza la placa del logo 4x más grande y la reduce -> bordes perfectamente
# suaves, sin pixelado (técnica de supersampling / antialiasing).
SUPERSAMPLE = 4


def _cargar_fuente(tamano):
    """Busca una fuente en negrita disponible en el sistema; si no hay ninguna,
    usa la fuente por defecto de Pillow (para que el script nunca truene)."""
    candidatos = [
        os.path.join(BASE_DIR, 'app', 'static', 'fonts', 'Montserrat-Bold.ttf'),
        os.path.join(BASE_DIR, 'app', 'static', 'fonts', 'Poppins-Bold.ttf'),
        "C:\\Windows\\Fonts\\arialbd.ttf",
        "C:\\Windows\\Fonts\\Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf",
    ]
    for ruta in candidatos:
        if os.path.exists(ruta):
            try:
                return ImageFont.truetype(ruta, tamano)
            except Exception:
                continue
    return ImageFont.load_default()


def conectar_db():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=int(os.environ.get('DB_PORT', 3306)),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', ''),
        database=os.environ.get('DB_NAME', 'vidplex'),
        cursorclass=pymysql.cursors.DictCursor,
    )


def _qr_a_transparente(img_qr_rgb):
    """Convierte el fondo blanco del QR en transparente, dejando solo
    los módulos negros (para imprimir en vinilo/sticker sobre vidrio)."""
    arr = np.array(img_qr_rgb.convert("RGB"))
    alpha = np.where(np.all(arr > 200, axis=2), 0, 255).astype(np.uint8)
    rgba = np.dstack([arr, alpha])
    return Image.fromarray(rgba, "RGBA")


def _qr_a_transparente(img_qr_rgb):
    """Convierte el fondo blanco del QR en transparente, dejando solo
    los módulos negros (para poder fusionarlo con la tarjeta de fondo)."""
    arr = np.array(img_qr_rgb.convert("RGB"))
    alpha = np.where(np.all(arr > 200, axis=2), 0, 255).astype(np.uint8)
    rgba = np.dstack([arr, alpha])
    return Image.fromarray(rgba, "RGBA")


def _fondo_tarjeta(w, h, radius, borde_ancho=2):
    """Fondo plateado con degradado para TODA la tarjeta (QR + texto en
    una sola pieza continua), con un borde negro muy delgado alrededor."""
    W, H, R = w * SUPERSAMPLE, h * SUPERSAMPLE, radius * SUPERSAMPLE
    grad = Image.new("RGB", (1, H))
    top, bot = (255, 255, 255), (255, 255, 255)
    for y in range(H):
        t = y / max(H - 1, 1)
        r = int(top[0] * (1 - t) + bot[0] * t)
        g = int(top[1] * (1 - t) + bot[1] * t)
        b = int(top[2] * (1 - t) + bot[2] * t)
        grad.putpixel((0, y), (r, g, b))
    grad = grad.resize((W, H)).convert("RGBA")

    mask = Image.new("L", (W, H), 0)
    dm = ImageDraw.Draw(mask)
    dm.rounded_rectangle([0, 0, W - 1, H - 1], radius=R, fill=255)
    grad.putalpha(mask)

    d = ImageDraw.Draw(grad)
    bw = max(1, borde_ancho * SUPERSAMPLE)
    d.rounded_rectangle(
        [bw // 2, bw // 2, W - 1 - bw // 2, H - 1 - bw // 2],
        radius=R, outline=(10, 10, 10, 255), width=bw,
    )
    return grad.resize((w, h), Image.LANCZOS)


def _placa_plateada(w, h, radius):
    """Placa con degradado plateado/metálico claro, para el texto de abajo."""
    W, H, R = w * SUPERSAMPLE, h * SUPERSAMPLE, radius * SUPERSAMPLE
    grad = Image.new("RGB", (1, H))
    top, bot = (238, 240, 243), (178, 184, 191)
    for y in range(H):
        t = y / max(H - 1, 1)
        r = int(top[0] * (1 - t) + bot[0] * t)
        g = int(top[1] * (1 - t) + bot[1] * t)
        b = int(top[2] * (1 - t) + bot[2] * t)
        grad.putpixel((0, y), (r, g, b))
    grad = grad.resize((W, H)).convert("RGBA")
    mask = Image.new("L", (W, H), 0)
    dm = ImageDraw.Draw(mask)
    dm.rounded_rectangle([0, 0, W - 1, H - 1], radius=R, fill=255)
    grad.putalpha(mask)
    d = ImageDraw.Draw(grad)
    d.rounded_rectangle(
        [SUPERSAMPLE, SUPERSAMPLE, W - 1 - SUPERSAMPLE, H - 1 - SUPERSAMPLE],
        radius=max(0, R - SUPERSAMPLE), outline=(140, 146, 152, 180), width=max(1, SUPERSAMPLE // 2),
    )
    return grad.resize((w, h), Image.LANCZOS)


def _placa_logo(w, h, radius):
    """Placa del mismo negro que los módulos del QR (para que el logo se
    vea integrado al patrón, no como una caja aparte) con un filo
    metálico fino que la distingue. Renderizado en alta resolución para
    bordes perfectamente suaves."""
    W, H, R = w * SUPERSAMPLE, h * SUPERSAMPLE, radius * SUPERSAMPLE
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=R, fill=_hex_a_rgb(COLOR_QR) + (255,))
    d.rounded_rectangle(
        [SUPERSAMPLE, SUPERSAMPLE, W - 1 - SUPERSAMPLE, H - 1 - SUPERSAMPLE],
        radius=max(0, R - SUPERSAMPLE),
        outline=(190, 196, 203, 255),
        width=max(1, SUPERSAMPLE),
    )
    return canvas.resize((w, h), Image.LANCZOS)


def _sombra_tarjeta(w, h, radius, blur=10, offset=6, opacidad=110):
    """Sombra suave detrás de la placa del logo, para que 'flote'
    ligeramente sobre el QR en vez de verse pegada y plana."""
    pad = blur * 2
    W, H, R = (w + pad * 2) * SUPERSAMPLE, (h + pad * 2) * SUPERSAMPLE, radius * SUPERSAMPLE
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    off = offset * SUPERSAMPLE
    p = pad * SUPERSAMPLE
    d.rounded_rectangle([p, p + off, W - p, H - p + off], radius=R, fill=(0, 0, 0, opacidad))
    canvas = canvas.resize((w + pad * 2, h + pad * 2), Image.LANCZOS)
    return canvas.filter(ImageFilter.GaussianBlur(blur))


def _hex_a_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def _agregar_logo(img_qr):
    """Pega el logo centrado sobre el QR, dentro de una placa negra
    (mismo color que el QR) con filo metálico y sombra sutil, para que
    se vea integrada al patrón en vez de una caja aparte."""
    if not os.path.exists(LOGO_PATH):
        return img_qr

    logo = Image.open(LOGO_PATH).convert("RGBA")
    qr_w, qr_h = img_qr.size

    # Tamaño del logo: ~34% del ancho del QR (más grande y notorio)
    logo_target_w = int(qr_w * 0.34)
    ratio = logo_target_w / logo.width
    logo = logo.resize((logo_target_w, max(1, int(logo.height * ratio))), Image.LANCZOS)

    pad_x = int(logo_target_w * 0.14)
    pad_y = int(logo.height * 0.42)
    card_w, card_h = logo.width + pad_x * 2, logo.height + pad_y * 2
    radius = int(card_h * 0.26)

    sombra = _sombra_tarjeta(card_w, card_h, radius)
    img_qr.alpha_composite(sombra, ((qr_w - sombra.width) // 2, (qr_h - sombra.height) // 2))

    placa = _placa_logo(card_w, card_h, radius)
    placa.paste(logo, (pad_x, pad_y), logo)
    img_qr.alpha_composite(placa, ((qr_w - card_w) // 2, (qr_h - card_h) // 2))
    return img_qr


def _agregar_marco_y_texto(img_qr, texto):
    """Arma la tarjeta final: fondo plateado degradado continuo (QR + texto
    en una sola pieza, sin costuras) con borde negro fino alrededor.
    Si FONDO_TRANSPARENTE=True, en cambio, todo el fondo queda
    transparente (solo tinta negra visible)."""
    qr_w, qr_h = img_qr.size

    ancho_final = qr_w + MARGEN_MARCO * 2
    alto_final = qr_h + MARGEN_MARCO * 2 + ALTO_FRANJA_TEXTO

    if FONDO_TRANSPARENTE:
        tarjeta = Image.new("RGBA", (ancho_final, alto_final), (0, 0, 0, 0))
        tarjeta.alpha_composite(img_qr, (MARGEN_MARCO, MARGEN_MARCO))
    else:
        tarjeta = _fondo_tarjeta(ancho_final, alto_final, RADIO_ESQUINAS)
        tarjeta.alpha_composite(img_qr, (MARGEN_MARCO, MARGEN_MARCO))

    draw = ImageDraw.Draw(tarjeta)

    # Texto en MAYÚSCULAS, directo sobre el fondo plateado (ya no necesita
    # su propia placa: toda la tarjeta comparte el mismo degradado)
    fuente = _cargar_fuente(27)
    max_ancho_texto = ancho_final - 40
    lineas = textwrap.wrap(texto, width=24)

    while True:
        anchos = [draw.textbbox((0, 0), linea, font=fuente)[2] for linea in lineas]
        if max(anchos, default=0) <= max_ancho_texto or fuente.size <= 14:
            break
        fuente = _cargar_fuente(fuente.size - 2)

    alto_linea = fuente.size + 10
    y_texto = MARGEN_MARCO + qr_h + (ALTO_FRANJA_TEXTO - alto_linea * len(lineas)) // 2

    for linea in lineas:
        bbox = draw.textbbox((0, 0), linea, font=fuente)
        ancho_linea = bbox[2] - bbox[0]
        x_texto = (ancho_final - ancho_linea) // 2
        draw.text((x_texto, y_texto), linea, font=fuente, fill=COLOR_TEXTO)
        y_texto += alto_linea

    if FONDO_TRANSPARENTE:
        # Ya es RGBA con fondo transparente, no hace falta enmascarar
        return tarjeta

    # Máscara con esquinas redondeadas para toda la tarjeta (solo modo blanco)
    mascara = Image.new("L", tarjeta.size, 0)
    draw_m = ImageDraw.Draw(mascara)
    draw_m.rounded_rectangle([0, 0, ancho_final - 1, alto_final - 1], radius=RADIO_ESQUINAS, fill=255)

    return tarjeta


def generar_qr_individual(ref_code, texto=TEXTO_QR):
    url = f"{SITE_URL}/producto/{ref_code}"

    qr = qrcode.QRCode(
        error_correction=ERROR_CORRECT_H,
        box_size=12,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)
    # Siempre se genera primero en blanco y negro y se le quita el fondo
    # blanco, para poder fusionarlo con la tarjeta plateada de abajo
    # (o dejarlo 100% transparente si FONDO_TRANSPARENTE=True).
    img = qr.make_image(fill_color=COLOR_QR, back_color="#FFFFFF").convert("RGBA")
    img = _qr_a_transparente(img)

    img = _agregar_logo(img)
    tarjeta_final = _agregar_marco_y_texto(img, texto)

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, f"{ref_code}.png")
    tarjeta_final.save(out_path)
    return out_path, url

def generar_qr_admin(texto="Acceso panel VidPlex"):
    """Genera el QR de acceso al login del panel de administración.
    Se guarda directo en app/static/img/ para poder mostrarlo en la
    plantilla del login con una ruta estática normal."""
    url = f"{SITE_URL}/admin"

    qr = qrcode.QRCode(
        error_correction=ERROR_CORRECT_H,
        box_size=12,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=COLOR_QR, back_color="#FFFFFF").convert("RGBA")
    img = _qr_a_transparente(img)

    img = _agregar_logo(img)
    tarjeta_final = _agregar_marco_y_texto(img, texto)

    out_dir = os.path.join(BASE_DIR, 'app', 'static', 'img')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'admin_qr.png')
    tarjeta_final.save(out_path)
    return out_path, url


def generar_qr_video_dvh(texto="Escanéame para información técnica"):
    """Genera el QR que lleva a la sección del video DVH con persianas
    integradas, en la página oficial vidplex.com (ancla #video-dvh)."""
    url = "https://vidplex.com/#video-dvh"

    qr = qrcode.QRCode(
        error_correction=ERROR_CORRECT_H,
        box_size=12,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=COLOR_QR, back_color="#FFFFFF").convert("RGBA")
    img = _qr_a_transparente(img)

    img = _agregar_logo(img)
    tarjeta_final = _agregar_marco_y_texto(img, texto)

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "video_dvh.png")
    tarjeta_final.save(out_path)
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

    print("\nGenerando QR de acceso al panel de administración...")
    admin_path, admin_url = generar_qr_admin()
    print(f"  admin_qr -> {admin_path}   ({admin_url})")

    print("\nGenerando QR del video DVH (vidplex.com)...")
    video_path, video_url = generar_qr_video_dvh()
    print(f"  video_dvh -> {video_path}   ({video_url})")


if __name__ == '__main__':
    main()