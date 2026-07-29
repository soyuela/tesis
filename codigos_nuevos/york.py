"""
Figuras del método de York para el factor de forma (1+k)
- 3 calados del P1 (T1: 0.165 m, T2: 0.180 m, T3: 0.195 m)
- KCS

Cada figura muestra, en el diagrama de Prohaska (C_TM/C_F0 vs Fr^4/C_F0):
  * los puntos experimentales (rojos los usados en el ajuste, grises los descartados)
  * la recta de York (regresión ponderada, error despreciable en el eje X)
  * el punto (1+k) extrapolado en la ordenada, con su barra de incertidumbre
  * las verticales Fr = 0.1 y Fr = 0.2 ubicadas en su x = Fr^4/C_F0 correcto

Incertidumbre de la coordenada vertical:
  - P1  : se propaga la incertidumbre combinada de la resistencia U_D
          (media de 4 repeticiones: 5.35 / 2.04 / 0.83 % en Fr = 0.14 / 0.26 / 0.37,
          interpolada linealmente en Fr).
  - KCS : se estima de la dispersión de las repeticiones disponibles a cada velocidad.

Formato estandarizado tesis: 31/20 pt, figsize (12, 8), colores mate.
"""

import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
from collections import defaultdict
from scipy import stats
import os

OUTPUT_DIR = './graficos_pdf'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================================
# CONSTANTES AMBIENTALES
# ============================================================================
g = 9.807          # m/s^2
visc = 9.869e-7    # m^2/s

# ============================================================================
# COLORES MATE
# ============================================================================
tred   = (0.8, 0.1, 0.1)
tblue  = (0.1, 0.1, 0.5)
tgreen = (0.1, 0.5, 0.1)
tgray  = (0.6, 0.6, 0.6)

# ============================================================================
# P1 - características por calado y datos EFD (velocidad [m/s], resistencia [N])
# ============================================================================
DENS_P1 = 997.96   # kg/m^3

