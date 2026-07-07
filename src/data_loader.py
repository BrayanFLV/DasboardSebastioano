import re
import pandas as pd

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]
MES_ABBR = {
    "ENE": "Enero", "ENERO": "Enero", "FEB": "Febrero", "FEBRERO": "Febrero",
    "MAR": "Marzo", "MARZO": "Marzo", "ABR": "Abril", "ABRIL": "Abril",
    "MAY": "Mayo", "MAYO": "Mayo", "JUN": "Junio", "JUNIO": "Junio",
    "JUL": "Julio", "JULIO": "Julio", "AGO": "Agosto", "AGOSTO": "Agosto",
    "SEP": "Septiembre", "SEPTIEMBRE": "Septiembre", "OCT": "Octubre", "OCTUBRE": "Octubre",
    "NOV": "Noviembre", "NOVIEMBRE": "Noviembre", "DIC": "Diciembre", "DICIEMBRE": "Diciembre",
}
MESES_ORDEN = {m: i + 1 for i, m in enumerate(MESES)}


def normalizar_proveedor(valor):
    txt = str(valor or "").upper().strip()
    txt = txt.replace("PALMERAS", "").replace("PALMERA", "")
    txt = txt.replace("S.A.S.", "").replace("S.A.S", "").replace("SAS", "")
    txt = txt.replace("PESS", "").replace("-", " ")
    txt = re.sub(r"[^A-ZÁÉÍÓÚÑ0-9 ]", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt


def normalizar_tipo(valor):
    txt = str(valor or "").upper().strip()
    if "TER" in txt:
        return "Terceros"
    if "GRU" in txt:
        return "Grupo"
    return "Sin clasificar"


def _normalizar_mes(valor):
    if pd.isna(valor):
        return None
    if isinstance(valor, (int, float)):
        try:
            return MESES[int(valor) - 1]
        except Exception:
            return None
    txt = str(valor).upper().strip()
    txt = re.sub(r"[^A-ZÁÉÍÓÚÑ]", "", txt)
    return MES_ABBR.get(txt, txt.title())


def cargar_datos_ingreso(ruta_excel):
    xl = pd.ExcelFile(ruta_excel)
    frames = []
    for sheet in xl.sheet_names:
        if not str(sheet).strip().isdigit():
            continue
        df = pd.read_excel(ruta_excel, sheet_name=sheet)
        if df.empty:
            continue
        df.columns = [str(c).strip() for c in df.columns]
        df["AÑO"] = pd.to_numeric(df.get("AÑO", sheet), errors="coerce").fillna(int(sheet)).astype(int)
        frames.append(df)
    if not frames:
        return pd.DataFrame()

    df = pd.concat(frames, ignore_index=True)
    df["proveedor"] = df.get("NOMBRE DEL PROVEEDOR", "").astype(str).str.strip()
    df["proveedor_key"] = df["proveedor"].map(normalizar_proveedor)
    df["tipo"] = df.get("GRUPO/ TERCEROS", "").map(normalizar_tipo)

    fecha = pd.to_datetime(df.get("FECHA DE SALIDA"), errors="coerce")
    fecha_alt = pd.to_datetime(df.get("FECHA DE INGRESO"), errors="coerce")
    df["fecha"] = fecha.fillna(fecha_alt)
    df["anio"] = pd.to_numeric(df["AÑO"], errors="coerce").fillna(df["fecha"].dt.year).astype("Int64")
    df["mes"] = df.get("MES", None).map(_normalizar_mes) if "MES" in df.columns else df["fecha"].dt.month.map(lambda x: MESES[int(x)-1] if pd.notna(x) else None)
    df["orden_mes"] = df["mes"].map(MESES_ORDEN)
    df["dia"] = pd.to_numeric(df.get("DÍA", df["fecha"].dt.day), errors="coerce").fillna(df["fecha"].dt.day)
    df["dia"] = df["dia"].astype("Int64")
    df["peso_ton"] = pd.to_numeric(df.get("PESO NETO"), errors="coerce").fillna(0) / 1000

    # Calidad viene en fracciones 0-1
    for col, new in [("% M", "maduro"), ("% V", "verde"), ("% S.M", "sobremaduro"), ("% P", "podrido"), ("% P.L", "pedunculo_largo")]:
        df[new] = pd.to_numeric(df.get(col), errors="coerce")

    return df[
        ["anio", "mes", "orden_mes", "dia", "fecha", "proveedor", "proveedor_key", "tipo", "peso_ton", "maduro", "verde", "sobremaduro", "podrido", "pedunculo_largo"]
    ].dropna(subset=["anio", "mes"])


def cargar_presupuesto(ruta_excel):
    xl = pd.ExcelFile(ruta_excel)
    frames = []
    for sheet in xl.sheet_names:
        if not str(sheet).strip().isdigit():
            continue
        raw = pd.read_excel(ruta_excel, sheet_name=sheet)
        if raw.empty:
            continue
        raw.columns = [str(c).strip() for c in raw.columns]
        year = int(sheet)
        # Normaliza columnas con nombres variables
        col_plant = next((c for c in raw.columns if "plant" in c.lower()), "Plantación")
        col_tipo = next((c for c in raw.columns if c.lower().startswith("tipo")), "Tipo")
        col_pess = next((c for c in raw.columns if "pess" in c.lower()), "RFF PESS")
        col_mes = next((c for c in raw.columns if c.lower() == "mes"), "Mes")
        col_pct = next((c for c in raw.columns if "porcentaje" in c.lower()), "Porcentajes")

        proveedores = raw[[col_tipo, col_plant, col_pess]].copy()
        proveedores.columns = ["tipo_raw", "proveedor", "rff_pess"]
        proveedores = proveedores.dropna(subset=["proveedor"])
        proveedores = proveedores[~proveedores["proveedor"].astype(str).str.upper().str.contains("TOTAL")]
        proveedores["tipo"] = proveedores["tipo_raw"].ffill().map(normalizar_tipo)
        proveedores["proveedor"] = proveedores["proveedor"].astype(str).str.strip()
        proveedores["proveedor_key"] = proveedores["proveedor"].map(normalizar_proveedor)
        proveedores["rff_pess"] = pd.to_numeric(proveedores["rff_pess"], errors="coerce").fillna(0)
        proveedores = proveedores[proveedores["rff_pess"] > 0]

        est = raw[[col_mes, col_pct]].copy().dropna(subset=[col_mes, col_pct])
        est.columns = ["mes", "pct_estacional"]
        est["mes"] = est["mes"].map(_normalizar_mes)
        est["orden_mes"] = est["mes"].map(MESES_ORDEN)
        est["pct_estacional"] = pd.to_numeric(est["pct_estacional"], errors="coerce").fillna(0)
        est = est.dropna(subset=["mes"])

        regs = []
        for _, p in proveedores.iterrows():
            for _, m in est.iterrows():
                regs.append({
                    "anio": year,
                    "proveedor": p["proveedor"],
                    "proveedor_key": p["proveedor_key"],
                    "tipo": p["tipo"],
                    "rff_pess": p["rff_pess"],
                    "mes": m["mes"],
                    "orden_mes": int(m["orden_mes"]),
                    "pct_estacional": m["pct_estacional"],
                    "presupuesto_mes": p["rff_pess"] * m["pct_estacional"],
                })
        frames.append(pd.DataFrame(regs))
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def cargar_modelo(ruta_ingreso="Files/Datos Ingreso y calidad.xlsx", ruta_presupuesto="Files/Presupuestado.xlsx"):
    ingreso = cargar_datos_ingreso(ruta_ingreso)
    presupuesto = cargar_presupuesto(ruta_presupuesto)
    return ingreso, presupuesto
