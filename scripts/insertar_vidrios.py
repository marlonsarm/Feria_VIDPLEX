import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask
from app import create_app
from app.db import get_db

app = create_app()

VIDRIOS = [
   (
    'SP-1258',                              # ref_code
    'Laminado Termoendurecido KNT155 8mm',  # nombre
    'Laminado Termoendurecido',             # tipo_vidrio
    'Vidrio laminado termoendurecido de alto desempeño, compuesto por 4mm Low-E Cool-Lite KNT155 + PVB 0.76mm + 4mm NC. Combina aislamiento térmico, control solar y reducción acústica en una sola unidad, ideal para fachadas y ventanales de alta exigencia.',  # descripcion
    'Composición: 4mm Low-E Cool-Lite KNT155 (HS) + PVB 0.76mm NC + 4mm NC (HS) | Espesor: 8.8mm | Peso: 20.0 kg/m2 | Emisividad: 0.13 | Acústica STC: 34 | Acústica OITC: 31 | Acústica Rw: 34 (c:-1, ctr:-2) | Claridad (TL): 47% | Factor Solar (SHGC): 0.442 | Transmisión Térmica: 5.40 W/m2K (invierno) | Filtro UV: 99.7% | SPF: 99 | Seguridad ANSI Z97: Clase B | Seguridad EN 12600: Clas. 2(B) | Medidas recomendadas: 350x350mm a 2500x2300mm',  # especificaciones
    '/static/img/vidrios/SP-1258.jpg',      # imagen_principal
    1                                        # activo
    ),
    (
        'CST-ST167.4',
        'Templado de Control Solar Estándar ST167 de 4mm',
        'Control Solar',
        'Vidrio templado de control solar compuesto por 4mm Cool-Lite ST167. Reduce la ganancia de calor solar manteniendo buena claridad, ideal para fachadas con alta exposición al sol.',
        'Composición: 4mm Cool-Lite ST167 (FT C2) | Espesor: 4.0mm | Peso: 10.0 kg/m2 | Acústica STC: 30 | Acústica Rw: 30 (c:-2, ctr:-2) | Claridad (TL): 67% | Factor Solar (SHGC): 0.68 | Transmisión Térmica: 5.70 W/m2K (verano e invierno) | Seguridad ANSI Z97: Clase B | Seguridad EN 12600: Clas. 2(C) | Medidas máximas recomendadas: 3210x2400mm | Medidas mínimas recomendadas: 300x400mm',
        '/static/img/vidrios/CST-ST167.4.jpg',
        1
    ),
   (
        'CSL-GRSC.8',
        'Laminado de Control Solar Gris SolarCool de 8mm 44.1',
        'Control Solar',
        'Vidrio laminado de control solar en tono gris, compuesto por 4mm SolarCool SolarGray + PVB 0.38mm + 4mm NC. Reduce el ingreso de calor solar con estética discreta.',
        'Composición: 4mm SolarCool SolarGray (AN) + PVB 0.38mm NC + 4mm NC (AN) | Espesor: 8.2mm | Peso: 20.6 kg/m2 | Acústica STC: 34 | Acústica Rw: 34 (c:-1, ctr:-2) | Claridad (TL): 21% | Factor Solar (SHGC): 0.4533 | Transmisión Térmica: 5.72 W/m2K (invierno) / 5.17 W/m2K (verano) | Filtro UV: 99.3% | SPF: 99 | Medidas máximas recomendadas: 3210x2400mm | Medidas mínimas recomendadas: 300x300mm',
        '/static/img/vidrios/CSL-GRSC.8.jpg',
        1
    ),
    (
        'VP-004',
        'Vidrio Low-E 4mm',
        'Low-E',
        'Vidrio de baja emisividad que mejora la eficiencia energética del edificio. Mantiene el calor interior en invierno y lo repele en verano.',
        'Espesor: 4mm | Emisividad: 0.03 | Transmisión luz: 80% | Uso: Ventanas residenciales',
        '/static/img/vidrios/VP-004.jpg',
        1
    ),
    (
        'SLH-GA.6',
        'Laminado de Seguridad [HS+HS] 6mm (3+3) Gris Asahi',
        'Seguridad',
        'Vidrio laminado de seguridad termoendurecido, compuesto por 3mm NC + PVB Gris Asahi + PVB 0.38mm + 3mm NC. Combina resistencia con estética en tono gris.',
        'Composición: 3mm NC (HS) + PVB 0.38mm Gris Asahi + PVB 0.38mm NC + 3mm NC (HS) | Espesor: 6.7mm | Peso: 16.8 kg/m2 | Acústica STC: 33 | Acústica Rw: 33 (c:-1, ctr:-4) | Claridad (TL): 40% | Factor Solar (SHGC): 0.6008 | Transmisión Térmica: 5.68 W/m2K (invierno) / 5.13 W/m2K (verano) | Filtro UV: 99.8% | SPF: 99 | Seguridad ANSI Z97: Clase A | Seguridad EN 12600: Clas. 1(B) | Resistencia EN 356: P1A',
        '/static/img/vidrios/SLH-GA.6.jpg',
        1
    ),
    (
        'VP-006',
        'Vidrio Grabado Ácido',
        'Decorativo',
        'Vidrio con acabado satinado por tratamiento ácido. Elegancia difusa que permite paso de luz con privacidad.',
        'Espesor: 5mm | Acabado: Satinado unilateral | Transmisión luz: 85% | Uso: Divisiones, puertas',
        '/static/img/vidrios/VP-006.jpg',
        1
    ),
    (
        'VP-007',
        'Vidrio Templado Curvo',
        'Templado Curvo',
        'Vidrio templado con curvatura personalizada para proyectos arquitectónicos únicos. Resistencia estructural mantenida.',
        'Espesor: 8-12mm | Curvatura: según diseño | Radio mínimo: 500mm | Uso: Barandas, fachadas curvas',
        '/static/img/vidrios/VP-007.jpg',
        1
    ),
    (
        'VP-008',
        'Vidrio Laminado Blindado',
        'Blindado',
        'Vidrio laminado de alta seguridad con capas de policarbonato. Resistencia a impactos balísticos nivel III-A.',
        'Espesor total: 24mm | Nivel: III-A | Capas: 3 vidrios + 2 policarbonatos | Uso: Bancos, embajadas',
        '/static/img/vidrios/VP-008.jpg',
        1
    ),
    (
        'VP-009',
        'Vidrio Antihumedad para Baño',
        'Antihumedad',
        'Vidrio con tratamiento hidrofóbico que repele el agua y evita manchas de cal. Ideal para mamparas de ducha.',
        'Espesor: 6mm | Tratamiento: Nanocapa hidrofóbica | Garantía: 5 años | Uso: Mamparas, divisiones húmedas',
        '/static/img/vidrios/VP-009.jpg',
        1
    ),
    (
        'VP-010',
        'Vidrio Serigrafiado Decorativo',
        'Serigrafiado',
        'Vidrio con diseños serigrafiados en cerámica cocida al fuego. Personalizable con logos o patrones arquitectónicos.',
        'Espesor: 6-10mm | Diseño: Personalizable | Durabilidad: Permanente | Uso: Fachadas, divisiones corporativas',
        '/static/img/vidrios/VP-010.jpg',
        1
    ),
]

with app.app_context():
    db = get_db()
    cur = db.cursor()

    for v in VIDRIOS:
        ref_code = v[0]
        cur.execute("SELECT id FROM productos WHERE ref_code = %s", (ref_code,))
        existe = cur.fetchone()

        if existe:
            cur.execute("""
                UPDATE productos 
                SET nombre=%s, tipo_vidrio=%s, descripcion=%s, especificaciones=%s, imagen_principal=%s, activo=%s
                WHERE ref_code=%s
            """, (v[1], v[2], v[3], v[4], v[5], v[6], ref_code))
            print(f"Actualizado: {ref_code}")
        else:
            cur.execute("""
                INSERT INTO productos (ref_code, nombre, tipo_vidrio, descripcion, especificaciones, imagen_principal, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, v)
            print(f"Insertado: {ref_code}")

    db.commit()
    print("Listo. 10 vidrios en base de datos.")