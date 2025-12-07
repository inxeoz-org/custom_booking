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
	new_phone: str | None = None,
	otp_phone: str | None = None,
	new_email: str | None = None,
	otp_email: str | None = None,
	new_email2: str | None = None,
	otp_email2: str | None = None,
):
	devoteee_id = frappe.local.form_dict.get("devoteee_id")

	devoteee = frappe.get_doc("Devoteee", devoteee_id, ignore_permissions=True)

	if new_email and (devoteee.email != new_email):
		if otp_email is None:
			status = send_email_otp(new_email)
			return status["message"]
		else:
			verification_status = verify_email_otp(email=new_email, otp=otp_email)
			if verification_status["VERIFIED"]:
				devoteee.email = new_email
			else:
				return verification_status["message"]

	if new_phone and (devoteee.phone != new_phone):
		if otp_phone is None:
			status = send_sms_otp(new_phone)
			return status["message"]
		else:
			verification_status = verify_sms_otp(phone=new_phone, otp=otp_phone)
			if verification_status["VERIFIED"]:
				devoteee.phone = new_phone
			else:
				return verification_status["message"]

	if new_email2 and (devoteee.email2 != new_email2):
		if otp_email2 is None:
			status = send_email_otp(new_email2)
			return status["message"]
		else:
			verification_status = verify_email_otp(email=new_email2, otp=otp_email2)
			if verification_status["VERIFIED"]:
				devoteee.email2 = new_email2
			else:
				return verification_status["message"]

	devoteee.save(ignore_permissions=True)
	return profile()


@frappe.whitelist(allow_guest=True)
@token_auth("devoteee_id")
def add_companion(companion_name: str, age: int, gender: str, phone: str | None = None):
	devoteee_id = frappe.local.form_dict.get("devoteee_id")
	devoteee_doc = frappe.get_doc("Devoteee", devoteee_id, ignore_permissions=True)
	try:
		child_row = frappe.new_doc("Companion Table")
		child_row.companion_name = companion_name
		child_row.age = age
		child_row.gender = gender
		if phone:
			child_row.phone = phone

		devoteee_doc.companion.append(child_row)

		devoteee_doc.save(ignore_permissions=True)
		return companion()
	except Exception as e:
		frappe.throw(str(e))


@frappe.whitelist(allow_guest=True)
@token_auth("devoteee_id")
def remove_companion(companion_id: str):
	devoteee_id = frappe.local.form_dict.get("devoteee_id")
	devoteee_doc = frappe.get_doc("Devoteee", devoteee_id)

	# find child row by name
	child_row = next((d for d in devoteee_doc.companion if d.name == companion_id), None)

	if not child_row:
		frappe.throw("Companion not found")

	devoteee_doc.remove(child_row)
	devoteee_doc.save(ignore_permissions=True)

	return companion()


@frappe.whitelist(allow_guest=True)
@token_auth("devoteee_id")
def companion():
	devoteee_id = frappe.local.form_dict.get("devoteee_id")
	devoteee = frappe.get_doc("Devoteee", devoteee_id)
	return {"companions": devoteee.companion}
