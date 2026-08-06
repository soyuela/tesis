"""
COMPILACIÓN DE CÓDIGOS PARA GENERAR TODOS LOS GRÁFICOS
Formato estandarizado - Tesis
Generados desde 2024

PARÁMETROS ESTANDARIZADOS:
- Títulos de ejes: 31pt
- Números de ejes: 20pt
- Leyenda: 20pt
- Etiquetas adicionales: 18pt
- Salida: PDF vectorial

═══════════════════════════════════════════════════════════════════════════════
1. PROHASKA TPA COMPARACIÓN (EFD)
═══════════════════════════════════════════════════════════════════════════════
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from io import StringIO

# ============================================================================
# 1. PROHASKA TPA COMPARACIÓN (EFD) - prohaska_tpa_comparacion.pdf
# ============================================================================

def generar_prohaska_tpa_efd():
    """Diagrama Prohaska para P1 con datos EFD de tres calados"""
    
    # Constantes
    g = 9.807
    dens = 997.96
    visc = 9.869e-7
    
    # Características del modelo
    calados = {
        'T1': {'Lows': 1.670, 'sup': 0.982, 'LFr': 1.634, 'Fr_min': 0.155, 'Fr_max': 0.2},
        'T2': {'Lows': 1.740, 'sup': 1.058, 'LFr': 1.662, 'Fr_min': 0.165, 'Fr_max': 0.2},
        'T3': {'Lows': 1.740, 'sup': 1.124, 'LFr': 1.641, 'Fr_min': 0.153, 'Fr_max': 0.2}
    }
    
    # Datos CSV
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
    
    # Procesar datos
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
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = {'T1': '#2ca02c', 'T2': '#1f77b4', 'T3': '#d62728'}
    markers = {'T1': 's', 'T2': 'D', 'T3': 'o'}
    
    for calado_name in ['T1', 'T2', 'T3']:
        f = datos_puntos[calado_name]['f']
        c = datos_puntos[calado_name]['c']
        ax.scatter(f, c, s=150, color=colors[calado_name], marker=markers[calado_name],
                   label=f'{calado_name}: {calados_m[calado_name]}', zorder=3)
    
    # Líneas verticales
    x_vertical1, x_vertical2 = 0.0194, 0.36
    ax.axvline(x=x_vertical1, color='black', linestyle=':', linewidth=2, alpha=0.5, zorder=1)
    ax.axvline(x=x_vertical2, color='black', linestyle=':', linewidth=2, alpha=0.5, zorder=1)
    
    ax.text(x_vertical1 + 0.01, 1.72, 'Fr = 0.1', fontsize=18, ha='left')
    ax.text(x_vertical2 - 0.01, 1.72, 'Fr = 0.2', fontsize=18, ha='right')
    
    # Grid y ejes
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel('$Fr^4/C_{FM}$', fontsize=31)
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
    print("✓ Generado: prohaska_tpa_comparacion.pdf")


# ============================================================================
# 2. FORM FACTOR RANGE TPA - efd_form_factor_tpa_range.pdf
# ============================================================================

def generar_form_factor_range_tpa():
    """Sensibilidad del factor de forma al rango de Froude - TPA"""
    
    data_str = """0.1	1.04367	1.187
