import html
from textwrap import dedent
import streamlit as st


def _fmt_num(value):
    try:
        return f"{float(value):,.1f}"
    except Exception:
        return "—"


def _fmt_pct(value):
    try:
        return f"{float(value) * 100:,.1f}%"
    except Exception:
        return "—"


def _type_class(tipo):
    txt = str(tipo or "").strip().lower()
    if "grupo" in txt:
        return "grupo"
    if "terc" in txt:
        return "terceros"
    return "total"


def _ordenar_por_tipo_y_valor(df, valor="ejecutado", asc_valor=False):
    if df.empty or "tipo" not in df.columns:
        return df
    data = df.copy()
    orden = {"Grupo": 0, "Terceros": 1, "Total": 2}
    data["_orden_tipo"] = data["tipo"].map(orden).fillna(9)
    sort_cols = ["_orden_tipo"]
    ascending = [True]
    if valor in data.columns:
        sort_cols.append(valor)
        ascending.append(asc_valor)
    data = data.sort_values(sort_cols, ascending=ascending).drop(columns=["_orden_tipo"])
    return data


def _render_html(markup: str):
    limpio = "\n".join(line.strip() for line in dedent(markup).strip().splitlines() if line.strip())
    st.markdown(limpio, unsafe_allow_html=True)




def _next_table_key(prefix="tabla"):
    st.session_state.setdefault("_table_filter_counter", 0)
    st.session_state["_table_filter_counter"] += 1
    return f"{prefix}_{st.session_state['_table_filter_counter']}"


def _aplicar_filtros_tabla(data, key_prefix, permitir_tipo=True, permitir_cumplimiento=True, permitir_top=True):
    """Filtros livianos y responsive para las tablas HTML del dashboard."""
    if data.empty:
        return data

    # Toolbar compacta y responsive para evitar bloques altos/desbalanceados.
    # label_visibility="collapsed" reduce la altura y los rótulos se pintan con HTML propio.
    with st.container(border=True):
        st.markdown('<div class="table-toolbar-title">Filtros rápidos</div>', unsafe_allow_html=True)
        cols = st.columns([1.7, .95, .95, .95], gap="small")

        with cols[0]:
            st.markdown('<div class="table-filter-label">Buscar</div>', unsafe_allow_html=True)
            busqueda = st.text_input(
                "Buscar",
                placeholder="Buscar proveedor...",
                key=f"{key_prefix}_buscar",
                label_visibility="collapsed",
            )

        tipo_sel = "Todos"
        if permitir_tipo and "tipo" in data.columns:
            tipos = ["Todos"] + sorted([str(x) for x in data["tipo"].dropna().unique().tolist()])
            with cols[1]:
                st.markdown('<div class="table-filter-label">Tipo</div>', unsafe_allow_html=True)
                tipo_sel = st.selectbox("Tipo", tipos, key=f"{key_prefix}_tipo", label_visibility="collapsed")

        estado_sel = "Todos"
        if permitir_cumplimiento and "cumplimiento" in data.columns:
            with cols[2]:
                st.markdown('<div class="table-filter-label">Estado</div>', unsafe_allow_html=True)
                estado_sel = st.selectbox(
                    "Estado",
                    ["Todos", "Cumple >=100%", "Atención 80%-99%", "Crítico <80%"],
                    key=f"{key_prefix}_estado",
                    label_visibility="collapsed",
                )

        top_sel = "Todos"
        if permitir_top:
            with cols[3]:
                st.markdown('<div class="table-filter-label">Mostrar</div>', unsafe_allow_html=True)
                top_sel = st.selectbox(
                    "Mostrar",
                    ["Todos", "Top 5", "Top 10", "Top 20"],
                    key=f"{key_prefix}_top",
                    label_visibility="collapsed",
                )

    filtrada = data.copy()
    if busqueda and "proveedor" in filtrada.columns:
        filtrada = filtrada[filtrada["proveedor"].astype(str).str.contains(busqueda, case=False, na=False)]
    if tipo_sel != "Todos" and "tipo" in filtrada.columns:
        filtrada = filtrada[filtrada["tipo"].astype(str) == tipo_sel]
    if estado_sel != "Todos" and "cumplimiento" in filtrada.columns:
        c = filtrada["cumplimiento"].fillna(0).astype(float)
        if estado_sel.startswith("Cumple"):
            filtrada = filtrada[c >= 1]
        elif estado_sel.startswith("Atención"):
            filtrada = filtrada[(c >= .8) & (c < 1)]
        elif estado_sel.startswith("Crítico"):
            filtrada = filtrada[c < .8]
    if top_sel != "Todos":
        n = int(top_sel.split()[-1])
        sort_col = "ejecutado" if "ejecutado" in filtrada.columns else filtrada.columns[0]
        filtrada = filtrada.sort_values(sort_col, ascending=False).head(n)

    return filtrada


