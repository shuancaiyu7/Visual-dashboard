import asyncio
import os
import sys
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dashboard.data_helpers import build_category_options, get_product_sort
from dashboard.ui import (
    DASHBOARD_CSS,
    PLOTLY_COLORS,
    apply_plotly_theme,
    render_empty_state,
    render_metric_card,
    render_page_header,
    render_panel_heading,
)
from storage.database import DatabaseManager


st.set_page_config(
    page_title="电商数据看板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_db() -> DatabaseManager:
    return DatabaseManager("sqlite:///./data/products.db")


def run_async(coro: Any):
    return asyncio.run(coro)


def render_metrics(db: DatabaseManager):
    stats = db.get_statistics()
    platforms = stats.get("platforms", {})
    avg_prices = [value.get("avg_price", 0) for value in platforms.values()]
    average_price = sum(avg_prices) / len(avg_prices) if avg_prices else 0
    metric_data = [
        ("商品总数", f"{stats.get('total_products', 0):,}", PLOTLY_COLORS["primary"]),
        ("覆盖平台", str(stats.get("total_platforms", 0)), PLOTLY_COLORS["comparison"]),
        ("商品类目", str(stats.get("total_categories", 0)), "#a78bfa"),
        ("平均价格", f"¥{average_price:,.0f}" if avg_prices else "暂无", PLOTLY_COLORS["attention"]),
    ]

    columns = st.columns(4)
    for column, (label, value, color) in zip(columns, metric_data):
        with column:
            st.markdown(render_metric_card(label, value, color), unsafe_allow_html=True)


def render_platform_comparison(db: DatabaseManager):
    stats = db.get_statistics()
    platforms = stats.get("platforms", {})

    if not platforms:
        st.markdown(render_empty_state("暂无平台数据，请先运行采集任务"), unsafe_allow_html=True)
        return

    platform_names = list(platforms.keys())
    platform_counts = [platforms[name]["count"] for name in platform_names]
    platform_avg_prices = [platforms[name]["avg_price"] for name in platform_names]
    left, right = st.columns(2)

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(render_panel_heading("平台商品数量", "查看各平台商品覆盖情况"), unsafe_allow_html=True)
        count_figure = go.Figure(
            go.Bar(
                x=platform_names,
                y=platform_counts,
                marker_color=PLOTLY_COLORS["comparison"],
                hovertemplate="%{x}<br>商品数量：%{y:,}<extra></extra>",
            )
        )
        count_figure.update_yaxes(title_text="商品数量")
        apply_plotly_theme(count_figure)
        st.plotly_chart(count_figure, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(render_panel_heading("平台平均价格", "比较不同平台的商品价格水平"), unsafe_allow_html=True)
        price_figure = go.Figure(
            go.Bar(
                x=platform_names,
                y=platform_avg_prices,
                marker_color=PLOTLY_COLORS["primary"],
                hovertemplate="%{x}<br>平均价格：¥%{y:,.2f}<extra></extra>",
            )
        )
        price_figure.update_yaxes(title_text="平均价格（¥）")
        apply_plotly_theme(price_figure)
        st.plotly_chart(price_figure, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    price_matrix = db.get_price_matrix()
    categories = price_matrix.get("categories", [])
    matrix_platforms = price_matrix.get("platforms", [])
    values = price_matrix.get("values", [])
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(render_panel_heading("类目价格矩阵", "比较各平台在不同类目中的平均价格"), unsafe_allow_html=True)
    if matrix_platforms and categories and values:
        heatmap = go.Figure(
            go.Heatmap(
                z=values,
                x=matrix_platforms,
                y=categories,
                colorscale=[[0, "#102a43"], [0.5, "#0f766e"], [1, "#5eead4"]],
                colorbar={"title": "平均价格", "tickfont": {"color": PLOTLY_COLORS["muted"]}},
                hovertemplate="类目：%{y}<br>平台：%{x}<br>平均价格：¥%{z:,.2f}<extra></extra>",
            )
        )
        apply_plotly_theme(heatmap, height=440)
        st.plotly_chart(heatmap, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown(render_empty_state("暂无可用于价格矩阵的商品数据"), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_category_analysis(db: DatabaseManager):
    categories = db.get_statistics().get("categories", {})
    if not categories:
        st.markdown(render_empty_state("暂无类目数据，请先运行采集任务"), unsafe_allow_html=True)
        return

    category_names = list(categories.keys())
    category_counts = [categories[name]["count"] for name in category_names]
    category_prices = [categories[name]["avg_price"] for name in category_names]
    left, right = st.columns(2)

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(render_panel_heading("类目商品分布", "查看各类目在当前数据中的占比"), unsafe_allow_html=True)
        distribution = px.pie(
            values=category_counts,
            names=category_names,
            hole=0.58,
            color_discrete_sequence=["#2dd4bf", "#60a5fa", "#a78bfa", "#f59e0b", "#f472b6", "#38bdf8"],
        )
        distribution.update_traces(textposition="inside", textinfo="percent+label", hovertemplate="%{label}<br>商品数量：%{value:,}<br>占比：%{percent}<extra></extra>")
        apply_plotly_theme(distribution)
        st.plotly_chart(distribution, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(render_panel_heading("类目平均价格", "按价格从高到低排列"), unsafe_allow_html=True)
        category_frame = pd.DataFrame({"类目": category_names, "平均价格": category_prices}).sort_values("平均价格", ascending=True)
        prices = px.bar(
            category_frame,
            x="平均价格",
            y="类目",
            orientation="h",
            color_discrete_sequence=[PLOTLY_COLORS["primary"]],
        )
        prices.update_traces(hovertemplate="%{y}<br>平均价格：¥%{x:,.2f}<extra></extra>")
        apply_plotly_theme(prices)
        st.plotly_chart(prices, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


def render_product_table(db: DatabaseManager):
    stats = db.get_statistics()
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(render_panel_heading("商品筛选", "按平台、类目和排序方式查找商品"), unsafe_allow_html=True)
    platform_column, category_column, sort_column, limit_column = st.columns(4)
    with platform_column:
        platform_filter = st.selectbox("平台", options=["全部", "jd", "tmall"], key="platform_filter")
    with category_column:
        category_filter = st.selectbox("类目", options=build_category_options(stats), key="category_filter")
    with sort_column:
        sort_option = st.selectbox("排序", options=["价格升序", "价格降序", "销量降序"], key="sort_option")
    with limit_column:
        limit_option = st.selectbox("显示数量", options=[20, 50, 100, 200], key="limit_option")
    st.markdown("</div>", unsafe_allow_html=True)

    sort_by, order = get_product_sort(sort_option)
    products = run_async(
        db.get_products(
            platform=platform_filter if platform_filter != "全部" else None,
            category=category_filter if category_filter != "全部" else None,
            sort_by=sort_by,
            order=order,
            limit=limit_option,
        )
    )
    if not products:
        st.markdown(render_empty_state("当前筛选条件下没有商品数据"), unsafe_allow_html=True)
        return

    frame = pd.DataFrame(products)
    if "price" in frame.columns:
        frame["price"] = frame["price"].apply(lambda value: f"¥{value:,.2f}")
    if "original_price" in frame.columns:
        frame["original_price"] = frame["original_price"].apply(lambda value: f"¥{value:,.2f}" if value else "暂无")

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(render_panel_heading("商品明细", f"共显示 {len(frame):,} 条记录"), unsafe_allow_html=True)
    st.dataframe(frame, use_container_width=True, hide_index=True, height=560)
    st.download_button(
        label="导出 CSV",
        data=frame.to_csv(index=False, encoding="utf-8-sig"),
        file_name=f"products_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_about():
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(render_panel_heading("关于本项目", "电商商品数据的采集、存储与分析"), unsafe_allow_html=True)
    st.markdown(
        """
        - 支持京东、天猫等平台的商品数据采集。
        - 通过定时任务自动更新数据，并提供结构化的数据存储。
        - 提供平台、类目、价格和商品明细的交互式分析。
        - 商品明细支持筛选、排序与 CSV 导出。
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)


def run_dashboard():
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)
    try:
        db = init_db()
        st.sidebar.markdown('<div class="brand">电商数据看板</div>', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="brand-subtitle">商品数据分析工作台</div>', unsafe_allow_html=True)
        page = st.sidebar.radio(
            "导航",
            ["数据概览", "平台对比", "类目分析", "商品明细", "关于项目"],
            label_visibility="collapsed",
        )

        page_descriptions = {
            "数据概览": ("数据概览", "快速了解商品覆盖、平台数量、类目结构和价格水平。"),
            "平台对比": ("平台对比", "比较各平台的商品规模、价格水平与类目覆盖。"),
            "类目分析": ("类目分析", "查看各类目商品占比与平均价格分布。"),
            "商品明细": ("商品明细", "通过筛选和排序定位具体商品，并导出当前结果。"),
            "关于项目": ("关于项目", "了解本看板的数据来源和可用分析能力。"),
        }
        title, description = page_descriptions[page]
        st.markdown(render_page_header(title, description), unsafe_allow_html=True)

        if page == "数据概览":
            render_metrics(db)
            st.markdown('<div class="section-title">平台与价格洞察</div>', unsafe_allow_html=True)
            render_platform_comparison(db)
        elif page == "平台对比":
            render_platform_comparison(db)
        elif page == "类目分析":
            render_category_analysis(db)
        elif page == "商品明细":
            render_product_table(db)
        else:
            render_about()

        st.markdown(
            f'<div class="footer">界面刷新时间：{pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} · 电商数据看板</div>',
            unsafe_allow_html=True,
        )
        db.close()
    except Exception as exc:
        st.error(f"看板启动失败：{exc}")
        st.markdown(render_empty_state("请确认数据库文件存在，并已完成数据采集。"), unsafe_allow_html=True)


if __name__ == "__main__":
    run_dashboard()
