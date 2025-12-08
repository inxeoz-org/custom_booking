# Copyright (c) 2025, inxeoz and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.workflow import apply_workflow
from frappe.utils import getdate, nowdate

from ..api.sms.sms import send_sms_otp, verify_sms_otp
from ..api.token.token import jwt_token, token_auth
from ..api.validation.validation import valid_otp, valid_phone


class Attender(Document):
	pass


@frappe.whitelist(allow_guest=True)
def attender_login(phone: str, otp: str | None = None):
	try:
		if not valid_phone(phone):
			frappe.throw("Invalid phone number")

		if otp and valid_otp(otp):
			verification_status = verify_sms_otp(phone=phone, otp=otp)
			if verification_status["VERIFIED"]:
				attender_id = frappe.db.get_value("Attender", {"phone": phone}, "name")
				if attender_id is None:
					return "Failed to get attender"
				return jwt_token({"attender_id": attender_id})
			else:
				return verification_status["message"]

		status = send_sms_otp(phone)
		return status["message"]
	except Exception as e:
		frappe.throw(str(e))


def get_list_of_available_attenders(slot_date: str | None = None, slot: str | None = None):
	## we need to implement using slot_date and slot_name
	return frappe.db.get_list("Attender", ignore_permissions=True)


@frappe.whitelist(allow_guest=True)
@token_auth("attender_id")
def mark_exit(appointment_id: str):
	attender_id = frappe.local.form_dict["attender_id"]
	frappe.set_user("attender@example.com")
	try:
		appointment_doc = frappe.get_doc("Vip Darshan Appointment", appointment_id)
		if appointment_doc.escort_person != attender_id:
			frappe.throw("Unauthorized Attender")

		today = getdate(nowdate())
		slot_date = getdate(appointment_doc.slot_date)

		if slot_date > today:
			frappe.throw("Appointment not yet started")

		apply_workflow(appointment_doc, "Mark Exit")
		return get_attender_appointment_details(appointment_id)
	except Exception as e:
		frappe.throw(str(e))
	finally:
		frappe.set_user("Guest")


@frappe.whitelist(allow_guest=True)
@token_auth("attender_id")
def get_attender_appointment_details(appointment_id: str):
	attender_id = frappe.local.form_dict["attender_id"]
	frappe.set_user("attender@example.com")
	try:
		appointment_doc = frappe.get_doc("Vip Darshan Appointment", appointment_id)
		if appointment_doc.escort_person != attender_id:
			frappe.throw("Unauthorized Attender")

		devoteee_doc = frappe.get_doc("Devotee", appointment_doc.devoteee_id)

		return {
			"devoteee_name": devoteee_doc.devoteee_name,
			"devoteee_phone": devoteee_doc.phone,
			"devoteee_gender": devoteee_doc.gender,
			"devoteee_id": appointment_doc.devoteee_id,
			"group_size": appointment_doc.group_size,
			"slot_date": appointment_doc.slot_date,
			"slot": appointment_doc.slot,
			"status": appointment_doc.status,
			"companion": appointment_doc.companion,
		}
	except Exception as e:
		frappe.throw(str(e))
	finally:
		frappe.set_user("Guest")


@frappe.whitelist(allow_guest=True)
@token_auth("attender_id")
def get_attender_appointment_list(
	devoteee_id: str | None = None,
	status: str | None = None,
	slot_date: str | None = None,
	slot: str | None = None,
	protocol: str | None = None,
	state: str | None = None,
):
	try:
		filter = {}
		attender_id = frappe.local.form_dict["attender_id"]
		filter["escort_person"] = attender_id
		if status:
			filter["workflow_state"] = status
		elif state:
			filter["state"] = state
		elif protocol:
			filter["protocol"] = protocol
		elif slot_date:
			filter["slot_date"] = slot_date
		elif slot:
			filter["slot"] = slot
		elif devoteee_id:
			filter["devoteee_id"] = devoteee_id

		return frappe.get_all(
			"Vip Darshan Appointment",
			filters=filter,
			fields=["name", "slot", "protocol", "state", "workflow_state", "group_size"],
		)
	except Exception as e:
		frappe.throw(str(e))
