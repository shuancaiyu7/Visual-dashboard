# Dashboard Dark Workspace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将全部 Streamlit 数据看板页面改造为统一、可读且适合普通电脑浏览器的深色工作台。

**Architecture:** 新增一个只负责主题、图表样式和展示辅助函数的 `dashboard/ui.py`，让 `dashboard/app.py` 保持数据读取与页面组合职责。页面渲染继续使用现有数据库接口，主题函数只接收和返回 Plotly 图表对象，因此可单独测试。

**Tech Stack:** Python、Streamlit、Plotly、Pandas、Pytest。

---

### Task 1: 添加可测试的界面主题模块

**Files:**
- Create: `dashboard/ui.py`
- Create: `tests/test_dashboard_ui.py`

- [ ] **Step 1: 写入预期会失败的主题测试**

```python
from dashboard.ui import PLOTLY_COLORS, apply_plotly_theme
import plotly.graph_objects as go


def test_apply_plotly_theme_sets_dark_layout_and_default_height():
    figure = apply_plotly_theme(go.Figure())

    assert figure.layout.paper_bgcolor == "#111827"
    assert figure.layout.plot_bgcolor == "#111827"
    assert figure.layout.font.color == "#e5e7eb"
    assert figure.layout.height == 380


def test_plotly_palette_uses_the_specified_semantic_colors():
    assert PLOTLY_COLORS["primary"] == "#2dd4bf"
    assert PLOTLY_COLORS["comparison"] == "#60a5fa"
    assert PLOTLY_COLORS["attention"] == "#f59e0b"
```

- [ ] **Step 2: 运行测试并确认失败原因是模块尚不存在**

Run: `.venv\\Scripts\\python.exe -m pytest tests/test_dashboard_ui.py -q`

Expected: 导入 `dashboard.ui` 失败。

- [ ] **Step 3: 实现最小主题函数**

```python
PLOTLY_COLORS = {
    "primary": "#2dd4bf",
    "comparison": "#60a5fa",
    "attention": "#f59e0b",
    "muted": "#94a3b8",
}


def apply_plotly_theme(figure, height=380):
    figure.update_layout(
        height=height,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font={"color": "#e5e7eb", "family": "Arial, sans-serif"},
    )
    return figure
```

- [ ] **Step 4: 运行主题测试并确认通过**

Run: `.venv\\Scripts\\python.exe -m pytest tests/test_dashboard_ui.py -q`

Expected: 2 passed。

### Task 2: 增加全局深色样式和公共展示函数

**Files:**
- Modify: `dashboard/ui.py`
- Modify: `tests/test_dashboard_ui.py`

- [ ] **Step 1: 写入预期会失败的样式测试**

```python
from dashboard.ui import DASHBOARD_CSS, render_empty_state


def test_dashboard_css_contains_dark_surfaces_and_sidebar_state():
    assert "#0b1120" in DASHBOARD_CSS
    assert ".metric-card" in DASHBOARD_CSS
    assert "[data-testid=\"stSidebar\"]" in DASHBOARD_CSS


def test_render_empty_state_returns_the_requested_message():
    assert "暂无数据" in render_empty_state("暂无数据")
```

- [ ] **Step 2: 运行测试并确认失败原因是常量与函数尚不存在**

Run: `.venv\\Scripts\\python.exe -m pytest tests/test_dashboard_ui.py -q`

Expected: 导入 `DASHBOARD_CSS` 或 `render_empty_state` 失败。

- [ ] **Step 3: 实现主题 CSS 和空状态 HTML**

```python
DASHBOARD_CSS = """
<style>
.stApp { background: #0b1120; color: #e5e7eb; }
[data-testid="stSidebar"] { background: #111827; border-right: 1px solid #263244; }
.metric-card { background: #172033; border: 1px solid #2b3850; border-radius: 6px; padding: 16px; }
</style>
"""


def render_empty_state(message):
    return f'<div class="empty-state">{message}</div>'
```

- [ ] **Step 4: 运行主题测试并确认通过**

Run: `.venv\\Scripts\\python.exe -m pytest tests/test_dashboard_ui.py -q`

Expected: 4 passed。

### Task 3: 将概览、平台与类目图表接入统一主题

**Files:**
- Modify: `dashboard/app.py`
- Test: `tests/test_dashboard_ui.py`

- [ ] **Step 1: 写入预期会失败的坐标轴样式测试**

