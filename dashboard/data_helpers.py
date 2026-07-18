def build_category_options(stats):
    categories = stats.get("categories", {})
    sorted_categories = sorted(categories.keys())
    return ["全部", *sorted_categories]


def get_product_sort(sort_option):
    sort_map = {
        "价格升序": ("price", "asc"),
        "价格降序": ("price", "desc"),
        "销量降序": ("comments_count", "desc"),
    }
    return sort_map.get(sort_option, ("price", "asc"))
