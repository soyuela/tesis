"""
Coeficiente viscoso Cv vs Reynolds
4 modelos de turbulencia CFD
Formato estandarizado tesis: 31/20/20pt, figsize=(12, 8)
"""

import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = './graficos_pdf'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generar():
    Re = np.array([6.4e5, 1.28e6, 1.92e6, 2.56e6, 5.13e6, 1.03e7,
                   1.54e7, 2.05e7, 5.13e7, 1.28e8, 1.79e8])
    
    cv_k_omega     = np.array([0.00795, 0.00720, 0.00720, 0.00775, 0.00600, 0.00500,
                               0.00450, 0.00420, 0.00404, 0.00370, 0.00370])
    cv_k_omega_sst = np.array([0.00615, 0.00590, 0.00600, 0.00625, 0.00505, 0.00450,
                               0.00400, 0.00380, 0.00360, 0.00339, 0.00340])
    cv_k_epsilon   = np.array([0.01220, 0.01025, 0.00910, 0.00829, 0.00611, 0.00500,
                               0.00495, 0.00494, 0.00430, 0.00385, 0.00365])
    cv_k_epsilon_r = np.array([0.00995, 0.00860, 0.00775, 0.00710, 0.00550, 0.00450,
                               0.00431, 0.00420, 0.00375, 0.00355, 0.00340])
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.plot(Re, cv_k_omega,     'o--', color='#1f77b4', linewidth=2.5, markersize=10,
            label=r'$k-\omega$',            markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    ax.plot(Re, cv_k_omega_sst, 'o--', color='#ff7f0e', linewidth=2.5, markersize=10,
            label=r'$k-\omega$ SST',        markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    ax.plot(Re, cv_k_epsilon,   'o--', color='#2ca02c', linewidth=2.5, markersize=10,
            label=r'$k-\varepsilon$',       markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    ax.plot(Re, cv_k_epsilon_r, 'o--', color='#d62728', linewidth=2.5, markersize=10,
            label=r'$k-\varepsilon$ realizable', markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    
    ax.set_xscale('log')
    ax.set_xlabel('Re', fontsize=31)
    ax.set_ylabel(r'$C_V$', fontsize=31)
    ax.set_xlim(5e5, 2.5e8)
    ax.set_ylim(0.003, 0.0128)
    
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    
    for side in ('top', 'right', 'bottom', 'left'):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(1.5)
    
    ax.tick_params(labelsize=20)
    ax.legend(fontsize=20, loc='upper right', framealpha=0.95)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/cv_turbulencia.pdf', format='pdf',
                bbox_inches='tight', pad_inches=0.1)
    plt.savefig(f'{OUTPUT_DIR}/cv_turbulencia.png', format='png',
                bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()
    print("✓ cv_turbulencia.pdf/png")


if __name__ == "__main__":
    generar()
