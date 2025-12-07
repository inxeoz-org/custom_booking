# Copyright (c) 2025, inxeoz and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
from frappe.utils import random_string
from typing_extensions import Dict

from ..api.sms.sms import send_sms_otp, verify_sms_otp
from ..api.token.token import jwt_token
from ..api.validation.validation import valid_otp, valid_phone


class Devoteee(Document):
	pass


@frappe.whitelist(allow_guest=True)
def devoteee_login(phone: str, otp: str | None = None):
	if not valid_phone(phone):
		frappe.throw("Invalid phone number")

	if otp and valid_otp(otp):
		verification_status = verify_sms_otp(phone=phone, otp=otp)
		if verification_status["VERIFIED"]:
			devoteee_id = create_devoteee(phone=phone)
			if devoteee_id is None:
				return "Failed to create devoteee"
			return jwt_token({"devoteee_id": devoteee_id})
		else:
			return verification_status["message"]

	status = send_sms_otp(phone)
	return status["message"]


def create_devoteee(
	phone: str | None = None,
	email: str | None = None,
	devoteee_name: str | None = None,
	is_companion: bool = False,
):
	if phone is None and email is None and not is_companion:
		return None

	exists = None
	if phone:
		exists = frappe.db.exists("Devoteee", {"phone": phone})
	if exists is None and email:
		exists = frappe.db.exists("Devoteee", {"email": email})

	if exists:
		devoteee_doc = frappe.get_doc("Devoteee", exists)
		return devoteee_doc.name

	# Create new customer doc
	new_devoteee = frappe.get_doc(
		{
			"doctype": "Devoteee",
			"devoteee_name": devoteee_name or email or f"{phone}",
			"phone": phone,
			"email": email,
			"is_companion": is_companion,
			"docstatus": 1,
		}
	)

	new_devoteee.insert(ignore_permissions=True)
	frappe.db.commit()
	return new_devoteee.name


import frappe
from google.auth.transport import requests
from google.oauth2 import id_token


@frappe.whitelist(allow_guest=True)
def google_login(token):
	try:
		# Verify ID token
		idinfo = id_token.verify_oauth2_token(
			token,
			requests.Request(),
			"877753772904-78b39tu876jt75f2he4t7nluuvlk7fi8.apps.googleusercontent.com",
		)

		email = idinfo["email"]
		name = idinfo.get("name")

		devoteee_id = create_devoteee(email=email, devoteee_name=name)

		return jwt_token({"devoteee_id": devoteee_id})

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Google Login Failed")
		frappe.throw("Google Login Failed")
