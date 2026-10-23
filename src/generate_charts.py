import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure directory exists
os.makedirs('assets/figures', exist_ok=True)

# Set global aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['figure.titlesize'] = 15

# Executive Palette Colors
TEAL_PRIMARY = '#00A86B'     # Vibrant Emerald/Teal Accent
TEAL_DARK = '#0A5C36'
NAVY_DEEP = '#0F172A'
SLATE_GRAY = '#64748B'
ALERT_RED = '#E11D48'
AMBER_WARN = '#F59E0B'
LIGHT_BG = '#F8FAFC'
CARD_BG = '#FFFFFF'

# Load datasets
df_emp = pd.read_csv('data/empleados_mensual.csv', encoding='latin-1')
df_eve = pd.read_csv('data/eventos_rrhh.csv', encoding='latin-1')
df_cap = pd.read_csv('data/capacitaciones.csv', encoding='latin-1')

emp_active = df_emp[df_emp['activo'] == True]
latest_active = df_emp[(df_emp['mes_snapshot'] == '2025-05-01') & (df_emp['activo'] == True)]
df_unique_last = df_emp.sort_values('mes_snapshot').groupby('empleado_id').last().reset_index()

print("--- GENERATING COMPLETE UNIFIED CHARTS ---")

# -------------------------------------------------------------
# FIG 1: TURNO NOCHE TRIPLE CRISIS (Scrap Rate vs Accident Rate)
# -------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(10, 5.8), dpi=300)
shifts = ['Mañana', 'Tarde', 'Noche', 'Rotativo', 'Administrativo']
scrap_by_shift = emp_active.groupby('turno_trabajo')['tasa_scrap_porcentaje'].mean()
acc_by_shift = df_eve[df_eve['tipo_evento'] == 'incidente_seguridad']['turno_evento'].value_counts()
emp_counts = emp_active['turno_trabajo'].value_counts()

scrap_vals = [scrap_by_shift.get(s, 0) for s in shifts]
acc_rates = [(acc_by_shift.get(s, 0) / emp_counts.get(s, 1)) * 1000 for s in shifts]

x = np.arange(len(shifts))
width = 0.35

rects1 = ax1.bar(x - width/2, scrap_vals, width, label='Tasa de Scrap Promedio (%)', color=['#3B82F6', '#3B82F6', ALERT_RED, '#3B82F6', '#94A3B8'], alpha=0.9)
ax1.set_ylabel('Tasa de Scrap (%)', color='#1E293B')
ax1.set_ylim(0, 4.5)
ax1.grid(axis='y', linestyle='--', alpha=0.5)

for rect in rects1:
    h = rect.get_height()
    ax1.annotate(f'{h:.2f}%', xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=9.5)

ax2 = ax1.twinx()
rects2 = ax2.bar(x + width/2, acc_rates, width, label='Tasa Incidentes (x 1.000 emp-mes)', color=['#10B981', '#10B981', '#B91C1C', '#10B981', '#64748B'], alpha=0.9)
ax2.set_ylabel('Incidentes por 1.000 Empleados-Mes', color='#1E293B')
ax2.set_ylim(0, 15)
ax2.grid(False)

for rect in rects2:
    h = rect.get_height()
    ax2.annotate(f'{h:.1f}', xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=9.5, color='#0F172A')

ax1.set_xticks(x)
ax1.set_xticklabels(shifts, fontsize=10.5, fontweight='bold')
ax1.set_title('La Triple Crisis del Turno Noche: Disparo de Scrap (+101%) y Accidentes (5.3x)', pad=20)

ax1.annotate('Turno Noche:\n* Scrap: 3.60% (Doble de diurno)\n* Accidentes: 11.8 x 1.000 emp\n* 83% de accidentes graves\n* 0 Supervisores Nivel 3/4',
            xy=(2, 3.6), xytext=(2.6, 3.7),
            arrowprops=dict(facecolor=ALERT_RED, shrink=0.08, width=1.5, headwidth=8),
            bbox=dict(boxstyle="round,pad=0.5", fc="#FFF1F2", ec=ALERT_RED, lw=1.5),
            fontsize=9, fontweight='bold')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True, facecolor='white', edgecolor='#E2E8F0')

