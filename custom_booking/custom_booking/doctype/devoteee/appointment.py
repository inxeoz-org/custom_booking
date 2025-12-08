import frappe
from frappe.model.document import Document
from typing_extensions import Dict, List

from custom_booking.custom_booking.doctype.api.token.token import token_auth
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
			child_row = frappe.new_doc("Companion Table")
			child_row.companion_name = c.get("companion_name")
			child_row.age = c.get("age")
			child_row.gender = c.get("gender")
			phone = c.get("phone")
			if phone:
				child_row.phone = phone

			new_appointment.companion.append(child_row)

		new_appointment.group_size = len(companion) + 1
		new_appointment.save(ignore_permissions=True)
		return get_appointment_details(new_appointment.name)
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
				"slot": appointment_doc.slot,
				"protocol": appointment_doc.protocol,
				"state": appointment_doc.state,
				"group_size": appointment_doc.group_size,
				"workflow_state": appointment_doc.workflow_state,
				"escort_person": appointment_doc.escort_person,
				"companion": [
					{
						"name": row.name,
						"companion_name": row.companion_name,
						"gender": row.gender,
						"age": row.age,
						"phone": row.phone,
					}
					for row in appointment_doc.companion
				],
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
			fields=["name", "slot_date", "slot", "protocol", "state", "group_size", "workflow_state"],
		)
		return appointments
	except Exception as e:
		frappe.throw(str(e))
