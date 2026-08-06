"""
Coeficiente de presión viscosa CPV vs Reynolds
4 modelos de turbulencia CFD
Formato estandarizado tesis: 31/20/20pt, figsize=(12, 8)
"""

import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = './graficos_pdf'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generar():
    Re = np.array([6.4e5, 1.28e6, 1.92e6, 2.56e6, 5e6, 1.03e7,
                   1.54e7, 2.05e7, 5.13e7, 1.28e8, 1.79e8])
    
    cpv_k_omega     = np.array([0.00286, 0.00256, 0.00249, 0.00250, 0.00178, 0.00167,
                                0.00168, 0.00164, 0.00147, 0.00142, 0.00140])
    cpv_k_omega_sst = np.array([0.00212, 0.00199, 0.00199, 0.00201, 0.00174, 0.00162,
                                0.00156, 0.00155, 0.00139, 0.00129, 0.00130])
    cpv_k_epsilon   = np.array([0.00350, 0.00296, 0.00271, 0.00254, 0.00190, 0.00170,
                                0.00163, 0.00160, 0.00149, 0.00141, 0.00142])
    cpv_k_epsilon_r = np.array([0.00308, 0.00252, 0.00226, 0.00206, 0.00185, 0.00157,
                                0.00150, 0.00152, 0.00145, 0.00137, 0.00138])
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.plot(Re, cpv_k_omega,     'o--', color='#1f77b4', linewidth=2.5, markersize=10,
            label=r'$k-\omega$',            markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    ax.plot(Re, cpv_k_omega_sst, 'o--', color='#ff7f0e', linewidth=2.5, markersize=10,
            label=r'$k-\omega$ SST',        markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    ax.plot(Re, cpv_k_epsilon,   'o--', color='#2ca02c', linewidth=2.5, markersize=10,
            label=r'$k-\varepsilon$',       markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    ax.plot(Re, cpv_k_epsilon_r, 'o--', color='#d62728', linewidth=2.5, markersize=10,
            label=r'$k-\varepsilon$ realizable', markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    
    ax.set_xscale('log')
    ax.set_xlabel('Re', fontsize=31)
    ax.set_ylabel(r'$C_{PV}$', fontsize=31)
    ax.set_xlim(5e5, 2.5e8)
    ax.set_ylim(0.0012, 0.0037)
    
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    
    for side in ('top', 'right', 'bottom', 'left'):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(1.5)
    
    ax.tick_params(labelsize=20)
    ax.legend(fontsize=20, loc='upper right', framealpha=0.95)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/cpv_turbulencia.pdf', format='pdf',
                bbox_inches='tight', pad_inches=0.1)
    plt.savefig(f'{OUTPUT_DIR}/cpv_turbulencia.png', format='png',
                bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()
    print("✓ cpv_turbulencia.pdf/png")


if __name__ == "__main__":
    generar()
