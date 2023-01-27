from unittest import TestCase
from app import app
from forex_python_methods import currency_converter, symbol_converter, currency_round, symbol_currency_concat
from forex_python.converter import RatesNotAvailableError

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class ForexAppPythonMethods(TestCase):
    def test_currency_converter(self):
        self.assertEqual(currency_converter('USD', 'USD', 1), 1.0)
        self.assertEqual(currency_converter('USD', 'USD', 1.9473), 1.9473)
        self.assertRaises(RatesNotAvailableError, currency_converter, 'URE', 'USD', 200)

    def test_symbol_converter(self):
        self.assertEqual(symbol_converter('USD'), '$')
        self.assertEqual(symbol_converter('EUR'), '€')
        self.assertEqual(symbol_converter('JPY'), '¥')

    def test_currency_round(self):
        self.assertEqual(currency_round(123.4567), 123.46)
        self.assertEqual(currency_round(45.7987), 45.80)

    def test_symbol_currency_concat(self):
        self.assertEqual(symbol_currency_concat('$', 45), '$45')
        self.assertEqual(symbol_currency_concat('¥', 200.26), '¥200.26')

class ForexAppFlaskTests(TestCase):
    def test_forex_converter_home_page_route(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<label for="convert-from">Convert From</label>', html)

    def test_check_currency_codes_redirect(self):
        with app.test_client() as client: 
            res = client.post('/check-currency-codes', data={"convert-from": 'USD', "convert-to": 'USD', "amount": 1})
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/')