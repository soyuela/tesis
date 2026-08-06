"""
═══════════════════════════════════════════════════════════════════════════════
CÓDIGO PARA GENERAR GRÁFICO ITTC vs NFL - FACTOR DE FORMA (1+k)
Formato estandarizado
═══════════════════════════════════════════════════════════════════════════════

PARÁMETROS ESTANDARIZADOS:
- Títulos de ejes: 31pt
- Números de ejes: 20pt
- Leyenda: 20pt
- Etiquetas adicionales: 18pt
- Salida: PDF vectorial
- Escala X: logarítmica

Uso:
    python generar_grafico_ittc_nfl.py

Requisitos:
    pip install numpy matplotlib scipy

═══════════════════════════════════════════════════════════════════════════════
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os

# Directorio de salida
OUTPUT_DIR = './graficos_pdf'
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================================
# DATOS EXTRAÍDOS DEL CÓDIGO MATLAB - FACTOR DE FORMA (1+k) vs REYNOLDS
# ============================================================================

# Escala 1:20
Re_20 = np.array([6.40E+05, 1.02E+06, 1.28E+06, 1.54E+06, 1.92E+06, 2.31E+06, 2.56E+06])
k_20_ittc = np.array([1.179, 1.251, 1.32, 1.378, 1.47, 1.598, 1.637])
k_20_nfl = np.array([1.352, 1.404, 1.468, 1.522, 1.611, 1.740, 1.775])

# Escala 1:10
Re_10 = np.array([1.81E+06, 2.90E+06, 3.62E+06, 4.35E+06, 5.43E+06, 6.52E+06, 7.25E+06])
k_10_ittc = np.array([1.399, 1.622, 1.57, 1.513, 1.465, 1.465, 1.473])
k_10_nfl = np.array([1.536, 1.752, 1.684, 1.615, 1.554, 1.546, 1.550])

# Escala 1:5
Re_5 = np.array([5.12E+06, 8.20E+06, 1.02E+07, 1.23E+07, 1.54E+07, 1.84E+07, 2.05E+07])
k_5_ittc = np.array([1.489, 1.484, 1.501, 1.522, 1.528, 1.548, 1.554])
k_5_nfl = np.array([1.581, 1.557, 1.566, 1.581, 1.580, 1.594, 1.597])

# Escala 1:1
Re_1 = np.array([5.73E+07, 9.17E+07, 1.15E+08, 1.37E+08, 1.72E+08])
k_1_ittc = np.array([1.654, 1.690, 1.713, 1.714, 1.727])
k_1_nfl = np.array([1.669, 1.694, 1.712, 1.708, 1.717])

# Líneas de Prohaska (horizontales)
Reynolds_Prohaska_ITTC57 = np.array([6.40E+05, 1.72E+08])
Prohaska_ITTC57 = np.array([1.19, 1.19])
Reynolds_Prohaska_NFL = np.array([6.40E+05, 1.72E+08])
Prohaska_NFL = np.array([1.335, 1.335])


# ============================================================================
# DEFINICIÓN DE COLORES MATE (según MATLAB original)
# ============================================================================

tgreen = np.array([0.1, 0.5, 0.1])      # verde mate
tblue = np.array([0.1, 0.1, 0.5])      # azul mate
tred = np.array([0.8, 0.1, 0.1])       # rojo mate
tpurple = np.array([0.5, 0.1, 0.5])    # morado mate
torange = np.array([0.9, 0.5, 0.1])    # naranja mate
tyellow = np.array([0.9, 0.9, 0.1])    # amarillo mate
tcyan = np.array([0.2, 0.6, 0.6])      # cian mate
tpink = np.array([0.6, 0.3, 0.6])      # rosado/morado claro mate


# ============================================================================
# FUNCIÓN PARA GENERAR GRÁFICO
# ============================================================================

def generar_ittc_nfl_comparacion():
    """
    Genera gráfico de comparación ITTC vs NFL para diferentes escalas
    con escala logarítmica en X
    """
    
    fig, ax = plt.subplots(figsize=(14, 9))
    
    # Scatter plots para cada escala y método
    # Formato: scatter(Re, k, color, label)
    
    # ITTC - diferentes escalas
    ax.scatter(Re_20, k_20_ittc, s=150, color=tblue, marker='o', 
               label='FV DB 1:20 - ITTC', zorder=3, edgecolors='black', linewidth=0.5)
    ax.scatter(Re_10, k_10_ittc, s=150, color=tgreen, marker='o',
               label='FV DB 1:10 - ITTC', zorder=3, edgecolors='black', linewidth=0.5)
    ax.scatter(Re_5, k_5_ittc, s=150, color=torange, marker='o',
               label='FV DB 1:5 - ITTC', zorder=3, edgecolors='black', linewidth=0.5)
    ax.scatter(Re_1, k_1_ittc, s=150, color=tcyan, marker='o',
               label='FV DB 1:1 - ITTC', zorder=3, edgecolors='black', linewidth=0.5)
    
    # NFL - diferentes escalas
    ax.scatter(Re_20, k_20_nfl, s=150, color=tred, marker='o',
               label='FV DB 1:20 - NFL', zorder=3, edgecolors='black', linewidth=0.5)
    ax.scatter(Re_10, k_10_nfl, s=150, color=tpurple, marker='o',
               label='FV DB 1:10 - NFL', zorder=3, edgecolors='black', linewidth=0.5)
    ax.scatter(Re_5, k_5_nfl, s=150, color=tyellow, marker='o',
               label='FV DB 1:5 - NFL', zorder=3, edgecolors='black', linewidth=0.5)
    ax.scatter(Re_1, k_1_nfl, s=150, color=tpink, marker='o',
               label='FV DB 1:1 - NFL', zorder=3, edgecolors='black', linewidth=0.5)
    
    # Líneas de Prohaska (horizontales)
    ax.plot(Reynolds_Prohaska_ITTC57, Prohaska_ITTC57, '--', color=tgreen, 
            linewidth=2.5, label='Prohaska - ITTC-57', zorder=2)
    ax.plot(Reynolds_Prohaska_NFL, Prohaska_NFL, '--', color=tpurple,
            linewidth=2.5, label='Prohaska - NFL', zorder=2)
    
    # Configuración de grid
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    
    # Escala logarítmica en X
    ax.set_xscale('log')
    
    # Etiquetas de ejes
    ax.set_xlabel('Re', fontsize=31)
    ax.set_ylabel('1+k', fontsize=31)
    
    # Límites de ejes
    ax.set_xlim(3e5, 3e8)
    ax.set_ylim(1.1, 1.8)
    
    # Configuración de spines
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    
    # Tamaño de números en ejes
    ax.tick_params(labelsize=20)
    
    # Leyenda con formato especial (3 columnas, debajo)
    ax.legend(fontsize=18, loc='upper center', framealpha=0.95, 
              ncol=3, bbox_to_anchor=(0.5, -0.12), columnspacing=1.2,
              handletextpad=0.5)
    
    # Ajustes de layout
    plt.tight_layout()
    
    # Guardar PDF
    plt.savefig(f'{OUTPUT_DIR}/ittc-nfl.pdf', format='pdf', bbox_inches='tight', 
                pad_inches=0.2, dpi=300)
    plt.close()
    print("✓ ittc-nfl.pdf")


# ============================================================================
# EJECUTAR
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("GENERANDO GRÁFICO ITTC vs NFL")
    print(f"Salida en: {OUTPUT_DIR}/")
    print("=" * 70)
    print()
    
    generar_ittc_nfl_comparacion()
    
    print()
    print("=" * 70)
    print(f"✓ COMPLETADO. Archivo en: {OUTPUT_DIR}/ittc-nfl.pdf")
    print("=" * 70)
