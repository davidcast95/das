
import frappe
from validation import *
from file_manager import upload
import datetime
from math import radians, cos, sin, asin, sqrt

from frappe.utils import cstr
import os
import PIL
from PIL import Image
import base64
from io import BytesIO


def strToTimedelta(time):
	time = str(time)
	if "." in time:
		t = datetime.datetime.strptime(time,"%H:%M:%S.%f")
	else:
		t = datetime.datetime.strptime(time,"%H:%M:%S")
	delta = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
	return delta

def strToDatetime(dateTime):
	dateTime = str(dateTime)
	if "." in dateTime:
		t = datetime.datetime.strptime(dateTime,"%Y-%m-%d %H:%M:%S.%f")
	else:
		t = datetime.datetime.strptime(dateTime,"%Y-%m-%d %H:%M:%S")
	return t

def strToDate(date):
	date = str(date)
	t = datetime.datetime.strptime(date,"%Y-%m-%d")
	return t

def timeDeltaToStr(timedelta):
	seconds = timedelta.total_seconds()
	hours = seconds / 3600
	minutes = (seconds % 3600) / 60
	seconds = seconds % 3600 % 60
	return "{}:{}:{}".format(int(hours),int(minutes),int(seconds))

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


def generate_thumbnail(filename, doctype, name, field):
	# generate thumbnail using Image PIL
	sitename = cstr(frappe.local.site)
	cd = os.getcwd()
	if 'private' not in filename:
		img = Image.open(os.path.join(cd,sitename,'public') + filename)
	else:
		img = Image.open(os.path.join(cd,sitename) + filename)
	basewidth = 600
	wpercent = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
	buffered = BytesIO()
	img.save(buffered,format="JPEG")
	img_str = base64.b64encode(buffered.getvalue())

	
	#upload thumnail image
	req = frappe.local.form_dict
	req.filedata = img_str
	req.name = name
	filename_attr = filename.split('/')
	req.filename = "thumbnail_{}".format(filename_attr[len(filename_attr) - 1])
	
	response = {}
	# try:
	uploaded = upload(doctype, req.name, 1)

	response["code"] = 200
	response["message"] = "Success"
	response["data"] = uploaded

	frappe.db.sql("UPDATE `tab{}` SET {}='{}' WHERE name='{}'".format(doctype, field, uploaded['file_url'], name))

	frappe.db.commit()


	# except Exception as e:
	# 	response["code"] = 400
	# 	response["message"] = e.message
	# 	response["data"] = ""
	# except UnboundLocalError as e:
	# 	response["code"] = 401
	# 	response["message"] = e.message
	# 	response["data"] = ""

	return response