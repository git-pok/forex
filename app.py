from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension 
from forex_python.converter import RatesNotAvailableError
from forex_python_methods import currency_converter, symbol_converter, currency_round, symbol_currency_concat

app = Flask(__name__)
app.config['SECRET_KEY'] = 'survey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

CONVERTED_CURRENCY_LIST = []

def append_currency_list(converted_output):
    """appends the final converted output to converted_currency_list"""
    return CONVERTED_CURRENCY_LIST.append(converted_output)

@app.route('/')
def forex_converter_home_page():
    """responds with the home page template"""
    return render_template('home.html', final_list=CONVERTED_CURRENCY_LIST)

@app.route('/check-currency-codes', methods=['POST'])
def check_currency_codes():
    """
    accesses the form values.
    makes variables out of them.
    checks if cvrt_from and cvrt_to are in currency_codes.
    executes currency_converter with variables passed in.
    redirects user to '/'.
    """
    cvrt_from = request.form.get('convert-from').upper()
    cvrt_to = request.form.get('convert-to').upper()
    amnt = request.form.get('amount')

    try:
        CONVERTED_CURRENCY_LIST.clear()
        converted_currency = currency_converter(cvrt_from, cvrt_to, amnt)
        rounded_currency = currency_round(converted_currency)
        converted_symbol = symbol_converter(cvrt_to)
        converted_output = symbol_currency_concat(converted_symbol, rounded_currency)
        append_currency_list(converted_output)
        flash("Converted!", 'success')
                
    except RatesNotAvailableError as exc:
        flash(f"{exc}", 'error')
    except ValueError as exc:
        str_exc = str(exc)
        exc_find = str_exc.find(':')
        exc_num = str_exc[exc_find::]
        flash(f"Invalid Number Input{exc_num}!", 'error')

    return redirect('/')