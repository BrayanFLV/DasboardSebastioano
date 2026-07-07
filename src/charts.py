import plotly.graph_objects as go
import plotly.express as px

VERDE = "#4f9b3f"
VERDE_OSCURO = "#0f4c33"
NARANJA = "#f28c28"
ROJO = "#cf4f3f"
AZUL = "#2d7dd2"
GRIS = "#6f7d75"
LINEA = "#dce7db"


def _is_daily(data):
    try:
        return str(data["granularidad"].iloc[0]).lower().startswith("d")
    except Exception:
        return False


def formato_figura(fig, height=390):
    fig.update_layout(
        height=height,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter", color="#17251d", size=12),
        margin=dict(l=10, r=10, t=30, b=24),
        legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="left", x=0),
        hovermode="x unified",
        autosize=True,
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor=LINEA,
        tickfont=dict(color=GRIS, size=11),
        automargin=True,
    )
    fig.update_yaxes(
        gridcolor=LINEA,
        linecolor=LINEA,
        tickfont=dict(color=GRIS, size=11),
        automargin=True,
        separatethousands=True,
        exponentformat="none",
        showexponent="none",
    )
    return fig


def grafico_real_vs_presupuesto(data):
    data = data.copy()
    x = data["periodo_label"].astype(str)
    diario = _is_daily(data)
    text_p = [f"{v:,.0f}" if v > 0 and (not diario or i % 2 == 0) else "" for i, v in enumerate(data["presupuesto"])]
    text_e = [f"{v:,.0f}" if v > 0 and (not diario or i % 2 == 0) else "" for i, v in enumerate(data["ejecutado"])]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=data["presupuesto"],
        name="Presupuesto",
        marker_color=VERDE,
        opacity=0.82,
        text=text_p,
        textposition="outside",
        cliponaxis=False,
    ))
    fig.add_trace(go.Bar(
        x=x,
        y=data["ejecutado"],
        name="Ejecutado",
        marker_color=VERDE_OSCURO,
        text=text_e,
        textposition="outside",
        cliponaxis=False,
    ))
    fig.update_layout(
        barmode="group",
        yaxis_title="Toneladas",
        xaxis_title="Día" if diario else "Mes",
        bargap=0.18 if not diario else 0.08,
        bargroupgap=0.08,
    )
    fig.update_yaxes(tickformat=",.0f", separatethousands=True)
    fig.update_yaxes(tickformat=",.0f", separatethousands=True)
    if diario:
        fig.update_xaxes(tickmode="linear", dtick=1, tickangle=0)
    else:
        fig.update_xaxes(tickangle=0)
    return formato_figura(fig, height=410)


def grafico_cumplimiento(data):
    data = data.copy()
    x = data["periodo_label"].astype(str)
    diario = _is_daily(data)
    colores = [VERDE if v >= 1 else (NARANJA if v >= 0.80 else ROJO) for v in data["cumplimiento"]]
    textos = [f"{v:.0%}" if v > 0 and (not diario or i % 2 == 0) else "" for i, v in enumerate(data["cumplimiento"])]
    ymax = max(1.15, float(data["cumplimiento"].max() or 1) * 1.16)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=data["cumplimiento"],
        name="Cumplimiento",
        marker=dict(
            color=colores,
            line=dict(color="rgba(15,76,51,.18)", width=1),
        ),
        text=textos,
        textposition="outside",
        cliponaxis=False,
        hovertemplate="<b>%{x}</b><br>Cumplimiento: %{y:.1%}<extra></extra>",
    ))
    fig.add_hrect(
        y0=0, y1=.80,
        fillcolor="#fde8e4", opacity=.35,
        line_width=0, layer="below",
    )
    fig.add_hrect(
        y0=.80, y1=1,
        fillcolor="#fff0dc", opacity=.35,
        line_width=0, layer="below",
    )
    fig.add_hrect(
        y0=1, y1=ymax,
        fillcolor="#e7f4e3", opacity=.32,
        line_width=0, layer="below",
    )
    fig.add_hline(y=1, line_dash="dash", line_color="#466b5a", line_width=2)
    fig.add_annotation(
        x=1, y=1.01, xref="paper", yref="y",
        text="Meta 100%", showarrow=False,
        xanchor="right", yanchor="bottom",
        bgcolor="white", bordercolor="#cfe0ca", borderwidth=1, borderpad=4,
        font=dict(size=11, color="#0f4c33"),
    )
    fig.update_layout(
        yaxis_tickformat=".0%",
        yaxis_title="Cumplimiento",
        xaxis_title="Día" if diario else "Mes",
        bargap=0.22 if not diario else 0.18,
        showlegend=False,
        uniformtext_minsize=9,
        uniformtext_mode="hide",
    )
    fig.update_yaxes(range=[0, ymax], tickformat=".0%")
    if diario:
        fig.update_xaxes(tickmode="linear", dtick=1, tickangle=0)
    else:
        fig.update_xaxes(tickangle=0)
    return formato_figura(fig, height=430)


