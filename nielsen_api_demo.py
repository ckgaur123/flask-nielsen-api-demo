import requests
import json

def get_headers():
	with open("authorizations/nielsen-api-token.txt") as f:
		token = f.read()
	headers = {"Authorization":token,"Content-Type": "application/json"}
	return headers

def get_template():
	with open("template.html") as f:
		template = f.read()
	return template

def get_live_data_for_date_and_network(date,network):

	headers = get_headers()

	base_url = "https://api.developer.nielsen.com/watchapi/national/analytics/api/v1/programRatings?"
	sample_p = "sample=National"
	date_p = "startDate={}&endDate={}".format(date,date)
	time_p = "startTime=06%3A00&endTime=05%3A59"
	demo_p = "demographics=Households"
	network_p = "originators={}".format(network)
	timeshift_p = "dataStreams=Live"
	misc_p = "mediaSources=TVwithDigital&contributions=LinearWithVOD"
	url = "&".join([base_url,sample_p,date_p,time_p,demo_p,network_p,timeshift_p,misc_p])

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