
import frappe
from validation import *
from file_manager import upload
import datetime
from math import radians, cos, sin, asin, sqrt

def strToTimedelta(time):
	if "." in time:
		t = datetime.datetime.strptime(time,"%H:%M:%S.%f")
	else:
		t = datetime.datetime.strptime(time,"%H:%M:%S")
	delta = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
	return delta

def attach(doctype,name,filedata):
	response = {}

	req = frappe.local.form_dict
	if (req == None):
		return {}

	now = frappe.utils.now()
	req.filename = "{}_{}_{}.jpg".format(doctype,name,now)
	req.filedata = filedata
	req.name = name


	try:
		uploaded = upload(doctype,req.name,1)

		response["code"] = 200
		response["data"] = uploaded


	except Exception as e:
		response["code"] = 400
		response["error"] = e.message
	except UnboundLocalError as e:
		response["code"] = 401
		response["error"] = e.message

	return response



def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r