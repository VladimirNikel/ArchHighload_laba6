import json
import datetime
import hashlib

def check_value_hash(check_login: str, check_hash: str):
	current_date_utc	= datetime.datetime.utcnow().strftime("%Y.%m.%d_%H:%M:%S")
	try_login			= "Nikel"
	try_password		= "Qwerty12345"	
	input_value			= try_login+current_date_utc+try_password
	calculate_hash		= str(hashlib.sha256(input_value.encode()).hexdigest())

	if(check_login==try_login and check_hash==calculate_hash):
		return json.dumps({"login": check_login, "result": "true"})
	else:
		return json.dumps({"login": check_login, "result": "false"})