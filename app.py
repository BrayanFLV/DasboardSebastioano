import streamlit as st
from textwrap import dedent

from src.styles import aplicar_estilos
from src.data_loader import cargar_modelo
from src.calculations import (
    resumen_periodo,
    serie_real_vs_presupuesto,
    resumen_por_tipo,
    resumen_proveedores,
    resumen_calidad,
    matriz_calidad_mensual,
    tendencia_historica,
)
from src.charts import (
    grafico_real_vs_presupuesto,
    grafico_cumplimiento,
    grafico_participacion_tipo,
    grafico_acumulado,
    grafico_ranking_proveedores,
    grafico_calidad_barras,
    grafico_tendencia_historica,
    grafico_barras_proveedores_mini,
    grafico_cumplimiento_gauge,
    grafico_acumulado_combo,
    grafico_top_proveedores_resumen,
)
from src.components.cards import card_kpi
from src.components.filters import filtros_superiores, selector_pagina
from src.components.tables import tabla_resumen_periodo, tabla_proveedores, tabla_calidad, tabla_matriz_calidad, tabla_tendencia_historica

st.set_page_config(
    page_title="Dashboard RFF San Sebastiano",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

aplicar_estilos()


def html(markup: str):
    limpio = "\n".join(line.strip() for line in dedent(markup).strip().splitlines() if line.strip())
    st.markdown(limpio, unsafe_allow_html=True)


RUTA_INGRESO = "Files/Datos Ingreso y calidad.xlsx"
RUTA_PRESUPUESTO = "Files/Presupuestado.xlsx"


@st.cache_data(show_spinner="Cargando información RFF...")
def cargar_base():
    return cargar_modelo(RUTA_INGRESO, RUTA_PRESUPUESTO)


try:
    ingreso, presupuesto = cargar_base()
except Exception as e:
    st.error("No pude cargar la información. Revisa que existan Datos Ingreso y calidad.xlsx y Presupuestado.xlsx en Files.")
    st.exception(e)
    st.stop()

proveedores_base = sorted(ingreso["proveedor"].dropna().astype(str).unique().tolist())
proveedores_count = ingreso["proveedor"].nunique()

# Valores iniciales para que el encabezado y filtros sean realmente dinámicos
anios_disponibles = sorted([int(x) for x in ingreso["anio"].dropna().unique().tolist()])
meses_disponibles = ingreso.sort_values("orden_mes")["mes"].dropna().unique().tolist()
if "global_filtro_anio" not in st.session_state:
    st.session_state["global_filtro_anio"] = anios_disponibles[-1] if anios_disponibles else 2026
if "global_filtro_meses" not in st.session_state:
    st.session_state["global_filtro_meses"] = meses_disponibles[:1] if meses_disponibles else ["Enero"]
if "global_filtro_tipo" not in st.session_state:
    st.session_state["global_filtro_tipo"] = "Total"
if "global_filtro_proveedor" not in st.session_state:
    st.session_state["global_filtro_proveedor"] = "Todos"

hero_kpi = resumen_periodo(
    ingreso,
    presupuesto,
    int(st.session_state.get("global_filtro_anio", anios_disponibles[-1] if anios_disponibles else 2026)),
    st.session_state.get("global_filtro_meses", meses_disponibles[:1] if meses_disponibles else ["Enero"]),
    st.session_state.get("global_filtro_tipo", "Total"),
    st.session_state.get("global_filtro_proveedor", "Todos"),
)
hero_periodo = ", ".join(st.session_state.get("global_filtro_meses", [])) or "Enero"
hero_proveedores = int(hero_kpi.get("proveedores", 0))

# =========================
# SIDEBAR MISMO DISEÑO
# =========================
st.sidebar.markdown(dedent("""
<div class="brand">
    <div class="brand-icon"><i class="ph ph-tree-palm"></i></div>
    <div>
        <div class="brand-title">SAN SEBASTIANO</div>
        <div class="brand-sub">EXTRACTORA</div>
    </div>
</div>

""").strip(), unsafe_allow_html=True)

pagina = selector_pagina()

st.sidebar.markdown(dedent("""
<div class="menu-title">CONFIGURACIÓN</div>
<div class="menu-item"><i class="ph ph-sliders-horizontal"></i><span>Parámetros</span></div>
<div class="menu-item"><i class="ph ph-user-circle"></i><span>Usuarios</span></div>
""").strip(), unsafe_allow_html=True)

# =========================
# TOPBAR + HERO
# =========================
col_title, col_actions = st.columns([1.55, 1])
with col_title:
    html("""
    <div class="topbar-title">
        <div class="page-kicker">Dashboard operativo</div>
        <h1>Dashboard RFF 2026</h1>
    </div>
    """)
with col_actions:
    a1, a2, a3 = st.columns([1.25, .9, .9])
    with a1:
        st.markdown('<div class="period-pill-real"><i class="ph ph-calendar-check"></i>&nbsp; Datos dinámicos</div>', unsafe_allow_html=True)
    with a2:
        st.download_button(
            "Descargar",
            data=ingreso.to_csv(index=False).encode("utf-8-sig"),
            file_name="ingreso_rff_filtrado_base.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with a3:
        if st.button("Actualizar", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

html(f"""
<div class="hero-card">
    <div class="hero-left">
        <div class="eyebrow">BÁSCULA · RECEPCIÓN DE FRUTA</div>
        <div class="hero-title">Tablero de Ingreso RFF</div>
        <div class="hero-desc">
            Seguimiento unificado de ingreso diario, mensual y anual; presupuesto, participación Grupo/Terceros y calidad del fruto por proveedor.
        </div>
        <div class="legend-row">
            <span><i class="dot orange"></i>Grupo propios</span>
            <span><i class="dot green"></i>Terceros</span>
            <span><i class="dot blue"></i>Total consolidado</span>
        </div>
    </div>
    <div class="hero-meta">
        <div class="meta-item"><i class="ph ph-calendar-check"></i><div><small>Periodo</small><b>{hero_periodo} {st.session_state.get("global_filtro_anio", "")}</b></div></div>
        <div class="meta-item"><i class="ph ph-clock-countdown"></i><div><small>Corte</small><b>Datos cargados desde Excel</b></div></div>
        <div class="meta-item"><i class="ph ph-users-three"></i><div><small>Proveedores con ingreso</small><b>{hero_proveedores}</b></div></div>
    </div>
</div>
""")

# =========================
# FILTROS
# =========================
anio, meses_sel, tipo, proveedor = filtros_superiores(ingreso, proveedores_base)

kpi = resumen_periodo(ingreso, presupuesto, anio, meses_sel, tipo, proveedor)
serie = serie_real_vs_presupuesto(ingreso, presupuesto, anio, meses_sel, tipo, proveedor)
res_tipo = resumen_por_tipo(ingreso, presupuesto, anio, meses_sel)
prov_df = resumen_proveedores(ingreso, presupuesto, anio, meses_sel, tipo)
if proveedor != "Todos":
    prov_df = prov_df[prov_df["proveedor"] == proveedor]
cal_df = resumen_calidad(ingreso, anio, meses_sel, tipo, proveedor)

# =========================
# KPIS DINÁMICOS - GRID RESPONSIVE
# =========================
granularidad = "Diaria" if len(meses_sel) == 1 else "Mensual"

def fmt_card(valor, unidad=""):
    try:
        if unidad == "%":
            return f"{valor:.1%}"
        if unidad == "Ton":
            return f"{valor:,.0f} Ton"
        if isinstance(valor, float):
            return f"{valor:,.1f}"
        return f"{valor:,}"
    except Exception:
        return str(valor)



def fmt_ton(valor):
    try:
        return f"{float(valor):,.0f} Ton"
    except Exception:
        return str(valor)


def fmt_pct(valor):
    try:
        return f"{float(valor):.1%}"
    except Exception:
        return "0.0%"


def estado_cumplimiento(cumplimiento):
    if cumplimiento >= 1:
        return "🟢 Periodo en meta", "good", "El ingreso ejecutado está igual o por encima del presupuesto."
    if cumplimiento >= .8:
        return "🟠 Desvío moderado", "warn", "Hay una brecha frente a la meta, pero todavía es controlable."
    return "🔴 Periodo crítico", "bad", "El cumplimiento está bajo y conviene revisar proveedores y días críticos."


def construir_insights(kpi, res_tipo, prov_df):
    insights = []
    cumplimiento = kpi.get("cumplimiento", 0)
    diferencia = kpi.get("diferencia", 0)
    if cumplimiento >= 1:
        insights.append(f"El periodo supera la meta en {fmt_ton(abs(diferencia))}.")
    else:
        insights.append(f"Faltan {fmt_ton(abs(diferencia))} para alcanzar el presupuesto del periodo.")

    try:
        tipos = res_tipo[res_tipo["tipo"].isin(["Grupo", "Terceros"])].copy()
        if not tipos.empty and tipos["ejecutado"].sum() > 0:
            top_tipo = tipos.sort_values("ejecutado", ascending=False).iloc[0]
            part = top_tipo["ejecutado"] / tipos["ejecutado"].sum()
            insights.append(f"La mayor participación viene de {top_tipo['tipo']} con {fmt_pct(part)} del total ejecutado.")
    except Exception:
        pass

    try:
        base = prov_df[prov_df["ejecutado"] > 0].copy()
        if not base.empty:
            lider = base.sort_values("ejecutado", ascending=False).iloc[0]
            insights.append(f"Proveedor líder del periodo: {lider['proveedor']} con {fmt_ton(lider['ejecutado'])}.")
            criticos = base[base["cumplimiento"] < .8]
            if not criticos.empty:
                insights.append(f"Hay {len(criticos)} proveedor(es) por debajo del 80% de cumplimiento.")
    except Exception:
        pass
    return insights[:4]

def kpi_card_html(titulo, valor, unidad, subtitulo, icono, tipo_clase=""):
    return f"""
    <div class="kpi-card {tipo_clase}">
        <div class="kpi-top">
            <div class="kpi-label">{titulo}</div>
            <div class="kpi-icon"><i class="ph {icono}"></i></div>
        </div>
        <div class="kpi-value">{fmt_card(valor, unidad)}</div>
        <div class="kpi-sub">{subtitulo}</div>
    </div>
    """

html("""
<div class="kpi-responsive-grid">
""" + "".join([
    kpi_card_html("RFF recibido", kpi["ejecutado"], "Ton", f"{kpi['viajes']:,} viajes", "ph-package"),
    kpi_card_html("Cumplimiento", kpi["cumplimiento"], "%", "Vs presupuesto", "ph-trend-up", "good" if kpi["cumplimiento"] >= 1 else "warn"),
    kpi_card_html("Presupuesto", kpi["presupuesto"], "Ton", "RFF PESS distribuido", "ph-target"),
    kpi_card_html("Diferencia", kpi["diferencia"], "Ton", "Ejecutado - meta", "ph-scales", "good" if kpi["diferencia"] >= 0 else "bad"),
    kpi_card_html("Proveedores", kpi["proveedores"], "", "Con ingreso en periodo", "ph-users-three"),
    kpi_card_html("Vista", granularidad, "", f"Gráficas por {granularidad.lower()}", "ph-calendar"),
]) + """
</div>
""")

# =========================
# PÁGINAS
# =========================
if pagina == "Vista general":
    estado_txt, estado_clase, estado_desc = estado_cumplimiento(kpi["cumplimiento"])
    insights = construir_insights(kpi, res_tipo, prov_df)
    top_prov = prov_df[prov_df["ejecutado"] > 0].sort_values("ejecutado", ascending=False).head(5)
    alertas_prov = prov_df[(prov_df["presupuesto"] > 0) & (prov_df["cumplimiento"] < .8)].sort_values("cumplimiento", ascending=True).head(5)

    html("""
    <div class="section-head">
        <div><div class="section-code">01 / RESUMEN EJECUTIVO</div><h2>Vista ejecutiva del periodo</h2><p>Lectura rápida del comportamiento real frente al presupuesto, participación y alertas principales.</p></div>
    </div>
    """)

    html(f"""
    <div class="executive-grid">
        <div class="executive-card narrative">
            <div class="exec-kicker">LECTURA DEL PERIODO</div>
            <h3>{estado_txt}</h3>
            <p>{estado_desc}</p>
            <div class="exec-mini-row">
                <span><b>{fmt_ton(kpi['ejecutado'])}</b><small>Ejecutado</small></span>
                <span><b>{fmt_ton(kpi['presupuesto'])}</b><small>Presupuesto</small></span>
                <span><b>{fmt_pct(kpi['cumplimiento'])}</b><small>Cumplimiento</small></span>
            </div>
        </div>
        <div class="executive-card insights {estado_clase}">
            <div class="exec-kicker">HALLAZGOS AUTOMÁTICOS</div>
            <ul>
                {''.join([f'<li>{x}</li>' for x in insights])}
            </ul>
        </div>
    </div>
    """)

    g1, g2 = st.columns([1.6, 1], gap="large")
    with g1:
        html('<div class="chart-title"><i class="ph ph-chart-bar"></i> Real vs presupuestado</div>')
        st.plotly_chart(grafico_real_vs_presupuesto(serie), use_container_width=True)
    with g2:
        html('<div class="chart-title"><i class="ph ph-gauge"></i> Cumplimiento ejecutivo</div>')
        st.plotly_chart(grafico_cumplimiento_gauge(kpi["cumplimiento"], kpi["ejecutado"], kpi["presupuesto"]), use_container_width=True)

    html('<div class="chart-title"><i class="ph ph-trend-up"></i> Cumplimiento por periodo</div>')
    st.plotly_chart(grafico_cumplimiento(serie), use_container_width=True)

    g3, g4 = st.columns([1, 1.45], gap="large")
    with g3:
        html('<div class="chart-title"><i class="ph ph-chart-donut"></i> Participación Grupo / Terceros</div>')
        st.plotly_chart(grafico_participacion_tipo(res_tipo), use_container_width=True)
    with g4:
        html('<div class="chart-title"><i class="ph ph-chart-line-up"></i> Acumulado real vs presupuesto</div>')
        st.plotly_chart(grafico_acumulado_combo(serie), use_container_width=True)

    h1, h2 = st.columns([1, 1], gap="large")
    with h1:
        html('<div class="chart-title"><i class="ph ph-trophy"></i> Top 5 proveedores del periodo</div>')
        st.plotly_chart(grafico_top_proveedores_resumen(top_prov, top=5), use_container_width=True)
    with h2:
        html('<div class="chart-title"><i class="ph ph-warning-circle"></i> Alertas por bajo cumplimiento</div>')
        if alertas_prov.empty:
            html('<div class="empty-state"><b>Sin alertas críticas</b><span>No hay proveedores por debajo del 80% en el periodo seleccionado.</span></div>')
        else:
            st.plotly_chart(grafico_barras_proveedores_mini(alertas_prov, metrica="cumplimiento", top=5), use_container_width=True)

    html('<div class="chart-title"><i class="ph ph-table"></i> Resumen Grupo / Terceros / Total</div>')
    tabla_resumen_periodo(res_tipo)

elif pagina == "Ingreso por proveedor":
    html("""
    <div class="section-head"><div><div class="section-code">02 / PROVEEDORES</div><h2>Ingreso por proveedor</h2><p>Vista ajustada para monitores pequeños: cada bloque queda en fila, con tabla y gráfico compacto al lado. En móvil baja uno debajo del otro.</p></div></div>
    """)

    html('<div class="chart-title"><i class="ph ph-ranking"></i> Ranking general de proveedores</div>')
    st.plotly_chart(grafico_ranking_proveedores(prov_df), use_container_width=True)

    mayores = prov_df.sort_values("cumplimiento", ascending=False)
    menores = prov_df.sort_values("cumplimiento", ascending=True)

    html('<div class="chart-title"><i class="ph ph-trend-up"></i> Mayores cumplimientos</div>')
    t1, g1 = st.columns([1.25, 1], gap="medium")
    with t1:
        tabla_proveedores(mayores, top=5)
    with g1:
        st.plotly_chart(grafico_barras_proveedores_mini(mayores, metrica="cumplimiento", top=5), use_container_width=True)

    html('<div class="chart-title"><i class="ph ph-warning-circle"></i> Menores cumplimientos</div>')
    t2, g2 = st.columns([1.25, 1], gap="medium")
    with t2:
        tabla_proveedores(menores, top=5)
    with g2:
        st.plotly_chart(grafico_barras_proveedores_mini(menores, metrica="cumplimiento", top=5), use_container_width=True)

    html('<div class="chart-title"><i class="ph ph-info"></i> Información general Grupo / Terceros</div>')
    t3, g3 = st.columns([1.05, 1.2], gap="medium")
    with t3:
        tabla_resumen_periodo(res_tipo)
    with g3:
        st.plotly_chart(grafico_barras_proveedores_mini(prov_df.sort_values("ejecutado", ascending=False), metrica="ejecutado", top=8), use_container_width=True)

    html('<div class="chart-title"><i class="ph ph-table"></i> Detalle completo por proveedor</div>')
    tabla_proveedores(prov_df)

elif pagina == "Real vs presupuesto":
    html("""
    <div class="section-head"><div><div class="section-code">03 / PRESUPUESTO</div><h2>Ingreso real vs presupuestado</h2><p>Presupuesto calculado desde RFF PESS y porcentaje mensual del archivo Presupuestado.xlsx.</p></div></div>
    """)
    g1, g2 = st.columns(2)
    with g1:
        html('<div class="chart-title"><i class="ph ph-chart-bar"></i> Comparativo del periodo</div>')
        st.plotly_chart(grafico_real_vs_presupuesto(serie), use_container_width=True)
    with g2:
        html('<div class="chart-title"><i class="ph ph-chart-line-up"></i> Acumulado</div>')
        st.plotly_chart(grafico_acumulado(serie), use_container_width=True)
    html('<div class="chart-title"><i class="ph ph-table"></i> Cumplimiento por proveedor</div>')
    tabla_proveedores(prov_df)

elif pagina == "Participación Grupo/Terceros":
    html("""
    <div class="section-head"><div><div class="section-code">04 / PARTICIPACIÓN</div><h2>Participación Grupo vs Terceros</h2><p>Participación en porcentaje para el periodo seleccionado.</p></div></div>
    """)
    g1, g2 = st.columns([1, 1.4])
    with g1:
        html('<div class="chart-title"><i class="ph ph-chart-donut"></i> Participación consolidada</div>')
        st.plotly_chart(grafico_participacion_tipo(res_tipo), use_container_width=True)
    with g2:
        html('<div class="chart-title"><i class="ph ph-table"></i> Resumen por tipo</div>')
        tabla_resumen_periodo(res_tipo)

elif pagina == "Calidad del fruto":
    html("""
    <div class="section-head"><div><div class="section-code">05 / CALIDAD</div><h2>Calidad RFF por proveedor</h2><p>Maduro &gt;89%, Verde &lt;1%, Sobremaduro &lt;10%, Podrido 0% y Pedúnculo largo 0%.</p></div></div>
    """)
    q1, q2, q3, q4, q5 = st.columns(5)
    if not cal_df.empty:
        q1.metric("Maduro", f"{cal_df['maduro'].mean():.1%}")
        q2.metric("Verde", f"{cal_df['verde'].mean():.1%}")
        q3.metric("Sobremaduro", f"{cal_df['sobremaduro'].mean():.1%}")
        q4.metric("Podrido", f"{cal_df['podrido'].mean():.1%}")
        q5.metric("Pedúnculo", f"{cal_df['pedunculo_largo'].mean():.1%}")
    html('<div class="chart-title"><i class="ph ph-leaf"></i> RFF maduro por proveedor</div>')
    st.plotly_chart(grafico_calidad_barras(cal_df, "maduro", .89), use_container_width=True)
    html('<div class="chart-title"><i class="ph ph-table"></i> Calidad consolidada por proveedor</div>')
    tabla_calidad(cal_df)
    html('<div class="chart-title"><i class="ph ph-grid-four"></i> Matriz mensual de maduro</div>')
    tabla_matriz_calidad(matriz_calidad_mensual(ingreso, anio, meses_sel, "maduro", tipo))

elif pagina == "Tendencia histórica":
    html("""
    <div class="section-head"><div><div class="section-code">06 / HISTÓRICO</div><h2>Comportamiento mensual de productividad</h2><p>Comparativo de toneladas por año respecto a cada mes. Aplica por proveedor, Grupo, Terceros o Total.</p></div></div>
    """)
    usar_ppto = st.toggle("Ver tendencia con presupuesto en lugar de ingreso real", value=False)
    anios_disp = sorted([int(x) for x in ingreso["anio"].dropna().unique().tolist()])
    tend = tendencia_historica(ingreso, presupuesto, anios_disp, meses_sel, tipo, proveedor, usar_presupuesto=usar_ppto)
    html('<div class="chart-title"><i class="ph ph-chart-line-up"></i> Comparativo mensual por año</div>')
    st.plotly_chart(grafico_tendencia_historica(tend), use_container_width=True)
    tabla_tendencia_historica(tend)
