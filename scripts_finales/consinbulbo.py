"""
═══════════════════════════════════════════════════════════════════════════════
COMPARACIÓN CON BULBO / SIN BULBO (Ctrl+Z) — CT, CV, CW, (1+k)
Calados 0.165 m y 0.195 m
Formato estandarizado (igual a generar_todos_los_graficos.py)
═══════════════════════════════════════════════════════════════════════════════

Los valores numéricos de este script fueron extraídos directamente de los
objetos vectoriales (paths de los marcadores) de los PDF originales
(Ct/Cv/Cw/k-consinbulbo-165/195.pdf), calibrando la posición de cada marcador
contra las líneas de grilla de los ejes. Por eso son más precisos que una
lectura visual del gráfico.

PARÁMETROS ESTANDARIZADOS:
- Títulos de ejes: 31pt
- Números de ejes: 20pt
- Leyenda: 20pt
- Salida: PDF vectorial

Uso:
    python generar_graficos_bulbo_CT_CV_CW_k.py

Requisitos:
    pip install numpy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Directorio de salida
OUTPUT_DIR = './graficos_pdf'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Colores estandarizados (coinciden con los PDF originales)
COLOR_SIN_BULBO = '#d62728'   # rojo (Ctrl+Z, sin bulbo) - marcador hueco
COLOR_CON_BULBO = '#1f77b4'   # azul (con bulbo) - marcador relleno


# ============================================================================
# DATOS EXTRAÍDOS DE LOS PDF ORIGINALES
# ============================================================================

Fn_full = [0.10, 0.16, 0.20, 0.24, 0.30, 0.36, 0.40]
Fn_cv   = [0.16, 0.20, 0.24, 0.30, 0.36, 0.40]   # Cv no tiene punto en Fn=0.10

DATA = {
    'CT': {
        '165': {
            'Fn': Fn_full,
            'sin_bulbo': [0.007562, 0.006762, 0.007112, 0.007212, 0.011962, 0.014262, 0.016812],
            'con_bulbo': [0.007062, 0.006262, 0.007062, 0.007912, 0.009962, 0.012562, 0.014162],
        },
        '195': {
            'Fn': Fn_full,
            'sin_bulbo': [0.006944, 0.006094, 0.007344, 0.006544, 0.010144, 0.012894, 0.015494],
            'con_bulbo': [0.006444, 0.006244, 0.006644, 0.007144, 0.009194, 0.013044, 0.015044],
        },
    },
    'CV': {
        '165': {
            'Fn': Fn_cv,
            'sin_bulbo': [0.005495, 0.005245, 0.005045, 0.004825, 0.004645, 0.004545],
            'con_bulbo': [0.005575, 0.005325, 0.005125, 0.004875, 0.004725, 0.004625],
        },
        '195': {
            'Fn': Fn_cv,
            'sin_bulbo': [0.005594, 0.005324, 0.005124, 0.004904, 0.004734, 0.004634],
            'con_bulbo': [0.005604, 0.005344, 0.005144, 0.004924, 0.004754, 0.004654],
        },
    },
    'CW': {
        '165': {
            'Fn': Fn_full,
            'sin_bulbo': [0.001497, 0.001377, 0.001877, 0.002177, 0.007177, 0.009627, 0.012277],
            'con_bulbo': [0.000927, 0.000727, 0.001777, 0.002827, 0.005077, 0.007877, 0.009577],
        },
        '195': {
            'Fn': Fn_full,
            'sin_bulbo': [0.000762, 0.000612, 0.002012, 0.001462, 0.005262, 0.008162, 0.010412],
            'con_bulbo': [0.000312, 0.000712, 0.001312, 0.002012, 0.004312, 0.008312, 0.010912],
        },
    },
    'K': {
        '165': {
            'Fn': Fn_full,
            'sin_bulbo': [0.787488, 0.919452, 1.015012, 1.133325, 1.358574, 1.563346, 1.697586],
            'con_bulbo': [0.867121, 0.999086, 1.121949, 1.260739, 1.511015, 1.777219, 1.715787],
        },
        '195': {
            'Fn': Fn_full,
            'sin_bulbo': [0.685064, 0.834133, 1.025793, 1.193115, 1.469958, 1.725504, 1.898911],
            'con_bulbo': [0.730697, 0.864555, 1.034920, 1.226580, 1.512549, 1.825898, 1.947587],
        },
    },
}

# Etiquetas de eje Y y nombre de archivo por magnitud
AXIS_LABELS = {
    'CT': '$C_T$',
    'CV': '$C_V$',
    'CW': '$C_W$',
    'K': '$(1+k)$',
}

FILE_TAGS = {
    'CT': 'Ct',
    'CV': 'Cv',
    'CW': 'Cw',
    'K': 'k',
}


# ============================================================================
# FUNCIÓN GENERAL DE GRAFICADO
# ============================================================================

def generar_grafico_bulbo(magnitud, calado):
    """
    Genera el gráfico de comparación con bulbo / sin bulbo para una magnitud
    (CT, CV, CW o K) y un calado (165 o 195).
    """
    d = DATA[magnitud][calado]
    Fn = np.array(d['Fn'])
    sin_bulbo = np.array(d['sin_bulbo'])
    con_bulbo = np.array(d['con_bulbo'])

    fig, ax = plt.subplots(figsize=(12, 8))

    # Ctrl+Z (sin bulbo) - marcador hueco, línea roja punteada
    ax.plot(Fn, sin_bulbo, linestyle='--', color=COLOR_SIN_BULBO, linewidth=1.5, zorder=2)
    ax.scatter(Fn, sin_bulbo, s=150, facecolors='none', edgecolors=COLOR_SIN_BULBO,
               linewidth=2, marker='o', label='Ctrl+Z (sin bulbo)', zorder=3)

    # Con bulbo - marcador relleno, línea azul punteada
    ax.plot(Fn, con_bulbo, linestyle='--', color=COLOR_CON_BULBO, linewidth=1.5, zorder=2)
    ax.scatter(Fn, con_bulbo, s=150, facecolors=COLOR_CON_BULBO, edgecolors=COLOR_CON_BULBO,
               linewidth=2, marker='o', label='Con bulbo', zorder=3)

    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    ax.set_xlabel('$Fr$', fontsize=31)
    ax.set_ylabel(AXIS_LABELS[magnitud], fontsize=31)

    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)

    ax.tick_params(labelsize=20)
    ax.legend(fontsize=20, loc='upper left', framealpha=0.95)

    plt.tight_layout()
    fname = f"{FILE_TAGS[magnitud]}-consinbulbo-{calado}.pdf"
    plt.savefig(f'{OUTPUT_DIR}/{fname}', format='pdf', bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(f"✓ {fname}")


# ============================================================================
# EJECUTAR TODOS
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("GENERANDO GRÁFICOS CON BULBO / SIN BULBO (CT, CV, CW, 1+k)")
    print(f"Salida en: {OUTPUT_DIR}/")
    print("=" * 70)
    print()

    for magnitud in ['CT', 'CV', 'CW', 'K']:
        for calado in ['165', '195']:
            generar_grafico_bulbo(magnitud, calado)

    print()
    print("=" * 70)
    print(f"✓ COMPLETADO. Archivos en: {OUTPUT_DIR}/")
    print("=" * 70)
