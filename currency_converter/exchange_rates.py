from urllib.request import urlopen
import xml.etree.ElementTree as et

import pandas as pd


def fetch_xml():
    """
    Fetch XML containing the euro exchange rate
    """
    EURO_REF_XML = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'
    return urlopen(EURO_REF_XML)


def parse_xml(xml):
    """
    Parse the XML and returns a list of dictionary objects
    [{date, currency, rate}]
    """
    eurofxref = '{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube'
    xtree = et.parse(xml)
    reference = []
    for node in xtree.iterfind(f'{eurofxref}/{eurofxref}'):
        date = node.attrib['time']
        for each in node.findall(eurofxref):
            currency = each.attrib['currency']
            rate = each.attrib['rate']
            reference.append({
                'date': date,
                'currency': currency,
                'rate': rate,
            })
    return reference


def create_exchange_dataframe(reference, columns):
    """
    Parses list of dictionary objects and returns a
    Dataframe with the specified columns
    """
    return pd.DataFrame(reference, columns=columns)


def load_exchange_data():
    """
    Returns a Dataframe containing the euro exchange rates
    """
    xml = fetch_xml()
    reference = parse_xml(xml)
    df = create_exchange_dataframe(reference, ['date', 'rate', 'currency'])
    return df


def lookup_exchange_rate(date, currency):
    """
    Queries the exchange rate for a given date & currency
    """
    rates_df = load_exchange_data()
    out = rates_df.query(f'date == "{date}" and currency == "{currency}"')
    return float(out.rate.values[0])


def convert_amount(amount, date, src_currency, dest_currency):
    """
    Returns a converted amount for a given
    amount, date, src_currency & dest_currency
    """
    if src_currency == 'EUR' and dest_currency == 'EUR':
        return round(amount, 2)
    if src_currency == 'EUR' and dest_currency != 'EUR':
        return round(amount * lookup_exchange_rate(date, dest_currency), 2)
    if src_currency != 'EUR' and dest_currency == 'EUR':
        return round(amount/lookup_exchange_rate(date, src_currency), 2)

    converted = (amount/lookup_exchange_rate(date, src_currency)) * \
        lookup_exchange_rate(date, dest_currency)
    return round(converted, 2)
