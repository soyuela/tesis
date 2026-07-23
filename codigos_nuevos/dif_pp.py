"""
Variación de Cpv y Cf por modelo de turbulencia
Bar chart agrupado - 3 modelos × 11 Reynolds
Colores: naranja=Cpv, azul=Cf
Hatches: //=k-omega, xx=k-epsilon, ..=realizable
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

OUTPUT_DIR = './graficos_pdf'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generar_barras_turbulencia():
    # =========================================================================
    # DATOS extraídos por análisis pixel a pixel
    # =========================================================================
    Re_labels = ['6.4e5', '1.28e6', '1.92e6', '2.56e6', '5.13e6', '1.03e7',
                 '1.54e7', '2.05e7', '5.13e7', '1.28e8', '1.79e8']
    n_groups = len(Re_labels)
    
    # k-omega
    cpv_komega   = np.array([11.6, 9.2, 7.8, 7.6, 0.0, 0.4, 2.4, 1.5, 1.3, 2.6, 0.0])
    cf_komega    = np.array([30.2, 22.1, 19.4, 23.2, 7.2, 11.3, 15.7, 17.3, 2.6, 8.5, 9.4])
    
    # k-epsilon
    cpv_kepsilon = np.array([21.9, 15.9, 11.3, 7.6, 1.5, 0.0, 1.1, 1.1, 1.9, 2.8, 0.0])
    cf_kepsilon  = np.array([99.8, 73.5, 51.2, 31.0, 15.1, 7.4, 6.7, 7.4, 3.2, 6.7, 7.8])
    
    # realizable (k-epsilon realizable)
    cpv_real     = np.array([15.1, 8.5, 3.7, 0.0, 1.5, 0.0, 0.0, 0.0, 0.0, 1.9, 0.0])
    cf_real      = np.array([63.0, 46.2, 27.8, 11.3, 14.6, 0.0, 0.0, 0.6, 1.1, 2.8, 1.1])
    
    # =========================================================================
    # PLOT
    # =========================================================================
    fig, ax = plt.subplots(figsize=(14, 7))
    
    color_cpv = '#ff7f0e'   # naranja
    color_cf  = '#1f77b4'   # azul
    
    bar_width = 0.28
    x = np.arange(n_groups)
    
    # Posiciones: 3 barras por grupo, ligeramente desplazadas
    x_ko = x - bar_width
    x_ke = x
    x_re = x + bar_width
    
    # Cada barra: Cf primero (más alto), luego Cpv encima (más bajo, superpuesto)
    # k-omega: hatch //
    ax.bar(x_ko, cf_komega, bar_width, color=color_cf, hatch='//',
           edgecolor='black', linewidth=0.6, zorder=2)
    ax.bar(x_ko, cpv_komega, bar_width, color=color_cpv, hatch='//',
           edgecolor='black', linewidth=0.6, zorder=3)
    
    # k-epsilon: hatch xx
    ax.bar(x_ke, cf_kepsilon, bar_width, color=color_cf, hatch='xx',
           edgecolor='black', linewidth=0.6, zorder=2)
    ax.bar(x_ke, cpv_kepsilon, bar_width, color=color_cpv, hatch='xx',
           edgecolor='black', linewidth=0.6, zorder=3)
    
    # realizable: hatch ..
    ax.bar(x_re, cf_real, bar_width, color=color_cf, hatch='..',
           edgecolor='black', linewidth=0.6, zorder=2)
    ax.bar(x_re, cpv_real, bar_width, color=color_cpv, hatch='..',
           edgecolor='black', linewidth=0.6, zorder=3)
    
    # =========================================================================
    # LEYENDA compuesta: colores + hatches
    # =========================================================================
    legend_elements = [
        mpatches.Patch(facecolor=color_cpv, edgecolor='black', label='Cpv'),
        mpatches.Patch(facecolor=color_cf, edgecolor='black', label='Cf'),
        mpatches.Patch(facecolor='white', edgecolor='black', hatch='//', label='k-omega'),
        mpatches.Patch(facecolor='white', edgecolor='black', hatch='xx', label='k-epsilon'),
        mpatches.Patch(facecolor='white', edgecolor='black', hatch='..', label='realizable'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=11,
              framealpha=0.95, ncol=1)
    
    # =========================================================================
    # FORMATO
    # =========================================================================
    ax.set_xticks(x)
    ax.set_xticklabels(Re_labels, rotation=45, ha='right', fontsize=11)
    
    ax.set_xlabel('Rn', fontsize=31)
    ax.set_ylabel('Porcentaje [%]', fontsize=31)
    
    ax.set_ylim(0, 105)
    
    ax.grid(True, axis='y', linestyle='--', color='gray', alpha=0.3, linewidth=0.6)
    ax.set_axisbelow(True)
    
    for side in ('top', 'right', 'bottom', 'left'):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(1.0)
        ax.spines[side].set_color('black')
    
    ax.tick_params(axis='y', labelsize=11)
    
    plt.tight_layout()
    
    plt.savefig(f'{OUTPUT_DIR}/variacion_cpv_cf.pdf',
                format='pdf', bbox_inches='tight', pad_inches=0.1)
    plt.savefig(f'{OUTPUT_DIR}/variacion_cpv_cf.png',
                format='png', bbox_inches='tight', pad_inches=0.1, dpi=150)
    plt.close()
    print("✓ variacion_cpv_cf.pdf")
    print("✓ variacion_cpv_cf.png")


if __name__ == "__main__":
    print("=" * 70)
    print("GENERANDO: Variación de Cpv y Cf")
    print("=" * 70)
    generar_barras_turbulencia()
    print("=" * 70)
