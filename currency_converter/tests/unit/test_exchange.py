from django.test import TestCase

from currency_converter.exchange import load_exchange_data


class RandomTestCase(TestCase):
    def test_load_exchange_data(self):
        df = load_exchange_data()

        assert df is not None

        dataframe_columns = ['date', 'rate', 'currency']
        assert df.columns.tolist() == dataframe_columns

        assert len(df) > 0

        unique_dates = len(df.date.unique())
        assert unique_dates < 90 and unique_dates > 60
