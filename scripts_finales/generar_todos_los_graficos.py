"""
═══════════════════════════════════════════════════════════════════════════════
CÓDIGOS FINALES PARA GENERAR TODOS LOS GRÁFICOS - TESIS
Formato estandarizado
═══════════════════════════════════════════════════════════════════════════════

PARÁMETROS ESTANDARIZADOS:
- Títulos de ejes: 31pt
- Números de ejes: 20pt
- Leyenda: 20pt
- Etiquetas adicionales: 18pt
- Salida: PDF vectorial

Uso:
    python generar_todos_los_graficos.py

Requisitos:
    pip install numpy matplotlib scipy

═══════════════════════════════════════════════════════════════════════════════
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from scipy import stats
from io import StringIO
import os

# Directorio de salida
OUTPUT_DIR = './graficos_pdf'
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================================
# CONSTANTES Y CARACTERÍSTICAS DEL P1
# ============================================================================

g = 9.807
dens = 997.96
visc = 9.869e-7

CALADOS_P1 = {
    'T1': {'name': '0.165m', 'Lows': 1.670, 'sup': 0.982, 'LFr': 1.634},
    'T2': {'name': '0.180m', 'Lows': 1.740, 'sup': 1.058, 'LFr': 1.662},
    'T3': {'name': '0.195m', 'Lows': 1.740, 'sup': 1.124, 'LFr': 1.641}
}

# Datos EFD del P1
EFD_DATA_P1 = {
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

# Datos CFD del P1 (Fr, V, RTM)
CFD_DATA_P1 = {
    'T1': """0.10	0.405	0.570
0.11	0.445	0.642
0.12	0.486	0.736
0.13	0.526	0.848
0.14	0.567	0.968
0.15	0.607	1.11
0.16	0.648	1.258
0.17	0.688	1.456
0.18	0.729	1.64
0.19	0.769	1.906
0.20	0.810	2.184""",
    'T2': """0.10	0.40	0.658
0.11	0.44	0.754
0.12	0.48	0.866
0.13	0.52	0.980
0.14	0.57	1.152
0.15	0.61	1.308
0.16	0.65	1.472
0.17	0.69	1.664
0.18	0.73	1.910
0.19	0.77	2.182
0.20	0.81	2.476""",
    'T3': """0.10	0.40	0.606
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

# Rangos EFD por calado (que dan los valores de la tabla del capítulo)
EFD_RANGES = {
    'T1': (0.140, 0.240),
    'T2': (0.150, 0.240),
    'T3': (0.155, 0.200)
}

# Valores EFD adoptados (de la tabla del capítulo)
EFD_VALUES = {
    'T1': 1.252,
    'T2': 1.211,
    'T3': 1.194
}


# ============================================================================
# 1. PROHASKA TPA COMPARACIÓN (EFD) - 3 calados en un gráfico
# ============================================================================

