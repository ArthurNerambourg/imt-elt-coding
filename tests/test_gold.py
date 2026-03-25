import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from src.gold import (
    _read_silver,
    _create_gold_table,
    _create_gold_view,
    create_daily_revenue,
    create_product_performance,
    create_customer_ltv,
    create_gold_layer
)

class TestReadSilver:

    @patch('src.gold.pd.read_sql')
    @patch('src.gold.get_engine')
    def test_read_silver(self, mock_get_engine, mock_read_sql):
        fake_engine = MagicMock()
        fake_df = pd.DataFrame({"order_id" : [1]})
        mock_get_engine.return_value = fake_engine
        mock_read_sql.return_value = fake_df

        result = _read_silver("fct_orders")
        assert result.equals(fake_df)

class TestCreateDailyRevenue:
    pass

class TestCreateProductPerformance:
    pass

class TestCreateCustomerLtv:
    pass