def tabla_resumen_periodo(df):
    if df.empty:
        st.info("No hay datos para los filtros seleccionados.")
        return
    rows = []
    for _, r in df.iterrows():
        c = float(r.get("cumplimiento", 0) or 0)
        pill = "good" if c >= 1 else "warn" if c >= .8 else "bad"
        rows.append(f"""
<tr>
<td><span class=\"type-tag {_type_class(r.get('tipo',''))}\">{html.escape(str(r.get('tipo','')))}</span></td>
<td class=\"num\">{_fmt_num(r.get('presupuesto'))}</td>
<td class=\"num\">{_fmt_num(r.get('ejecutado'))}</td>
<td class=\"num\">{_fmt_num(r.get('diferencia'))}</td>
<td class=\"num\"><span class=\"pill {pill}\">{_fmt_pct(c)}</span></td>
<td class=\"num\">{int(r.get('proveedores',0) or 0)}</td>
</tr>
""")
    _render_html(f"""
<div class=\"table-card\"><div class=\"responsive-table-wrap\"><table class=\"pro-table\">
<thead><tr><th>Tipo</th><th class=\"num\">Presupuesto</th><th class=\"num\">Ejecutado</th><th class=\"num\">Diferencia</th><th class=\"num\">Cumplimiento</th><th class=\"num\">Proveedores</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div></div>
""")


def tabla_proveedores(df, titulo="Datos por proveedor", top=None, filtros=False, key=None):
    data = df.copy()
    if top:
        data = data.head(top)
    else:
        data = _ordenar_por_tipo_y_valor(data, valor="ejecutado", asc_valor=False)

    if filtros:
        key = key or _next_table_key("proveedores")
        data = _aplicar_filtros_tabla(data, key, permitir_tipo=True, permitir_cumplimiento=True, permitir_top=True)

    if data.empty:
        st.info("No hay proveedores para los filtros seleccionados.")
        return

    rows = []
    for _, r in data.iterrows():
        c = float(r.get("cumplimiento", 0) or 0)
        pill = "good" if c >= 1 else "warn" if c >= .8 else "bad"
        rows.append(f"""
<tr>
<td>{html.escape(str(r.get('proveedor','')))}</td>
<td><span class="type-tag {_type_class(r.get('tipo',''))}">{html.escape(str(r.get('tipo','')))}</span></td>
<td class="num">{_fmt_num(r.get('presupuesto'))}</td>
<td class="num">{_fmt_num(r.get('ejecutado'))}</td>
<td class="num">{_fmt_num(r.get('diferencia'))}</td>
<td class="num"><span class="pill {pill}">{_fmt_pct(c)}</span></td>
<td class="num">{_fmt_pct(r.get('participacion',0))}</td>
</tr>
""")
    _render_html(f"""
<div class="table-card"><div class="responsive-table-wrap"><table class="pro-table">
<thead><tr><th>Proveedor</th><th>Tipo</th><th class="num">Presupuesto</th><th class="num">Ejecutado</th><th class="num">Diferencia</th><th class="num">Cumplimiento</th><th class="num">Participación</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div></div>
""")


