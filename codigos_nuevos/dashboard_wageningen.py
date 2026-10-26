"""
dashboard.py
============
Genera las 5 figuras del Cap. 5 (efectos de escala B4-60), estilo tesis (fondo blanco).

Colocar en ~/soyuela/surfaces/
Los perfiles radiales deben estar en radial_profiles_D05_D2_D8.png
Uso: python3 dashboard.py

CAMBIOS RESPECTO DE LA VERSIÓN ANTERIOR (correcciones punto 11, Cap. 5)
-----------------------------------------------------------------------
1. Los coeficientes del sweep estaban multiplicados por 4 (0.74475 = 4 x 0.1862).
   Para el CFD no importaba (eta0 es un cociente), pero la corrección ITTC,
   calculada para la hélice completa, quedaba diluida por 4. Ahora se dividen
   explícitamente por FACTOR_SWEEP = 4.
2. La geometría de la sección usada en el ITTC era la de la P206
   (c/D = 0.23, t/c = 0.05). Se reemplaza por la de la B4-60.
3. La sección representativa pasa de 0.7R a 0.75R, como en la definición del
   ITTC-78 del capítulo de metodología.
4. Extrapolación LISA: C_DS se evalúa con la misma ley de fricción lisa que
   C_DM, al Reynolds de cada escala (sin la expresión rugosa con k_p = 30 um),
   para comparar contra un CFD de superficie lisa.

Verificación esperada a D = 8 m:
   Kt_ITTC = 0.1875 | 10Kq_ITTC = 0.2566 | eta0_ITTC = 0.582 (+6.1 %)
   eta0_CFD = 0.598 (+9.1 %)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from pathlib import Path

plt.rcParams.update({
    'font.family': 'serif', 'font.serif': ['DejaVu Serif'],
    'mathtext.fontset': 'dejavuserif',
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'grid.linestyle': '--', 'grid.color': '#cccccc', 'grid.linewidth': 0.7,
    'legend.framealpha': 1.0, 'legend.edgecolor': '#aaaaaa',
    'savefig.dpi': 220, 'figure.facecolor': 'white', 'axes.facecolor': 'white',
})

# ══════════════════════════════════════════════════════════════════════
# DATOS
# ══════════════════════════════════════════════════════════════════════
J=0.5; rho=998.8; nu=1.04e-6; Z=4; PD=0.81; AeA0=0.60

# Coeficientes tal como salen del post-proceso (multiplicados por 4)
sweep = [
    ('D=0.14', 0.14, 17.00, 0.74475, 0.75861,-0.01385, 0.10810, 0.09535, 0.01275),
    ('D=0.50', 0.50, 10.00, 0.75235, 0.76385,-0.01150, 0.10594, 0.09578, 0.01016),
    ('D=1.0',  1.00, 10.00, 0.76413, 0.77223,-0.00810, 0.10396, 0.09670, 0.00726),
    ('D=2.0',  2.00,  5.00, 0.77356, 0.78068,-0.00712, 0.10431, 0.09791, 0.00640),
    ('D=4.0',  4.00,  2.50, 0.77678, 0.78315,-0.00637, 0.10397, 0.09824, 0.00573),
    ('D=8.0',  8.00,  1.25, 0.77973, 0.78549,-0.00575, 0.10373, 0.09856, 0.00517),
]
FACTOR_SWEEP = 4.0   # [CORREGIDO] los valores de 'sweep' están multiplicados por 4

labels = [s[0] for s in sweep]
D_arr  = np.array([s[1] for s in sweep])
n_arr  = np.array([s[2] for s in sweep])
Re_arr = n_arr * D_arr**2 / nu
Kt  = np.array([s[3] for s in sweep]) / FACTOR_SWEEP
Ktp = np.array([s[4] for s in sweep]) / FACTOR_SWEEP
Ktf = np.array([s[5] for s in sweep]) / FACTOR_SWEEP
Kq  = np.array([s[6] for s in sweep]) / FACTOR_SWEEP
Kqp = np.array([s[7] for s in sweep]) / FACTOR_SWEEP
Kqf = np.array([s[8] for s in sweep]) / FACTOR_SWEEP

dKtp = Ktp - Ktp[0]; dKtf = Ktf - Ktf[0]; dKt = Kt - Kt[0]
dKqp = Kqp - Kqp[0]; dKqf = Kqf - Kqf[0]; dKq = Kq - Kq[0]

# ── Corrección ITTC-78, extrapolación LISA ───────────────────────────
# [CORREGIDO] Geometría de la B4-60 a r/R = 0.75 (serie Wageningen B):
#   c·Z/(D·Ae/A0) = 2.144 (0.7R) y 1.970 (0.8R)  ->  2.057 a 0.75R
#   c/D = 2.057 · 0.60 / 4 = 0.3086
#   t/c ≈ 0.033 (efecto despreciable sobre el resultado)
rR_ittc = 0.75
cD_075  = 0.3086
tc_075  = 0.033

def CD_liso(Re):
    """Arrastre de sección con ley de fricción lisa (misma forma que C_DM del ITTC-78)."""
    return 2*(1+2*tc_075)*(0.044/Re**(1/6) - 5/Re**(2/3))

# Reynolds de sección a 0.75R: V_R = sqrt(Va^2 + (0.75·pi·n·D)^2)
Re_c = np.sqrt((J*n_arr*D_arr)**2 + (rR_ittc*np.pi*n_arr*D_arr)**2) * cD_075*D_arr / nu

CD_sec   = CD_liso(Re_c)            # C_DM en el modelo, C_DS (liso) en cada escala
dCD      = CD_sec[0] - CD_sec       # ΔC_D = C_DM − C_DS
dKt_ittc =  0.3  * dCD * PD * cD_075 * Z    # K_TS = K_TM + 0.3·ΔC_D·P/D·cZ/D
dKq_ittc = -0.25 * dCD * cD_075 * Z         # K_QS = K_QM − 0.25·ΔC_D·cZ/D
Kt_ittc  = Kt[0] + dKt_ittc
Kq_ittc  = Kq[0] + dKq_ittc
ITTC_LBL = 'ITTC-78 (liso)'

r_R    = np.array([0.3,    0.4,    0.5,    0.6,    0.7,    0.8,    0.9  ])
Cl_014 = np.array([0.2570, 0.2441, 0.2217, 0.2043, 0.1836, 0.1621, 0.1516])
Cl_05  = np.array([0.2575, 0.2444, 0.2172, 0.2028, 0.1821, 0.1631, 0.1517])
Cl_1   = np.array([0.2566, 0.2456, 0.2232, 0.2076, 0.1870, 0.1652, 0.1538])
Cl_2   = np.array([0.2575, 0.2458, 0.2216, 0.2069, 0.1871, 0.1661, 0.1541])
Cl_4   = np.array([0.2590, 0.2470, 0.2230, 0.2089, 0.1879, 0.1657, 0.1545])
Cl_8   = np.array([0.2594, 0.2471, 0.2229, 0.2086, 0.1878, 0.1667, 0.1547])
Cl_cases = [
    ('D=0.14m', Cl_014, '#94a3b8'),
    ('D=0.5m',  Cl_05,  '#16a34a'),
    ('D=1.0m',  Cl_1,   '#f59e0b'),
    ('D=2.0m',  Cl_2,   '#3b82f6'),
    ('D=4.0m',  Cl_4,   '#a78bfa'),
    ('D=8.0m',  Cl_8,   '#ef4444'),
]

# ── Verificación numérica ────────────────────────────────────────────
def eta0(Kt, Kq): return J*Kt/(2*np.pi*Kq)
eta_cfd  = eta0(Kt, Kq)
eta_ittc = eta0(Kt_ittc, Kq_ittc)

print("Verificación ITTC-78 liso (0.75R, B4-60):")
print(f"  Re_c modelo (D=0.14 m) = {Re_c[0]:.3e}")
print(f"  {'D [m]':>6} {'Kt CFD':>8} {'Kt ITTC':>8} {'10Kq CFD':>9} {'10Kq ITTC':>10}"
      f" {'eta CFD':>8} {'eta ITTC':>9} {'dEta CFD':>9} {'dEta ITTC':>10}")
for i in range(len(D_arr)):
    print(f"  {D_arr[i]:6.2f} {Kt[i]:8.4f} {Kt_ittc[i]:8.4f} {10*Kq[i]:9.4f} {10*Kq_ittc[i]:10.4f}"
          f" {eta_cfd[i]:8.4f} {eta_ittc[i]:9.4f}"
          f" {100*(eta_cfd[i]/eta_cfd[0]-1):8.2f}% {100*(eta_ittc[i]/eta_cfd[0]-1):9.2f}%")
print()


# ══════════════════════════════════════════════════════════════════════
# ESTILO (tesis)
# ══════════════════════════════════════════════════════════════════════
K='#1a1a1a'; BLUE='#1f6db5'; RED='#c0392b'; GREEN='#2a7f3e'; GRAY='#7f7f7f'
BAR_B='#3f82c4'; BAR_R='#c9524a'
lRe = np.log10(Re_arr[1:]); D_plot = D_arr[1:]
def save(name):
    plt.tight_layout(); plt.savefig(name, bbox_inches='tight'); plt.close(); print("Guardado:", name)

# FIG 1 — Kt vs Re
fig, ax = plt.subplots(figsize=(8,5))
ax.semilogx(Re_arr, Kt,      'o-',  color=K,     lw=1.8, ms=6, label=r'$K_T$ CFD total')
ax.semilogx(Re_arr, Ktp,     's--', color=BLUE,  lw=1.8, ms=6, label=r'$K_{Tp}$ (presión)')
ax.semilogx(Re_arr, Ktf,     '^--', color=RED,   lw=1.8, ms=6, label=r'$K_{Tf}$ (fricción)')
ax.semilogx(Re_arr, Kt_ittc, 'D:',  color=GREEN, lw=1.8, ms=6, label=r'$K_T$ '+ITTC_LBL)
ax.set_xlabel(r'$Re_n = nD^2/\nu$'); ax.set_ylabel(r'$K_T$')
ax.legend(loc='lower right'); save("fig1_Kt_Re.png")

# FIG 2 — ΔKT y ΔKQ [%] vs log10(Re)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13,4.8))
w=0.14
a1.bar(lRe-w/2-0.01, dKtp[1:]/Kt[0]*100, width=w, color=BAR_B, label=r'$\Delta K_{Tp}$ (presión)')
a1.bar(lRe+w/2+0.01, dKtf[1:]/Kt[0]*100, width=w, color=BAR_R, label=r'$\Delta K_{Tf}$ (fricción)')
a1.plot(lRe, dKt[1:]/Kt[0]*100,      'o-',  color=K,     lw=1.8, ms=6, label=r'$\Delta K_T$ total CFD')
a1.plot(lRe, dKt_ittc[1:]/Kt[0]*100, 'D--', color=GREEN, lw=1.8, ms=6, label=r'$\Delta K_T$ '+ITTC_LBL)
a1.axhline(0, color=GRAY, lw=0.8)
a1.set_xlabel(r'$\log_{10}(Re_n)$'); a1.set_ylabel(r'$\Delta K_T/K_{T,\mathrm{ref}}$ [%]')
a1.legend(loc='upper left')
a2.bar(lRe-w/2-0.01, dKqp[1:]/Kq[0]*100, width=w, color=BAR_B, label=r'$\Delta K_{Qp}$ (presión)')
a2.bar(lRe+w/2+0.01, dKqf[1:]/Kq[0]*100, width=w, color=BAR_R, label=r'$\Delta K_{Qf}$ (fricción)')
a2.plot(lRe, dKq[1:]/Kq[0]*100,      'o-',  color=K,     lw=1.8, ms=6, label=r'$\Delta K_Q$ total CFD')
a2.plot(lRe, dKq_ittc[1:]/Kq[0]*100, 'D--', color=GREEN, lw=1.8, ms=6, label=r'$\Delta K_Q$ '+ITTC_LBL)
a2.axhline(0, color=GRAY, lw=0.8)
a2.set_xlabel(r'$\log_{10}(Re_n)$'); a2.set_ylabel(r'$\Delta K_Q/K_{Q,\mathrm{ref}}$ [%]')
a2.legend(loc='lower left')
save("fig2_delta_descomp.png")

# FIG 2b — η0 (eje izq.) y Δη0 [%] (eje der.)
eta_nofix = np.full_like(eta_cfd, eta_cfd[0])
fig, ax = plt.subplots(figsize=(8,5))
ax.semilogx(Re_arr, eta_ittc,  'D--', color=GREEN, lw=1.8, ms=6, label='M1 — '+ITTC_LBL)
ax.semilogx(Re_arr, eta_cfd,   'o-',  color=K,     lw=1.8, ms=6, label='M2 — CFD')
ax.semilogx(Re_arr, eta_nofix, 's:',  color=GRAY,  lw=1.8, ms=6, label='M3 — Sin corrección')
ax.set_xlabel(r'$Re_n = nD^2/\nu$'); ax.set_ylabel(r'$\eta_0$')
e0=eta_cfd[0]
sec=ax.secondary_yaxis('right', functions=(lambda e:(e/e0-1)*100, lambda p:e0*(1+p/100)))
sec.set_ylabel(r'$\Delta\eta_0$ [%] respecto al modelo')
ax.legend(loc='upper left'); save("fig2b_eficiencia.png")

# FIG 3 — ΔKT y 10ΔKQ vs D
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13,4.8))
a1.plot(D_plot, dKtp[1:], 's-', color=BLUE, lw=1.8, ms=6, label=r'$\Delta K_{Tp}$ (presión)')
a1.plot(D_plot, dKtf[1:], '^-', color=RED,  lw=1.8, ms=6, label=r'$\Delta K_{Tf}$ (fricción)')
a1.plot(D_plot, dKt[1:],  'o-', color=K,    lw=2.2, ms=6, label=r'$\Delta K_T$ total CFD')
a1.plot(D_plot, dKt_ittc[1:], '--', color=GREEN, lw=1.8, label=ITTC_LBL)
a1.axhline(0, color=GRAY, lw=0.8)
a1.set_xlabel(r'$D$ [m]'); a1.set_ylabel(r'$\Delta K_T$  (ref. $D=0{,}14$ m)'); a1.legend(loc='center right')
a2.plot(D_plot, 10*dKqp[1:], 's-', color=BLUE, lw=1.8, ms=6, label=r'$10\,\Delta K_{Qp}$ (presión)')
a2.plot(D_plot, 10*dKqf[1:], '^-', color=RED,  lw=1.8, ms=6, label=r'$10\,\Delta K_{Qf}$ (fricción)')
a2.plot(D_plot, 10*dKq[1:],  'o-', color=K,    lw=2.2, ms=6, label=r'$10\,\Delta K_Q$ total CFD')
a2.plot(D_plot, 10*dKq_ittc[1:], '--', color=GREEN, lw=1.8, label=ITTC_LBL)
a2.axhline(0, color=GRAY, lw=0.8)
a2.set_xlabel(r'$D$ [m]'); a2.set_ylabel(r'$10\,\Delta K_Q$  (ref. $D=0{,}14$ m)'); a2.legend(loc='center right')
save("fig3_delta_vs_D.png")

# FIG 4 — brecha ITTC y fracción de presión
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13,4.8))
gap = Kt[1:] - Kt_ittc[1:]
x = np.arange(len(D_plot))
a1.bar(x, gap, width=0.6, color=BAR_B)
for xi, g in zip(x, gap):
    a1.text(xi, g + gap.max()*0.02, f'{g:.4f}', ha='center', va='bottom', fontsize=9)
a1.set_xticks(x)
a1.set_xticklabels([f'{d:g}' for d in D_plot])
a1.set_ylim(0, gap.max()*1.25)
a1.set_xlabel(r'$D$ [m]'); a1.set_ylabel(r'$K_{T,\mathrm{CFD}} - K_{T,\mathrm{ITTC}}$')
frac = dKtp[1:]/dKt[1:]*100
a2.plot(D_plot, frac, 'o-', color=K, lw=2.2, ms=6, label=r'B4-60  ($Z=4$, $P/D=0{,}81$, $A_E/A_0=0{,}60$)')
a2.plot([1,4,8], [71,77,79], 's--', color=BLUE, lw=1.8, ms=6, label=r'Gaggero (2026)  ($Z=4$, $P/D=1{,}4$, $A_E/A_0=0{,}70$)')
a2.plot([1,4,8], [89,91,92], '^--', color=RED,  lw=1.8, ms=6, label=r'Gaggero (2026)  ($Z=6$, $P/D=1{,}0$, $A_E/A_0=0{,}50$)')
a2.axhline(100, color=GRAY, lw=0.8, ls=':')
a2.set_ylim(0, 110); a2.set_xlabel(r'$D$ [m]'); a2.set_ylabel(r'$\Delta K_{Tp}/\Delta K_T$ [%]')
a2.legend(loc='lower right', fontsize=9)
save("fig4_gap_fraccion.png")
