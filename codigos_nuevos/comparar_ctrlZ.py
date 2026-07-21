"""
Descomposicion de resistencia P1 con y sin bulbo (Ctrl+Z).

Usa UNICAMENTE la resistencia total de CFD (RTM) y el factor de forma
obtenido por Prohaska:

    CT = RTM / (0.5 rho V^2 S)
    CF0 = 0.075 / (log10(Re) - 2)^2        (ITTC-57)
    CV = (1+k) * CF0
    CW = CT - CV

Las columnas Rp / Rv del CSV (fuerzas normal y tangencial de OpenFOAM)
NO se usan: no corresponden a CW y CV.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Propiedades del fluido.
# La columna ReM de datos_195.csv (primeras filas, las unicas coherentes)
# implica nu = v*L/Re = 9.29e-7 m2/s, o sea agua dulce a ~23.5 C.
# VERIFICAR contra la temperatura registrada en el ensayo.
RHO = 998.87      # kg/m3
NU  = 1.09e-6    # m2/s
G   = 9.81       # m/s2

# Directorio de salida (poner la ruta a images/ de la tesis si se quiere
# sobrescribir directamente las figuras del .tex)
OUTDIR = "."
# ----------------------------------------------------------------------

CASOS = {
    "165": {
        "archivo": "datos_165.csv",
        "titulo": r"$T = 0.165$ m",
        "bulbo":  {"L": 1.634, "S": 0.982, "k1": 1.204, "label": "Con bulbo"},
        "ctrlz":  {"L": 1.515, "S": 0.969, "k1": 1.169, "label": "Sin bulbo (Ctrl+Z)"},
    },
    "195": {
        "archivo": "datos_195.csv",
        "titulo": r"$T = 0.195$ m",
        "bulbo":  {"L": 1.641, "S": 1.124, "k1": 1.196, "label": "Con bulbo"},
        "ctrlz":  {"L": 1.575, "S": 1.122, "k1": 1.204, "label": "Sin bulbo (Ctrl+Z)"},
    },
}


def a_float(v):
    """Convierte a float tolerando coma decimal y celdas vacias."""
    if isinstance(v, str):
        v = v.strip().replace(",", ".")
    try:
        return float(v)
    except (TypeError, ValueError):
        return np.nan


def cf_ittc57(Re):
    return 0.075 / (np.log10(Re) - 2.0) ** 2


def procesar(calado):
    cfg = CASOS[calado]

    # skiprows=1 -> descarta la fila de unidades. Se toman las columnas por
    # posicion porque los encabezados difieren entre los dos archivos.
    df = pd.read_csv(cfg["archivo"], skiprows=1, header=None,
                     usecols=[0, 3, 6],
                     names=["vM", "RT_bulbo", "RT_ctrlz"])

    for c in df.columns:
        df[c] = df[c].map(a_float)
    df = df.dropna().reset_index(drop=True)

    out = pd.DataFrame({"vM": df["vM"]})

    for cfg_key, rt_col in (("bulbo", "RT_bulbo"), ("ctrlz", "RT_ctrlz")):
        p = cfg[cfg_key]
        v = df["vM"].to_numpy()

        # Fr y Re se recalculan a partir de vM y la eslora de cada casco.
        # La columna Fr de datos_195.csv esta corrida una fila y no se usa.
        Fr = v / np.sqrt(G * p["L"])
        Re = v * p["L"] / NU
        CF0 = cf_ittc57(Re)

        CT = df[rt_col].to_numpy() / (0.5 * RHO * v**2 * p["S"])
        CV = p["k1"] * CF0
        CW = CT - CV

        s = "_" + cfg_key
        out["Fr" + s] = Fr
        out["Re" + s] = Re
        out["CF0" + s] = CF0
        out["CT" + s] = CT
        out["CV" + s] = CV
        out["CW" + s] = CW

    return out, cfg


def figura(res, cfg, coef, ylabel, nombre):
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    for key, st in (("bulbo", "o-"), ("ctrlz", "s--")):
        ax.plot(res["Fr_" + key], res[coef + "_" + key], st,
                lw=1.8, ms=6, label=cfg[key]["label"])
    ax.set_xlabel(r"$F_n$ [-]")
    ax.set_ylabel(ylabel)
    ax.set_title(f"{ylabel.strip('$')} — {cfg['titulo']}", fontsize=11)
    ax.legend(frameon=False)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    ruta = f"{OUTDIR}/{nombre}"
    fig.savefig(ruta, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  {ruta}")


for calado in ("165", "195"):
    res, cfg = procesar(calado)

    print(f"\nCalado {calado}  ({len(res)} puntos)")
    figura(res, cfg, "CT", r"$C_T$", f"Ct-consinbulbo-{calado}.png")
    figura(res, cfg, "CW", r"$C_W$", f"Cw-consinbulbo-{calado}.png")
    figura(res, cfg, "CV", r"$C_V$", f"Cv-consinbulbo-{calado}.png")

    res.to_csv(f"{OUTDIR}/coeficientes_{calado}.csv", index=False)
    print(f"  coeficientes_{calado}.csv")

    # control rapido: CW no deberia ser negativo a bajo Fn
    for key in ("bulbo", "ctrlz"):
        neg = (res["CW_" + key] < 0).sum()
        if neg:
            print(f"  AVISO: {neg} valores de CW negativos en {key}")

print("\nListo.")
