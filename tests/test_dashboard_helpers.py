from dashboard.data_helpers import build_category_options, get_product_sort


def test_sales_desc_option_sorts_by_comments_count_desc():
    assert get_product_sort("销量降序") == ("comments_count", "desc")


def test_category_options_include_available_categories_after_all():
    stats = {
        "categories": {
            "耳机音箱": {"count": 3, "avg_price": 200.0},
            "手机数码": {"count": 2, "avg_price": 1000.0},
        }
    }

    assert build_category_options(stats) == ["全部", "手机数码", "耳机音箱"]
