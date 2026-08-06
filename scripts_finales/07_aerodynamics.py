"""
Factores de forma (1+k) para cuerpos de revolución en función de L/B
Correlaciones empíricas + comparación CFD DB (P1, P2, P3, KCS)
Formato estandarizado tesis: 31/20/20pt, figsize=(12, 8)
Convertido desde aerodynamics.m
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import os

OUTPUT_DIR = './graficos_pdf'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generar():
    # =========================================================================
    # DATOS
    # =========================================================================
    L_B        = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
    Hoerner    = np.array([2.405, 1.548, 1.297, 1.190, 1.134, 1.101,
                           1.080, 1.065, 1.054, 1.046, 1.040, 1.035])
    Raymer_new = np.array([2.673, 1.870, 1.535, 1.360, 1.255, 1.187,
                           1.141, 1.108, 1.083, 1.065, 1.050, 1.039])
    Torenbeek  = np.array([2.253, 1.564, 1.334, 1.227, 1.167, 1.130,
                           1.105, 1.087, 1.073, 1.063, 1.055, 1.049])
    Shevell    = np.array([1.856, 1.571, 1.394, 1.288, 1.225, 1.183,
                           1.148, 1.116, 1.088, 1.075, 1.095, 1.174])
    Roskam     = np.array([8.505, 3.230, 1.948, 1.493, 1.293, 1.192,
                           1.137, 1.105, 1.085, 1.073, 1.065, 1.060])
    
    # Puntos destacados
    x_p1, y_p1   = 3.53, 1.73    # P1 (TPA)
    x_kcs, y_kcs = 7.14, 1.12    # KCS
    x_p2, y_p2   = 3.23, 2.60    # P2 (Contessi)
    x_p3, y_p3   = 2.85, 2.70    # P3 (JPA)
    
    # Colores mate (idénticos al script MATLAB original)
    tgreen  = (0.1, 0.5, 0.1)
    tblue   = (0.1, 0.1, 0.5)
    tred    = (0.8, 0.1, 0.1)
    tpurple = (0.5, 0.1, 0.5)
    torange = (0.9, 0.5, 0.1)
    tyellow = (0.9, 0.9, 0.1)
    tbrown  = (0.6, 0.4, 0.2)
    tgray   = (0.3, 0.3, 0.3)
    
    # Interpolación spline
    xq = np.linspace(L_B.min(), L_B.max(), 200)
    Hoerner_spline   = CubicSpline(L_B, Hoerner)(xq)
    Raymer_spline    = CubicSpline(L_B, Raymer_new)(xq)
    Torenbeek_spline = CubicSpline(L_B, Torenbeek)(xq)
    Shevell_spline   = CubicSpline(L_B, Shevell)(xq)
    Roskam_spline    = CubicSpline(L_B, Roskam)(xq)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Curvas empíricas
    ax.plot(xq, Hoerner_spline,   '-', color=tblue,   linewidth=2, label='Hoerner',    zorder=2)
    ax.plot(xq, Raymer_spline,    '-', color=tred,    linewidth=2, label='Raymer new', zorder=2)
    ax.plot(xq, Torenbeek_spline, '-', color=tpurple, linewidth=2, label='Torenbeek',  zorder=2)
    ax.plot(xq, Shevell_spline,   '-', color=torange, linewidth=2, label='Shevell',    zorder=2)
    ax.plot(xq, Roskam_spline,    '-', color=tyellow, linewidth=2, label='Roskam',     zorder=2)
    
    # Líneas guía dashed (antes que scatter para que queden atrás)
    ax.plot([0, x_p1],  [y_p1,  y_p1],  '--', color=tgreen, linewidth=1.5, zorder=3)
    ax.plot([x_p1, x_p1], [1, y_p1],    '--', color=tgreen, linewidth=1.5, zorder=3)
    ax.plot([0, x_kcs], [y_kcs, y_kcs], '--', color='black', linewidth=1.5, zorder=3)
    ax.plot([x_kcs, x_kcs], [1, y_kcs], '--', color='black', linewidth=1.5, zorder=3)
    ax.plot([0, x_p2],  [y_p2,  y_p2],  '--', color=tbrown, linewidth=1.5, zorder=3)
    ax.plot([x_p2, x_p2], [1, y_p2],    '--', color=tbrown, linewidth=1.5, zorder=3)
    ax.plot([0, x_p3],  [y_p3,  y_p3],  '--', color=tgray, linewidth=1.5, zorder=3)
    ax.plot([x_p3, x_p3], [1, y_p3],    '--', color=tgray, linewidth=1.5, zorder=3)
    
    # Puntos destacados (scatter)
    ax.scatter(x_kcs, y_kcs, s=150, color='black', edgecolor='black',
               linewidth=0.8, label='KCS', zorder=5)
    ax.scatter(x_p1,  y_p1,  s=150, color=tgreen,  edgecolor='black',
               linewidth=0.8, label='P1',  zorder=5)
    ax.scatter(x_p2,  y_p2,  s=150, color=tbrown,  edgecolor='black',
               linewidth=0.8, label='P2',  zorder=5)
    ax.scatter(x_p3,  y_p3,  s=150, color=tred,    edgecolor='black',
               linewidth=0.8, label='P3',  zorder=5)
    
    ax.set_xlim(0, 14)
    ax.set_ylim(1, 2.75)
    ax.set_xlabel('L/B', fontsize=31)
    ax.set_ylabel('1+k', fontsize=31)
    
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    
    for side in ('top', 'right', 'bottom', 'left'):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(1.5)
    
    ax.tick_params(labelsize=20)
    ax.legend(loc='upper right', fontsize=20, framealpha=0.95, ncol=2)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/aerodynamics.pdf', format='pdf',
                bbox_inches='tight', pad_inches=0.1)
    plt.savefig(f'{OUTPUT_DIR}/aerodynamics.png', format='png',
                bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()
    print("✓ aerodynamics.pdf/png")


if __name__ == "__main__":
    generar()
