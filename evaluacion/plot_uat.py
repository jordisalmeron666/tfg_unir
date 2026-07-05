#!/usr/bin/env python3
"""
plot_uat.py — Genera el cuadro de mando UAT a partir de uat_data.json

Uso:  python3 evaluacion/plot_uat.py
      (requiere haber ejecutado parse_uat.py antes)
Salida: evaluacion/uat_dashboard.png
"""

import json
import math
import statistics
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')          # sin GUI; cambiar a 'TkAgg' si quieres ventana
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches

# ── Datos ─────────────────────────────────────────────────────────────────────

base = Path(__file__).parent
data_path = base / 'uat_data.json'
if not data_path.exists():
    raise FileNotFoundError(
        'No se encontró uat_data.json. Ejecuta primero parse_uat.py'
    )

with data_path.open(encoding='utf-8') as f:
    data = json.load(f)

N = len(data)

# ── Helpers ───────────────────────────────────────────────────────────────────

def vals(key):
    return [r[key] for r in data if r.get(key) is not None]

def mean_of(key):
    v = vals(key)
    return statistics.mean(v) if v else 0.0

def pstd_of(key):
    v = vals(key)
    return statistics.pstdev(v) if v else 0.0

def block_mean(items):
    v = [r[q] for r in data for q in items if r.get(q) is not None]
    return statistics.mean(v) if v else 0.0

def p5_counts(block_key, label_list):
    return [sum(1 for r in data if r.get(block_key, {}).get(lbl, False))
            for lbl in label_list]

# ── Ítems Likert ──────────────────────────────────────────────────────────────

ITEMS_B1 = ['P1.1', 'P1.2', 'P1.3', 'P1.4', 'P1.5']
ITEMS_B2 = ['P2.1', 'P2.2', 'P2.3', 'P2.4', 'P2.5', 'P2.6']
ITEMS_B3 = ['P3.1', 'P3.2', 'P3.3', 'P3.4']
ALL_ITEMS = ITEMS_B1 + ITEMS_B2 + ITEMS_B3

ITEM_LABELS = {
    'P1.1': 'Fácil\nde usar',  'P1.2': 'Natural/\nintuitivo',
    'P1.3': 'Tiempo\nresp.',   'P1.4': 'Comunica\nlímites',
    'P1.5': 'Uso en\npartida',
    'P2.1': 'Precisión',       'P2.2': 'Cita\nfuente',
    'P2.3': 'Completitud',     'P2.4': 'Claridad',
    'P2.5': 'No\nalucina',     'P2.6': 'Confianza',
    'P3.1': 'Resuelve\nproblema', 'P3.2': 'Más rápido\nque PDF',
    'P3.3': 'Ahorra\ntiempo',  'P3.4': 'Lo\nrecomendaría',
}

item_means = [mean_of(k) for k in ALL_ITEMS]
item_stds  = [pstd_of(k)  for k in ALL_ITEMS]

b1_mean = block_mean(ITEMS_B1)
b2_mean = block_mean(ITEMS_B2)
b3_mean = block_mean(ITEMS_B3)

p61_mean = mean_of('P6.1')
p61_std  = pstd_of('P6.1')

# ── Paleta ────────────────────────────────────────────────────────────────────

C_B1  = '#4C72B0'   # azul  — Usabilidad
C_B2  = '#55A868'   # verde — Calidad
C_B3  = '#DD8452'   # naranja — Utilidad
C_REF = '#E74C3C'   # rojo  — umbral / referencia
C_BG  = '#F7F9FC'

BAR_COLORS = [C_B1]*len(ITEMS_B1) + [C_B2]*len(ITEMS_B2) + [C_B3]*len(ITEMS_B3)

# ── Figura ────────────────────────────────────────────────────────────────────

fig = plt.figure(figsize=(20, 15), facecolor=C_BG)

gs = gridspec.GridSpec(
    3, 3,
    figure=fig,
    height_ratios=[1.7, 1.1, 1.1],
    hspace=0.60, wspace=0.38,
    left=0.06, right=0.97, top=0.91, bottom=0.06,
)

ax_radar  = fig.add_subplot(gs[0, 0], projection='polar')
ax_likert = fig.add_subplot(gs[0, 1:])
ax_p51    = fig.add_subplot(gs[1, 0])
ax_p52    = fig.add_subplot(gs[1, 1:])
ax_p4     = fig.add_subplot(gs[2, 0])
ax_p62    = fig.add_subplot(gs[2, 1])
ax_p63    = fig.add_subplot(gs[2, 2])

