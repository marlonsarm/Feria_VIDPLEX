# VidPlex — Captura de leads por QR (Feria 2026)

Cada vidrio del stand tiene un QR único. Al escanearlo, el cliente ve la
ficha de ese vidrio (foto, specs, fotos/video extra bajo demanda) y deja
sus datos. Todo queda en MySQL, con panel de administración para el equipo.

## 1. Base de datos

1. Abre MySQL Workbench y conéctate a tu servidor.
2. Abre `schema.sql` y ejecútalo completo (▶ Execute). Esto crea la base
   `vidplex`, todas las tablas, y **un producto de ejemplo (VP-001)**.
3. Para agregar los demás vidrios (hasta 30), copia el patrón del INSERT
   de ejemplo dentro de `schema.sql` — no necesitas tocar código Python
   para esto, solo Workbench.

Columnas por producto: `ref_code` (el que va en el QR, ej. `VP-002`),
`nombre`, `tipo_vidrio`, `descripcion`, `especificaciones` (formato
`Clave: valor | Clave: valor`) e `imagen_principal`.

Para fotos/video extra del panel deslizador, inserta filas en
`producto_media` apuntando al `producto_id` correspondiente.

## 2. Instalación local

```bash
python -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edita .env con tus datos reales de MySQL
```

## 3. Crear tu usuario de administrador

```bash
python scripts/crear_admin.py
```

Te pedirá usuario/contraseña y te imprime un `INSERT` — pégalo y
ejecútalo en Workbench. Así nunca queda una contraseña en texto plano
en ningún archivo.

## 4. Correr en local

```bash
python run.py
```

Abre `http://localhost:5000/producto/VP-001` para ver la ficha de
ejemplo, y `http://localhost:5000/admin` para el panel (con el usuario
que creaste en el paso 3).

## 5. Imágenes

Pon las fotos en `app/static/img/productos/` con el mismo nombre que
usaste en la columna `imagen_principal`. Instrucciones de tamaño
recomendado en el archivo `LEEME.txt` de esa carpeta.

Si quieres el logo dentro de cada QR, coloca `logo.png` en
`app/static/img/logo.png` (fondo transparente, cuadrado) antes del
paso 7.

## 6. Desplegar en Railway

1. Sube este proyecto a un repositorio de GitHub.
2. En Railway: **New Project → Deploy from GitHub repo**.
3. Agrega un servicio **MySQL** dentro del mismo proyecto de Railway
   (Railway te da host, usuario, password y puerto automáticamente).
4. En el servicio de tu app, ve a **Variables** y pega los mismos
   nombres del `.env.example`, usando los valores que te dio el
   servicio MySQL de Railway.
5. Agrega también `SITE_URL` con la URL pública que Railway te asigna
   (algo como `https://vidplex-production.up.railway.app`).
6. Railway detecta el `Procfile` y despliega solo.
7. Entra a MySQL Workbench apuntando al host de Railway y corre
   `schema.sql` ahí también (la base de producción es independiente de
   tu base local).

## 7. Generar los QR para imprimir

Con `SITE_URL` ya apuntando a tu dominio de Railway en `.env`:

```bash
python scripts/generar_qr.py
```

Esto crea un PNG por producto en `qr_generados/`, con corrección de
errores alta (se leen aunque estén algo sucios, doblados, o con el
logo encima). Imprime cada uno junto a su vidrio en el stand.

## Qué mide el sistema

- **Escaneos**: cada vez que alguien abre la ficha de un vidrio (interés,
  aunque no deje datos).
- **Leads**: contactos que sí llenaron el formulario, deduplicados por
  correo — si la misma persona escanea 3 vidrios distintos, queda como
  **un** contacto con tres intereses, no tres filas sueltas.
- **Panel admin** (`/admin`): tabla completa + gráfica de escaneos vs.
  leads por vidrio (para ver cuál gustó más) + botón de exportar CSV.

## Seguridad

- Contraseñas de admin con `bcrypt`, nunca en texto plano.
- Sesión de admin con cookie `HttpOnly`.
- Toda la validación del formulario se repite en el servidor
  (`app/routes.py`), nunca se confía solo en el JavaScript del navegador.
- El formulario exige el checkbox de autorización de datos (Ley 1581 de
  2012) antes de guardar cualquier dato.
- Si el wifi de la feria falla justo al enviar el formulario, el dato se
  guarda en el navegador y se reintenta solo al recuperar conexión — no
  se pierde ningún lead por mala señal.
