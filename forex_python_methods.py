from forex_python.converter import CurrencyRates, CurrencyCodes
from forex_python.converter import RatesNotAvailableError

c_convert = CurrencyRates()
c_codes = CurrencyCodes()

def currency_converter(cvrt_from, cvrt_to, amnt):
    """converts currency amounts and raises errors for specific exc in app.py"""
    if not c_codes.get_symbol(cvrt_from):
        raise RatesNotAvailableError(f"{cvrt_from} is not a valid currency at this time!")
    if not c_codes.get_symbol(cvrt_to):
        raise RatesNotAvailableError(f"{cvrt_to} is not a valid currency at this time!")    
    if float(amnt):
        return c_convert.convert(cvrt_from, cvrt_to, float(amnt))
    if int(amnt):
        return c_convert.convert(cvrt_from, cvrt_to, int(amnt))
    else:
        raise ValueError
        # line 18 wont print correctly when I get amnt errors

def symbol_converter(cvrt_to):
    """converts country code to symbol"""
    return c_codes.get_symbol(cvrt_to)

def currency_round(converted_currency):
    """rounds the converted output two decimals"""
    converted_output = int(converted_currency)
    return round(converted_currency, 2)

def symbol_currency_concat(converted_symbol, rounded_currency):
    """concatenates and returns the converted amount and symbol"""
    return f"{converted_symbol}{rounded_currency}"