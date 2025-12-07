from typing import Dict

import frappe
from frappe.utils import random_string

from ..api.sms.sms import send_email_otp, send_sms_otp, verify_email_otp, verify_sms_otp
from ..api.token.token import token_auth
from ..api.validation.validation import to_frappe_date


@frappe.whitelist(allow_guest=True)
@token_auth("devoteee_id")
def profile():
	devoteee_id = frappe.local.form_dict["devoteee_id"]

	devoteee = frappe.get_doc("Devoteee", devoteee_id, ignore_permissions=True)

	return {
		"devoteee_name": devoteee.devoteee_name,
		"email": devoteee.email,
		"gender": devoteee.gender,
		"dob": devoteee.dob,
		"aadhar": devoteee.aadhar,
		"location": devoteee.location,
		"companion": devoteee.companion,
		"phone": devoteee.phone,
	}


@frappe.whitelist(allow_guest=True)
@token_auth("devoteee_id")
def update_profile(
	devoteee_name: str | None = None,
	gender: str | None = None,
	dob: str | None = None,
	aadhar: str | None = None,
	location: str | None = None,
):
	try:
		devoteee_id = frappe.local.form_dict.get("devoteee_id")

		devoteee = frappe.get_doc("Devoteee", devoteee_id, ignore_permissions=True)

		if devoteee_name:
			devoteee.devoteee_name = devoteee_name.lower()
		if gender:
			devoteee.gender = gender.lower()
		if dob:
			devoteee.dob = to_frappe_date(dob)
		if aadhar:
			devoteee.aadhar = aadhar
		if location:
			devoteee.location = location.lower()

		devoteee.save(ignore_permissions=True)
		return profile()
	except Exception as e:
		frappe.throw(str(e))


@frappe.whitelist(allow_guest=True)
@token_auth("devoteee_id")
def update_cred(
	phone: str | None = None,
	otp_phone: str | None = None,
	email: str | None = None,
	otp_email: str | None = None,
	email2: str | None = None,
	otp_email2: str | None = None,
):
	devoteee_id = frappe.local.form_dict.get("devoteee_id")

	devoteee = frappe.get_doc("Devoteee", devoteee_id, ignore_permissions=True)

	if email and (devoteee.email != email):
		if otp_email is None:
			status = send_email_otp(email)
			return status["message"]
		else:
			verification_status = verify_email_otp(email=email, otp=otp_email)
			if verification_status["VERIFIED"]:
				devoteee.email = email
			else:
				return verification_status["message"]

	if phone and (devoteee.phone != phone):
		if otp_phone is None:
			status = send_sms_otp(phone)
			return status["message"]
		else:
			verification_status = verify_sms_otp(phone=phone, otp=otp_phone)
			if verification_status["VERIFIED"]:
				devoteee.phone = phone
			else:
				return verification_status["message"]

	if email2 and (devoteee.email2 != email2):
		if otp_email2 is None:
			status = send_email_otp(email2)
			return status["message"]
		else:
			verification_status = verify_email_otp(email=email2, otp=otp_email2)
			if verification_status["VERIFIED"]:
				devoteee.email2 = email2
			else:
				return verification_status["message"]

	devoteee.save(ignore_permissions=True)
	return profile()


@frappe.whitelist(allow_guest=True)
@token_auth("devoteee_id")
def add_companion(
	companion_name: str, companion_age: int, companion_gender: str, companion_phone: str | None = None
):
	devoteee_id = frappe.local.form_dict.get("devoteee_id")
	devoteee_doc = frappe.get_doc("Devoteee", devoteee_id, ignore_permissions=True)
	try:
		devoteee_doc.companions.append(
			{
				"companion_name": companion_name,
				"age": companion_age,
				"gender": companion_gender,
				"phone": companion_phone,
			}
		)
		devoteee_doc.save(ignore_permissions=True)
		return companion(devoteee_id)
	except Exception as e:
		frappe.throw(str(e))


def companion(devoteee_id: str):
	devoteee = frappe.get_doc("Devoteee", devoteee_id)
	return {"companion": devoteee.companion}
