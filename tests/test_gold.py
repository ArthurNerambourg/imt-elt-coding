import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from src.gold import (
    _read_silver,
    create_daily_revenue,
    create_product_performance,
    create_customer_ltv,
    SILVER_SCHEMA,
)


class TestReadSilver:
    @patch("src.gold.pd.read_sql")
    @patch("src.gold.get_engine")
    def test_read_silver(self, mock_get_engine, mock_read_sql):
        fake_engine = MagicMock()
        fake_df = pd.DataFrame({"order_id": [1]})

        mock_get_engine.return_value = fake_engine
        mock_read_sql.return_value = fake_df

        result = _read_silver("fct_orders")

        mock_read_sql.assert_called_once_with(
            f"SELECT * FROM {SILVER_SCHEMA}.fct_orders",
            fake_engine,
        )
        assert result.equals(fake_df)


class TestCreateDailyRevenue:
    @patch("src.gold._create_gold_table")
    @patch("src.gold.pd.read_sql")
    @patch("src.gold.get_engine")
    def test_creates_daily_revenue_table(
        self, mock_get_engine, mock_read_sql, mock_create_table, sample_daily_revenue
    ):
        mock_read_sql.return_value = sample_daily_revenue

        create_daily_revenue()

        mock_read_sql.assert_called_once()
        mock_create_table.assert_called_once_with(sample_daily_revenue, "daily_revenue")

    @patch("src.gold._create_gold_table")
    @patch("src.gold.pd.read_sql")
    @patch("src.gold.get_engine")
    def test_sql_filters_invalid_statuses(
        self, mock_get_engine, mock_read_sql, mock_create_table, sample_daily_revenue
    ):
        mock_read_sql.return_value = sample_daily_revenue

        create_daily_revenue()

        sql_query = mock_read_sql.call_args[0][0]
        assert "cancelled" in sql_query
        assert "chargeback" in sql_query
        assert "GROUP BY DATE(o.order_date)" in sql_query

    @patch("src.gold._create_gold_table")
    @patch("src.gold.pd.read_sql", side_effect=Exception("DB read failed"))
    def test_propagates_error(self, mock_read_sql, mock_create_table):
        with pytest.raises(Exception, match="DB read failed"):
            create_daily_revenue()


class TestCreateProductPerformance:
    @patch("src.gold._create_gold_table")
    @patch("src.gold.pd.read_sql")
    @patch("src.gold.get_engine")
    def test_creates_product_performance_table(
        self, mock_get_engine, mock_read_sql, mock_create_table, sample_product_performance
    ):
        mock_read_sql.return_value = sample_product_performance

        create_product_performance()

        mock_read_sql.assert_called_once()
        mock_create_table.assert_called_once_with(
            sample_product_performance, "product_performance"
        )

    @patch("src.gold._create_gold_table")
    @patch("src.gold.pd.read_sql")
    @patch("src.gold.get_engine")
    def test_sql_joins_products_and_orders(
        self, mock_get_engine, mock_read_sql, mock_create_table, sample_product_performance
    ):
        mock_read_sql.return_value = sample_product_performance

        create_product_performance()

        sql_query = mock_read_sql.call_args[0][0]
        assert f"FROM {SILVER_SCHEMA}.fct_order_lines ol" in sql_query
        assert f"INNER JOIN {SILVER_SCHEMA}.dim_products p" in sql_query
        assert f"INNER JOIN {SILVER_SCHEMA}.fct_orders o" in sql_query

    @patch("src.gold._create_gold_table")
    @patch("src.gold.pd.read_sql", side_effect=Exception("DB read failed"))
    def test_propagates_error(self, mock_read_sql, mock_create_table):
        with pytest.raises(Exception, match="DB read failed"):
            create_product_performance()


class TestCreateCustomerLtv:
    @patch("src.gold._create_gold_table")
    @patch("src.gold.pd.read_sql")
    @patch("src.gold.get_engine")
    def test_creates_customer_ltv_table(
        self, mock_get_engine, mock_read_sql, mock_create_table, sample_customer_ltv
    ):
        mock_read_sql.return_value = sample_customer_ltv

        create_customer_ltv()

        mock_read_sql.assert_called_once()
        mock_create_table.assert_called_once_with(sample_customer_ltv, "customer_ltv")

    @patch("src.gold._create_gold_table")
    @patch("src.gold.pd.read_sql")
    @patch("src.gold.get_engine")
    def test_sql_computes_customer_metrics(
        self, mock_get_engine, mock_read_sql, mock_create_table, sample_customer_ltv
    ):
        mock_read_sql.return_value = sample_customer_ltv

        create_customer_ltv()

        sql_query = mock_read_sql.call_args[0][0]
        assert f"FROM {SILVER_SCHEMA}.dim_users u" in sql_query
        assert f"INNER JOIN {SILVER_SCHEMA}.fct_orders o" in sql_query
        assert "MIN(o.order_date)" in sql_query
        assert "MAX(o.order_date)" in sql_query

    @patch("src.gold._create_gold_table")
    @patch("src.gold.pd.read_sql", side_effect=Exception("DB read failed"))
    def test_propagates_error(self, mock_read_sql, mock_create_table):
        with pytest.raises(Exception, match="DB read failed"):
            create_customer_ltv()