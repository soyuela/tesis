"""
Coeficiente de fricción CF vs Reynolds - Modelos de turbulencia
Datos extraídos por análisis pixel-a-pixel de la imagen original
Formato similar al gráfico 1+k
"""

import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = './graficos_pdf'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generar_cf_turbulencia():
    """
    Coeficiente de fricción CF vs Reynolds
    4 modelos de turbulencia CFD + línea ITTC-1957
    """
    
    # =========================================================================
    # DATOS EXTRAÍDOS DE LA IMAGEN
    # Serie común de Reynolds
    # =========================================================================
    
    # k-ω (7 puntos - los de alta Re quedan ocultos por otras curvas)
    Re_k_omega = np.array([6.4e5, 1.28e6, 1.92e6, 2.56e6, 5e6, 1.03e7, 1.54e7,
                             2.05e7, 5.13e7, 1.28e8, 1.79e8])

    cf_k_omega = np.array([0.00509, 0.00464, 0.00472, 0.00527, 0.00366, 0.00330, 0.00328, 0.00324, 0.00244, 0.00225, 0.00223])
    
    # k-ω SST (7 puntos)
    Re_k_omega_sst = np.array([6.4e5, 1.28e6, 1.92e6, 2.56e6, 5e6, 1.03e7, 1.54e7,
                             2.05e7, 5.13e7, 1.28e8, 1.79e8])

    cf_k_omega_sst = np.array([0.00399, 0.00388, 0.00401, 0.00429, 0.00329, 0.00284, 0.00271, 0.00255, 0.00240, 0.00215, 0.00205])
    
    # k-ε (10 puntos - falta en Re=5.13e6)
    Re_k_epsilon = np.array([6.4e5, 1.28e6, 1.92e6, 2.56e6, 5e6, 1.03e7, 1.54e7,
                             2.05e7, 5.13e7, 1.28e8, 1.79e8])
    cf_k_epsilon = np.array([0.00870, 0.00724, 0.00640, 0.00578, 0.00395, 0.00330, 0.00294,
                             0.00286, 0.00244, 0.00224, 0.00222])
    
    # k-ε realizable (11 puntos - serie completa)
    Re_k_epsilon_r = np.array([6.4e5, 1.28e6, 1.92e6, 2.56e6, 5e6, 1.03e7, 1.54e7,
                             2.05e7, 5.13e7, 1.28e8, 1.79e8])

    cf_k_epsilon_r = np.array([0.00690, 0.00608, 0.00546, 0.00500, 0.00395, 0.00292,
                               0.00271, 0.00261, 0.00234, 0.00213, 0.00203])
    
    # ITTC-1957: CF = 0.075/(log10(Re) - 2)^2
    Re_ittc = np.logspace(np.log10(6.4e5), np.log10(1.79e8), 200)
    cf_ittc = 0.075 / (np.log10(Re_ittc) - 2)**2
    
    # =========================================================================
    # CREAR GRÁFICO - mismo formato que 1+k
    # =========================================================================
    
    fig, ax = plt.subplots(figsize=(9, 6))
    
    # Colores matplotlib default (tab10)
    color_k_omega = '#1f77b4'           # Azul
    color_k_omega_sst = '#ff7f0e'       # Naranja
    color_k_epsilon = '#2ca02c'         # Verde
    color_k_epsilon_r = '#d62728'       # Rojo
    color_ittc = '#000000'              # Negro
    
    # Curvas CFD - marcadores con bordes negros
    ax.plot(Re_k_omega, cf_k_omega, 'o--', color=color_k_omega, linewidth=1.5,
            markersize=7, label=r'$k-\omega$', zorder=3,
            markeredgecolor='black', markeredgewidth=0.5)
    ax.plot(Re_k_omega_sst, cf_k_omega_sst, 'o--', color=color_k_omega_sst, linewidth=1.5,
            markersize=7, label=r'$k-\omega$ SST', zorder=3,
            markeredgecolor='black', markeredgewidth=0.5)
    ax.plot(Re_k_epsilon, cf_k_epsilon, 'o--', color=color_k_epsilon, linewidth=1.5,
            markersize=7, label=r'$k-\varepsilon$', zorder=3,
            markeredgecolor='black', markeredgewidth=0.5)
    ax.plot(Re_k_epsilon_r, cf_k_epsilon_r, 'o--', color=color_k_epsilon_r, linewidth=1.5,
            markersize=7, label=r'$k-\varepsilon$ realizable', zorder=3,
            markeredgecolor='black', markeredgewidth=0.5)
    
    # Línea ITTC - curva suave sólida
    ax.plot(Re_ittc, cf_ittc, '-', color=color_ittc, linewidth=2.0,
            label='ITTC', zorder=4)
    
    # =========================================================================
    # FORMATO (mismo que 1+k)
    # =========================================================================
    
    ax.set_xscale('log')
    
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    
    ax.set_xlabel('Rn', fontsize=14)
    ax.set_ylabel(r'$C_F$', fontsize=14)
    
    ax.set_xlim(5e5, 2.5e8)
    ax.set_ylim(0.0018, 0.0092)
    
    # 4 bordes negros del recuadro
    for side in ('top', 'right', 'bottom', 'left'):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(1.0)
        ax.spines[side].set_color('black')
    
    ax.tick_params(labelsize=12)
    ax.legend(fontsize=12, loc='upper right', framealpha=0.95)
    
    plt.tight_layout()
    
    plt.savefig(f'{OUTPUT_DIR}/cf_turbulencia.pdf',
                format='pdf', bbox_inches='tight', pad_inches=0.1)
    plt.savefig(f'{OUTPUT_DIR}/cf_turbulencia.png',
                format='png', bbox_inches='tight', pad_inches=0.1, dpi=150)
    plt.close()
    print("✓ cf_turbulencia.pdf")
    print("✓ cf_turbulencia.png")


if __name__ == "__main__":
    print("=" * 70)
    print("GENERANDO: CF vs Reynolds")
    print("=" * 70)
    generar_cf_turbulencia()
    print("=" * 70)
