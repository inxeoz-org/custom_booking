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


from frappe.model.workflow import apply_workflow


@frappe.whitelist(allow_guest=True)
@token_auth("approver_id")
def approve_vip_appointment(appointment_id: str):
	# ✅ Switch to a real system user with permission
	frappe.set_user("Approver")

	try:
		appointment_doc = frappe.get_doc("Vip Darshan Appointment", appointment_id, ignore_permissions=True)

		if not appointment_doc:
			frappe.throw("Vip Darshan Appointment not found")

		if appointment_doc.workflow_state == "Approved":
			frappe.throw("Vip Darshan Appointment already approved")

		attender_list = get_list_of_available_attenders(
			slot_date=appointment_doc.slot_date, slot=appointment_doc.slot
		)

		if not attender_list:
			frappe.throw("No available attenders")

		appointment_doc.escort_person = attender_list[0].name
		appointment_doc.save(ignore_permissions=True)

		# ✅ THIS is the only valid way to change workflow state
		apply_workflow(appointment_doc, "Approve")

		return appointment_doc

	except Exception:
		frappe.log_error(frappe.get_traceback(), "VIP Approval Failed")
		raise

	finally:
		# ✅ Always restore Guest user
		frappe.set_user("Guest")


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
