from flask import Flask
from flask import request
import requests
import json

app = Flask(__name__)

def get_headers():
	with open("authorizations/nielsen-api-token.txt") as f:
		token = f.read()
	headers = {"Authorization":token,"Content-Type": "application/json"}
	return headers


def get_cnn_live_data_for_date(date,network):

	headers = get_headers()
	url = "https://api.developer.nielsen.com/watchapi/national/analytics/api/v1/programRatings?sample=National&startDate={}&endDate={}&startTime=06%3A00&endTime=05%3A59&demographics=Households&originators={}&dataStreams=Live&mediaSources=TVwithDigital&contributions=LinearWithVOD"
	url = url.format(date,date,network)

	r = requests.get(url,headers=headers)
	data = json.loads(r.text)

	clean_data = []

	for row in data:

		clean_row = {
			"name":row['programName'],
			"liveAudience":row['dataStreams'][0]['marketBreaks'][0]['demographicRatings'][0]["usAaProjUnits"]
		}

		clean_data = clean_data + [clean_row]

	return str(clean_data)

@app.route("/")
def hello():
	return "Hello, World!"


@app.route("/data")
def data():

	date = request.args.get('date')
	network = request.args.get('network')

	website_html = '''
	<html>
	<head>
	<script src="https://d3js.org/d3.v4.min.js"></script>
	</head>
	<body>
	<center><div style="height:500px; width:500px" id="viz"></div></center>
	<script>
	data = INSERT_DATA_HERE

	var svg = d3.select("#viz").append("svg")
	  .attr("width", 500)
	  .attr("height", 500)

	barSpace = 2
	barWidth = 10

	svg.selectAll(".bar")
          .data(data)
        .enter().append("rect")
          .attr("class", "bar")
          .attr("height", barWidth)
          .attr("width", function(d) { return d.liveAudience/10000+10; })
          .attr("x", 0)
          .attr("y", function(d,i) { return i*(barWidth+barSpace)+10; })
          .attr("fill","#00AEFF")

    	svg.selectAll(".barText")
          .data(data)
        .enter().append("text")
          .attr("class", "barText")
          .text(function(d) { return d.name; })
          .attr("x", function(d) { return d.liveAudience/10000+15; })
          .attr("y", function(d,i) { return i*(barWidth+barSpace)+10+7; })
          .attr("fill", "black")
          .attr("font-family","sans-serif")
          .attr("font-size","10px")
	</script>
	</body>
	</html>
	'''

	data = get_cnn_live_data_for_date(date,network)
	website_html = website_html.replace("INSERT_DATA_HERE",data)

	return website_html
		