fig.suptitle(
    'Cuadro de mando UAT — Bot de consulta de reglamentos de wargames\n'
    f'n={N} evaluadores  ·  Puntuación global media: {p61_mean:.1f}/10  '
    f'(σ={p61_std:.2f})',
    fontsize=14, fontweight='bold', y=0.96,
)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. RADAR — 5 dimensiones
# ═══════════════════════════════════════════════════════════════════════════════

confianza_mean = statistics.mean([mean_of('P2.5'), mean_of('P2.6')])
velocidad_mean = statistics.mean([mean_of('P1.3'), mean_of('P3.2')])

radar_labels = [
    f'Usabilidad\n({b1_mean:.2f})',
    f'Calidad\n({b2_mean:.2f})',
    f'Utilidad\n({b3_mean:.2f})',
    f'Confianza\n({confianza_mean:.2f})',
    f'Velocidad\n({velocidad_mean:.2f})',
]
radar_vals = [b1_mean, b2_mean, b3_mean, confianza_mean, velocidad_mean]

n_dim = len(radar_vals)
angles = np.linspace(0, 2 * math.pi, n_dim, endpoint=False).tolist()
# close polygon
rv_full  = radar_vals + radar_vals[:1]
ang_full = angles + angles[:1]
ref_full = [4.0] * n_dim + [4.0]

ax_radar.set_facecolor(C_BG)
ax_radar.plot(ang_full, rv_full,  'o-',  color=C_B1, linewidth=2.5, zorder=3)
ax_radar.fill(ang_full, rv_full,          color=C_B1, alpha=0.20, zorder=2)
ax_radar.plot(ang_full, ref_full, '--',  color=C_REF, linewidth=1.5, alpha=0.75,
              label='Umbral 4.0', zorder=1)
ax_radar.fill(ang_full, ref_full,         color=C_REF, alpha=0.04, zorder=0)

ax_radar.set_xticks(angles)
ax_radar.set_xticklabels(radar_labels, size=8.5)
ax_radar.set_ylim(0, 5)
ax_radar.set_yticks([1, 2, 3, 4, 5])
ax_radar.set_yticklabels(['1', '2', '3', '4', '5'], size=7, color='#888888')
ax_radar.tick_params(pad=8)
ax_radar.set_title('Perfil de dimensiones', fontsize=10, fontweight='bold', pad=18)
ax_radar.legend(loc='lower left', bbox_to_anchor=(-0.15, -0.12), fontsize=8)

# ═══════════════════════════════════════════════════════════════════════════════
# 2. BARRAS — todos los ítems Likert
# ═══════════════════════════════════════════════════════════════════════════════

x_pos = np.arange(len(ALL_ITEMS))
ax_likert.bar(x_pos, item_means, color=BAR_COLORS, alpha=0.82,
              edgecolor='white', linewidth=0.6, zorder=2)
ax_likert.errorbar(x_pos, item_means, yerr=item_stds,
                   fmt='none', color='#333333', capsize=3, linewidth=1.4, zorder=3)
ax_likert.axhline(4.0, color=C_REF, linewidth=1.8, linestyle='--', alpha=0.85,
                  label='Umbral satisfactorio (4.0)', zorder=4)

ax_likert.set_xticks(x_pos)
ax_likert.set_xticklabels(
    [ITEM_LABELS[k] for k in ALL_ITEMS],
    rotation=0, ha='center', fontsize=8,
)
ax_likert.set_ylim(0, 5.8)
ax_likert.set_ylabel('Media (1–5)', fontsize=9)
ax_likert.set_title('Medias por ítem Likert (agrupadas por bloque)', fontsize=10, fontweight='bold')
ax_likert.set_facecolor(C_BG)
ax_likert.grid(axis='y', alpha=0.30, zorder=0)

# Separadores entre bloques
for sep in (len(ITEMS_B1) - 0.5, len(ITEMS_B1) + len(ITEMS_B2) - 0.5):
    ax_likert.axvline(sep, color='#AAAAAA', linewidth=1, linestyle=':', zorder=1)

# Etiquetas de bloque encima de cada grupo
b1_mid = (len(ITEMS_B1) - 1) / 2
b2_mid = len(ITEMS_B1) + (len(ITEMS_B2) - 1) / 2
b3_mid = len(ITEMS_B1) + len(ITEMS_B2) + (len(ITEMS_B3) - 1) / 2