def tabla_calidad(df, filtros=False, key=None):
    df = _ordenar_por_tipo_y_valor(df, valor="maduro", asc_valor=False)
    if filtros:
        key = key or _next_table_key("calidad")
        df = _aplicar_filtros_tabla(df, key, permitir_tipo=True, permitir_cumplimiento=False, permitir_top=True)
    if df.empty:
        st.info("No hay datos de calidad para los filtros seleccionados.")
        return
    rows = []
    for _, r in df.iterrows():
        mad = float(r.get("maduro", 0) or 0)
        verde = float(r.get("verde", 0) or 0)
        sm = float(r.get("sobremaduro", 0) or 0)
        pod = float(r.get("podrido", 0) or 0)
        pl = float(r.get("pedunculo_largo", 0) or 0)
        rows.append(f"""
<tr>
<td>{html.escape(str(r.get('proveedor', r.get('tipo',''))))}</td>
<td><span class=\"type-tag {_type_class(r.get('tipo',''))}\">{html.escape(str(r.get('tipo','')))}</span></td>
<td class=\"num\"><span class=\"pill {'good' if mad >= .89 else 'warn'}\">{_fmt_pct(mad)}</span></td>
<td class=\"num\"><span class=\"pill {'good' if verde <= .01 else 'bad'}\">{_fmt_pct(verde)}</span></td>
<td class=\"num\"><span class=\"pill {'good' if sm <= .10 else 'warn'}\">{_fmt_pct(sm)}</span></td>
<td class=\"num\"><span class=\"pill {'good' if pod <= 0 else 'bad'}\">{_fmt_pct(pod)}</span></td>
<td class=\"num\"><span class=\"pill {'good' if pl <= 0 else 'warn'}\">{_fmt_pct(pl)}</span></td>
</tr>
""")
    _render_html(f"""
<div class=\"table-card\"><div class=\"responsive-table-wrap\"><table class=\"pro-table\">
<thead><tr><th>Proveedor</th><th>Tipo</th><th class=\"num\">Maduro &gt;89%</th><th class=\"num\">Verde &lt;1%</th><th class=\"num\">Sobremaduro &lt;10%</th><th class=\"num\">Podrido 0%</th><th class=\"num\">Pedúnculo 0%</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div></div>
""")


def tabla_matriz_calidad(tabla):
    if tabla.empty:
        st.info("No hay matriz de calidad para estos filtros.")
        return

    data = tabla.copy()
    pct_cols = [c for c in data.columns if c not in ["tipo", "proveedor"]]

    headers = "".join(
        f"<th class=\"{'num' if c in pct_cols else ''}\">{html.escape(str(c))}</th>"
        for c in data.columns
    )

    rows = []
    for _, r in data.iterrows():
        cells = []
        for c in data.columns:
            if c in pct_cols:
                val = r.get(c)
                txt = _fmt_pct(val) if val == val else "—"
                try:
                    raw = float(val)
                except Exception:
                    raw = 0
                pill = "good" if raw >= .89 else "warn" if raw >= .80 else "bad"
                cells.append(f"<td class=\"num\"><span class=\"pill {pill}\">{txt}</span></td>")
            elif c == "tipo":
                cells.append(f"<td><span class=\"type-tag {_type_class(r.get(c, ''))}\">{html.escape(str(r.get(c, '')))}</span></td>")
            else:
                cells.append(f"<td>{html.escape(str(r.get(c, '')))}</td>")
        rows.append(f"<tr>{''.join(cells)}</tr>")

    _render_html(f'''
<div class="table-card"><div class="responsive-table-wrap"><table class="pro-table quality-matrix-table">
<thead><tr>{headers}</tr></thead>
<tbody>{''.join(rows)}</tbody></table></div></div>
''')


def tabla_tendencia_historica(df):
    """Tabla pivote clara para tendencia histórica: años en filas y meses en columnas."""
    if df.empty:
        st.info("No hay datos de tendencia para estos filtros.")
        return

    meses_orden = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
    ]

    pivot = df.pivot_table(
        index="anio",
        columns="mes",
        values="toneladas",
        aggfunc="sum",
        fill_value=0,
    )

    cols = [m for m in meses_orden if m in pivot.columns]
    pivot = pivot[cols]
    pivot["Total"] = pivot.sum(axis=1)
    pivot = pivot.reset_index()

    rows = []
    value_cols = [c for c in pivot.columns if c != "anio"]
    for _, r in pivot.iterrows():
        cells = [f"<td><b>{int(r['anio'])}</b></td>"]
        for c in value_cols:
            cells.append(f"<td class=\"num\">{_fmt_num(r.get(c, 0))}</td>")
        rows.append(f"<tr>{''.join(cells)}</tr>")

    headers = ["Año"] + value_cols
    ths = "".join([f"<th class=\"{'num' if h != 'Año' else ''}\">{html.escape(str(h))}</th>" for h in headers])

    _render_html(f"""
<div class=\"table-card\"><div class=\"responsive-table-wrap\"><table class=\"pro-table trend-table\">
<thead><tr>{ths}</tr></thead>
<tbody>{''.join(rows)}</tbody></table></div></div>
""")