plt.tight_layout()
plt.savefig('assets/figures/fig1_turno_noche_crisis.png', dpi=300)
plt.close()
print("Saved fig1_turno_noche_crisis.png")

# -------------------------------------------------------------
# FIG 2: OVERTIME EXPONENTIAL ACCIDENT RISK CURVE
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2), dpi=300)

# Subplot 1: Probability of Accident by Overtime Bucket (Blue Collar)
blue_df = df_emp[df_emp['categoria_collar'] == 'Blue'].copy()
blue_df['tuvo_incidente'] = (blue_df['incidentes_seguridad_count'] > 0).astype(int)
blue_df['he_bucket'] = pd.cut(blue_df['horas_extra'], bins=[-1, 8, 12, 16, 20, 40], labels=['0-8 hs', '8-12 hs', '12-16 hs', '16-20 hs', '>20 hs'])
ot_risk = blue_df.groupby('he_bucket', observed=False)['tuvo_incidente'].mean() * 100

x_b = np.arange(len(ot_risk))
colors_ot = ['#10B981', '#3B82F6', AMBER_WARN, '#EA580C', ALERT_RED]
bars_ot = ax1.bar(x_b, ot_risk.values, color=colors_ot, width=0.55)
ax1.set_xticks(x_b)
ax1.set_xticklabels(ot_risk.index, fontweight='bold')
ax1.set_ylabel('Probabilidad Mensual de Accidente (%)')
ax1.set_xlabel('Carga Mensual de Horas Extra')
ax1.set_title('Umbral Crítico de Fatiga: Riesgo de Accidente Salta 5.4x en >20 hs', fontsize=11.5)
ax1.set_ylim(0, 4.2)
ax1.grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars_ot:
    h = bar.get_height()
    ax1.annotate(f'{h:.2f}%', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=9.5)

ax1.annotate('Umbral de Colapso (>20h):\nRiesgo sube de 0.63% a 3.40%', xy=(4, 3.4), xytext=(2.6, 3.6),
             arrowprops=dict(facecolor=ALERT_RED, shrink=0.08, width=1.5, headwidth=7),
             bbox=dict(boxstyle="round,pad=0.4", fc="#FFF1F2", ec=ALERT_RED, lw=1.2), fontsize=8.5, fontweight='bold')

# Subplot 2: Overtime cost by Area ($1.422B total)
ot_area = emp_active.groupby('area')['costo_horas_extra'].sum().sort_values(ascending=True) / 1e6
y_pos = np.arange(len(ot_area))
bars_c = ax2.barh(y_pos, ot_area.values, color=np.where(ot_area.values > 200, ALERT_RED, '#3B82F6'), height=0.6)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(ot_area.index, fontsize=9.5, fontweight='semibold')
ax2.set_xlabel('Costo Total Horas Extra (Millones de Pesos - 17 Meses)')
ax2.set_title('Gasto Acumulado en Horas Extra: $1.422M', fontsize=11.5)
ax2.set_xlim(0, 470)
ax2.grid(axis='x', linestyle='--', alpha=0.5)

for bar in bars_c:
    w = bar.get_width()
    ax2.annotate(f'${w:,.0f}M', xy=(w, bar.get_y() + bar.get_height()/2), xytext=(5, 0), textcoords="offset points", ha='left', va='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('assets/figures/fig2_overtime_cost_by_area.png', dpi=300)
plt.close()
print("Saved fig2_overtime_cost_by_area.png")

# -------------------------------------------------------------
# FIG 3: RETIREMENT CLIFF & THE ARGENTINE LEGAL RETIREMENT AUDIT
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300, gridspec_kw={'width_ratios': [1.1, 1]})

