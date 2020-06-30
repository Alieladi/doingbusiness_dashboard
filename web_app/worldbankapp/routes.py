from worldbankapp import app
import json, plotly
from flask import render_template, request, Response, jsonify
from wrangling_scripts.wrangle_data import return_results

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    default_countries = ["Morocco", "France", "Finland", "China", "United States"]
    # Parse the POST request countries list
    if (request.method == 'POST') and request.form:
        figures, all_countries, close_ranks = return_results(request.form)
        countries_selected = []

        for country in request.form.lists():
            countries_selected.append(country)

	# GET request returns all countries for initial page load
    else:
        figures, all_countries, close_ranks = return_results(default_countries)
        countries_selected = []
        for country in default_countries:
            countries_selected.append(country)

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', ids=ids,
    	figuresJSON=figuresJSON,
    	all_countries=all_countries,
    	countries_selected=countries_selected,
        close_ranks=close_ranks)