0.115	1.1133	
0.13	1.1554	
0.14	1.1862	
0.153	1.1927	
0.163	1.1283	1.187"""
    
    lines = data_str.strip().split('\n')
    Fn, Fn_range, EFD = [], [], []
    
    for line in lines:
        parts = line.split('\t')
        Fn.append(float(parts[0]))
        Fn_range.append(float(parts[1]))
        EFD.append(float(parts[2]) if len(parts) > 2 and parts[2].strip() else np.nan)
    
    Fn = np.array(Fn)
    Fn_range = np.array(Fn_range)
    EFD = np.array(EFD)
    valid_idx = np.where(~np.isnan(EFD))[0]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    tblue = '#3333cc'
    tred = '#cc3333'
    
    ax.scatter(Fn, Fn_range, s=150, color=tblue, marker='o', label='Rango evaluado', zorder=3)
    
    if len(valid_idx) >= 2:
        first_idx, last_idx = valid_idx[0], valid_idx[-1]
        ax.plot(Fn[[first_idx, last_idx]], EFD[[first_idx, last_idx]],
                's-', color=tred, markersize=10, linewidth=2, label='1+k EFD', zorder=2)
    
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel('Fr', fontsize=31)
    ax.set_ylabel('1+k', fontsize=31)
    x_margin = 0.01
    ax.set_xlim(min(Fn) - x_margin, max(Fn) + x_margin)
    ax.set_ylim(0.8, 1.3)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.tick_params(labelsize=20)
    ax.legend(fontsize=20, loc='upper left', framealpha=0.95)
    
    plt.subplots_adjust(top=0.90)
    plt.savefig('efd_form_factor_tpa_range.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("✓ Generado: efd_form_factor_tpa_range.pdf")


# ============================================================================
# 3. PROHASKA KCS - RTM-FR.pdf
# ============================================================================

def generar_prohaska_kcs():
    """Diagrama Prohaska para modelo KCS"""
    
    data_str = """0.566,1.031
0.65,1.302
0.652,1.311
0.65,1.32
0.65,1.327
0.658,1.36
0.738,1.752
0.75,1.786
0.749,1.812
0.81,2.044
0.81,2.067
0.815,2.117
0.852,2.33
0.86,2.351
0.852,2.37
0.909,2.587
0.915,2.661
0.915,2.666
0.963,2.849
0.957,2.926
0.971,2.934
0.968,2.984
1.056,3.439
1.067,3.55
1.07,3.619"""
    
    data = np.array([line.split(',') for line in data_str.strip().split('\n')], dtype=float)
    V1 = data[:, 0]
    RTM1 = data[:, 1]
    
    g, dens, visc = 9.807, 998, 9.869e-7
    Lows, sup, LFr = 2.9114, 1.527, 2.9114
    Fr_min, Fr_max = 0.1, 0.2
    
    FR1 = V1 / np.sqrt(g * LFr)
    REY1 = V1 * Lows / visc
    CFM1 = 0.075 / (np.log10(REY1) - 2)**2
    CTM1 = RTM1 / (0.5 * dens * sup * V1**2)
    
    ind1 = (FR1 >= Fr_min) & (FR1 <= Fr_max)
    f1, c1 = (FR1[ind1]**4) / CFM1[ind1], CTM1[ind1] / CFM1[ind1]
    
    slope, intercept, _, _, _ = stats.linregress(f1, c1)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.scatter(f1, c1, s=150, color='#3333cc', marker='o', zorder=3)
    px1 = np.array([min(f1), max(f1)])
    py1 = slope * px1 + intercept
    ax.plot(px1, py1, color='black', linewidth=2, zorder=2)
    
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel('$Fr^4/C_{F0}$', fontsize=31)
    ax.set_ylabel('$C_{TM}/C_{F0}$', fontsize=31)
    ax.set_xlim(0, 0.45)
    ax.set_ylim(0.8, 1.4)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.tick_params(labelsize=20)
    
    plt.subplots_adjust(top=0.90)
    plt.savefig('RTM-FR.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("✓ Generado: RTM-FR.pdf")


# ============================================================================
# 4. FORM FACTOR RANGE KCS - kcs_efd_form_factor_range.pdf
# ============================================================================

def generar_form_factor_range_kcs():
    """Sensibilidad del factor de forma al rango de Froude - KCS"""
    
    data_str = """0.1	1.0151	1.0563
