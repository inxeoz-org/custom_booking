from typing import Dict

import frappe
from frappe.utils import random_string

from ..api.sms.sms import send_email_otp, send_sms_otp, verify_email_otp, verify_sms_otp
from ..api.token.token import token_auth


@frappe.whitelist(allow_guest=True)
@token_auth("approver_id")
def profile():
	approver_id = frappe.local.form_dict["approver_id"]

	approver_doc = frappe.get_doc("Approver", approver_id, ignore_permissions=True)

	return {
		"approver_name": approver_doc.approver_name,
		"email": approver_doc.email,
		"gender": approver_doc.gender,
		"dob": approver_doc.dob,
		"aadhar": approver_doc.aadhar,
		"location": approver_doc.location,
		"phone": approver_doc.phone,
	}


@frappe.whitelist(allow_guest=True)
@token_auth("approver_id")
def update_profile(
	approver_name: str | None = None,
	gender: str | None = None,
	dob: str | None = None,
	aadhar: str | None = None,
	location: str | None = None,
):
	try:
		approver_id = frappe.local.form_dict.get("approver_id")

		approver_doc = frappe.get_doc("Approver", approver_id, ignore_permissions=True)

		if approver_name:
			approver_doc.approver_name = approver_name.lower()
		if gender:
			approver_doc.gender = gender.lower()
		if dob:
			approver_doc.dob = dob
		if aadhar:
			approver_doc.aadhar = aadhar
		if location:
			approver_doc.location = location.lower()

		approver_doc.save(ignore_permissions=True)
		return profile()
	except Exception as e:
		frappe.throw(str(e))


@frappe.whitelist(allow_guest=True)
@token_auth("approver_id")
def update_cred(
	phone: str | None = None,
	otp_phone: str | None = None,
	email: str | None = None,
	otp_email: str | None = None,
	email2: str | None = None,
	otp_email2: str | None = None,
):
	approver_id = frappe.local.form_dict.get("approver_id")

	approver_doc = frappe.get_doc("Approver", approver_id, ignore_permissions=True)

	if email and (approver_doc.email != email):
		if otp_email is None:
			status = send_email_otp(email)
			return status["message"]
		else:
			verification_status = verify_email_otp(email=email, otp=otp_email)
			if verification_status["VERIFIED"]:
				approver_doc.email = email
			else:
				return verification_status["message"]

	if phone and (approver_doc.phone != phone):
		if otp_phone is None:
			status = send_sms_otp(phone)
			return status["message"]
		else:
			verification_status = verify_sms_otp(phone=phone, otp=otp_phone)
			if verification_status["VERIFIED"]:
				approver_doc.phone = phone
			else:
				return verification_status["message"]

	if email2 and (approver_doc.email2 != email2):
		if otp_email2 is None:
			status = send_email_otp(email2)
			return status["message"]
		else:
			verification_status = verify_email_otp(email=email2, otp=otp_email2)
			if verification_status["VERIFIED"]:
				approver_doc.email2 = email2
			else:
				return verification_status["message"]

	approver_doc.save(ignore_permissions=True)
	return profile()
