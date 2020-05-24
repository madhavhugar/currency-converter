from unittest.mock import Mock, patch
from django.test import TestCase
import pandas as pd

from currency_converter.exchange_rates import load_exchange_data, convert_amount, lookup_exchange_rate


class ExchangeRatesTestCase(TestCase):
    dict_df = {
            'date': ['2020-05-19', '2020-05-20', '2020-05-20'],
            'rate': [2.0958, 1.0958, 0.89358],
            'currency': ['USD', 'USD', 'GBP'],
        }

    def test_load_exchange_data(self):
        df = load_exchange_data()

        assert df is not None

        dataframe_columns = ['date', 'rate', 'currency']
        assert df.columns.tolist() == dataframe_columns

        assert len(df) > 0

        unique_dates = len(df.date.unique())
        assert unique_dates < 90 and unique_dates > 60

    @patch('currency_converter.exchange_rates.load_exchange_data',
           return_value=pd.DataFrame(data=dict_df))
    def test_lookup_exchange_rate(self, mock_load_exchange_data):
        wanted = 1.0958
        got = lookup_exchange_rate('2020-05-20', 'USD')
        assert got == wanted

    @patch('currency_converter.exchange_rates.load_exchange_data',
           return_value=pd.DataFrame(data=dict_df))
    def test_convert_amount(self, mock_load_exchange_data):
        amount = 20.0
        reference_date = '2020-05-20'

        wanted = 21.92
        got = convert_amount(amount, reference_date, 'EUR', 'USD')
        assert wanted == got

        wanted = 20.00
        got = convert_amount(amount, reference_date, 'EUR', 'EUR')
        assert wanted == got

        wanted = 16.31
        got = convert_amount(amount, reference_date, 'USD', 'GBP')
        assert wanted == got

        wanted = 18.25
        got = convert_amount(amount, reference_date, 'USD', 'EUR')
        assert wanted == got