0.11	1.0175	
0.13	1.0551	
0.14	1.0563	
0.15	1.0619	
0.16	1.0746	
0.17	1.0779	1.0563"""
    
    lines = data_str.strip().split('\n')
    Fn, Fn_range, EFD = [], [], []
    
    for line in lines:
        parts = line.split('\t')
        Fn.append(float(parts[0]))
        Fn_range.append(float(parts[1]))
        EFD.append(float(parts[2]) if len(parts) > 2 and parts[2].strip() else np.nan)
    
    Fn = np.array(Fn)
    Fn_range = np.array(Fn_range)
    EFD = np.array(EFD)
    valid_idx = np.where(~np.isnan(EFD))[0]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    tblue, tred = '#3333cc', '#cc3333'
    
    ax.scatter(Fn, Fn_range, s=150, color=tblue, marker='o', label='Rango evaluado', zorder=3)
    
    if len(valid_idx) >= 2:
        first_idx, last_idx = valid_idx[0], valid_idx[-1]
        ax.plot(Fn[[first_idx, last_idx]], EFD[[first_idx, last_idx]],
                's-', color=tred, markersize=10, linewidth=2, label='1+k EFD', zorder=2)
    
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel('Fr', fontsize=31)
    ax.set_ylabel('1+k', fontsize=31)
    x_margin = 0.01
    ax.set_xlim(min(Fn) - x_margin, max(Fn) + x_margin)
    ax.set_ylim(0.8, 1.3)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.tick_params(labelsize=20)
    ax.legend(fontsize=20, loc='upper left', framealpha=0.95)
    
    plt.subplots_adjust(top=0.90)
    plt.savefig('kcs_efd_form_factor_range.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("✓ Generado: kcs_efd_form_factor_range.pdf")


# ============================================================================
# 5. EFD KCS LITERATURA - efd_kcs_lit.pdf
# ============================================================================

def generar_efd_kcs_literatura():
    """Comparación EFD KCS: Literatura vs LabHiNO"""
    
    Re_KCS_EFD_Lit = np.array([2281465.895, 3337500.959, 6346048.446, 17949335.56, 
                              6346048.446, 11713995.83, 17950187.62, 33132183.54])
    k_KCS_EFD_Lit = np.array([1.032903, 1.085161, 1.102581, 1.11807, 
                             1.155769231, 1.123076923, 1.142307692, 1.121153846])
    
    Re_KCS_EFD_CE = np.array([2.28392E+06])
    k_KCS_EFD_CE = np.array([1.0563])
    
    tyellow = '#e6e600'
    tred = '#cc3333'
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.scatter(Re_KCS_EFD_Lit, k_KCS_EFD_Lit, s=150, color=tyellow, marker='o',
               label='EFD Data Set', zorder=3, edgecolors='black', linewidth=1)
    ax.scatter(Re_KCS_EFD_CE, k_KCS_EFD_CE, s=150, color=tred, marker='o',
               label='EFD LabHiNO', zorder=3, edgecolors='black', linewidth=1)
    
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xscale('log')
    ax.set_xlabel('Re', fontsize=31)
    ax.set_ylabel('1+k', fontsize=31)
    ax.set_xlim(1e6, 5e7)
    ax.set_ylim(0.95, 1.3)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.tick_params(labelsize=20)
    ax.legend(fontsize=20, loc='upper right', framealpha=0.95)
    
    plt.subplots_adjust(top=0.90)
    plt.savefig('efd_kcs_lit.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("✓ Generado: efd_kcs_lit.pdf")


# ============================================================================
# 6. PROHASKA TPA CFD - prohaska_tpa_cfd_comparacion.pdf
# ============================================================================

def generar_prohaska_tpa_cfd():
    """Diagrama Prohaska para P1 con datos CFD de tres calados"""
    
    calados = {
        'T1': {
            'name': 'T1: 0.165m',
            'Lows': 1.670, 'sup': 0.982, 'LFr': 1.634,
            'data': """0.10	0.405	0.570
0.11	0.445	0.642
0.12	0.486	0.736
0.13	0.526	0.848
0.14	0.567	0.968
0.15	0.607	1.11
0.16	0.648	1.258
0.17	0.688	1.456
0.18	0.729	1.64
0.19	0.769	1.906
0.20	0.810	2.184"""
        },
        'T2': {
            'name': 'T2: 0.180m',
            'Lows': 1.740, 'sup': 1.058, 'LFr': 1.662,
            'data': """0.10	0.40	0.658
