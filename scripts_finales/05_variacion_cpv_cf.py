"""
Variación de Cpv y Cf por modelo de turbulencia (bar chart)
Colores: naranja=Cpv, azul=Cf
Hatches: //=k-omega, xx=k-epsilon, ..=realizable
Formato estandarizado tesis: 31/20/20pt
figsize aumentada a (16, 9) para acomodar 11 grupos de barras + ticks 20pt
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

OUTPUT_DIR = './graficos_pdf'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generar():
    Re_labels = ['6.4e5', '1.28e6', '1.92e6', '2.56e6', '5.13e6', '1.03e7',
                 '1.54e7', '2.05e7', '5.13e7', '1.28e8', '1.79e8']
    n_groups = len(Re_labels)
    
    # k-omega
    cpv_ko  = np.array([11.6, 9.2, 7.8, 7.6, 0.0, 0.4, 2.4, 1.5, 1.3, 2.6, 0.0])
    cf_ko   = np.array([30.2, 22.1, 19.4, 23.2, 7.2, 11.3, 15.7, 17.3, 2.6, 8.5, 9.4])
    # k-epsilon
    cpv_ke  = np.array([21.9, 15.9, 11.3, 7.6, 1.5, 0.0, 1.1, 1.1, 1.9, 2.8, 0.0])
    cf_ke   = np.array([99.8, 73.5, 51.2, 31.0, 15.1, 7.4, 6.7, 7.4, 3.2, 6.7, 7.8])
    # realizable
    cpv_re  = np.array([15.1, 8.5, 3.7, 0.0, 1.5, 0.0, 0.0, 0.0, 0.0, 1.9, 0.0])
    cf_re   = np.array([63.0, 46.2, 27.8, 11.3, 14.6, 0.0, 0.0, 0.6, 1.1, 2.8, 1.1])
    
    fig, ax = plt.subplots(figsize=(16, 9))
    
    color_cpv = '#ff7f0e'
    color_cf  = '#1f77b4'
    
    bar_width = 0.28
    x = np.arange(n_groups)
    x_ko = x - bar_width
    x_ke = x
    x_re = x + bar_width
    
    # Cada barra: Cf (más alto) primero, luego Cpv encima (superpuesto)
    ax.bar(x_ko, cf_ko, bar_width, color=color_cf, hatch='//', edgecolor='black', linewidth=0.8, zorder=2)
    ax.bar(x_ko, cpv_ko, bar_width, color=color_cpv, hatch='//', edgecolor='black', linewidth=0.8, zorder=3)
    ax.bar(x_ke, cf_ke, bar_width, color=color_cf, hatch='xx', edgecolor='black', linewidth=0.8, zorder=2)
    ax.bar(x_ke, cpv_ke, bar_width, color=color_cpv, hatch='xx', edgecolor='black', linewidth=0.8, zorder=3)
    ax.bar(x_re, cf_re, bar_width, color=color_cf, hatch='..', edgecolor='black', linewidth=0.8, zorder=2)
    ax.bar(x_re, cpv_re, bar_width, color=color_cpv, hatch='..', edgecolor='black', linewidth=0.8, zorder=3)
    
    # Leyenda compuesta
    legend_elements = [
        mpatches.Patch(facecolor=color_cpv, edgecolor='black', label='Cpv'),
        mpatches.Patch(facecolor=color_cf,  edgecolor='black', label='Cf'),
        mpatches.Patch(facecolor='white', edgecolor='black', hatch='//', label=r'$k-\omega$'),
        mpatches.Patch(facecolor='white', edgecolor='black', hatch='xx', label=r'$k-\varepsilon$'),
        mpatches.Patch(facecolor='white', edgecolor='black', hatch='..', label='realizable'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=20, framealpha=0.95)
    
    ax.set_xticks(x)
    ax.set_xticklabels(Re_labels, rotation=45, ha='right', fontsize=20)
    
    ax.set_xlabel('Re', fontsize=31)
    ax.set_ylabel('Porcentaje [%]', fontsize=31)
    
    ax.set_ylim(0, 105)
    
    ax.grid(True, axis='y', linestyle='--', color='gray', alpha=0.3, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    
    for side in ('top', 'right', 'bottom', 'left'):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(1.5)
    
    ax.tick_params(axis='y', labelsize=20)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/variacion_cpv_cf.pdf', format='pdf',
                bbox_inches='tight', pad_inches=0.1)
    plt.savefig(f'{OUTPUT_DIR}/variacion_cpv_cf.png', format='png',
                bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()
    print("✓ variacion_cpv_cf.pdf/png")


if __name__ == "__main__":
    generar()
