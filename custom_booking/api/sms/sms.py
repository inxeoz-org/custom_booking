import random

import frappe
import requests
from frappe.utils import random_string
from typing_extensions import Dict

from ..token.token import jwt_token


def send_sms_otp(phone):
	otp = str(random.randint(100000, 999999))
	# store OTP
	frappe.cache().set_value(f"otp_{phone}", otp, expires_in_sec=180)
	print("#" * 30, "\n", otp, "\n", "#" * 30)

	# # SMS API CALL (example)
	# sms_api_url = "https://YOUR_SMS_GATEWAY/send"
	# requests.get(sms_api_url, params={
	#     "apikey": "YOUR_KEY",
	#     "number": phone,
	#     "message": f"Your OTP is {otp}"
	# })

	return {"otp_sent": True, "message": "OTP sent"}


def verify_sms_otp(phone, otp):
	saved_otp = frappe.cache().get_value(f"otp_{phone}")

	if not saved_otp:
		return {"verified": False, "message": "OTP expired"}

	if otp != saved_otp:
		return {"verified": False, "message": "Invalid OTP"}

	if otp == saved_otp:
		frappe.cache().delete_value(f"otp_{phone}")
		return {"verified": True, "message": "OTP verified"}

	return {"verified": False, "message": "Invalid OTP"}
