# Copyright (c) 2025, inxeoz and contributors
# For license information, please see licensd

import frappe
from frappe.model.document import Document

from custom_booking.custom_booking.doctype.attender.attender import get_list_of_available_attenders

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


@frappe.whitelist(allow_guest=True)
@token_auth("approver_id")
def approve_vip_appointment(appointment_id: str):
	appointment_doc = frappe.get_doc("Appointment", appointment_id)

	if not appointment_doc:
		frappe.throw("Appointment not found")
	if appointment_doc.status != "Submitted":
		frappe.throw("Appointment is not submitted")

	attender_list = get_list_of_available_attenders(
		slot_date=appointment_doc.slot_date, slot=appointment_doc.slot
	)
	appointment_doc.escort_person = attender_list[0].name
	appointment_doc.status = "Approved"
	appointment_doc.save()

	return "Appointment approved successfully"


@frappe.whitelist(allow_guest=True)
@token_auth("approver_id")
def list_of_vip_appointments(
	escort_person: str | None = None, devoteee_id: str | None = None, workflow_state: str | None = None
):
	filters = {}

	# Add filters only if values exist
	if devoteee_id:
		filters["devoteee_id"] = devoteee_id

	if workflow_state:
		filters["workflow_state"] = workflow_state

	if escort_person:
		filters["escort_person"] = escort_person

	appointments = frappe.get_all(
		"Vip Darshan Appointment",
		filters=filters,
		fields=[
			"name",
			"slot_date",
			"slot",
			"escort_person",
			"group_size",
			"protocol",
			"workflow_state",
		],
		order_by="slot_date, slot",
	)

	return appointments
