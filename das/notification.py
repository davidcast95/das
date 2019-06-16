import frappe
from frappe.utils import get_request_session
import json

def send_notification(auth_key,data):
	try:
		s = get_request_session()
		url = "https://fcm.googleapis.com/fcm/send"	
		header = {"Authorization": "key={}".format(auth_key),"Content-Type": "application/json"}
		content = {
			"to":"/topics/all",
			"data":data
		}
		res = s.post(url=url,headers=header,data=json.dumps(content))
		return res
	except:
		return "Error"

def send_notification(user,auth_key,data):
	try:
		s = get_request_session()
		url = "https://fcm.googleapis.com/fcm/send"

		user = frappe.get_doc("User",user)
		
		if (len(user.social_logins) > 0):
			frappe_userid = user.social_logins[0].userid

			header = {"Authorization": "key={}".format(auth_key),"Content-Type": "application/json"}
			content = {
				"to":"/topics/{}".format(frappe_userid),
				"data":data
			}
			res = s.post(url=url,headers=header,data=json.dumps(content))
			return res
	except:
		return "Error"


def send_notification_by_mobile_no(mobile_no,auth_key,data):
	try:
		s = get_request_session()
		url = "https://fcm.googleapis.com/fcm/send"
		
		header = {"Authorization": "key={}".format(auth_key),"Content-Type": "application/json"}
		content = {
			"to":"/topics/{}".format(mobile_no),
			"data":data
		}
		res = s.post(url=url,headers=header,data=json.dumps(content))
	except:
		return "Error"
