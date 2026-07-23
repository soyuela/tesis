"""
Factor de forma vs Reynolds - Modelos de turbulencia
Datos extraídos por análisis pixel-a-pixel de la imagen original
Formato estandarizado de la tesis
"""

import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = './graficos_pdf'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generar_factor_forma_turbulencia():
    """
    Gráfico de Factor de forma (1+k) vs Reynolds
    4 modelos de turbulencia CFD + valor experimental
    """
    
    # =========================================================================
    # DATOS EXTRAÍDOS DE LA IMAGEN
    # Reynolds común (donde se hicieron simulaciones):
    # [6.4e5, 1.28e6, 1.92e6, 2.56e6, 5.13e6, 1.03e7, 1.54e7, 2.05e7, 5.13e7, 1.28e8, 1.79e8]
    # =========================================================================
    
    # k-ω (10 puntos, sin punto en Re=5.13e7)
    Re_k_omega = np.array([6.4e5, 1.28e6, 1.92e6, 2.56e6, 5.13e6, 1.03e7,
                               1.54e7, 2.05e7, 5.13e7, 1.28e8, 1.79e8])

    k_omega = np.array([1.54, 1.62, 1.76, 2.02, 1.60, 1.68, 
                        1.78, 1.83, 1.72, 1.79, 1.90])
    
    # k-ω SST (9 puntos, sin puntos en Re=1.54e7 y 5.13e7)
    Re_k_omega_sst = np.array([6.4e5, 1.28e6, 1.92e6, 2.56e6, 5.13e6, 1.03e7,
                               1.54e7, 2.05e7, 5.13e7, 1.28e8, 1.79e8])

    k_omega_sst = np.array([1.18, 1.32, 1.46, 1.63, 1.48, 1.49,
                            1.52, 1.55, 1.65, 1.65, 1.73])
    
    # k-ε (9 puntos, sin puntos en Re=2.56e6 y 5.13e6)
    Re_k_epsilon = np.array([6.4e5, 1.28e6, 1.92e6, 2.56e6, 5.13e6, 1.03e7,
                               1.54e7, 2.05e7, 5.13e7, 1.28e8, 1.79e8])

    k_epsilon = np.array([2.36, 2.29, 2.23, 1.83, 1.71, 1.62, 1.64, 
                          1.67, 1.72, 1.77, 1.87])
    
    # k-ε realizable (11 puntos, serie completa)
    Re_k_epsilon_r = np.array([6.4e5, 1.28e6, 1.92e6, 2.56e6, 5.13e6, 1.03e7,
                               1.54e7, 2.05e7, 5.13e7, 1.28e8, 1.79e8])
    k_epsilon_r = np.array([1.93, 1.93, 1.89, 1.83, 1.71, 1.51,
                            1.52, 1.57, 1.65, 1.70, 1.76])
    
    # Experimental (línea horizontal con 2 marcadores en los extremos)
    Re_exp = np.array([6.4e5, 1.79e8])
    k_exp = np.array([1.18, 1.18])
    
    # =========================================================================
    # CREAR GRÁFICO
    # =========================================================================
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Colores matplotlib default (tab10)
    color_k_omega = '#1f77b4'           # Azul
    color_k_omega_sst = '#ff7f0e'       # Naranja
    color_k_epsilon = '#2ca02c'         # Verde
    color_k_epsilon_r = '#d62728'       # Rojo
    color_exp = '#000000'               # Negro
    
    # Curvas CFD con marcadores y líneas punteadas
    ax.plot(Re_k_omega, k_omega, 'o--', color=color_k_omega, linewidth=2.5, 
            markersize=9, label=r'$k-\omega$', zorder=3)
    ax.plot(Re_k_omega_sst, k_omega_sst, 'o--', color=color_k_omega_sst, linewidth=2.5, 
            markersize=9, label=r'$k-\omega$ SST', zorder=3)
    ax.plot(Re_k_epsilon, k_epsilon, 'o--', color=color_k_epsilon, linewidth=2.5, 
            markersize=9, label=r'$k-\varepsilon$', zorder=3)
    ax.plot(Re_k_epsilon_r, k_epsilon_r, 'o--', color=color_k_epsilon_r, linewidth=2.5, 
            markersize=9, label=r'$k-\varepsilon$ realizable', zorder=3)
    
    # Experimental - línea sólida horizontal con marcadores en los extremos
    ax.plot(Re_exp, k_exp, 'o-', color=color_exp, linewidth=2.5, 
            markersize=9, label='Experimental', zorder=3)
    
    # =========================================================================
    # FORMATO
    # =========================================================================
    
    # Escala logarítmica en X
    ax.set_xscale('log')
    
    # Grid
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    
    # Etiquetas
    ax.set_xlabel('Rn', fontsize=31)
    ax.set_ylabel('1+k', fontsize=31)
    
    # Límites
    ax.set_xlim(5e5, 2.5e8)
    ax.set_ylim(1.15, 2.45)
    
    # Bordes
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    
    # Tick labels
    ax.tick_params(labelsize=20)
    
    # Leyenda
    ax.legend(fontsize=20, loc='upper right', framealpha=0.95)
    
    plt.tight_layout()
    
    # Guardar
    plt.savefig(f'{OUTPUT_DIR}/factor_forma_turbulencia.pdf', 
                format='pdf', bbox_inches='tight', pad_inches=0.1)
    plt.savefig(f'{OUTPUT_DIR}/factor_forma_turbulencia.png', 
                format='png', bbox_inches='tight', pad_inches=0.1, dpi=150)
    plt.close()
    print("✓ factor_forma_turbulencia.pdf")
    print("✓ factor_forma_turbulencia.png")


if __name__ == "__main__":
    print("=" * 70)
    print("REGENERANDO: Factor de forma vs Reynolds")
    print("=" * 70)
    generar_factor_forma_turbulencia()
    print("=" * 70)
