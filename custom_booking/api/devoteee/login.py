import re
import stat
from pickletools import stackslice
from xxlimited import new

import frappe
from frappe.utils import random_string
from typing_extensions import Dict

from ..sms.sms import send_sms_otp, verify_sms_otp
from ..token.token import jwt_token


@frappe.whitelist(allow_guest=True)
def login(name):
	return "You got logged in! " + name


@frappe.whitelist(allow_guest=True)
def devoteee_login_req(phone, otp=None):
	if otp is None:
		status = send_sms_otp(phone)
		return status["message"]
	else:
		verification_status = verify_sms_otp(phone, otp)
		if verification_status["VERIFIED"]:
			devoteee_id = create_customer(phone=phone)
			if devoteee_id is None:
				return "Failed to create customer"
			return jwt_token({"id": devoteee_id})
		else:
			return verification_status["message"]


def create_customer(phone: int | None = None, email: str | None = None, name: str | None = None):
	if phone is None and email is None:
		return None

	exists = None
	if phone:
		exists = frappe.db.exists("Customer", {"custom_phone": phone})
	if exists is None and email:
		exists = frappe.db.exists("Customer", {"custom_email": email})

	if exists:
		customer_doc = frappe.get_doc("Customer", exists)
		return customer_doc.custom_devoteee_id

	# Create new customer doc
	new_customer = frappe.get_doc(
		{
			"doctype": "Customer",
			"customer_name": name or phone or email,
			"customer_type": "Individual",
			"custom_phone": phone or "",
			"custom_email": email or "",
			"custom_devoteee_id": frappe.model.naming.make_autoname("CUST-.###########"),
		}
	)

	new_customer.insert(ignore_permissions=True)
	frappe.db.commit()
	return new_customer.custom_devoteee_id


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

		devoteee_id = create_customer(email=email, name=name)

		return jwt_token({"id": devoteee_id})

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Google Login Failed")
		frappe.throw("Google Login Failed")
