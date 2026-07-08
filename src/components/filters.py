import streamlit as st


PAGE_OPTIONS = [
    ("Vista general", "⌂", "Resumen ejecutivo"),
    ("Ingreso por proveedor", "♣", "Proveedores"),
    ("Real vs presupuesto", "▮", "Real vs presupuesto"),
    ("Participación Grupo/Terceros", "◔", "Participación Grupo/Terceros"),
    ("Calidad del fruto", "☑", "Calidad del fruto"),
    ("Tendencia histórica", "↗", "Tendencia histórica"),
]


def _default_meses(meses):
    return meses[:1] if meses else []


def _sync_filtros_desde_widgets():
    """Copia los valores visibles a llaves globales que no dependen de la página."""
    for origen, destino in [
        ("ui_filtro_anio", "global_filtro_anio"),
        ("ui_filtro_meses", "global_filtro_meses"),
        ("ui_filtro_tipo", "global_filtro_tipo"),
        ("ui_filtro_proveedor", "global_filtro_proveedor"),
    ]:
        if origen in st.session_state:
            st.session_state[destino] = st.session_state[origen]


def filtros_superiores(ingreso, proveedores=None):
    anios = sorted([int(x) for x in ingreso["anio"].dropna().unique().tolist()])
    meses = ingreso.sort_values("orden_mes")["mes"].dropna().unique().tolist()
    tipos = ["Total", "Grupo", "Terceros"]
    proveedores = proveedores or ["Todos"]
    if "Todos" not in proveedores:
        proveedores = ["Todos"] + proveedores

    # Llaves globales: estas son las que se usan en TODAS las pestañas.
    st.session_state.setdefault("global_filtro_anio", anios[-1] if anios else None)
    st.session_state.setdefault("global_filtro_meses", _default_meses(meses))
    st.session_state.setdefault("global_filtro_tipo", "Total")
    st.session_state.setdefault("global_filtro_proveedor", "Todos")

    if st.session_state.get("reset_filters", False):
        st.session_state["global_filtro_anio"] = anios[-1] if anios else None
        st.session_state["global_filtro_meses"] = _default_meses(meses)
        st.session_state["global_filtro_tipo"] = "Total"
        st.session_state["global_filtro_proveedor"] = "Todos"
        st.session_state["reset_filters"] = False

    # Validaciones sin reiniciar por cambiar de menú.
    if st.session_state.get("global_filtro_anio") not in anios and anios:
        st.session_state["global_filtro_anio"] = anios[-1]
    st.session_state["global_filtro_meses"] = [
        m for m in st.session_state.get("global_filtro_meses", []) if m in meses
    ] or _default_meses(meses)
    if st.session_state.get("global_filtro_tipo") not in tipos:
        st.session_state["global_filtro_tipo"] = "Total"
    if st.session_state.get("global_filtro_proveedor") not in proveedores:
        st.session_state["global_filtro_proveedor"] = "Todos"

    # Sincroniza los widgets desde las llaves globales antes de pintarlos.
    st.session_state["ui_filtro_anio"] = st.session_state["global_filtro_anio"]
    st.session_state["ui_filtro_meses"] = st.session_state["global_filtro_meses"]
    st.session_state["ui_filtro_tipo"] = st.session_state["global_filtro_tipo"]
    st.session_state["ui_filtro_proveedor"] = st.session_state["global_filtro_proveedor"]

    st.markdown(
        """
        <div class="filter-card">
            <div class="filter-title-row">
                <i class="ph ph-funnel-simple"></i>
                <span>Filtros de análisis</span>
            </div>
        """,
        unsafe_allow_html=True,
    )

    col0, col1, col2, col3, col4 = st.columns([.75, 1.7, 1.0, 1.4, .75])

    with col0:
        anio = st.selectbox(
            "AÑO",
            anios,
            key="ui_filtro_anio",
            on_change=_sync_filtros_desde_widgets,
        )

    with col1:
        meses_sel = st.multiselect(
            "MES",
            meses,
            key="ui_filtro_meses",
            on_change=_sync_filtros_desde_widgets,
        )
        if not meses_sel:
            meses_sel = _default_meses(meses)
            st.session_state["ui_filtro_meses"] = meses_sel
            st.session_state["global_filtro_meses"] = meses_sel

    with col2:
        tipo = st.selectbox(
            "TIPO",
            tipos,
            key="ui_filtro_tipo",
            on_change=_sync_filtros_desde_widgets,
        )

    with col3:
        proveedor = st.selectbox(
            "PROVEEDOR",
            proveedores,
            key="ui_filtro_proveedor",
            on_change=_sync_filtros_desde_widgets,
        )

    # Refuerzo final: en cada ejecución guarda lo seleccionado, así al cambiar pestaña no se pierde.
    st.session_state["global_filtro_anio"] = anio
    st.session_state["global_filtro_meses"] = meses_sel
    st.session_state["global_filtro_tipo"] = tipo
    st.session_state["global_filtro_proveedor"] = proveedor

    with col4:
        st.markdown('<div class="filter-button-spacer"></div>', unsafe_allow_html=True)
        if st.button("Limpiar", use_container_width=True, key="btn_limpiar_filtros"):
            st.session_state["reset_filters"] = True
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    return int(anio), meses_sel, tipo, proveedor


def selector_pagina():
    """Menú funcional alineado a la izquierda y sin limpiar filtros."""
    if "pagina_dashboard" not in st.session_state:
        st.session_state["pagina_dashboard"] = "Vista general"

    current = st.session_state.get("pagina_dashboard", "Vista general")
    paginas = [page for page, _, _ in PAGE_OPTIONS]
    iconos = {page: icon for page, icon, _ in PAGE_OPTIONS}
    labels = {page: label for page, _, label in PAGE_OPTIONS}

    if current not in paginas:
        current = paginas[0]
        st.session_state["pagina_dashboard"] = current

    st.sidebar.markdown('<div class="menu-title">NAVEGACIÓN</div>', unsafe_allow_html=True)

    seleccionado = st.sidebar.radio(
        "Navegación",
        paginas,
        index=paginas.index(current),
        format_func=lambda page: f"{iconos[page]}  {labels[page]}",
        key="pagina_dashboard_radio",
        label_visibility="collapsed",
    )

    st.session_state["pagina_dashboard"] = seleccionado
    return seleccionado
