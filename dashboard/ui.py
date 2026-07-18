from html import escape


PLOTLY_COLORS = {
    "primary": "#2dd4bf",
    "comparison": "#60a5fa",
    "attention": "#f59e0b",
    "muted": "#94a3b8",
    "surface": "#111827",
    "grid": "#263244",
}


DASHBOARD_CSS = """
<style>
    :root {
        --bg: #0b1120;
        --surface: #111827;
        --surface-raised: #172033;
        --border: #263244;
        --text: #e5e7eb;
        --muted: #94a3b8;
        --sidebar-text: #f8fafc;
        --sidebar-muted: #cbd5e1;
        --primary: #2dd4bf;
        --comparison: #60a5fa;
        --attention: #f59e0b;
    }
    .stApp { background: var(--bg); color: var(--text); }
    [data-testid="stHeader"] { background: rgba(11, 17, 32, 0.95); }
    [data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.2rem; }
    .block-container { max-width: 1440px; padding: 1.4rem 2rem 1.8rem; }
    .brand { color: var(--sidebar-text); font-size: 1.2rem; font-weight: 700; margin: 0 0 .2rem; }
    .brand-subtitle { color: var(--sidebar-muted); font-size: .78rem; margin: 0 0 1.3rem; }
    .page-kicker { color: var(--primary); font-size: .75rem; font-weight: 700; margin-bottom: .35rem; }
    .page-title { color: var(--text); font-size: 1.85rem; font-weight: 700; margin: 0; }
    .page-description { color: var(--muted); font-size: .93rem; margin: .35rem 0 1.25rem; }
    .metric-card {
        min-height: 116px; background: var(--surface-raised); border: 1px solid var(--border);
        border-radius: 6px; padding: 1rem 1.05rem; box-sizing: border-box;
    }
    .metric-label { color: var(--muted); font-size: .8rem; margin-bottom: .55rem; }
    .metric-value { color: var(--text); font-size: 1.7rem; font-weight: 700; line-height: 1; }
    .metric-accent { height: 3px; border-radius: 3px; margin-top: .9rem; }
    .panel {
        background: var(--surface); border: 1px solid var(--border); border-radius: 6px;
        padding: .9rem 1rem .35rem; margin-bottom: 1rem;
    }
    .panel-title { color: var(--text); font-size: 1rem; font-weight: 650; margin: 0 0 .15rem; }
    .panel-description { color: var(--muted); font-size: .8rem; margin: 0 0 .55rem; }
    .section-title { color: var(--text); font-size: 1.15rem; font-weight: 650; margin: 1.2rem 0 .75rem; }
    .empty-state {
        background: var(--surface); border: 1px dashed #3b4b66; border-radius: 6px;
        color: var(--muted); padding: 2rem 1.25rem; text-align: center; margin: .5rem 0 1rem;
    }
    .footer { color: #64748b; font-size: .75rem; padding: .75rem 0 .1rem; }
    [data-testid="stSidebar"] .stRadio label {
        border-radius: 5px; margin: .1rem 0; padding: .3rem .4rem;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] label span, [data-testid="stSidebar"] label p {
        color: var(--sidebar-text) !important;
        font-weight: 600;
    }
    [data-testid="stSidebar"] .stRadio label:has(input:checked) {
        background: #1e3a4c;
        box-shadow: inset 3px 0 0 var(--primary);
    }
    [data-testid="stSidebar"] .stRadio label:has(input:checked),
    [data-testid="stSidebar"] .stRadio label:has(input:checked) span,
    [data-testid="stSidebar"] .stRadio label:has(input:checked) p { color: #ffffff !important; }
    [data-testid="stSelectbox"] label, [data-testid="stDownloadButton"] label { color: var(--muted); font-size: .82rem; }
    [data-baseweb="select"] > div, [data-baseweb="input"] > div {
        background: var(--surface-raised); border-color: var(--border); color: var(--text);
    }
    [data-baseweb="popover"] { background: var(--surface); }
    .stButton > button, .stDownloadButton > button {
        background: #0f766e; border: 1px solid #2dd4bf; border-radius: 5px; color: #f0fdfa;
        font-weight: 650;
    }
    .stButton > button:hover, .stDownloadButton > button:hover { background: #115e59; border-color: #5eead4; }
    [data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 6px; overflow: hidden; }
    [data-testid="stDataFrame"] [role="columnheader"] { background: #172033; }
    div[data-testid="stMetric"] { background: var(--surface-raised); border: 1px solid var(--border); border-radius: 6px; padding: .8rem; }
    @media (max-width: 900px) {
        .block-container { padding: 1rem; }
        .page-title { font-size: 1.55rem; }
        .metric-card { min-height: 102px; }
    }
</style>
"""


def apply_plotly_theme(figure, height: int = 380):
    figure.update_layout(
        height=height,
        paper_bgcolor=PLOTLY_COLORS["surface"],
        plot_bgcolor=PLOTLY_COLORS["surface"],
        font={"color": "#e5e7eb", "family": "Arial, sans-serif"},
        margin={"l": 32, "r": 22, "t": 28, "b": 36},
        legend={"font": {"color": "#cbd5e1"}, "bgcolor": "rgba(0,0,0,0)"},
        xaxis={
            "tickfont": {"color": PLOTLY_COLORS["muted"]},
            "title_font": {"color": PLOTLY_COLORS["muted"]},
            "gridcolor": PLOTLY_COLORS["grid"],
            "zerolinecolor": PLOTLY_COLORS["grid"],
        },
        yaxis={
            "tickfont": {"color": PLOTLY_COLORS["muted"]},
            "title_font": {"color": PLOTLY_COLORS["muted"]},
            "gridcolor": PLOTLY_COLORS["grid"],
            "zerolinecolor": PLOTLY_COLORS["grid"],
        },
        hoverlabel={"bgcolor": "#172033", "font": {"color": "#f8fafc"}},
    )
    return figure


def render_empty_state(message: str) -> str:
    return f'<div class="empty-state">{escape(message)}</div>'


def render_metric_card(label: str, value: str, color: str) -> str:
    return (
        '<div class="metric-card">'
        f'<div class="metric-label">{escape(label)}</div>'
        f'<div class="metric-value">{escape(value)}</div>'
        f'<div class="metric-accent" style="background:{escape(color)}"></div>'
        '</div>'
    )


def render_page_header(title: str, description: str) -> str:
    return (
        '<div class="page-kicker">数据工作台</div>'
        f'<h1 class="page-title">{escape(title)}</h1>'
        f'<p class="page-description">{escape(description)}</p>'
    )


def render_panel_heading(title: str, description: str = "") -> str:
    description_markup = f'<p class="panel-description">{escape(description)}</p>' if description else ""
    return f'<div class="panel-title">{escape(title)}</div>{description_markup}'