def grafico_participacion_tipo(df_tipo):
    data = df_tipo[df_tipo["tipo"].isin(["Grupo", "Terceros"])].copy()
    fig = px.pie(
        data,
        names="tipo",
        values="ejecutado",
        hole=0.64,
        color="tipo",
        color_discrete_map={"Grupo": VERDE, "Terceros": NARANJA},
    )
    fig.update_traces(textinfo="percent+label", textfont_size=13, marker=dict(line=dict(color="white", width=3)))
    fig.update_layout(showlegend=False)
    return formato_figura(fig, height=390)


def grafico_acumulado(data):
    base = data.copy()
    base["presupuesto_acum"] = base["presupuesto"].cumsum()
    base["ejecutado_acum"] = base["ejecutado"].cumsum()
    x = base["periodo_label"].astype(str)
    diario = _is_daily(base)
    text_p = [f"{v:,.0f}" if v > 0 and (not diario or i % 2 == 0) else "" for i, v in enumerate(base["presupuesto_acum"])]
    text_e = [f"{v:,.0f}" if v > 0 and (not diario or i % 2 == 0) else "" for i, v in enumerate(base["ejecutado_acum"])]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=base["presupuesto_acum"],
        name="Presupuesto acum.",
        marker_color=VERDE,
        opacity=0.78,
        text=text_p,
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{x}<br>Presupuesto acum.: %{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=x,
        y=base["ejecutado_acum"],
        name="Ejecutado acum.",
        marker_color=VERDE_OSCURO,
        text=text_e,
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{x}<br>Ejecutado acum.: %{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        barmode="group",
        yaxis_title="Toneladas acumuladas",
        xaxis_title="Día" if diario else "Mes",
        bargap=0.18 if not diario else 0.10,
        bargroupgap=0.08,
    )
    fig.update_yaxes(tickformat=",.0f", separatethousands=True, exponentformat="none", showexponent="none")
    if diario:
        fig.update_xaxes(tickmode="linear", dtick=1, tickangle=0)
    else:
        fig.update_xaxes(tickangle=0)
    return formato_figura(fig, height=410)


def grafico_ranking_proveedores(df, top=15):
    data = df.head(top).sort_values("ejecutado", ascending=True)
    colores = [VERDE if x >= 1 else (NARANJA if x >= .75 else ROJO) for x in data["cumplimiento"]]
    fig = go.Figure()
    fig.add_trace(go.Bar(y=data["proveedor"], x=data["presupuesto"], orientation="h", name="Presupuesto", marker_color="rgba(79,155,63,.25)"))
    fig.add_trace(go.Bar(y=data["proveedor"], x=data["ejecutado"], orientation="h", name="Ejecutado", marker_color=colores, text=[f"{x:.0%}" for x in data["cumplimiento"]], textposition="outside"))
    fig.update_layout(barmode="overlay", xaxis_title="Toneladas", yaxis_title=None)
    fig.update_xaxes(tickformat=",.0f", separatethousands=True)
    return formato_figura(fig, height=520)


def grafico_calidad_barras(df_calidad, indicador="maduro", meta=0.89):
    if df_calidad.empty:
        return formato_figura(go.Figure(), height=390)

    data = df_calidad.sort_values(indicador, ascending=False).head(25).copy()

    fig = px.bar(
        data,
        x="proveedor",
        y=indicador,
        color="tipo" if "tipo" in data.columns else None,
        color_discrete_map={"Grupo": VERDE_OSCURO, "Terceros": NARANJA, "Total": AZUL},
        text=data[indicador].map(lambda v: f"{v:.1%}"),
    )

    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.add_hline(
        y=meta,
        line_color=VERDE,
        line_width=3,
        annotation_text=f"Meta {meta:.0%}",
        annotation_position="top right",
    )
    fig.update_layout(
        yaxis_tickformat=".0%",
        yaxis_title="Porcentaje",
        xaxis_title=None,
        legend_title_text="Tipo",
    )
    fig.update_xaxes(tickangle=-30)
    return formato_figura(fig, height=430)


def grafico_tendencia_historica(df):
    fig = go.Figure()
    if df.empty:
        return formato_figura(fig, height=430)
    colores = {2023: "#8aa6a0", 2024: "#b3a369", 2025: NARANJA, 2026: VERDE_OSCURO}
    max_anio = max(df["anio"])
    for anio, data in df.groupby("anio"):
        fig.add_trace(go.Scatter(
            x=data["mes"],
            y=data["toneladas"],
            mode="lines+markers+text" if anio == max_anio else "lines+markers",
            name=str(anio),
            line=dict(width=4 if anio == max_anio else 2.5, color=colores.get(int(anio), AZUL), shape="spline"),
            marker=dict(size=10 if anio == max_anio else 7),
            text=[f"{v:,.0f}" for v in data["toneladas"]] if anio == max_anio else None,
            textposition="top center",
        ))
    fig.update_layout(yaxis_title="Toneladas", xaxis_title=None)
    fig.update_yaxes(tickformat=",.0f", separatethousands=True)
    return formato_figura(fig, height=440)


def grafico_barras_proveedores_mini(df, metrica="ejecutado", top=8, titulo=None):
    """Gráfico compacto para acompañar tablas en la página de proveedores."""
    fig = go.Figure()
    if df is None or df.empty:
        return formato_figura(fig, height=300)
    data = df.copy().head(top)
    if metrica not in data.columns:
        metrica = "ejecutado"
    data = data.sort_values(metrica, ascending=True)
    colores = [VERDE_OSCURO if str(t).lower().startswith("grupo") else NARANJA for t in data.get("tipo", [])]
    textos = []
    for v in data[metrica]:
        if metrica == "cumplimiento":
            textos.append(f"{v:.0%}")
        else:
            textos.append(f"{v:,.0f}")
    fig.add_trace(go.Bar(
        y=data["proveedor"].astype(str),
        x=data[metrica],
        orientation="h",
        marker_color=colores,
        text=textos,
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}<br>%{x:,.1f}<extra></extra>",
    ))
    if metrica == "cumplimiento":
        fig.update_xaxes(tickformat=".0%")
        fig.add_vline(x=1, line_dash="dash", line_color="#8b9a92")
    else:
        fig.update_xaxes(tickformat=",.0f", separatethousands=True)
    fig.update_layout(
        showlegend=False,
        xaxis_title="Cumplimiento" if metrica == "cumplimiento" else "Toneladas",
        yaxis_title=None,
        margin=dict(l=8, r=24, t=18, b=20),
    )
    return formato_figura(fig, height=310)



