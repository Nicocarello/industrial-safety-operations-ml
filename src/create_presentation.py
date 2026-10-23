import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Brand Colors
TEAL = RGBColor(0, 168, 107)         # Emerald / Teal Accent
DARK_TEAL = RGBColor(10, 92, 54)
NAVY = RGBColor(15, 23, 42)          # Text header
BODY_GRAY = RGBColor(71, 85, 105)    # Body text
CARD_BG = RGBColor(248, 250, 252)    # #F8FAFC
ALERT_RED = RGBColor(225, 29, 72)
WHITE = RGBColor(255, 255, 255)
LIGHT_BORDER = RGBColor(226, 232, 240)

def create_unified_deck():
    prs = Presentation('template_base.pptx')
    slide_width = prs.slide_width
    slide_height = prs.slide_height

    def add_header(slide, title_text, category_text="TECHNOSTAMP INDUSTRIES | DECISION SCIENCE REPORT"):
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = category_text.upper()
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEAL

        txBox2 = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.5), Inches(0.6))
        tf2 = txBox2.text_frame
        tf2.word_wrap = True
        p2 = tf2.paragraphs[0]
        p2.text = title_text
        p2.font.size = Pt(19)
        p2.font.bold = True
        p2.font.color.rgb = NAVY

    def add_card(slide, left, top, width, height, title, points, bg_color=CARD_BG, border_color=LIGHT_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.18)
        tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.18)
        tf.margin_bottom = Inches(0.18)

        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = NAVY

        for pt in points:
            p_pt = tf.add_paragraph()
            p_pt.text = "* " + pt
            p_pt.font.size = Pt(9.5)
            p_pt.font.color.rgb = BODY_GRAY
            p_pt.space_after = Pt(3)
        return shape

    # SLIDE 1: Cover Slide
    s1 = prs.slides[0]
    tb = s1.shapes.add_textbox(Inches(4.5), Inches(2.1), Inches(8.2), Inches(3.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "DECISION SCIENCE & ADVANCED ANALYTICS | C-LEVEL"
    p0.font.bold = True
    p0.font.size = Pt(12)
    p0.font.color.rgb = TEAL
    p0.space_after = Pt(6)

    p1 = tf.add_paragraph()
    p1.text = "TechnoStamp Industries: Del Dato a la Estrategia"
    p1.font.bold = True
    p1.font.size = Pt(27)
    p1.font.color.rgb = NAVY
    p1.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = "Diagnóstico integral, auditoría forense de datos, econometría y modelos predictivos para el Directorio y CEO."
    p2.font.size = Pt(13.5)
    p2.font.color.rgb = BODY_GRAY
    p2.space_after = Pt(14)

    p3 = tf.add_paragraph()
    p3.text = "People Analytics & Decision Science | Strategic Workforce Advisory"
    p3.font.size = Pt(11)
    p3.font.italic = True
    p3.font.color.rgb = TEAL

    # SLIDE 2: Resumen Ejecutivo
    s2 = prs.slides[1]
    tb_s2 = s2.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.5), Inches(0.8))
    tf_s2 = tb_s2.text_frame
    p_s2 = tf_s2.paragraphs[0]
    p_s2.text = "RESUMEN EJECUTIVO: 5 INSIGHTS CLAVE PARA EL DIRECTORIO"
    p_s2.font.bold = True
    p_s2.font.size = Pt(21)
    p_s2.font.color.rgb = WHITE

    kpi_cards = [
        {"title": "1. Crisis Turno Noche", "val": "5.3x Riesgo / +101% Scrap", "desc": "Concentra el 56% de accidentes y doble de scrap. 0 supervisores en planta. Pico de scrap de invierno 2024 derivó en despido del Plant Manager."},
        {"title": "2. Abismo de Sucesión", "val": "80% en <= 12 Meses", "desc": "Logística pierde el 100% de jefaturas. Error legal en ERP (fórmula 65 años) ocultó que Teresa Rodríguez (64a) ya puede jubilarse de inmediato."},
        {"title": "3. Sobrecarga y Fuga", "val": "$1.422M en HE / 35% Rotación", "desc": "Mantenimiento Eléctrico sufre Time-to-Fill de 67 días. 4 supervisores concentran el 60-80% de las renuncias voluntarias por exceso de horas extra."},
        {"title": "4. Seguridad y Modelo ML", "val": "Umbral >20h = 5.4x Riesgo", "desc": "78% de accidentados no fue capacitado. Desarrollamos un Modelo Predictivo (ROC-AUC 0.88) que captura el 83.3% de accidentes en el top 20% de riesgo."}
    ]
    for i, c in enumerate(kpi_cards):
        left = Inches(0.8 + i * 2.95)
        add_card(s2, left, Inches(1.75), Inches(2.75), Inches(4.7), c["title"], [
            f"MÉTRICA CLAVE: {c['val']}",
            c["desc"],
            "Impacto Directo: >$360M ARS anuales de ahorro potencial en EBITDA."
        ], bg_color=WHITE)

    # SLIDE 3: Pregunta 1 - Turno Noche y Crisis de Invierno 2024
    s3 = prs.slides[2]
    add_header(s3, "1. La Triple Crisis del Turno Noche y el Veredicto del Scrap")
    if os.path.exists('assets/figures/fig1_turno_noche_crisis.png'):
        s3.shapes.add_picture('assets/figures/fig1_turno_noche_crisis.png', Inches(0.8), Inches(1.5), width=Inches(7.1))

    add_card(s3, Inches(8.1), Inches(1.5), Inches(4.4), Inches(5.3), "Diagnóstico e Impacto Operativo", [
        "Doble de Scrap: Turno Noche promedia 3.60% vs 1.79% diurno (t=42.17, p<0.0001). Aporta 1.757 días perdidos (71.4% de la planta) y >18.600 piezas de scrap excedente.",
        "5.3x Mayor Tasa de Accidentes: 11.77 por mil emp-mes vs 2.22 diurno. Concentra 25 de 45 accidentes y 5 de 6 casos graves.",
        "Causa Raíz Organizacional: Planta acéfala. Cero Supervisores (Nivel 3) ni Gerentes (Nivel 4/5) presentes de noche.",
        "Crisis Oculta de Invierno 2024: En Jun-Ago 2024 el scrap en Estampado saltó a 4.78% (Setup 5.45%), provocando el despido del Plant Manager (Damián Barbieri, ID 1001) en Dic 2024. Puesto sigue VACANTE en 2025.",
        "Acción: Asignar 2 Supervisores rotativos al Turno Noche y cubrir de inmediato la Gerencia de Planta."
    ])

    # SLIDE 4: Pregunta 2 - Puestos Críticos y Error Legal
    s4 = prs.slides[3]
    add_header(s4, "2. Abismo de Sucesión y el 'Punto Ciego Legal' de RRHH")
    if os.path.exists('assets/figures/fig3_retirement_cliff_logistica.png'):
        s4.shapes.add_picture('assets/figures/fig3_retirement_cliff_logistica.png', Inches(0.8), Inches(1.5), width=Inches(7.2))

    add_card(s4, Inches(8.2), Inches(1.5), Inches(4.3), Inches(5.3), "Vulnerabilidad en Continuidad", [
        "Pérdida del 80% en 12 Meses: De 5 posiciones críticas activas, 4 se jubilan en <=12 meses.",
        "Decapitación Total en Logística: En 12 meses se van la Supervisora (Ana Ortiz, 6m) y ambos Team Leaders (Sergio Reyes, 9m; Miguel De Luca, 12m).",
        "El Error Legal de RRHH: El ERP calculó jubilación a los 65 años para ambos géneros. En Argentina, las mujeres se jubilan a los 60 años.",
        "Riesgo Omitido: Teresa Rodríguez (Técnico Setup Estampado, 64 años, 11.3 años de experiencia) ya tiene edad vencida y puede jubilarse de inmediato sin sucesor.",
        "Falsas Jubilaciones en ERP: 6 empleados de 26 a 45 años fueron rotulados erróneamente como 'Jubilación' por falta de validación en el sistema.",
        "Acción: Activar programa de Shadowing de 90 días en Logística y Estampado con incentivo por transferencia de know-how."
    ])

    # SLIDE 5: Pregunta 3 - Horas Extra, Reclutamiento y Managers Tóxicos
    s5 = prs.slides[4]
    add_header(s5, "3. Horas Extra ($1.422M), Time to Fill (67d) y Efecto Manager")
    if os.path.exists('assets/figures/fig6_recruitment_bottlenecks.png'):
        s5.shapes.add_picture('assets/figures/fig6_recruitment_bottlenecks.png', Inches(0.8), Inches(1.5), width=Inches(7.2))

    add_card(s5, Inches(8.2), Inches(1.5), Inches(4.3), Inches(5.3), "Círculo Vicioso de Dotación", [
        "Gasto Crónico: $1.422M en 98.260 hs extra. El 99.8% de operarios hace horas extra mensuales. No son picos: es falta de personal.",
        "El Cuello de Botella: Time to Fill promedia 66.6 días en Mantenimiento Eléctrico y 70.9 días en Mecánico. Tardan 2 meses y medio en cubrir cada baja.",
        "Efecto 'Manager Tóxico': La rotación se concentra en 4 supervisores puntuales: Alan Marino (80% bajas), Facundo Ricci (80%), Isaías Peña (71%) y Luciano Chávez (60%).",
        "Evasión de Fuga en Mantenimiento: El área perdió el 34.8% de su dotación (23.9% por renuncia voluntaria) por jornadas de >21 hs extra/mes.",
        "Acción: Alianza con agencias técnicas para bajar Time-to-Fill a <25 días y auditar el estilo de liderazgo de los 4 supervisores críticos."
    ])

    # SLIDE 6: Pregunta 4 & 5 - Seguridad, Fatiga y Modelo Predictivo ML
    s6 = prs.slides[5]
    add_header(s6, "4. Seguridad, Umbral de Fatiga y Sistema Predictivo ML")
    if os.path.exists('assets/figures/fig2_overtime_cost_by_area.png'):
        s6.shapes.add_picture('assets/figures/fig2_overtime_cost_by_area.png', Inches(0.8), Inches(1.5), width=Inches(7.2))

    add_card(s6, Inches(8.2), Inches(1.5), Inches(4.3), Inches(5.3), "Prevención Científica y ROI", [
        "Umbral Crítico de Fatiga: Operarios con >20 hs extra/mes quintuplican su probabilidad de accidente (de 0.63% a 3.40%).",
        "Brecha en Capacitación: El 78% de los accidentados jamás tuvo entrenamiento en seguridad. Completar cursos de seguridad reduce la siniestralidad en 59.7% (de 13.3 a 5.4 por mil).",
        "Discrepancia de Seguridad: Panel tiene 100 incidentes (enfermería/leves) vs 45 en eventos_rrhh (bajas formales a ART).",
        "Modelo Predictivo en Producción: Entrenamos un algoritmo LightGBM (ROC-AUC 0.88) que predice siniestros y permite intervenir preventivamente sobre el top 20% de mayor score, capturando el 83.3% de los accidentes futuros.",
        "Diversidad: 37% de mujeres. No hay brecha salarial en Niveles 1 a 3 (<1%), pero sí un gap de 7% en Nivel 4 y baja presencia en Ensamble (26.8%) e Ingeniería (28.6%)."
    ])

    # SLIDE 7: Plan 30-60-90 y Proyección EBITDA
    s7 = prs.slides[6]
    add_header(s7, "5. Hoja de Ruta 30-60-90 Días y Retorno en EBITDA (+$363M)")

    plans = [
        {"title": "0 - 30 DÍAS: CONTENCIÓN", "pts": [
            "Supervisión Nocturna: Reasignar 2 Supervisores Nivel 3 al Turno Noche rotativos.",
            "Sucesión de Emergencia: Nombrar aprendices para Ana Ortiz y Teresa Rodríguez.",
            "Cubrir Plant Manager: Designar de inmediato al Director de Planta vacante desde Dic 2024.",
            "Auditoría a 4 Supervisores: Intervención de RRHH en equipos con 60-80% de bajas."
        ]},
        {"title": "31 - 60 DÍAS: ESTABILIZACIÓN", "pts": [
            "Reducción Time-to-Fill: Alianzas técnicas para acortar cobertura eléctrica a <25 días.",
            "Capacitación Obligatoria: 100% de operarios de Ensamble y Estampado en Seguridad.",
            "Hard-Cap de Horas Extra: Tope de 15 hs/mes por operario para cortar accidentes por fatiga.",
            "Corrección ERP: Ajustar edad jubilatoria femenina a 60 años y limpiar falsas jubilaciones."
        ]},
        {"title": "61 - 90+ DÍAS: INSTITUCIONALIZACIÓN", "pts": [
            "Despliegue de Modelo ML: Tablero diario de Early Warning para alertar riesgo de accidente.",
            "Alineación Salarial: Nivelar brecha del 7% en Nivel 4 y promover operarias Top Performers.",
            "Incentivos por Calidad: Bonos atados a tasa de scrap y días sin accidentes.",
            "Impacto Neto en EBITDA: Ahorro anualizado de >$363 Millones de pesos en P&L."
        ]}
    ]

    for idx, p in enumerate(plans):
        add_card(s7, Inches(0.8 + idx * 3.95), Inches(1.5), Inches(3.75), Inches(5.3), p["title"], p["pts"],
                 border_color=TEAL if idx==0 else LIGHT_BORDER)

    output_path = 'Presentacion_Directorio_TechnoStamp.pptx'
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == '__main__':
    create_unified_deck()
