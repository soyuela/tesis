"""
COMPILACIÓN DE CÓDIGOS PARA GENERAR TODOS LOS GRÁFICOS
Formato estandarizado - Tesis
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from io import StringIO

# PARÁMETROS ESTANDARIZADOS
# Títulos: 31pt | Ejes: 20pt | Leyenda: 20pt | Etiquetas: 18pt

# ============================================================================
# 1. PROHASKA TPA COMPARACIÓN (EFD)
# ============================================================================

def generar_prohaska_tpa_efd():
    g = 9.807
    dens = 997.96
    visc = 9.869e-7
    
    calados = {
        'T1': {'Lows': 1.670, 'sup': 0.982, 'LFr': 1.634},
        'T2': {'Lows': 1.740, 'sup': 1.058, 'LFr': 1.662},
        'T3': {'Lows': 1.740, 'sup': 1.124, 'LFr': 1.641}
    }
    
    csv_data = {
        'T1': """0.45,0.51
0.48,0.6
0.55,0.87
0.61,1.11
0.64,1.28
0.71,1.65
0.74,1.8
0.8,2.24
0.86,2.78
0.89,3.06
0.94,3.55
0.94,3.52
0.95,3.66""",
        'T2': """0.33,0.192
0.38,0.341
0.45,0.5
0.45,0.542
0.5,0.682
0.51,0.735
0.54,0.856
0.55,0.87
0.59,1.059
0.6,1.094
0.65,1.336
0.65,1.38
0.71,1.674
0.71,1.717
0.74,1.93
0.76,2.021
0.79,2.242
0.8,2.347
0.84,2.726
0.85,2.781
0.88,3.036
0.89,3.122
0.92,4.299
0.93,3.485
0.94,3.681
0.96,3.795""",
        'T3': """0.39,0.393
