import frappe
from frappe.model.document import Document
from typing_extensions import Dict, List

from custom_booking.custom_booking.doctype.api.token.token import token_auth
from custom_booking.custom_booking.doctype.api.validation.validation import to_frappe_date
from custom_booking.custom_booking.doctype.vip_darshan_slot.vip_darshan_slot import create_slot


@frappe.whitelist(allow_guest=True)
@token_auth("devoteee_id")
def create_appointment(slot, slot_date, protocol, state, companion: List):
	try:
		devoteee_id = frappe.local.form_dict["devoteee_id"]
		new_appointment = frappe.new_doc("Vip Darshan Appointment")
		new_appointment.devoteee_id = devoteee_id
		new_appointment.slot = slot
		slot_date = create_slot(slot_date)
		new_appointment.slot_date = slot_date
		new_appointment.protocol = protocol
		new_appointment.state = state

		for c in companion:
			print("companion ", c["companion_name"])
			print("age ", c["age"])
			print("gender ", c["gender"])
			print("phone ", c["phone"])

			child_row = frappe.new_doc("Companion Table")
			child_row.companion_name = c["companion_name"]
			child_row.age = c["age"]
			child_row.gender = c["gender"]
			child_row.phone = c["phone"]

			new_appointment.companion.append(child_row)

		new_appointment.group_size = len(companion) + 1
		new_appointment.save(ignore_permissions=True)
		return new_appointment.name
	except Exception as e:
		frappe.throw(str(e))


@frappe.whitelist(allow_guest=True)
@token_auth("devoteee_id")
def submit_appointment(appointment_id):
	devoteee_id = frappe.local.form_dict["devoteee_id"]
	frappe.set_user("devoteee@example.com")
	try:
		appointment_doc = frappe.get_doc("Vip Darshan Appointment", appointment_id)

		if appointment_doc.devoteee_id != devoteee_id:
			frappe.throw("Unauthorized access")
		if appointment_doc.workflow_state != "Draft":
			frappe.throw("Appointment is not in draft state")
		appointment_doc.submit()
		return get_appointment_details(appointment_id)

	except Exception as e:
		frappe.throw(str(e))

	finally:
		frappe.set_user("Guest")


@frappe.whitelist(allow_guest=True)
@token_auth("devoteee_id")
def get_appointment_details(appointment_id):
	devoteee_id = frappe.local.form_dict["devoteee_id"]
	try:
		appointment_doc = frappe.get_doc("Vip Darshan Appointment", appointment_id)
		if appointment_doc.devoteee_id == devoteee_id:
			return {
				"name": appointment_doc.name,
				"slot_date": appointment_doc.slot_date,
				"protocol": appointment_doc.protocol,
				"state": appointment_doc.state,
				"group_size": appointment_doc.group_size,
				"status": appointment_doc.workflow_state,
				"companion": [child.as_dict() for child in appointment_doc.companion],
			}

	except Exception as e:
		frappe.throw(str(e))


@frappe.whitelist(allow_guest=True)
@token_auth("devoteee_id")
def get_appointment_list():
	devoteee_id = frappe.local.form_dict["devoteee_id"]
	try:
		appointments = frappe.get_all(
			"Vip Darshan Appointment",
			filters={"devoteee_id": devoteee_id},
			fields=["name", "slot_date", "protocol", "state", "group_size", "workflow_state"],
		)
		return appointments
	except Exception as e:
		frappe.throw(str(e))
