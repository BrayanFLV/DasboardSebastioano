import streamlit as st


def aplicar_estilos():
    CSS = r"""
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css">
        <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/fill/style.css">

        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        :root {
            --bg: #f4f8f1;
            --panel: #ffffff;
            --panel-soft: #f8fcf6;
            --green: #0f4c33;
            --green-2: #4f9b3f;
            --green-3: #dff0da;
            --orange: #f28c28;
            --blue: #2d7dd2;
            --red: #cf4f3f;
            --text: #17251d;
            --muted: #6f7d75;
            --faint: #93a198;
            --line: #dce7db;
            --shadow: 0 18px 45px rgba(21, 64, 42, .10);
            --shadow-soft: 0 10px 24px rgba(21, 64, 42, .07);
            --radius: 20px;
        }

        html, body, .stApp {
            background:
                radial-gradient(900px 500px at 88%% -15%%, rgba(242,140,40,.15), transparent 60%%),
                radial-gradient(720px 420px at -5%% 5%%, rgba(79,155,63,.18), transparent 60%%),
                var(--bg);
            font-family: 'Inter', sans-serif;
            color: var(--text);
        }

        .block-container {
            max-width: 1500px;
            padding-top: 1.35rem;
            padding-bottom: 4rem;
        }

        header[data-testid="stHeader"] { background: transparent; }
        #MainMenu, footer { visibility: hidden; }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #e7f2e2, #f8fbf5);
            border-right: 1px solid var(--line);
        }
        [data-testid="stSidebar"] * { color: var(--text) !important; }
        [data-testid="stSidebar"] > div { padding-top: 1.2rem; }

        .brand {
            display: flex;
            align-items: center;
            gap: 13px;
            margin: 8px 0 34px;
        }
        .brand-icon {
            width: 52px;
            height: 52px;
            display: grid;
            place-items: center;
            border-radius: 17px;
            background: linear-gradient(135deg, #ffffff, #dff0da);
            border: 1px solid var(--line);
            box-shadow: var(--shadow-soft);
        }
        .brand-icon i { font-size: 34px; color: var(--green); }
        .brand-title {
            font-weight: 900;
            font-size: 17px;
            letter-spacing: .04em;
            color: var(--green) !important;
            line-height: 1.05;
        }
        .brand-sub {
            margin-top: 4px;
            font-size: 11px;
            letter-spacing: .32em;
            color: var(--green-2) !important;
            font-weight: 800;
        }
        .menu-title {
            margin: 26px 0 10px;
            font-size: 11px;
            font-weight: 900;
            letter-spacing: .14em;
            color: #7b917d !important;
        }
        .menu-item, .menu-active {
            display: flex;
            align-items: center;
            gap: 11px;
            padding: 13px 15px;
            border-radius: 15px;
            margin-bottom: 8px;
            font-size: 14px;
            font-weight: 700;
            color: var(--muted) !important;
        }
        .menu-item i, .menu-active i {
            font-size: 19px;
            color: var(--green-2) !important;
        }
        .menu-active {
            color: var(--green) !important;
            background: linear-gradient(90deg, #dff0da, #f8fbf5);
            border-left: 4px solid var(--green-2);
            box-shadow: var(--shadow-soft);
        }
        .menu-active i { color: var(--green) !important; }

        /* Topbar */
        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
            margin-bottom: 18px;
        }
        .page-kicker {
            color: var(--orange);
            font-size: 12px;
            font-weight: 900;
            letter-spacing: .16em;
            text-transform: uppercase;
            margin-bottom: 3px;
        }
        .topbar h1 {
            margin: 0;
            color: var(--green);
            font-size: 32px;
            font-weight: 900;
            letter-spacing: -.04em;
        }
        .top-actions {
            display: flex;
            align-items: center;
            gap: 11px;
            flex-wrap: wrap;
        }
        .action-pill {
            display: inline-flex;
            align-items: center;
            gap: 9px;
            border: 1px solid var(--line);
            background: white;
            border-radius: 14px;
            padding: 11px 16px;
            font-size: 13px;
            font-weight: 800;
            color: var(--text);
            box-shadow: var(--shadow-soft);
        }
        .action-pill i { font-size: 18px; color: var(--green-2); }
        .action-pill.primary {
            color: white;
            border-color: var(--green);
            background: linear-gradient(135deg, var(--green), #1f6a49);
        }
        .action-pill.primary i { color: white; }

        /* Hero */
        .hero-card {
            background: linear-gradient(135deg, #ffffff 0%%, #ffffff 55%%, #eff8eb 100%);
            border: 1px solid var(--line);
            border-radius: 24px;
            padding: 30px 34px;
            box-shadow: var(--shadow);
            display: grid;
            grid-template-columns: 1.55fr .92fr;
            gap: 32px;
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
        }
        .hero-card::after {
            content: "";
            position: absolute;
            right: 42%%;
            top: 15px;
            width: 180px;
            height: 180px;
            border-radius: 50%%;
            background: rgba(79,155,63,.08);
        }
        .hero-card::before {
            content: "";
            position: absolute;
            right: -45px;
            bottom: -60px;
            width: 220px;
            height: 220px;
            border-radius: 55px;
            background: rgba(242,140,40,.09);
            transform: rotate(25deg);
        }
        .hero-left, .hero-meta { position: relative; z-index: 2; }
        .eyebrow {
            color: var(--orange);
            font-size: 12px;
            font-weight: 900;
            letter-spacing: .16em;
            margin-bottom: 10px;
        }
        .hero-title {
            color: var(--green);
            font-size: 33px;
            font-weight: 900;
            letter-spacing: -.04em;
            margin-bottom: 12px;
        }
        .hero-desc {
            max-width: 720px;
            color: var(--muted);
            font-size: 15px;
            line-height: 1.6;
        }
        .legend-row {
            display: flex;
            gap: 19px;
            margin-top: 23px;
            color: var(--muted);
            font-size: 13px;
            font-weight: 700;
            flex-wrap: wrap;
        }
        .dot {
            width: 10px;
            height: 10px;
            display: inline-block;
            border-radius: 3px;
            margin-right: 7px;
        }
        .orange { background: var(--orange); }
        .green { background: var(--green-2); }
        .blue { background: var(--blue); }
        .hero-meta {
            border-left: 1px dashed #c9d9c4;
            padding-left: 32px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 17px;
        }
        .meta-item {
            display: flex;
            align-items: center;
            gap: 14px;
        }
        .meta-item > i {
            min-width: 44px;
            width: 44px;
            height: 44px;
            border-radius: 50%%;
            background: #eaf6e6;
            display: grid;
            place-items: center;
            color: var(--green);
            font-size: 24px;
            border: 1px solid #d7e8d2;
        }
        .meta-item small {
            display: block;
            color: var(--muted);
            font-size: 12px;
            font-weight: 800;
            margin-bottom: 3px;
        }
        .meta-item b {
            color: var(--text);
            font-size: 14px;
            font-weight: 900;
        }

        /* Filters */
        .filter-title-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 18px 0 8px;
            color: var(--muted);
            font-weight: 900;
            font-size: 13px;
        }
        .filter-title-row i { color: var(--green-2); font-size: 18px; }
        div[data-testid="stSelectbox"] label {
            color: var(--muted) !important;
            font-size: 12px !important;
            font-weight: 900 !important;
            letter-spacing: .04em;
        }
        div[data-baseweb="select"] > div {
            border-radius: 14px !important;
            border-color: var(--line) !important;
            background-color: #ffffff !important;
            box-shadow: var(--shadow-soft);
        }
        .stButton > button {
            border-radius: 14px;
            border: 1px solid var(--line);
            background: white;
            color: var(--green);
            font-weight: 900;
            box-shadow: var(--shadow-soft);
            min-height: 43px;
        }

        /* Custom KPI */
        .kpi-card {
            background: linear-gradient(180deg, #ffffff, #fbfdf9);
            border: 1px solid var(--line);
            border-radius: 20px;
            padding: 17px 16px;
            box-shadow: var(--shadow);
            min-height: 142px;
            position: relative;
            overflow: hidden;
        }
        .kpi-card::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: var(--orange);
        }
        .kpi-card.good::before { background: var(--green-2); }
        .kpi-card.bad::before { background: var(--red); }
        .kpi-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            margin-bottom: 14px;
        }
        .kpi-icon {
            width: 42px;
            height: 42px;
            border-radius: 14px;
            display: grid;
            place-items: center;
            background: #eef7e9;
            color: var(--green);
            border: 1px solid #d9ead4;
        }
        .kpi-icon i { font-size: 23px; }
        .kpi-label {
            color: var(--muted);
            font-size: 11px;
            font-weight: 900;
            letter-spacing: .06em;
            text-transform: uppercase;
            line-height: 1.25;
        }
        .kpi-value {
            color: var(--text);
            font-size: 25px;
            font-weight: 900;
            letter-spacing: -.03em;
            line-height: 1.05;
        }
        .kpi-sub {
            margin-top: 8px;
            color: var(--faint);
            font-size: 12px;
            font-weight: 700;
        }

        /* Sections and panels */
        .section-head {
            display: flex;
            justify-content: space-between;
            margin: 30px 0 12px;
        }
        .section-head.compact { margin-top: 24px; }
        .section-code {
            color: var(--orange);
            font-size: 12px;
            font-weight: 900;
            letter-spacing: .14em;
        }
        .section-head h2 {
            color: var(--text);
            margin: 6px 0 3px;
            font-size: 24px;
            font-weight: 900;
            letter-spacing: -.02em;
        }
        .section-head p {
            color: var(--muted);
            margin: 0;
            font-size: 14px;
        }
        .chart-title {
            display: flex;
            align-items: center;
            gap: 9px;
            background: white;
            border: 1px solid var(--line);
            border-bottom: none;
            border-radius: 20px 20px 0 0;
            padding: 16px 20px 6px;
            font-weight: 900;
            color: var(--text);
            font-size: 16px;
            box-shadow: var(--shadow-soft);
        }
        .chart-title i { color: var(--green-2); font-size: 20px; }
        div[data-testid="stPlotlyChart"] {
            background: white;
            border: 1px solid var(--line);
            border-top: none;
            border-radius: 0 0 20px 20px;
            padding: 6px 14px 14px;
            box-shadow: var(--shadow);
        }
        div[data-testid="stDataFrame"] {
            background: white;
            border: 1px solid var(--line);
            border-top: none;
            border-radius: 0 0 20px 20px;
            padding: 12px;
            box-shadow: var(--shadow);
        }


        /* ===== Resumen Ejecutivo V2 - tarjetas premium ===== */
        .executive-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.05fr) minmax(0, 1.35fr);
            gap: 18px;
            margin: 18px 0 22px;
            align-items: stretch;
        }
        .executive-card {
            position: relative;
            overflow: hidden;
            border: 1px solid #cfe0ca;
            border-radius: 24px;
            padding: 22px 24px;
            background:
                radial-gradient(circle at top right, rgba(79,155,63,.17), transparent 34%),
                linear-gradient(135deg, #ffffff 0%, #f7fbf5 100%);
            box-shadow: 0 18px 42px rgba(15,76,51,.10);
            min-height: 206px;
        }
        .executive-card::before {
            content: "";
            position: absolute;
            inset: 0 auto 0 0;
            width: 7px;
            background: linear-gradient(180deg, var(--green-2), var(--orange));
        }
        .executive-card.narrative h3 {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 10px 0 10px;
            color: var(--text);
            font-size: clamp(25px, 3vw, 36px);
            line-height: 1.05;
            font-weight: 950;
            letter-spacing: -.04em;
        }
        .executive-card.narrative p {
            color: var(--muted);
            font-size: 14px;
            line-height: 1.55;
            margin: 0 0 18px;
            max-width: 720px;
        }
        .exec-kicker {
            color: var(--green-2);
            font-weight: 950;
            letter-spacing: .14em;
            font-size: 11px;
            text-transform: uppercase;
        }
        .exec-mini-row {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin-top: 16px;
        }
        .exec-mini-row span {
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 78px;
            padding: 14px 16px;
            border: 1px solid #d7e7d2;
            border-radius: 18px;
            background: rgba(255,255,255,.82);
            box-shadow: 0 10px 25px rgba(15,76,51,.06);
        }
        .exec-mini-row b {
            display: block;
            font-size: clamp(18px, 2.2vw, 25px);
            line-height: 1.1;
            font-weight: 950;
            color: var(--text);
            white-space: nowrap;
        }
        .exec-mini-row small {
            margin-top: 6px;
            color: var(--faint);
            font-size: 11px;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: .08em;
        }
        .executive-card.insights {
            background:
                radial-gradient(circle at top right, rgba(242,140,40,.16), transparent 36%),
                linear-gradient(135deg, #ffffff 0%, #fbfaf4 100%);
        }
        .executive-card.insights.good::before { background: linear-gradient(180deg, #42b86b, #0f4c33); }
        .executive-card.insights.warn::before { background: linear-gradient(180deg, #f6b14a, #f28c28); }
        .executive-card.insights.bad::before { background: linear-gradient(180deg, #de6a55, #cf4f3f); }
        .executive-card.insights ul {
            margin: 16px 0 0;
            padding: 0;
            list-style: none;
            display: grid;
            gap: 10px;
        }
        .executive-card.insights li {
            position: relative;
            padding: 12px 14px 12px 42px;
            border: 1px solid #e1eadf;
            border-radius: 16px;
            background: rgba(255,255,255,.82);
            color: var(--text);
            font-size: 14px;
            line-height: 1.35;
            box-shadow: 0 8px 20px rgba(15,76,51,.045);
        }
        .executive-card.insights li::before {
            content: "✓";
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            width: 20px;
            height: 20px;
            border-radius: 999px;
            display: grid;
            place-items: center;
            background: #e7f4e3;
            color: var(--green-2);
            font-size: 12px;
            font-weight: 950;
        }
        .empty-state {
            min-height: 330px;
            display: grid;
            place-items: center;
            text-align: center;
            gap: 6px;
            background: white;
            border: 1px solid var(--line);
            border-top: none;
            border-radius: 0 0 20px 20px;
            box-shadow: var(--shadow);
            color: var(--muted);
            padding: 24px;
        }
        .empty-state b {
            display: block;
            color: var(--text);
            font-size: 18px;
            margin-bottom: 6px;
        }
        @media (max-width: 1050px) {
            .executive-grid { grid-template-columns: 1fr; }
            .exec-mini-row { grid-template-columns: repeat(3, minmax(130px, 1fr)); }
        }
        @media (max-width: 680px) {
            .executive-card { padding: 18px; border-radius: 20px; }
            .exec-mini-row { grid-template-columns: 1fr; }
            .executive-card.insights li { font-size: 13px; }
        }

        @media (max-width: 1100px) {
            .hero-card { grid-template-columns: 1fr; }
            .hero-meta { border-left: none; border-top: 1px dashed #c9d9c4; padding-left: 0; padding-top: 22px; }
            .topbar { flex-direction: column; align-items: flex-start; }
        }


        /* ===== Ajustes PRO v4: filtros visibles, hover y tabla responsive ===== */
        .topbar-grid {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 22px;
            align-items: center;
            margin-bottom: 18px;
        }
        .topbar-actions-real {
            display: flex;
            gap: 10px;
            align-items: center;
            justify-content: flex-end;
            flex-wrap: wrap;
        }
        .period-pill-real {
            display: inline-flex;
            align-items: center;
            min-height: 44px;
            padding: 0 18px;
            border-radius: 14px;
            border: 1px solid var(--line);
            background: #fff;
            color: var(--text);
            font-size: 13px;
            font-weight: 900;
            box-shadow: var(--shadow-soft);
            white-space: nowrap;
        }

        .filter-card {
            background: rgba(255, 255, 255, .58);
            border: 1px solid rgba(220, 231, 219, .85);
            border-radius: 20px;
            padding: 16px 18px 18px;
            margin: 18px 0 16px;
            box-shadow: 0 14px 32px rgba(21, 64, 42, .07);
            backdrop-filter: blur(8px);
        }
        .filter-title-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 0 0 10px;
            color: var(--green) !important;
            font-weight: 900;
            font-size: 13px;
        }
        .filter-title-row i { color: var(--green-2) !important; font-size: 18px; }
        .filter-button-spacer { height: 27px; }

        div[data-testid="stSelectbox"] label {
            color: var(--green) !important;
            font-size: 12px !important;
            font-weight: 900 !important;
            letter-spacing: .06em;
        }
        div[data-baseweb="select"],
        div[data-baseweb="select"] > div {
            background: #ffffff !important;
            border-radius: 14px !important;
            border-color: var(--line) !important;
            color: var(--text) !important;
            min-height: 44px !important;
            box-shadow: var(--shadow-soft);
        }
        div[data-baseweb="select"] *,
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div {
            color: var(--text) !important;
            opacity: 1 !important;
        }
        div[data-baseweb="popover"] * {
            color: var(--text) !important;
        }

        .stButton > button,
        .stDownloadButton > button {
            border-radius: 14px !important;
            border: 1px solid var(--line) !important;
            background: white !important;
            color: var(--green) !important;
            font-weight: 900 !important;
            box-shadow: var(--shadow-soft) !important;
            min-height: 44px !important;
            transition: all .18s ease !important;
        }
        .stButton > button:hover,
        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            border-color: var(--green-2) !important;
            box-shadow: 0 18px 34px rgba(21, 64, 42, .13) !important;
        }

        .kpi-card {
            transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
            cursor: default;
        }
        .kpi-card:hover {
            transform: translateY(-6px) scale(1.01);
            box-shadow: 0 24px 55px rgba(21, 64, 42, .18);
            border-color: rgba(79,155,63,.45);
        }
        .kpi-card:hover .kpi-icon {
            transform: rotate(-4deg) scale(1.08);
            background: #e2f3dc;
        }
        .kpi-icon { transition: transform .18s ease, background .18s ease; }
        .menu-item { transition: all .16s ease; }
        .menu-item:hover {
            background: rgba(255,255,255,.55);
            transform: translateX(4px);
            color: var(--green) !important;
        }

        .table-card {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 0 0 20px 20px;
            padding: 14px;
            box-shadow: var(--shadow);
            overflow: hidden;
        }
        .responsive-table-wrap {
            width: 100%;
            overflow-x: auto;
            border-radius: 14px;
        }
        .pro-table {
            width: 100%;
            min-width: 850px;
            border-collapse: separate;
            border-spacing: 0;
            font-size: 13px;
            color: var(--text);
        }
        .pro-table thead th {
            position: sticky;
            top: 0;
            background: #f3f8f0;
            color: var(--green);
            text-align: left;
            padding: 13px 14px;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: .07em;
            border-bottom: 1px solid var(--line);
            white-space: nowrap;
        }
        .pro-table tbody td {
            padding: 13px 14px;
            border-bottom: 1px solid #edf3ea;
            font-weight: 700;
            white-space: nowrap;
        }
        .pro-table tbody tr {
            background: #ffffff;
            transition: background .14s ease, transform .14s ease;
        }
        .pro-table tbody tr:hover {
            background: #f5fbf2;
        }
        .pro-table tbody tr.selected-row {
            background: #eaf6e6;
            box-shadow: inset 4px 0 0 var(--green-2);
        }
        .pro-table .num { text-align: right; font-variant-numeric: tabular-nums; }
        .type-tag {
            display: inline-flex;
            padding: 4px 9px;
            border-radius: 999px;
            background: #eef7e9;
            color: var(--green);
            border: 1px solid #d8ead2;
            font-size: 12px;
            font-weight: 900;
        }
        .pill {
            display: inline-flex;
            padding: 4px 9px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 900;
        }
        .pill.good { background: #dff0da; color: var(--green); }
        .pill.warn { background: #fff0dc; color: #b05f0f; }
        .pill.bad { background: #fde8e4; color: var(--red); }

        @media (max-width: 900px) {
            .topbar-grid { grid-template-columns: 1fr; }
            .topbar-actions-real { justify-content: flex-start; }
            .filter-card { padding: 14px; }
            .pro-table { min-width: 760px; }
        }

                /* ==========================================
        FIX DROPDOWNS STREAMLIT
        ========================================== */

        .stSelectbox div[data-baseweb="select"] {
            background: #ffffff !important;
            color: #0f2f21 !important;
            border: 1px solid #d7e4d3 !important;
            border-radius: 14px !important;
        }

        .stSelectbox div[data-baseweb="select"] * {
            color: #0f2f21 !important;
        }

        /* Popup del dropdown */
        div[data-baseweb="popover"] {
            background: #ffffff !important;
        }

        /* Lista de opciones */
        ul[role="listbox"] {
            background: #ffffff !important;
            border: 1px solid #d7e4d3 !important;
            border-radius: 14px !important;
            box-shadow: 0 18px 40px rgba(15, 76, 51, 0.16) !important;
        }

        /* Opciones */
        li[role="option"] {
            background: #ffffff !important;
            color: #0f2f21 !important;
            font-weight: 600 !important;
        }

        /* Hover */
        li[role="option"]:hover {
            background: #eaf5e6 !important;
            color: #0f4c33 !important;
        }

        /* Seleccionado */
        li[aria-selected="true"] {
            background: #dff0d8 !important;
            color: #0f4c33 !important;
        }

        /* Botones */
        .stButton button {
            background: #ffffff !important;
            color: #0f4c33 !important;
            border: 1px solid #d7e4d3 !important;
            border-radius: 14px !important;
            font-weight: 700 !important;
            height: 46px !important;
            transition: all .2s ease;
        }

        .stButton button:hover {
            background: #eaf5e6 !important;
            border-color: #4f9b3f !important;
            transform: translateY(-2px);
            box-shadow: 0 12px 28px rgba(15, 76, 51, 0.12);
        }



        /* Multiselect sin chips rojos */
        div[data-baseweb="tag"] {
            background: #eaf5e6 !important;
            border: 1px solid #cfe5c8 !important;
            border-radius: 999px !important;
            color: var(--green) !important;
            font-weight: 900 !important;
        }
        div[data-baseweb="tag"] span,
        div[data-baseweb="tag"] svg {
            color: var(--green) !important;
            fill: var(--green) !important;
        }

        /* Navegación funcional del sidebar con el mismo diseño */
        [data-testid="stSidebar"] .stButton > button {
            justify-content: flex-start !important;
            padding: 13px 15px !important;
            border-radius: 15px !important;
            margin-bottom: 8px !important;
            background: transparent !important;
            border: 1px solid transparent !important;
            box-shadow: none !important;
            color: var(--muted) !important;
            font-weight: 800 !important;
            min-height: 46px !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255,255,255,.62) !important;
            transform: translateX(4px) !important;
            color: var(--green) !important;
            border-color: rgba(220,231,219,.8) !important;
            box-shadow: var(--shadow-soft) !important;
        }
        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            color: var(--green) !important;
            background: linear-gradient(90deg, #dff0da, #f8fbf5) !important;
            border-left: 4px solid var(--green-2) !important;
            box-shadow: var(--shadow-soft) !important;
        }

        /* Dataframe nativo claro cuando se use */
        div[data-testid="stDataFrame"] {
            background: #ffffff !important;
            border: 1px solid var(--line) !important;
            border-radius: 20px !important;
            padding: 10px !important;
            box-shadow: var(--shadow) !important;
        }


        /* Navegación principal con iconos */
        .nav-link {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 13px 16px;
            margin: 7px 0;
            border-radius: 16px;
            color: var(--text) !important;
            text-decoration: none !important;
            font-weight: 850;
            transition: all .18s ease;
        }
        .nav-link i {
            color: var(--green-2) !important;
            font-size: 18px;
        }
        .nav-link:hover {
            background: rgba(255,255,255,.65);
            transform: translateX(4px);
            color: var(--green) !important;
        }
        .nav-link.active {
            background: linear-gradient(90deg, #dff0da, #ffffff);
            box-shadow: inset 4px 0 0 var(--green-2), 0 12px 26px rgba(21,64,42,.08);
            color: var(--green) !important;
        }

        /* Multiselect: chips en verde claro, no rojo */
        [data-testid="stMultiSelect"] div[data-baseweb="tag"],
        [data-testid="stMultiSelect"] span[data-baseweb="tag"],
        div[data-baseweb="tag"] {
            background-color: #e6f4df !important;
            border: 1px solid #b9ddb0 !important;
            border-radius: 10px !important;
            color: var(--green) !important;
        }
        [data-testid="stMultiSelect"] div[data-baseweb="tag"] span,
        [data-testid="stMultiSelect"] div[data-baseweb="tag"] svg,
        div[data-baseweb="tag"] span,
        div[data-baseweb="tag"] svg {
            color: var(--green) !important;
            fill: var(--green) !important;
        }
        [data-testid="stMultiSelect"] div[data-baseweb="select"] {
            background: #ffffff !important;
        }

        .quality-matrix-table .pill {
            min-width: 62px;
            justify-content: center;
        }


        /* FIX FINAL: multiselect sin chips rojos en cualquier tema */
        [data-testid="stMultiSelect"] span[data-baseweb="tag"],
        [data-testid="stMultiSelect"] div[data-baseweb="tag"],
        [data-testid="stMultiSelect"] [data-baseweb="tag"],
        span[data-baseweb="tag"],
        div[data-baseweb="tag"] {
            background: #e6f4df !important;
            background-color: #e6f4df !important;
            border: 1px solid #b9ddb0 !important;
            border-radius: 10px !important;
            color: var(--green) !important;
            box-shadow: none !important;
        }
        [data-testid="stMultiSelect"] [data-baseweb="tag"] *,
        span[data-baseweb="tag"] *,
        div[data-baseweb="tag"] * {
            color: var(--green) !important;
            fill: var(--green) !important;
            background: transparent !important;
        }
        [data-testid="stMultiSelect"] [data-baseweb="tag"] button,
        [data-testid="stMultiSelect"] [data-baseweb="tag"] svg {
            color: var(--green) !important;
            fill: var(--green) !important;
        }

        /* Menú lateral funcional con botones, mismo look e iconos */
        [data-testid="stSidebar"] .stButton > button {
            justify-content: flex-start !important;
            text-align: left !important;
            gap: 11px !important;
            padding: 13px 15px !important;
            border-radius: 15px !important;
            margin-bottom: 8px !important;
            background: transparent !important;
            border: 1px solid transparent !important;
            box-shadow: none !important;
            color: var(--text) !important;
            font-weight: 850 !important;
            min-height: 46px !important;
        }
        [data-testid="stSidebar"] .stButton > button p,
        [data-testid="stSidebar"] .stButton > button span {
            color: var(--text) !important;
            font-weight: 850 !important;
        }
        [data-testid="stSidebar"] .stButton > button svg {
            color: var(--green-2) !important;
            fill: var(--green-2) !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255,255,255,.65) !important;
            transform: translateX(4px) !important;
            color: var(--green) !important;
            border-color: rgba(220,231,219,.8) !important;
            box-shadow: var(--shadow-soft) !important;
        }
        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: linear-gradient(90deg, #dff0da, #ffffff) !important;
            box-shadow: inset 4px 0 0 var(--green-2), 0 12px 26px rgba(21,64,42,.08) !important;
            color: var(--green) !important;
            border-color: transparent !important;
        }
        [data-testid="stSidebar"] .stButton > button[kind="primary"] p,
        [data-testid="stSidebar"] .stButton > button[kind="primary"] span,
        [data-testid="stSidebar"] .stButton > button[kind="primary"] svg {
            color: var(--green) !important;
            fill: var(--green) !important;
        }




        /* ==================================================
           RESPONSIVE FINAL - no cambia el diseño, lo adapta
        ================================================== */
        .kpi-responsive-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin: 18px 0 28px;
            align-items: stretch;
        }
        .kpi-responsive-grid .kpi-card {
            width: 100%;
            min-width: 0;
            height: 100%;
        }
        .kpi-responsive-grid .kpi-value {
            overflow-wrap: anywhere;
        }

        /* Hace que las columnas de Streamlit bajen mejor cuando la pantalla es estrecha */
        @media (max-width: 1200px) {
            .hero-card {
                grid-template-columns: 1fr;
                gap: 22px;
            }
            .hero-meta {
                border-left: none !important;
                border-top: 1px dashed #cddccb;
                padding-left: 0 !important;
                padding-top: 20px;
                display: grid !important;
                grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
            }
            .kpi-responsive-grid {
                grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            }
            .topbar-title h1,
            .topbar h1 {
                font-size: clamp(26px, 4vw, 34px) !important;
            }
        }

        @media (max-width: 900px) {
            .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
            .hero-card {
                padding: 22px 20px;
                border-radius: 20px;
            }
            .hero-title { font-size: 28px; }
            .hero-desc { font-size: 14px; }
            .legend-row { flex-wrap: wrap; gap: 10px; }
            .kpi-responsive-grid {
                grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
                gap: 12px;
            }
            .kpi-card {
                min-height: 128px;
                padding: 15px 14px;
            }
            .kpi-value { font-size: clamp(18px, 4.6vw, 24px); }
            .kpi-label { font-size: 10px; }
            .kpi-icon { width: 36px; height: 36px; }
            .chart-title { font-size: 14px; }
            .section-head h2 { font-size: 22px; }
            .pro-table { min-width: 720px; }
        }

        @media (max-width: 640px) {
            .kpi-responsive-grid {
                grid-template-columns: 1fr 1fr;
            }
            .hero-meta {
                grid-template-columns: 1fr;
            }
            .brand-title { font-size: 15px; }
            .brand-sub { letter-spacing: .22em; }
        }

        /* Multiselect: forzar chips verdes, anulando el color rojo de Streamlit/Baseweb */
        [data-testid="stMultiSelect"] [data-baseweb="tag"],
        [data-testid="stMultiSelect"] [data-baseweb="tag"] > span,
        [data-testid="stMultiSelect"] [data-baseweb="tag"] div,
        [data-testid="stMultiSelect"] [data-baseweb="tag"] button,
        [data-baseweb="tag"] {
            background: #e6f4df !important;
            background-color: #e6f4df !important;
            border-color: #b9ddb0 !important;
            color: var(--green) !important;
            box-shadow: none !important;
        }
        [data-testid="stMultiSelect"] [data-baseweb="tag"] *,
        [data-baseweb="tag"] * {
            color: var(--green) !important;
            fill: var(--green) !important;
        }
        [data-testid="stMultiSelect"] [aria-label="close"],
        [data-testid="stMultiSelect"] [aria-label="Clear all"] {
            color: var(--green) !important;
            fill: var(--green) !important;
        }

        /* Mejor lectura de ejes en gráficas y evitar cortes visuales */
        div[data-testid="stPlotlyChart"] {
            min-width: 0 !important;
            overflow: hidden !important;
        }
        .js-plotly-plot, .plotly, .plot-container {
            max-width: 100% !important;
        }


/* Iconos internos sin depender de CDN: reemplazo para clases ph */
.ph {
    display:inline-block !important;
    width:1em !important;
    height:1em !important;
    vertical-align:-0.16em !important;
    background-color: currentColor !important;
    -webkit-mask: var(--icon) no-repeat center / contain !important;
    mask: var(--icon) no-repeat center / contain !important;
    font-style: normal !important;
    flex: 0 0 auto !important;
}
.ph-tree-palm{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M12%2022h-2l1-9C8%2014%205%2016%203%2019c0-4%202-8%206-10-3%200-6%201-8%203%201-4%205-7%209-7-2-2-3-3-7-3%204-2%209-1%2012%203%202-2%205-3%208-2-3%201-5%203-6%206%203%200%205%202%206%205-3-2-6-2-9-1l-2%209z'/%3E%3C/svg%3E");}
.ph-sliders-horizontal{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M4%207h8v2H4V7zm10-2h2v2h4v2h-4v2h-2V5zM4%2015h4v2H4v-2zm6-2h2v2h8v2h-8v2h-2v-6z'/%3E%3C/svg%3E");}
.ph-user-circle{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M12%202a10%2010%200%20100%2020%2010%2010%200%20000-20zm0%203a3%203%200%20110%206%203%203%200%20010-6zm0%2015a8%208%200%2001-6-2.7c1.2-2.2%203.4-3.3%206-3.3s4.8%201.1%206%203.3A8%208%200%200112%2020z'/%3E%3C/svg%3E");}
.ph-calendar-check{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M7%202h2v2h6V2h2v2h3v18H4V4h3V2zm11%208H6v10h12V10zM6%208h12V6H6v2zm5%209l-3-3%201.4-1.4L11%2014.2l3.6-3.6L16%2012l-5%205z'/%3E%3C/svg%3E");}
.ph-clock-countdown{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M12%202a10%2010%200%201010%2010h-2a8%208%200%2011-2.3-5.7L15%209h7V2l-2.9%202.9A10%2010%200%200012%202zm1%205h-2v6l5%203%201-1.7-4-2.3V7z'/%3E%3C/svg%3E");}
.ph-users-three{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M12%2012a4%204%200%20100-8%204%204%200%20000%208zm0%202c-4%200-7%202-7%205v1h14v-1c0-3-3-5-7-5zM5%2011a3%203%200%20110-6%203%203%200%20010%206zm14%200a3%203%200%20100-6%203%203%200%20000%206zM5%2013c-2.4.2-4%201.7-4%204v1h3c.3-1.7%201.4-3%203-4-.6-.3-1.3-.7-2-1zm14%200c-.7.3-1.4.7-2%201%201.6%201%202.7%202.3%203%204h3v-1c0-2.3-1.6-3.8-4-4z'/%3E%3C/svg%3E");}
.ph-package{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M12%202l9%205v10l-9%205-9-5V7l9-5zm0%202.3L6.2%207.5%2012%2010.7l5.8-3.2L12%204.3zM5%209.2v6.6l6%203.4v-6.7L5%209.2zm14%200l-6%203.3v6.7l6-3.4V9.2z'/%3E%3C/svg%3E");}
.ph-trend-up{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M3%2017l6-6%204%204%207-8v5h2V4h-8v2h4.5L13%2012.2l-4-4L1.6%2015.6%203%2017z'/%3E%3C/svg%3E");}
.ph-target{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M12%202a10%2010%200%201010%2010h-2a8%208%200%2011-8-8V2zm0%204a6%206%200%20106%206h-2a4%204%200%2011-4-4V6zm0%204a2%202%200%20102%202h-2v-2zm5.5-7.5V6H14l-2%202h4v4l2-2V6.5h3.5l-4-4z'/%3E%3C/svg%3E");}
.ph-scales{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M11%203h2v3h7v2h-2.2l3.2%206a4%204%200%2001-8%200l3.2-6H13v11h4v2H7v-2h4V8H7.8l3.2%206a4%204%200%2001-8%200l3.2-6H4V6h7V3zM5%2014h4L7%2010l-2%204zm10%200h4l-2-4-2%204z'/%3E%3C/svg%3E");}
.ph-calendar{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M7%202h2v2h6V2h2v2h3v18H4V4h3V2zm11%208H6v10h12V10zM6%208h12V6H6v2z'/%3E%3C/svg%3E");}
.ph-chart-bar{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M4%2020h17v2H2V3h2v17zm3-2h3V9H7v9zm5%200h3V5h-3v13zm5%200h3v-7h-3v7z'/%3E%3C/svg%3E");}
.ph-chart-donut{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M11%202v7a3%203%200%20103%203h7A10%2010%200%201111%202zm3%20.5V9h6.5A8%208%200%200014%202.5z'/%3E%3C/svg%3E");}
.ph-chart-line-up{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M4%2020h17v2H2V3h2v17zm2-4l4-5%204%203%205-7v4h2V3h-8v2h4.3l-3.7%205.2-4-3L4.4%2014.8%206%2016z'/%3E%3C/svg%3E");}
.ph-table{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M3%204h18v16H3V4zm2%202v3h14V6H5zm0%205v7h4v-7H5zm6%200v7h8v-7h-8z'/%3E%3C/svg%3E");}
.ph-ranking{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M4%2013h4v8H4v-8zm6-10h4v18h-4V3zm6%207h4v11h-4V10zM5%206h3v2H5V6zm11-2h5v2h-5V4z'/%3E%3C/svg%3E");}
.ph-warning-circle{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M12%202a10%2010%200%201010%2010A10%2010%200%200012%202zm1%2015h-2v-2h2v2zm0-4h-2V7h2v6z'/%3E%3C/svg%3E");}
.ph-info{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M11%2010h2v8h-2v-8zm0-4h2v2h-2V6zm1-4a10%2010%200%201010%2010A10%2010%200%200012%202z'/%3E%3C/svg%3E");}
.ph-leaf{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M21%203C12%203%205%207%205%2014c0%202%201%203.8%202.5%205L4%2022h3l2.2-2C18%2020%2021%2012%2021%203zm-4%204c-3%205-6%208-10%2011%202-6%205-9%2010-11z'/%3E%3C/svg%3E");}
.ph-grid-four{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M4%204h7v7H4V4zm9%200h7v7h-7V4zM4%2013h7v7H4v-7zm9%200h7v7h-7v-7z'/%3E%3C/svg%3E");}
.ph-funnel-simple{--icon:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%3E%3Cpath%20d='M3%205h18v2H3V5zm4%206h10v2H7v-2zm3%206h4v2h-4v-2z'/%3E%3C/svg%3E");}

        /* Ajuste visual Grupo/Terceros en todas las tablas */
        .type-tag.grupo {
            background: #e4f1ff !important;
            color: #1d5f99 !important;
            border-color: #bad8f5 !important;
        }
        .type-tag.terceros {
            background: #fff0dc !important;
            color: #a95504 !important;
            border-color: #f2cf9b !important;
        }
        .type-tag.total {
            background: #e6f4df !important;
            color: var(--green) !important;
            border-color: #b9ddb0 !important;
        }

        /* En monitores pequeños evita que tablas y gráficos queden apretados/remontados */
        @media (max-width: 1150px) {
            div[data-testid="stHorizontalBlock"] {
                flex-wrap: wrap !important;
                gap: 1rem !important;
            }
            div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                min-width: min(100%, 460px) !important;
                flex: 1 1 460px !important;
            }
            .pro-table { min-width: 680px; }
            div[data-testid="stPlotlyChart"] { margin-bottom: 8px; }
        }

        @media (max-width: 760px) {
            div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                min-width: 100% !important;
                flex: 1 1 100% !important;
            }
            .pro-table { min-width: 620px; font-size: 12px; }
            .pro-table thead th, .pro-table tbody td { padding: 10px 11px; }
        }


</style>
""".strip()

    # st.html evita que Streamlit/Markdown muestre el CSS como bloque de código.
    if hasattr(st, "html"):
        st.html(CSS)
    else:
        st.markdown(CSS, unsafe_allow_html=True)
