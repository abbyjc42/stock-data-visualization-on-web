from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from .forms import StockForm
from .charts import *


@app.route("/", methods=['GET', 'POST'])
@app.route("/stocks", methods=['GET', 'POST'])
def stocks():
    
    form = StockForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            #Get the form data to query the api
            symbol = request.form['symbol']
            chart_type = request.form['chart_type']
            time_series = request.form['time_series']
            start_date = convert_date(request.form['start_date'])
            end_date = convert_date(request.form['end_date'])

            if end_date <= start_date:
                #Generate error message as pass to the page
                err = "ERROR: End date cannot be earlier than Start date."
                chart = None
            else:
                #query the api using the form data
                err = None

                ###################### 
                #THIS IS WHERE YOU WILL CALL THE METHODS FROM THE CHARTS.PY FILE AND IMPLEMENT YOUR CODE
            
                request_url = build_URL(time_series, symbol)
                err = request_url
                json_data = parse_json(request_url, (end_date - start_date), time_series)
                open_line = generate_coordinates(json_data, "1. open")
                high_line = generate_coordinates(json_data, "2. high")
                low_line = generate_coordinates(json_data, "3. low")
                close_line = generate_coordinates(json_data, "4. close")

                chart_data = generate_graph(symbol, chart_type, open_line, high_line, low_line, close_line)
                
                #######################
                
                #This chart variable is what is passed to the stock.html page to render the chart returned from the api
                chart = chart_data.render_data_uri()

            return render_template("stock.html", form=form, template="form-template", err = err, chart = chart)
    
    return render_template("stock.html", form=form, template="form-template")
