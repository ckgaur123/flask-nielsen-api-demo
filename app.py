from flask import Flask
from flask import request

from nielsen_api_demo import *

app = Flask(__name__)

@app.route("/")
def data():

	date = request.args.get('date')
	network = request.args.get('network')

	website_html = get_template()

	data = get_live_data_for_date_and_network(date,network)
	website_html = website_html.replace("INSERT_DATA_HERE",data)

	return website_html
		