def grafico_cumplimiento_gauge(cumplimiento, ejecutado=0, presupuesto=0):
    """Indicador ejecutivo tipo gauge para el cumplimiento del periodo."""
    valor = float(cumplimiento or 0)
    valor_pct = max(0, min(valor * 100, 140))
    color = VERDE if valor >= 1 else (NARANJA if valor >= .8 else ROJO)
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=valor_pct,
        number={"suffix": "%", "font": {"size": 42, "color": VERDE_OSCURO}},
        delta={"reference": 100, "suffix": "%", "relative": False, "font": {"size": 14}},
        title={"text": "Cumplimiento del periodo", "font": {"size": 16, "color": "#17251d"}},
        gauge={
            "axis": {"range": [0, 140], "tickwidth": 1, "tickcolor": "#6f7d75"},
            "bar": {"color": color, "thickness": .28},
            "bgcolor": "white",
            "borderwidth": 1,
            "bordercolor": LINEA,
            "steps": [
                {"range": [0, 80], "color": "#fde8e4"},
                {"range": [80, 100], "color": "#fff0dc"},
                {"range": [100, 140], "color": "#dff0da"},
            ],
            "threshold": {"line": {"color": VERDE_OSCURO, "width": 4}, "thickness": .75, "value": 100},
        },
        domain={"x": [0, 1], "y": [0, 1]},
    ))
    fig.add_annotation(
        x=.5,
        y=-.05,
        xref="paper",
        yref="paper",
        text=f"Ejecutado: {ejecutado:,.0f} Ton · Presupuesto: {presupuesto:,.0f} Ton",
        showarrow=False,
        font=dict(size=12, color=GRIS),
    )
    fig.update_layout(margin=dict(l=12, r=12, t=42, b=32))
    return formato_figura(fig, height=360)


def grafico_acumulado_combo(data):
    """Acumulado con barras para ejecutado y línea para presupuesto para lectura ejecutiva."""
    base = data.copy()
    base["presupuesto_acum"] = base["presupuesto"].cumsum()
    base["ejecutado_acum"] = base["ejecutado"].cumsum()
    x = base["periodo_label"].astype(str)
    diario = _is_daily(base)
    textos = [f"{v:,.0f}" if v > 0 and (not diario or i % 2 == 0) else "" for i, v in enumerate(base["ejecutado_acum"])]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=base["ejecutado_acum"],
        name="Ejecutado acum.",
        marker_color=VERDE_OSCURO,
        text=textos,
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{x}<br>Ejecutado acum.: %{y:,.0f} Ton<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=x,
        y=base["presupuesto_acum"],
        name="Presupuesto acum.",
        mode="lines+markers",
        line=dict(color=NARANJA, width=4, shape="spline"),
        marker=dict(size=9, color=NARANJA, line=dict(width=2, color="white")),
        hovertemplate="%{x}<br>Presupuesto acum.: %{y:,.0f} Ton<extra></extra>",
    ))
    fig.update_layout(
        yaxis_title="Toneladas acumuladas",
        xaxis_title="Día" if diario else "Mes",
        bargap=0.18 if not diario else 0.10,
    )
    fig.update_yaxes(tickformat=",.0f", separatethousands=True, exponentformat="none", showexponent="none")
    if diario:
        fig.update_xaxes(tickmode="linear", dtick=1, tickangle=0)
    return formato_figura(fig, height=390)


def grafico_top_proveedores_resumen(df, top=5):
    """Top compacto para insertar en la vista ejecutiva."""
    return grafico_barras_proveedores_mini(df.sort_values("ejecutado", ascending=False), metrica="ejecutado", top=top)
