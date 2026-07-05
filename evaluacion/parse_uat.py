#!/usr/bin/env python3
"""
parse_uat.py — Lee los ficheros uat_respuesta_*.md y extrae los datos en uat_data.json

Uso:  python3 evaluacion/parse_uat.py
      (o desde dentro de la carpeta evaluacion/)
"""

import re
import json
import statistics
from pathlib import Path

# ── Mappings ─────────────────────────────────────────────────────────────────

COMPARISON_MAP = {
    'mucho peor': -2, 'peor': -1, 'similar': 0, 'mejor': 1, 'mucho mejor': 2
}

P01_MAP = {
    '< 1 año': 1, '1-3 años': 2, '3-10 años': 3, '> 10 años': 4
}

LIKERT_BLOCKS = {
    'B1': ['P1.1', 'P1.2', 'P1.3', 'P1.4', 'P1.5'],
    'B2': ['P2.1', 'P2.2', 'P2.3', 'P2.4', 'P2.5', 'P2.6'],
    'B3': ['P3.1', 'P3.2', 'P3.3', 'P3.4'],
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def parse_likert_row(row: str):
    """Devuelve (question_id, score 1-5) para una fila de tabla Likert, o None."""
    cells = [c.strip() for c in row.split('|') if c.strip()]
    if not cells or not re.match(r'^P\d+\.\d+$', cells[0]):
        return None
    qid = cells[0]
    # score columns start at index 2 (cells[2]=score1, ..., cells[6]=score5)
    for i, cell in enumerate(cells[2:7], start=1):
        if '✓' in cell:
            return qid, i
    return None


def parse_bold_answer(text: str, question_id: str) -> str | None:
    """Extrae el valor en negrita de la fila de tabla con el ID dado."""
    pattern = rf'\|\s*{re.escape(question_id)}\s*\|[^|]+\|\s*\*\*(.+?)\*\*'
    m = re.search(pattern, text)
    return m.group(1).strip() if m else None


def extract_block(text: str, start_marker: str, end_marker: str) -> str:
    """Extrae el fragmento de texto entre dos marcadores."""
    i = text.find(start_marker)
    j = text.find(end_marker, i + 1) if i != -1 else -1
    if i == -1:
        return ''
    return text[i: j if j != -1 else i + 2000]


def parse_checkboxes(block: str, keyword_map: dict) -> dict:
    """
    Dado un bloque de texto y un dict {label: keyword}, devuelve
    {label: True/False} según si el checkbox está marcado con [x].
    """
    result = {}
    for label, keyword in keyword_map.items():
        m = re.search(
            rf'- \[(x| )\][^\n]*{re.escape(keyword)}',
            block,
            re.IGNORECASE,
        )
        result[label] = bool(m and m.group(1).strip() == 'x')
    return result


# ── Main parser ───────────────────────────────────────────────────────────────

def parse_file(filepath: Path) -> dict:
    text = filepath.read_text(encoding='utf-8')
    row = {'file': filepath.name}

    # ── Ítems Likert ──────────────────────────────────────────────────────────
    for line in text.splitlines():
        result = parse_likert_row(line)
        if result:
            qid, score = result
            row[qid] = score

    # ── Perfil ────────────────────────────────────────────────────────────────
    exp_raw = parse_bold_answer(text, 'P0.1')
    row['experiencia_raw'] = exp_raw
    row['experiencia'] = P01_MAP.get((exp_raw or '').lower(), None)

    games_raw = parse_bold_answer(text, 'P0.3')
    row['juegos'] = [g.strip() for g in games_raw.split(',')] if games_raw else []

    tech_raw = parse_bold_answer(text, 'P0.4')
    row['perfil_tecnico_raw'] = tech_raw

    # ── P4.2 / P4.3 ──────────────────────────────────────────────────────────
    for qid in ('P4.2', 'P4.3'):
        raw = parse_bold_answer(text, qid)
        row[f'{qid}_raw'] = raw
        row[qid] = COMPARISON_MAP.get((raw or '').lower(), None)

    # ── P5.1 — Problemas ──────────────────────────────────────────────────────
    p51_block = extract_block(text, '**P5.1**', '**P5.2**')
    row['P5.1'] = parse_checkboxes(p51_block, {
        'Tardó demasiado':          'tardó demasiado',
        'No entendió la pregunta':  'no entendió',
        'Resp. incompleta':         'correcta pero incompleta',
        'Resp. incorrecta':         'incorrecta o contradijo',
        'Sin info (había):':        'no tener información cuando sí',
        'No supe expresarme':       'hacerme entender',
        'Sin problemas':            'ningún problema',
    })

    # ── P5.2 — Mejoras ────────────────────────────────────────────────────────
    p52_block = extract_block(text, '**P5.2**', '**P5.3**')
    row['P5.2'] = parse_checkboxes(p52_block, {
        'Más reglamentos':          'más reglamentos',
        'Trasfondo/lore':           'trasfondo',
        'Resps. más cortas':        'más cortas',
        'Resps. más detalladas':    'más detalladas',
        'Historial de chat':        'historial',
        'Acceso web/app':           'acceso web',
        'Multimodal (voz/img)':     'multimodal',
        'Búsqueda keywords':        'búsqueda por palabras',
        'Otra (modo torneo)':       'otra:',
    })

    # ── P6.1 — Puntuación global ──────────────────────────────────────────────
    p61_raw = parse_bold_answer(text, 'P6.1')
    m = re.search(r'(\d+)', p61_raw or '')
    row['P6.1'] = int(m.group(1)) if m else None

    # ── P6.2 / P6.3 ──────────────────────────────────────────────────────────
    row['P6.2_raw'] = parse_bold_answer(text, 'P6.2')
    row['P6.3_raw'] = parse_bold_answer(text, 'P6.3')

    return row


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    base = Path(__file__).parent
    files = sorted(base.glob('uat_respuesta_*.md'))
    if not files:
        print('ERROR: No se encontraron ficheros uat_respuesta_*.md')
        return

    records = [parse_file(f) for f in files]

    # ── Guardar JSON ──────────────────────────────────────────────────────────
    out = base / 'uat_data.json'
    out.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'✓ {len(records)} encuestas → {out}')

    # ── Resumen rápido ────────────────────────────────────────────────────────
    print('\n── Medias Likert ────────────────────────────────')
    all_items = [q for items in LIKERT_BLOCKS.values() for q in items]
    for block, items in LIKERT_BLOCKS.items():
        scores_block = [records[i][q] for i in range(len(records)) for q in items
                        if records[i].get(q) is not None]
        print(f'  {block}: media={statistics.mean(scores_block):.2f}  '
              f'σ={statistics.pstdev(scores_block):.2f}')
    for qid in all_items:
        vals = [r[qid] for r in records if r.get(qid) is not None]
        if vals:
            print(f'    {qid}: {vals}  → {statistics.mean(vals):.2f}')

    p61_vals = [r['P6.1'] for r in records if r.get('P6.1')]
    print(f'\n── P6.1 global: media={statistics.mean(p61_vals):.1f}/10')
    print(f'── P6.2: {[r["P6.2_raw"] for r in records]}')
    print(f'── P6.3: {[r["P6.3_raw"] for r in records]}')


if __name__ == '__main__':
    main()
