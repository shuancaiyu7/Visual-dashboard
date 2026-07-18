import asyncio

from fastapi import HTTPException

import api.main as api_main


class DummyStatsManager:
    def get_statistics(self):
        return {
            "total_products": 1,
            "total_platforms": 1,
            "total_categories": 1,
            "platforms": {"jd": {"count": 1, "avg_price": 100.0}},
            "categories": {"手机数码": {"count": 1, "avg_price": 100.0}},
        }


def test_statistics_endpoint_uses_sync_database_method():
    original = api_main.db_manager
    api_main.db_manager = DummyStatsManager()
    try:
        response = asyncio.run(api_main.get_statistics())
    except HTTPException as exc:
        raise AssertionError(f"statistics endpoint raised HTTP {exc.status_code}: {exc.detail}") from exc
    finally:
        api_main.db_manager = original

    assert response.total_products == 1
    assert response.platforms["jd"]["avg_price"] == 100.0
