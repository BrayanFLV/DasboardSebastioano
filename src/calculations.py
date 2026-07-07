import pandas as pd
import numpy as np

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]
MESES_ORDEN = {m: i + 1 for i, m in enumerate(MESES)}


def filtrar_ingreso(df, anios=None, meses=None, tipo="Total", proveedor="Todos"):
    data = df.copy()
    if anios:
        data = data[data["anio"].isin(anios)]
    if meses:
        data = data[data["mes"].isin(meses)]
    if tipo and tipo != "Total":
        data = data[data["tipo"] == tipo]
    if proveedor and proveedor != "Todos":
        data = data[data["proveedor"] == proveedor]
    return data


def filtrar_presupuesto(df, anios=None, meses=None, tipo="Total", proveedor="Todos"):
    data = df.copy()
    if anios:
        data = data[data["anio"].isin(anios)]
    if meses:
        data = data[data["mes"].isin(meses)]
    if tipo and tipo != "Total":
        data = data[data["tipo"] == tipo]
    if proveedor and proveedor != "Todos":
        data = data[data["proveedor"] == proveedor]
    return data


def resumen_periodo(ingreso, presupuesto, anio, meses, tipo="Total", proveedor="Todos"):
    ing = filtrar_ingreso(ingreso, [anio], meses, tipo, proveedor)
    ppto = filtrar_presupuesto(presupuesto, [anio], meses, tipo, proveedor)
    ejecutado = ing["peso_ton"].sum()
    presupuestado = ppto["presupuesto_mes"].sum()
    diferencia = ejecutado - presupuestado
    cumplimiento = ejecutado / presupuestado if presupuestado else 0
    proveedores = ing["proveedor"].nunique()
    viajes = len(ing)
    return {
        "ejecutado": ejecutado,
        "presupuesto": presupuestado,
        "diferencia": diferencia,
        "cumplimiento": cumplimiento,
        "proveedores": proveedores,
        "viajes": viajes,
    }


def serie_real_vs_presupuesto(ingreso, presupuesto, anio, meses, tipo="Total", proveedor="Todos"):
    """Si recibe un solo mes, devuelve serie diaria. Si son varios meses, mensual."""
    ing = filtrar_ingreso(ingreso, [anio], meses, tipo, proveedor)
    ppto = filtrar_presupuesto(presupuesto, [anio], meses, tipo, proveedor)

    if len(meses) == 1:
        mes = meses[0]
        dias = sorted(ing["dia"].dropna().astype(int).unique().tolist())
        if not dias:
            dias = list(range(1, 32))
        total_ppto = ppto["presupuesto_mes"].sum()
        max_dia = max(dias) if dias else 30
        presupuesto_dia = total_ppto / max_dia if max_dia else 0
        ejecutado = ing.groupby("dia", as_index=False)["peso_ton"].sum().rename(columns={"peso_ton": "ejecutado"})
        base = pd.DataFrame({"periodo": dias, "dia": dias})
        base = base.merge(ejecutado, on="dia", how="left")
        base["ejecutado"] = base["ejecutado"].fillna(0)
        base["presupuesto"] = presupuesto_dia
        base["cumplimiento"] = np.where(base["presupuesto"] > 0, base["ejecutado"] / base["presupuesto"], 0)
        base["granularidad"] = "Día"
        base["periodo_label"] = base["dia"].astype(str)
        return base

    ing_m = ing.groupby(["orden_mes", "mes"], as_index=False)["peso_ton"].sum().rename(columns={"peso_ton": "ejecutado"})
    ppto_m = ppto.groupby(["orden_mes", "mes"], as_index=False)["presupuesto_mes"].sum().rename(columns={"presupuesto_mes": "presupuesto"})
    base = pd.DataFrame({"mes": meses})
    base["orden_mes"] = base["mes"].map(MESES_ORDEN)
    base = base.merge(ppto_m, on=["orden_mes", "mes"], how="left").merge(ing_m, on=["orden_mes", "mes"], how="left")
    base[["presupuesto", "ejecutado"]] = base[["presupuesto", "ejecutado"]].fillna(0)
    base["cumplimiento"] = np.where(base["presupuesto"] > 0, base["ejecutado"] / base["presupuesto"], 0)
    base["granularidad"] = "Mes"
    base["periodo_label"] = base["mes"]
    return base.sort_values("orden_mes")


def resumen_por_tipo(ingreso, presupuesto, anio, meses):
    rows = []
    for tipo in ["Grupo", "Terceros", "Total"]:
        rows.append({"tipo": tipo, **resumen_periodo(ingreso, presupuesto, anio, meses, tipo=tipo)})
    return pd.DataFrame(rows)


def resumen_proveedores(ingreso, presupuesto, anio, meses, tipo="Total"):
    ing = filtrar_ingreso(ingreso, [anio], meses, tipo, "Todos")
    ppto = filtrar_presupuesto(presupuesto, [anio], meses, tipo, "Todos")
    e = ing.groupby(["proveedor", "tipo"], as_index=False)["peso_ton"].sum().rename(columns={"peso_ton": "ejecutado"})
    p = ppto.groupby(["proveedor", "tipo"], as_index=False)["presupuesto_mes"].sum().rename(columns={"presupuesto_mes": "presupuesto"})
    df = p.merge(e, on=["proveedor", "tipo"], how="outer").fillna({"presupuesto": 0, "ejecutado": 0})
    if "tipo_x" in df.columns:
        pass
    df["diferencia"] = df["ejecutado"] - df["presupuesto"]
    df["cumplimiento"] = np.where(df["presupuesto"] > 0, df["ejecutado"] / df["presupuesto"], 0)
    total = df["ejecutado"].sum()
    df["participacion"] = np.where(total > 0, df["ejecutado"] / total, 0)
    return df.sort_values("ejecutado", ascending=False)


def resumen_calidad(ingreso, anio, meses, tipo="Total", proveedor="Todos", nivel="proveedor"):
    ing = filtrar_ingreso(ingreso, [anio], meses, tipo, proveedor)
    if ing.empty:
        return pd.DataFrame()
    group_cols = ["proveedor", "tipo"] if nivel == "proveedor" else ["tipo"]
    vals = ["maduro", "verde", "sobremaduro", "podrido", "pedunculo_largo"]
    df = ing.groupby(group_cols, as_index=False)[vals].mean()
    return df


def matriz_calidad_mensual(ingreso, anio, meses, indicador="maduro", tipo="Total"):
    ing = filtrar_ingreso(ingreso, [anio], meses, tipo, "Todos")
    if ing.empty:
        return pd.DataFrame()
    tab = ing.pivot_table(index=["tipo", "proveedor"], columns="mes", values=indicador, aggfunc="mean")
    # orden columnas
    cols = [m for m in MESES if m in tab.columns]
    tab = tab[cols]
    tab["Total general"] = tab.mean(axis=1)
    return tab.reset_index()


def tendencia_historica(ingreso, presupuesto, anios, meses, tipo="Total", proveedor="Todos", usar_presupuesto=False):
    if usar_presupuesto:
        data = filtrar_presupuesto(presupuesto, anios, meses, tipo, proveedor)
        col = "presupuesto_mes"
    else:
        data = filtrar_ingreso(ingreso, anios, meses, tipo, proveedor)
        col = "peso_ton"
    if data.empty:
        return pd.DataFrame(columns=["anio", "mes", "orden_mes", "toneladas"])
    df = data.groupby(["anio", "orden_mes", "mes"], as_index=False)[col].sum().rename(columns={col: "toneladas"})
    return df.sort_values(["anio", "orden_mes"])
