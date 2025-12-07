# Copyright (c) 2025, inxeoz and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

from ..api.validation.validation import to_frappe_date
from ..vip_darshan_slot.vip_darshan_slot import create_slot


class VipDarshanAppointment(Document):
	pass


def attach_appointment_to_slot(slot_date, appointment_id):
	slot = frappe.db.get_value("Vip Darshan Appointment", {"name": appointment_id}, "slot")
	group_size = frappe.db.get_value("Vip Darshan Appointment", {"name": appointment_id}, "group_size")

	slot_date_doc = create_slot(slot_date)
	current_slot_capacity = slot_date_doc.slot_info[slot].capacity

	if current_slot_capacity >= group_size:
		slot_date_doc.slot_info[slot].capacity -= group_size
		slot_date_doc.append("appointments", {"appointment": appointment_id})
		slot_date_doc.save(ignore_permissions=True)
	else:
		frappe.throw("Slot capacity exceeded")
