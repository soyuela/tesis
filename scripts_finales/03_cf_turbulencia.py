"""
Coeficiente de fricción Cf vs Reynolds
4 modelos de turbulencia CFD + línea ITTC-1957
Formato estandarizado tesis: 31/20/20pt, figsize=(12, 8)
"""

import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = './graficos_pdf'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generar():
    # k-omega (7 puntos visibles)
    Re_k_omega = np.array([6.4e5, 1.28e6, 1.92e6, 2.56e6, 5.13e6, 1.54e7, 2.05e7])
    cf_k_omega = np.array([0.00509, 0.00464, 0.00472, 0.00527, 0.00366, 0.00328, 0.00324])
    
    # k-omega SST (7 puntos)
    Re_k_omega_sst = np.array([6.4e5, 1.28e6, 1.92e6, 2.56e6, 5.13e6, 1.03e7, 2.05e7])
    cf_k_omega_sst = np.array([0.00399, 0.00388, 0.00401, 0.00429, 0.00329, 0.00284, 0.00255])
    
    # k-epsilon (10 puntos)
    Re_k_epsilon = np.array([6.4e5, 1.28e6, 1.92e6, 2.56e6, 1.03e7, 1.54e7,
                             2.05e7, 5.13e7, 1.28e8, 1.79e8])
    cf_k_epsilon = np.array([0.00870, 0.00724, 0.00640, 0.00578, 0.00330, 0.00294,
                             0.00286, 0.00244, 0.00224, 0.00222])
    
    # k-epsilon realizable (11 puntos)
    Re_k_epsilon_r = np.array([6.4e5, 1.28e6, 1.92e6, 2.56e6, 5.13e6, 1.03e7,
                               1.54e7, 2.05e7, 5.13e7, 1.28e8, 1.79e8])
    cf_k_epsilon_r = np.array([0.00690, 0.00608, 0.00546, 0.00500, 0.00395, 0.00292,
                               0.00271, 0.00261, 0.00234, 0.00213, 0.00203])
    
    # ITTC-1957: Cf = 0.075 / (log10(Re) - 2)^2
    Re_ittc = np.logspace(np.log10(6.4e5), np.log10(1.79e8), 200)
    cf_ittc = 0.075 / (np.log10(Re_ittc) - 2)**2
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.plot(Re_k_omega, cf_k_omega, 'o--', color='#1f77b4', linewidth=2.5, markersize=10,
            label=r'$k-\omega$',            markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    ax.plot(Re_k_omega_sst, cf_k_omega_sst, 'o--', color='#ff7f0e', linewidth=2.5, markersize=10,
            label=r'$k-\omega$ SST',        markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    ax.plot(Re_k_epsilon, cf_k_epsilon, 'o--', color='#2ca02c', linewidth=2.5, markersize=10,
            label=r'$k-\varepsilon$',       markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    ax.plot(Re_k_epsilon_r, cf_k_epsilon_r, 'o--', color='#d62728', linewidth=2.5, markersize=10,
            label=r'$k-\varepsilon$ realizable', markeredgecolor='black', markeredgewidth=0.8, zorder=3)
    ax.plot(Re_ittc, cf_ittc, '-', color='black', linewidth=2.5, label='ITTC', zorder=4)
    
    ax.set_xscale('log')
    ax.set_xlabel('Re', fontsize=31)
    ax.set_ylabel(r'$C_F$', fontsize=31)
    ax.set_xlim(5e5, 2.5e8)
    ax.set_ylim(0.0018, 0.0092)
    
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    
    for side in ('top', 'right', 'bottom', 'left'):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(1.5)
    
    ax.tick_params(labelsize=20)
    ax.legend(fontsize=20, loc='upper right', framealpha=0.95)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/cf_turbulencia.pdf', format='pdf',
                bbox_inches='tight', pad_inches=0.1)
    plt.savefig(f'{OUTPUT_DIR}/cf_turbulencia.png', format='png',
                bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()
    print("✓ cf_turbulencia.pdf/png")


if __name__ == "__main__":
    generar()