for mid, bm, col, lbl in [
    (b1_mid, b1_mean, C_B1, f'B1 Usabilidad\n{b1_mean:.2f}'),
    (b2_mid, b2_mean, C_B2, f'B2 Calidad resp.\n{b2_mean:.2f}'),
    (b3_mid, b3_mean, C_B3, f'B3 Utilidad\n{b3_mean:.2f}'),
]:
    ax_likert.text(mid, 5.45, lbl, ha='center', fontsize=8.5, fontweight='bold',
                   color=col,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                             edgecolor=col, alpha=0.9))

legend_patches = [
    mpatches.Patch(color=C_B1, label=f'B1 Usabilidad  ({b1_mean:.2f})'),
    mpatches.Patch(color=C_B2, label=f'B2 Calidad resp.  ({b2_mean:.2f})'),
    mpatches.Patch(color=C_B3, label=f'B3 Utilidad  ({b3_mean:.2f})'),
    plt.Line2D([0], [0], color=C_REF, linestyle='--', label='Umbral 4.0'),
]
ax_likert.legend(handles=legend_patches, loc='lower right', fontsize=8.5)

# ═══════════════════════════════════════════════════════════════════════════════
# 3. P5.1 — Problemas encontrados
# ═══════════════════════════════════════════════════════════════════════════════

P51_LABELS = [
    'Tardó demasiado',
    'No entendió la pregunta',
    'Resp. incompleta',
    'Resp. incorrecta',
    'Sin info (había):',
    'No supe expresarme',
    'Sin problemas',
]
p51_counts = p5_counts('P5.1', P51_LABELS)
p51_colors = ['#27AE60' if lbl == 'Sin problemas' else '#E74C3C' for lbl in P51_LABELS]

y51 = np.arange(len(P51_LABELS))
ax_p51.barh(y51, p51_counts, color=p51_colors, alpha=0.80, edgecolor='white', zorder=2)
ax_p51.set_yticks(y51)
ax_p51.set_yticklabels(P51_LABELS, fontsize=8.5)
ax_p51.set_xlabel('Nº evaluadores', fontsize=8)
ax_p51.set_xlim(0, N + 0.8)
ax_p51.set_xticks(range(N + 1))
ax_p51.set_title('P5.1 — Problemas encontrados', fontsize=10, fontweight='bold')
for i, v in enumerate(p51_counts):
    if v:
        ax_p51.text(v + 0.08, i, str(v), va='center', fontsize=9.5, fontweight='bold')
ax_p51.set_facecolor(C_BG)
ax_p51.grid(axis='x', alpha=0.30, zorder=0)
ax_p51.invert_yaxis()

# ═══════════════════════════════════════════════════════════════════════════════
# 4. P5.2 — Mejoras deseadas (ordenadas por demanda)
# ═══════════════════════════════════════════════════════════════════════════════

P52_LABELS = [
    'Más reglamentos',
    'Trasfondo/lore',
    'Resps. más cortas',
    'Resps. más detalladas',
    'Historial de chat',
    'Acceso web/app',
    'Multimodal (voz/img)',
    'Búsqueda keywords',
    'Otra (modo torneo)',
]
p52_counts_raw = p5_counts('P5.2', P52_LABELS)

# Ordenar descendente
pairs = sorted(zip(p52_counts_raw, P52_LABELS), reverse=True)
p52_counts_s = [c for c, _ in pairs]
p52_labels_s = [l for _, l in pairs]

cmap = plt.cm.YlOrRd
max_c = max(p52_counts_s) if max(p52_counts_s) > 0 else 1
p52_colors_s = [cmap(0.35 + 0.65 * (c / max_c)) for c in p52_counts_s]

y52 = np.arange(len(P52_LABELS))
ax_p52.barh(y52, p52_counts_s, color=p52_colors_s, alpha=0.85, edgecolor='white', zorder=2)
ax_p52.set_yticks(y52)
ax_p52.set_yticklabels(p52_labels_s, fontsize=8.5)
ax_p52.set_xlabel('Nº evaluadores', fontsize=8)
ax_p52.set_xlim(0, N + 0.8)
ax_p52.set_xticks(range(N + 1))
ax_p52.set_title('P5.2 — Mejoras deseadas (orden por demanda)', fontsize=10, fontweight='bold')
for i, v in enumerate(p52_counts_s):
    if v:
        ax_p52.text(v + 0.08, i, str(v), va='center', fontsize=9.5, fontweight='bold')
ax_p52.set_facecolor(C_BG)
ax_p52.grid(axis='x', alpha=0.30, zorder=0)
ax_p52.invert_yaxis()