crit_data = [
    {'Nombre': 'Teresa Rodríguez (64a)', 'Área': 'Estampado', 'Puesto': 'Técnico Setup', 'Meses': 6, 'Status': 'Vencida según ley (60a)'},
    {'Nombre': 'Ana Beatriz Ortiz (64a)', 'Área': 'Logística', 'Puesto': 'Supervisor Logística', 'Meses': 6, 'Status': 'Vencida según ley (60a)'},
    {'Nombre': 'Sergio Reyes (63a)', 'Área': 'Logística', 'Puesto': 'Team Leader Logística', 'Meses': 9, 'Status': 'Retiro en 9 meses'},
    {'Nombre': 'Miguel A. De Luca (62a)', 'Área': 'Logística', 'Puesto': 'Team Leader Logística', 'Meses': 12, 'Status': 'Retiro en 12 meses'},
]
df_crit_plot = pd.DataFrame(crit_data)

bars_crit = ax1.barh(df_crit_plot['Nombre'], df_crit_plot['Meses'], color=[ALERT_RED, ALERT_RED, AMBER_WARN, AMBER_WARN], height=0.55)
ax1.set_xlabel('Meses Restantes hasta Jubilación en ERP')
ax1.set_title('Pérdida Inminente del 80% de Posiciones Críticas Activas', fontsize=11.5)
ax1.set_xlim(0, 15)
ax1.grid(axis='x', linestyle='--', alpha=0.5)

for bar, row in zip(bars_crit, crit_data):
    w = bar.get_width()
    ax1.annotate(f"{w} meses | {row['Puesto']} ({row['Área']})", xy=(w, bar.get_y() + bar.get_height() / 2), xytext=(8, 0), textcoords="offset points", ha='left', va='center', fontweight='bold', fontsize=9)

ax1.axvline(12, color=ALERT_RED, linestyle='--', linewidth=1.5, alpha=0.7)
ax1.text(12.2, 0.2, 'Límite 12 meses', color=ALERT_RED, fontweight='bold', rotation=90, va='bottom', fontsize=8.5)

# Subplot 2: Audit of Argentine Retirement Age vs System Blindspot
ax2.set_facecolor('#F8FAFC')
ax2.axis('off')
ax2.set_title('Auditoría Forense: El Punto Ciego Legal de RRHH', fontsize=11.5, fontweight='bold', pad=12)

boxes = [
    {'title': 'Error de Fórmula en el ERP de RRHH', 'desc': 'La columna meses_hasta_jubilacion asumió 65 años para ambos géneros. En Argentina, las mujeres se jubilan a los 60 años.', 'color': '#FFF1F2', 'border': ALERT_RED},
    {'title': 'Caso Testigo: Paola Marino (Estampado)', 'desc': 'Se jubiló en Mayo 2025 con 60 años, mientras el sistema reportaba que le faltaban 55 meses.', 'color': '#FEF3C7', 'border': AMBER_WARN},
    {'title': 'Riesgo de Omisión: Teresa Rodríguez', 'desc': 'Con 64 años y 11.3 años en Setup de prensas, tiene edad vencida y puede jubilarse de inmediato sin sucesor.', 'color': '#FEE2E2', 'border': ALERT_RED},
    {'title': 'Decapitación del 100% en Logística', 'desc': 'La Supervisora y ambos Team Leaders se jubilan en <=12 meses sin reemplazos identificados.', 'color': '#FEE2E2', 'border': ALERT_RED}
]

for idx, b in enumerate(boxes):
    y_coord = 0.85 - idx * 0.25
    ax2.annotate(f"* {b['title']}\n  {b['desc']}",
                xy=(0.5, y_coord), xycoords='axes fraction',
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.6', fc=b['color'], ec=b['border'], lw=1.5),
                fontsize=8.5, fontweight='semibold', color='#1E293B')

