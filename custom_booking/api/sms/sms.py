import random
from datetime import datetime

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

	return {"otp_sent": True, "message": otp}  # testing


def verify_sms_otp(phone, otp):
	saved_otp = frappe.cache().get_value(f"otp_{phone}")

	if not saved_otp:
		return {"VERIFIED": False, "message": "OTP expired"}

	if otp != saved_otp:
		return {"VERIFIED": False, "message": "Invalid OTP"}

	if otp == saved_otp:
		frappe.cache().delete_value(f"otp_{phone}")
		return {"VERIFIED": True, "message": "OTP VERIFIED"}

	return {"VERIFIED": False, "message": "Invalid OTP"}


def send_email_otp(email):
	otp = str(random.randint(100000, 999999))
	# store OTP
	frappe.cache().set_value(f"otp_{email}", otp, expires_in_sec=180)
	print("#" * 30, "\n", otp, "\n", "#" * 30)
	# # Email API CALL (example)
	# email_api_url = "https://YOUR_EMAIL_GATEWAY/send"
	# requests.get(email_api_url, params={
	#     "apikey": "YOUR_KEY",
	#     "email": email,
	#     "subject": "OTP Verification",
	#     "body": f"Your OTP is {otp}"
	# })

	return {"otp_sent": True, "message": otp}  # testing


def verify_email_otp(email, otp):
	saved_otp = frappe.cache().get_value(f"otp_{email}")

	if not saved_otp:
		return {"VERIFIED": False, "message": "OTP expired"}

	if otp != saved_otp:
		return {"VERIFIED": False, "message": "Invalid OTP"}

	if otp == saved_otp:
		frappe.cache().delete_value(f"otp_{email}")
		return {"VERIFIED": True, "message": "OTP VERIFIED"}

	return {"VERIFIED": False, "message": "Invalid OTP"}