def generar_prohaska_tpa_efd():
    datos_puntos = {}
    calados_m = {'T1': '0.165m', 'T2': '0.180m', 'T3': '0.195m'}
    
    for calado_name, calado_params in CALADOS_P1.items():
        data = np.loadtxt(StringIO(EFD_DATA_P1[calado_name]), delimiter=',')
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
    ax.text(x_vertical1 + 0.01, 1.72, 'Fr = 0.1', fontsize=18, ha='left')
    ax.text(x_vertical2 - 0.01, 1.72, 'Fr = 0.2', fontsize=18, ha='right')
    
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
    plt.savefig(f'{OUTPUT_DIR}/prohaska_tpa_comparacion.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("✓ prohaska_tpa_comparacion.pdf")


# ============================================================================
# 2. PROHASKA TPA CFD (3 calados)
# ============================================================================

def generar_prohaska_tpa_cfd():
    datos_puntos = {}
    calados_m = {'T1': '0.165m', 'T2': '0.180m', 'T3': '0.195m'}
    
    for calado_name in ['T1', 'T2', 'T3']:
        calado = CALADOS_P1[calado_name]
        lines = CFD_DATA_P1[calado_name].strip().split('\n')
        Fr_data, V, RTM = [], [], []
        for line in lines:
            parts = line.split('\t')
            Fr_data.append(float(parts[0]))
            V.append(float(parts[1]))
            RTM.append(float(parts[2]))
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
                   label=f'{calado_name}: {calados_m[calado_name]}', zorder=3)
    
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
    ax.legend(fontsize=20, loc='upper center', framealpha=0.95, ncol=3, bbox_to_anchor=(0.5, 1.25))
    
    plt.subplots_adjust(top=0.80)
    plt.savefig(f'{OUTPUT_DIR}/prohaska_tpa_cfd_comparacion.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("✓ prohaska_tpa_cfd_comparacion.pdf")


# ============================================================================
# 3. FORM FACTOR RANGE EFD - P1 (sensibilidad)
# ============================================================================

def generar_form_factor_range_tpa():
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
    plt.savefig(f'{OUTPUT_DIR}/efd_form_factor_tpa_range.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("✓ efd_form_factor_tpa_range.pdf")


# ============================================================================
# 4. FORM FACTOR RANGE CFD - P1 Calado 3
# ============================================================================

def generar_cfd_form_factor_195_range():
    # Datos CFD del calado 0.195
    Fr_cfd = np.array([0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20])
    V_cfd = np.array([0.40, 0.44, 0.48, 0.52, 0.56, 0.60, 0.64, 0.68, 0.72, 0.76, 0.80])
    RTM_cfd = np.array([0.606, 0.714, 0.822, 0.952, 1.112, 1.27, 1.44, 1.656, 1.914, 2.192, 2.45])
    
    calado = CALADOS_P1['T3']
    REY_all = V_cfd * calado['Lows'] / visc
    CTM_all = RTM_cfd / (0.5 * dens * calado['sup'] * V_cfd**2)
    CFM_all = 0.075 / (np.log10(REY_all) - 2)**2
    
    Fn_limits = np.arange(0.10, 0.18, 0.01)
    k_values = []
    
    for Fn_lower in Fn_limits:
        ind = (Fr_cfd >= Fn_lower) & (Fr_cfd <= 0.20)
        if np.sum(ind) >= 2:
            f = (Fr_cfd[ind]**4) / CFM_all[ind]
            c = CTM_all[ind] / CFM_all[ind]
            _, intercept, _, _, _ = stats.linregress(f, c)
            k_values.append(intercept)
        else:
            k_values.append(np.nan)
    
    k_values = np.array(k_values)
    
    # Buscar valor adoptado (estable Fn > 0.15)
    stable_region = np.where(Fn_limits >= 0.15)[0]
    adopted_idx = stable_region[0] if len(stable_region) > 0 else np.nanargmin(np.abs(np.diff(k_values))) + 1
    adopted_k = k_values[adopted_idx]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    tblue, tred = '#3333cc', '#cc3333'
    
    ax.scatter(Fn_limits, k_values, s=150, color=tblue, marker='o', label='Rango evaluado', zorder=3)
    ax.plot([0.1, 0.18], [adopted_k, adopted_k], 's-', color=tred, markersize=10, linewidth=2,
            label='1+k CFD', zorder=2)
    
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel('Fr', fontsize=31)
    ax.set_ylabel('1+k', fontsize=31)
    x_margin = 0.01
    ax.set_xlim(min(Fn_limits) - x_margin, 0.19)
    ax.set_ylim(0.8, 1.5)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.tick_params(labelsize=20)
    ax.legend(fontsize=20, loc='upper left', framealpha=0.95)
    
    plt.subplots_adjust(top=0.90)
    plt.savefig(f'{OUTPUT_DIR}/cfd_form_factor_tpa_195_range.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("✓ cfd_form_factor_tpa_195_range.pdf")


# ============================================================================
# 5. PROHASKA COMPARACIÓN EFD vs CFD (3 calados individuales)
# ============================================================================

def generar_prohaska_efd_cfd_comparacion():
    color_efd = '#d62728'
    color_cfd = '#1f77b4'
    
    for calado_name, calado in CALADOS_P1.items():
        # EFD
        data_efd = np.loadtxt(StringIO(EFD_DATA_P1[calado_name]), delimiter=',')
        V_efd = data_efd[:, 0]
        RTM_efd = data_efd[:, 1]
        FR_efd = V_efd / np.sqrt(g * calado['LFr'])
        REY_efd = V_efd * calado['Lows'] / visc
        CTM_efd = RTM_efd / (0.5 * dens * calado['sup'] * V_efd**2)
        CFM_efd = 0.075 / (np.log10(REY_efd) - 2)**2
        f_efd_all = (FR_efd**4) / CFM_efd
        c_efd_all = CTM_efd / CFM_efd
        
        # CFD
        lines_cfd = CFD_DATA_P1[calado_name].strip().split('\n')
        Fr_cfd, V_cfd, RTM_cfd = [], [], []
        for line in lines_cfd:
            parts = line.split('\t')
            Fr_cfd.append(float(parts[0]))
            V_cfd.append(float(parts[1]))
            RTM_cfd.append(float(parts[2]))
        Fr_cfd = np.array(Fr_cfd)
        V_cfd = np.array(V_cfd)
        RTM_cfd = np.array(RTM_cfd)
        
        REY_cfd = V_cfd * calado['Lows'] / visc
        CTM_cfd = RTM_cfd / (0.5 * dens * calado['sup'] * V_cfd**2)
        CFM_cfd = 0.075 / (np.log10(REY_cfd) - 2)**2
        f_cfd = (Fr_cfd**4) / CFM_cfd
        c_cfd = CTM_cfd / CFM_cfd
        
        # Filtros
        fn_min_efd, fn_max_efd = EFD_RANGES[calado_name]
        ind_efd = (FR_efd >= fn_min_efd) & (FR_efd <= fn_max_efd)
        ind_cfd = (Fr_cfd >= 0.16) & (Fr_cfd <= 0.20)
        
        slope_cfd, intercept_cfd, _, _, _ = stats.linregress(f_cfd[ind_cfd], c_cfd[ind_cfd])
        slope_efd, intercept_efd, _, _, _ = stats.linregress(f_efd_all[ind_efd], c_efd_all[ind_efd])
        
        # Posición en el eje X (Fr^4/CFM) correspondiente a Fr = 0.10 y Fr = 0.20
        # El eje X no es Fr directamente, así que se recalcula vía V -> Re -> CFM -> f
        Fr_marks = [0.10, 0.20]
        x_marks = []
        for Fr_mark in Fr_marks:
            V_mark = Fr_mark * np.sqrt(g * calado['LFr'])
            REY_mark = V_mark * calado['Lows'] / visc
            CFM_mark = 0.075 / (np.log10(REY_mark) - 2)**2
            x_marks.append((Fr_mark**4) / CFM_mark)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        ax.scatter(f_efd_all, c_efd_all, s=150, color=color_efd, marker='o',
                   zorder=3, edgecolors='black', linewidth=0.5, label='EFD')
        ax.scatter(f_cfd, c_cfd, s=150, color=color_cfd, marker='o',
                   zorder=3, edgecolors='black', linewidth=0.5, label='CFD')
        
        x_line = np.linspace(0, 0.4, 100)
        ax.plot(x_line, slope_cfd * x_line + intercept_cfd, color=color_cfd, linewidth=2.5, zorder=2)
        ax.plot(x_line, slope_efd * x_line + intercept_efd, color=color_efd, linewidth=2.5, zorder=2)
        
        ax.axvline(x=x_marks[0], color='black', linestyle=':', linewidth=2, alpha=0.5, zorder=1)
        ax.axvline(x=x_marks[1], color='black', linestyle=':', linewidth=2, alpha=0.5, zorder=1)
        ax.text(x_marks[0] + 0.01, 1.9, 'Fr = 0.10', fontsize=18, ha='left')
        ax.text(x_marks[1] - 0.01, 1.9, 'Fr = 0.20', fontsize=18, ha='right')
        
        ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)
        ax.set_xlabel(r'$\mathrm{Fr^4/C_{F0}}$', fontsize=31)
        ax.set_ylabel(r'$\mathrm{C_{TM}/C_{F0}}$', fontsize=31)
        ax.set_xlim(0, 0.4)
        ax.set_ylim(1.0, 2.0)
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_linewidth(1.5)
        ax.spines['left'].set_linewidth(1.5)
        ax.tick_params(labelsize=20)
        ax.legend(fontsize=20, loc='lower right', framealpha=0.95)
        
        plt.tight_layout()
        num = calado['name'].replace('m', '').replace('0.', '')
        filename = f'prohaska-efd-cfd-{num}.pdf'
        plt.savefig(f'{OUTPUT_DIR}/{filename}', format='pdf', bbox_inches='tight', pad_inches=0.1)
        plt.close()
        print(f"✓ {filename}")


# ============================================================================
# 6. COMPARACIÓN RANGE EFD vs CFD (3 calados)
# ============================================================================

def generar_comparacion_range_efd_cfd():
    color_efd = '#d62728'
    color_cfd = '#1f77b4'
    Fn_limits = np.arange(0.10, 0.19, 0.01)
    
    for calado_name, calado in CALADOS_P1.items():
        # EFD
        data_efd = np.loadtxt(StringIO(EFD_DATA_P1[calado_name]), delimiter=',')
        V_efd = data_efd[:, 0]
        RTM_efd = data_efd[:, 1]
        FR_efd = V_efd / np.sqrt(g * calado['LFr'])
        REY_efd = V_efd * calado['Lows'] / visc
        CTM_efd = RTM_efd / (0.5 * dens * calado['sup'] * V_efd**2)
        CFM_efd = 0.075 / (np.log10(REY_efd) - 2)**2
        f_efd = (FR_efd**4) / CFM_efd
        c_efd = CTM_efd / CFM_efd
        
        # CFD
        lines_cfd = CFD_DATA_P1[calado_name].strip().split('\n')
        Fr_cfd, V_cfd, RTM_cfd = [], [], []
        for line in lines_cfd:
            parts = line.split('\t')
            Fr_cfd.append(float(parts[0]))
            V_cfd.append(float(parts[1]))
            RTM_cfd.append(float(parts[2]))
        Fr_cfd = np.array(Fr_cfd)
        V_cfd = np.array(V_cfd)
        RTM_cfd = np.array(RTM_cfd)
        REY_cfd = V_cfd * calado['Lows'] / visc
        CTM_cfd = RTM_cfd / (0.5 * dens * calado['sup'] * V_cfd**2)
        CFM_cfd = 0.075 / (np.log10(REY_cfd) - 2)**2
        f_cfd = (Fr_cfd**4) / CFM_cfd
        c_cfd = CTM_cfd / CFM_cfd
        
        # Calcular 1+k para cada límite inferior
        k_efd_list, k_cfd_list = [], []
        for Fn_low in Fn_limits:
            ind_efd = (FR_efd >= Fn_low) & (FR_efd <= 0.20)
            if np.sum(ind_efd) >= 2:
                _, intercept, _, _, _ = stats.linregress(f_efd[ind_efd], c_efd[ind_efd])
                k_efd_list.append(intercept)
            else:
                k_efd_list.append(np.nan)
            
            ind_cfd = (Fr_cfd >= Fn_low) & (Fr_cfd <= 0.20)
            if np.sum(ind_cfd) >= 2:
                _, intercept, _, _, _ = stats.linregress(f_cfd[ind_cfd], c_cfd[ind_cfd])
                k_cfd_list.append(intercept)
            else:
                k_cfd_list.append(np.nan)
        
        k_efd_arr = np.array(k_efd_list)
        k_cfd_arr = np.array(k_cfd_list)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.scatter(Fn_limits, k_efd_arr, s=150, color=color_efd, marker='o',
                   zorder=3, edgecolors='black', linewidth=0.5, label='EFD')
        ax.scatter(Fn_limits, k_cfd_arr, s=150, color=color_cfd, marker='o',
                   zorder=3, edgecolors='black', linewidth=0.5, label='CFD')
        
        ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)
        ax.set_xlabel('Fr', fontsize=31)
        ax.set_ylabel('1+k', fontsize=31)
        x_margin = 0.005
        ax.set_xlim(min(Fn_limits) - x_margin, max(Fn_limits) + x_margin)
        ax.set_ylim(0, 1.5)
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_linewidth(1.5)
        ax.spines['left'].set_linewidth(1.5)
        ax.tick_params(labelsize=20)
        ax.legend(fontsize=20, loc='upper center', framealpha=0.95, ncol=2, bbox_to_anchor=(0.5, 1.15))
        
        plt.subplots_adjust(top=0.85)
        num = calado['name'].replace('m', '').replace('0.', '')
        filename = f'comparacion_1k_range_{num}.pdf'
        plt.savefig(f'{OUTPUT_DIR}/{filename}', format='pdf', bbox_inches='tight', pad_inches=0.1)
        plt.close()
        print(f"✓ {filename}")


# ============================================================================
# 7. FORM FACTOR RANGE KCS
# ============================================================================

def generar_form_factor_range_kcs():
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
    plt.savefig(f'{OUTPUT_DIR}/kcs_efd_form_factor_range.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("✓ kcs_efd_form_factor_range.pdf")


# ============================================================================
# 8. PROHASKA KCS (RTM-FR)
# ============================================================================

def generar_prohaska_kcs():
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
    
    g_local, dens_local, visc_local = 9.807, 998, 9.869e-7
    Lows, sup, LFr = 2.9114, 1.527, 2.9114
    Fr_min, Fr_max = 0.1, 0.2
    
    FR1 = V1 / np.sqrt(g_local * LFr)
    REY1 = V1 * Lows / visc_local
    CFM1 = 0.075 / (np.log10(REY1) - 2)**2
    CTM1 = RTM1 / (0.5 * dens_local * sup * V1**2)
    
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
    plt.savefig(f'{OUTPUT_DIR}/RTM-FR.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("✓ RTM-FR.pdf")


# ============================================================================
# 9. EFD KCS LITERATURA
# ============================================================================

def generar_efd_kcs_literatura():
    Re_KCS_EFD_Lit = np.array([2281465.895, 3337500.959, 6346048.446, 17949335.56,
                              6346048.446, 11713995.83, 17950187.62, 33132183.54])
    k_KCS_EFD_Lit = np.array([1.032903, 1.085161, 1.102581, 1.11807,
                             1.155769231, 1.123076923, 1.142307692, 1.121153846])
    Re_KCS_EFD_CE = np.array([2.28392E+06])
    k_KCS_EFD_CE = np.array([1.0563])
    
    tyellow, tred = '#e6e600', '#cc3333'
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
    plt.savefig(f'{OUTPUT_DIR}/efd_kcs_lit.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("✓ efd_kcs_lit.pdf")


# ============================================================================
# 10. CFD DB P1 (3 calados individuales - solo puntos azules)
# ============================================================================

def generar_cfd_db_p1_individual():
    data_str = """0.10	1.1660	1.1626	1.1792
0.16	1.2410	1.2348	1.2505
0.20	1.3036	1.3021	1.3199
0.24	1.3583	1.3575	1.3778
0.30	1.4430	1.4439	1.4701
0.36	1.5275	1.5522	1.5985
0.40	1.5595	1.5889	1.6366"""
    
    lines = data_str.strip().split('\n')
    Fn, T1, T2, T3 = [], [], [], []
    for line in lines:
        parts = line.split('\t')
        Fn.append(float(parts[0]))
        T1.append(float(parts[1]))
        T2.append(float(parts[2]))
        T3.append(float(parts[3]))
    
    Fn = np.array(Fn)
    tblue = '#1f77b4'
    
    calados = [
        {'name': 'T1: 0.165m', 'filename': 'tpa_CFD_DB_165.pdf', 'data': np.array(T1)},
        {'name': 'T2: 0.180m', 'filename': 'tpa_CFD_DB_180.pdf', 'data': np.array(T2)},
        {'name': 'T3: 0.195m', 'filename': 'tpa_CFD_DB_195.pdf', 'data': np.array(T3)}
    ]
    
    for calado in calados:
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.scatter(Fn, calado['data'], s=150, color=tblue, marker='o',
                   label='CFD - DB LabHiNO', zorder=3)
        
        ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)
        ax.set_xlabel('Fr', fontsize=31)
        ax.set_ylabel('1+k', fontsize=31)
        x_margin = 0.01
        ax.set_xlim(min(Fn) - x_margin, max(Fn) + x_margin)
        ax.set_ylim(1.0, 2.0)
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_linewidth(1.5)
        ax.spines['left'].set_linewidth(1.5)
        ax.tick_params(labelsize=20)
        ax.legend(fontsize=20, loc='upper left', framealpha=0.95)
        
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/{calado["filename"]}', format='pdf', bbox_inches='tight', pad_inches=0.1)
        plt.close()
        print(f"✓ {calado['filename']}")


# ============================================================================
# 11. CFD DB P1 + EFD (línea horizontal) - 3 calados individuales
# ============================================================================

def generar_cfd_db_prohaska_combinado():
    data_str = """0.10	1.1660	1.1626	1.1792
0.16	1.2410	1.2348	1.2505
0.20	1.3036	1.3021	1.3199
0.24	1.3583	1.3575	1.3778
0.30	1.4430	1.4439	1.4701
0.36	1.5275	1.5522	1.5985
0.40	1.5595	1.5889	1.6366"""
    
    lines = data_str.strip().split('\n')
    Fn, T1, T2, T3 = [], [], [], []
    for line in lines:
        parts = line.split('\t')
        Fn.append(float(parts[0]))
        T1.append(float(parts[1]))
        T2.append(float(parts[2]))
        T3.append(float(parts[3]))
    
    Fn = np.array(Fn)
    color_cfd = '#1f77b4'
    color_efd = '#a52a2a'
    
    calados = [
        {'name': 'T1', 'filename': 'tpa_CFD_DB_prohaska_165.pdf', 'data': np.array(T1), 'efd': EFD_VALUES['T1']},
        {'name': 'T2', 'filename': 'tpa_CFD_DB_prohaska_180.pdf', 'data': np.array(T2), 'efd': EFD_VALUES['T2']},
        {'name': 'T3', 'filename': 'tpa_CFD_DB_prohaska_195.pdf', 'data': np.array(T3), 'efd': EFD_VALUES['T3']}
    ]
    
    for calado in calados:
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.scatter(Fn, calado['data'], s=150, color=color_cfd, marker='o',
                   label='CFD - DB LabHiNO', zorder=3)
        ax.plot([Fn.min(), Fn.max()], [calado['efd'], calado['efd']],
                'o-', color=color_efd, markersize=10, linewidth=2,
                label='EFD - LabHiNO', zorder=2)
        
        ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)
        ax.set_xlabel('Fr', fontsize=31)
        ax.set_ylabel('1+k', fontsize=31)
        x_margin = 0.01
        ax.set_xlim(min(Fn) - x_margin, max(Fn) + x_margin)
        ax.set_ylim(1.0, 2.0)
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_linewidth(1.5)
        ax.spines['left'].set_linewidth(1.5)
        ax.tick_params(labelsize=20)
        ax.legend(fontsize=20, loc='upper left', framealpha=0.95)
        
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/{calado["filename"]}', format='pdf', bbox_inches='tight', pad_inches=0.1)
        plt.close()
        print(f"✓ {calado['filename']}")


# ============================================================================
# 12. KCS DB PROHASKA
# ============================================================================

def generar_kcs_db_prohaska():
    Re_1_79 = np.array([2.8549E+05, 5.7098E+05, 8.5647E+05, 1.1420E+06, 1.4274E+06, 1.71E+06, 2.00E+06, 2.2839E+06, 2.5694E+06, 2.8549E+06,
                        3.1404E+06, 3.43E+06, 3.7114E+06, 3.9969E+06, 4.28E+06, 4.57E+06, 4.8533E+06, 5.1388E+06, 5.4243E+06, 5.71E+06])
    y_1_79 = np.array([1.00, 1.01, 1.02, 1.09, 1.14, 1.20, 1.297, 1.301, 1.28, 1.25,
                       1.21, 1.18, 1.15, 1.13, 1.11, 1.11, 1.11, 1.11, 1.11, 1.11])

    Re_Terziev = np.array([3.78E+05, 7.55E+05, 1.13E+06, 1.51E+06, 1.89E+06, 2.27E+06, 2.64E+06, 3.02E+06, 3.40E+06, 3.78E+06,
                           4.15E+06, 4.53E+06, 4.91E+06, 5.29E+06])
    y_Terziev = np.array([1.120, 1.240, 1.255, 1.200, 1.180, 1.160, 1.140, 1.125, 1.115, 1.110,
                          1.105, 1.100, 1.095, 1.090])

    y_Prohaska = 1.0563
    tblue, tred = '#3333cc', '#cc3333'
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(Re_1_79, y_1_79, s=150, color=tblue, marker='o', label='CFD - DB LabHiNO', zorder=3)
    ax.scatter(Re_Terziev, y_Terziev, s=150, color=tred, marker='o', label='CFD - DB Data Set', zorder=3)
    
    Re_min = min(Re_1_79.min(), Re_Terziev.min())
    Re_max = max(Re_1_79.max(), Re_Terziev.max())
    ax.plot([Re_min, Re_max], [y_Prohaska, y_Prohaska], 'k-', linewidth=2, label='EFD LabHiNO', zorder=2)
    
    ax.axvline(x=1.427E+06, color='black', linestyle=':', linewidth=2, alpha=0.5, zorder=1)
    ax.axvline(x=2.854E+06, color='black', linestyle=':', linewidth=2, alpha=0.5, zorder=1)
    ax.text(1.427E+06 - 0.15e6, 1.32, 'Fr = 0.1', fontsize=18, ha='right')
    ax.text(2.854E+06 + 0.15e6, 1.32, 'Fr = 0.2', fontsize=18, ha='left')
    
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
    plt.savefig(f'{OUTPUT_DIR}/kcs_DB_prohaska.pdf', format='pdf', bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print("✓ kcs_DB_prohaska.pdf")


# ============================================================================
# 13. COMPARACIÓN TOTAL KCS + TPA
# ============================================================================

def generar_comparacion_total_kcs_tpa():
    Re_KCS_1_79 = np.array([2.8549E+05, 5.7098E+05, 8.5647E+05, 1.1420E+06, 1.4274E+06, 1.7129E+06, 1.9984E+06, 2.2839E+06, 2.5694E+06, 2.8549E+06,
                            3.1404E+06, 3.4259E+06, 3.7114E+06, 3.9969E+06, 4.2823E+06, 4.5678E+06, 4.8533E+06, 5.1388E+06, 5.4243E+06, 5.7098E+06])
    y_KCS_1_79 = np.array([0.998, 1.010, 1.025, 1.090, 1.144, 1.203, 1.297, 1.301, 1.283, 1.253,
                           1.215, 1.182, 1.153, 1.129, 1.114, 1.114, 1.113, 1.109, 1.114, 1.113])

    Re_Terziev = np.array([3.78E+05, 7.55E+05, 1.13E+06, 1.51E+06, 1.89E+06, 2.27E+06, 2.64E+06, 3.02E+06, 3.40E+06, 3.78E+06,
                           4.15E+06, 4.53E+06, 4.91E+06, 5.29E+06])
    y_Terziev = np.array([1.120, 1.240, 1.255, 1.200, 1.180, 1.160, 1.140, 1.125, 1.115, 1.110, 1.105, 1.100, 1.095, 1.090])

    Re_TPA_1_20 = np.array([6.41E+05, 1.03E+06, 1.28E+06, 1.54E+06, 1.92E+06, 2.31E+06, 2.56E+06])
    y_TPA_1_20 = np.array([1.1792, 1.2505, 1.3199, 1.3778, 1.4701, 1.5985, 1.6366])

    Re_Prohaska_1_79 = np.array([2.3875E+05, 6E+06])
    y_Prohaska_1_79 = np.array([1.0563, 1.0563])
    Re_Prohaska_TPA = np.array([2.3875E+05, 6E+06])
    y_Prohaska_TPA = np.array([1.19, 1.19])

    color_kcs_labhino = '#1f77b4'
    color_kcs_dataset = '#d62728'
    color_tpa_cfd = '#2ca02c'
    color_kcs_efd = '#e6b800'
    color_tpa_efd = '#8033b3'

    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.scatter(Re_KCS_1_79, y_KCS_1_79, s=150, color=color_kcs_labhino, marker='o',
               label='CFD DB - KCS LabHiNO', zorder=3)
    ax.scatter(Re_Terziev, y_Terziev, s=150, color=color_kcs_dataset, marker='o',
               label='CFD DB - KCS Data Set', zorder=3)
    ax.scatter(Re_TPA_1_20, y_TPA_1_20, s=150, color=color_tpa_cfd, marker='o',
               label='CFD DB - P1', zorder=3)
    
    ax.plot(Re_Prohaska_1_79, y_Prohaska_1_79, 'o-', color=color_kcs_efd,
            markersize=10, linewidth=2, label='EFD - KCS LabHiNO', zorder=2,
            markeredgecolor='black', markeredgewidth=0.5)
    ax.plot(Re_Prohaska_TPA, y_Prohaska_TPA, 'o-', color=color_tpa_efd,
            markersize=10, linewidth=2, label='EFD - P1', zorder=2,
            markeredgecolor='black', markeredgewidth=0.5)
    
    ax.axvline(x=6.40489E+05, color='black', linestyle=':', linewidth=2, alpha=0.5, zorder=1)
    ax.axvline(x=1.28098E+06, color='black', linestyle=':', linewidth=2, alpha=0.5, zorder=1)
    ax.text(6.40489E+05 - 0.05e6, 1.68, 'Fr = 0.1', fontsize=18, ha='right')
    ax.text(1.28098E+06 + 0.05e6, 1.68, 'Fr = 0.2', fontsize=18, ha='left')
    
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    
    def format_re(x, pos):
        if x == 0:
            return '0'
        return f'{x/1e6:.1f}'
    
    ax.xaxis.set_major_formatter(FuncFormatter(format_re))
    ax.set_xlabel('Re (×10$^6$)', fontsize=31)
    ax.set_ylabel('1+k', fontsize=31)
    ax.set_ylim(0.95, 1.7)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.tick_params(labelsize=20)
    ax.legend(fontsize=18, loc='upper right', framealpha=0.95)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/comparacion_total_kcs_tpa.pdf', format='pdf', bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print("✓ comparacion_total_kcs_tpa.pdf")


# ============================================================================
# 14. CFD LITERATURA vs LabHiNO
# ============================================================================

def generar_cfd_lit_kcs():
    # Datos de literatura CFD KCS (Data Set completo)
    # NOTA: Estos datos vienen del archivo CSV que subiste
    # Aquí los incluyo hardcoded para no depender del CSV externo
    Re_DataSet = np.array([
        1683412, 2281466, 2539580, 3337501, 4908933, 4908933, 4908933, 5318602,
        5509649, 5542389, 5672215, 5815769, 5826207, 6197898, 6217842, 6346048,
        6346048, 6570522, 6657041, 6800560, 7001148, 7330000, 7330000, 7330000,
        7330000, 8342018, 8342018, 8342018, 11713996, 12600000, 12600000,
        12600000, 12600000, 13519243, 14000000, 14000000, 15757198, 17006945,
        17949336, 17950188, 17950188, 17950188, 17950188, 24709112, 30722983,
        33132184, 44798245, 73968637, 90462839, 123719171, 215000000, 351736955,
        1029449389, 2400000000, 2560000000, 2580000000, 2580000000, 2761696821,
        3188445519, 3188445519, 3188445519
    ])
    k_DataSet = np.array([
        1.036751, 1.048387, 1.058141, 1.075484, 1.110615778, 1.1124, 1.1124,
        1.204, 1.2049, 1.084091, 1.2057, 1.2064, 1.2064, 1.2082, 1.2082,
        1.154839, 1.167307692, 1.21, 1.2104, 1.211, 1.212, 1.088, 1.117,
        1.169, 1.158, 1.105002159, 1.105, 1.1135, 1.15, 1.06, 1.132, 1.169,
        1.159, 1.119214, 1.108, 1.116, 1.115909, 1.10181, 1.170323,
        1.142307692, 1.191442928, 1.1941, 1.1172, 1.128866, 1.103167,
        1.136538462, 1.140909, 1.134831, 1.111312, 1.165909, 1.133026,
        1.181818, 1.190909, 1.10873, 1.158824, 1.12, 1.28, 1.195455,
        1.113198963, 1.133, 1.1599
    ])
    
    # Datos KCS 1:79 (LabHiNO)
    Re_KCS_1_79 = np.array([2.8549E+05, 5.7098E+05, 8.5647E+05, 1.1420E+06, 1.4274E+06, 1.7129E+06, 1.9984E+06, 2.2839E+06, 2.5694E+06, 2.8549E+06,
                            3.1404E+06, 3.4259E+06, 3.7114E+06, 3.9969E+06, 4.2823E+06, 4.5678E+06, 4.8533E+06, 5.1388E+06, 5.4243E+06, 5.7098E+06])
    y_KCS_1_79 = np.array([0.998, 1.010, 1.025, 1.090, 1.144, 1.203, 1.297, 1.301, 1.283, 1.253,
                           1.215, 1.182, 1.153, 1.129, 1.114, 1.114, 1.113, 1.109, 1.114, 1.113])
    
    tblue = '#3333cc'
    tyellow = '#e6b800'
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(Re_DataSet, k_DataSet, s=150, color=tyellow, marker='o',
               label='CFD - DB Data Set', zorder=3, edgecolors='black', linewidth=1)
    ax.scatter(Re_KCS_1_79, y_KCS_1_79, s=150, color=tblue, marker='o',
               label='CFD - DB LabHiNO', zorder=3)
    
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xscale('log')
    ax.set_xlabel('Re', fontsize=31)
    ax.set_ylabel('1+k', fontsize=31)
    ax.set_ylim(0.95, 1.35)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.tick_params(labelsize=20)
    ax.legend(fontsize=20, loc='upper right', framealpha=0.95)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/cfd_lit_kcs_comparacion.pdf', format='pdf', bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print("✓ cfd_lit_kcs_comparacion.pdf")


# ============================================================================
# EJECUTAR TODOS
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("GENERANDO TODOS LOS GRÁFICOS DE LA TESIS")
    print(f"Salida en: {OUTPUT_DIR}/")
    print("=" * 70)
    print()
    
    print("--- Prohaska P1 (EFD y CFD) ---")
    generar_prohaska_tpa_efd()
    generar_prohaska_tpa_cfd()
    
    print("\n--- Sensibilidad al rango de Froude ---")
    generar_form_factor_range_tpa()
    generar_cfd_form_factor_195_range()
    
    print("\n--- Comparación EFD vs CFD por calado ---")
    generar_prohaska_efd_cfd_comparacion()
    generar_comparacion_range_efd_cfd()
    
    print("\n--- KCS ---")
    generar_prohaska_kcs()
    generar_form_factor_range_kcs()
    generar_efd_kcs_literatura()
    generar_kcs_db_prohaska()
    generar_cfd_lit_kcs()
    
    print("\n--- CFD DB P1 ---")
    generar_cfd_db_p1_individual()
    generar_cfd_db_prohaska_combinado()
    
    print("\n--- Comparación total ---")
    generar_comparacion_total_kcs_tpa()
    
    print("\n" + "=" * 70)
    print(f"✓ COMPLETADO. Archivos en: {OUTPUT_DIR}/")
    print("=" * 70)
