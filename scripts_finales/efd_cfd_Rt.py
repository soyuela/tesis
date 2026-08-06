"""
9 gráficos de resistencia (R_T vs Fr) - P1
EFD 165 / 180 / 195
CFD 165 / 180 / 195
EFD vs CFD 165 / 180 / 195

Formato estandarizado del proyecto:
- Títulos de ejes: 31pt
- Números de ejes: 20pt
- Leyenda: 20pt, loc='upper left', framealpha=0.95 (mismo formato en los 9)
- Solo puntos (sin línea de unión)
- Salida: PDF vectorial
"""

import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = './graficos_pdf'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================================
# DATOS EFD (vM, Fr, RTM)
# ============================================================================

EFD_T1 = """0.42,0.104,0.620
0.52,0.13,0.950
0.61,0.15,1.110
0.64,0.16,1.280
0.68,0.17,1.640
0.71,0.18,1.650
0.74,0.184,1.800
0.80,0.20,2.240
0.84,0.21,2.700
0.89,0.22,3.060
0.92,0.23,3.530
0.95,0.236,3.660
1.04,0.26,4.910
1.14,0.285,6.170
1.17,0.29,6.340
1.29,0.32,10.670
1.38,0.34,13.350
1.40,0.35,13.960
1.49,0.37,16.610
1.52,0.38,17.490
1.61,0.40,22.010
1.82,0.45,45.190"""

EFD_T2 = """0.45,0.11,0.521
0.50,0.12,0.700
0.59,0.15,1.06
0.65,0.16,1.350
0.74,0.18,1.824
0.80,0.20,2.347
0.85,0.21,2.781
0.88,0.22,3.040
0.93,0.23,3.416
0.96,0.24,3.795
1.07,0.26,4.811
1.18,0.29,7.162
1.30,0.32,11.022
1.42,0.35,15.070
1.61,0.399,22.440
1.82,0.450,42.786"""

EFD_T3 = """0.56,0.14,1.012
0.65,0.163,1.456
0.75,0.19,2.198
0.93,0.232,3.484
1.05,0.263,4.656
1.19,0.296,7.135
1.29,0.321,10.482
1.52,0.379,17.631
1.60,0.399,22.143
1.75,0.436,32.923
1.84,0.460,45.464"""

# ============================================================================
# DATOS CFD (vM, Fr, RTM)
# ============================================================================

CFD_T1 = """0.42,0.104,0.596
0.52,0.13,0.829
0.61,0.15,1.115
0.64,0.16,1.250
0.74,0.184,1.756
0.84,0.21,2.5
0.92,0.23,3.15
0.95,0.236,3.55
1.04,0.26,4.587
1.14,0.285,5.95
1.17,0.29,6.582
1.38,0.34,11.59
1.49,0.37,14.71
1.52,0.38,15.885
1.61,0.40,20.7
1.82,0.45,41.16"""

CFD_T2 = """0.45,0.11,0.776
0.50,0.12,0.908
0.59,0.15,1.229
0.65,0.16,1.487
0.74,0.18,1.997
0.80,0.20,2.403
0.85,0.21,2.771
0.88,0.22,3.043
0.93,0.23,3.511
0.96,0.24,3.744
1.07,0.26,4.764
1.18,0.29,6.871
1.30,0.32,10.5
1.42,0.35,13.76
1.61,0.399,21.6
1.82,0.450,43.26"""

CFD_T3 = """0.56,0.14,1.152
0.64,0.16,1.316
0.75,0.19,2.349
1.05,0.26,3.648
1.19,0.30,7.430
1.34,0.334,12.520
1.48,0.369,16.640
1.73,0.432,35.376
1.79,0.447,41.970"""

EFD_DATA = {'T1': EFD_T1, 'T2': EFD_T2, 'T3': EFD_T3}
CFD_DATA = {'T1': CFD_T1, 'T2': CFD_T2, 'T3': CFD_T3}
CALADOS_M = {'T1': '0.165m', 'T2': '0.180m', 'T3': '0.195m'}

COLOR_EFD = '#d62728'
COLOR_CFD = '#1f77b4'

# Formato de leyenda común a los 9 gráficos
LEGEND_KWARGS = dict(fontsize=20, loc='upper left', framealpha=0.95)


def cargar(data_dict):
    datos = {}
    for calado, txt in data_dict.items():
        arr = np.array([line.split(',') for line in txt.strip().split('\n')], dtype=float)
        V, Fr, RT = arr[:, 0], arr[:, 1], arr[:, 2]
        datos[calado] = {'V': V, 'Fr': Fr, 'RT': RT}
    return datos