CALADOS_P1 = {
    'T1': dict(nombre='0.165 m', Lows=1.670, sup=0.982, LFr=1.634, rango=(0.155, 0.20)),
    'T2': dict(nombre='0.180 m', Lows=1.740, sup=1.058, LFr=1.662, rango=(0.165, 0.20)),
    'T3': dict(nombre='0.195 m', Lows=1.740, sup=1.124, LFr=1.641, rango=(0.153, 0.20)),
}

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
0.96,3.928""",
}

# Incertidumbre combinada de la resistencia del P1 (media de 4 repeticiones):
# U_D (%) en funcion de Fr, interpolada linealmente.
FR_UD_REF = [0.14, 0.26, 0.37]
UD_REF    = [5.35, 2.04, 0.83]   # %

# ============================================================================
# KCS - características y datos crudos (dia, velocidad [m/s], resistencia [N])
# ============================================================================
DENS_KCS = 998.0   # kg/m^3
KCS = dict(nombre='KCS', Lows=2.9114, sup=1.527, LFr=2.9114, rango=(0.13, 0.20))

# (dia, V [m/s], N [Newton]) - todas las corridas con lectura de fuerza
KCS_DATA = [
    ('16', 0.493, 0.799), ('16', 0.507, 0.780), ('16', 0.546, 0.893),
    ('16', 0.525, 0.927), ('16', 0.522, 0.934), ('16', 0.633, 1.381),
    ('17', 0.750, 1.855), ('17', 0.755, 1.869), ('17', 0.747, 1.916),
    ('17', 0.741, 1.833), ('17', 0.749, 1.873), ('17', 0.977, 3.160),
    ('17', 0.964, 2.977), ('17', 1.005, 3.031), ('17', 0.534, 0.963),
    ('17', 0.639, 1.352),
    ('18', 0.539, 1.190), ('18', 0.540, 1.113), ('18', 0.540, 1.057),
    ('18', 0.538, 1.042), ('18', 0.543, 1.060), ('18', 0.642, 1.396),
    ('18', 0.641, 1.387), ('18', 0.650, 1.431), ('18', 0.644, 1.402),
    ('18', 0.641, 1.450),
    ('24', 0.568, 0.935), ('24', 0.810, 2.044), ('24', 0.748, 1.786),
    ('24', 0.648, 1.320), ('24', 0.915, 2.661), ('24', 0.658, 1.360),
    ('24', 0.566, 1.031), ('24', 0.522, 0.857), ('24', 0.567, 0.984),
    ('24', 0.738, 1.752), ('24', 1.176, 4.345), ('24', 1.070, 3.619),
    ('25', 0.552, 0.946), ('25', 0.811, 2.067), ('25', 0.736, 1.691),
    ('25', 0.648, 1.302), ('25', 0.915, 2.666), ('25', 0.568, 0.991),
    ('25', 0.563, 0.991), ('25', 0.563, 0.980), ('25', 0.852, 2.374),
    ('25', 0.814, 2.117),
]


# ============================================================================
# FUNCIONES DE CÁLCULO
# ============================================================================
def cf_ittc(Re):
    """Línea de fricción ITTC-57."""
    return 0.075 / (np.log10(Re) - 2)**2


def prohaska_vars(V, RTM, dens, Lows, sup, LFr):
    """Devuelve Fr y las variables de Prohaska X = Fr^4/C_F0, Y = C_TM/C_F0,
    junto con el coeficiente de fricción C_F0 y la presión dinámica q."""
    Fr = V / np.sqrt(g * LFr)
    Re = V * Lows / visc
    CTM = RTM / (0.5 * dens * sup * V**2)
    CF0 = cf_ittc(Re)
    X = Fr**4 / CF0
    Y = CTM / CF0
    q = 0.5 * dens * sup * V**2
    return Fr, X, Y, CF0, q


def york_error_en_Y(X, Y, sY):
    """Ajuste de York con error despreciable en X (regresión lineal ponderada
    por 1/sigma_Y^2). Devuelve ordenada (1+k), pendiente e incertidumbre de la
    ordenada (propagación directa, sin escalar por chi^2)."""
    w = 1.0 / sY**2
    Sw   = w.sum()
    Swx  = (w * X).sum()
    Swy  = (w * Y).sum()
    Swxx = (w * X**2).sum()
    Swxy = (w * X * Y).sum()
    D = Sw * Swxx - Swx**2
    b = (Sw * Swxy - Swx * Swy) / D          # pendiente
    a = (Swxx * Swy - Swx * Swxy) / D        # ordenada = (1+k)
    var_a = Swxx / D
    return a, b, np.sqrt(var_a)


def x_de_Fr(Fr_val, Lows, LFr):
    """Coordenada x = Fr^4/C_F0 correspondiente a un dado Fr (para las
    verticales Fr = 0.1 y Fr = 0.2)."""
    V = Fr_val * np.sqrt(g * LFr)
    Re = V * Lows / visc
    return Fr_val**4 / cf_ittc(Re)


# ============================================================================
# FIGURA
# ============================================================================
def figura_york(X, Y, sY, ind, a, b, ua, xFr01, xFr02, fname,
                xlim=(-0.01, 0.4), ylim=None, lbl_y=1.75, a_recta=None,
                visible=None):
    """Genera una figura de York.
    - xlim, ylim: límites de los ejes.
    - lbl_y: altura Y de las etiquetas Fr=0.1 / Fr=0.2.
    - a_recta: ordenada usada para dibujar la recta y el punto extrapolado
      (si difiere de 'a'; p.ej. valor adoptado por Prohaska). Por defecto usa 'a'.
    - visible: máscara booleana de puntos a mostrar (para filtro de dispersión).
      Los ocultos no se grafican; el cálculo del ajuste no se altera.
    """
    if a_recta is None:
        a_recta = a
    if visible is None:
        visible = np.ones(len(X), bool)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.grid(True, linestyle='--', color='gray', alpha=0.4, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    mask = np.zeros(len(X), bool)
    mask[ind] = True

    # puntos visibles fuera del ajuste (grises)
    vis_out = visible & ~mask
    vis_fit = visible & mask
    ax.errorbar(X[vis_out], Y[vis_out], yerr=sY[vis_out], fmt='o', color=tgray, alpha=0.4,
                markersize=9, capsize=4, markeredgecolor='black', markeredgewidth=0.5,
                zorder=2, label='Fuera del ajuste')
    # puntos del ajuste (rojos)
    ax.errorbar(X[vis_fit], Y[vis_fit], yerr=sY[vis_fit], fmt='o', color=tred,
                markersize=11, capsize=5, markeredgecolor='black', markeredgewidth=0.8,
                zorder=3, label='Puntos del ajuste')
    # recta de York (dibujada hasta el límite del eje)
    xr = np.array([0.0, xlim[1]])
    ax.plot(xr, a_recta + b * xr, '-', color=tblue, linewidth=2.5, zorder=4,
            label='Ajuste de York')
    # (1+k) extrapolado en la ordenada, con incertidumbre
    ax.errorbar([0], [a_recta], yerr=[ua], fmt='D', color=tgreen, markersize=13, capsize=6,
                capthick=2, elinewidth=2, markeredgecolor='black', markeredgewidth=1.0,
                zorder=5, label=r'$(1+k)$ extrapolado')

    # verticales Fr = 0.1 y Fr = 0.2 en su x correcto
    for xv, lbl in [(xFr01, 'Fr = 0.1'), (xFr02, 'Fr = 0.2')]:
        ax.axvline(x=xv, color='black', linestyle=':', linewidth=2, alpha=0.6, zorder=1)
        ax.text(xv, lbl_y, lbl, fontsize=17, ha='center', va='top',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85,
                          edgecolor='none'))

    ax.set_xlabel(r'$Fr^{4}/C_{F0}$', fontsize=31)
    ax.set_ylabel(r'$C_{TM}/C_{F0}$', fontsize=31)
    ax.tick_params(labelsize=20)
    for s in ('top', 'right', 'bottom', 'left'):
        ax.spines[s].set_linewidth(1.5)
    ax.set_xlim(*xlim)
    if ylim is not None:
        ax.set_ylim(*ylim)

    ax.text(0.30, 0.10, rf'$(1+k) = {a_recta:.3f} \pm {ua:.3f}$', fontsize=20,
            transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))
    ax.legend(fontsize=18, loc='lower right', framealpha=0.95)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/{fname}.pdf', format='pdf', bbox_inches='tight', pad_inches=0.1)
    plt.savefig(f'{OUTPUT_DIR}/{fname}.png', format='png', bbox_inches='tight', pad_inches=0.1, dpi=150)
    plt.close()
    print(f"\u2713 {fname}.pdf/png  ->  (1+k) = {a_recta:.3f} +/- {ua:.3f}  ({ua/a_recta*100:.1f}%)")


# ============================================================================
# GENERADORES
# ============================================================================
def generar_p1():
    fnames = {'T1': 'york_tpa_165', 'T2': 'york_tpa_180', 'T3': 'york_tpa_195'}
    for t, cal in CALADOS_P1.items():
        data = np.loadtxt(StringIO(EFD_DATA_P1[t]), delimiter=',')
        V, RTM = data[:, 0], data[:, 1]
        Fr, X, Y, CF0, q = prohaska_vars(V, RTM, DENS_P1, cal['Lows'], cal['sup'], cal['LFr'])
        # sigma_Y: propagar U_D(%) * RTM a la variable Y = C_TM/C_F0
        UD = np.interp(Fr, FR_UD_REF, UD_REF) / 100.0
        sY = (UD * RTM) / (q * CF0)
        fmin, fmax = cal['rango']
        ind = np.where((Fr > fmin) & (Fr < fmax))[0]
        a, b, ua = york_error_en_Y(X[ind], Y[ind], sY[ind])
        figura_york(X, Y, sY, ind, a, b, ua,
                    x_de_Fr(0.1, cal['Lows'], cal['LFr']),
                    x_de_Fr(0.2, cal['Lows'], cal['LFr']),
                    fnames[t],
                    xlim=(-0.01, 0.4), ylim=(0.5, 1.8), lbl_y=1.72)


def generar_kcs():
    """KCS: se ajusta sobre los 25 puntos promediados (los del diagrama de
    Prohaska). El valor de (1+k) adoptado es el de Prohaska (mínimos cuadrados
    simple); York aporta la incertidumbre. Los sigma provienen de la dispersión
    de las repeticiones crudas por velocidad. Un filtro de dispersión oculta los
    puntos de muy baja velocidad con residuo > 2.5 sigma respecto de la recta."""
    # 25 puntos promediados (V [m/s], R [N]) del diagrama de Prohaska del KCS
    prom = np.array([
        [0.566, 1.031], [0.650, 1.302], [0.652, 1.311], [0.650, 1.320],
        [0.650, 1.327], [0.658, 1.360], [0.738, 1.752], [0.750, 1.786],
        [0.749, 1.812], [0.810, 2.044], [0.810, 2.067], [0.815, 2.117],
        [0.852, 2.330], [0.860, 2.351], [0.852, 2.370], [0.909, 2.587],
        [0.915, 2.661], [0.915, 2.666], [0.963, 2.849], [0.957, 2.926],
        [0.971, 2.934], [0.968, 2.984], [1.056, 3.439], [1.067, 3.550],
        [1.070, 3.619],
    ])
    V, RTM = prom[:, 0], prom[:, 1]

    # sigma de la resistencia: dispersión de las repeticiones crudas por velocidad
    Vc = np.array([d[1] for d in KCS_DATA])
    Nc = np.array([d[2] for d in KCS_DATA])
    grupos = defaultdict(list)
    for v, n in zip(Vc, Nc):
        grupos[round(v, 2)].append(n)
    cvs = [np.std(x, ddof=1) / np.mean(x) for x in grupos.values() if len(x) > 1]
    cv_med = np.median(cvs)
    sigma_N = np.array([
        np.std(grupos[round(v, 2)], ddof=1) if len(grupos[round(v, 2)]) > 1 else cv_med * rtm
        for v, rtm in zip(V, RTM)
    ])

    Fr, X, Y, CF0, q = prohaska_vars(V, RTM, DENS_KCS, KCS['Lows'], KCS['sup'], KCS['LFr'])
    sY = sigma_N / (q * CF0)
    fmin, fmax = KCS['rango']
    ind = np.where((Fr >= fmin) & (Fr <= fmax))[0]

    # Valor adoptado = Prohaska (mínimos cuadrados simple sobre el rango)
    s_ls, i_ls, _, _, _ = stats.linregress(X[ind], Y[ind])
    a_prohaska = i_ls
    # York: para la pendiente de la recta y la incertidumbre de la ordenada
    a_york, b_york, ua = york_error_en_Y(X[ind], Y[ind], sY[ind])

    # Filtro de dispersión: ocultar puntos con residuo > 2.5 sigma respecto
    # de la recta de Prohaska (son los de muy baja velocidad, fuera del rango).
    resid = Y - (i_ls + s_ls * X)
    std_r = resid[ind].std()
    visible = np.abs(resid) <= 2.5 * std_r

    figura_york(X, Y, sY, ind, a_prohaska, b_york, ua,
                x_de_Fr(0.1, KCS['Lows'], KCS['LFr']),
                x_de_Fr(0.2, KCS['Lows'], KCS['LFr']),
                'york_kcs',
                xlim=(-0.01, 0.46), ylim=(0.5, 1.8), lbl_y=1.72,
                a_recta=a_prohaska, visible=visible)


# ============================================================================
if __name__ == "__main__":
    print("Generando figuras de York...")
    generar_p1()
    generar_kcs()
    print(f"Listo. Archivos en: {OUTPUT_DIR}/")
