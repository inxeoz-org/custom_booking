# Copyright (c) 2025, inxeoz and contributors
# For license information, please see licensd

import frappe
from frappe.model.document import Document

from ..api.sms.sms import send_sms_otp, verify_sms_otp
from ..api.token.token import jwt_token
from ..api.validation.validation import valid_otp, valid_phone


class Approver(Document):
	pass


@frappe.whitelist(allow_guest=True)
def approver_login(phone: str, otp: str | None = None):
	try:
		if not valid_phone(phone):
			frappe.throw("Invalid phone number")

		if otp and valid_otp(otp):
			verification_status = verify_sms_otp(phone=phone, otp=otp)
			if verification_status["VERIFIED"]:
				approver_id = frappe.db.get_value("Approver", {"phone": phone}, "name")
				if approver_id is None:
					return "Failed to create approver"
				return jwt_token({"approver_id": approver_id})
			else:
				return verification_status["message"]

		status = send_sms_otp(phone)
		return status["message"]
	except Exception as e:
		frappe.throw(str(e))
