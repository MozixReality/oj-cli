import json
import os
from getpass import getpass

from constants import COOKIES_DIR
from constants import ASSIGNMENT_MAPPING_PATH
from util.common import get_csrf_token
from util.curl import curl
from util.colors import cyan_wrapper

def update_map():
	endpoint = "contests?offset=0&limit=10&status=0"
	inputstr = '{'
	result = json.loads(curl("get", endpoint=endpoint, use_x_csrf_token=True))
	counter = 1
	for i in range(0,len(result['data']['results'])):
		contestid = result['data']['results'][i]['id']
		payload = {
				"contest_id" : str(contestid)
				}
		endpoint = "contest/problem?contest_id=" + str(contestid)
		result2 = json.loads(curl("get", payload=payload, endpoint=endpoint, use_x_csrf_token=True))
		if result2["error"] == "error":
			print("Error : " + result2["data"])
			continue
		q_string3 = result['data']['results'][i]["title"]
		q_string2 = ""
		for q1 in q_string3.split(" "):
			try:
				q_string2 += q1.encode("ascii") + " "
			except:
				q_string2 += "XX "
		q_string = result2['data'][0]['_id']
		_pid = q_string.split()[0] + "+" + q_string.split()[1]
		print("Found HomeWork: " + cyan_wrapper("hw" + str(counter) + " [" + q_string2 + "]"))
		if counter != 1:
			inputstr += ','
		inputstr += '"hw' + str(counter)+'":{"contest_name":"' + str(q_string2) + '","contest_id":' + str(contestid) + ',"contest_problem_id":"' + str(_pid)+ '","problem_id":' + str(result2["data"][0]["id"]) + '}'
		counter += 1
	inputstr += '}'
	f = open(ASSIGNMENT_MAPPING_PATH,'w')
	f.write(inputstr.encode("utf-8"))
	f.close
	print("Updated successfully!")