def formatear_ejes(ax):
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel('Fr', fontsize=31)
    ax.set_ylabel('$R_T$ [N]', fontsize=31)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.tick_params(labelsize=20)


# ============================================================================
# 1-3. GRÁFICOS EFD INDIVIDUALES (165, 180, 195)
# ============================================================================

def generar_efd_individuales():
    datos = cargar(EFD_DATA)
    for calado_name in ['T1', 'T2', 'T3']:
        Fr = datos[calado_name]['Fr']
        RT = datos[calado_name]['RT']

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.scatter(Fr, RT, s=150, color=COLOR_EFD, marker='o', zorder=3,
                   edgecolors='black', linewidth=0.5,
                   label=f'EFD - {calado_name}: {CALADOS_M[calado_name]}')

        formatear_ejes(ax)
        ax.legend(**LEGEND_KWARGS)

        plt.tight_layout()
        num = CALADOS_M[calado_name].replace('m', '').replace('0.', '')
        filename = f'efd_{num}.pdf'
        plt.savefig(f'{OUTPUT_DIR}/{filename}', format='pdf', bbox_inches='tight', pad_inches=0.1)
        plt.close()
        print(f"✓ {filename}")


# ============================================================================
# 4-6. GRÁFICOS CFD INDIVIDUALES (165, 180, 195)
# ============================================================================

def generar_cfd_individuales():
    datos = cargar(CFD_DATA)
    for calado_name in ['T1', 'T2', 'T3']:
        Fr = datos[calado_name]['Fr']
        RT = datos[calado_name]['RT']

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.scatter(Fr, RT, s=150, color=COLOR_CFD, marker='o', zorder=3,
                   edgecolors='black', linewidth=0.5,
                   label=f'CFD - {calado_name}: {CALADOS_M[calado_name]}')

        formatear_ejes(ax)
        ax.legend(**LEGEND_KWARGS)

        plt.tight_layout()
        num = CALADOS_M[calado_name].replace('m', '').replace('0.', '')
        filename = f'cfd_{num}.pdf'
        plt.savefig(f'{OUTPUT_DIR}/{filename}', format='pdf', bbox_inches='tight', pad_inches=0.1)
        plt.close()
        print(f"✓ {filename}")


# ============================================================================
# 7-9. GRÁFICOS EFD vs CFD (165, 180, 195)
# ============================================================================

def generar_efd_vs_cfd():
    datos_efd = cargar(EFD_DATA)
    datos_cfd = cargar(CFD_DATA)

    for calado_name in ['T1', 'T2', 'T3']:
        Fr_efd = datos_efd[calado_name]['Fr']
        RT_efd = datos_efd[calado_name]['RT']
        Fr_cfd = datos_cfd[calado_name]['Fr']
        RT_cfd = datos_cfd[calado_name]['RT']

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.scatter(Fr_efd, RT_efd, s=150, color=COLOR_EFD, marker='o',
                   zorder=3, edgecolors='black', linewidth=0.5,
                   label=f'EFD - {calado_name}: {CALADOS_M[calado_name]}')
        ax.scatter(Fr_cfd, RT_cfd, s=150, color=COLOR_CFD, marker='o',
                   zorder=3, edgecolors='black', linewidth=0.5,
                   label=f'CFD - {calado_name}: {CALADOS_M[calado_name]}')

        formatear_ejes(ax)
        ax.legend(**LEGEND_KWARGS)

        plt.tight_layout()
        num = CALADOS_M[calado_name].replace('m', '').replace('0.', '')
        filename = f'efd_vs_cfd_{num}.pdf'
        plt.savefig(f'{OUTPUT_DIR}/{filename}', format='pdf', bbox_inches='tight', pad_inches=0.1)
        plt.close()
        print(f"✓ {filename}")


if __name__ == "__main__":
    print("=" * 70)
    print("GENERANDO 9 GRÁFICOS DE RESISTENCIA (EFD, CFD, EFD vs CFD) - P1")
    print(f"Salida en: {OUTPUT_DIR}/")
    print("=" * 70)
    print()
    generar_efd_individuales()
    generar_cfd_individuales()
    generar_efd_vs_cfd()
    print()
    print("=" * 70)
    print(f"✓ COMPLETADO. Archivos en: {OUTPUT_DIR}/")
    print("=" * 70)