```python
from dashboard.ui import apply_plotly_theme
import plotly.graph_objects as go


def test_apply_plotly_theme_sets_muted_axis_labels_and_grid_lines():
    figure = apply_plotly_theme(go.Figure())
    assert figure.layout.xaxis.tickfont.color == "#94a3b8"
    assert figure.layout.yaxis.gridcolor == "#263244"
```

- [ ] **Step 2: 运行测试并确认失败原因是坐标轴样式尚未设置**

Run: `.venv\\Scripts\\python.exe -m pytest tests/test_dashboard_ui.py -q`

Expected: 断言失败，因为 `apply_plotly_theme` 尚未定义坐标轴文字和网格颜色。

- [ ] **Step 3: 将图表创建改为统一颜色和主题函数**

```python
fig.add_trace(go.Bar(marker_color=PLOTLY_COLORS["comparison"], ...))
apply_plotly_theme(fig, height=380)

fig_heat = go.Figure(data=go.Heatmap(colorscale="Tealgrn", ...))
apply_plotly_theme(fig_heat, height=460)
```

在 `apply_plotly_theme` 中添加 `xaxis={"tickfont": {"color": "#94a3b8"}, "gridcolor": "#263244"}` 和相同的 `yaxis` 配置。所有柱状图、饼图、热力图在 `st.plotly_chart` 前都调用该函数，平台图使用 `comparison`，类目图使用 `primary`，提醒色只用于强调项。

- [ ] **Step 4: 运行主题测试并确认通过**

Run: `.venv\\Scripts\\python.exe -m pytest tests/test_dashboard_ui.py -q`

Expected: 5 passed。

### Task 4: 改造页面框架、指标、筛选与表格展示

**Files:**
- Modify: `dashboard/app.py`
- Test: `tests/test_dashboard_helpers.py`

- [ ] **Step 1: 运行既有筛选与排序测试，建立改造前基线**

Run: `.venv\\Scripts\\python.exe -m pytest tests/test_dashboard_helpers.py -q`

Expected: 既有测试全部通过。

- [ ] **Step 2: 重组界面渲染但不改变数据调用**

```python
st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)
st.sidebar.markdown("<div class='brand'>电商数据看板</div>", unsafe_allow_html=True)
st.markdown("<div class='page-kicker'>数据工作台</div>", unsafe_allow_html=True)
```

将指标改为 `metric-card` 容器；将页面标题改为左对齐紧凑标题；为图表和商品表格增加 `panel` 容器。保持 `db.get_statistics()`、`db.get_price_matrix()`、`db.get_products()`、`build_category_options()`、`get_product_sort()` 的参数与返回值不变。

- [ ] **Step 3: 用深色表格和统一的空状态替换默认展示**

```python
if not products:
    st.markdown(render_empty_state("当前筛选条件下没有商品数据"), unsafe_allow_html=True)
    return

st.dataframe(df, use_container_width=True, hide_index=True, height=560)
```

为各个无数据分支调用 `render_empty_state`，筛选控件保留四列布局并为较窄窗口添加 CSS 换行规则。

- [ ] **Step 4: 重新运行既有筛选与排序测试**

Run: `.venv\\Scripts\\python.exe -m pytest tests/test_dashboard_helpers.py -q`

Expected: 既有测试全部通过。

### Task 5: 完整验证与桌面界面检查

**Files:**
- Modify: `dashboard/app.py`
- Modify: `dashboard/ui.py`
- Modify: `tests/test_dashboard_ui.py`

- [ ] **Step 1: 运行完整测试与语法检查**

Run: `.venv\\Scripts\\python.exe -m pytest tests -q`

Expected: 全部测试通过。

Run: `.venv\\Scripts\\python.exe -m compileall -q dashboard tests`

Expected: 命令退出状态为 0。

- [ ] **Step 2: 启动 Streamlit 并在普通桌面尺寸检查所有页面**

Run: `.venv\\Scripts\\python.exe -m streamlit run app.py --server.headless true --server.port 8501`

Expected: 服务在 `http://localhost:8501` 启动。

检查概览、平台对比、类目分析与商品明细页面，确认深色主题一致、文字不重叠、筛选可操作、图表可见、表格可读且无数据状态清晰。

- [ ] **Step 3: 提交本次界面改造**

```bash
git add dashboard/app.py dashboard/ui.py tests/test_dashboard_ui.py
git commit -m "feat: redesign dashboard as dark workspace"
```
