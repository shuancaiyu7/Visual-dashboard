from dashboard.ui import DASHBOARD_CSS, PLOTLY_COLORS, apply_plotly_theme, render_empty_state


class FakeFigure:
    def __init__(self):
        self.layout = {}

    def update_layout(self, **kwargs):
        self.layout.update(kwargs)


def test_apply_plotly_theme_sets_dark_workspace_defaults():
    figure = apply_plotly_theme(FakeFigure())

    assert figure.layout["paper_bgcolor"] == "#111827"
    assert figure.layout["plot_bgcolor"] == "#111827"
    assert figure.layout["font"]["color"] == "#e5e7eb"
    assert figure.layout["height"] == 380
    assert figure.layout["xaxis"]["tickfont"]["color"] == "#94a3b8"
    assert figure.layout["yaxis"]["gridcolor"] == "#263244"


def test_plotly_palette_uses_semantic_colors():
    assert PLOTLY_COLORS["primary"] == "#2dd4bf"
    assert PLOTLY_COLORS["comparison"] == "#60a5fa"
    assert PLOTLY_COLORS["attention"] == "#f59e0b"


def test_render_empty_state_returns_message_in_panel_markup():
    markup = render_empty_state("暂无商品数据")

    assert "暂无商品数据" in markup
    assert "empty-state" in markup


def test_sidebar_navigation_uses_high_contrast_text_colors():
    assert "--sidebar-text: #f8fafc;" in DASHBOARD_CSS
    assert "--sidebar-muted: #cbd5e1;" in DASHBOARD_CSS
    assert '[data-testid="stSidebar"] label, [data-testid="stSidebar"] label span' in DASHBOARD_CSS
