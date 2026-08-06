"""
FORM FACTOR (1+k) vs Re
Modelos: KCS, P1 (ex TPA), P2 (ex JPA), P3 (ex CONTESSI)

Correspondencia de nomenclatura (confirmada):
    FV1 -> P1  (ex TPA)
    FV2 -> P3  (ex CONTESSI)
    FV3 -> P2  (ex JPA)

Los datos, colores y marcadores originales no cambian; solo se actualizan
las etiquetas (labels) y el orden de graficado, para que la leyenda
(3 columnas) quede ordenada igual que en la figura final:
    Fila 1: KCS CFD | P1 CFD | P2 CFD
    Fila 2: P3 CFD  | KCS EFD | P1 EFD
    Fila 3: P2 EFD  | P3 EFD
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Fishing vessel P1 (ex TPA) ---
Re_P1_CFD = np.array([6.40e5, 1.02e6, 1.28e6, 1.54e6, 1.81e6, 1.92e6, 2.31e6, 2.56e6,
                       2.90e6, 3.62e6, 4.35e6, 5.43e6, 6.52e6, 5.12e6, 7.25e6, 8.20e6,
                       1.02e7, 1.23e7, 1.54e7, 1.84e7, 2.05e7, 5.73e7, 9.17e7, 1.15e8,
                       1.37e8, 1.72e8])
k_P1_CFD = np.array([1.179, 1.251, 1.320, 1.378, 1.399, 1.470, 1.598, 1.637,
                      1.622, 1.570, 1.513, 1.465, 1.465, 1.489, 1.473, 1.484,
                      1.501, 1.522, 1.528, 1.548, 1.554, 1.654, 1.690, 1.713,
                      1.714, 1.727])

# --- Fishing vessel P2 (ex JPA) ---
Re_P3_CFD = np.array([6.41e5, 1.03e6, 1.28e6, 1.54e6, 1.92e6, 2.31e6, 2.69e6, 4.30e6,
                       5.38e6, 6.45e6, 8.07e6, 9.68e6, 2.98e7, 4.76e7, 7.14e7, 8.93e7])
k_P3_CFD = np.array([1.728, 1.796, 1.908, 2.131, 2.340, 2.473, 2.224, 2.102,
                      2.141, 2.202, 2.195, 2.163, 2.388, 2.490, 2.581, 2.704])

# --- Fishing vessel P3 (ex CONTESSI) ---
Re_P2_CFD = np.array([1.33e6, 2.66e6, 3.99e6, 7.52e6, 1.13e7, 4.21e7, 8.41e7, 1.26e8])
k_P2_CFD = np.array([1.856, 1.923, 2.063, 2.002, 2.082, 2.257, 2.474, 2.623])

# --- KCS CFD (Data Set / Literature) ---
Re_KCS_CFD_Lit = np.array([1683412, 2281466, 2539580, 3337501, 4908933, 4908933, 4908933,
    5318602, 5509649, 5542389, 5672215, 5815769, 5826207, 6197898, 6217842, 6346048,
    6346048, 6570522, 6657041, 6800560, 7001148, 7330000, 7330000, 7330000, 7330000,
    8342018, 8342018, 8342018, 11713996, 12600000, 12600000, 12600000, 12600000,
    13519243, 14000000, 14000000, 15757198, 17006945, 17949336, 17950188, 17950188,
    17950188, 17950188, 24709112, 30722983, 33132184, 44798245, 73968637, 90462839,
    123719171, 215000000, 351736955, 1029449389, 2400000000, 2560000000, 2580000000,
    2580000000, 2761696821, 3188445519, 3188445519, 3188445519])
k_KCS_CFD_Lit = np.array([1.036751, 1.048387, 1.058141, 1.075484, 1.110616, 1.1124, 1.1124,
    1.204, 1.2049, 1.084091, 1.2057, 1.2064, 1.2064, 1.2082, 1.2082, 1.154839,
    1.167308, 1.21, 1.2104, 1.211, 1.212, 1.088, 1.117, 1.169, 1.158, 1.105002,
    1.105, 1.1135, 1.15, 1.06, 1.132, 1.169, 1.159, 1.119214, 1.108, 1.116,
    1.115909, 1.10181, 1.170323, 1.142308, 1.191443, 1.1941, 1.1172, 1.128866,
    1.103167, 1.136538, 1.140909, 1.134831, 1.111312, 1.165909, 1.133026, 1.181818,
    1.190909, 1.10873, 1.158824, 1.12, 1.28, 1.195455, 1.113199, 1.133, 1.1599])

# --- Valores EFD (Prohaska) ---
Re_KCS_EFD_CE, k_KCS_EFD_CE = [2.2839e6], [1.0563]
Re_P1_EFD_CE, k_P1_EFD_CE = [1.02e6], [1.19]
Re_P2_EFD_CE, k_P2_EFD_CE = [1.02e6], [1.41]
Re_P3_EFD_CE, k_P3_EFD_CE = [1.5e6], [1.7]

x_p1, y_p1 = 2e9, 1.19
x_kcs, y_kcs = 2e9, 1.0563
x_p3, y_p3 = 2e9, 1.7
x_p2, y_p2 = 2e9, 1.4

fig, ax = plt.subplots(figsize=(9, 6))

# --- Colores suaves y diferenciables (idénticos al script original) ---
color_KCS_CFD_Lit = (0.3, 0.3, 0.7)   # azul mate
color_P1_CFD = (0.9, 0.6, 0.2)        # naranja mate  (ex TPA)
color_P2_CFD = (0.7, 0.6, 0.3)        # marrón claro  (ex JPA)
color_P3_CFD = (0.5, 0.7, 0.5)        # verde oliva claro (ex CONTESSI)
color_FV_EFD_P1 = (0.9, 0.9, 0.2)     # amarillo mate (EFD P1, ex TPA)
color_FV_EFD_KCS = (0.2, 0.6, 0.4)    # verde petróleo mate (EFD KCS)
color_FV_EFD_P2 = (0.3, 0.6, 0.8)     # celeste grisáceo mate (EFD P2, ex JPA)
color_FV_EFD_P3 = (0.5, 0.5, 0.8)     # lavanda mate fría (EFD P3, ex CONTESSI)

# --- Series principales (orden ajustado: KCS, P1, P2, P3) ---
ax.scatter(Re_KCS_CFD_Lit, k_KCS_CFD_Lit, s=30, marker='o',
           edgecolor=color_KCS_CFD_Lit, facecolor=color_KCS_CFD_Lit,
           label='CFD DB KCS Data Set', zorder=3)

ax.scatter(Re_P1_CFD, k_P1_CFD, s=35, marker='s',
           edgecolor=color_P1_CFD, facecolor=color_P1_CFD,
           label='CFD DB P1 LabHiNO', zorder=3)

ax.scatter(Re_P2_CFD, k_P2_CFD, s=35, marker='^',
           edgecolor=color_P3_CFD, facecolor=color_P3_CFD,
           label='CFD DB P2 LabHiNO', zorder=3)

ax.scatter(Re_P3_CFD, k_P3_CFD, s=35, marker='D',
           edgecolor=color_P2_CFD, facecolor=color_P2_CFD,
           label='CFD DB P3 LabHiNO', zorder=3)

# --- EFD (Prohaska) ---
ax.scatter(Re_KCS_EFD_CE, k_KCS_EFD_CE, s=100, marker='*',
           edgecolor=color_FV_EFD_KCS, facecolor=color_FV_EFD_KCS,
           label='EFD KCS LabHiNO', zorder=4)
ax.plot([5e5, x_kcs], [y_kcs, y_kcs], color=color_FV_EFD_KCS, linestyle='--', zorder=2)

ax.scatter(Re_P1_EFD_CE, k_P1_EFD_CE, s=100, marker='*',
           edgecolor=color_FV_EFD_P1, facecolor=color_FV_EFD_P1,
           label='EFD P1 LabHiNO', zorder=4)
ax.plot([5e5, x_p1], [y_p1, y_p1], color=color_FV_EFD_P1, linestyle='--', zorder=2)

ax.scatter(Re_P2_EFD_CE, k_P2_EFD_CE, s=100, marker='*',
           edgecolor=color_FV_EFD_P2, facecolor=color_FV_EFD_P2,
           label='EFD P2 LabHiNO', zorder=4)
ax.plot([5e5, x_p2], [y_p2, y_p2], color=color_FV_EFD_P2, linestyle='--', zorder=2)

ax.scatter(Re_P3_EFD_CE, k_P3_EFD_CE, s=100, marker='*',
           edgecolor=color_FV_EFD_P3, facecolor=color_FV_EFD_P3,
           label='EFD P3 LabHiNO', zorder=4)
ax.plot([5e5, x_p3], [y_p3, y_p3], color=color_FV_EFD_P3, linestyle='--', zorder=2)

# --- Ajustes de ejes y formato ---
ax.set_xscale('log')
ax.set_xlim(5e5, 5e8)
ax.set_ylim(1.0, 2.8)
ax.set_xlabel('Re', fontsize=14)
ax.set_ylabel('1 + k', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_axisbelow(True)

# --- Leyenda inferior, 3 columnas ---
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=11,
          framealpha=0.95)

plt.tight_layout()
plt.savefig('formfactor_vs_Re_FV_KCS.pdf', format='pdf', bbox_inches='tight')
plt.close()
print("✓ formfactor_vs_Re_FV_KCS.pdf")
