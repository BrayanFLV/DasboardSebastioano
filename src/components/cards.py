import streamlit as st


def _formatear_valor(valor, unidad):
    try:
        if unidad == "%":
            return f"{valor:.1%}"
        if abs(valor) >= 1000:
            return f"{valor:,.0f} {unidad}"
        return f"{valor:,.1f} {unidad}".strip()
    except Exception:
        return str(valor)


def card_kpi(titulo, valor, unidad="", subtitulo="", icono="ph-chart-bar", tipo=""):
    texto = _formatear_valor(valor, unidad)
    clase = f"kpi-card {tipo}".strip()

    st.markdown(
        f"""
        <div class="{clase}">
            <div class="kpi-top">
                <div class="kpi-label">{titulo}</div>
                <div class="kpi-icon"><i class="ph {icono}"></i></div>
            </div>
            <div class="kpi-value">{texto}</div>
            <div class="kpi-sub">{subtitulo}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
