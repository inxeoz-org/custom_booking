# Copyright (c) 2025, inxeoz and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from typing_extensions import Dict, List

from custom_booking.custom_booking.doctype.api.token.token import token_auth
from custom_booking.custom_booking.doctype.api.validation.validation import to_frappe_date


class VipDarshanAppointment(Document):
	pass


@frappe.whitelist(allow_guest=True)
@token_auth("devoteee_id")
def create_appointment(slot, slot_date, protocol, state, companion: List):
	try:
		devoteee_id = frappe.local.form_dict["devoteee_id"]
		new_appointment = frappe.new_doc("Vip Darshan Appointment")
		new_appointment.devoteee = devoteee_id
		new_appointment.slot = slot
		new_appointment.slot_date = to_frappe_date(slot_date)
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