0.46,0.605
0.46,0.604
0.49,0.734
0.56,1.012
0.61,1.252
0.65,1.456
0.72,1.842
0.72,1.816
0.77,2.198
0.81,2.518
0.86,2.925
0.89,3.267
0.95,3.812
0.96,3.928"""
    }
    
    datos_puntos = {}
    calados_m = {'T1': '0.165m', 'T2': '0.180m', 'T3': '0.195m'}
    
    for calado_name, calado_params in calados.items():
        data = np.loadtxt(StringIO(csv_data[calado_name]), delimiter=',')
        V = data[:, 0]
        RTM = data[:, 1]
        
        FR = V / np.sqrt(g * calado_params['LFr'])
        REY = V * calado_params['Lows'] / visc
        CTM = RTM / (0.5 * dens * calado_params['sup'] * V**2)
        CFM = 0.075 / (np.log10(REY) - 2)**2
        
        f = (FR**4) / CFM
        c = CTM / CFM
        
        datos_puntos[calado_name] = {'f': f, 'c': c}
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = {'T1': '#2ca02c', 'T2': '#1f77b4', 'T3': '#d62728'}
    markers = {'T1': 's', 'T2': 'D', 'T3': 'o'}
    
    for calado_name in ['T1', 'T2', 'T3']:
        f = datos_puntos[calado_name]['f']
        c = datos_puntos[calado_name]['c']
        ax.scatter(f, c, s=150, color=colors[calado_name], marker=markers[calado_name],
                   label=f'{calado_name}: {calados_m[calado_name]}', zorder=3)
    
    x_vertical1, x_vertical2 = 0.0194, 0.36
    ax.axvline(x=x_vertical1, color='black', linestyle=':', linewidth=2, alpha=0.5, zorder=1)
    ax.axvline(x=x_vertical2, color='black', linestyle=':', linewidth=2, alpha=0.5, zorder=1)
    
    ax.text(x_vertical1 + 0.01, 1.72, 'Fn = 0.1', fontsize=18, ha='left')
    ax.text(x_vertical2 - 0.01, 1.72, 'Fn = 0.2', fontsize=18, ha='right')
    
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel('$F_n^4/C_{FM}$', fontsize=31)
    ax.set_ylabel('$C_T/C_{FM}$', fontsize=31)
    ax.set_xlim(0, 0.4)
    ax.set_ylim(0.5, 1.8)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.tick_params(labelsize=20)
    ax.legend(fontsize=20, loc='upper center', framealpha=0.95, ncol=3, bbox_to_anchor=(0.5, 1.15))
    
    plt.subplots_adjust(top=0.80)
    plt.savefig('prohaska_tpa_comparacion.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("✓ prohaska_tpa_comparacion.pdf")


# ============================================================================
# 2. KCS DB PROHASKA
# ============================================================================

def generar_kcs_db_prohaska():
    from matplotlib.ticker import FuncFormatter
    
    Re_1_79 = np.array([2.8549E+05, 5.7098E+05, 8.5647E+05, 1.1420E+06, 1.4274E+06, 1.71E+06, 2.00E+06, 2.2839E+06, 2.5694E+06, 2.8549E+06,
                        3.1404E+06, 3.43E+06, 3.7114E+06, 3.9969E+06, 4.28E+06, 4.57E+06, 4.8533E+06, 5.1388E+06, 5.4243E+06, 5.71E+06])
    y_1_79 = np.array([1.00, 1.01, 1.02, 1.09, 1.14, 1.20, 1.297, 1.301, 1.28, 1.25,
                       1.21, 1.18, 1.15, 1.13, 1.11, 1.11, 1.11, 1.11, 1.11, 1.11])

    Re_Terziev = np.array([3.78E+05, 7.55E+05, 1.13E+06, 1.51E+06, 1.89E+06, 2.27E+06, 2.64E+06, 3.02E+06, 3.40E+06, 3.78E+06,
                           4.15E+06, 4.53E+06, 4.91E+06, 5.29E+06])
    y_Terziev = np.array([1.120, 1.240, 1.255, 1.200, 1.180, 1.160, 1.140, 1.125, 1.115, 1.110,
                          1.105, 1.100, 1.095, 1.090])

    y_Prohaska = 1.0563
    tblue = '#3333cc'
    tred = '#cc3333'

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.scatter(Re_1_79, y_1_79, s=150, color=tblue, marker='o', label='CFD - DB LabHiNO', zorder=3)
    ax.scatter(Re_Terziev, y_Terziev, s=150, color=tred, marker='o', label='CFD - DB Data Set', zorder=3)

    Re_min = min(Re_1_79.min(), Re_Terziev.min())
    Re_max = max(Re_1_79.max(), Re_Terziev.max())
    ax.plot([Re_min, Re_max], [y_Prohaska, y_Prohaska], 'k-', linewidth=2, label='EFD LabHiNO', zorder=2)

    ax.axvline(x=1.427E+06, color='black', linestyle=':', linewidth=2, alpha=0.5, zorder=1)
    ax.axvline(x=2.854E+06, color='black', linestyle=':', linewidth=2, alpha=0.5, zorder=1)

    ax.text(1.427E+06 - 0.15e6, 1.32, 'Fn = 0.1', fontsize=18, ha='right')
    ax.text(2.854E+06 + 0.15e6, 1.32, 'Fn = 0.2', fontsize=18, ha='left')

    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    def format_re(x, pos):
        if x == 0:
            return '0'
        return f'{x/1e6:.2f}'

    ax.xaxis.set_major_formatter(FuncFormatter(format_re))
    ax.set_xlabel('Re (×10$^6$)', fontsize=31)
    ax.set_ylabel('1+k', fontsize=31)
    ax.set_ylim(0.95, 1.35)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.tick_params(labelsize=20)
    ax.legend(fontsize=20, loc='upper right', framealpha=0.95)

    plt.tight_layout()
    plt.savefig('kcs_DB_prohaska.pdf', format='pdf', bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print("✓ kcs_DB_prohaska.pdf")


# ============================================================================
# EJECUTAR
# ============================================================================

if __name__ == "__main__":
    print("Generando gráficos...")
    generar_prohaska_tpa_efd()
    generar_kcs_db_prohaska()
    print("\n✓ Completado")
