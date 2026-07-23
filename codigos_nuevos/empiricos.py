"""
Valores de (1+k) para el P1 en función de Rn
CFD DB, EFD y correlaciones empíricas de la literatura
FORMATO ESTANDARIZADO (mismo que el .py original de la tesis):
- Títulos ejes: 31pt
- Números ejes: 20pt
- Leyenda: 20pt
- figsize=(12, 8)
"""

import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = './graficos_pdf'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generar_empiricos():
    # TPA CFD 195 (excluyendo últimos 2 puntos)
    Re_CFD = np.array([6.40e5, 1.02e6, 1.28e6, 1.54e6, 1.81e6, 1.92e6, 2.31e6,
                       2.56e6, 2.90e6, 3.62e6, 4.35e6, 5.43e6, 6.52e6, 5.12e6,
                       7.25e6, 8.20e6, 1.02e7, 1.23e7, 1.54e7, 1.84e7, 2.05e7,
                       5.73e7, 9.17e7, 1.15e8, 1.37e8, 1.72e8])
    
    k_CFD = np.array([1.179, 1.251, 1.32, 1.378, 1.399, 1.47, 1.598, 1.637,
                      1.622, 1.596, 1.513, 1.465, 1.465, 1.489, 1.473, 1.484,
                      1.501, 1.522, 1.528, 1.548, 1.554, 1.633, 1.69, 1.713,
                      1.714, 1.736])
    
    Re_range = np.array([6.40e5, 1.72e8])
    
    # Colores mate
    tgreen  = (0.1, 0.5, 0.1)
    tblue   = (0.1, 0.1, 0.5)
    tred    = (0.8, 0.1, 0.1)
    tpurple = (0.5, 0.1, 0.5)
    torange = (0.9, 0.5, 0.1)
    tyellow = (0.9, 0.9, 0.1)
    
    # =========================================================================
    # PLOT con formato estandarizado
    # =========================================================================
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Scatter CFD - marcadores grandes (s=150 como el estándar)
    ax.scatter(Re_CFD, k_CFD, marker='o', color=tgreen,
               edgecolor='black', linewidth=0.8, s=150, zorder=3,
               label='CFD - DB P1 LabHiNO')
    
    # Correlaciones empíricas - líneas gruesas, marcadores grandes
    ax.plot(Re_range, [1.66, 1.66], 'o-', color=tred,
            markerfacecolor=tred, markeredgecolor='black', markeredgewidth=0.8,
            linewidth=2, markersize=12, label='Watanabe', zorder=2)
    
    ax.plot(Re_range, [1.545, 1.545], 'o-', color=tblue,
            markerfacecolor=tblue, markeredgecolor='black', markeredgewidth=0.8,
            linewidth=2, markersize=12, label='Conn and Ferguson', zorder=2)
    
    ax.plot(Re_range, [1.534, 1.534], 'o-', color=tpurple,
            markerfacecolor=tpurple, markeredgecolor='black', markeredgewidth=0.8,
            linewidth=2, markersize=12, label='Grigson', zorder=2)
    
    ax.plot(Re_range, [1.457, 1.457], 'o-', color=torange,
            markerfacecolor=torange, markeredgecolor='black', markeredgewidth=0.8,
            linewidth=2, markersize=12, label='Wright', zorder=2)
    
    ax.plot(Re_range, [1.616, 1.616], 'o-', color=tyellow,
            markerfacecolor=tyellow, markeredgecolor='black', markeredgewidth=0.8,
            linewidth=2, markersize=12, label='Couser', zorder=2)
    
    ax.plot(Re_range, [1.19, 1.19], 'o-', color=tgreen,
            markerfacecolor=tgreen, markeredgecolor='black', markeredgewidth=0.8,
            linewidth=2, markersize=12, label='EFD - LabHiNO', zorder=2)
    
    # =========================================================================
    # FORMATO ESTANDARIZADO
    # =========================================================================
    ax.set_xscale('log')
    
    ax.set_xlabel('Rn', fontsize=31)
    ax.set_ylabel('1+k', fontsize=31)
    
    # Grid
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    
    # Límites
    ax.set_xlim(5e5, 2.5e8)
    ax.set_ylim(1.10, 1.85)
    
    # Bordes: los 4 lados con linewidth=1.5
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['top'].set_linewidth(1.5)
    ax.spines['right'].set_linewidth(1.5)
    
    # Ticks a 20pt
    ax.tick_params(labelsize=20)
    
    # Leyenda a 20pt, abajo con 3 columnas
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              ncol=3, fontsize=20, framealpha=0.95)
    
    plt.tight_layout()
    
    plt.savefig(f'{OUTPUT_DIR}/empiricos.pdf',
                format='pdf', bbox_inches='tight', pad_inches=0.1)
    plt.savefig(f'{OUTPUT_DIR}/empiricos.png',
                format='png', bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()
    print("✓ empiricos.pdf")
    print("✓ empiricos.png")


if __name__ == "__main__":
    print("=" * 70)
    print("GENERANDO empíricos con formato estandarizado (31/20/20pt)")
    print("=" * 70)
    generar_empiricos()
    print("=" * 70)
