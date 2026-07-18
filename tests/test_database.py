# tests/test_database.py
"""
数据库模块单元测试
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from storage.database import DatabaseManager
from crawler.base_crawler import ProductData
from datetime import datetime


class TestDatabaseManager:
    """测试数据库管理器"""
    
    @pytest.fixture
    def db(self, tmp_path):
        """创建测试数据库实例"""
        db = DatabaseManager(f"sqlite:///{tmp_path / 'test_products.db'}")
        yield db
        db.close()
    
    def test_save_product(self, db):
        """测试保存商品"""
        product = ProductData(
            product_id="test_prod_001",
            title="测试手机",
            price=2999.00,
            platform="jd",
            category="手机数码"
        )
        result = asyncio.run(db.save_product(product))
        assert result == True
    
    def test_get_products(self, db):
        """测试获取商品列表"""
        # 先保存一些数据
        for i in range(5):
            product = ProductData(
                product_id=f"test_get_{i}",
                title=f"测试商品{i}",
                price=100.0 * (i + 1),
                platform="jd",
                category="测试"
            )
            asyncio.run(db.save_product(product))
        
        # 获取商品
        products = asyncio.run(db.get_products(platform="jd", limit=10))
        assert len(products) >= 5

    def test_get_price_matrix_groups_by_platform_and_category(self, db):
        """测试按平台和类目生成真实均价矩阵"""
        products = [
            ProductData(product_id="matrix_jd_phone_1", title="京东手机1", price=100.0, platform="jd", category="手机"),
            ProductData(product_id="matrix_jd_phone_2", title="京东手机2", price=300.0, platform="jd", category="手机"),
            ProductData(product_id="matrix_tmall_phone_1", title="天猫手机1", price=500.0, platform="tmall", category="手机"),
            ProductData(product_id="matrix_jd_watch_1", title="京东手表1", price=800.0, platform="jd", category="手表"),
        ]
        for product in products:
            asyncio.run(db.save_product(product))

        matrix = db.get_price_matrix()

        assert matrix["platforms"] == ["jd", "tmall"]
        assert matrix["categories"] == ["手机", "手表"]
        assert matrix["values"] == [[200.0, 500.0], [800.0, None]]


import asyncio