# ═══════════════════════════════════════════════════════════════════════════════
# 5. P4.2 / P4.3 — Bot vs. alternativas actuales
# ═══════════════════════════════════════════════════════════════════════════════

options     = [-2, -1, 0, 1, 2]
opt_labels  = ['Mucho\npeor', 'Peor', 'Similar', 'Mejor', 'Mucho\nmejor']
p42_vals    = vals('P4.2')
p43_vals    = vals('P4.3')
p42_counts  = [p42_vals.count(o) for o in options]
p43_counts  = [p43_vals.count(o) for o in options]

xp4 = np.arange(len(options))
w   = 0.36
ax_p4.bar(xp4 - w/2, p42_counts, w, label='Bot vs PDF',          color='#3498DB', alpha=0.82)
ax_p4.bar(xp4 + w/2, p43_counts, w, label='Bot vs otros jugadores', color='#9B59B6', alpha=0.82)
ax_p4.set_xticks(xp4)
ax_p4.set_xticklabels(opt_labels, fontsize=8.5)
ax_p4.set_ylabel('Nº evaluadores', fontsize=8)
ax_p4.set_ylim(0, N + 0.8)
ax_p4.set_yticks(range(N + 1))
ax_p4.set_title('P4 — Bot vs. alternativas actuales', fontsize=10, fontweight='bold')
ax_p4.legend(fontsize=8)
ax_p4.set_facecolor(C_BG)
ax_p4.grid(axis='y', alpha=0.30)
# zona verde para "Mejor" y "Mucho mejor"
ax_p4.axvspan(2.4, len(options) - 0.5, alpha=0.07, color='green')
ax_p4.text(3.5, N + 0.3, '✓', ha='center', fontsize=14, color='#27AE60', fontweight='bold')

# ═══════════════════════════════════════════════════════════════════════════════
# 6. P6.2 — ¿Cumple su objetivo?
# ═══════════════════════════════════════════════════════════════════════════════

P62_OPTIONS = ['Sí, plenamente', 'Sí, con matices', 'Parcialmente', 'No']
P62_COLORS  = ['#2ECC71', '#F39C12', '#E67E22', '#E74C3C']
p62_raw     = [r.get('P6.2_raw', '') for r in data]
p62_counts  = [p62_raw.count(o) for o in P62_OPTIONS]

p62_data = [(c, o, cl) for c, o, cl in zip(p62_counts, P62_OPTIONS, P62_COLORS) if c > 0]
if p62_data:
    counts_, labels_, colors_ = zip(*p62_data)
    wedges, _, autotexts = ax_p62.pie(
        counts_, labels=labels_, colors=colors_,
        autopct='%1.0f%%', startangle=90, pctdistance=0.72,
        textprops={'fontsize': 8.5},
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight('bold')
ax_p62.set_title('P6.2 — ¿Cumple su objetivo?', fontsize=10, fontweight='bold')

# ═══════════════════════════════════════════════════════════════════════════════
# 7. P6.3 — ¿Lo usarías regularmente?
# ═══════════════════════════════════════════════════════════════════════════════

P63_OPTIONS = ['Sí, sin duda', 'Probablemente sí', 'Tal vez', 'Probablemente no', 'No']
P63_COLORS  = ['#1ABC9C', '#3498DB', '#F39C12', '#E67E22', '#E74C3C']
p63_raw     = [r.get('P6.3_raw', '') for r in data]
p63_counts  = [p63_raw.count(o) for o in P63_OPTIONS]

p63_data = [(c, o, cl) for c, o, cl in zip(p63_counts, P63_OPTIONS, P63_COLORS) if c > 0]
if p63_data:
    counts_, labels_, colors_ = zip(*p63_data)
    wedges, _, autotexts = ax_p63.pie(
        counts_, labels=labels_, colors=colors_,
        autopct='%1.0f%%', startangle=90, pctdistance=0.72,
        textprops={'fontsize': 8.5},
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight('bold')
ax_p63.set_title(
    f'P6.3 — ¿Lo usarías regularmente?\n'
    f'(P6.1 puntuación media: {p61_mean:.1f}/10  σ={p61_std:.2f})',
    fontsize=10, fontweight='bold',
)

# ═══════════════════════════════════════════════════════════════════════════════
# Guardar
# ═══════════════════════════════════════════════════════════════════════════════

out_path = base / 'uat_dashboard.png'
plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor=C_BG)
print(f'✓ Dashboard guardado: {out_path}')