plt.tight_layout()
plt.savefig('assets/figures/fig3_retirement_cliff_logistica.png', dpi=300)
plt.close()
print("Saved fig3_retirement_cliff_logistica.png")

# -------------------------------------------------------------
# FIG 4: SAFETY TYPOLOGY & TRAINING GAP (22% trained vs 78% untrained)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

acc = df_eve[df_eve['tipo_evento']=='incidente_seguridad']
acc_subtypes = acc['subtipo_evento'].value_counts()

ax1.barh(acc_subtypes.index[::-1], acc_subtypes.values[::-1], color='#3B82F6', height=0.6)
ax1.set_title('Tipología de Incidentes en Planta (N=45 reportes formales)', fontsize=11.5)
ax1.set_xlabel('Cantidad de Incidentes')
for i, v in enumerate(acc_subtypes.values[::-1]):
    ax1.text(v + 0.3, i, f"{v} ({v/len(acc)*100:.1f}%)", va='center', fontweight='bold', fontsize=9)
ax1.set_xlim(0, 16)
ax1.grid(axis='x', linestyle='--', alpha=0.5)

# Donut chart: Training gap among accident victims
labels = ['Sin Capacitación\nde Seguridad (78.0%)', 'Con Capacitación\nde Seguridad (22.0%)']
sizes = [32, 9]
colors = [ALERT_RED, TEAL_PRIMARY]
explode = (0.05, 0)

ax2.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.0f%%',
        startangle=140, pctdistance=0.75, textprops={'fontsize': 9.5, 'fontweight': 'bold'},
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2))
ax2.set_title('Brecha Crítica: 78% de las Víctimas Jamás Recibió Capacitación\n(Efectividad de Seguridad: reduce incidentes de 13.3 a 5.4 por mil)', fontsize=11)

plt.tight_layout()
plt.savefig('assets/figures/fig4_safety_accidents_training_gap.png', dpi=300)
plt.close()
print("Saved fig4_safety_accidents_training_gap.png")

# -------------------------------------------------------------
# FIG 5: GENDER DIVERSITY & MERITOCRACY DIAGNOSTIC
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2), dpi=300)

gender_area = pd.crosstab(latest_active['area'], latest_active['genero'], normalize='index') * 100
gender_area = gender_area.sort_values(by='F', ascending=True)

y = np.arange(len(gender_area))
ax1.barh(y, gender_area['F'], color='#8B5CF6', height=0.6, label='% Mujeres (F)', alpha=0.9)
ax1.barh(y, gender_area['M'], left=gender_area['F'], color='#CBD5E1', height=0.6, label='% Varones (M)', alpha=0.9)
ax1.axvline(37.0, color='#6D28D9', linestyle='--', linewidth=1.5, label='Media Empresa (37%)')

ax1.set_yticks(y)
ax1.set_yticklabels(gender_area.index, fontsize=9.5, fontweight='semibold')
ax1.set_xlabel('% Distribución de Género')
ax1.set_title('Segregación Horizontal: Fuerte Déficit en Ensamble e Ingeniería', fontsize=11.5)
ax1.legend(loc='lower right', fontsize=8.5)
ax1.grid(axis='x', linestyle='--', alpha=0.5)

for i, f_val in enumerate(gender_area['F']):
    ax1.text(f_val / 2, i, f"{f_val:.1f}%", ha='center', va='center', color='white', fontweight='bold', fontsize=8.5)

# Performance & Pay comparison
x_comp = np.arange(4)
w = 0.35
rect1 = ax2.bar(x_comp - w/2, [3.26, 9.13, 1.67, 5.56], w, label='Mujeres (F)', color='#8B5CF6', alpha=0.9)
rect2 = ax2.bar(x_comp + w/2, [3.17, 7.34, 1.66, 5.97], w, label='Varones (M)', color='#64748B', alpha=0.9)

