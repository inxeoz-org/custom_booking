# Copyright (c) 2025, inxeoz and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

from ..api.validation.validation import to_frappe_date
from ..vip_darshan_slot.vip_darshan_slot import create_slot


class VipDarshanAppointment(Document):
	pass


@frappe.whitelist(allow_guest=True)
def attach_appointment_to_slot(appointment_id):
	try:
		# Fetch appointment info
		slot, group_size, slot_date = frappe.db.get_value(
			"Vip Darshan Appointment", appointment_id, ["slot", "group_size", "slot_date"]
		)

		# Ensure slot_date exists
		slot_date = create_slot(slot_date)
		slot_date_doc = frappe.get_doc("Vip Darshan Slot", slot_date)

		# --- FIX: Find slot row ---
		slot_row = next((row for row in slot_date_doc.slot_info if row.slot_name == slot), None)

		if not slot_row:
			frappe.throw(f"Slot '{slot}' not found in slot_date {slot_date}")

		# print("info ", "*" * 20, slot, group_size, slot_date, slot_row)
		# Check capacity
		if slot_row.current_capacity >= group_size:
			slot_row.current_capacity -= group_size
			slot_date_doc.append("appointments", {"appointment": appointment_id})
			slot_date_doc.save(ignore_permissions=True)
		else:
			frappe.throw("Slot capacity exceeded")

	except Exception as e:
		frappe.throw(str(e))
