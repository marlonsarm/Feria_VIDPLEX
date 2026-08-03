-- ============================================================
-- VidPlex — Esquema de base de datos
-- Ejecutar completo en MySQL Workbench una sola vez.
-- ============================================================

CREATE DATABASE IF NOT EXISTS vidplex CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE vidplex;

-- ------------------------------------------------------------
-- Catálogo de vidrios (uno por cada QR de la feria)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS productos (
  id                INT AUTO_INCREMENT PRIMARY KEY,
  ref_code          VARCHAR(20) NOT NULL UNIQUE,      -- ej: VP-001  (esto va en la URL del QR)
  nombre            VARCHAR(120) NOT NULL,
  tipo_vidrio       VARCHAR(60)  NOT NULL,             -- Templado / Laminado / DVH
  descripcion       TEXT,
  especificaciones  TEXT,                              -- texto libre: espesor, norma, acabado...
  imagen_principal  VARCHAR(255),                      -- ruta relativa dentro de static/img/
  activo            TINYINT(1) NOT NULL DEFAULT 1,
  fecha_creacion    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Fotos y videos extra que solo se cargan al abrir el panel deslizador
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS producto_media (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  producto_id  INT NOT NULL,
  tipo         ENUM('imagen','video') NOT NULL,
  url          VARCHAR(500) NOT NULL,   -- ruta local (imagen) o URL embed (video de YouTube/Vimeo)
  orden        INT NOT NULL DEFAULT 0,
  FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Contactos capturados (deduplicados por correo)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS leads (
  id                  INT AUTO_INCREMENT PRIMARY KEY,
  nombre              VARCHAR(120) NOT NULL,
  telefono            VARCHAR(20)  NOT NULL,
  correo              VARCHAR(150) NOT NULL UNIQUE,
  tipo_proyecto       ENUM('residencial','comercial','constructora') NULL,
  autorizo_datos      TINYINT(1) NOT NULL DEFAULT 0,   -- Habeas Data — Ley 1581 de 2012
  fecha_autorizacion  DATETIME NULL,
  fecha_creacion      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ultima_actividad    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Un lead puede interesarse en varios vidrios (relación N:N)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS lead_producto (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  lead_id        INT NOT NULL,
  producto_id    INT NOT NULL,
  fecha_interes  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY unico_lead_producto (lead_id, producto_id),
  FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE,
  FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Cada vez que alguien escanea un QR y abre la ficha (mide interés real)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS escaneos (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  producto_id  INT NOT NULL,
  fecha        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Usuarios del panel de administración (contraseña siempre hasheada)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS admin_usuarios (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  usuario        VARCHAR(60) NOT NULL UNIQUE,
  password_hash  VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

-- ============================================================
-- Producto de ejemplo — así se ve el patrón para agregar los otros 29
-- ============================================================
INSERT INTO productos (ref_code, nombre, tipo_vidrio, descripcion, especificaciones, imagen_principal)
VALUES (
  'VP-001',
  'Vidrio Templado Clear 6mm',
  'Templado',
  'Vidrio de seguridad templado, resistente a impactos y cambios térmicos bruscos. Al romperse se fragmenta en piezas pequeñas y no cortantes. Ideal para fachadas, puertas y divisiones de oficina.',
  'Espesor: 6 mm | Resistencia: 5x el vidrio recocido | Norma: NTC 1974 | Acabado: Clear | Uso recomendado: fachadas, puertas, divisiones',
  'productos/vp-001.jpg'
);

INSERT INTO producto_media (producto_id, tipo, url, orden) VALUES
  (1, 'imagen', 'productos/vp-001-detalle-1.jpg', 1),
  (1, 'imagen', 'productos/vp-001-detalle-2.jpg', 2),
  (1, 'video',  'https://www.youtube.com/embed/REEMPLAZAR_CON_ID_DEL_VIDEO', 3);

-- Para agregar el producto #2, #3... copia el patrón de arriba:
-- INSERT INTO productos (ref_code, nombre, tipo_vidrio, descripcion, especificaciones, imagen_principal)
-- VALUES ('VP-002', 'Nombre del vidrio', 'Laminado', 'Descripción...', 'Especificaciones...', 'productos/vp-002.jpg');
