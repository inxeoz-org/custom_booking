import re

import frappe
from dateutil import parser
from typing_extensions import Dict

# def to_frappe_date(date_str, format="%Y-%m-%d"):
# 	"""Convert ANY date format to YYYY-MM-DD (Frappe standard)."""
# 	try:
# 		print("*" * 20, date_str)
# 		parsed = parser.parse(date_str, dayfirst=True)  # handles most formats

# 		print("Converted to", parsed.strftime(format))
# 		return parsed.strftime(format)
# 	except Exception as e:
# 		frappe.throw(str(e))


# as frappe originally uses data type for phone number
def valid_phone(phone: str):
	return re.match(r"^\d{10}$", phone)


def valid_email(email: str):
	return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)


def valid_name(name: str):
	return re.match(r"^[a-zA-Z\s]+$", name)


def valid_aadhar(aadhar: str):
	return re.match(r"^\d{12}$", str(aadhar))


def valid_gender(gender: str):
	return gender.lower() in ["male", "female", "other"]


def valid_dob(dob: str):
	return re.match(r"^\d{2}-\d{2}-\d{4}$", dob)


def valid_location(location: str):
	return re.match(r"^[a-zA-Z\s]+$", location)


def valid_date(date: str):
	return re.match(r"^\d{2}-\d{2}-\d{4}$", date)


def valid_24hrtime(time: str):
	return re.match(r"^\d{2}:\d{2}$", time)


def valid_12hrtime(time: str):
	return re.match(r"^\d{1,2}:\d{2} [APap][Mm]$", time)


def valid_otp(otp: str):
	return len(f"{otp}") == 6


def validate_companion(companion: Dict):
	for key, value in companion.items():
		if key == "companion_name":
			if not valid_name(value):
				frappe.throw("Invalid name")
		elif key == "email":
			if not valid_email(value):
				frappe.throw("Invalid email")
		elif key == "phone":
			if not valid_phone(value):
				frappe.throw("Invalid phone number")
		elif key == "gender":
			if not valid_gender(value):
				frappe.throw("Invalid gender")
		elif key == "dob":
			if not valid_dob(value):
				frappe.throw("Invalid date of birth")
		elif key == "location":
			if not valid_location(value):
				frappe.throw("Invalid location")