0.11	0.44	0.754
0.12	0.48	0.866
0.13	0.52	0.980
0.14	0.57	1.152
0.15	0.61	1.308
0.16	0.65	1.472
0.17	0.69	1.664
0.18	0.73	1.910
0.19	0.77	2.182
0.20	0.81	2.476"""
        },
        'T3': {
            'name': 'T3: 0.195m',
            'Lows': 1.740, 'sup': 1.124, 'LFr': 1.641,
            'data': """0.10	0.40	0.606
0.11	0.44	0.714
0.12	0.48	0.822
0.13	0.52	0.952
0.14	0.56	1.112
0.15	0.60	1.27
0.16	0.64	1.44
0.17	0.68	1.656
0.18	0.72	1.914
0.19	0.76	2.192
0.20	0.80	2.45"""
        }
    }
    
    g, dens, visc = 9.807, 997.96, 9.869e-7
    datos_puntos = {}
    
    for calado_name in ['T1', 'T2', 'T3']:
        calado = calados[calado_name]
        lines = calado['data'].strip().split('\n')
        Fr_data, V, RTM = [], [], []
        
        for line in lines:
            parts = line.split('\t')
            Fr_data.append(float(parts[0].replace(',', '.')))
            V.append(float(parts[1].replace(',', '.')))
            RTM.append(float(parts[2].replace(',', '.')))
        
        Fr_data = np.array(Fr_data)
        V = np.array(V)
        RTM = np.array(RTM)
        
        REY = V * calado['Lows'] / visc
        CTM = RTM / (0.5 * dens * calado['sup'] * V**2)
        CFM = 0.075 / (np.log10(REY) - 2)**2
        
        f = (Fr_data**4) / CFM
        c = CTM / CFM
        
        datos_puntos[calado_name] = {'f': f, 'c': c}
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = {'T1': '#2ca02c', 'T2': '#1f77b4', 'T3': '#d62728'}
    markers = {'T1': 's', 'T2': 'D', 'T3': 'o'}
    
    for calado_name in ['T1', 'T2', 'T3']:
        f = datos_puntos[calado_name]['f']
        c = datos_puntos[calado_name]['c']
        ax.scatter(f, c, s=150, color=colors[calado_name], marker=markers[calado_name],
                   label=calados[calado_name]['name'], zorder=3)
    
    x_vertical1, x_vertical2 = 0.01, 0.33
    ax.axvline(x=x_vertical1, color='black', linestyle=':', linewidth=2, alpha=0.5, zorder=1)
    ax.axvline(x=x_vertical2, color='black', linestyle=':', linewidth=2, alpha=0.5, zorder=1)
    
    ax.text(x_vertical1 + 0.01, 1.72, 'Fr = 0.1', fontsize=18, ha='left')
    ax.text(x_vertical2 - 0.01, 1.72, 'Fr = 0.2', fontsize=18, ha='right')
    
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel('$Fr^4/C_{FM}$', fontsize=31)
    ax.set_ylabel('$C_T/C_{FM}$', fontsize=31)
    ax.set_xlim(0, 0.4)
    ax.set_ylim(0.6, 2.0)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.tick_params(labelsize=20)
    ax.legend(fontsize=20, loc='upper center', framealpha=0.95, ncol=3,
              bbox_to_anchor=(0.5, 1.25))
    
    plt.subplots_adjust(top=0.80)
    plt.savefig('prohaska_tpa_cfd_comparacion.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("✓ Generado: prohaska_tpa_cfd_comparacion.pdf")


# ============================================================================
# EJECUTAR TODOS
# ============================================================================

if __name__ == "__main__":
    print("Generando todos los gráficos con formato estandarizado...")
    print()
    generar_prohaska_tpa_efd()
    generar_form_factor_range_tpa()
    generar_prohaska_kcs()
    generar_form_factor_range_kcs()
    generar_efd_kcs_literatura()
    generar_prohaska_tpa_cfd()
    print()
    print("✓ Todos los gráficos generados correctamente")