ax2.set_xticks(x_comp)
ax2.set_xticklabels(['Rating\n(Escala 1-5)', 'Top Performer\n(%)', 'Salario Niv 1\n($ Millones)', 'Salario Niv 4\n($ Millones)'], fontsize=9, fontweight='bold')
ax2.set_title('Paradoja del Mérito: Mayor Rendimiento Femenino pero Brecha en Nivel 4', fontsize=11.5)
ax2.legend(loc='upper left', fontsize=9)
ax2.grid(axis='y', linestyle='--', alpha=0.5)

for rect in rect1:
    h = rect.get_height()
    ax2.annotate(f'{h:.2f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')
for rect in rect2:
    h = rect.get_height()
    ax2.annotate(f'{h:.2f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig('assets/figures/fig5_gender_segregation_analysis.png', dpi=300)
plt.close()
print("Saved fig5_gender_segregation_analysis.png")

# -------------------------------------------------------------
# FIG 6: TOXIC MANAGERS & ATTRITION IN MAINTENANCE (NEW COMBINED)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2), dpi=300)

# Subplot 1: Top 5 Toxic Managers (Turnover Rate %)
mgr_bajas = df_unique_last.groupby(['manager_nombre', 'area']).agg(
    total=('empleado_id', 'count'),
    bajas=('activo', lambda x: (~x).sum()),
    rotacion_pct=('activo', lambda x: (~x).mean()*100),
    he_mean=('horas_extra', 'mean')
).reset_index()
top_mgr = mgr_bajas[mgr_bajas['total'] >= 5].sort_values(by='rotacion_pct', ascending=True).tail(6)

y_m = np.arange(len(top_mgr))
bars_m = ax1.barh(y_m, top_mgr['rotacion_pct'], color=ALERT_RED, height=0.55)
ax1.set_yticks(y_m)
ax1.set_yticklabels([f"{r['manager_nombre']} ({r['area'][:10]})" for _, r in top_mgr.iterrows()], fontsize=9, fontweight='semibold')
ax1.set_xlabel('% Rotación Total del Equipo')
ax1.set_title('El "Efecto Manager": 4 Supervisores con 60% a 80% de Fuga', fontsize=11.5)
ax1.set_xlim(0, 100)
ax1.grid(axis='x', linestyle='--', alpha=0.5)

for bar, (_, r) in zip(bars_m, top_mgr.iterrows()):
    w = bar.get_width()
    ax1.annotate(f"{w:.0f}% ({r['bajas']}/{r['total']}) | HE: {r['he_mean']:.1f}h", xy=(w, bar.get_y() + bar.get_height()/2), xytext=(5, 0), textcoords="offset points", ha='left', va='center', fontweight='bold', fontsize=8.5)

# Subplot 2: Time to Fill vs Turnover by Area
area_rot = df_unique_last.groupby('area').agg(
    rotacion_pct=('motivo_salida', lambda x: (x == 'Renuncia voluntaria').mean()*100),
    ttf_mean=('dias_time_to_fill', 'mean')
).dropna().sort_values(by='rotacion_pct', ascending=True)

y_a = np.arange(len(area_rot))
bars_a = ax2.barh(y_a, area_rot['rotacion_pct'], color=np.where(area_rot['rotacion_pct'] > 14, ALERT_RED, '#3B82F6'), height=0.55)
ax2.set_yticks(y_a)
ax2.set_yticklabels(area_rot.index, fontsize=9.5, fontweight='semibold')
ax2.set_xlabel('% Renuncia Voluntaria (Fuga de Talento)')
ax2.set_title('Mantenimiento Eléctrico: Mayor Fuga (24%) y Mayor Demora (67d)', fontsize=11.5)
ax2.set_xlim(0, 30)
ax2.grid(axis='x', linestyle='--', alpha=0.5)

for bar, (_, r) in zip(bars_a, area_rot.iterrows()):
    w = bar.get_width()
    ax2.annotate(f"{w:.1f}% (Time-to-Fill: {r['ttf_mean']:.0f}d)", xy=(w, bar.get_y() + bar.get_height()/2), xytext=(5, 0), textcoords="offset points", ha='left', va='center', fontweight='bold', fontsize=8.5)

plt.tight_layout()
plt.savefig('assets/figures/fig6_recruitment_bottlenecks.png', dpi=300)
plt.close()
print("Saved fig6_recruitment_bottlenecks.png")

# -------------------------------------------------------------
# FIG 7: WINTER 2024 SCRAP SPIKE & PLANT MANAGER TIMELINE (NEW)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 4.8), dpi=300)

scrap_trend = df_emp.pivot_table(index='mes_snapshot', columns='area', values='tasa_scrap_porcentaje', aggfunc='mean')
months = [m[2:7] for m in scrap_trend.index]

ax.plot(months, scrap_trend['Estampado'], marker='o', linewidth=2.5, color=ALERT_RED, label='Estampado (Pico Jun-Ago: 4.78%)')
ax.plot(months, scrap_trend['Ensamble'], marker='s', linewidth=1.8, color='#3B82F6', label='Ensamble (Prom: 1.95%)')
ax.plot(months, scrap_trend['Pintura'], marker='^', linewidth=1.8, color=TEAL_PRIMARY, label='Pintura (Prom: 2.28%)')

ax.set_ylabel('Tasa de Scrap Promedio (%)')
ax.set_xlabel('Mes Snapshot (2024 - 2025)')
ax.set_title('La Crisis Oculta de Scrap de Invierno 2024 y el Despido del Plant Manager', pad=15)
ax.set_ylim(1.0, 5.5)
ax.grid(True, linestyle='--', alpha=0.5)

# Annotate spike and Plant Manager dismissal
ax.annotate('Pico Crítico de Scrap:\n* Estampado salta a 4.78%\n* Setup alcanza 5.45%\n* Costo: >15.000 piezas scrap',
            xy=('24-06', 4.78), xytext=('24-03', 4.8),
            arrowprops=dict(facecolor=ALERT_RED, shrink=0.08, width=1.5, headwidth=7),
            bbox=dict(boxstyle="round,pad=0.4", fc="#FFF1F2", ec=ALERT_RED, lw=1.2), fontsize=8.5, fontweight='bold')

ax.annotate('Diciembre 2024:\nDespido del Plant Manager\n(Damián Barbieri, ID 1001)\nPuesto sigue VACANTE',
            xy=('24-12', 2.17), xytext=('24-10', 3.5),
            arrowprops=dict(facecolor=NAVY_DEEP, shrink=0.08, width=1.5, headwidth=7),
            bbox=dict(boxstyle="round,pad=0.4", fc="#F1F5F9", ec=NAVY_DEEP, lw=1.2), fontsize=8.5, fontweight='bold')

ax.legend(loc='lower left', frameon=True, facecolor='white', edgecolor='#E2E8F0', fontsize=9.5)
plt.tight_layout()
plt.savefig('assets/figures/fig7_scrap_spike_timeline.png', dpi=300)
plt.close()
print("Saved fig7_scrap_spike_timeline.png")

# Copy to brain artifact directory as well
import shutil
artifact_dir = r'C:\Users\nico_\.gemini\antigravity-ide\brain\f4fde8fa-2e92-42e0-8b3f-f5b8a85a727c'
for f in ['fig1_turno_noche_crisis.png', 'fig2_overtime_cost_by_area.png', 'fig3_retirement_cliff_logistica.png',
          'fig4_safety_accidents_training_gap.png', 'fig5_gender_segregation_analysis.png', 'fig6_recruitment_bottlenecks.png',
          'fig7_scrap_spike_timeline.png']:
    src_f = os.path.join('assets/figures', f)
    if os.path.exists(src_f):
        shutil.copy(src_f, os.path.join(artifact_dir, f))
print("All charts generated and copied to artifact directory successfully.")
