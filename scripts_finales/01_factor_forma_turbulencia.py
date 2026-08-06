"""
Factor de forma (1+k) vs Reynolds
Comparación de 4 modelos de turbulencia CFD + valor experimental
Formato estandarizado tesis: 31/20/20pt, figsize=(12, 8)
"""

import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = './graficos_pdf'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generar():
    # Serie común de Reynolds (11 puntos)
    Re = np.array([6.4e5, 1.28e6, 1.92e6, 2.56e6, 5.13e6, 1.03e7,
                   1.54e7, 2.05e7, 5.13e7, 1.28e8, 1.79e8])
    
    k_omega       = np.array([1.54, 1.62, 1.76, 2.02, 1.60, 1.68, 1.78, 1.83, 1.72, 1.79, 1.90])
    k_omega_sst   = np.array([1.18, 1.32, 1.46, 1.63, 1.48, 1.49, 1.52, 1.55, 1.65, 1.65, 1.73])
    k_epsilon     = np.array([2.36, 2.29, 2.23, 1.83, 1.71, 1.62, 1.64, 1.67, 1.72, 1.77, 1.87])
    k_epsilon_r   = np.array([1.93, 1.93, 1.89, 1.83, 1.71, 1.51, 1.52, 1.57, 1.65, 1.70, 1.76])
    
    Re_exp = np.array([6.4e5, 1.79e8])
    k_exp  = np.array([1.18, 1.18])
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.plot(Re, k_omega,     'o--', color='#1f77b4', linewidth=2.5, markersize=10,
            label=r'$k-\omega$',            markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    ax.plot(Re, k_omega_sst, 'o--', color='#ff7f0e', linewidth=2.5, markersize=10,
            label=r'$k-\omega$ SST',        markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    ax.plot(Re, k_epsilon,   'o--', color='#2ca02c', linewidth=2.5, markersize=10,
            label=r'$k-\varepsilon$',       markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    ax.plot(Re, k_epsilon_r, 'o--', color='#d62728', linewidth=2.5, markersize=10,
            label=r'$k-\varepsilon$ realizable', markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    ax.plot(Re_exp, k_exp,   'o-',  color='black',   linewidth=2.5, markersize=10,
            label='Experimental',           markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    
    ax.set_xscale('log')
    ax.set_xlabel('Re', fontsize=31)
    ax.set_ylabel('1+k', fontsize=31)
    ax.set_xlim(5e5, 2.5e8)
    ax.set_ylim(1.1, 2.45)
    
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    
    for side in ('top', 'right', 'bottom', 'left'):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(1.5)
    
    ax.tick_params(labelsize=20)
    ax.legend(fontsize=20, loc='upper right', framealpha=0.95)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/factor_forma_turbulencia.pdf', format='pdf',
                bbox_inches='tight', pad_inches=0.1)
    plt.savefig(f'{OUTPUT_DIR}/factor_forma_turbulencia.png', format='png',
                bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()
    print("✓ factor_forma_turbulencia.pdf/png")


if __name__ == "__main__":
    generar()
