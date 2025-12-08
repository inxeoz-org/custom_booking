from typing import Dict

import frappe
from frappe.utils import random_string

from ..api.sms.sms import send_email_otp, send_sms_otp, verify_email_otp, verify_sms_otp
from ..api.token.token import token_auth


@frappe.whitelist(allow_guest=True)
@token_auth("attender_id")
def profile():
	attender_id = frappe.local.form_dict["attender_id"]

	attender_doc = frappe.get_doc("Attender", attender_id, ignore_permissions=True)

	return {
		"attender_name": attender_doc.attender_name,
		"email": attender_doc.email,
		"gender": attender_doc.gender,
		"dob": attender_doc.dob,
		"aadhar": attender_doc.aadhar,
		"location": attender_doc.location,
		"phone": attender_doc.phone,
	}


@frappe.whitelist(allow_guest=True)
@token_auth("attender_id")
def update_profile(
	attender_name: str | None = None,
	gender: str | None = None,
	dob: str | None = None,
	aadhar: str | None = None,
	location: str | None = None,
):
	try:
		attender_id = frappe.local.form_dict.get("attender_id")

		attender_doc = frappe.get_doc("Attender", attender_id, ignore_permissions=True)

		if attender_name:
			attender_doc.attender_name = attender_name.lower()
		if gender:
			attender_doc.gender = gender.lower()
		if dob:
			attender_doc.dob = dob
		if aadhar:
			attender_doc.aadhar = aadhar
		if location:
			attender_doc.location = location.lower()

		attender_doc.save(ignore_permissions=True)
		return profile()
	except Exception as e:
		frappe.throw(str(e))


@frappe.whitelist(allow_guest=True)
@token_auth("attender_id")
def update_cred(
	phone: str | None = None,
	otp_phone: str | None = None,
	email: str | None = None,
	otp_email: str | None = None,
	email2: str | None = None,
	otp_email2: str | None = None,
):
	attender_id = frappe.local.form_dict.get("attender_id")

	attender_doc = frappe.get_doc("Attender", attender_id, ignore_permissions=True)

	if email and (attender_doc.email != email):
		if otp_email is None:
			status = send_email_otp(email)
			return status["message"]
		else:
			verification_status = verify_email_otp(email=email, otp=otp_email)
			if verification_status["VERIFIED"]:
				attender_doc.email = email
			else:
				return verification_status["message"]

	if phone and (attender_doc.phone != phone):
		if otp_phone is None:
			status = send_sms_otp(phone)
			return status["message"]
		else:
			verification_status = verify_sms_otp(phone=phone, otp=otp_phone)
			if verification_status["VERIFIED"]:
				attender_doc.phone = phone
			else:
				return verification_status["message"]

	if email2 and (attender_doc.email2 != email2):
		if otp_email2 is None:
			status = send_email_otp(email2)
			return status["message"]
		else:
			verification_status = verify_email_otp(email=email2, otp=otp_email2)
			if verification_status["VERIFIED"]:
				attender_doc.email2 = email2
			else:
				return verification_status["message"]

	attender_doc.save(ignore_permissions=True)
	return profile()
