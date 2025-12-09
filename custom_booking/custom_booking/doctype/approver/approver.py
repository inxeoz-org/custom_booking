# Copyright (c) 2025, inxeoz and contributors
# For license information, please see licensd

import frappe
from frappe.model.document import Document
from frappe.model.workflow import apply_workflow

from custom_booking.custom_booking.doctype.attender.attender import get_list_of_available_attenders
from custom_booking.custom_booking.doctype.vip_darshan_appointment.vip_darshan_appointment import (
	attach_appointment_to_slot,
)

from ..api.sms.sms import send_sms_otp, verify_sms_otp
from ..api.token.token import jwt_token, token_auth
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
					return "Failed to get approver"
				return jwt_token({"approver_id": approver_id})
			else:
				return verification_status["message"]

		status = send_sms_otp(phone)
		return status["message"]
	except Exception as e:
		frappe.throw(str(e))
